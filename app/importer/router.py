import codecs
import csv

from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/import", tags=["Загрузка csv"])


@router.post("/{table_name}")
async def upload_csv_file(table_name, file: UploadFile = File(...)):
    csv_reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'), delimiter=';')
    data = list(csv_reader)
