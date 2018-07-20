import QtQuick 2.9
import QtQuick.Controls 2.2

ApplicationWindow {
    id: appWindow
    objectName: "appWindow"
    visible: true
    width: 640
    height: 480
    title: qsTr("Tabs")

    SwipeView {
        id: swipeView
        y: 93
        height: 307
        anchors.topMargin: 94
        objectName: "swipeView"
        anchors.fill: parent
        currentIndex: tabBar.currentIndex

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

    footer: TabBar {
        id: tabBar
        objectName: "tabBar"
        currentIndex: swipeView.currentIndex

        TabButton {
            text: qsTr("Voltar")
            onClicked: {
                parent.currentIndex = parent.currentIndex - 1;
                console.log(parent.currentIndex);
            }
        }
        TabButton {
            text: qsTr("Avançar")
            onClicked: {
                parent.currentIndex = parent.currentIndex + 1;
                console.log(parent.currentIndex);
            }
        }
    }
}
