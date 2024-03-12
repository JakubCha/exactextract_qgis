import os
import time
import timeit

import psycopg2
import pytest
from PyQt5.QtCore import QSettings
from qgis.core import (QgsProject, QgsApplication, QgsVectorLayer, QgsDataSourceUri, QgsRelation, QgsRelationManager)

# noinspection PyArgumentList
QGIS_INSTANCE = QgsProject.instance()

