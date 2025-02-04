import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    visible: true
    width: 240
    height: 480
    title: "Account"

    ComboBox {
        width: 200
        model: accountViewModel.accountList

        onCurrentTextChanged: {
            console.log("account combobox onCurrentTextChanged")
            accountViewModel.currentAccount = currentText
            accountViewModel.account_info()
        }
    }

    Component.onCompleted: {
        console.log("account component completed")
        accountViewModel.login_info()
    }
}
