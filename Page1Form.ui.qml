import QtQuick 2.9
import QtQuick.Controls 2.2

Page {
    id: page1
    width: 600
    height: 400

    header: Label {
        text: qsTr("Page 1")
        font.pixelSize: Qt.application.font.pixelSize * 2
        padding: 10
    }

    Label {
        text: qsTr("You are on Page 1.")
        anchors.centerIn: parent
    }

    Button {
        id: button
        x: 250
        y: 220
        text: qsTr("Click me")

        //		onClicked: {
        //			console.log("Clicked!");
        //		}
    }
}
