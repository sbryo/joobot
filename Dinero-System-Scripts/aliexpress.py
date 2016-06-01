#API KEY: 21503
#Call frequency: 100000
#Digital signature: zhtdoJpKbv

from aliexpress_api_client import AliExpress

aliexpress = AliExpress('21503', 'zhtdoJpKbv')

products = aliexpress.get_product_list(['productId', 'productTitle', 'salePrice'])

for product in products:
    print '#%s %s: %s' % (product['productId'], product['productTitle'], product['salePrice'])