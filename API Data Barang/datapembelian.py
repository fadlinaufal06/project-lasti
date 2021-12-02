import json
from typing import Dict, List
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sklearn.preprocessing import LabelEncoder
import pickle
import pandas
import numpy

from pydantic import BaseModel

file_model = 'finalized_model.sav'
model = pickle.load(open(file_model, 'rb'))

with open("datapembelian.json", "r") as read_file:
    data = json.load(read_file)

datamodel = data["pembelian"]


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
    return {'API data pembelian'}

@app.get('/pembelian')
async def take_all():
    return data['pembelian']

@app.get('/pembelian{ID_pembelian}')
async def take_one(id: int):
    for pembelian in data['pembelian']:
        if pembelian['ID_pembelian'] == id:
            return pembelian
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.get('/pembelian/rekomendasi', response_model = List[RekomendasiBase])
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


@app.post('pembelian')
async def add(id: int, id_barang: int, warna: str, merek: str, jenis: str, harga: float, size: int, diskon: float, rating: float):
    id = 1
    if (len(data['pembelian'])>0):
        id = data['pembelian'][len(data['pembelian'])-1]['ID_pembelian']+1
    new_data = {'ID_pembelian':id,'ID_barang':id_barang,'Warna_barang':warna, 'Merek': merek, 'Jenis': jenis, 'Harga': harga, 'Universal_size_(1-10)': size, 'Diskon_(%)':diskon, 'Rating': rating}
    data['pembelian'].append(dict(new_data))
    read_file.close()
    with open("datapembelian.json", "w") as write_file:
        json.dump(data, write_file, indent = 4)
    write_file.close()
    return (new_data)

    raise HTTPException(
        status_code=500, detail=f'Internal Server Error'
    )

@app.put('/pembelian')
async def change(id: int, id_barang: int,warna: str, merek: str, jenis: str, harga: float, size: int, diskon: float, rating: float):
    for pembelian in data['pembelian']:
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
                json.dump(data, write_file, indent = 4)
            write_file.close()
            return {"message":"Data updated successfully"}

    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.delete('/pembelian')
async def delete_all():
    new_data = data['pembelian'].clear()
    read_file.close()
    with open("datapembelian.json", "w") as write_file:
        json.dump(new_data, write_file, indent = 4)
    write_file.close()
    return {"message":"All data has been successfully deleted"}   

@app.delete('/pembelian{ID_barang}')
async def delete_one(id: int):
    for pembelian in data['pembelian']:
        if pembelian['ID_pembelian'] == id:
            data['pembelian'].remove(pembelian)
            read_file.close()
            with open("datapembelian.json", "w") as write_file:
                json.dump(data, write_file, indent = 4)
            write_file.close()
            return {"message":"Data deleted successfully"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )   