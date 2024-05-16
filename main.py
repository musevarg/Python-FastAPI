from typing import Union
from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text, insert, Column, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

Base = declarative_base()
engine = create_engine('postgresql+psycopg2://max2:pswd@localhost/pgdb',future=True)
Base.metadata.create_all(engine)

metadata = MetaData()
quote_table = Table('Quotes',
                    metadata,
                    Column('Id', Integer, primary_key=True),
                    Column('Quote', String),
                    Column('Author', String)
                    )

class QuoteObject(Base):
    __tablename__ = "Quotes"
    id = Column(Integer, primary_key=True)
    quote = Column(String)
    author = Column(String)

PydanticQuote = sqlalchemy_to_pydantic(QuoteObject)

def getQuote(id):
    with engine.connect() as conn:
        result = conn.execution_options(stream_results=True).execute(text("SELECT Id, Quote, Author FROM Quotes WHERE Id = " + str(id)))
        row = result.fetchone()
        return row

def insertQuote(q: QuoteObject):
    stmt = insert(quote_table).values(Id=q.id, Quote=q.quote, Author=q.author)
    print(stmt)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
        print('Inserted Primary Key: %s' % str(result.inserted_primary_key))

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    quote = PydanticQuote.from_orm(getQuote(item_id))
    print(quote)
    return quote



@app.post("/items/")
async def create_item(request: Request):
    req = await request.json()
    quote = QuoteObject(**req)
    print(quote.author)
    insertQuote(quote)
    return quote