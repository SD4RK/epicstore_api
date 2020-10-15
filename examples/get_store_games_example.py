from epicstore_api import EpicGamesStoreAPI
import json


def main():
    """
    Print all games in filter range
    """
    api = EpicGamesStoreAPI()
    games = api.fetch_store_games(
        product_type='games/edition/base|bundles/games|editors',
        # Default filter in store page.
        count=30,
        sort_by='releaseDate',
        sort_dir='DESC',
        release_date="[2019-09-16T14:02:36.304Z,2019-09-26T14:02:36.304Z]",
        with_price=True,
    )
    print('API Response:\n', json.dumps(games, indent=4))


if __name__ == '__main__':
    main()
