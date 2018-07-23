import QtQuick 2.9
import QtQuick.Controls 2.2

ApplicationWindow {
    id: appWindow
    objectName: "appWindow"
    visible: true
    width: 640
    height: 480
    title: qsTr("Tabs")

    Rectangle {
        id: rectangle
        x: 0
        y: 0
        width: 640
        height: 93
        color: "#dfdfdf"

        Image {
            id: image
            x: 145
            y: 0
            width: 350
            height: 93
            source: "codeplan.png"
        }
    }

    SwipeView {
        id: view
        y: 93
        height: 307
        anchors.topMargin: 94
        objectName: "view"
        anchors.fill: parent
        //currentIndex: tabBar.currentIndex

        Page1Form {
        }

        Page2Form {
        }

        Page3Form {
        }

        Page4Form {
        }

        Page5Form {
        }

        Page6Form {
        }
    }

    footer: Row {
        id: row
        objectName: "column"

        Button {
            id: previous
            text: qsTr("Voltar")
            width: parent.width / 2
            onClicked: {
                if (view.currentIndex > 0) {
                    view.currentIndex -= 1;
                }
            }
        }
        Button {
            id: next 
            text: qsTr("Avançar")
            width: parent.width / 2
            onClicked: {
                if (view.currentIndex < view.count - 1) {
                    view.currentIndex += 1;
                }
            }
        }
    }
}
