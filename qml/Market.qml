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
    }

    StockInputField {
        id: stockInputField
        y: 50
        width: 200
        height: 40

        stockListView: _stockListView

        onReturnPressed: {
            console.log("stockInputField onReturnPressed")
            var stock = stockListView.getCurrentStock()
            if (typeof(stock) !== 'undefined') {
                marketViewModel.setCurrentStock(stock)
            }
        }
    }

    StockListView {
        id: _stockListView
        anchors.top: stockInputField.bottom
        anchors.topMargin: 2
        width: 200
        height: 200
        model: marketViewModel.stockList
    }
}
