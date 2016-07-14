from amazon.api import AmazonAPI
amazon = AmazonAPI('AKIAIEFAOD3KNCREQ2DQ', 'J+2zn8j81K9ul+NyE05bY0JqFNawSvxfCuyyGj83', 'shaked02-20')
products = amazon.search(Keywords='Diesel Watch', SearchIndex='All')
for i, product in enumerate(products):
    print "{0}. '{1}'".format(product.title)

