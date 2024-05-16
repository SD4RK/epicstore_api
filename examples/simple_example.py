from epicstore_api import EpicGamesStoreAPI, OfferData


def main() -> None:
    """Prints offer ID and developer for every offer of the first product in mapping."""
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


if __name__ == '__main__':
    main()
