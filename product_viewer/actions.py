# coding: utf-8
import sys

from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QFileDialog

from product_viewer.loader import YMLLoader


class ExitAction(QAction):
    def __init__(self, *args):
        super(ExitAction, self).__init__(*args)

        self.setStatusTip('Exit product viewer')
        self.triggered.connect(lambda: sys.exit())


class UploadAction(QAction):
    """Handles uploading of yml file."""

    def __init__(self, *args):
        super(UploadAction, self).__init__(*args)
        self.setStatusTip('Upload new YML file')
        self.triggered.connect(self.handler)

    def handler(self):
        """YML loader parses file, result stored in RedisStore."""

        filename, filetype_mask = QFileDialog().getOpenFileName(
            caption='Select YML file',
            filter='XML Files (*.xml)')

        # Closing QFileDialog sets
        # filename to empty string
        if not filename:
            return

        loader = YMLLoader(filename)
        for offer in loader.offers:
            self.parent().store.dump(
                offer.id, (
                    offer.name,
                    offer.category,
                    '{} {}'.format(offer.price, offer.currency)))
