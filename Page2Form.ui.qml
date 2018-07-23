import QtQuick 2.9
import QtQuick.Controls 2.2

Page {
    id: page2
    width: 600
    height: 400

    header: Label {
        text: qsTr("Selecione no máximo 4 colunas:")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    Row {
        anchors.centerIn: parent
        spacing: 5

        Rectangle {
            width: 180
            height: 200
            color: "#FFFFFF"
            radius: 2

            Component {
                id: leftContactDelegate
                Item {
                    width: 180
                    height: 20
                    Column {
                        Text {
                            text: name
                        }
                    }
                }
            }

            ListView {
                anchors.fill: parent

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
                }

                delegate: leftContactDelegate
                highlight: Rectangle {
                    color: "lightsteelblue"
                    radius: 2
                }
                focus: true
            }
        }

        Column {
            spacing: 5

            Button {
                text: qsTr('+')
                id: addButton
                onClicked: console.log('(+) clicked')
            }

            Button {
                text: qsTr('-')
                id: removeButton
                onClicked: console.log('(-) clicked')
            }
        }

        Rectangle {
            width: 180
            height: 200
            color: "#FFFFFF"
            radius: 2

            Component {
                id: rightContactDelegate
                Item {
                    width: 180
                    height: 20
                    Column {
                        Text {
                            text: name
                        }
                    }
                }
            }

            ListView {
                anchors.fill: parent

                model: ListModel {
                }

                delegate: rightContactDelegate
                highlight: Rectangle {
                    color: "lightsteelblue"
                    radius: 2
                }
                focus: true
            }
        }
    }
}
