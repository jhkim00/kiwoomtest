import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    visible: true
    width: 240
    height: 480
    title: "kiwoomtest"

    TextButton {
        id: btnLogin
        width: 200
        height: 30
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 10
        text: "login"
        textSize: 20
        normalColor: 'lightsteelblue'
        radius: 4
        onBtnClicked: {
            console.log('btnLogin clicked')
            mainViewModel.login()
        }
    }
}
