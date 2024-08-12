# Help
This is a tool for the QGIS that allows to aggregate/summarize values of the raster over polygonal (vector) areas using exactextract library. This library allows to treat pixel cells as partially covered by polygons using weighting according to the extent of cover. If you want to know more about the library working in the backend of this plugin it's highly recommend to visit its [github repository](https://github.com/isciences/exactextract/tree/master).
<br />

## Input
<br />

### Values

`Values` input for zonal statistics are raster layers with values that will be aggregated using zones inside polygons. `Values` raster may have multiple bands. In such case statistics are calculated for each band separately and put in result in separate columns.  
It's possible to calculate zonal statistics for multiple rasters. In such case statistics are calculated for each band separately and put in result in separate columns.

### Weights

`Weights` is a raster layer with weighting values. The weighting raster does not need to have the same resolution and extent as the value raster, but the resolutions of the two rasters must be integer multiples of each other, and any difference between the grid origin points must be an integer multiple of the smallest cell size.

### Vector

`Vector` is a vector layer with polygon geometry. For each polygon in this layer `exactextract` computes the area of each raster cell that is covered and aggregates the values of these raster cells.

### ID Column

`Vector` layer need to have unique, numerical column that's used as identifier of polygons based on which calculated statistics can be joined to.
<br />
<br />

## Parameters
<br />

### Output statistics column prefix

Prefix for result column names.

### Number of subtasks

Plugin allows to divide calculation to multiple **threads** (subtasks) to speed up calculation of big input data. In case of small input data usage of multiple threads will slow down calculation due to overhead needed to configure and start threads. 
It's up to user to decide whether usage of subtasks is profitable.
*Plugin developer suggestion is to start using subtasks with more than 100 000 polygons*

> **Note:** Use QGIS parallel engine to create threads

### Output File Path

Path to the output file that result will be written to.
In current version of the plugin possible outputs are **CSV** or **Parquet** (requires *fastparquet* python library) files.
**Parquet** format correctly defines the datatype of output columns values.

### Checkbox: Join to Input Vector Layer

If checked columns with calculated values will be joined to input vector, polygon layer. 
In order to permanently add calculated columns to input vector, it should be saved while joined.
<br />
<br />

## Statistics
Description of statistics possible to use in tool is available in `exactextract` library [repository](https://github.com/isciences/exactextract/tree/master?tab=readme-ov-file#supported-statistics)
<br />


### Aggregates

Statistics that aggregate values from `Values` raster in `Vector` to single value for each input polygon.

### Arrays

Statistics that returns array of raster values for each polygon in `Vector`.

### Custom Function

Write custom Python code to define extra, additional features for raster zonal statistics. Custom functions should accept raster `values` and `coverage` attributes.
> **Example:**  Calculate 90th percentile of raster values:
> ```python
>import numpy as np
>
>def 90th_perc(values, cov):
>    return np.percentile(values, 90)
> ```
> If given statistic is checked in Custom Function combo box there will be new column `90th_perc` added.

There is also option to modify custom functions defined by user earlier. In order to load the code of existing function and modify it the function name should be checked in Custom Function combo box. Custom functions defined in this plugin are removed when plugin is reloaded or qgis is restarted. User should save custom functions for later usage outside of the plugin.

> **Warning:** If there's an error during processing of custom function code whole processing will be stopped. Wrong function may also block QGIS or make it crash.
