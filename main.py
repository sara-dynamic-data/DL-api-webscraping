from fastapi import FastAPI
from functions.webscraping import get_rad_info
from mangum import Mangum

app = FastAPI()


@app.get('/{radicado}')
def get_info_rad(radicado):
    table = get_rad_info(radicado)
    print(type(table))
    table = table.reset_index()
    table = table.set_index('index').T.to_dict('dict')
    return table


handler = Mangum(app)
