import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Excel Processor")

        self.result_table = QTableWidget(self)
        self.result_table.setGeometry(QtCore.QRect(10, 10, 2000, 1000))
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(['Item Code', 'Item Description', 'Cost', 'Sales', 'Classification', 'Value'])

        self.process_excel()

    def process_excel(self):
        # Define the Excel file path
        excel_file = r"D:\sem-4\bpo\Excel files\VED.xlsx"

        # Read the inventory data from the Excel file
        ved = pd.read_excel(excel_file)

        # Calculate the demand based on the desired columns in your dataset
        ved['demand'] = ved['sales'] + ved['manufacturing_time'] + ved['processing_time'] + ved['transit_time'] + ved['lead_time']

        # Find the column name for demand
        demand_column = 'demand'

        # Check if demand column exists
        if demand_column not in ved.columns:
            self.result_table.setRowCount(1)
            self.result_table.setItem(0, 0, QTableWidgetItem("Demand column not found in the Excel file."))
            return

        # Calculate the value of each item and sort the items by value
        ved['value'] = ved[demand_column] * ved['sales']
        ved = ved.sort_values(by='value', ascending=False)

        # Determine the VED classification for each item
        total_demand = ved[demand_column].sum()
        ved['cumulative_demand'] = ved[demand_column].cumsum() / total_demand
        ved.loc[ved['cumulative_demand'] <= 0.8, 'classification'] = 'Vital'
        ved.loc[(ved['cumulative_demand'] > 0.8) & (ved['cumulative_demand'] <= 0.95), 'classification'] = 'Essential'
        ved.loc[ved['cumulative_demand'] > 0.95, 'classification'] = 'Desirable'

        # Display the results in the table
        self.result_table.setRowCount(len(ved))
        for row in range(len(ved)):
            item_code = QTableWidgetItem(str(ved.iloc[row]['ITEM CODE']))
            item_description = QTableWidgetItem(str(ved.iloc[row]['ITEM DESCRIPTION']))
            cost = QTableWidgetItem(str(ved.iloc[row]['cost']))
            sales = QTableWidgetItem(str(ved.iloc[row]['sales']))
            classification = QTableWidgetItem(str(ved.iloc[row]['classification']))
            value = QTableWidgetItem('{:.2f}'.format(ved.iloc[row]['value']))

            self.result_table.setItem(row, 0, item_code)
            self.result_table.setItem(row, 1, item_description)
            self.result_table.setItem(row, 2, cost)
            self.result_table.setItem(row, 3, sales)
            self.result_table.setItem(row, 4, classification)
            self.result_table.setItem(row, 5, value)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.resize(620, 460)
    main_window.show()
    sys.exit(app.exec())
