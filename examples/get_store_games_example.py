from epicstore_api import EpicGamesStoreAPI, OfferData
import json

def main():
    """
    Print all games in filter range
    """
    api = EpicGamesStoreAPI(country='VN')
    games = api.fetch_store_games(
        product_type='games/edition/base|bundles/games|editors', #default filter in store page
        count=30,
        sort_by='releaseDate',
        sort_dir='DESC',
        releaseDate="[2019-09-16T14:02:36.304Z,2019-09-26T14:02:36.304Z]",
        withPrice=True,
        )
    print(json.dumps(games))
    f = open("games.txt", "w")
    f.write(json.dumps(games))
    f.close()

if __name__ == '__main__':
    main()