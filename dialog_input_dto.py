from dataclasses import dataclass
from typing import List
from pathlib import Path

from qgis.core import QgsVectorLayer

@dataclass
class DialogInputDTO:
    raster_layer_path: str
    weights_layer_path: str
    vector_layer: QgsVectorLayer
    parallel_jobs: int
    output_file_path: Path
    aggregates_stats_list: List[str]
    arrays_stats_list: List[str]
    prefix: str
    input_layername: str = None
    output_layername: str = None
    