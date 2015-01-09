#!/usr/bin/env python
# This file is part of product_price_with_tax module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.tests.test_tryton import test_view, test_depends
import trytond.tests.test_tryton
import unittest


class ProductPriceWithTaxTestCase(unittest.TestCase):
    'Test Product Price With Tax module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('product_price_with_tax')

    def test0005views(self):
        'Test views'
        test_view('product_price_with_tax')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPriceWithTaxTestCase))
    return suite
