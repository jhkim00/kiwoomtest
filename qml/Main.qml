import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    visible: true
    width: 1200
    height: 480
    title: "kiwoomtest"

    TextButton {
        id: btnLogin
        width: 200
        height: 30
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 10
        anchors.topMargin: 10
        text: "login"
        textSize: 20
        normalColor: 'grey'
        radius: 4
        onBtnClicked: {
            console.log('btnLogin clicked')

        }
    }
}
