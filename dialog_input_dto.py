from dataclasses import dataclass
from typing import List, Dict, Callable
from pathlib import Path

import numpy as np

from qgis.core import QgsVectorLayer

@dataclass
class DialogInputDTO:
    raster_layer_path: str
    vector_layer: QgsVectorLayer
    parallel_jobs: int
    output_file_path: Path
    aggregates_stats_list: List[str]
    arrays_stats_list: List[str]
    custom_functions_str_dict: Dict[str, str]  # before conversion to function - function name: function code in str
    prefix: str
    input_layername: str = None
    output_layername: str = None
    
    def __post_init__(self):
        self.custom_functions_list: List[Callable] = []  # after conversion of function code to function - function name: function
        self.convert_custom_functions()
    
    def convert_custom_functions(self):
        # for loop: convert custom_functions_str_dict to custom_functions_list using eval
        # Define a helper function to create custom functions. 
        # It's defined outside loop to workaround pythons' late binding
        def create_custom_function(function_str):
            def custom_temp_function(values, cov):
                return eval(function_str)
            return custom_temp_function
        
        for function_name, function_str in self.custom_functions_str_dict.items():
            custom_function = create_custom_function(function_str)
            custom_function.__name__ = function_name  # exactextract uses function name as stat name if it's Callable
            self.custom_functions_list.append(custom_function)
    