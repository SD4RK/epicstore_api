from epicstore_api import EpicGamesStoreAPI
from epicstore_api.models import EGSCollectionType


def main() -> None:
    """Prints list of the current top sellers."""
    api = EpicGamesStoreAPI()
    top_sellers = api.get_collection(EGSCollectionType.TOP_SELLERS)['data'][
        'Storefront'
    ]['collectionLayout']['collectionOffers']
    print('Top sellers list:')
    for game in top_sellers:
        print(
            f'{game["title"]} - {game["price"]["totalPrice"]["fmtPrice"]["originalPrice"]}',
        )


if __name__ == '__main__':
    main()
