# -*- coding: utf-8 -*-
"""
/***************************************************************************
 borrowed from serval,  A QGIS plugin


 Map tools for manipulating raster cell values

    begin            : 2015-12-30
    copyright        : (C) 2019 Radosław Pasiok for Lutra Consulting Ltd.
                        2024: modified by Jakub Charyton
    email            : info@lutraconsulting.co.uk
                        jakub.charyton@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtWidgets import QMessageBox, QPlainTextEdit
from qgis.core import QgsMessageLog, Qgis


class UserCommunication:
    """Class for communication with user"""

    def __init__(self, iface, context):
        self.iface = iface
        self.context = context

    def show_info(self, msg):
        QMessageBox.information(self.iface.mainWindow(), self.context, msg)

    def show_warn(self, msg):
        QMessageBox.warning(self.iface.mainWindow(), self.context, msg)

    def log_info(self, msg):
        QgsMessageLog.logMessage(msg, self.context, Qgis.Info)

    def bar_error(self, msg, dur=60):
        self.iface.messageBar().pushMessage(
            self.context, msg, level=Qgis.Critical, duration=dur
        )

    def bar_warn(self, msg, dur=5):
        self.iface.messageBar().pushMessage(
            self.context, msg, level=Qgis.Warning, duration=dur
        )

    def bar_info(self, msg, dur=5):
        self.iface.messageBar().pushMessage(
            self.context, msg, level=Qgis.Info, duration=dur
        )

    def clear_bar_messages(self):
        self.iface.messageBar().clearWidgets()


class WidgetPlainTextWriter:
    """Class for writing text to PlainTextEdit Widget"""

    def __init__(self, plain_text_widget: QPlainTextEdit):
        self.plain_text_widget: QPlainTextEdit = plain_text_widget

    def write_info(self, msg: str):
        self.plain_text_widget.appendPlainText(f"[INFO]: {msg}")

    def write_warn(self, msg: str):
        self.plain_text_widget.appendPlainText(f"[WARNING]: {msg}")

    def write_error(self, msg: str):
        self.plain_text_widget.appendPlainText(f"[ERROR]: {msg}")
