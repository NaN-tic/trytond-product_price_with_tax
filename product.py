# This file is part of product_price_with_tax module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from trytond.config import config
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['Template']
__metaclass__ = PoolMeta

STATES = {
    'readonly': ~Eval('active', True),
    }
DEPENDS = ['active']
DIGITS = int(config.get('digits', 'unit_price_digits', 4))


class Template:
    __name__ = "product.template"
    list_price_with_tax = fields.Property(fields.Numeric('List Price With Tax',
            states=STATES, digits=(16, DIGITS), depends=DEPENDS, required=True)
            )
    cost_price_with_tax = fields.Property(fields.Numeric('Cost Price With Tax',
            states=STATES, digits=(16, DIGITS), depends=DEPENDS, required=True)
            )

    @fields.depends('list_price')
    def on_change_list_price(self):
        pool = Pool()
        Tax = pool.get('account.tax')
        try:
            changes = super(Template, self).on_change_list_price()
        except AttributeError:
            changes = {}
        if self.list_price:
            taxes = [Tax(t) for t in self.get_taxes('customer_taxes')]
            taxes = Tax.compute(taxes, self.list_price, 1.0)
            tax_amount = sum([t['amount'] for t in taxes], Decimal('0.0'))
            changes['list_price_with_tax'] = self.list_price + tax_amount
        return changes

    @fields.depends('list_price_with_tax')
    def on_change_list_price_with_tax(self):
        pool = Pool()
        Tax = pool.get('account.tax')
        try:
            changes = super(Template, self).on_change_list_price_with_tax()
        except AttributeError:
            changes = {}
        if self.list_price_with_tax:
            taxes = [Tax(t) for t in self.get_taxes('customer_taxes')]
            tax_amount = Tax.reverse_compute(self.list_price_with_tax, taxes)
            changes['list_price'] = tax_amount.quantize(
                Decimal(str(10.0 ** -DIGITS)))
        return changes

    @fields.depends('cost_price')
    def on_change_cost_price(self):
        pool = Pool()
        Tax = pool.get('account.tax')
        try:
            changes = super(Template, self).on_change_cost_price()
        except AttributeError:
            changes = {}
        if self.cost_price:
            taxes = [Tax(t) for t in self.get_taxes('supplier_taxes')]
            taxes = Tax.compute(taxes, self.cost_price, 1.0)
            tax_amount = sum([t['amount'] for t in taxes], Decimal('0.0'))
            changes['cost_price_with_tax'] = self.cost_price + tax_amount
        return changes

    @fields.depends('cost_price_with_tax')
    def on_change_cost_price_with_tax(self):
        pool = Pool()
        Tax = pool.get('account.tax')
        try:
            changes = super(Template, self).on_change_cost_price_with_tax()
        except AttributeError:
            changes = {}
        if self.cost_price_with_tax:
            taxes = [Tax(t) for t in self.get_taxes('supplier_taxes')]
            tax_amount = Tax.reverse_compute(self.cost_price_with_tax, taxes)
            changes['cost_price'] = tax_amount.quantize(
                Decimal(str(10.0 ** -DIGITS)))
        return changes
