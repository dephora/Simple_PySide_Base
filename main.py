################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
## This project can be used freely for all uses, as long as they maintain the
## respective credits only in the Python scripts, any information in the visual
## interface (GUI) can be modified without any implication.
##
## There are limitations on Qt licenses if you want to use your products
## commercially, I recommend reading them on the official website:
## https://doc.qt.io/qtforpython/licenses.html
##
################################################################################

import os
import sys
import platform

# from PySide2 import QtCore, QtGui, QtWidgets
# from PySide2.QtCore import (
#     QCoreApplication,
#     QPropertyAnimation,
#     QDate,
#     QDateTime,
#     QMetaObject,
#     QObject,
#     QPoint,
#     QRect,
#     QSize,
#     QTime,
#     QUrl,
#     Qt,
#     QEvent,
# )
# from PySide2.QtGui import (
#     QBrush,
#     QColor,
#     QConicalGradient,
#     QCursor,
#     QFont,
#     QFontDatabase,
#     QIcon,
#     QKeySequence,
#     QLinearGradient,
#     QPalette,
#     QPainter,
#     QPixmap,
#     QRadialGradient,
# )
# from PySide2.QtWidgets import *

from qgis.PyQt.QtGui import QColor, QFontDatabase

from qgis.PyQt.QtWidgets import QMainWindow, QAction, QWidget, QHeaderView

from qgis.PyQt.QtCore import Qt, QRectF, QSize, QEvent

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

# GUI FILE
from app_modules import *
from mapper.mapper_widget import MapCanvasWidget

# IMPORT FUNCTIONS
from ui_functions import *


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_viewports(self.ui)

        ## PRINT ==> SYSTEM
        print("System: " + platform.system())
        print("Version: " + platform.release())

        ########################################################################
        ## START - WINDOW ATTRIBUTES
        ########################################################################

        ## REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        ## ==> END ##

        ## SET ==> WINDOW TITLE
        self.setWindowTitle("Main Window - Python Base")
        UIFunctions.labelTitle(self, "Main Window - Python Base")
        UIFunctions.labelDescription(self, "Set text")
        ## ==> END ##

        ## WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)
        ## ==> END ##

        ## ==> CREATE MENUS
        ########################################################################

        ## ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(
            lambda: UIFunctions.toggleMenu(self, 220, True)
        )
        ## ==> END ##

        ## ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(
            self, "HOME", "btn_home", "url(:/icons/16x16/cil-home.png)", True
        )
        UIFunctions.addNewMenu(
            self,
            "Users",
            "btn_new_user",
            "url(:/icons/16x16/cil-user-follow.png)",
            True,
        )
        UIFunctions.addNewMenu(
            self,
            "Widgets",
            "btn_widgets",
            "url(:/icons/16x16/cil-equalizer.png)",
            False,
        )
        ## ==> END ##

        # START MENU => SELECTION
        UIFunctions.selectStandardMenu(self, "btn_home")
        ## ==> END ##

        ## ==> START PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        ## ==> END ##

        ## USER ICON ==> SHOW HIDE
        UIFunctions.userIcon(self, "WM", "", True)
        ## ==> END ##

        ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        ## ==> END ##

        ## ==> LOAD DEFINITIONS
        ########################################################################
        UIFunctions.uiDefinitions(self)
        ## ==> END ##

        ########################################################################
        ## END - WINDOW ATTRIBUTES
        ############################## ---/--/--- ##############################

        ########################################################################
        #                                                                      #
        ## START -------------- WIDGETS FUNCTIONS/PARAMETERS ---------------- ##
        #                                                                      #
        ## ==> USER CODES BELLOW                                              ##
        ########################################################################

        ## ==> QTableWidget RARAMETERS
        ########################################################################
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ## ==> END ##

        ########################################################################
        #                                                                      #
        ## END --------------- WIDGETS FUNCTIONS/PARAMETERS ----------------- ##
        #                                                                      #
        ############################## ---/--/--- ##############################

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ########################################################################
    ## MENUS ==> DYNAMIC MENUS FUNCTIONS
    ########################################################################
    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE NEW USER
        if btnWidget.objectName() == "btn_new_user":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_new_user")
            UIFunctions.labelPage(self, "New User")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE WIDGETS
        if btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "Custom Widgets")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    ## ==> END ##

    ########################################################################
    ## START ==> APP EVENTS
    ########################################################################

    ## EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())

    ## ==> END ##

    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print("Mouse click: LEFT CLICK")
        if event.buttons() == Qt.RightButton:
            print("Mouse click: RIGHT CLICK")
        if event.buttons() == Qt.MidButton:
            print("Mouse click: MIDDLE BUTTON")

    ## ==> END ##

    ## EVENT ==> KEY PRESSED
    ########################################################################
    def keyPressEvent(self, event):
        print("Key: " + str(event.key()) + " | Text Press: " + str(event.text()))

    ## ==> END ##

    ## EVENT ==> RESIZE EVENT
    ########################################################################
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print("Height: " + str(self.height()) + " | Width: " + str(self.width()))

    ## ==> END ##

    ########################################################################
    ## END ==> APP EVENTS
    ############################## ---/--/--- ##############################

    def setup_viewports(self, ui):

        # path = os.path.abspath(os.path.dirname(__file__))
        # path_to_gpkg = os.path.join(path, "beziers.gpkg")

        # gpkg_countries_layer = path_to_gpkg + "|layername=beziers"
        # ui.test_vlayer = QgsVectorLayer(
        #     gpkg_countries_layer,
        #     "beziers",
        #     "ogr",
        # )
        # if not ui.test_vlayer.isValid():
        #     print("Layer failed to load!")

        # ui.test_vlayer.updateExtents()

        def create_test_layer():
            """Example vector layer with a single linestring"""
            layer_info = "LineString?crs=epsg:4326"
            layer = QgsVectorLayer(layer_info, "MyLine", "memory")
            pr = layer.dataProvider()
            linstr = QgsFeature()
            wkt = "LINESTRING (1 1, 10 15, 40 35)"
            geom = QgsGeometry.fromWkt(wkt)
            linstr.setGeometry(geom)
            pr.addFeatures([linstr])
            return layer

        ui.viewport1 = MapCanvasWidget()
        ui.viewport2 = MapCanvasWidget()
        ui.viewport3 = MapCanvasWidget()
        ui.viewport4 = MapCanvasWidget()

        ui.layout_viewport.addWidget(ui.viewport1, 0, 0)
        ui.vlayer1 = create_test_layer()
        ui.vlayer1.updateExtents()
        ui.viewport1.add_layer(ui.vlayer1)
        # ui.viewport1.add_layer(ui.test_vlayer)
        ui.viewport1.show()

        ui.layout_viewport.addWidget(ui.viewport2, 0, 1)
        ui.vlayer2 = create_test_layer()
        ui.vlayer2.updateExtents()
        ui.viewport2.add_layer(ui.vlayer2)
        ui.viewport2.show()

        ui.layout_viewport.addWidget(ui.viewport3, 1, 0)
        ui.vlayer3 = create_test_layer()
        ui.vlayer3.updateExtents()
        ui.viewport3.add_layer(ui.vlayer3)
        ui.viewport3.show()

        ui.layout_viewport.addWidget(ui.viewport4, 1, 1)
        ui.vlayer4 = create_test_layer()
        ui.vlayer4.updateExtents()
        ui.viewport4.add_layer(ui.vlayer4)
        ui.viewport4.show()


def create_test_layer():
    """Example vector layer with a single linestring"""
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
    """Sample canvas.

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
    # vlayer = create_test_layer()
    # vlayer.updateExtents()

    QFontDatabase.addApplicationFont("fonts/segoeui.ttf")
    QFontDatabase.addApplicationFont("fonts/segoeuib.ttf")

    window = MainWindow()
    window.show()

    window.raise_()  # unsure

    # Finally, exitQgis() is called to remove the
    # provider and layer registries from memory
    app.exitQgis()
    sys.exit(app.exec_())

    # app.deleteLater()  # unsure


if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     app = QgsApplication(sys.argv)
#     QtGui.QFontDatabase.addApplicationFont("fonts/segoeui.ttf")
#     QtGui.QFontDatabase.addApplicationFont("fonts/segoeuib.ttf")
#     window = MainWindow()
#     sys.exit(app.exec_())
