import pytest

from epicstore_api import EGSException, EpicGamesStoreAPI


def main() -> None:
    api = EpicGamesStoreAPI()
    with pytest.raises(EGSException):
        api.get_product('this_slug_does_not_exist')
    satisfactory_page = api.get_product('satisfactory')
    assert satisfactory_page['namespace'] == 'crab'


if __name__ == '__main__':
    main()
