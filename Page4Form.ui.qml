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

    function onFinish() {
        //PySingleton.abreArquivo(lb_nome_arquivo.text)
        var qtdRegistrosPorAquivo
        if (rpa_todos.checked === true)
            qtdRegistrosPorAquivo = rpa_todos.value
        else if (rpa_10.checked === true)
            qtdRegistrosPorAquivo = rpa_10.value
        else if (rpa_100.checked === true)
            qtdRegistrosPorAquivo = rpa_100.value
        else if (rpa_mil.checked === true)
            qtdRegistrosPorAquivo = rpa_mil.value
        else
            qtdRegistrosPorAquivo = rpa_10_mil.value
        PySingleton.registrosPorArquivo(qtdRegistrosPorAquivo)
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
