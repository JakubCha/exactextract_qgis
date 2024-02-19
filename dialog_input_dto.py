from dataclasses import dataclass
from typing import List
from pathlib import Path

@dataclass
class DialogInputDTO:
    raster_layer_path: str
    vector_layer_path: str
    parallel_jobs: int
    output_file_path: str
    aggregates_stats_list: List[str]
    arrays_stats_list: List[str]
    input_layername: str = None
    output_layername: str = None
    
    def __post_init__(self):
        layer_extension_str = '|layername='
        if layer_extension_str in Path(self.vector_layer_path).suffix:
            vector_layer_path_split = self.vector_layer_path.split(layer_extension_str)
            self.vector_layer_path = vector_layer_path_split[0]
            self.input_layername = vector_layer_path_split[1]
            