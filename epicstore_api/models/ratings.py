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

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ESRBRatingCode(Enum):
    """Standard ESRB (Entertainment Software Rating Board) rating codes."""
    EC = "EC"
    E = "E"
    E10_PLUS = "E10+"
    T = "T"
    M = "M"
    AO = "AO"
    RP = "RP"


@dataclass
class ESRBRating:
    """Represents the ESRB rating of a game.

    Attributes:
        rating: ESRB rating code (EC, E, E10+, T, M, AO, RP)
        descriptors: List of content descriptors (e.g., Blood, Violence, Nudity)
        raw_data: Original data from the API as reference point
    """
    rating: Optional[str] = None
    descriptors: list[str] = None
    raw_data: Optional[list | dict] = None

    def __post_init__(self):
        if self.descriptors is None:
            self.descriptors = []

