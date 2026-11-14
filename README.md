# 🥗 Daily Diet API

API para controle de dieta diária, feita no desafio da Formação Python da Rocketseat.

O usuário registra as refeições, informando se estão dentro ou fora da dieta.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Passlib (hash de senha com bcrypt)

## Funcionalidades

- Cadastrar usuário (senha salva com hash)
- Registrar refeição (nome, descrição, data/hora e se está dentro da dieta)
- Editar refeição
- Apagar refeição
- Listar todas as refeições de um usuário
- Ver uma única refeição

## Rotas

| Método | Rota | Descrição |
|---|---|---|
| POST | `/user` | Cadastra um usuário |
| POST | `/dieta` | Registra uma refeição |
| GET | `/users/{user_id}/refeicoes` | Lista as refeições de um usuário |
| GET | `/refeicoes/{refeicoes_id}` | Mostra uma refeição |
| PUT | `/refeicoes/{refeicoes_id}` | Edita uma refeição |
| DELETE | `/refeicoes/{refeicoes_id}` | Apaga uma refeição |

### Exemplo de body (criar refeição)

```json
{
  "nome_ref": "Arroz com frango",
  "descricao": "Almoço",
  "data_hora": "2026-11-13T12:30:00",
  "dentro_dieta": true,
  "usuario_id": 1
}
```

Se `data_hora` não for enviado, a API usa a data e hora atuais.

## Como rodar

1. Clone o repositório:
```bash
git clone https://github.com/LuigiT2703/daily-diet-api.git
cd daily-diet-api
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um banco chamado `diet_db` no PostgreSQL.

4. Copie o `.env.example` para `.env` e coloque a sua senha do banco:
```
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost/diet_db
```

5. Crie as tabelas:
```bash
python create_db.py
```

6. Rode a API:
```bash
uvicorn main:app --reload
```

7. Acesse a documentação em `http://localhost:8000/docs`.

## Próximos passos

- Login com JWT, para cada usuário mexer só nas próprias refeições
- Métricas: total de refeições, quantas dentro/fora da dieta e a melhor sequência dentro da dieta

---

Feito por [Luigi](https://github.com/LuigiT2703)