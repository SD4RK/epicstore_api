# epicstore_api

A library that provide you a functionality for work with Epic Games Store 
easy and fast

## Installing

**Python 3.6 or higher is required**

To install the library you can just run the following command:

``` sh
# Linux/macOS
python3 -m pip install -U epicstore_api

# Windows
py -3 -m pip install -U epicstore_api
```


### Quick Example

``` py
api = EpicGamesStoreAPI()
namespace, slug = list(api.get_product_mapping().items())[0]
first_product = api.get_product(slug)
offers = []
for page in first_product['pages']:
    if page.get('offer') is not None:
        offers.append(OfferData(page['namespace'], page['offer']['id']))
offers_data = api.get_offers_data(*offers)
for offer_data in offers_data:
    data = offer_data['data']['Catalog']['catalogOffer']
    developer_name = ''
    for custom_attribute in data['customAttributes']:
        if custom_attribute['key'] == 'developerName':
            developer_name = custom_attribute['value']
    print('Offer ID:', data['id'], '\nDeveloper Name:', developer_name)
```

You can find more examples in the examples directory.

### Contributing
Feel free to contribute by creating PRs and sending your issues

## Links
* [Documentation](https://epicstore-api.readthedocs.io/en/latest/)
