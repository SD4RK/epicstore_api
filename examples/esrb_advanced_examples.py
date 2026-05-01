from epicstore_api import EpicGamesStoreAPI, EGSCollectionType


def example_free_games_ratings():
    print("=" * 70)
    print("EXAMPLE 1: Free Games with ESRB Ratings")
    print("=" * 70)

    api = EpicGamesStoreAPI()
    free_games = api.get_free_games_with_ratings()

    print(f"\nFound {len(free_games.get('data', []))} free games:\n")
    for game in free_games.get('data', [])[:5]:  # Show first 5
        title = game.get('title', 'Unknown')
        esrb = game.get('esrb_rating', {})
        rating = esrb.get('rating') or 'Not Rated'
        descriptors = esrb.get('descriptors', [])

        print(f"Title: {title}")
        print(f"  Rating: {rating}")
        if descriptors:
            print(f"  Content: {', '.join(descriptors)}")
        print()


def example_filter_by_rating():
    print("=" * 70)
    print("EXAMPLE 2: Filter Games by ESRB Rating")
    print("=" * 70)

    api = EpicGamesStoreAPI()
    free_games = api.get_free_games_with_ratings()

    ratings_to_check = ['E', 'T', 'M']

    for rating_code in ratings_to_check:
        games = [
            game for game in free_games.get('data', [])
            if game.get('esrb_rating', {}).get('rating') == rating_code
        ]
        print(f"\nGames rated {rating_code}: {len(games)}")
        for game in games[:3]:  # Show first 3
            print(f"  - {game.get('title')}")


def example_filter_by_content():
    print("=" * 70)
    print("EXAMPLE 3: Filter Games by Content Descriptors")
    print("=" * 70)

    api = EpicGamesStoreAPI()
    free_games = api.get_free_games_with_ratings()
    content_filters = {
        'Violence': ['violence', 'intense violence', 'fantasy violence', 'cartoon violence'],
        'Blood': ['blood', 'animated blood', 'mild blood', 'blood and gore'],
        'Language': ['language', 'mild language', 'strong language'],
        'Suggestive': ['suggestive themes', 'nudity', 'partial nudity'],
    }

    for content_type, keywords in content_filters.items():
        matching_games = []
        for game in free_games.get('data', []):
            descriptors = game.get('esrb_rating', {}).get('descriptors', [])
            if any(
                any(keyword in desc.lower() for keyword in keywords)
                for desc in descriptors
            ):
                matching_games.append(game)

        print(f"\nGames with {content_type}: {len(matching_games)}")
        for game in matching_games[:3]:  # Show first 3
            rating = game.get('esrb_rating', {}).get('rating', 'Not Rated')
            descriptors = game.get('esrb_rating', {}).get('descriptors', [])
            print(f"  - {game.get('title')} ({rating})")
            if descriptors:
                matching_desc = [
                    d for d in descriptors
                    if any(k in d.lower() for k in keywords)
                ]
                if matching_desc:
                    print(f"    {', '.join(matching_desc)}")


def example_extract_from_store_search():
    print("=" * 70)
    print("EXAMPLE 4: Extract from Store Search")
    print("=" * 70)

    api = EpicGamesStoreAPI()

    search_terms = ['Fortnite', 'Valorant', 'Star Wars']

    for term in search_terms:
        print(f"\nSearching for '{term}':")
        result = api.fetch_store_games(keywords=term, count=3)

        games = result.get('data', {}).get('Catalog', {}).get('searchStore', {}).get('elements', [])
        for game in games:
            esrb = api.extract_esrb_rating(game)
            title = game.get('title', 'Unknown')
            rating = esrb.rating or 'Not Rated'
            descriptors = esrb.descriptors or []

            print(f"  {title}: {rating}")
            if descriptors:
                print(f"    Content: {', '.join(descriptors)}")


def example_extract_from_collection():
    """Example 5: Extract ESRB ratings from collections."""
    print("=" * 70)
    print("EXAMPLE 5: Extract from Collections")
    print("=" * 70)

    api = EpicGamesStoreAPI()
    print("\nFetching Featured games...")
    try:
        collection = api.get_collection(EGSCollectionType.FEATURED)
        games = collection.get('Storefront', {}).get('collectionLayout', {}).get('collectionOffers', [])

        print(f"Found {len(games)} featured games\n")
        for game in games[:5]:  # Show first 5
            esrb = api.extract_esrb_rating(game)
            title = game.get('title', 'Unknown')
            rating = esrb.rating or 'Not Rated'

            print(f"  {title}: {rating}")
    except Exception as e:
        print(f"Error fetching collection: {e}")


def example_rating_statistics():
    print("=" * 70)
    print("EXAMPLE 6: Rating Statistics")
    print("=" * 70)

    api = EpicGamesStoreAPI()
    free_games = api.get_free_games_with_ratings()

    rating_counts = {}
    descriptor_counts = {}
    total_games = 0

    for game in free_games.get('data', []):
        total_games += 1
        esrb = game.get('esrb_rating', {})
        rating = esrb.get('rating') or 'Not Rated'

        rating_counts[rating] = rating_counts.get(rating, 0) + 1

        for descriptor in esrb.get('descriptors', []):
            descriptor_counts[descriptor] = descriptor_counts.get(descriptor, 0) + 1

    print(f"\nTotal Free Games: {total_games}")
    print("\nRating Distribution:")
    for rating in ['E', 'E10+', 'T', 'M', 'AO', 'RP', 'Not Rated']:
        count = rating_counts.get(rating, 0)
        if count > 0:
            percentage = (count / total_games) * 100
            print(f"  {rating:10s}: {count:3d} ({percentage:5.1f}%)")

    print("\nTop 10 Content Descriptors:")
    sorted_descriptors = sorted(descriptor_counts.items(), key=lambda x: x[1], reverse=True)
    for descriptor, count in sorted_descriptors[:10]:
        percentage = (count / total_games) * 100
        print(f"  {descriptor:25s}: {count:3d} ({percentage:5.1f}%)")


def main():
    try:
        example_free_games_ratings()
        example_filter_by_rating()
        example_filter_by_content()
        example_extract_from_store_search()
        example_extract_from_collection()
        example_rating_statistics()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()

