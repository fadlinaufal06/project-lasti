from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Data Barang", description="Project LaSTI")

with open("databarang.json", "r") as read_file:
    data = json.load(read_file)

@app.get('/')
def root():
    return{'Data Barang'}


## CRUD Barang ##################################


#Untuk Get Barang
@app.get('/barang')
async def read_all_barang():
    return data

#Get by id
@app.get('/barang{item_id}')
async def read_barang(item_id: str):
    for barang_item in data['barang']:
        if barang_item['id'] == item_id:
            return barang_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

#Untuk Tambah barang  # Tolong Ini ID nya didapat dari scan RFID ini gatau python bisa read atau masukin manual
# Sementara ID dibikin integer dulu dan updatenya increment dari 1 (sama dengan tst)
@app.post('/barang')
async def post_barang(barang_warna:str, jenis_barang:str, merek:str, waktu_pembelian:str, waktu_penjualan:str, jumlah_pembelian:str):
    id=1 
    if(len(data["barang"])>0):
        id=data["barang"][len(data["barang"])-1]["id"]+1
    new_data={'id':id, 'warna':barang_warna, 'jenis':jenis_barang, "merek":merek, "waktu pembelian":waktu_pembelian, 'waktu_penjualan':waktu_penjualan, 'jumlah pembelian': jumlah_pembelian}
    data['barang'].append(dict(new_data))
    read_file.close()
    with open("barang.json", "w") as write_file:
        json.dump(data,write_file,indent=4)
    write_file.close()

    return (new_data)
    raise HTTPException(
        status_code=500, detail=f'Error'
    )   


#Untuk Delete barang bedasarkan Id
@app.delete('/barang{item_id}')
async def delete_barang(item_id: int):
    for barang_item in data['barang']:
        if barang_item['id'] == item_id:
            data['barang'].remove(barang_item) 
            read_file.close()
            with open("barang.json", "w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()
            return{"message":"Data successfully deleted"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

# ini sama id nya dari RFID gatau manual apa engga
@app.put('/barang{item_id}')
async def update_barang(item_id: int, name:str):
    for barang_item in data['barang']:
        if barang_item['id'] == item_id:
            barang_item['name'] = name
            read_file.close()
            with open("barang.json", "w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()
            return{"message":"Data successfully updated"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

    
