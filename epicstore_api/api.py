# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2020 SD4RK

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
import requests
from typing import Union, List, NamedTuple
from .exc import EGSNotFound, EGSException
from .models import EGSCategory, EGSProductType
from .queries import (CATALOG_QUERY,
                      PROMOTIONS_QUERY,
                      CATALOG_TAGS_QUERY,
                      FEED_QUERY,
                      PREREQUISITES_QUERY,
                      OFFERS_QUERY)


class OfferData(NamedTuple):
    namespace: str
    offer_id: str


__all__ = ['EpicGamesStoreAPI', 'OfferData']


class EpicGamesStoreAPI:
    """
    Class for interacting with EGS web API without user credentials TODO?
    """
    def __init__(self, locale="en-US", country="US", session=None):
        """
        :param locale: EGS locale (this parameter depends on responses locale)
        :param country: EGS country
        """
        self._session = requests.Session() or session
        self.locale = locale
        self.country = country

    def get_product_mapping(self) -> dict:
        """
        Returns product mapping in {namespace: slug} format
        """
        return self._make_api_query(
            '/content/productmapping', method='GET'
        )

    def get_product(self, slug: str) -> dict:
        """
        Returns a product's data by slug

        :param slug: Product's slug
        """
        return self._make_api_query(
            f'/content/products/{slug}', method='GET', use_locale=True
        )

    def get_store(self) -> dict:
        """
        Returns a JSON data about store page
        """
        return self._make_api_query(
            '/content/store', method='GET'
        )

    def get_mver_status(self) -> bool:
        return self._make_api_query(
            '/mver-status', method='GET'
        )['result']

    def get_epic_store_status(self) -> dict:
        """
        Returns an Epic Games Store server status
        """
        return self._session.get(
            'https://status.epicgames.com/api/v2/status.json'
        ).json()

    def get_offers_data(
        self,
        *offers: OfferData,
        should_calculate_tax: bool = False
    ) -> dict:
        """
        Get offer(s) full data by offers' id and namespace

        :param offers: Offers you need to get data from
        :param should_calculate_tax: Should EGS API calculate tax for offers?
        """
        return self._make_graphql_query(
            OFFERS_QUERY,
            *[{
                'productNamespace': offer.namespace,
                'offerId': offer.offer_id,
                'lineOffers': [{
                    'offerId': offer.offer_id,
                    'quantity': 1
                }],
                'calculateTax': should_calculate_tax
            } for offer in offers]
        )

    def fetch_prerequisites(self, *offers: OfferData) -> dict:
        """
        Fetches offer(s) prerequisites

        :param offers: Offer(s) we need to get prerequisites from
        """
        return self._make_graphql_query(
            PREREQUISITES_QUERY,
            offerParams=[{
                'offerId': offer.offer_id,
                'namespace': offer.namespace
            } for offer in offers]  # OfferData -> dict for every offer in list
        )

    def fetch_feed(
        self,
        offset: int = 0,
        count: int = 10,
        category: str = ''
    ) -> dict:
        """
        Fetches Epic Games Store feed by given params

        :param offset: From which news (index) we need to start
        :param count: Count of the news we need to fetch
        :param category: News categories
        """
        return self._make_graphql_query(
            FEED_QUERY,
            offset=offset,
            countryCode=self.country,
            postsPerPage=count,
            category=category
        )

    def fetch_catalog_tags(self, namespace: str = 'epic') -> dict:
        """
        Fetches tags for a products with namespace ``namespace``

        :param namespace: Products' namespace (**epic** = all)
        """
        return self._make_graphql_query(
            CATALOG_TAGS_QUERY,
            namespace=namespace
        )

    def fetch_promotions(self, namespace: str = 'epic') -> dict:
        """
        Fetches a global promotions

        :param namespace: Products' namespace (**epic** = all)
        """
        return self._make_graphql_query(
            PROMOTIONS_QUERY,
            namespace=namespace
        )

    def fetch_catalog(
        self,
        count: int = 30,
        product_type: Union[EGSProductType, str] = EGSProductType.ALL_PRODUCTS,
        namespace: str = 'epic',
        sort_by: str = 'effectiveDate',
        sort_dir: str = 'DESC',
        start: int = 0,
        keywords: str = '',
        categories: List[EGSCategory] = None
    ) -> dict:
        """
        Fetches a catalog with given parameters

        :param count: Count of  products you need to fetch
        :param product_type: Product type(s) you need to get from EGS
        :param namespace: Products namespace (epic = all namespaces)
        :param sort_by: Parameter which EGS will use to sort products
        :param sort_dir: You can use only **ASC** or **DESC**:

        - **ASC**: Sorts from higher ``sort_by`` parameter to lower
        - **DESC**: Sorts from lower ``sort_by`` parameter to higher

        :param start: From which game EGS should start
        :param keywords: Search keywords
        :param categories: Categories you need to fetch
        :rtype: dict
        :raises: ValueError  if ``sort_by`` not equals to **ASC** or **DESC**
        """
        sort_dir = sort_dir.upper()
        if sort_dir not in ('ASC', 'DESC'):
            raise ValueError(f'Parameter ``sort_dir`` have to be equals to'
                             f' ASC or DESC, not to {sort_dir}')
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
            tag=categories
        )

    def _make_api_query(
        self,
        endpoint: str,
        method: str,
        use_locale: bool = False,
        **variables
    ) -> dict:
        func = getattr(self._session, method.lower())
        base_url = 'https://www.epicgames.com/store'
        base_url += '/api' if not use_locale else f'/{self.locale}/api'
        response = func(
            base_url + endpoint,
            json=variables
        )
        if response.status_code == 404:
            raise EGSException(f'Page with endpoint {endpoint} was not found')
        response = response.json()
        self._get_errors(response)
        return response

    def _make_graphql_query(
        self,
        query_string,
        *multiple_query_variables,
        **variables
    ) -> dict:
        if not multiple_query_variables:
            variables.update({'locale': self.locale, 'country': self.country})
            # This variables are default and exist in all graphql queries
            response = self._session.post(
                'https://graphql.epicgames.com/graphql',
                json={'query': query_string, 'variables': variables}
            ).json()
        else:
            data = []
            for variables in multiple_query_variables:
                variables_ = {
                    'locale': self.locale,
                    'country': self.country,
                }
                variables_.update(variables)
                data.append({
                    'query': query_string,
                    'variables': variables_
                })
            response = self._session.post(
                'https://graphql.epicgames.com/graphql',
                json=data
            ).json()
        self._get_errors(response)
        return response

    @staticmethod
    def _get_errors(resp):
        r = []
        if not isinstance(resp, list):
            r.append(resp)
        for response in r:
            if response.get('errors'):
                error = response['errors'][0]
                if not error['serviceResponse']:
                    raise EGSException(
                        error['message'],
                        service_response=error
                    )
                service_response = json.loads(
                    error['serviceResponse']
                )
                if service_response['errorCode'].endswith('not_found'):
                    raise EGSNotFound(
                        service_response['errorMessage'],
                        service_response['numericErrorCode'],
                        service_response
                    )
                # FIXME: Need to handle more errors than the code is handling now
