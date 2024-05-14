"""MIT License.

Copyright (c) 2020-2023 SD4RK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
from typing import NamedTuple

import requests

from epicstore_api.exc import EGSException, EGSNotFound
from epicstore_api.models import EGSCategory, EGSCollectionType, EGSProductType
from epicstore_api.queries import (
    ADDONS_QUERY,
    CATALOG_QUERY,
    CATALOG_TAGS_QUERY,
    COLLECTION_QUERY,
    FEED_QUERY,
    MEDIA_QUERY,
    OFFERS_QUERY,
    PREREQUISITES_QUERY,
    PRODUCT_REVIEWS_QUERY,
    PROMOTIONS_QUERY,
    STORE_QUERY,
)


class OfferData(NamedTuple):
    namespace: str
    offer_id: str


__all__ = ['EpicGamesStoreAPI', 'OfferData']


def _clean_1004_errors(raw):
    # On some responses EGS API returns 1004 errors for no reason, however the responses being sent are valid otherwise.
    # Official launcher ignores those errors, so we probably should do that as well. That function cleans up the mess
    # from raw response so error handling is still possible.
    if 'errors' in raw:
        for error in raw['errors'].copy():
            service_response = json.loads(error.get('serviceResponse', {}))
            if service_response and service_response.get('numericErrorCode') == 1004:
                raw['errors'].remove(error)
        if not raw['errors']:
            raw.pop('errors')
    return raw


class EpicGamesStoreAPI:
    """Class for interacting with EGS web API without user credentials TODO?."""

    def __init__(self, locale="en-US", country="US", session=None) -> None:
        """:param locale: EGS locale (this parameter depends on responses locale)
        :param country: EGS country
        """
        self._session = requests.Session() or session
        self.locale = locale
        self.country = country

    def get_product_mapping(self) -> dict:
        """Returns product mapping in {namespace: slug} format."""
        return self._make_api_query('/content/productmapping', method='GET')

    def get_product(self, slug: str) -> dict:
        """Returns a product's data by slug.

        :param slug: Product's slug.
        """
        return self._make_api_query(
            f'/content/products/{slug}',
            method='GET',
            use_locale=True,
        )

    def get_store(self) -> dict:
        """Returns a JSON data about store page."""
        return self._make_api_query('/content/store', method='GET', use_locale=True)

    def get_free_games(self, allow_countries: str | None = None) -> dict:
        """Returns the games from "Free Games" section in the EGS."""
        if allow_countries is None:
            allow_countries = self.country
        api_uri = (
            'https://store-site-backend-static.ak.epicgames.com/'
            f'freeGamesPromotions?locale={self.locale}&country={self.country}&allowCountries={allow_countries}'
        )
        data = _clean_1004_errors(self._session.get(api_uri).json())
        self._get_errors(data)
        return data

    def get_mver_status(self) -> bool:
        return self._make_api_query('/mver-status', method='GET')['result']

    def get_epic_store_status(self) -> dict:
        """Returns an Epic Games Store server status."""
        return self._session.get(
            'https://status.epicgames.com/api/v2/status.json',
        ).json()

    def get_offers_data(
        self,
        *offers: OfferData,
        should_calculate_tax: bool = False,
        include_sub_items: bool = False,
    ) -> dict:
        """Get offer(s) full data by offers' id and namespace.

        :param offers: Offers you need to get data from.
        :param should_calculate_tax: Should EGS API calculate tax for offers?
        :param include_sub_items: Should EGS API include sub-items for offers?
        """
        return self._make_graphql_query(
            OFFERS_QUERY,
            {},
            *[
                {
                    'productNamespace': offer.namespace,
                    'offerId': offer.offer_id,
                    'lineOffers': [{'offerId': offer.offer_id, 'quantity': 1}],
                    'calculateTax': should_calculate_tax,
                    'includeSubItems': include_sub_items,
                }
                for offer in offers
            ],
        )

    def get_collection(self, collection: EGSCollectionType) -> dict:
        """Returns games from the collection by the given collection type
        (see the documentation for CollectionType class).

        :param collection: Needed collection type.
        """
        # Cleanup for the 1004 errors that always pop up by default to not mess someone up by this.
        return _clean_1004_errors(
            self._make_graphql_query(
                COLLECTION_QUERY,
                slug=collection.value,
                # This query always returns 1004 error by default. That is not controlled by us and the error itself
                # is happening even in the official EGS client itself, they're just ignoring it, so we will too.
                suppress_errors=True,
            ),
        )

    def fetch_media(self, media_ref_id: str) -> dict:
        """Returns media-file (type of the file, its url and so on) by the
        file's media ref ID.

        :param media_ref_id: File's media ref ID.
        """
        return self._make_graphql_query(MEDIA_QUERY, mediaRefId=media_ref_id)

    def fetch_multiple_media_files(self, *media_ref_ids: str):
        """Equivalent to `fetch_media` function, except this one can fetch
        a few media files at the same moment (using only one request).
        """
        return self._make_graphql_query(
            MEDIA_QUERY,
            {},
            *[{'mediaRefId': media_ref_id} for media_ref_id in media_ref_ids],
        )

    def get_addons_by_namespace(
        self,
        namespace: str,
        categories: str = 'addons|digitalextras',
        count: int = 250,
        sort_by: str = 'releaseDate',
        sort_dir: str = 'DESC',
    ):
        """Returns product's addons by product's namespace.

        :param namespace: Product's namespace, can be obtained using the
        :meth:`epicstore_api.api.EpicGamesStoreAPI.get_product` function.

        :param categories: Addon's categories.
        :param count: Count of addon's you want EGS to give you.
        :param sort_by: By which key EGS should sort addons.
        :param sort_dir: You can use only **ASC** or **DESC**:

        - **ASC**: Sorts from higher ``sort_by`` parameter to lower;
        - **DESC**: Sorts from lower ``sort_by`` parameter to higher.
        """
        sort_dir = sort_dir.upper()
        if sort_dir not in ('ASC', 'DESC'):
            msg = (
                f'Parameter ``sort_dir`` have to be equals to'
                f' ASC or DESC, not to {sort_dir}'
            )
            raise ValueError(
                msg,
            )
        return self._make_graphql_query(
            ADDONS_QUERY,
            namespace=namespace,
            count=count,
            categories=categories,
            sortBy=sort_by,
            sortDir=sort_dir,
        )

    def get_product_reviews(self, product_sku: str) -> dict:
        """Returns product's reviews by product's sku.

        :param product_sku: SKU of the Product. Usually just slug of the
        product with `EPIC_` prefix.
        """
        try:
            return self._make_graphql_query(PRODUCT_REVIEWS_QUERY, sku=product_sku)
        except EGSNotFound as exc:
            exc.message = (
                'There are no reviews for this product, '
                f'or the given sku ({product_sku}) is incorrect.'
            )
            raise

    def fetch_prerequisites(self, *offers: OfferData) -> dict:
        """Fetches offer(s) prerequisites.

        :param offers: Offer(s) we need to get prerequisites from
        """
        return self._make_graphql_query(
            PREREQUISITES_QUERY,
            offerParams=[
                {'offerId': offer.offer_id, 'namespace': offer.namespace}
                for offer in offers
            ],  # OfferData -> dict for every offer in list
        )

    def fetch_feed(self, offset: int = 0, count: int = 10, category: str = '') -> dict:
        """Fetches Epic Games Store feed by given params.

        :param offset: From which news (index) we need to start.
        :param count: Count of the news we need to fetch.
        :param category: News categories.
        """
        return self._make_graphql_query(
            FEED_QUERY,
            offset=offset,
            countryCode=self.country,
            postsPerPage=count,
            category=category,
        )

    def fetch_catalog_tags(self, namespace: str = 'epic') -> dict:
        """Fetches tags for a products with namespace ``namespace``.

        :param namespace: Products' namespace (**epic** = all)
        """
        return self._make_graphql_query(CATALOG_TAGS_QUERY, namespace=namespace)

    def fetch_promotions(self, namespace: str = 'epic') -> dict:
        """Fetches a global promotions.

        :param namespace: Products' namespace (**epic** = all).
        """
        return self._make_graphql_query(PROMOTIONS_QUERY, namespace=namespace)

    def fetch_catalog(
        self,
        count: int = 30,
        product_type: EGSProductType | str = EGSProductType.ALL_PRODUCTS,
        namespace: str = 'epic',
        sort_by: str = 'effectiveDate',
        sort_dir: str = 'DESC',
        start: int = 0,
        keywords: str = '',
        categories: list[EGSCategory] | str | None = None,
    ) -> dict:
        """Fetches a catalog with given parameters.

        :param count: Count of  products you need to fetch.
        :param product_type: Product type(s) you need to get from EGS.
        :param namespace: Products namespace (epic = all namespaces).
        :param sort_by: Parameter which EGS will use to sort products.
        :param sort_dir: You can use only **ASC** or **DESC**:

        - **ASC**: Sorts from higher ``sort_by`` parameter to lower;
        - **DESC**: Sorts from lower ``sort_by`` parameter to higher.

        :param start: From which game EGS should start.
        :param keywords: Search keywords.
        :param categories: Categories you need to fetch.
        :rtype: dict
        :raises: ValueError  if ``sort_by`` not equals to **ASC** or **DESC**.
        """
        sort_dir = sort_dir.upper()
        if sort_dir not in ('ASC', 'DESC'):
            msg = (
                f'Parameter ``sort_dir`` have to be equals to'
                f' ASC or DESC, not to {sort_dir}'
            )
            raise ValueError(
                msg,
            )
        if categories is None:
            categories = ''
        else:
            categories = EGSCategory.join_categories(*categories)
        if isinstance(product_type, EGSProductType):
            product_type = product_type.value
        return self._make_graphql_query(
            CATALOG_QUERY,
            count=count,
            category=product_type,
            namespace=namespace,
            sortBy=sort_by,
            sortDir=sort_dir,
            start=start,
            keywords=keywords,
            tag=categories,
        )

    def fetch_store_games(
        self,
        count: int = 30,
        product_type: EGSProductType | str = EGSProductType.ALL_PRODUCTS,
        allow_countries: str = 'US',
        namespace: str = '',
        sort_by: str = 'title',
        sort_dir: str = 'ASC',
        release_date: str | None = None,
        start: int = 0,
        keywords: str = '',
        categories: list[EGSCategory] | str | None = None,
        *,
        with_price: bool = True,
    ) -> dict:
        """Fetches a store games with given parameters.

        :param count: Count of  products you need to fetch.
        :param product_type: Product type(s) you need to get from EGS.
        :param allow_countries: Products in the country. Default to 'US'.
        :param namespace: Products namespace ('' = all namespaces).
        :param sort_by: Parameter which EGS will use to sort products:

        - **releaseDate**:  Sorts by release date;
        - **title**: Sorts by game title, alphabetical.

        :param sort_dir: You can use only **ASC** or **DESC**:

        - **ASC**: Sorts from higher ``sort_by`` parameter to lower;
        - **DESC**: Sorts from lower ``sort_by`` parameter to higher.

        :param release_date: Available when ``sort_by`` is 'releaseDate'.

        - Date is in ISO 8601 format. General format: f'[{startDate}, {endDate}]'.
        - Example: '[2019-09-16T14:02:36.304Z, 2019-09-26T14:02:36.304Z]'
        - Leaving ``startDate`` or ``endDate`` blank will not limit start/end date.

        :param start: From which game EGS should start.
        :param keywords: Search keywords.
        :param categories: Categories you need to fetch.
        :param with_price: To fetch price or not.
        :rtype: dict
        :raises: ValueError  if ``sort_by`` not equals to **ASC** or **DESC**.
        """
        sort_dir = sort_dir.upper()
        if sort_dir not in ('ASC', 'DESC'):
            msg = (
                f'Parameter ``sort_dir`` have to be equals to'
                f' ASC or DESC, not to {sort_dir}'
            )
            raise ValueError(
                msg,
            )
        if categories is None:
            categories = ''
        else:
            categories = EGSCategory.join_categories(*categories)
        if isinstance(product_type, EGSProductType):
            product_type = product_type.value
        return self._make_graphql_query(  # This type of fetch needs headers.
            STORE_QUERY,
            headers={'content-type': 'application/json;charset=UTF-8'},
            count=count,
            category=product_type,
            allowCountries=allow_countries,
            namespace=namespace,
            sortBy=sort_by,
            sortDir=sort_dir,
            releaseDate=release_date,
            start=start,
            keywords=keywords,
            tag=categories,
            withPrice=with_price,
        )

    def _make_api_query(
        self,
        endpoint: str,
        method: str,
        *,
        use_locale: bool = False,
        **variables,
    ) -> dict:
        func = getattr(self._session, method.lower())
        base_url = 'https://store-content.ak.epicgames.com'
        base_url += '/api' if not use_locale else f'/api/{self.locale}'
        response = func(base_url + endpoint, data=variables)
        if response.status_code == 404:
            msg = f'Page with endpoint {endpoint} was not found'
            raise EGSException(msg)
        response = response.json()
        self._get_errors(response)
        return response

    def _make_graphql_query(
        self,
        query_string,
        headers=None,
        *multiple_query_variables,
        suppress_errors=False,
        **variables,
    ) -> dict:
        if headers is None:
            headers = {}
        if not multiple_query_variables:
            variables.update({'locale': self.locale, 'country': self.country})
            # This variables are default and exist in all graphql queries
            response = self._session.post(
                'https://graphql.epicgames.com/graphql',
                json={'query': query_string, 'variables': variables},
                headers=headers,
            ).json()
        else:
            data = []
            for variables in multiple_query_variables:
                variables_ = {
                    'locale': self.locale,
                    'country': self.country,
                }
                variables_.update(variables)
                data.append({'query': query_string, 'variables': variables_})
            response = self._session.post(
                'https://graphql.epicgames.com/graphql',
                json=data,
                headers=headers,
            ).json()
        if not suppress_errors:
            self._get_errors(response)
        return response

    @staticmethod
    def _get_errors(resp) -> None:
        r = []
        if not isinstance(resp, list):
            r.append(resp)
        for response in r:
            if response.get('errors'):
                error = response['errors'][0]
                if not error['serviceResponse']:
                    raise EGSException(error['message'], service_response=error)
                service_response = json.loads(error['serviceResponse'])
                if isinstance(service_response, dict):
                    if service_response['errorCode'].endswith('not_found'):
                        raise EGSNotFound(
                            service_response['errorMessage'],
                            service_response['numericErrorCode'],
                            service_response,
                        )
                elif (
                    isinstance(service_response, str)
                    and service_response == 'not found'
                ):
                    msg = (
                        'The resource was not found, '
                        'No more data provided by Epic Games Store.'
                    )
                    raise EGSNotFound(
                        msg,
                    )
                # FIXME: Need to handle more errors than the code is handling now
