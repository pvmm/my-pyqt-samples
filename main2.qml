import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Universal 2.2

ApplicationWindow {
    id: appWindow
    objectName: "appWindow"
    visible: true
    width: 640
    height: 480
    title: qsTr("Geocode")
    Universal.background: "#dfdfdf"
    flags: Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint

    Image {
        id: image
        x: 145
        y: 0
        width: 350
        height: 93
        source: "codeplan.png"
    }

    SwipeView {
        id: view
        y: 93
        height: 307
        anchors.topMargin: 94
        objectName: "view"
        anchors.fill: parent
        interactive: false

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
        objectName: "row"
        spacing: 5

        Button {
            id: previous
            text: qsTr("Voltar")
            width: parent.width / 2
            enabled: false

            onClicked: {
                next.enabled = true;
                view.currentIndex = Math.max(view.currentIndex - 1, 0);

                if (typeof view.currentItem.onStart === "function") {
                    view.currentItem.onStart()
                }
            }
        }
        Button {
            id: next
            text: qsTr("Avançar")
            width: parent.width / 2
            enabled: false

            onClicked: {
                // Se onFinish() existir e retornar false, cancela o avanço de tela.
                if (typeof view.currentItem.onFinish === "function") {
                    if (view.currentItem.onFinish() === false) {
                        return
                    }
                }

                previous.enabled = true;
                view.currentIndex = view.currentIndex + 1;

                if (view.currentIndex == view.count) {
                    Qt.exit(0)
                } else if (typeof view.currentItem.onStart === "function") {
                    view.currentItem.onStart()
                }
            }
        }
    }
}
