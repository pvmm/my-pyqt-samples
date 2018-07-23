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
                }

                delegate: Text {
                    text: name
                    width: parent.width
                    height: 30
                    verticalAlignment: Text.AlignVCenter
                    MouseArea {
                        anchors.fill: parent
                        onClicked: listview1.currentIndex = index
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
                onClicked: console.log('(→) clicked')
            }

            Button {
                text: qsTr('←')
                id: removeButton
                onClicked: console.log('(←) clicked')
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
    }
}
