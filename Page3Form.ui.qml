import QtQuick 2.9
import QtQuick.Controls 2.2

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
