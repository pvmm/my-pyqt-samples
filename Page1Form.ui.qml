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
        id: button
        x: 150
        y: 119
        width: parent.width / 2
        text: qsTr("Procurar")
        font.pointSize: 12

        //onClicked: {

        //fileDialog.open()
        //}
    }

    FileDialog {
        id: fileDialog
        title: "Selecione um arquivo .csv"
        folder: shortcuts.home

        Component.onCompleted: visible = false
    }

    Label {
        id: label
        x: 150
        y: 172
        text: qsTr("Delimitador:")
        font.pointSize: 12
    }

    RadioButton {
        id: radioButton
        x: 245
        y: 161
        text: qsTr(";")
    }

    RadioButton {
        id: radioButton1
        x: 299
        y: 161
        text: qsTr(",")
    }

    RadioButton {
        id: radioButton2
        x: 348
        y: 161
        /*onClicked: {
            delimitador_outro.readOnly = true
        }*/
    }

    TextField {
        id: delimitador_outro
        x: 391
        y: 161
        width: 59
        height: 40
        maximumLength: 1
        placeholderText: "Outro"
        readOnly: true
    }
}
