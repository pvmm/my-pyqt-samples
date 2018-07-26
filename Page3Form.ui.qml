import QtQuick 2.9
import QtQuick.Controls 2.2
import PySingletonModule 1.0

Page {
    id: page3
    width: 600
    height: 400
    spacing: -1

    header: Label {
        text: qsTr("Filtro (Opcional):")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    function onDisplay() {
        var combobox_coluna = PySingleton.colunas_disponiveis
        combobox_coluna.unshift('<Selecione>')
        comboBox_filtro_coluna.model = combobox_coluna
        //console.log(PySingleton.preenche_combobox_coluna())
    }

    Grid {
        id: grid
        x: 30
        y: 42
        width: parent.width * .9
        height: 200
        spacing: 5
        columns: 2
        rows: 2

        Label {
            x: 126
            y: 102
            //            color: "#2b2626"
            text: qsTr("Coluna")
            font.pointSize: 12
        }

        Label {
            x: 429
            y: 102
            //            color: "#2b2626"
            text: qsTr("Valor")
            font.pointSize: 12
        }

        ComboBox {
            id: comboBox_filtro_coluna
            x: 16
            y: 135
            width: parent.width * .5
            height: 40
            model: []

            Connections {
                target: PySingleton
                onValoresFiltradosChanged: {
                    console.log('onValoresFiltradosChanged!')
                    comboBox_filtro_valor.model = PySingleton.valores_filtrados
                }
            }

            onDisplayTextChanged: {
                console.log('onDisplayTextChanged.current text = ' + currentText)
                PySingleton.filtraColuna(currentText)
            }
        }

        ComboBox {
            id: comboBox_filtro_valor
            x: 314
            y: 135
            width: parent.width * .5
            height: 40
        }
    }
}
