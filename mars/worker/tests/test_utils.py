# Copyright 1999-2018 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import unittest

import numpy as np

from mars.worker.utils import ExpMeanHolder, ExpiringCache


class Test(unittest.TestCase):
    def testExpMeanHolder(self):
        holder = ExpMeanHolder(0.8)
        values = np.array([5, 4, 1, 3, 2])
        coeffs = np.power(0.8, np.arange(len(values)))[::-1]

        self.assertEqual(holder.count(), 0)
        self.assertEqual(holder.mean(), 0)
        self.assertEqual(holder.var(), 0)
        self.assertEqual(holder.std(), 0)

        for v in values:
            holder.put(v)

        coeff_v = values * coeffs
        coeff_v2 = values * values * coeffs

        coeff_mean = coeff_v.sum() / coeffs.sum()
        self.assertAlmostEqual(coeff_mean, holder.mean())

        coeff_var = coeff_v2.sum() / coeffs.sum() - coeff_mean ** 2
        self.assertAlmostEqual(coeff_var, holder.var())
        self.assertAlmostEqual(np.sqrt(coeff_var), holder.std())

    def testExpiringCache(self):
        cache = ExpiringCache(_expire_time=0.5)
        cache['v1'] = 1
        cache['v2'] = 2

        time.sleep(0.2)
        cache['v2'] = 2
        self.assertIn('v1', cache)
        self.assertIn('v2', cache)

        time.sleep(0.4)
        cache['v3'] = 3
        self.assertNotIn('v1', cache)
        self.assertIn('v2', cache)
        self.assertIn('v3', cache)
