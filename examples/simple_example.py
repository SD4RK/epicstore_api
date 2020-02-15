from epicstore_api import EpicGamesStoreAPI, OfferData


def main():
    """
    Prints offer ID and developer for every offer of the first product in mapping
    """
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


if __name__ == '__main__':
    main()
