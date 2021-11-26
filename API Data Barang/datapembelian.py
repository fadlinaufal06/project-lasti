import json
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

with open("datapembelian.json", "r") as read_file:
    data = json.load(read_file)

app = FastAPI()

@app.get('/')
async def root():
    return {'API data pembelian'}

@app.get('/pembelian')
async def take_all():
    return data['pembelian']

@app.get('/pembelian{ID_barang}')
async def take_one(id: int):
    for pembelian in data['pembelian']:
        if pembelian['ID_barang'] == id:
            return pembelian
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.post('pembelian')
async def add(id: int, warna: str, merek: str, jenis: str, harga: float, size: int, diskon: float, rating: float):
    id = 1
    if (len(data['pembelian'])>0):
        id = data['pembelian'][len(data['pembelian'])-1]['ID_barang']+1
    new_data = {'ID_barang':id,'Warna_barang':warna, 'Merek': merek, 'Jenis': jenis, 'Harga': harga, 'Universal_size_(1-10)': size, 'Diskon_(%)':diskon, 'Rating': rating}
    data['pembelian'].append(dict(new_data))
    read_file.close()
    with open("datapembelian.json", "w") as write_file:
        json.dump(data, write_file, indent = 4)
    write_file.close()
    return (new_data)

    raise HTTPException(
        status_code=500, detail=f'Internal Server Error'
    )

@app.put('pembelian')
async def change(id: int, warna: str, merek: str, jenis: str, harga: float, size: int, diskon: float, rating: float):
    for pembelian in data['pembelian']:
        if pembelian['ID_barang'] == id:
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
        if pembelian['ID_barang'] == id:
            data['pembelian'].remove(pembelian)
            read_file.close()
            with open("datapembelian.json", "w") as write_file:
                json.dump(data, write_file, indent = 4)
            write_file.close()
            return {"message":"Data deleted successfully"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )   