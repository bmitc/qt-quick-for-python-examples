"""Python backend for a minimal Qt Quick application. See the QML code defined in qml/Main.qml"""

# These variables *must* be placed prior to the imports due to some particulars of how PySide6
# works. The import name is how QML code can import the singleton object defined in this file.
# In QML, the import can be done like this: `import com.backend.model`
QML_IMPORT_NAME = "com.backend.model"
QML_IMPORT_MAJOR_VERSION = 1

# Core dependencies
import datetime
import sys
from pathlib import Path

# Package dependencies
from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot
from PySide6.QtQml import QmlElement, QmlSingleton, QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

############################################################
#### QML Singleton object ##################################
############################################################


@QmlElement
@QmlSingleton
class BackendModel(QObject):
    TIME_CHANGED = Signal()
    COUNTER_CHANGED = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.__current_time: datetime.time = datetime.datetime.now().time()
        self.__counter: int = 0

        # This timer is used to periodically request the system's time every second so that it can
        # be displayed on the GUI
        self.__system_time_timer = QTimer()

        # The timer interval is in milliseconds
        self.__system_time_timer.setInterval(1000)
        self.__system_time_timer.timeout.connect(self.__update_system_time)
        self.__system_time_timer.start()

    ############################################################
    #### Qt properties for QML #################################
    ############################################################

    @Property(str, notify=TIME_CHANGED)
    def time(self) -> str:
        return self.__current_time.strftime("%H:%M:%S")

    @Property(int, notify=COUNTER_CHANGED)
    def counter(self) -> int:
        return self.__counter

    ############################################################
    #### Slots for QML #########################################
    ############################################################

    @Slot()
    def __update_system_time(self) -> None:
        self.__current_time = datetime.datetime.now().time()
        self.TIME_CHANGED.emit()

    @Slot(int)
    def increment_counter(self, increment_amount: int) -> None:
        self.__counter += increment_amount
        self.COUNTER_CHANGED.emit()


def main() -> None:
    """Main entry point for the application"""

    application = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Load up the top-level QML file
    qml_file = Path(__file__).resolve().parent / "qml" / "Main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    backend_model: BackendModel = engine.singletonInstance(
        QML_IMPORT_NAME, "BackendModel"
    )

    sys.exit(application.exec())


if __name__ == "__main__":
    main()
