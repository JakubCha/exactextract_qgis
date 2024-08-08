import pytest
import pandas as pd

from qgis.core import QgsTask
from qgis.PyQt.QtWidgets import QPlainTextEdit

from zonal_exact.task_classes import MergeStatsTask
from zonal_exact.user_communication import WidgetPlainTextWriter


@pytest.fixture
def setup_stats_dfs():
    # Create two dataframes with different statistics
    stats_df1 = pd.DataFrame(
        {
            "id": [100, 101, 102],
            "mean": [1, 2, 3],
            "max": [2, 3, 4],
            "min": [0, 1, 2],
        }
    )
    stats_df2 = pd.DataFrame(
        {
            "id": [110, 111, 112],
            "mean": [4, 5, 6],
            "max": [5, 6, 7],
            "min": [3, 4, 5],
        }
    )
    stats_df3 = pd.DataFrame(
        {
            "id": [200, 201, 202],
            "mean": [7, 8, 9],
            "max": [8, 9, 10],
            "min": [6, 7, 8],
        }
    )
    return stats_df1, stats_df2, stats_df3


@pytest.fixture
def init_merge_stats_task(setup_stats_dfs):
    stats_df1, stats_df2, stats_df3 = setup_stats_dfs
    result_list = [stats_df1, stats_df2, stats_df3]
    # Create a console writer
    console = WidgetPlainTextWriter(plain_text_widget=QPlainTextEdit())
    task = MergeStatsTask(
        "Merge statistics",
        QgsTask.CanCancel,
        result_list,
        "id",
        "pytest_",
    )
    task.taskChanged.connect(console.write_info)

    return task, console


def test_task_init(init_merge_stats_task):
    task, _ = init_merge_stats_task

    assert task.description == "Merge statistics"


def test_task_run(init_merge_stats_task):
    task, _ = init_merge_stats_task
    result = task.run()

    # Check if the task ran successfully and variables are set correctly
    assert result is True
    assert task.calculated_stats.shape == (
        9,
        4,
    )  # (9 features, id column + 3 statistics)
    assert task.calculated_stats["id"].tolist() == [
        100,
        101,
        102,
        110,
        111,
        112,
        200,
        201,
        202,
    ]
    assert task.calculated_stats["pytest_mean"].tolist() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert task.calculated_stats["pytest_max"].tolist() == [2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert task.calculated_stats["pytest_min"].tolist() == [0, 1, 2, 3, 4, 5, 6, 7, 8]


def test_task_console_output(init_merge_stats_task):
    task, console = init_merge_stats_task
    task.run()
    # Simulate task finished with success and failure
    task.finished(True)
    task.finished(False)

    # Check if the console output is correct
    console_output = console.plain_text_widget.toPlainText().split("\n")
    assert console_output[0] == "[INFO]: Inside MergeStatsTask Task: Merge statistics"
    assert (
        console_output[1]
        == "[INFO]: Finished MergeStatsTask Task: Merge statistics, result: Successful"
    )
    assert (
        console_output[2]
        == "[INFO]: Finished MergeStatsTask Task: Merge statistics, result: Failed"
    )
