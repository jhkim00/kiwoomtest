import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    visible: true
    x: 0
    y: 480
    width: fixedWidth
    height: fixedHeight
    minimumWidth: fixedWidth
    maximumWidth: fixedWidth
    minimumHeight: fixedHeight
    maximumHeight: fixedHeight
    title: "Market"

    property var fixedWidth: 840
    property var fixedHeight: 480

    Component.onCompleted: {
        console.log("market component completed")
        marketViewModel.load()
    }

    ComboBox {
        id: comboBox
        width: 200
        y: 10
        model: marketViewModel.stockComboBoxModel
        textRole: "display"

        /*onCurrentTextChanged: {
            console.log("market combobox onCurrentTextChanged")
        }*/
    }
}
