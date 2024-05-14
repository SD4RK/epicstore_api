import operator
from datetime import datetime

from epicstore_api import EpicGamesStoreAPI


def main() -> None:
    """Fetches current free games from the store."""
    api = EpicGamesStoreAPI()
    free_games = api.get_free_games()['data']['Catalog']['searchStore']['elements']

    # Few odd items do not seems game and don't have the promotion attribute, so let's check it !
    free_games = sorted(
        filter(lambda g: g.get('promotions'), free_games),
        key=operator.itemgetter('title'),
    )

    for game in free_games:
        game_title = game['title']
        game_publisher = game['seller']['name']
        game_url = f"https://store.epicgames.com/fr/p/{game['catalogNs']['mappings'][0]['pageSlug']}"
        # Can be useful when you need to also show the thumbnail of the game.
        # Like in Discord's embeds for example, or anything else.
        # Here I showed it just as example and won't use it.
        for image in game['keyImages']:
            if image['type'] == 'Thumbnail':
                game_thumbnail = image['url']

        game_price = game['price']['totalPrice']['fmtPrice']['originalPrice']
        game_price_promo = game['price']['totalPrice']['fmtPrice']['discountPrice']

        game_promotions = game['promotions']['promotionalOffers']
        upcoming_promotions = game['promotions']['upcomingPromotionalOffers']

        if game_promotions and game['price']['totalPrice']['discountPrice'] == 0:
            # Promotion is active.
            promotion_data = game_promotions[0]['promotionalOffers'][0]
            start_date_iso, end_date_iso = (
                promotion_data['startDate'][:-1],
                promotion_data['endDate'][:-1],
            )
            # Remove the last "Z" character so Python's datetime can parse it.
            start_date = datetime.fromisoformat(start_date_iso)
            end_date = datetime.fromisoformat(end_date_iso)
            print(
                f'* {game_title} ({game_price}) is FREE now, until {end_date} --> {game_url}',
            )
        elif not game_promotions and upcoming_promotions:
            # Promotion is not active yet, but will be active soon.
            promotion_data = upcoming_promotions[0]['promotionalOffers'][0]
            start_date_iso, end_date_iso = (
                promotion_data['startDate'][:-1],
                promotion_data['endDate'][:-1],
            )
            # Remove the last "Z" character so Python's datetime can parse it.
            start_date = datetime.fromisoformat(start_date_iso)
            end_date = datetime.fromisoformat(end_date_iso)
            print(
                f'* {game_title} ({game_price}) will be free from {start_date} to {end_date} UTC --> {game_url}',
            )
        elif game_promotions:
            # Promotion is active.
            promotion_data = game_promotions[0]['promotionalOffers'][0]
            start_date_iso, end_date_iso = (
                promotion_data['startDate'][:-1],
                promotion_data['endDate'][:-1],
            )
            # Remove the last "Z" character so Python's datetime can parse it.
            start_date = datetime.fromisoformat(start_date_iso)
            end_date = datetime.fromisoformat(end_date_iso)
            print(
                f'* {game_title} is in promotion ({game_price} -> {game_price_promo}) from {start_date} to {end_date} UTC --> {game_url}',
            )
        else:
            print(f'* {game_title} is always free --> {game_url}')


if __name__ == '__main__':
    main()
