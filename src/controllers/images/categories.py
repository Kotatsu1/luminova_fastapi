from fastapi import HTTPException
import cloudinary
import cloudinary.api
from dotenv import load_dotenv
from controllers.images import favorite
from schemas.image_schemas import FetchFromCategory, FetchCategoryFavorites


load_dotenv()

config = cloudinary.config(secure=True)

def get_categories() -> dict:
    response = cloudinary.api.root_folders()
    for i in response['folders']:
        i['name'] = i['name'].capitalize().replace('-', ' ')
    return response


def get_images_with_params(type: str, cursor: str) -> dict:
    return cloudinary.Search().max_results("50").next_cursor(cursor).expression(f"folder:{type}").execute()


def add_page_preview(data: dict, params: str) -> dict:
    data.update({'page_preview': f'http://45.87.246.48:8000/page_preview/{params}.avif'})
    return data


def get_images_from_category(request: FetchFromCategory):
    try:
        images = get_images_with_params(request.folder, request.next_cursor)
        return add_page_preview(images, request.folder)
    except Exception:
        raise HTTPException(status_code=404, detail='Cound not get images from category')


def get_category_images_with_favorite(request: FetchCategoryFavorites):
    all_images = get_images_with_params(request.category, request.next_cursor)
    added_preview = add_page_preview(all_images, request.category)
    resources = added_preview['resources']
    favorite_images = favorite.user_favorive_images(request.token)

    def mark_favorite(image):
        if image['public_id'] in favorite_images:
            image['favorite'] = True
        else:
            image['favorite'] = False
        return image

    # resources = list(map(lambda image: image['favorite'] = True if image["public_id"] in favorite_images else image['favorite'] = False, resources))
    resources = list(map(mark_favorite, resources))
    return added_preview