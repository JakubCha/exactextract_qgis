## About
This plugin use [exactextract](https://github.com/isciences/exactextract/tree/master) library. It's an external package that's not shipped with QGIS by default.
<br />

## Installation
### Automatic
This plugin comes with automatic installation module which installs `exactextract` to QGIS user `profile` directory.
### Manual
User might also install library by himself using `OSGeo4W Shell` command: `pip install exactextract`
<br />

## Update
### Plugin was installed automatically
Similar to `Manual` installation step input command: `pip install exactextract --upgrade`
### Plugin was installed with `OSGeo4W Shell`
1. Close QGIS.
2. Go to `C:\Users\<Username>\AppData\Roaming\QGIS\QGIS3\profiles\<profile name>\python\plugins\python3.9`
and remove directories with `exactextract` in name.
3. Open QGIS and let plugin install the package using `Automatic` method.
