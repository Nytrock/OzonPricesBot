from utils.url_parser import get_product_id_from_url

# Тестирование получения id товара из ссылки
print(get_product_id_from_url('https://www.ozon.ru/product/finish-power-all-in-1-tabletki-dlya-posudomoechnoy-mashiny-100-sht-136311798/?campaignId=441&oos_search=false'))
print(get_product_id_from_url('ozon.ru/product/upakovochnaya-bumaga-v-rulone-panda-paketiko-76sm-1000-sm-1sht-1667404254/'))