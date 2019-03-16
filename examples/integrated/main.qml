import QtQuick 2.0
import QtQuick.Controls 2.0
import myapp 1.0

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
