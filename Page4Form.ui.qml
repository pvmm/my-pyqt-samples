import QtQuick 2.9
import QtQuick.Controls 2.2
import PySingletonModule 1.0

Page {
    id: page4
    width: 600
    height: 400

    header: Label {
        text: qsTr("Quantidade de registros por arquivo:")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    function isChecked(c) {
        return c.checked
    }

    function onFinish() {
        var radio = [rpa_todos, rpa_10, rpa_100, rpa_mil, rpa_10_mil].filter(
                    isChecked).pop()
        PySingleton.registrosPorArquivo(radio.value)
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
            property int value: -1
            ButtonGroup.group: cb_registros_por_arquivo
        }

        RadioButton {
            id: rpa_10
            text: qsTr("10")
            property int value: 10
            ButtonGroup.group: cb_registros_por_arquivo
        }

        RadioButton {
            id: rpa_100
            text: qsTr("100")
            property int value: 100
            ButtonGroup.group: cb_registros_por_arquivo
        }

        RadioButton {
            id: rpa_mil
            text: qsTr("1 000")
            property int value: 1000
            ButtonGroup.group: cb_registros_por_arquivo
        }

        RadioButton {
            id: rpa_10_mil
            text: qsTr("10 000")
            property int value: 10000
            ButtonGroup.group: cb_registros_por_arquivo
        }
    }
}

/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
 ##^##*/
