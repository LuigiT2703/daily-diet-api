from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from passlib.context import CryptContext
from database import SessionLocal
import models


app = FastAPI()
db = SessionLocal()
pwd_context = CryptContext(schemes=["bcrypt"])
class RefeicaoCreate(BaseModel):
  nome_ref: str
  descricao: Optional[str] = None
  data_hora: datetime = Field(default_factory=datetime.now)
  dentro_dieta: bool
  usuario_id: int

class RefeicaoResponse(RefeicaoCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
   nome: str
   email: str
   password: str

class UserResponse(BaseModel):
   id: int
   nome: str
   email: str
   model_config = ConfigDict(from_attributes=True)

@app.post("/user", response_model=UserResponse, status_code=201)
def create_user(dados: UserCreate):
   db_user = db.query(models.User).filter(models.User.email == dados.email).first()

   if db_user:
      raise HTTPException(status_code=400, detail="usuario ja esta em uso!")

   usuario = models.User(
      nome = dados.nome,
      email = dados.email,
      password_hashed = pwd_context.hash(dados.password)
   )

   db.add(usuario)
   db.commit()
   db.refresh(usuario)

   return usuario

@app.post("/refeicoes", response_model=RefeicaoResponse, status_code=201)
def create_diet(diet: RefeicaoCreate):
   usuario = db.query(models.User).filter(models.User.id == diet.usuario_id).first()

   if usuario is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario inexistente")

   refeicao = models.Refeicao(
      nome_ref = diet.nome_ref,
      descricao = diet.descricao,
      data_hora = diet.data_hora,
      dentro_dieta = diet.dentro_dieta,
      usuario_id = diet.usuario_id
   )

   db.add(refeicao)
   db.commit()
   db.refresh(refeicao)

   return refeicao

@app.get("/refeicoes/{refeicoes_id}", response_model=RefeicaoResponse, status_code=200)
def get_ref(refeicoes_id: int):
   ref = db.query(models.Refeicao).filter(models.Refeicao.id == refeicoes_id).first()

   if ref is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Essa refeicao nao existe!")
   
   return ref

@app.get("/users/{user_id}/refeicoes", response_model=List[RefeicaoResponse], status_code=200)
def get_ref_user(user_id:int):
   usuario = db.query(models.User).filter(models.User.id == user_id).first()
   if usuario is None:
      raise HTTPException(status_code=404, detail="Usuario nao encontrado!")

   ref_user = db.query(models.Refeicao).filter(models.Refeicao.usuario_id == user_id).all()

   return ref_user
   

@app.put("/refeicoes/{refeicoes_id}", response_model=RefeicaoResponse, status_code=200)
def put_ref(refeicoes_id: int, dados: RefeicaoCreate):
   ref_db = db.query(models.Refeicao).filter(models.Refeicao.id == refeicoes_id).first()

   if ref_db is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="refeicao nao encontrada")

   ref_db.nome_ref = dados.nome_ref
   ref_db.descricao = dados.descricao
   ref_db.data_hora = dados.data_hora
   ref_db.dentro_dieta = dados.dentro_dieta
   ref_db.usuario_id = dados.usuario_id


   db.commit()
   db.refresh(ref_db)
   

   return ref_db

@app.delete("/refeicoes/{refeicoes_id}", status_code=200)
def delete_refeicao(refeicoes_id: int):
   ref_db = db.query(models.Refeicao).filter(models.Refeicao.id == refeicoes_id).first()

   if ref_db is None:
      raise HTTPException(status_code=404, detail="refeicao nao encontrada")

   db.delete(ref_db)
   db.commit()

   return {"message": "refeicao deletado"}