import QtQuick
import QtQuick.Controls
import myapp

ApplicationWindow {
  id: root
  width: 300
  height: 300
  visible: true
  title: qsTr("Example App")

  MainPanel {
    id: main
    anchors.fill: parent
  }
}
