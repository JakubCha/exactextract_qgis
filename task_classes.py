from exactextract import exact_extract
import pandas as pd

from qgis.core import QgsTask, QgsMessageLog, QgsVectorLayer

class CalculateStatsTask(QgsTask):
    def __init__(self, description, flags, widget_console, result_list, polygon_layer, raster, stats, include_cols):
        super().__init__(description, flags)
        self.description = description
        self.widget_console = widget_console
        self.polygon_layer: QgsVectorLayer = polygon_layer
        self.raster = raster
        self.stats = stats
        self.include_cols = include_cols
        
        self.result_list = result_list
    
    def run(self):
        QgsMessageLog.logMessage(f'Started task: {self.description} with {self.polygon_layer.featureCount()} polygons')
        self.widget_console.write_info(f'Started task: {self.description} with {self.polygon_layer.featureCount()} polygons')
        
        result_stats = exact_extract(vec=self.polygon_layer, rast=self.raster, ops=self.stats, include_cols=self.include_cols, output="pandas")
        self.result_list.append(result_stats)
        
        return True
        
    def finished(self, result):
        self.widget_console.write_info(f'Finished task: {self.description}')

class PostprocessStatsTask(QgsTask):
    def __init__(self, description, flags, widget_console, result_list, index_column, prefix):
        super().__init__(description, flags)
        self.description = description
        self.widget_console = widget_console
        self.result_list = result_list
        self.index_column = index_column
        self.prefix = prefix
        
        self.calculated_stats = None
        
    def run(self):
        QgsMessageLog.logMessage(f'Inside Postprocess Task: {self.description}')
        self.widget_console.write_info(f'Inside Postprocess Task: {self.description}')
        
        # result_indexed_list = [df.set_index(self.index_column) for df in self.result_list]
        calculated_stats = pd.concat(self.result_list)

        if len(self.prefix) > 0:
            # rename columns to include prefix string
            rename_dict = {column: f"{self.prefix}_{column}" for column in calculated_stats.columns if column != self.index_column}
            calculated_stats = calculated_stats.rename(columns=rename_dict)
        
        self.calculated_stats = calculated_stats
        
        return True
    
    def finished(self, result):
        self.widget_console.write_info(f'Finished Postprocess Task: {self.description}, {result}')
