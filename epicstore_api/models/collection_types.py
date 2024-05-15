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

from enum import Enum


class EGSCollectionType(Enum):
    """A helper enum that is used for the collections query
    (see :meth:`epicstore_api.api.EpicGamesStoreAPI.get_collection`). You can see the game that fall under particular
    collections under the free games on the main page of the Epic Games Store. Collections that are not included
    (such as New Releases and Coming Soon can be obtained through catalog query with specific sort queries such as
    sortBy=releaseDate and sortBy=comingSoon).
    """

    TOP_SELLERS = "top-sellers"
    MOST_PLAYED = "most-played"
    TOP_UPCOMING_WISHLISTED = "top-wishlisted"
    MOST_POPULAR = "most-popular"
    TOP_PLAYER_RATED = "top-player-reviewed"
