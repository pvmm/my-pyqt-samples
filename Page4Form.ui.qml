import QtQuick 2.9
import QtQuick.Controls 2.2

Page {
    id: page4
    width: 600
    height: 400

    header: Label {
        text: qsTr("Quantidade de registros por arquivo:")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    Label {
        text: qsTr("You are on Page 4.")
        anchors.centerIn: parent
    }
}
