from epicstore_api import EpicGamesStoreAPI
from datetime import datetime


def main():
    """Fetches current free games from the store."""
    api = EpicGamesStoreAPI()
    free_games = api.get_free_games()['data']['Catalog']['searchStore']['elements']
    for game in free_games:
        game_name = game['title']
        game_thumbnail = None
        # Can be useful when you need to also show the thumbnail of the game.
        # Like in Discord's embeds for example, or anything else.
        # Here I showed it just as example and won't use it.
        for image in game['keyImages']:
            if image['type'] == 'Thumbnail':
                game_thumbnail = image['url']
        game_price = game['price']['totalPrice']['fmtPrice']['originalPrice']
        try:
            game_promotions = game['promotions']['promotionalOffers']
            upcoming_promotions = game['promotions']['upcomingPromotionalOffers']
            if not game_promotions and upcoming_promotions:
                # Promotion is not active yet, but will be active soon.
                promotion_data = upcoming_promotions[0]['promotionalOffers'][0]
                start_date_iso, end_date_iso = (
                    promotion_data['startDate'][:-1], promotion_data['endDate'][:-1]
                )
                # Remove the last "Z" character so Python's datetime can parse it.
                start_date = datetime.fromisoformat(start_date_iso)
                end_date = datetime.fromisoformat(end_date_iso)
                print('{} ({}) will be free from {} to {} UTC.'.format(
                    game_name, game_price, start_date, end_date
                ))
            else:
                print('{} ({}) is FREE now.'.format(
                    game_name, game_price
                ))
        except TypeError:
            pass
            # or
            #print('No discounts for this game')
            # your choice


if __name__ == '__main__':
    main()
