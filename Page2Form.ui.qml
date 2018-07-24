import QtQuick 2.9
import QtQuick.Controls 2.2
import PySingletonModule 1.0

Page {
    id: page2
    width: 600
    height: 400

    function onDisplay() {
        checaBotaoAvancar()
    }

    function checaBotaoAvancar() {
        if (PySingleton.colunas === 0) {
            next.enabled = false
        } else {
            next.enabled = true
        }
    }

    function moveItem(listview1, listview2) {
        listview2.model.append(listview1.model.get(listview1.currentIndex))
        listview1.model.remove(listview1.currentIndex)
    }

    function adicionaColuna() {
        if (PySingleton.colunas < 4) {
            if (listview1.model.get(listview1.currentIndex)) {
                PySingleton.adicionaColuna(listview1.model.get(
                                               listview1.currentIndex).name)
                moveItem(listview1, listview2)
            }
        }
        if (PySingleton.colunas === 4) {
            addButton.enabled = false
        }
        removeButton.enabled = true
        checaBotaoAvancar()
    }

    function removeColuna() {
        if (listview2.model.get(listview2.currentIndex)) {
            PySingleton.removeColuna(listview2.model.get(
                                         listview2.currentIndex).name)
            moveItem(listview2, listview1)
            addButton.enabled = true
        }
        if (PySingleton.colunas === 0) {
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
                color: "#FFFFFF"
                radius: 2

                ListView {
                    id: listview1
                    anchors.fill: parent
                    keyNavigationEnabled: true

                    model: ListModel {
                        ListElement {
                            name: "RA"
                        }
                        ListElement {
                            name: "Endereço"
                        }
                        ListElement {
                            name: "CEP"
                        }
                        ListElement {
                            name: "AAA"
                        }
                        ListElement {
                            name: "BBB"
                        }
                    }

                    delegate: Text {
                        text: name
                        width: parent.width
                        height: 30
                        verticalAlignment: Text.AlignVCenter
                        MouseArea {
                            anchors.fill: parent
                            onClicked: listview1.currentIndex = index
                            onDoubleClicked: adicionaColuna()
                        }
                    }
                    highlight: Rectangle {
                        color: "lightsteelblue"
                        radius: 2
                    }
                    highlightFollowsCurrentItem: true
                    focus: true
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
                color: "#FFFFFF"
                radius: 2

                ListView {
                    id: listview2
                    anchors.fill: parent
                    keyNavigationEnabled: true

                    model: ListModel {
                    }

                    delegate: Text {
                        text: name
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
                    //focus: true
                }
            }
        }
    }
}

/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
 ##^##*/
