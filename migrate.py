import subprocess
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python migrate.py \"mensagem da migration\"")
        sys.exit(1)

    message = sys.argv[1]
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message], check=True)
    subprocess.run(["alembic", "upgrade", "head"], check=True)

    print("Migração criada e aplicada com sucesso!")

if __name__ == "__main__":
    main()
