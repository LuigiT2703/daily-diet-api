from database import Base, engine
from models import User, Refeicao

print("Criando o banco...")

Base.metadata.create_all(engine)