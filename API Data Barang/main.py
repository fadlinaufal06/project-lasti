import json
from typing import Dict, List
from fastapi import FastAPI,HTTPException, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sklearn.preprocessing import LabelEncoder
import pickle
import pandas
import numpy
import uvicorn
from datetime import datetime, timedelta
from pydantic import BaseModel
from passlib.context import CryptContext

file_model = 'finalized_model.sav'
model = pickle.load(open(file_model, 'rb'))

with open("datapembelian.json", "r") as read_file:
    datapembelian = json.load(read_file)

with open("databarang.json", "r") as read_file:
    databarang = json.load(read_file)


datamodel = datapembelian["pembelian"]


def check_id(array,id,string):
    check = False
    for item in array:
        if (item[string] == id):
            check = True
    return check

class RekomendasiBase(BaseModel):
    id_produk: int
    rekomendasi :str

app = FastAPI()

@app.get('/')
async def root():
    return {'API data pembelian dan barang'}

@app.get('/pembelian',tags = ['pembelian'])
async def take_all():
    return datapembelian['pembelian']

@app.get('/pembelian{ID_pembelian}',tags = ['pembelian'])
async def take_one(id: int):
    for pembelian in datapembelian['pembelian']:
        if pembelian['ID_pembelian'] == id:
            return pembelian
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.get('/pembelian/rekomendasi', response_model = List[RekomendasiBase],tags = ['pembelian'])
def recommend_all():
    df3= pandas.DataFrame(datamodel)
    label_encoder = LabelEncoder()
    df3.drop(['ID_pembelian','Diskon_(%)','Universal_size_(1-10)'], axis=1)
    df3['Jenis'] = label_encoder.fit_transform(df3['Jenis'])
    df3['Warna_barang'] = label_encoder.fit_transform(df3['Warna_barang'])
    df3['Merek'] = label_encoder.fit_transform(df3['Merek'])
    df3['Harga'] = df3['Harga'].str.replace(r'.','').astype(float)
    df3['Rating'] = df3['Rating'].str.replace(r',','.').astype(float)
    df3['Harga'] = df3['Harga'].div(1000000)
    
    df3 = df3.dropna()
    basearray = []
    rekomendasi = []
    for i, row in df3.iterrows():
        temp = [[(row['Harga']), row['Merek'],row['Jenis'],row['Rating'],row['Warna_barang']]]
        temp = numpy.asarray(temp, dtype=object)
        temp.reshape(1,-1)
        if (not check_id(rekomendasi,row["ID_barang"],"id_produk")):
            recom_dict = {}
            recom_dict["id_produk"] = row["ID_barang"]
            arr = model.predict(temp)
            recom_dict['rekomendasi'] = str(arr[0])
            rekomendasi.append(recom_dict)
        basearray.append(temp)
    
    return rekomendasi


@app.post('pembelian',tags = ['pembelian'])
async def add(id: int, id_barang: int, warna: str, merek: str, jenis: str, harga: float, size: int, diskon: float, rating: float):
    id = 1
    if (len(datapembelian['pembelian'])>0):
        id = datapembelian['pembelian'][len(datapembelian['pembelian'])-1]['ID_pembelian']+1
    new_data = {'ID_pembelian':id,'ID_barang':id_barang,'Warna_barang':warna, 'Merek': merek, 'Jenis': jenis, 'Harga': harga, 'Universal_size_(1-10)': size, 'Diskon_(%)':diskon, 'Rating': rating}
    datapembelian['pembelian'].append(dict(new_data))
    read_file.close()
    with open("datapembelian.json", "w") as write_file:
        json.dump(datapembelian, write_file, indent = 4)
    write_file.close()
    return (new_data)

    raise HTTPException(
        status_code=500, detail=f'Internal Server Error'
    )

@app.put('/pembelian',tags = ['pembelian'])
async def change(id: int, id_barang: int,warna: str, merek: str, jenis: str, harga: float, size: int, diskon: float, rating: float):
    for pembelian in datapembelian['pembelian']:
        if pembelian['ID_pembelian'] == id:
            pembelian['ID_barang'] = id_barang
            pembelian['Warna_barang'] = warna
            pembelian['Merek'] = merek
            pembelian['Jenis'] = jenis
            pembelian['Harga'] = harga
            pembelian['Universal_size_(1-10)'] = size
            pembelian['Diskon_(%)'] = diskon
            pembelian['Rating'] = rating
            read_file.close()
            with open("datapembelian.json", "w") as write_file:
                json.dump(datapembelian, write_file, indent = 4)
            write_file.close()
            return {"message":"Data updated successfully"}

    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.delete('/pembelian',tags = ['pembelian'])
async def delete_all():
    new_data = datapembelian['pembelian'].clear()
    read_file.close()
    with open("datapembelian.json", "w") as write_file:
        json.dump(new_data, write_file, indent = 4)
    write_file.close()
    return {"message":"All data has been successfully deleted"}   

@app.delete('/pembelian{ID_barang}',tags = ['pembelian'])
async def delete_one(id: int):
    for pembelian in datapembelian['pembelian']:
        if pembelian['ID_pembelian'] == id:
            datapembelian['pembelian'].remove(pembelian)
            read_file.close()
            with open("datapembelian.json", "w") as write_file:
                json.dump(datapembelian, write_file, indent = 4)
            write_file.close()
            return {"message":"Data deleted successfully"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    ) 


@app.get('/barang',tags = ['barang'])
async def read_all_barang():
    return databarang

#Get by id
@app.get('/barang{tag_id}',tags = ['barang'])
async def read_barang(tag_id: int):
    for barang_item in databarang['barang']:
        if barang_item['id_tag'] == tag_id:
            return barang_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

#Untuk Tambah barang  # Tolong Ini ID nya didapat dari scan RFID ini gatau python bisa read atau masukin manual
# Sementara ID dibikin integer dulu dan updatenya increment dari 1 (sama dengan tst)
@app.post('/barang',tags = ['barang'])
async def post_barang(jenis:str, merek:str, nama:str, harga: str, id_tag:int):
    id=1
    if(len(databarang["barang"])>0):
        id=databarang["barang"][len(databarang["barang"])-1]["id_barang"]+1
    new_data={'id_barang':id, 'jenis':jenis, 'merek':merek, "nama":nama, "harga":harga, "id_tag":id_tag}
    databarang['barang'].append(dict(new_data))
    read_file.close()
    with open("databarang.json", "w") as write_file:
        json.dump(databarang,write_file,indent=4)
    write_file.close()

    return (new_data)
    raise HTTPException(
        status_code=500, detail=f'Error'
    )   
  


#Untuk Delete barang bedasarkan Id
@app.delete('/barang{item_id}',tags = ['barang'])
async def delete_barang(item_id: int):
    for barang_item in databarang['barang']:
        if barang_item['id_barang'] == item_id:
            databarang['barang'].remove(barang_item) 
            read_file.close()
            with open("databarang.json", "w") as write_file:
                json.dump(databarang,write_file,indent=4)
            write_file.close()
            return{"message":"Data successfully deleted"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

# ini sama id nya dari RFID gatau manual apa engga
@app.put('/barang{item_id}',tags = ['barang'])
async def update_barang(item_id: int, nama:str):
    for barang_item in databarang['barang']:
        if barang_item['id_barang'] == item_id:
            barang_item['nama'] = nama
            read_file.close()
            with open("databarang.json", "w") as write_file:
                json.dump(databarang,write_file,indent=4)
            write_file.close()
            return{"message":"Data successfully updated"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000,reload=True)  