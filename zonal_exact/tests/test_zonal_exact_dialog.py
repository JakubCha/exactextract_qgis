import pytest

from qgis.core import QgsProject

from zonal_exact.zonal_exact_dialog import ZonalExactDialog


@pytest.fixture
def dialog(qgis_iface):
    # Create a ZonalExactDialog instance
    return ZonalExactDialog(
        uc=None, iface=qgis_iface, task_manager=None, project=QgsProject.instance()
    )


def test_dialog_creation(dialog):
    # Test if the dialog is created successfully
    assert isinstance(dialog, ZonalExactDialog)


def test_dialog_show(dialog):
    # Test if the dialog can be shown and properly closed
    dialog.show()
    assert dialog.isVisible()
    dialog.close()
    assert dialog.isVisible() is False
