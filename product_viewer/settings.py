# coding: utf-8
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout

SETTINGS = QSettings('robotehnik', 'Product Viewer')


class RedisSettingsForm(QGroupBox):
    def __init__(self, *args):
        super(RedisSettingsForm, self).__init__(*args)
        layout = QFormLayout()

        self.host = QLineEdit(SETTINGS.value('redis/host', 'localhost', str))
        self.port = QLineEdit(SETTINGS.value('redis/port', '6379', str))
        self.db = QLineEdit(SETTINGS.value('redis/db', '0', str))

        layout.addRow(QLabel('Host:'), self.host)
        layout.addRow(QLabel('Port:'), self.port)
        layout.addRow(QLabel('DB Number:'), self.db)

        self.setLayout(layout)


class SettingsDialog(QDialog):
    def __init__(self, *args):
        super(SettingsDialog, self).__init__(*args)
        self.setWindowTitle('Preferences')
        buttons = QDialogButtonBox(
            QDialogButtonBox.Save |
            QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.form = RedisSettingsForm('Redis database')
        layout = QVBoxLayout()
        layout.addWidget(self.form)
        layout.addWidget(buttons)
        self.setLayout(layout)


class SettingsAction(QAction):
    def __init__(self, *args):
        super(SettingsAction, self).__init__(*args)
        self.setStatusTip('Edit preferences')
        self.triggered.connect(self.handler)

    def handler(self):
        """Saves settings on save action."""

        dialog = SettingsDialog(self.parent())
        if dialog.exec_():
            SETTINGS.setValue('redis/host', dialog.form.host.text())
            SETTINGS.setValue('redis/port', dialog.form.port.text())
            SETTINGS.setValue('redis/db', dialog.form.db.text())
