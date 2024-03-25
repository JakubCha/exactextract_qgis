from dataclasses import dataclass
from typing import List, Dict, Callable
from pathlib import Path

from qgis.core import QgsVectorLayer

from .utils import extract_function_name

@dataclass
class DialogInputDTO:
    raster_layers_path: List[str]
    weights_layer_path: str
    vector_layer: QgsVectorLayer
    parallel_jobs: int
    output_file_path: Path
    aggregates_stats_list: List[str]
    arrays_stats_list: List[str]
    custom_functions_str_list: List[str]  # before conversion to function - function name: function code in str
    prefix: str
    input_layername: str = None
    output_layername: str = None
    
    def __post_init__(self):
        self.custom_functions_list: List[Callable] = []  # after conversion of function code to function - function name: function
        self.convert_custom_functions()
    
    def convert_custom_functions(self):
        """
        This method converts a list of custom function strings into a list of callable custom functions. 
        It uses a helper function to extract the function name and another helper function to create 
        the custom function.
        """
        # Define a helper function to create custom functions. 
        # It's defined outside loop to workaround pythons' late binding
        def create_custom_function(function_str: str):
            namespace = {}
            exec(function_str, namespace)
            return namespace[extract_function_name(function_str)]

        for function_str in self.custom_functions_str_list:
            custom_function = create_custom_function(function_str)
            self.custom_functions_list.append(custom_function)
    