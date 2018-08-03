import QtQuick 2.9
import QtQuick.Controls 2.2
import PySingletonModule 1.0
import QtQuick.Dialogs 1.2

Page {
    id: page5
    width: 600
    height: 400
    property int quantidadeRegistros: 0

    function onStart() {
        // Ultima tela antes de confirmar operação.
        next.text = qsTr("Concluir")
        quantidadeRegistros = PySingleton.quantidade_registros
    }

    function onFinish() {
        progressDialog.visible = true
        PySingleton.iniciaOperacao()
    }

    header: Label {
        text: qsTr("Serviço de Geocodificação:")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    TextField {
        id: textField
        x: 30
        y: 66
        width: parent.width * .9
        height: 40
        text: PySingleton.url
    }

    Dialog {
        id: progressDialog
        visible: false
        title: qsTr("Processando...")
        standardButtons: StandardButton.Cancel

        Text {
            id: mensagem
            text: qsTr("Atualizando contador de processamento: %1 de %2").arg(
                      0).arg(quantidadeRegistros)
        }

        onButtonClicked: PySingleton.cancelaOperacao()
    }

    Connections {
        target: PySingleton
        onRegistroProcessado: {
            console.log('onRegistroProcessado: ' + indice)
            mensagem.text = qsTr(
                        "Atualizando contador de processamento: %1 de %2").arg(
                        indice).arg(quantidadeRegistros)
        }
        onStatusOperacaoChanged: {
            console.log('onStatusOperacaoChanged: ' + status)

            if (status == 0) {
                progressDialog.standardButtons = StandardButton.OK
            } else {
                progressDialog.standardButtons = StandardButton.OK
                mensagem.text = erro
            }
        }
    }
}

/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
 ##^##*/
