import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0
import QtQuick.Window 2.0
import example.module 1.0

Item {
    id: root

    Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        color: "red"

        Row {
        }

        Text {
            anchors.centerIn: parent
            text: "fooba"
        }
    }
}
