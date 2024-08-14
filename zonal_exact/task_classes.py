from pathlib import Path
from typing import List
from exactextract import exact_extract
import pandas as pd

from qgis.core import QgsTask, QgsMessageLog, QgsVectorLayer
import processing
from PyQt5.QtCore import pyqtSignal


class CalculateStatsTask(QgsTask):
    """
    A class representing a task to calculate statistics using the exact_extract function.
    """

    taskChanged = pyqtSignal(str)

    def __init__(
        self,
        description: str,
        flags: QgsTask.Flag,
        result_list: List,
        polygon_layer: QgsVectorLayer,
        rasters: List[str],
        weights: List[str],
        stats: List[str],
        include_cols: List[str],
        geospatial_output: bool,
    ):
        """
        Attributes:
        description (str): The description of the task.
        flags (QgsTask.Flag): The flags for the task.
        result_list (List[str]): The list to store the results of the task.
        polygon_layer (QgsVectorLayer): The polygon layer to perform the statistics on.
        rasters (List[str]): The list of raster files to use in the statistics.
        weights (List[str]): The list of weights to use in the statistics.
        stats (List[str]): The list of statistics to calculate.
        include_cols (List[str]): The list of columns to include in the output.
        geo_spatial_output (bool): A boolean indicating whether to include the geometry in the output and use QGIS writer in exactextract.
        """
        super().__init__(description, flags)
        self.description = description
        self.polygon_layer: QgsVectorLayer = polygon_layer
        self.rasters: List[str] = rasters
        self.weights: List[str] = weights
        self.stats: List[str] = stats
        self.include_cols: List[str] = include_cols
        self.geo_spatial_output: bool = geospatial_output

        self.result_list: List[pd.DataFrame] = result_list

        self.completed_succesfully = False

    def run(self):
        """
        Run the task and calculate the statistics using exactextract
        """
        message = f"Started task: {self.description} with {self.polygon_layer.featureCount()} polygons"
        QgsMessageLog.logMessage(message)
        self.taskChanged.emit(message)

        if self.geo_spatial_output:
            result_stats = exact_extract(
                vec=self.polygon_layer,
                rast=self.rasters,
                weights=self.weights,
                ops=self.stats,
                include_cols=self.include_cols,
                include_geom=True,
                output="qgis",
            )
        else:
            result_stats = exact_extract(
                vec=self.polygon_layer,
                rast=self.rasters,
                weights=self.weights,
                ops=self.stats,
                include_cols=self.include_cols,  # TODO: add include_cols to exact_extract in case of geospatial output
                include_geom=False,
                output="pandas",
            )
        self.result_list.append(result_stats)

        self.completed_succesfully = True
        return True

    def finished(self, result: bool):
        """
        Method that is called when the task has finished

        Args:
            result (bool):  The result of the task. True if  the task was successful otherwise False.
        """
        message = f"Finished task: {self.description}, result: {'Successful' if result else 'Failed'}"
        self.taskChanged.emit(message)


class MergeStatsTask(QgsTask):
    """
    A custom QgsTask for merging statistics from a list of pandas DataFrames and optionally prefixing column names.
    """

    taskChanged = pyqtSignal(str)

    def __init__(
        self,
        description: str,
        flags: QgsTask.Flag,
        result_list: List,
        index_column: str,
        prefix: str,
        geospatial_output: bool,
        output_file_path: Path,
    ):
        """
        Attributes:
            description (str): A description of the task.
            flags (QgsTask.Flag): Flags indicating the task's behavior.
            result_list (List[pd.DataFrame]): A list of pandas DataFrames containing the statistics to be merged.
            index_column (str): The name of the index column.
            prefix (str): A prefix string to be added to the column names.
            geo_spatial_output (bool): A boolean indicating whether output is geospatial layer.
        """
        super().__init__(description, flags)
        self.description: str = description
        self.result_list: List[pd.DataFrame] = result_list
        self.index_column: str = index_column
        self.prefix: str = prefix
        self.geospatial_output: bool = geospatial_output
        self.output_file_path: Path = output_file_path

        self.completed_succesfully = False
        self.calculated_stats: pd.DataFrame = None

    def run(self):
        """
        Merges all dataframes in the list into one dataframe and adds prefix to column names if necessary.
        """
        message = f"Inside MergeStatsTask Task: {self.description}"
        QgsMessageLog.logMessage(message)
        self.taskChanged.emit(message)

        if self.geospatial_output:
            # rename calculated columns to include prefix string
            # TODO: add prefix to column names
            # merge all vectors in a list
            parameters = {'LAYERS': self.result_list, 
                        'OUTPUT': str(self.output_file_path)}
            processing.run("qgis:mergevectorlayers", parameters) 
        else:
            calculated_stats = pd.concat(self.result_list)

            if len(self.prefix) > 0:
                # rename columns to include prefix string
                rename_dict = {
                    column: f"{self.prefix}{column}"
                    for column in calculated_stats.columns
                    if column != self.index_column
                }
                calculated_stats = calculated_stats.rename(columns=rename_dict)

            self.calculated_stats = calculated_stats
        
        self.completed_succesfully = True
        return True

    def finished(self, result: bool):
        """
        Method that is called when the task has finished

        Args:
            result (bool):  The result of the task. True if  the task was successful otherwise False.
        """
        message = f"Finished MergeStatsTask Task: {self.description}, result: {'Successful' if result else 'Failed'}"
        self.taskChanged.emit(message)
