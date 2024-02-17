from dataclasses import dataclass
from typing import List

@dataclass
class DialogInputDTO:
    raster_layer_path: str
    vector_layer_path: str
    parallel_jobs: int
    output_file_path: str
    aggregates_stats_list: List[str]
    arrays_stats_list: List[str]
