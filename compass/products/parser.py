import xml.etree.ElementTree as ET

from urllib.request import urlopen

def get_products_dict() -> dict:
    link= 'https://compass-shop.ru/yandex.xml'

    tree = ET.parse(urlopen(link))
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
        dimensions = ''.join([param.text for param in list(offer) if param.get('name')== 'Размеры изделия, см'])
        model_line = ''.join([param.text for param in list(offer) if param.get('name')== 'Модельная линейка'])
        height = ''.join([param.text for param in list(offer) if param.get('name')== 'Высота изделия, см'])
        width = ''.join([param.text for param in list(offer) if param.get('name')== 'Ширина изделия, см'])
        depth = ''.join([param.text for param in list(offer) if param.get('name')== 'Глубина изделия, см'])

        barcode = offer.find('barcode').text
        weight = 0  #offer.find('weight').text if offer.find('weight') else offer.find('Вес брутто, кг.').text
        id = offer.get('id')

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
