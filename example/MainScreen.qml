import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0
import QtQuick.Window 2.0
import example.module 1.0

Item {
  id: root

  Calculator {
    id: calc
    in1: Number(in1Input.text)
    in2: Number(in2Input.text)
  }

  Rectangle {
    anchors.fill: parent
    anchors.margins: 10
    color: "green"

    Row {
      anchors.centerIn: parent
      spacing: 10

      TextInput {
        id: in1Input
        text: "5"
      }

      Text {
        text: "+"
      }

      TextInput {
        id: in2Input
        text: "4"
      }

      Text {
        text: "="
      }

      Text {
        text: calc.out
      }
    }
  }
}
