from sqlalchemy import Column, String, DateTime, Text, Boolean, Integer, ForeignKey
from database import Base


class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  nome = Column(String(100), nullable=False)
  email = Column(Text, nullable=False, unique=True)
  password_hashed = Column(String(100), nullable=False)

class Refeicao(Base):
  __tablename__ = "refeicoes"
  id = Column(Integer, primary_key=True)
  nome_ref = Column(Text, nullable=False)
  descricao = Column(Text)
  data_hora = Column(DateTime, nullable=False)
  dentro_dieta = Column(Boolean, nullable=False)
  usuario_id = Column(Integer, ForeignKey(User.id), nullable=False)
  
