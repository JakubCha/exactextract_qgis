import pytest
from pathlib import Path

from qgis.core import QgsVectorLayer

from zonal_exact.dialog_input_dto import DialogInputDTO


@pytest.fixture
def setup_dialog_input_dto(tmp_path):
    # Create a QgsVectorLayer instance
    vector_layer = QgsVectorLayer("Point", "test_layer", "memory")

    # Initialize the DialogInputDTO class
    dto = DialogInputDTO(
        raster_layers_path=["/path/to/raster1", "/path/to/raster2"],
        weights_layer_path="/path/to/weights",
        vector_layer=vector_layer,
        parallel_jobs=2,
        output_file_path=Path(tmp_path / "output_file"),
        aggregates_stats_list=["mean", "sum"],
        arrays_stats_list=["min", "max"],
        custom_functions_str_list=[
            "def add(a, b): return a + b",
            "def subtract(a, b): return a - b",
        ],
        prefix="test",
        input_layername="input",
        output_layername="output",
        strategy="feature-sequential",
    )

    return dto


def test_custom_functions_are_callable(setup_dialog_input_dto):
    dto = setup_dialog_input_dto

    for func in dto.custom_functions_list:
        assert callable(func)


def test_convert_custom_functions(setup_dialog_input_dto):
    dto = setup_dialog_input_dto

    assert len(dto.custom_functions_list) == 2
    assert dto.custom_functions_list[0](2, 3) == 5
    assert dto.custom_functions_list[1](5, 2) == 3
