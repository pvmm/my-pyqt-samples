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

    Row {
        id: row
        x: 30
        y: 66
        width: parent.width * .9
        height: 40
        spacing: 37

        ButtonGroup {
            id: cb_registros_por_arquivo
        }

        RadioButton {
            id: rpa_todos
            text: qsTr("Todos")
            checked: true
            ButtonGroup.group: cb_registros_por_arquivo
        }

        RadioButton {
            id: rpa_10
            text: qsTr("10")
            ButtonGroup.group: cb_registros_por_arquivo
        }

        RadioButton {
            id: rpa_100
            text: qsTr("100")
            ButtonGroup.group: cb_registros_por_arquivo
        }

        RadioButton {
            id: rpa_mil
            text: qsTr("1 000")
            ButtonGroup.group: cb_registros_por_arquivo
        }

        RadioButton {
            id: rpa_10_mil
            text: qsTr("10 000")
            ButtonGroup.group: cb_registros_por_arquivo
        }
    }
}
