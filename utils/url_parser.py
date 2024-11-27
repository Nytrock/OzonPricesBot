def get_product_id_from_url(url: str) -> int:
    if 'ozon.ru/product/' not in url:
        return -1

    url_parts = url.split('/')
    for i, url_part in enumerate(url_parts):
        if url_part == 'product' and i + 1 < len(url_parts):
            return int(url_parts[i + 1].split('-')[-1])

    return -1

def get_product_id_from_inner_url(url: str) -> int:
    return get_product_id_from_url('ozon.ru' + url)
