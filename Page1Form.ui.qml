import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.0

Page {
    id: page1
    width: 600
    height: 400

    header: Label {
        text: qsTr("Selecione um arquivo .csv:")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    Button {
        id: bt_buscar_arquivo
        x: 201
        y: 66
        width: 205
        height: 40
        text: qsTr("Procurar")
        font.pointSize: 12

        onClicked: {
            fileDialog.open()
        }
    }

    FileDialog {
        id: fileDialog
        title: "Selecione um arquivo .csv"
        folder: shortcuts.home
        nameFilters: ["Arquivos csv (*.csv)"]

        //Component.onCompleted: visible = false
        visible: false
    }

    ButtonGroup {
        id: cb_delimitador
    }
    function checkedComboBox() {
        if (delimitador_outro.checked === true) {
            delimitador_outro_tf.readOnly = false
        } else
            delimitador_outro_tf.readOnly = true
    }

    RadioButton {
        id: delimitador_ponto_virgula
        x: 201
        y: 171
        text: qsTr(";")
        checked: true
        ButtonGroup.group: cb_delimitador
        onClicked: checkedComboBox()
    }

    RadioButton {
        id: delimitador_virgula
        x: 255
        y: 171
        text: qsTr(",")
        ButtonGroup.group: cb_delimitador
        onClicked: checkedComboBox()
    }

    RadioButton {
        id: delimitador_outro
        x: 304
        y: 171
        ButtonGroup.group: cb_delimitador
        onClicked: checkedComboBox()
    }

    TextField {
        id: delimitador_outro_tf
        x: 347
        y: 171
        width: 59
        height: 40
        font.pointSize: 10
        maximumLength: 1
        placeholderText: "Outro"
        readOnly: true
        /*onClicked: {
            delimitador_outro.checked = true
            this.readOnly = false
        }*/
    }

    Label {
        x: 201
        y: 148
        width: 205
        height: 22
        text: qsTr("Delimitador:")
        rightPadding: 0
        bottomPadding: 0
        leftPadding: 0
        topPadding: 0
        font.pixelSize: 16
        horizontalAlignment: Text.AlignHCenter
        padding: 0
    }

    Label {
        id: lb_nome_arquivo
        x: 0
        y: 116
        width: parent.width
        height: 17
        //text: qsTr("/home/user/Documents/AMOSTRA.csv")
        text: (fileDialog.fileUrl)
        font.bold: true
        horizontalAlignment: Text.AlignHCenter
    }
}
