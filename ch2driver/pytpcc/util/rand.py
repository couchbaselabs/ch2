# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Copyright (C) 2011
# Andy Pavlo
# http://www.cs.brown.edu/~pavlo/
#
# Original Java Version:
# Copyright (C) 2008
# Evan Jones
# Massachusetts Institute of Technology
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------------------

import random
import string

import constants
import numpy as np

from . import nurand

SYLLABLES = [ "BAR", "OUGHT", "ABLE", "PRI", "PRES", "ESE", "ANTI", "CALLY", "ATION", "EING" ]

NP_ALPHANUMERIC = np.array(list(string.ascii_letters + string.digits))


class Rand:

    def __init__(self, datagenSeed=None):
        self.nurandVar = None # NURand
        self.rng = random.Random()
        self.nprng = np.random.default_rng()
        if datagenSeed is not None and datagenSeed != constants.CH2_DATAGEN_SEED_NOT_SET:
            self.rng.seed(datagenSeed)
            self.nprng = np.random.default_rng(datagenSeed)

        self.random_bytes_for_astring = self._gen_random_bytes_for_astring()
        self.astring_randint_idx = 0
        self.random_bytes_for_nstring = self._gen_random_bytes_for_nstring()
        self.nstring_randint_idx = 0

    def setNURand(self, nu):
        self.nurandVar = nu
    ## DEF

    def nuRand(self, a, x, y):
        """Return non-uniform random number, as defined by TPC-C 2.1.6. (page 20)."""
        assert x <= y
        #    assert nurand != None
        if self.nurandVar is None:
            self.setNURand(nurand.makeForLoad(self.rng))
        if a == 255:
            c = self.nurandVar.cLast
        elif a == 1023:
            c = self.nurandVar.cId
        elif a == 8191:
            c = self.nurandVar.orderLineItemId
        else:
            raise Exception("a = " + a + " is not a supported value")

        return (((self.number(0, a) | self.number(x, y)) + c) % (y - x + 1)) + x
    ## DEF

    def number(self, minimum, maximum):
        value = int(self.rng.random() * (maximum - minimum + 1)) + minimum
        assert minimum <= value and value <= maximum
        return value
    ## DEF

    def numberExcluding(self, minimum, maximum, excluding):
        """Return number in the range [`minimum`, `maximum`], excluding `excluding`."""
        assert minimum < maximum
        assert minimum <= excluding and excluding <= maximum

        ## Generate 1 less number than the range
        num = self.number(minimum, maximum-1)

        ## Adjust the numbers to remove excluding
        if num >= excluding:
            num += 1
        assert minimum <= num and num <= maximum and num != excluding
        return num
    ## DEF

    def fixedPoint(self, decimal_places, minimum, maximum):
        assert decimal_places > 0
        assert minimum < maximum

        multiplier = 10**decimal_places
        int_min = int(minimum * multiplier + 0.5)
        int_max = int(maximum * multiplier + 0.5)

        return float(self.number(int_min, int_max) / float(multiplier))
    ## DEF

    def selectUniqueIds(self, numUnique, minimum, maximum):
        rows = set()
        for i in range(0, numUnique):
            index = None
            while index is None or index in rows:
                index = self.number(minimum, maximum)
            ## WHILE
            rows.add(index)
        ## FOR
        assert len(rows) == numUnique
        return rows
    ## DEF

    def _gen_random_bytes_for_astring(self):
        # ord('a') = 97, ord('z') = 122
        return self.nprng.integers(97, 123, size=10_000_000, dtype="int32").view("U1")

    def _maybe_refresh_random_bytes_for_astring(self, astring_len):
        if self.astring_randint_idx + astring_len >= self.random_bytes_for_astring.size:
            self.random_bytes_for_astring = self._gen_random_bytes_for_astring()
            self.astring_randint_idx = 0

    def astring(self, minimum_length, maximum_length):
        """Return random alphabetic string with length in range [`minimum_length`, `maximum_length`]."""
        length = self.number(minimum_length, maximum_length)
        self._maybe_refresh_random_bytes_for_astring(length)
        next_astring_idx = self.astring_randint_idx + length

        string = (
            self.random_bytes_for_astring[self.astring_randint_idx : next_astring_idx]
            .view("U%d" % length)
            .item()
        )
        self.astring_randint_idx = next_astring_idx
        return string

    ## DEF

    def _gen_random_bytes_for_nstring(self):
        # ord('0') = 48, ord('9') = 57
        return self.nprng.integers(48, 58, size=10_000_000, dtype="int32").view("U1")

    def _maybe_refresh_random_bytes_for_nstring(self, nstring_len):
        if self.nstring_randint_idx + nstring_len >= self.random_bytes_for_nstring.size:
            self.random_bytes_for_nstring = self._gen_random_bytes_for_nstring()
            self.nstring_randint_idx = 0

    def nstring(self, minimum_length, maximum_length):
        """Return random numeric string with length in range [`minimum_length`, `maximum_length`]."""
        length = self.number(minimum_length, maximum_length)
        self._maybe_refresh_random_bytes_for_nstring(length)
        next_nstring_idx = self.nstring_randint_idx + length

        string = (
            self.random_bytes_for_nstring[self.nstring_randint_idx : next_nstring_idx]
            .view("U%d" % length)
            .item()
        )
        self.nstring_randint_idx = next_nstring_idx
        return string
    ## DEF

    def randomStringMinMax(self, minimum_length, maximum_length):
        length = self.number(minimum_length, maximum_length)
        return self.randomStringLength(length)
    ## DEF

    def randomStringLength(self, length):
    # With combination of lower and upper case and digits
        return self.nprng.choice(NP_ALPHANUMERIC, length).view("U%d" % length).item()
    ## DEF

    def randomStringsWithEmbeddedSubstrings(self, minimum_length, maximum_length, substr1, substr2):
        lenSubstr1 = len(substr1)
        lenSubstr2 = len(substr2)
        rlength = 0
        while rlength < lenSubstr1 + lenSubstr2:
            rlength = self.number(minimum_length, maximum_length)
        l1 = self.number(0, rlength - lenSubstr1 - lenSubstr2)
        l2 = self.number(0, rlength - l1 - lenSubstr1 - lenSubstr2)
        l3 = rlength - l1 - l2 - lenSubstr1 - lenSubstr2
        return (
            self.randomStringLength(l1)
            if l1
            else "" + substr1 + self.randomStringLength(l2)
            if l2
            else "" + substr2 + self.randomStringLength(l3)
        )
    ## DEF

    def makeLastName(self, number):
        """Return last name as defined by TPC-C 4.3.2.3. Not actually random."""
        global SYLLABLES
        assert 0 <= number and number <= 999
        indicies = [ int(number/100), int((number/10)%10), int(number%10) ]
        return "".join(map(lambda x: SYLLABLES[x], indicies))
    ## DEF

    def makeRandomLastName(self, maxCID):
        """Return non-uniform random last name, as defined by TPC-C 4.3.2.3.

        The name will be limited to `maxCID`.
        """
        min_cid = 999
        if (maxCID - 1) < min_cid:
            min_cid = maxCID - 1
        return self.makeLastName(self.nuRand(255, 0, min_cid))
    ## DEF
## CLASS

