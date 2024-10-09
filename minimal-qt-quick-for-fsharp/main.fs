/// F# backend for a minimal Qt Quick application

// I don't know how this would be handled
// QML_IMPORT_NAME = "com.backend.model"
// QML_IMPORT_MAJOR_VERSION = 1

// Core dependencies
open System

// Package dependencies
open PySide6.QtCore
open PySide6.QtQml
open PySide6.QtWidgets

[<QmlElement; QmlSingleton>]
type BackendModel() =
    inherit QObject()

    let timeChanged = Signal()
    let counterChanged = Signal()

    let mutable currentTime = DateTime.Now
    let mutable counter = 0

    [<Slot()>]
    let updateSystemTime () =
        currentTime <- DateTime.Now
        timeChanged.Emit()

    let systemTimeTimer = QTimer()
    systemTimeTimer.Interval <- 1000
    systemTimeTimer.Timeout.Connect(updateSystemTime)

    do
        systemTimeTimer.Start()

    [<Property; Notify=time_changed>]
    member this.Time = currentTime.ToString("HH:mm:ss")

    [<Property; Notify=counter_changed>]
    member this.Counter = counter

    [<Slot(int)>]
    member this.IncrementCounter incrementAmount =
        counter <- counter + incrementAmount
        counterChanged.Emit()


application = QApplication(Environment.GetCommandLineArgs())
engine = QQmlApplicationEngine()

qmlFile = "Main.qml"
engine.load(qmlFile)

if not engine.rootObjects():
    exit -1

backendModel = engine.SingletonInstance("com.backend.model", "BackendModel")

application.Exec()
