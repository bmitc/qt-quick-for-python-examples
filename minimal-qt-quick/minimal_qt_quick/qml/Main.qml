import QtQuick
import QtQuick.Controls.Universal
import QtQuick.Layouts
import com.backend.model

ApplicationWindow {
    id: root

    visible: true
    title: "Minimal Qt Quick application"
    width: 500
    height: 500

    GridLayout {
        anchors.fill: parent

        rows: 4
        columns: 2

        Label {
            text: "Current time"
        }

        TextField {
            Layout.preferredWidth: 100
            readOnly: false
            text: BackendModel.time
        }

        Label {
            text: "Increment amount"
        }

        SpinBox {
            id: increment
            value: 1
            from: -10
            to: 10
        }

        Item {}

        Button {
            text: "Increment counter"
            onClicked: BackendModel.increment_counter(increment.value)
        }

        Label {
            text: "Counter value"
        }

        TextField {
            readOnly: false
            text: BackendModel.counter
        }
    }
}
