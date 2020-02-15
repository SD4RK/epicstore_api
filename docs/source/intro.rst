.. _intro:

Introduction
==============

This is the documentation for epicstore_api,
library for working with the Epic Games Store API

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