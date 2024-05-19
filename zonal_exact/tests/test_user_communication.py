import pytest_qgis
from qgis.core import Qgis

from zonal_exact.user_communication import UserCommunication


def test_init_uc(qgis_iface):
    uc = UserCommunication(qgis_iface, "Zonal ExactExtract")

    assert isinstance(uc.iface, pytest_qgis.qgis_interface.QgisInterface)
    assert uc.context == "Zonal ExactExtract"


def test_bar_error(qgis_iface):
    uc = UserCommunication(qgis_iface, "Zonal ExactExtract")

    msg = "example error message"
    uc.bar_error(msg=msg, dur=15)
    returned_message = qgis_iface.messageBar().messages.get(Qgis.Critical)
    assert returned_message == [f"Zonal ExactExtract:{msg}"]


def test_bar_warn(qgis_iface):
    uc = UserCommunication(qgis_iface, "Zonal ExactExtract")

    msg = "example warn message"
    uc.bar_warn(msg=msg, dur=15)
    returned_message = qgis_iface.messageBar().messages.get(Qgis.Warning)
    assert returned_message == [f"Zonal ExactExtract:{msg}"]


def test_bar_info(qgis_iface):
    uc = UserCommunication(qgis_iface, "Zonal ExactExtract")

    msg = "example info message"
    uc.bar_info(msg=msg, dur=15)
    returned_message = qgis_iface.messageBar().messages.get(Qgis.Info)
    assert returned_message == [f"Zonal ExactExtract:{msg}"]
