from fastapi import UploadFile, APIRouter
import shutil

router = APIRouter(
    prefix='/images',
    tags=['Загрузка картинок']
)


@router.post('/hotels')
async def add_hotel_image(name: int,
                          file: UploadFile):
    with open(file=f'app/static/images/{name}.webp', mode='wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)