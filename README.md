# VED Analysis using Excel Processor

This Python project performs VED (Vital, Essential, Desirable) analysis on inventory data using the Excel Processor application. VED analysis helps classify items based on their criticality and importance for effective inventory management.

## Prerequisites

- Python 3.7 or higher
- PyQt5
- pandas

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ved-analysis.git
   ```

2. Install the required dependencies using pip:

   ```bash
   pip install pandas PyQt5
   ```

## Usage

1. Open the `main.py` file in a text editor or IDE of your choice.

2. Modify the `excel_file` variable in the `process_excel()` method to specify the path to your Excel file containing inventory data:

   ```python
   excel_file = r"path/to/your/inventory.xlsx"
   ```

3. Save the changes.

4. Run the application using the following command:

   ```bash
   python main.py
   ```

5. The Excel Processor window will open, displaying the processed inventory data and the VED analysis results in a table.

## Customization

You can customize the application according to your requirements:

- To modify the displayed columns in the table, edit the `setHorizontalHeaderLabels` line in the `__init__()` method of the `MainWindow` class:

  ```python
  self.result_table.setHorizontalHeaderLabels(['Column 1', 'Column 2', ...])
  ```

- To adjust the thresholds for VED classification or add more classifications, modify the conditions in the `process_excel()` method:

  ```python
  ved.loc[ved['cumulative_demand'] <= 0.8, 'classification'] = 'Vital'
  ved.loc[(ved['cumulative_demand'] > 0.8) & (ved['cumulative_demand'] <= 0.95), 'classification'] = 'Essential'
  ved.loc[ved['cumulative_demand'] > 0.95, 'classification'] = 'Desirable'
  ```

## Acknowledgements

- The Excel Processor application was developed using the [PyQt5](https://pypi.org/project/PyQt5/) library.
- The data processing and analysis were performed using the [pandas](https://pandas.pydata.org/) library.

Feel free to customize this README file further based on your specific project details and requirements.
