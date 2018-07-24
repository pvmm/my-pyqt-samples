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
                        onDoubleClicked: {
                            listview2.model.append(listview1.model.get(
                                                       listview1.currentIndex))
                            listview1.model.remove(listview1.currentIndex)
                        }
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
                onClicked: {
                    console.log('(→) clicked')
                    listview2.model.append(listview1.model.get(
                                               listview1.currentIndex))
                    listview1.model.remove(listview1.currentIndex)
                }
            }

            Button {
                text: qsTr('←')
                id: removeButton
                onClicked: {
                    console.log('(←) clicked')
                    listview1.model.append(listview2.model.get(
                                               listview2.currentIndex))
                    listview2.model.remove(listview2.currentIndex)
                }
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
                        onDoubleClicked: {
                            listview1.model.append(listview2.model.get(
                                                       listview2.currentIndex))
                            listview2.model.remove(listview2.currentIndex)
                        }
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

/*##^## Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
 ##^##*/
