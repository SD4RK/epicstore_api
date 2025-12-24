from epicstore_api import EpicGamesStoreAPI


def main() -> None:
    api = EpicGamesStoreAPI()
    free_games = api.get_free_games_with_ratings()

    print("Free Games with ESRB Ratings:")
    print("=" * 70)

    for game in free_games.get('data', []):
        title = game.get('title', 'Unknown')
        esrb_rating = game.get('esrb_rating', {})
        rating = esrb_rating.get('rating', 'Not Rated')
        descriptors = esrb_rating.get('descriptors', [])

        print(f"\nTitle: {title}")
        print(f"ESRB Rating: {rating}")
        if descriptors:
            print(f"Content Descriptors: {', '.join(descriptors)}")
        else:
            print("Content Descriptors: None")

    print("\n" + "=" * 70)
    print("\nGames rated M (Mature 17+):")
    print("=" * 70)

    for game in free_games.get('data', []):
        esrb_rating = game.get('esrb_rating', {})
        if esrb_rating.get('rating') == 'M':
            title = game.get('title', 'Unknown')
            descriptors = esrb_rating.get('descriptors', [])
            print(f"\n{title}")
            if descriptors:
                print(f"  Content: {', '.join(descriptors)}")
    print("\n" + "=" * 70)
    print("\nGames with Violence Content:")
    print("=" * 70)

    for game in free_games.get('data', []):
        esrb_rating = game.get('esrb_rating', {})
        descriptors = esrb_rating.get('descriptors', [])
        has_violence = any('violence' in d.lower() for d in descriptors)
        if has_violence:
            title = game.get('title', 'Unknown')
            rating = esrb_rating.get('rating', 'Not Rated')
            print(f"{title} ({rating})")


if __name__ == '__main__':
    main()

