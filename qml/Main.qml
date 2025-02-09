import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    visible: true
    width: 240
    height: 480
    title: "kiwoomtest"

    Column {
        width: parent.width
        y: 10
        spacing: 10

        TextButton {
            id: btnLogin
            width: 200
            height: 30
            anchors.horizontalCenter: parent.horizontalCenter
            text: "login"
            textSize: 20
            normalColor: 'lightsteelblue'
            radius: 4
            onBtnClicked: {
                console.log('btnLogin clicked')
                mainViewModel.login()
            }
        }

        TextButton {
            id: btnOpenAccountInfo
            width: 200
            height: 30
            anchors.horizontalCenter: parent.horizontalCenter
            text: "open account info"
            textSize: 20
            normalColor: 'lightsteelblue'
            radius: 4
            enabled: mainViewModel.login_completed
            onBtnClicked: {
                console.log('btnOpenAccountInfo clicked')
                mainViewModel.login_info()
            }
        }

        TextButton {
            id: btnOpenCurrentPrice
            width: 200
            height: 30
            anchors.horizontalCenter: parent.horizontalCenter
            text: "open current price"
            textSize: 20
            normalColor: 'lightsteelblue'
            radius: 4
            enabled: mainViewModel.login_completed
            onBtnClicked: {
                console.log('btnOpenCurrentPrice clicked')
                mainViewModel.account_info()
            }
        }
    }
}
