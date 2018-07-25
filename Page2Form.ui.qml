import QtQuick 2.9
import QtQuick.Controls 2.2
import PySingletonModule 1.0

Page {
    id: page2
    width: 600
    height: 400

    function onDisplay() {
        checaBotaoAvancar()

        // Lista de colunas disponíveis lida do arquivo .CSV.
        if (listview2.model.length === 0) {
            listview1.model = PySingleton.colunas_disponiveis
        }

        // Desativa botão de próximo se não existem colunas disponíveis no arquivo lido.
        if (listview1.model.length === 0) {
            addButton.enabled = false
        }

        listview1.forceActiveFocus()
    }

    function checaBotaoAvancar() {
        if (PySingleton.colunas.length === 0) {
            next.enabled = false
        } else {
            next.enabled = true
        }
    }

    function moveItem(listview1, listview2) {
        var list2 = listview2.model
        list2.push(listview1.model[listview1.currentIndex])
        listview2.model = list2

        var list1 = listview1.model
        list1.splice(listview1.currentIndex, 1)
        listview1.model = list1
    }

    function adicionaColuna() {
        if (PySingleton.colunas.length < 4) {
            if (listview1.model[listview1.currentIndex]) {
                PySingleton.adicionaColuna(
                            listview1.model[listview1.currentIndex])
                moveItem(listview1, listview2)
            }
        }
        if (PySingleton.colunas.length === 4) {
            addButton.enabled = false
        }
        removeButton.enabled = true
        checaBotaoAvancar()
    }

    function removeColuna() {
        if (listview2.model[listview2.currentIndex]) {
            PySingleton.removeColuna(listview2.model[listview2.currentIndex])
            moveItem(listview2, listview1)
            addButton.enabled = true
        }
        if (PySingleton.colunas.length === 0) {
            removeButton.enabled = false
        }
        checaBotaoAvancar()
    }

    header: Text {
        text: qsTr("Selecione no máximo 4 colunas:")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    Column {
        anchors.centerIn: parent

        Row {
            spacing: 5

            Rectangle {
                width: 180
                height: 200
                color: "#ffffff"
                radius: 2
                border.width: 2
                border.color: listview1.focus ? "#6b6b6b" : "#ffffff"

                ListView {
                    id: listview1
                    anchors.margins: 2
                    anchors.fill: parent
                    keyNavigationEnabled: true
                    model: []

                    Keys.onPressed: {
                        if (event.key === Qt.Key_Space)
                            adicionaColuna()
                        else if (event.key === Qt.Key_Return)
                            adicionaColuna()
                        else if (event.key === Qt.Key_Right)
                            listview2.forceActiveFocus()
                    }

                    delegate: Text {
                        text: modelData
                        width: parent.width-2
                        height: 30
                        verticalAlignment: Text.AlignVCenter
                        padding: 2

                        MouseArea {
                            anchors.fill: parent
                            onClicked: listview1.currentIndex = index
                            onDoubleClicked: adicionaColuna()
                        }
                    }
                    highlight: Rectangle {
                        x: 1
                        color: "lightsteelblue"
                        radius: 2
                    }
                    highlightFollowsCurrentItem: true
                }
            }

            Column {
                spacing: 5

                Button {
                    text: qsTr('→')
                    id: addButton
                    onClicked: adicionaColuna()
                }

                Button {
                    text: qsTr('←')
                    id: removeButton
                    enabled: false
                    onClicked: removeColuna()
                }
            }

            Rectangle {
                width: 180
                height: 200
                color: "#ffffff"
                radius: 2
                border.width: 2
                border.color: listview2.focus ? "#6b6b6b" : "#ffffff"

                ListView {
                    id: listview2
                    anchors.margins: 2
                    anchors.fill: parent
                    keyNavigationEnabled: true
                    model: []

                    Keys.onPressed: {
                        if (event.key === Qt.Key_Space)
                            removeColuna()
                        else if (event.key === Qt.Key_Return)
                            removeColuna()
                        else if (event.key === Qt.Key_Left)
                            listview1.forceActiveFocus()
                    }

                    delegate: Text {
                        text: modelData
                        width: parent.width
                        height: 30
                        verticalAlignment: Text.AlignVCenter
                        MouseArea {
                            anchors.fill: parent
                            onClicked: listview2.currentIndex = index
                            onDoubleClicked: removeColuna()
                        }
                    }
                    highlight: Rectangle {
                        color: "lightsteelblue"
                        radius: 2
                    }
                    highlightFollowsCurrentItem: true
                }
            }
        }
    }
}

/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
 ##^##*/
