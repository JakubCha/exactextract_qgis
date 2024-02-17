from typing import Any, List
from multiprocess import Pool

import geopandas as gpd
import pandas as pd

class ZonalStats:
    @staticmethod
    def _chunks(data: gpd.GeoDataFrame, n: int, raster: str, stats: List[str], include_cols: List[str]) -> List[Any]:
        """Yield successive n-sized chunks from a slice-able iterable."""
        for i in range(0, len(data), n):
            yield [data[i:i + n], raster, stats, include_cols]    

    @staticmethod
    def _zonal_stats_partial(feats: gpd.GeoDataFrame, raster: str, stats: List[str], include_cols: List[str]) -> List[Any]:
        from exactextract import exact_extract
        """Wrapper for zonal stats, takes a geodataframe"""
        return exact_extract(vec=feats, rast=raster, ops=stats, include_cols=include_cols, output="pandas")

    @staticmethod
    def calculate_stats_parallel(polygon_layer_gdf: gpd.GeoDataFrame, raster: str, stats: List[str], pool: Pool, include_cols=['id'], n_jobs=16, index_column: str='id', prefix: str=''):
        """
        Calculate zonal statistics for a raster and a GeoDataFrame of polygons" in parallel.

        Args:
            polygon_layer_gdf (gpd.GeoDataFrame): A GeoDataFrame of polygons.
            raster (str): The path to the raster file.
            stats (List[str]): A list of statistics to calculate.
            pool (Pool): Pool of a jobs in multiprocess library.
            include_cols (List[str], optional): A list of columns to include in the output. Defaults to ['id'].
            n_jobs (int, optional): The number of cores to use for parallel processing. Defaults to 16.
            index_column (str, optional): The name of the index column. Defaults to 'id'.
            prefix (str, optional): A prefix string to add to the column names. Defaults to ''.

        Returns:
            pd.DataFrame: A DataFrame of zonal statistics.
        """
        # Define the number of cores to use for parallel processing
        
        # Use starmap and chunks for parallel processing
        stats_list = pool.starmap(ZonalStats._zonal_stats_partial,
                                ZonalStats._chunks(polygon_layer_gdf, round(len(polygon_layer_gdf) / pool._processes),
                                        raster,  stats, include_cols))
        stats_list = [df.set_index(index_column) for df in stats_list]
        calculated_stats = pd.concat(stats_list)
        
        if index_column is not None and index_column in include_cols:
            # change index dtype to dtype of index column in input layer
            index_dtype = str(polygon_layer_gdf[index_column].dtype)
            calculated_stats = calculated_stats.reset_index().astype({index_column:index_dtype})
            
        if len(prefix) > 0:
            # rename columns to include prefix string
            rename_dict = {stat: f"{prefix}{stat}" for stat in stats}
            calculated_stats = calculated_stats.rename(columns=rename_dict)
        
        return calculated_stats
        