from typing import List
from exactextract import exact_extract
import pandas as pd

from qgis.core import QgsTask, QgsMessageLog, QgsVectorLayer
from .user_communication import WidgetPlainTextWriter

class CalculateStatsTask(QgsTask):
    def __init__(self, description, flags, widget_console, result_list, polygon_layer, rasters, weights, stats, include_cols):
        super().__init__(description, flags)
        self.description = description
        self.widget_console: WidgetPlainTextWriter = widget_console
        self.polygon_layer: QgsVectorLayer = polygon_layer
        self.rasters: str = rasters
        self.weights: str = weights
        self.stats: List[str] = stats
        self.include_cols: List[str] = include_cols
        
        self.result_list: List[pd.DataFrame] = result_list
    
    def run(self):
        QgsMessageLog.logMessage(f'Started task: {self.description} with {self.polygon_layer.featureCount()} polygons')
        self.widget_console.write_info(f'Started task: {self.description} with {self.polygon_layer.featureCount()} polygons')
        
        result_stats = exact_extract(vec=self.polygon_layer, rast=self.rasters, weights=self.weights, ops=self.stats, 
                                    include_cols=self.include_cols, output="pandas")
        self.result_list.append(result_stats)
        
        return True
        
    def finished(self, result):
        self.widget_console.write_info(f'Finished task: {self.description}')

class MergeStatsTask(QgsTask):
    def __init__(self, description, flags, widget_console, result_list, index_column, prefix):
        super().__init__(description, flags)
        self.description: str = description
        self.widget_console: WidgetPlainTextWriter = widget_console
        self.result_list: List[pd.DataFrame] = result_list
        self.index_column: str = index_column
        self.prefix: str = prefix
        
        self.calculated_stats: pd.DataFrame = None
        
    def run(self):
        QgsMessageLog.logMessage(f'Inside MergeStatsTask Task: {self.description}')
        self.widget_console.write_info(f'Inside MergeStatsTask Task: {self.description}')
        
        calculated_stats = pd.concat(self.result_list)

        if len(self.prefix) > 0:
            # rename columns to include prefix string
            rename_dict = {column: f"{self.prefix}{column}" for column in calculated_stats.columns if column != self.index_column}
            calculated_stats = calculated_stats.rename(columns=rename_dict)
        
        self.calculated_stats = calculated_stats
        
        return True
    
    def finished(self, result):
        self.widget_console.write_info(f'Finished MergeStatsTask Task: {self.description}, {result}')
