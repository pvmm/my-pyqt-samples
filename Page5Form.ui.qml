import QtQuick 2.9
import QtQuick.Controls 2.2
import PySingletonModule 1.0

Page {
    id: page5
    width: 600
    height: 400

    function onDisplay() {
        // Ultima tela antes de confirmar operação.
        next.text = qsTr("Concluir")
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
}

/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
 ##^##*/
