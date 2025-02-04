import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "./component"

ApplicationWindow {
    visible: true
    width: 480
    height: 480
    minimumWidth: 480
    maximumWidth: 480
    minimumHeight: 480
    maximumHeight: 480
    title: "Account"

    Component.onCompleted: {
        console.log("account component completed")
        accountViewModel.login_info()
    }

    ComboBox {
        width: 200
        y: 10
        model: accountViewModel.accountList

        onCurrentTextChanged: {
            console.log("account combobox onCurrentTextChanged")
            accountViewModel.currentAccount = currentText
            accountViewModel.account_info()
        }
    }

    GridView {
        y: 60
        width: parent.width
        height: 400
        cellWidth: 120
        cellHeight: 100
        model: accountViewModel.currentAccountInfo

        delegate: Column {
            width: 120
            spacing: 1
            Rectangle {
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width - 1
                height: 48
                border.width: 1
                color: "lightgrey"
                Text {
                    text: modelData[0]
                    anchors.fill: parent
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }
            Rectangle {
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width - 1
                height: 48
                border.width: 1
                Text {
                    text: modelData[1]
                    anchors.fill: parent
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                }
            }
        }

        onModelChanged: {
            console.log("model changed")
            console.log(model)
        }
    }
}
