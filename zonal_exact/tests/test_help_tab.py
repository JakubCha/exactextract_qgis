import pytest

from qgis.core import (
    QgsProject,
)

from zonal_exact.zonal_exact_dialog import ZonalExactDialog
from zonal_exact.user_communication import UserCommunication

@pytest.fixture
def dialog(qgis_iface, qgis_app):
    # Create a ZonalExactDialog instance
    dialog = ZonalExactDialog(
        iface=qgis_iface,
        project=QgsProject.instance(),
        task_manager=qgis_app.taskManager(),
        uc=UserCommunication(qgis_iface, "Zonal ExactExtract"),
    )
    yield dialog
    
def test_help_tab_exists(dialog):
    # Open the help tab
    dialog.tabWidget.setCurrentIndex(1)
    dialog.tabWidget.show()
    
    # Check if the help tab is visible
    assert dialog.tabWidget.currentWidget().objectName() == "helpTab"

def test_help_browser_exists(dialog):
    assert dialog.helpTextBrowser.objectName() == "helpTextBrowser"

def test_help_tab_content(dialog):
    # Open the help tab
    dialog.tabWidget.setCurrentIndex(1)
    
    # Check if the help tab contains the expected content
    assert dialog.helpTextBrowser.toPlainText().split("\n")[0] == "Help"
    