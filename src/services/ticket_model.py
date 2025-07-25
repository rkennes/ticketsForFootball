from src.database import database
from databases.interfaces import Record
from fastapi import HTTPException, status
from src.models.ticket_model import ticket_model
from src.schemas.ticket_model import TicketModelIn
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import func,select
from src.services.sector import SectorService
from collections import defaultdict
from src.models.ticket_model import ticket_model, ticket_model_sector

class TicketModelService: 
   
    @staticmethod
    def get_created_at(created_at: datetime):
        return created_at or datetime.now()
    
    async def read_ticketModel(self, cnpj_param: str, limit: int, skip: int = 0) -> list[dict]:
        query = (
            select(
                ticket_model.c.ticket_model_id,
                ticket_model.c.cnpj,
                ticket_model.c.name,
                ticket_model.c.created_at,
                ticket_model_sector.c.sector_id,
                ticket_model_sector.c.price,
                ticket_model_sector.c.ticket_load
            )
            .select_from(
                ticket_model.join(
                    ticket_model_sector,
                    (ticket_model.c.ticket_model_id == ticket_model_sector.c.ticket_model_id) &
                    (ticket_model.c.cnpj == ticket_model_sector.c.cnpj)
                )
            )
            .where(ticket_model.c.cnpj == cnpj_param)
            .limit(limit)
            .offset(skip)
        )

        rows = await database.fetch_all(query)

        # Agrupar os setores por modelo
        grouped: dict[int, dict] = defaultdict(lambda: {"sectors": []})

        for row in rows:            
            tm_id = row.ticket_model_id

            if "ticket_model_id" not in grouped[tm_id]:
                grouped[tm_id].update({
                    "ticket_model_id": tm_id,
                    "cnpj": row.cnpj,
                    "name": row.name,
                    "created_at": row.created_at,
                })

            grouped[tm_id]["sectors"].append({
                "sector_id": row.sector_id,
                "price": row.price,
                "ticket_load": row.ticket_load
            })

        return list(grouped.values()) 
        
    async def create_ticketModel(self, data: TicketModelIn) -> dict:
        # Validação dos setores
        for sector_data in data.sectors:
            await SectorService._get_sector(data.cnpj, sector_data.sector_id)

        # Geração do próximo ID
        query = select(func.max(ticket_model.c.ticket_model_id)).where(
            ticket_model.c.cnpj == data.cnpj
        )
        last_id = await database.fetch_val(query) or 0
        next_id = last_id + 1

        # Inserir no ticket_model
        await database.execute(
            ticket_model.insert().values(
                cnpj=data.cnpj,
                ticket_model_id=next_id,
                name=data.name,
                created_at=self.get_created_at(data.created_at),
            )
        )

        # Inserir os setores relacionados no ticket_model_sector
        for sector_data in data.sectors:
            await database.execute(
                ticket_model_sector.insert().values(
                    cnpj=data.cnpj,
                    ticket_model_id=next_id,
                    sector_id=sector_data.sector_id,
                    price=sector_data.price,
                    ticket_load=sector_data.ticket_load
                )
            )

        return {"message": "Ticket model created.", "ticket_model_id": next_id}
    
    async def delete_ticket_model(self, cnpj: str, ticket_model_id: int) -> dict:
        validate_model = await self._validate_model(cnpj, ticket_model_id)
        if not validate_model:
            return
        
        # Deleta os setores primeiro
        delete_sectors_query = ticket_model_sector.delete().where(
            (ticket_model_sector.c.cnpj == cnpj) & 
            (ticket_model_sector.c.ticket_model_id == ticket_model_id)
        )
        await database.execute(delete_sectors_query)

        # Deleta o modelo
        delete_model_query = ticket_model.delete().where(
            (ticket_model.c.cnpj == cnpj) & 
            (ticket_model.c.ticket_model_id == ticket_model_id)
        )
        await database.execute(delete_model_query)

        return {"message": "Ticket model and its sectors deleted successfully."}
    
    async def delete_sector_from_model(self, cnpj: str, ticket_model_id: int, sector_id: int) -> dict:
        validate_model = await self._validate_model(cnpj, ticket_model_id)
        if not validate_model:
            return
                    
        validate_ticket_model_sector = await self._validate_ticket_model_sector(cnpj, ticket_model_id, sector_id)
        if not validate_ticket_model_sector:
            return
        
        # Deleta o setor
        delete_sector_query = ticket_model_sector.delete().where(
            (ticket_model_sector.c.cnpj == cnpj) &
            (ticket_model_sector.c.ticket_model_id == ticket_model_id) &
            (ticket_model_sector.c.sector_id == sector_id)
        )
        await database.execute(delete_sector_query)

        # Verifica se ainda há setores associados
        check_query = ticket_model_sector.select().where(
            (ticket_model_sector.c.cnpj == cnpj) &
            (ticket_model_sector.c.ticket_model_id == ticket_model_id)
        )
        remaining_sectors = await database.fetch_all(check_query)

        if not remaining_sectors:
            # Nenhum setor restante — deleta o modelo também
            delete_model_query = ticket_model.delete().where(
                (ticket_model.c.cnpj == cnpj) &
                (ticket_model.c.ticket_model_id == ticket_model_id)
            )
            await database.execute(delete_model_query)

            return {"message": "Sector deleted. No sectors left, model also deleted."}

        return {"message": "Sector deleted from ticket model."}
    
    async def update_ticket_model(
        self,
        cnpj: str,
        ticket_model_id: int,
        data
    ) -> dict:
        
        validate_model = await self._validate_model(cnpj, ticket_model_id)
        if not validate_model:
            return
        
        if data.name is not None:
            stmt = (
                ticket_model.update()
                .where(
                    (ticket_model.c.cnpj == cnpj) &
                    (ticket_model.c.ticket_model_id == ticket_model_id)
                )
                .values(name=data.name)
            )
            await database.execute(stmt)

        # 2. atualiza setores
        for s in data.sectors:
            
            validate_sector = await SectorService._get_sector(cnpj, s.sector_id)
            if not validate_sector:
                return
                        
            values = {}
            if s.price is not None:
                values["price"] = s.price
            if s.ticket_load is not None:
                values["ticket_load"] = s.ticket_load

            if values:                        # só executa se tiver algo pra mudar
                stmt = (
                    ticket_model_sector.update()
                    .where(
                        (ticket_model_sector.c.cnpj == cnpj) &
                        (ticket_model_sector.c.ticket_model_id == ticket_model_id) &
                        (ticket_model_sector.c.sector_id == s.sector_id)
                    )
                    .values(**values)
                )
                await database.execute(stmt)

        return {"message": "Ticket model updated."}
    
    
    async def add_sectors_to_model(
        self,
        cnpj: str,
        ticket_model_id: int,
        sectors_payload  
    ) -> dict:
        
        validate_model = await self._validate_model(cnpj, ticket_model_id)
        if not validate_model:
            return
        
        for s in sectors_payload:
            
            validate_sector = await SectorService._get_sector(cnpj, s.sector_id)
            if not validate_sector:
                return
          
            exists = await self._validate_sector_linked_model(cnpj, ticket_model_id, s.sector_id)
            if exists:
                return
            
            query = ticket_model_sector.insert().values(
                cnpj=cnpj,
                ticket_model_id=ticket_model_id,
                sector_id=s.sector_id,
                price=s.price,
                ticket_load=s.ticket_load
            )
            await database.execute(query)

        return {"message": "Sector(s) added to ticket model."}

    @staticmethod
    async def _validate_model(cnpj: str, ticket_model_id: int) -> Record:
    
        query = ticket_model.select().where(
            (ticket_model.c.cnpj == cnpj) & 
            (ticket_model.c.ticket_model_id == ticket_model_id)
        )
        model = await database.fetch_one(query)

        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket model not found."
            )
            
        return model
    
    @staticmethod
    async def _validate_ticket_model_sector(cnpj: str, ticket_model_id: int, sector_id: int):
    
        # Verifica se o setor está vinculado ao modelo
        sector_query = ticket_model_sector.select().where(
            (ticket_model_sector.c.cnpj == cnpj) &
            (ticket_model_sector.c.ticket_model_id == ticket_model_id) &
            (ticket_model_sector.c.sector_id == sector_id)
        )
        sector = await database.fetch_one(sector_query)
        
        if not sector:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sector not found in this model."
            )
            
        return sector
            
    @staticmethod
    async def _validate_sector_linked_model(cnpj: str, ticket_model_id: int, sector_id: int):       
        query = select().where((ticket_model_sector.c.cnpj == cnpj) 
                             & (ticket_model_sector.c.ticket_model_id == ticket_model_id) 
                             & (ticket_model_sector.c.sector_id == sector_id)
            )
        
        validate_ticket_model_sector = await database.fetch_one(query)
        if validate_ticket_model_sector:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sector {sector_id} already linked to this model."
            )
        
        return validate_ticket_model_sector