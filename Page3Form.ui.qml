import QtQuick 2.9
import QtQuick.Controls 2.2

Page {
    id: page3
    width: 600
    height: 400

    header: Label {
        text: qsTr("Filtro (Opcional):")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    Grid {
        id: grid
        x: 0
        y: 114
        width: 600
        height: 67
        layoutDirection: Qt.LeftToRight
        flow: Grid.LeftToRight
        rows: 2
        columns: 2
        horizontalItemAlignment: Grid.AlignHCenter
        verticalItemAlignment: Grid.AlignHCenter
        spacing: 10.

        Label {
            id: label1
            x: 133
            y: 102
            color: "#2b2626"
            text: qsTr("Coluna")
            font.pointSize: 12
        }

        Label {
            id: label2
            x: 413
            y: 102
            color: "#2b2626"
            text: qsTr("Valor")
            font.pointSize: 12
        }

        ComboBox {
            id: comboBox
            //x: 46
            //y: 127
            //width: 240
            //height: 40
            width: grid.width * .40
        }

        ComboBox {
            id: comboBox1
            //x: 313
            //y: 127
            //width: 240
            //height: 40
            width: parent.width * .40
        }
    }
}
