# Alembic
    # Criar migrations usando alembic
        alembic revision --autogenerate -m "Mensagem da migration"

    # Executar a migração
        alembic upgrade head

# Uvicorn
    # Rodar o servidor com reload
        uvicorn main:app --reload

    # Rodar o servidor sem reload
        uvicorn main:app --host 0.0.0.0 --port 8000