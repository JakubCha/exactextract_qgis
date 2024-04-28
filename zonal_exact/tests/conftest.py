from typing import Tuple
import pytest
import numpy as np
from osgeo import gdal
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsGeometry,
    QgsFeature,
    QgsField,
    QgsFields,
)
from PyQt5.QtCore import QVariant


@pytest.fixture(scope="function")
def setup_layers(tmp_path) -> Tuple[QgsVectorLayer, QgsRasterLayer]:
    """
    Set up vector and raster layers for testing.

    Args:
        tmp_path (str): The temporary path where the raster file will be created.

    Returns:
        Tuple[QgsVectorLayer, QgsRasterLayer]: A tuple containing the created vector layer and raster layer.
    """

    vector_layer = QgsVectorLayer("Polygon?crs=epsg:3035", "polygon_layer", "memory")

    provider = vector_layer.dataProvider()

    # Define the fields
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))

    # Add the fields to the layer
    provider.addAttributes(fields)
    vector_layer.updateFields()

    # Create 5 polygons in the left side of the raster
    for i in range(0, 6):
        feature = QgsFeature()
        feature.setGeometry(
            QgsGeometry.fromWkt(f"POLYGON((0 {i-1}, 1 {i-1}, 1 {i}, 0 {i}, 0 {i-1}))")
        )
        feature.setAttributes([i])
        provider.addFeature(feature)
    # Create 5 polygons in the right side of the raster
    for i in range(5, 0, -1):
        feature = QgsFeature()
        feature.setGeometry(
            QgsGeometry.fromWkt(f"POLYGON((5 {i}, 4 {i}, 4 {i+1}, 5 {i+1}, 5 {i}))")
        )
        feature.setAttributes([i + 10])
        provider.addFeature(feature)
    # Create huge polygon spanning over most part of the raster
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromWkt("POLYGON((1 -1, 5 -1, 1 5, 1 -1))"))
    feature.setAttributes([20])
    provider.addFeature(feature)

    # Create a raster file
    raster_file = str(tmp_path / "pytest_raster.tif")
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(raster_file, 6, 6, 2, gdal.GDT_Float32)
    dataset.SetGeoTransform(
        [0, 1, 0, 5, 0, -1]
    )  # Define the affine transform (how raster is scaled, rotated, skewed, and/or translated)

    nodata_value = -9999.0
    for i in range(1, 3):
        band = dataset.GetRasterBand(i)
        band.SetNoDataValue(nodata_value)
        data_array = np.array([[(j + i) + (k + i) for j in range(6)] for k in range(6)])
        data_array[5, :] = nodata_value  # Set last row to NoData value
        data_array[:, 5] = nodata_value  # Set last column to NoData value
        band.WriteArray(data_array)

    dataset.FlushCache()

    # Create a raster layer from the raster file
    raster_layer = QgsRasterLayer(raster_file, "raster_layer")
    raster_layer.setCrs(QgsCoordinateReferenceSystem("EPSG:3035"))

    return vector_layer, raster_layer
