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

from qgis.PyQt.QtWidgets import QMainWindow, QAction

from qgis.PyQt.QtCore import Qt, QRectF

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


# class CircleCanvasItem(QgsMapCanvasItem):
#   def __init__(self, canvas):
#     super().__init__(canvas)
#     self.center = QgsPoint(0, 0)
#     self.size   = 100
#
#   def setCenter(self, center):
#     self.center = center
#
#   def center(self):
#     return self.center
#
#   def setSize(self, size):
#     self.size = size
#
#   def size(self):
#     return self.size
#
#   def boundingRect(self):
#     return QRectF(self.center.x() - self.size/2,
#       self.center.y() - self.size/2,
#       self.center.x() + self.size/2,
#       self.center.y() + self.size/2)
#
#   def paint(self, painter, option, widget):
#     path = QPainterPath()
#     path.moveTo(self.center.x(), self.center.y());
#     path.arcTo(self.boundingRect(), 0.0, 360.0)
#     painter.fillPath(path, QColor("red"))
#


class RectangleMapTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, True)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        self.reset()

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(True)

    def canvasPressEvent(self, e):
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showRect(self.startPoint, self.endPoint)

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        r = self.rectangle()
        if r is not None:
            print("Rectangle:", r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum())

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return

        self.endPoint = self.toMapCoordinates(e.pos())
        self.showRect(self.startPoint, self.endPoint)

    def showRect(self, startPoint, endPoint):
        self.rubberBand.reset(QGis.Polygon)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return

        point1 = QgsPoint(startPoint.x(), startPoint.y())
        point2 = QgsPoint(startPoint.x(), endPoint.y())
        point3 = QgsPoint(endPoint.x(), endPoint.y())
        point4 = QgsPoint(endPoint.x(), startPoint.y())

        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)  # true to update canvas
        self.rubberBand.show()

    def rectangle(self):
        if self.startPoint is None or self.endPoint is None:
            return None
        elif (
            self.startPoint.x() == self.endPoint.x()
            or self.startPoint.y() == self.endPoint.y()
        ):
            return None

            return QgsRectangle(self.startPoint, self.endPoint)

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()

