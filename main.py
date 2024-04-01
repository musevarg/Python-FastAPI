from typing import Union
from fastapi import FastAPI
from sqlalchemy import create_engine, text

engine = create_engine('postgresql+psycopg2://max2:pswd@localhost/pgdb')

def getQuote(id):
    with engine.connect() as conn:
        result = conn.execution_options(stream_results=True).execute(text("SELECT Id, Quote, Author fROM Quotes WHERE Id = " + str(id)))
        parsed_result = result.fetchone()
        return parsed_result

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}