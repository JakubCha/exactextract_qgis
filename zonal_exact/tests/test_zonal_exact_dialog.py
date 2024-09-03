import time
import pytest
from pathlib import Path
import numpy as np
import pandas as pd

from qgis.core import (
    QgsProject,
    QgsFeature,
    QgsGeometry,
    QgsVectorLayer,
    QgsFeatureRequest,
)
from qgis.PyQt.QtWidgets import QPlainTextEdit

from zonal_exact.zonal_exact_dialog import ZonalExactDialog
from zonal_exact.user_communication import UserCommunication, WidgetPlainTextWriter
from zonal_exact.dialog_input_dto import DialogInputDTO


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
    # dialog.close()


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

    dialog.temp_index_field = "id"
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

    dialog.temp_index_field = "id"
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
    dialog.temp_index_field = "id"
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
    dialog.temp_index_field = None
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


def test_control_input_non_necessary_id_field(dialog, setup_layers):
    # Test if the control_input method raises an exception when ID field is not necessary
    vector_layer, _ = setup_layers
    dialog.temp_index_field = None
    raster_layers_path = "/path/to/raster"
    output_file_path = Path("/path/to/output.gpkg")
    aggregates_stats_list = ["mean"]
    arrays_stats_list = []

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
    dialog.temp_index_field = "id"
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
    dialog.temp_index_field = "id"
    output_file_path = Path("/path/to/output.abc")
    aggregates_stats_list = ["mean"]
    arrays_stats_list = []

    with pytest.raises(ValueError, match="Output file extension *"):
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
    dialog.temp_index_field = "id"
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
    dialog.temp_index_field = "id"
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


def test_control_input_non_unique_id_column(dialog, setup_layers):
    # Test if the control_input method raises an exception when the ID column is not unique
    vector_layer, _ = setup_layers

    dialog.temp_index_field = "id"
    raster_layers_path = "/path/to/raster"
    output_file_path = Path("/path/to/output.csv")
    aggregates_stats_list = ["mean"]
    arrays_stats_list = []

    # Add a new feature with the same ID as the first feature
    provider = vector_layer.dataProvider()
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromWkt("POLYGON((0 -1, 1 -1, 1 0, 0 0, 0 -1))"))
    feature.setAttributes([0])
    provider.addFeature(feature)

    with pytest.raises(
        ValueError,
        match="id field values are not unique. Please select unique field as ID field.",
    ):
        dialog.control_input(
            raster_layers_path,
            vector_layer,
            output_file_path,
            aggregates_stats_list,
            arrays_stats_list,
        )


def test_extract_layers_path(dialog, setup_layers):
    # Test if the extract_layers_path method returns the correct path
    vector_layer, raster_layer = setup_layers

    layers_list = [vector_layer, raster_layer]

    extracted_layers_paths = dialog.extract_layers_path(layers_list)

    assert (
        extracted_layers_paths[0]
        == "memory?geometry=Polygon&crs=EPSG:3035&field=id:integer(0,0)"
    )
    assert extracted_layers_paths[1].split("/")[-1] == "pytest_raster.tif"


def test_process_calculations_single_task(tmp_path, dialog, setup_layers):
    # Test if the process_calculations method processes the calculations correctly
    vector_layer, raster_layer = setup_layers

    raster_layers_path = dialog.extract_layers_path([raster_layer])

    dialog.dialog_input = DialogInputDTO(
        raster_layers_path=raster_layers_path,
        weights_layer_path=None,
        vector_layer=vector_layer,
        parallel_jobs=1,
        output_file_path=str(tmp_path / "output_single_task.csv"),
        aggregates_stats_list=["mean"],
        arrays_stats_list=[],
        prefix="prefix",
        custom_functions_str_list=[],
        strategy="feature-sequential",
    )

    dialog.temp_index_field = "id"
    dialog.input_attributes_dict = {dialog.temp_index_field: 0}
    dialog.widget_console = WidgetPlainTextWriter(plain_text_widget=QPlainTextEdit())
    dialog.features_count = vector_layer.featureCount()

    dialog.process_calculations(vector_layer, dialog.features_count)

    # manually run merge task as pytest is unable to detect that CalculateStatsTask is finished
    # wait up to 5 seconds to let the task finish
    max_wait_time = 5  # Maximum wait time in seconds
    wait_interval = 0.5  # Wait interval in seconds

    elapsed_time = 0
    calculation_task = dialog.tasks[0]
    while not calculation_task.completed_succesfully:
        time.sleep(wait_interval)
        elapsed_time += wait_interval
        if elapsed_time >= max_wait_time:
            raise TimeoutError("Maximum wait time exceeded")
    dialog.merge_task.run()
    calculated_stats = dialog.merge_task.calculated_stats.sort_values(
        by="id", ascending=True
    )

    assert len(dialog.intermediate_result_list) == 1  # Only one task was run
    assert list(calculated_stats.columns) == [
        "id",
        "prefixpytest_raster_band_1_mean",
        "prefixpytest_raster_band_2_mean",
    ]
    assert calculated_stats.shape == (12, 3)
    assert calculated_stats["id"].to_list() == [
        0,
        1,
        2,
        3,
        4,
        5,
        11,
        12,
        13,
        14,
        15,
        20,
    ]
    assert calculated_stats[
        "prefixpytest_raster_band_1_mean"
    ].to_list() == pytest.approx(
        [
            np.nan,
            6.0,
            5.0,
            4.0,
            3.0,
            2.0,
            9.0,
            8.0,
            7.0,
            6.0,
            np.nan,
            6.460000038146973,
        ],
        nan_ok=True,
    )
    assert calculated_stats[
        "prefixpytest_raster_band_2_mean"
    ].to_list() == pytest.approx(
        [
            np.nan,
            8.0,
            7.0,
            6.0,
            5.0,
            4.0,
            11.0,
            10.0,
            9.0,
            8.0,
            np.nan,
            8.460000038146973,
        ],
        nan_ok=True,
    )


def test_process_calculations_multiple_tasks(tmp_path, dialog, setup_layers):
    # Test if the process_calculations method processes the calculations correctly
    vector_layer, raster_layer = setup_layers

    raster_layers_path = dialog.extract_layers_path([raster_layer])

    dialog.dialog_input = DialogInputDTO(
        raster_layers_path=raster_layers_path,
        weights_layer_path=None,
        vector_layer=vector_layer,
        parallel_jobs=3,
        output_file_path=str(tmp_path / "output_single_task.csv"),
        aggregates_stats_list=["mean"],
        arrays_stats_list=[],
        prefix="prefix",
        custom_functions_str_list=[],
        strategy="feature-sequential",
    )

    dialog.temp_index_field = "id"
    dialog.input_attributes_dict = {dialog.temp_index_field: 0}
    dialog.widget_console = WidgetPlainTextWriter(plain_text_widget=QPlainTextEdit())
    dialog.features_count = vector_layer.featureCount()

    dialog.process_calculations(vector_layer, 4)

    # manually run merge task as pytest is unable to detect that CalculateStatsTask is finished
    # wait up to 5 seconds to let the task finish
    max_wait_time = 5  # Maximum wait time in seconds
    wait_interval = 0.5  # Wait interval in seconds

    elapsed_time = 0
    calculation_task = dialog.tasks[0]
    while not calculation_task.completed_succesfully:
        time.sleep(wait_interval)
        elapsed_time += wait_interval
        if elapsed_time >= max_wait_time:
            raise TimeoutError("Maximum wait time exceeded")
    dialog.merge_task.run()
    calculated_stats = dialog.merge_task.calculated_stats

    assert (
        len(dialog.intermediate_result_list) == 3
    )  # Three tasks were run - 12 / 4 = 3
    assert list(calculated_stats.columns) == [
        "id",
        "prefixpytest_raster_band_1_mean",
        "prefixpytest_raster_band_2_mean",
    ]
    assert calculated_stats.shape == (12, 3)

    expected_df = pd.DataFrame(
        {
            "id": [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 20],
            "prefixpytest_raster_band_1_mean": [
                np.nan,
                6.0,
                5.0,
                4.0,
                3.0,
                2.0,
                9.0,
                8.0,
                7.0,
                6.0,
                np.nan,
                6.46,
            ],
            "prefixpytest_raster_band_2_mean": [
                np.nan,
                8.0,
                7.0,
                6.0,
                5.0,
                4.0,
                11.0,
                10.0,
                9.0,
                8.0,
                np.nan,
                8.46,
            ],
        }
    )
    expected_df = expected_df.sort_values("id").reset_index(drop=True)
    calculated_stats = calculated_stats.sort_values("id").reset_index(drop=True)

    pd.testing.assert_frame_equal(
        expected_df, calculated_stats, check_exact=False, rtol=1e-05, atol=1e-08
    )


def test_process_calculations_geospatial_output_created(
    tmp_path, dialog, setup_layers, qgis_processing
):
    # Test if the process_calculations method processes the calculations correctly
    vector_layer, raster_layer = setup_layers

    raster_layers_path = dialog.extract_layers_path([raster_layer])

    dialog.dialog_input = DialogInputDTO(
        raster_layers_path=raster_layers_path,
        weights_layer_path=None,
        vector_layer=vector_layer,
        parallel_jobs=1,
        output_file_path=Path(tmp_path / "output_single_task.gpkg"),
        aggregates_stats_list=["mean"],
        arrays_stats_list=[],
        prefix="prefix",
        custom_functions_str_list=[],
        strategy="feature-sequential",
    )

    dialog.control_input(
        raster_layers_path,
        vector_layer,
        dialog.dialog_input.output_file_path,
        dialog.dialog_input.aggregates_stats_list,
        dialog.dialog_input.arrays_stats_list,
    )

    dialog.temp_index_field = "id"
    dialog.input_attributes_dict = {dialog.temp_index_field: 0}
    dialog.widget_console = WidgetPlainTextWriter(plain_text_widget=QPlainTextEdit())
    dialog.features_count = vector_layer.featureCount()

    dialog.process_calculations(vector_layer, dialog.features_count)

    # manually run merge task as pytest is unable to detect that CalculateStatsTask is finished
    # wait up to 5 seconds to let the task finish
    max_wait_time = 5  # Maximum wait time in seconds
    wait_interval = 0.5  # Wait interval in seconds

    elapsed_time = 0
    calculation_task = dialog.tasks[0]
    while not calculation_task.completed_succesfully:
        time.sleep(wait_interval)
        elapsed_time += wait_interval
        if elapsed_time >= max_wait_time:
            raise TimeoutError("Maximum wait time exceeded")
    dialog.merge_task.run()

    # assert that output file is created
    assert (tmp_path / "output_single_task.gpkg").exists()


def test_process_calculations_geospatial_output_contents(
    tmp_path, dialog, setup_layers, qgis_processing
):
    # Test if the process_calculations method processes the calculations correctly
    vector_layer, raster_layer = setup_layers

    raster_layers_path = dialog.extract_layers_path([raster_layer])
    output_file_path = Path(tmp_path / "output_single_task.gpkg")

    dialog.dialog_input = DialogInputDTO(
        raster_layers_path=raster_layers_path,
        weights_layer_path=None,
        vector_layer=vector_layer,
        parallel_jobs=1,
        output_file_path=output_file_path,
        aggregates_stats_list=["mean"],
        arrays_stats_list=[],
        prefix="prefix",
        custom_functions_str_list=[],
        strategy="feature-sequential",
    )

    dialog.control_input(
        raster_layers_path,
        vector_layer,
        dialog.dialog_input.output_file_path,
        dialog.dialog_input.aggregates_stats_list,
        dialog.dialog_input.arrays_stats_list,
    )

    dialog.temp_index_field = "id"
    dialog.input_attributes_dict = {dialog.temp_index_field: 0}
    dialog.widget_console = WidgetPlainTextWriter(plain_text_widget=QPlainTextEdit())
    dialog.features_count = vector_layer.featureCount()

    dialog.process_calculations(vector_layer, dialog.features_count)

    # manually run merge task as pytest is unable to detect that CalculateStatsTask is finished
    # wait up to 5 seconds to let the task finish
    max_wait_time = 5  # Maximum wait time in seconds
    wait_interval = 0.5  # Wait interval in seconds

    elapsed_time = 0
    calculation_task = dialog.tasks[0]
    while not calculation_task.completed_succesfully:
        time.sleep(wait_interval)
        elapsed_time += wait_interval
        if elapsed_time >= max_wait_time:
            raise TimeoutError("Maximum wait time exceeded")
    dialog.merge_task.run()

    output_geospatial_layer = QgsVectorLayer(
        str(output_file_path),
        output_file_path.stem,
        "ogr",
    )

    assert output_geospatial_layer.name() == "output_single_task"
    assert output_geospatial_layer.featureCount() == 12
    assert output_geospatial_layer.fields().count() == 6
    assert output_geospatial_layer.fields().names() == [
        "fid",
        "id",
        "prefixpytest_raster_band_1_mean",
        "prefixpytest_raster_band_2_mean",
        "layer",
        "path",
    ]

    request = QgsFeatureRequest()
    request.addOrderBy("id")
    features = output_geospatial_layer.getFeatures(request)
    for f in output_geospatial_layer.getSelectedFeatures(request):
        print(f["City"])

    assert next(features).attributes()[1:5] == [0, None, None, "temporary_layer"]
    assert next(features).attributes()[1:5] == [1, 6.0, 8.0, "temporary_layer"]
    assert next(features).attributes()[1:5] == [2, 5.0, 7.0, "temporary_layer"]
    assert next(features).attributes()[1:5] == [3, 4.0, 6.0, "temporary_layer"]
    assert next(features).attributes()[1:5] == [4, 3.0, 5.0, "temporary_layer"]
    assert next(features).attributes()[1:5] == [5, 2.0, 4.0, "temporary_layer"]
    assert next(features).attributes()[1:5] == [11, 9.0, 11.0, "temporary_layer"]
    assert next(features).attributes()[1:5] == [12, 8.0, 10.0, "temporary_layer"]
    assert next(features).attributes()[1:5] == [13, 7.0, 9.0, "temporary_layer"]
    assert next(features).attributes()[1:5] == [14, 6.0, 8.0, "temporary_layer"]
    assert next(features).attributes()[1:5] == [15, None, None, "temporary_layer"]
    assert next(features).attributes()[1:5] == [
        20,
        pytest.approx(6.46),
        pytest.approx(8.46),
        "temporary_layer",
    ]
