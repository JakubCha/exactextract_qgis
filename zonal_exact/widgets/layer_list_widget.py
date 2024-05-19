"""
Inspired by this post: https://gis.stackexchange.com/a/419115
by Ben W: https://gis.stackexchange.com/users/100254/ben-w
created by: Jakub Charyton, 2024
"""

from typing import List
from qgis.PyQt import QtWidgets, QtCore
from qgis.core import QgsMapLayerType, QgsRasterLayer


class MultiRasterLayerSelectionWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        """
        Initializes the MultiRasterLayerSelectionWidget class.

        Args:
            parent: The parent widget.
        """
        super().__init__()
        self.project = parent.project
        self.previously_selected: List[str] = []
        layer_tree = self.project.layerTreeRoot()

        # Connect to signals for layer tree change events
        self.project.layersAdded.connect(self.update_layers)
        layer_tree.nameChanged.connect(self.update_layers)
        self.project.layersRemoved.connect(self.update_layers)

        # Initial population of layers
        self.update_layers()

    def checked_layers(self):
        """
        Returns layers that were checked in the list

        Returns:
            List[QgsRasterLayer]: A list of checked raster layers.
        """
        checked_items_text = []
        for n in range(self.count()):
            i = self.item(n)
            if i.checkState() == QtCore.Qt.Checked:
                checked_items_text.append(i.text())
        # create checked layers name list
        checked_layers_name = [t.split(" ")[0] for t in checked_items_text]
        layers: List[QgsRasterLayer] = [
            layer
            for layer in self.project.mapLayers().values()
            if layer.type() == QgsMapLayerType.RasterLayer
            and layer.name() in checked_layers_name
        ]
        # save currently selected layer names to keep it selected after calculation
        # finish or layers are added/deleted from layer tree
        self.previously_selected = checked_layers_name
        return layers

    def update_layers(self):
        """
        Updates the list of layers in the widget to the current state
        """
        self.clear()
        # Update the list of layers in the widget whenever layers are
        # added or removed from the legend
        layers = [
            layer
            for layer in self.project.mapLayers().values()
            if layer.type() == QgsMapLayerType.RasterLayer
        ]
        items = [f"{layer.name()} [{layer.crs().authid()}]" for layer in layers]
        for s in items:
            name = s.split(" ")[0]
            i = QtWidgets.QListWidgetItem(s)
            i.setFlags(i.flags() | QtCore.Qt.ItemIsUserCheckable)
            if name in self.previously_selected:
                i.setCheckState(QtCore.Qt.Checked)
            else:
                i.setCheckState(QtCore.Qt.Unchecked)
            self.addItem(i)
