# coding: utf-8
from typing import Iterator
from lxml import etree

from collections import namedtuple

Item = namedtuple('Item', 'id, name, category, price, currency')


class YMLLoader:
    """REsponsible for parsing YML file."""

    def __init__(self, filename: str):
        with open(filename) as f:
            self.tree = etree.fromstring(f.read().encode())

        # Mapping with categories like {<id>: <category name>}
        self.categories = dict(
            (category.get('id'), category.text)
            for category in self.tree.findall('.//category'))

    @staticmethod
    def _get_name(offer_tag: etree._Element) -> str:
        """Returns product name."""

        name = offer_tag.find('name')
        if name is not None:
            name = name.text
        else:
            # Tries to combine name from prefix,
            # vendor and model
            name = ' '.join(
                o.text for o in (
                    offer_tag.find('typePrefix'),
                    offer_tag.find('vendor'),
                    offer_tag.find('model')
                ) if o is not None)
        return name

    @property
    def offers(self) -> Iterator[Item]:
        for offer in self.tree.findall('.//offer'):
            yield Item(
                id=offer.get('id'),
                name=self._get_name(offer),
                category=self.categories.get(
                    offer.find('categoryId').text, ''),
                price=offer.find('price').text,
                currency=offer.find('currencyId').text,
            )