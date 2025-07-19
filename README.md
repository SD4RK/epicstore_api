# epicstore_api

[![Current pypi version](https://img.shields.io/pypi/v/epicstore-api.svg)](https://pypi.org/project/epicstore-api/)
[![Supported py versions](https://img.shields.io/pypi/pyversions/epicstore-api.svg)](https://pypi.org/project/epicstore-api/)
[![Downloads](https://pepy.tech/badge/epicstore-api)](https://pypi.org/project/epicstore-api/)

An unofficial library to work with Epic Games Store Web API.
**The library works with `cloudscraper` under the hood to battle the anti-bot protections, please be careful with the amount of requests you do, as this is not a silver bullet.**

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
namespace, slug = next(iter(api.get_product_mapping().items()))
first_product = api.get_product(slug)
offers = [
    OfferData(page['namespace'], page['offer']['id'])
    for page in first_product['pages']
    if page.get('offer') and 'id' in page['offer']
]
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
