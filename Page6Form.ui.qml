import QtQuick 2.9
import QtQuick.Controls 2.2

Page {
    id: page6
    width: 600
    height: 400

    header: Label {
        text: qsTr("Arquivos gerados:")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    TextArea {
        id: textArea
        x: 30
        y: 66
        width: parent.width * .9
        height: 210
        text: qsTr("Text Area")
        readOnly: true
    }
}
