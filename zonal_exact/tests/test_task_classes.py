import pytest
import numpy as np
import pandas as pd

from qgis.core import QgsTask
from qgis.PyQt.QtWidgets import QPlainTextEdit

from zonal_exact.task_classes import CalculateStatsTask
from zonal_exact.user_communication import WidgetPlainTextWriter

@pytest.fixture
def init_calculate_stats_task(setup_layers):
    vector_layer, raster_layer = setup_layers
    raster_layer_path = raster_layer.dataProvider().dataSourceUri()
    
    # Create a console writer
    console = WidgetPlainTextWriter(plain_text_widget=QPlainTextEdit())
    stats_to_calculate = ["mean", "max", "min"]
    # Initialize the task and run it
    task = CalculateStatsTask(
        "Test Task",
        QgsTask.CanCancel,
        console,
        [],
        vector_layer,
        [raster_layer_path],
        None,  # No weights
        stats_to_calculate,
        ["id"]
    )
    
    return task

def test_calculate_stats_task_init(init_calculate_stats_task):
    task = init_calculate_stats_task
    
    assert task.description == "Test Task"

def test_calculate_stats_task_run(init_calculate_stats_task):
    task = init_calculate_stats_task
    result = task.run()
    
    # Check if the task ran successfully and variables are set correctly
    assert result is True
    assert len(task.result_list) == 1

def test_calculate_stats_task_calculation(init_calculate_stats_task):
    task = init_calculate_stats_task
    task.run()
    
    # Check for correctness of the output statistics
    result_df = task.result_list[0]
    assert pd.isna(result_df['id']).sum() == 0  # No NaN values in the id column
    # (number of polygons, (number of stats * number of bands) + id column)
    assert result_df.shape == (12, 7)
    # 1 pixel laying over NoData value in raster and 1 totally outside of raster 
    assert pd.isna(result_df['pytest_raster_band_1_mean']).sum() == 2

def test_calculate_stats_task_single_nodata_pixel_polygon(init_calculate_stats_task):
    task = init_calculate_stats_task
    task.run()
    
    result_df = task.result_list[0]
    # Check for correctness of the output statistics at the single polygon laying on one NoData value pixel
    polygon_on_nodata = result_df.loc[result_df['id']==0].iloc[0]
    assert pd.isna(polygon_on_nodata['pytest_raster_band_1_mean'])
    assert pd.isna(polygon_on_nodata['pytest_raster_band_2_mean'])
    assert polygon_on_nodata['pytest_raster_band_1_max'] == -9999.0
    assert polygon_on_nodata['pytest_raster_band_2_max'] == -9999.0
    assert polygon_on_nodata['pytest_raster_band_1_min'] == -9999.0
    assert polygon_on_nodata['pytest_raster_band_2_min'] == -9999.0
    
def test_calculate_stats_task_single_pixel_polygon(init_calculate_stats_task):
    task = init_calculate_stats_task
    task.run()
    
    result_df = task.result_list[0]

    polygon_on_single_pixel = result_df.loc[result_df['id']==3].iloc[0]
    assert polygon_on_single_pixel['pytest_raster_band_1_mean'] == 4.0
    assert polygon_on_single_pixel['pytest_raster_band_2_mean'] == 6.0
    assert polygon_on_single_pixel['pytest_raster_band_1_max'] == polygon_on_single_pixel['pytest_raster_band_1_mean'] == polygon_on_single_pixel['pytest_raster_band_1_min']
    assert polygon_on_single_pixel['pytest_raster_band_2_max'] == polygon_on_single_pixel['pytest_raster_band_2_mean'] == polygon_on_single_pixel['pytest_raster_band_2_min']

def test_calculate_stats_task_single_big_polygon(init_calculate_stats_task):
    task = init_calculate_stats_task
    task.run()
    
    result_df = task.result_list[0]
    
    big_polygon = result_df.loc[result_df['id']==20].iloc[0]
    assert np.isclose(big_polygon['pytest_raster_band_1_mean'], 6.46)
    assert np.isclose(big_polygon['pytest_raster_band_2_mean'], 8.46)
    assert big_polygon['pytest_raster_band_1_max'] == 10
    assert big_polygon['pytest_raster_band_2_max'] == 12
    assert big_polygon['pytest_raster_band_1_min'] == 3
    assert big_polygon['pytest_raster_band_2_min'] == 5

def test_calculate_stats_task_single_polygon_outside_raster(init_calculate_stats_task):
    task = init_calculate_stats_task
    task.run()
    
    result_df = task.result_list[0]
    polygon_outside_raster = result_df.loc[result_df['id']==15].iloc[0]
    assert pd.isna(polygon_outside_raster['pytest_raster_band_1_mean'])
    assert pd.isna(polygon_outside_raster['pytest_raster_band_2_mean'])
    assert polygon_outside_raster['pytest_raster_band_1_max'] == -9999.0
    assert polygon_outside_raster['pytest_raster_band_2_max'] == -9999.0
    assert polygon_outside_raster['pytest_raster_band_1_min'] == -9999.0
    assert polygon_outside_raster['pytest_raster_band_2_min'] == -9999.0
