from typing import List
from exactextract import exact_extract
import pandas as pd

from qgis.core import QgsTask, QgsMessageLog, QgsVectorLayer
from .user_communication import WidgetPlainTextWriter


class CalculateStatsTask(QgsTask):
    """
    A class representing a task to calculate statistics using the exact_extract function.
    """

    def __init__(
        self,
        description: str,
        flags: QgsTask.Flag,
        widget_console: WidgetPlainTextWriter,
        result_list: List,
        polygon_layer: QgsVectorLayer,
        rasters: List[str],
        weights: List[str],
        stats: List[str],
        include_cols: List[str],
    ):
        """
        Attributes:
        description (str): The description of the task.
        flags (QgsTask.Flag): The flags for the task.
        widget_console (WidgetPlainTextWriter): The console to write task progress.
        result_list (List[str]): The list to store the results of the task.
        polygon_layer (QgsVectorLayer): The polygon layer to perform the statistics on.
        rasters (List[str]): The list of raster files to use in the statistics.
        weights (List[str]): The list of weights to use in the statistics.
        stats (List[str]): The list of statistics to calculate.
        include_cols (List[str]): The list of columns to include in the output.
        """
        super().__init__(description, flags)
        self.description = description
        self.widget_console: WidgetPlainTextWriter = widget_console
        self.polygon_layer: QgsVectorLayer = polygon_layer
        self.rasters: List[str] = rasters
        self.weights: List[str] = weights
        self.stats: List[str] = stats
        self.include_cols: List[str] = include_cols

        self.result_list: List[pd.DataFrame] = result_list

        self.completed_succesfully = False

    def run(self):
        """
        Run the task and calculate the statistics using exactextract
        """
        QgsMessageLog.logMessage(
            f"Started task: {self.description} with {self.polygon_layer.featureCount()} polygons"
        )
        self.widget_console.write_info(
            f"Started task: {self.description} with {self.polygon_layer.featureCount()} polygons"
        )

        def task_progress_update(frac: float, message: str):
            self.setProgress(frac * 100)
        
        result_stats = exact_extract(
            vec=self.polygon_layer,
            rast=self.rasters,
            weights=self.weights,
            ops=self.stats,
            include_cols=self.include_cols,
            output="pandas",
            progress=task_progress_update,
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
        self.widget_console.write_info(
            f"Finished task: {self.description}, result: {'Successful' if result else 'Failed'}"
        )


class MergeStatsTask(QgsTask):
    """
    A custom QgsTask for merging statistics from a list of pandas DataFrames and optionally prefixing column names.
    """

    def __init__(
        self,
        description: str,
        flags: QgsTask.Flag,
        widget_console: WidgetPlainTextWriter,
        result_list: List,
        index_column: str,
        prefix: str,
    ):
        """
        Attributes:
            description (str): A description of the task.
            flags (QgsTask.Flag): Flags indicating the task's behavior.
            widget_console (WidgetPlainTextWriter): A widget for writing console output.
            result_list (List[pd.DataFrame]): A list of pandas DataFrames containing the statistics to be merged.
            index_column (str): The name of the index column.
            prefix (str): A prefix string to be added to the column names.
        """
        super().__init__(description, flags)
        self.description: str = description
        self.widget_console: WidgetPlainTextWriter = widget_console
        self.result_list: List[pd.DataFrame] = result_list
        self.index_column: str = index_column
        self.prefix: str = prefix

        self.completed_succesfully = False
        self.calculated_stats: pd.DataFrame = None

    def run(self):
        """
        Merges all dataframes in the list into one dataframe and adds prefix to column names if necessary.
        """
        QgsMessageLog.logMessage(f"Inside MergeStatsTask Task: {self.description}")
        self.widget_console.write_info(
            f"Inside MergeStatsTask Task: {self.description}"
        )

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
        self.widget_console.write_info(
            f"Finished MergeStatsTask Task: {self.description}, result: {'Successful' if result else 'Failed'}"
        )
