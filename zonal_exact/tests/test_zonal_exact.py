from zonal_exact.zonal_exact import ZonalExact


def test_plugin_init(qgis_iface):
    # Test the run method of the dialog
    plugin = ZonalExact(qgis_iface)
    plugin.initGui(add_to_menu=False)

    assert plugin.first_start is True
