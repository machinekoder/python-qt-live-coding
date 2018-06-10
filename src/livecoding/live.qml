import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import QtQuick.Window 2.0
import Qt.labs.settings 1.0
import livecoding 1.0

ApplicationWindow {
    id: root
    title: qsTr("Python Qt Live Coding")
    width: 1024
    height: 800
    visible: true
    visibility: Window.AutomaticVisibility

    QtObject {
        id: d

        function reload() {
            busyIndicator.running = true;
            loader.source = "";
            LiveCoding.clearQmlComponentCache();
            loader.source = fileDialog.file;
            busyIndicator.running = false;
        }

        function openWithSystemEditor() {
            LiveCoding.openUrlWithDefaultApplication(fileDialog.file);
        }

        function unload() {
            loader.source = "";
            fileDialog.selected = false;
            browser.update();
        }

        function restart() {
            PythonReloader.restart();
        }
    }

    Settings {
        id: windowSettings
        category: "window"
        property alias width: root.width
        property alias height: root.height
        property alias x: root.x
        property alias y: root.y
        property alias  visibility: root.visibility
    }

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            Button {
                Layout.preferredHeight: 30
                text: qsTr("Edit")
                onClicked: d.openWithSystemEditor()
            }

            Button {
                Layout.preferredHeight: 30
                text: qsTr("Reload")
                onClicked: d.reload()
            }

            Button {
                Layout.preferredHeight: 30
                text: qsTr("Unload")
                onClicked: d.unload()
            }

            Button {
                Layout.preferredHeight: 30
                text: qsTr("Restart")
                onClicked: d.restart()
            }

            Item {
                Layout.fillWidth: true
            }

            BusyIndicator {
                Layout.preferredHeight: 30
                id: busyIndicator
                running: false
            }
        }

        Loader {
            id: loader
            Layout.fillWidth: true
            Layout.fillHeight: true

            onStatusChanged: {
                if (status !== Loader.Error) {
                    return;
                }

                var msg = loader.sourceComponent.errorString();
                errorLabel.text = qsTr("QML Error: Loading QML file failed:\n") + msg;
            }

            Label {
                id: errorLabel
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.Wrap
                visible: loader.status === Loader.Error
            }

            FileSelectionDialog {
                id: fileDialog
                anchors.fill: parent
                model: browser.qmlFiles
                visible: loader.status === Loader.Null

                onSelectedChanged: {
                    if (selected) {
                        d.reload();
                    }
                }
            }

        }
    }

    ProjectBrowser {
        id: browser
        projectPath: userProjectPath
    }

    FileWatcher {
        id: fileWatcher
        fileUrl: browser.projectPath
        recursive: true
        enabled: fileDialog.selected
        onFileChanged: {
            d.reload();
        }
        nameFilters: [
            "*.qmlc",
            "*.jsc",
            "*.pyc",
            ".#*",
            "__pycache__",
            "*___jb_tmp___", // PyCharm safe write
            "*___jb_old___",
        ]
    }

    // add additional components that should only be loaded once here.
}
