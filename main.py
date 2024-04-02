from typing import Union
from fastapi import FastAPI
from sqlalchemy import create_engine, text, insert, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

Base = declarative_base()
engine = create_engine('postgresql+psycopg2://max2:pswd@localhost/pgdb')
Base.metadata.create_all(engine)

class QuoteObject(Base):
    __tablename__ = "Quotes"
    id = Column(Integer, primary_key=True)
    quote = Column(String)
    author = Column(String)

PydanticQuote = sqlalchemy_to_pydantic(QuoteObject)

def getQuote(id):
    with engine.connect() as conn:
        result = conn.execution_options(stream_results=True).execute(text("SELECT Id, Quote, Author fROM Quotes WHERE Id = " + str(id)))
        row = result.fetchone()
        return row


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    quote = PydanticQuote.from_orm(getQuote(item_id))
    print(quote)
    return quote



@app.post("/items/")
async def create_item(quote: QuoteObject):
    return quote