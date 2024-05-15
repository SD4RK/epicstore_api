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


class EGSCategory(Enum):
    """Class that provides a code for every category in the EGS with
    a human-readable name and a few useful methods.

    .. note::
      Here you can see only that categories that are displayed in EGS,
      for other categories you can call an API function
      :meth:`epicstore_api.api.EpicGamesStoreAPI.fetch_catalog_tags`
    """

    CATEGORY_ACTION = "1216"  #: Action games
    CATEGORY_EDITOR = "9559"  #: Editors for games
    CATEGORY_ADVENTURE = "1117"  #: Adventure games
    CATEGORY_PUZZLE = "1298"  #: Puzzle games
    CATEGORY_RACING = "1212"  #: Racing games
    CATEGORY_RPG = "1367"  #: RPG games
    CATEGORY_SHOOTER = "1210"  #: Shooter games
    CATEGORY_STRATEGY = "1115"  #: Strategy games
    CATEGORY_SURVIVAL = "1080"  #: Survival games
    CATEGORY_OSX = "9548"  #: Games for OSX (Mac OS)
    CATEGORY_WINDOWS = "9547"  #: Games for Windows
    CATEGORY_SINGLE_PLAYER = "1370"  #: Single-player games
    CATEGORY_MULTIPLAYER = "1203"  #: Multiplayer games

    @staticmethod
    def join_categories(*categories_list) -> str:
        """Joins the given categories into a string for EGS API queries
        :param categories_list: list of categories you need
        :type categories_list: List[EGSCategory]
        :rtype: str.
        """
        return '|'.join([category.value for category in categories_list])

    def __add__(self, other):
        if isinstance(other, EGSCategory):
            return self.join_categories(self, other)
        raise NotImplementedError
