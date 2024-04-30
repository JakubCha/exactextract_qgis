import pytest
from pathlib import Path

from qgis.core import QgsProject, QgsApplication

from zonal_exact.zonal_exact_dialog import ZonalExactDialog
from zonal_exact.user_communication import UserCommunication


@pytest.fixture
def dialog(qgis_iface):
    # Create a ZonalExactDialog instance
    dialog = ZonalExactDialog(
        iface=qgis_iface,
        project=QgsProject.instance(),
        task_manager=QgsApplication.taskManager(),
        uc=UserCommunication(qgis_iface, "Zonal ExactExtract"),
    )
    yield dialog
    dialog.close()


def test_dialog_creation(dialog):
    # Test if the dialog is created successfully
    assert isinstance(dialog, ZonalExactDialog)


def test_dialog_show(dialog):
    # Test if the dialog can be shown and properly closed
    dialog.show()
    assert dialog.isVisible()
    dialog.close()
    assert dialog.isVisible() is False


def test_control_input_valid_parameters(dialog, setup_layers):
    # Test if the control_input method processes valid parameters correctly
    vector_layer, _ = setup_layers

    dialog.temp_index_field = "fid"
    raster_layers_path = "/path/to/raster"
    output_file_path = Path("/path/to/output.csv")
    aggregates_stats_list = ["mean"]
    arrays_stats_list = []

    dialog.control_input(
        raster_layers_path,
        vector_layer,
        output_file_path,
        aggregates_stats_list,
        arrays_stats_list,
    )
    # Assert that no exception is raised


def test_control_input_missing_raster_layer(dialog, setup_layers):
    # Test if the control_input method raises an exception when raster layer is missing
    vector_layer, _ = setup_layers

    dialog.temp_index_field = "fid"
    raster_layers_path = ""
    output_file_path = Path("/path/to/output.csv")
    aggregates_stats_list = ["mean"]
    arrays_stats_list = []

    with pytest.raises(
        ValueError, match="You didn't select raster layer or vector layer"
    ):
        dialog.control_input(
            raster_layers_path,
            vector_layer,
            output_file_path,
            aggregates_stats_list,
            arrays_stats_list,
        )


def test_control_input_missing_vector_layer(dialog):
    # Test if the control_input method raises an exception when vector layer is missing
    raster_layers_path = "/path/to/raster"
    dialog.temp_index_field = "fid"
    vector_layer = None
    output_file_path = Path("/path/to/output.csv")
    aggregates_stats_list = ["mean"]
    arrays_stats_list = []

    with pytest.raises(
        ValueError, match="You didn't select raster layer or vector layer"
    ):
        dialog.control_input(
            raster_layers_path,
            vector_layer,
            output_file_path,
            aggregates_stats_list,
            arrays_stats_list,
        )


def test_control_input_missing_id_field(dialog, setup_layers):
    # Test if the control_input method raises an exception when ID field is missing
    vector_layer, _ = setup_layers

    raster_layers_path = "/path/to/raster"
    output_file_path = Path("/path/to/output.csv")
    aggregates_stats_list = ["mean"]
    arrays_stats_list = []

    with pytest.raises(ValueError, match="You didn't select ID field"):
        dialog.control_input(
            raster_layers_path,
            vector_layer,
            output_file_path,
            aggregates_stats_list,
            arrays_stats_list,
        )


def test_control_input_missing_output_file_path(dialog, setup_layers):
    # Test if the control_input method raises an exception when output file path is missing
    vector_layer, _ = setup_layers

    raster_layers_path = "/path/to/raster"
    dialog.temp_index_field = "fid"
    output_file_path = None
    aggregates_stats_list = ["mean"]
    arrays_stats_list = []

    with pytest.raises(ValueError, match="You didn't select output file path"):
        dialog.control_input(
            raster_layers_path,
            vector_layer,
            output_file_path,
            aggregates_stats_list,
            arrays_stats_list,
        )


def test_control_input_invalid_output_file_extension(dialog, setup_layers):
    # Test if the control_input method raises an exception when output file extension is invalid
    vector_layer, _ = setup_layers

    raster_layers_path = "/path/to/raster"
    dialog.temp_index_field = "fid"
    output_file_path = Path("/path/to/output.txt")
    aggregates_stats_list = ["mean"]
    arrays_stats_list = []

    with pytest.raises(ValueError, match="Allowed output formats are *"):
        dialog.control_input(
            raster_layers_path,
            vector_layer,
            output_file_path,
            aggregates_stats_list,
            arrays_stats_list,
        )


def test_control_input_missing_stats_lists(dialog, setup_layers):
    # Test if the control_input method raises an exception when both stats lists are empty
    vector_layer, _ = setup_layers

    raster_layers_path = "/path/to/raster"
    dialog.temp_index_field = "fid"
    output_file_path = Path("/path/to/output.csv")
    aggregates_stats_list = []
    arrays_stats_list = []

    with pytest.raises(
        ValueError, match="You didn't select anything from either Aggregates and Arrays"
    ):
        dialog.control_input(
            raster_layers_path,
            vector_layer,
            output_file_path,
            aggregates_stats_list,
            arrays_stats_list,
        )


def test_control_input_invalid_output_format_with_array_stats(dialog, setup_layers):
    # Test if the control_input method raises an exception when using invalid output format with array stats
    vector_layer, _ = setup_layers

    raster_layers_path = "/path/to/raster"
    dialog.temp_index_field = "fid"
    output_file_path = Path("/path/to/output.parquet")
    aggregates_stats_list = []
    arrays_stats_list = ["mean", "std"]

    with pytest.raises(ValueError):
        dialog.control_input(
            raster_layers_path,
            vector_layer,
            output_file_path,
            aggregates_stats_list,
            arrays_stats_list,
        )
