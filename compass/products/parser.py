import xml.etree.ElementTree as ET

from urllib.request import urlopen
import ssl

context = ssl._create_unverified_context()
def get_products_dict() -> dict:
    link= 'https://compass-shop.ru/yandex.xml'

    context = ssl._create_unverified_context()
    tree = ET.parse(urlopen(link, context=context))
    root = tree.getroot()
    BUFFER = {}


    def find_category(id: int) -> str:
        for category in root.iter('category'):
            if category.get('id') == id:
                return category.text.replace('\n', '')

    for offer in root.iter('offer'):
        price = offer.find('price').text
        category = find_category(offer.find('categoryId').text)
        sku = offer.find('sku').text
        name = offer.find('name').text
        url = offer.find('url').text
        description = offer.find('description').text
        barcode = offer.find('barcode').text
        id = offer.get('id')
        dimensions = ''.join([str(param.text) for param in list(offer) if param.get('name') == 'Размеры изделия, см'])        
        model_line = ''.join([str(param.text) for param in list(offer) if param.get('name') == 'Модельная линейка'and param.text is not None])
        height = ''.join([str(param.text) for param in list(offer) if param.get('name') == 'Высота изделия, см' and param.text is not None])
        width = ''.join([(param.text) for param in list(offer) if param.get('name') == 'Ширина изделия, см' and param.text is not None]   )
        depth = ''.join([param.text for param in list(offer) if param.get('name') == 'Глубина изделия, см' and param.text is not None])
        weight = ''.join([param.text for param in list(offer) if param.get('name') == 'Вес брутто, кг.' and param.text is not None]) 

        BUFFER[sku] = {
            'name':name,
            'id':id,
            'price':price,
            'url':url,
            'barcode':barcode,
            'model_line':model_line,
            'weight':weight,
            'description':description,
            'dimensions':dimensions,
            'category':category,
            'height': height,
            'width': width,
            'depth': depth,
        }
    
    return BUFFER
