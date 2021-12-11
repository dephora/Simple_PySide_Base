import os
import sys

import PyQt5.QtWidgets

# from PyFlow.Core import NodeBase
# from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
# from PyFlow.Core.Common import *
# from Qt import QtWidgets

# from qgis.core import *
# from qgis.gui import *
# from Qt.QtGui import *
# from Qt.QtCore import *

# from Qt.QtWidgets import QApplication, QMainWindow


from qgis.PyQt.QtGui import QColor

from qgis.PyQt.QtWidgets import QMainWindow, QAction, QWidget, QVBoxLayout

from qgis.PyQt.QtCore import Qt, QRectF, pyqtSignal

from PyQt5.QtCore import Qt

from qgis.core import (
    QgsApplication,
    QgsFeature,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsPoint,
    QgsPointXY,
    QgsProject,
    QgsGeometry,
    QgsMapRendererJob,
)

from qgis.gui import (
    QgsMapCanvas,
    QgsVertexMarker,
    QgsMapCanvasItem,
    QgsMapToolPan,
    QgsMapToolZoom,
    QgsRubberBand,
    QgsMapToolEmitPoint,
)

# from sandbox.mapper.helpers.vectors import create_test_layer

QGSAPP = True


class MapCanvasWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        # Create the canvas
        self.canvas = QgsMapCanvas()
        self.canvas.setCanvasColor(Qt.black)

    def add_layer(self, layer):

        # Set layer
        self.canvas.setExtent(layer.extent())
        self.canvas.setLayers([layer])

        self.actionZoomIn = QAction("Zoom in", self)
        self.actionZoomOut = QAction("Zoom out", self)
        self.actionPan = QAction("Pan", self)

        self.actionZoomIn.setCheckable(True)
        self.actionZoomOut.setCheckable(True)
        self.actionPan.setCheckable(True)

        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionPan.triggered.connect(self.pan)

        # No toolbar as it's a widget, not a window - controls will be redone
        # self.toolbar = self.addToolBar("Canvas actions")
        # self.toolbar.addAction(self.actionZoomIn)
        # self.toolbar.addAction(self.actionZoomOut)
        # self.toolbar.addAction(self.actionPan)

        # create the map tools
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolPan.setAction(self.actionPan)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False)  # false = in
        self.toolZoomIn.setAction(self.actionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True)  # true = out
        self.toolZoomOut.setAction(self.actionZoomOut)

        self.pan()

        # Handle layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.setGeometry(600, 100, 800, 600)
        self.setWindowFlag(Qt.FramelessWindowHint)  # hide title bar

    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self.canvas.setMapTool(self.toolPan)


def create_test_layer():
    """ Example vector layer with a single linestring"""
    layer_info = "LineString?crs=epsg:4326"
    layer = QgsVectorLayer(layer_info, "MyLine", "memory")
    pr = layer.dataProvider()
    linstr = QgsFeature()
    wkt = "LINESTRING (1 1, 10 15, 40 35)"
    geom = QgsGeometry.fromWkt(wkt)
    linstr.setGeometry(geom)
    pr.addFeatures([linstr])
    return layer


def main():
    """ Sample canvas.

    https://docs.qgis.org/3.16/en/docs/pyqgis_developer_cookbook/canvas.html
    https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/intro.html#using-pyqgis-in-custom-applications

    :return:
    """

    # Supply the path to the qgis install location.
    # Doesn't appear necessary when running in conda with `conda-develop` set.
    # QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX'], True)

    # Create a reference to the QgsApplication.
    # Setting the second argument to True enables the GUI.  We need
    # this since this is a custom application.
    app = QgsApplication([], True)

    # Load providers
    app.initQgis()

    # Write your code here to load some layers, use processing
    # algorithms, etc.

    # Create a test layer
    vlayer = create_test_layer()
    vlayer.updateExtents()

    # Create canvas widget and add layer
    map_canvas_widget = MapCanvasWidget()
    map_canvas_widget.add_layer(vlayer)
    map_canvas_widget.show()

    map_canvas_widget.raise_()  # unsure

    # Finally, exitQgis() is called to remove the provider and layer registries from memory
    app.exitQgis()
    sys.exit(app.exec_())

    # app.deleteLater()  # unsure


if __name__ == "__main__":
    main()
