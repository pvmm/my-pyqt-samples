import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Universal 2.2

ApplicationWindow {
    id: appWindow
    objectName: "appWindow"
    visible: true
    width: 640
    height: 480
    title: qsTr("Tabs")
    Universal.background: "#dfdfdf"

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

        Button {
            id: previous
            text: qsTr("Voltar")
            width: parent.width / 2
            enabled: false

            onClicked: {
                next.enabled = true;
                view.currentIndex = Math.max(view.currentIndex - 1, 0);
                if (view.currentIndex === 0) {
                    enabled = false;
                }
            }
        }
        Button {
            id: next 
            text: qsTr("Avançar")
            width: parent.width / 2
            onClicked: {
                previous.enabled = true;
                view.currentIndex = view.currentIndex + 1;

                // Ultima tela antes de confirmar operação.
                if (view.currentIndex === view.count - 2) {
                    text = qsTr("Concluir");
                }

                // Conclui operação e não permite mais voltar.
                if (view.currentIndex === view.count - 1) {
                    row.enabled = false;
                }
            }
        }
    }
}
