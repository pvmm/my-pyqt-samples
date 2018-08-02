import QtQuick 2.9
import QtQuick.Controls 2.2

Page {
    id: page6
    width: 600
    height: 400

    function onStart() {
        // Conclui operação e não permite mais voltar.
        previous.enabled = false
        next.text = qsTr("Fechar")
    }

    header: Label {
        text: qsTr("Arquivos gerados:")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    TextArea {
        id: textArea
        x: 30
        y: 66
        width: parent.width * .9
        height: 210
        text: qsTr("Text Area")
        readOnly: true
    }
}

/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
 ##^##*/
