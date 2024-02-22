from exactextract import exact_extract
import pandas as pd

from qgis.core import QgsTask, QgsMessageLog

class CalculateStatsTask(QgsTask):
    def __init__(self, description, flags, widget_console, result_list, polygon_layer_gdf, raster, stats, include_cols):
        super().__init__(description, flags)
        self.description = description
        self.widget_console = widget_console
        self.polygon_layer_gdf = polygon_layer_gdf
        self.raster = raster
        self.stats = stats
        self.include_cols = include_cols
        
        self.result_list = result_list
    
    def run(self):
        QgsMessageLog.logMessage(f'Started task: {self.description} with {self.polygon_layer_gdf.shape[0]} polygons')
        self.widget_console.write_info(f'Started task: {self.description} with {self.polygon_layer_gdf.shape[0]} polygons')
        
        result_stats = exact_extract(vec=self.polygon_layer_gdf, rast=self.raster, ops=self.stats, include_cols=self.include_cols, output="pandas")
        self.result_list.append(result_stats)
        
        return True
        
    def finished(self, result):
        self.widget_console.write_info(f'Finished task: {self.description}')

class PostprocessStatsTask(QgsTask):
    def __init__(self, description, flags, widget_console, result_list, index_column, index_column_dtype, stats, prefix):
        super().__init__(description, flags)
        self.description = description
        self.widget_console = widget_console
        self.result_list = result_list
        self.index_column = index_column
        self.index_column_dtype = index_column_dtype
        self.stats = stats
        self.prefix = prefix
        
        self.calculated_stats = None
        
    def run(self):
        QgsMessageLog.logMessage(f'Inside Postprocess Task: {self.description}')
        self.widget_console.write_info(f'Inside Postprocess Task: {self.description}')
        
        # result_indexed_list = [df.set_index(self.index_column) for df in self.result_list]
        calculated_stats = pd.concat(self.result_list)
        
        if self.index_column is not None and self.index_column_dtype is not None:
            # change index dtype to dtype of index column in input layer
            index_dtype = str(self.index_column_dtype)
            calculated_stats = calculated_stats.astype({self.index_column:index_dtype})
        
        if len(self.prefix) > 0:
            # rename columns to include prefix string
            rename_dict = {stat: f"{self.prefix}_{stat}" for stat in self.stats}
            calculated_stats = calculated_stats.rename(columns=rename_dict)
        
        self.calculated_stats = calculated_stats
        
        return True
    
    def finished(self, result):
        self.widget_console.write_info(f'Inside Postprocess Task: {self.description}')
