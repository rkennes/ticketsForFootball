from src.database import database
from databases.interfaces import Record
from fastapi import HTTPException, status
from src.models.sector import sector
from src.schemas.sector import sectorIn
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import func,select

class SectorService: 
   
    @staticmethod
    def get_created_at(created_at: datetime):
        return created_at or datetime.now()
    
    async def read_sectors(self, cnpj_param: str, limit: int, skip: int = 0) -> list[Record]:
        query = sector.select().where(
            sector.c.cnpj == cnpj_param).limit(limit).offset(skip)
        return await database.fetch_all(query) 
        
    async def create_sector(self, data:sectorIn) -> Record:  
        query = select(func.max(sector.c.sector_id)).where(sector.c.cnpj == data.cnpj)
        last_id = await database.fetch_val(query) or 0
        next_id = last_id + 1
        
        command = sector.insert().values(
            cnpj=data.cnpj,
            sector_id = next_id,
            name=data.name,  
		    created_at=self.get_created_at(data.created_at), 
        ) 
        
        await database.execute(command) 
        return {"message": "Sector created."}
        
    async def delete_sector(self, cnpj_param: str, sector_id:int) -> Record:
        sector_record = await self.__get_sector(cnpj_param, sector_id)  

        if not sector_record:
            return
        
        delete_sector = sector.delete().where(
            (sector.c.cnpj == cnpj_param) & 
            (sector.c.sector_id == sector_id)
            )
        await database.execute(delete_sector)

        return {"message": "Sector removed."}
    
    async def update_sector(self, sector_id:int, data:sectorIn) -> Record:
        sector_record = await self.__get_sector(data.cnpj, sector_id)  

        if not sector_record:
            return
        
        sector_record = sector.update().where(
             (sector.c.cnpj == data.cnpj) & 
             (sector.c.sector_id == sector_id)
             ).values(
            name=data.name
        )
        
        await database.execute(sector_record)

        return {"message": "Sector updated."}
    
        
    async def __get_sector(self, cnpj:str, sector_id:int) -> Record: 
        query = sector.select().where(
            (sector.c.cnpj == cnpj) & 
            (sector.c.sector_id == sector_id)) 
        
        result = await database.fetch_one(query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sector not found.")
        
        return result