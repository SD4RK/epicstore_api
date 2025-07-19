.. _intro:

Introduction
==============

This is the documentation for epicstore_api,
library for working with the Epic Games Store API. The library works with `cloudscraper` under the hood to battle the anti-bot protections, please be careful with the amount of requests you do, as this is not a silver bullet.

Prerequisites
---------------

epicstore_api works with Python 3.6 or higher, other versions may not work.



.. _installing:

Installing
-----------

You can get the library directly from PyPI: ::

    python3 -m pip install -U epicstore_api

If you are using Windows, then the following should be used instead: ::

    py -3 -m pip install -U epicstore_api


Remember to check your permissions!


Quick Example
----------------
Code that will print offer id(s) and their developer for the first product in mapping.
You can see other examples in ``examples/`` directory:

.. code-block:: python3

    from epicstore_api import EpicGamesStoreAPI, OfferData

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