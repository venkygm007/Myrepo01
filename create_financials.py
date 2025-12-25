import pandas as pd
import xlsxwriter

def create_store_financials():
    file_name = "GM_Store_Financials.xlsx"
    workbook = xlsxwriter.Workbook(file_name)
    
    # Define Formats
    header_fmt = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#4F81BD', 'border': 1})
    money_fmt = workbook.add_format({'num_format': '₹#,##0.00', 'border': 1})
    date_fmt = workbook.add_format({'num_format': 'dd/mm/yyyy', 'border': 1})
    percent_fmt = workbook.add_format({'num_format': '0.0%', 'border': 1})
    border_fmt = workbook.add_format({'border': 1})
    profit_fmt = workbook.add_format({'bold': True, 'font_color': '#006100', 'bg_color': '#C6EFCE', 'border': 1, 'num_format': '₹#,##0.00'})
    loss_fmt = workbook.add_format({'bold': True, 'font_color': '#9C0006', 'bg_color': '#FFC7CE', 'border': 1, 'num_format': '₹#,##0.00'})

    # 1. INCOME SHEET
    income_ws = workbook.add_worksheet('Income (Sales)')
    income_headers = ['Date', 'Product', 'Category', 'Quantity', 'Unit Price', 'Total Income']
    for col, header in enumerate(income_headers):
        income_ws.write(0, col, header, header_fmt)
    
    # Sample Income Data
    sample_income = [
        ['01/01/2024', 'Almonds 500g', 'Dryfruits', 10, 450, 4500],
        ['02/01/2024', 'Chicken Pickle 250g', 'Pickles', 5, 180, 900],
        ['03/01/2024', 'Storage Set', 'Plastics', 2, 120, 240],
    ]
    for row, data in enumerate(sample_income):
        income_ws.write(row + 1, 0, data[0], date_fmt)
        income_ws.write(row + 1, 1, data[1], border_fmt)
        income_ws.write(row + 1, 2, data[2], border_fmt)
        income_ws.write(row + 1, 3, data[3], border_fmt)
        income_ws.write(row + 1, 4, data[4], money_fmt)
        income_ws.write_formula(row + 1, 5, f'=D{row+2}*E{row+2}', money_fmt)
    
    income_ws.set_column('A:F', 15)

    # 2. EXPENSES SHEET
    expense_ws = workbook.add_worksheet('Expenses')
    expense_headers = ['Date', 'Expense Type', 'Description', 'Amount']
    for col, header in enumerate(expense_headers):
        expense_ws.write(0, col, header, header_fmt)
        
    sample_expenses = [
        ['01/01/2024', 'Inventory', 'Stock Purchase - Almonds', 3000],
        ['05/01/2024', 'Utilities', 'Electricity Bill', 1200],
        ['10/01/2024', 'Rent', 'Store Rent Jan', 5000],
    ]
    for row, data in enumerate(sample_expenses):
        expense_ws.write(row + 1, 0, data[0], date_fmt)
        expense_ws.write(row + 1, 1, data[1], border_fmt)
        expense_ws.write(row + 1, 2, data[2], border_fmt)
        expense_ws.write(row + 1, 3, data[3], money_fmt)
        
    expense_ws.set_column('A:D', 18)

    # 3. PROFIT & LOSS SUMMARY
    summary_ws = workbook.add_worksheet('Profit & Loss Summary')
    summary_ws.set_column('A:B', 30)
    
    summary_ws.write(0, 0, 'Financial Summary', header_fmt)
    summary_ws.write(0, 1, 'Value', header_fmt)
    
    summary_ws.write(1, 0, 'Total Income (Sales)', border_fmt)
    summary_ws.write_formula(1, 1, "='Income (Sales)'!SUM(F:F)", money_fmt)
    
    summary_ws.write(2, 0, 'Total Expenses', border_fmt)
    summary_ws.write_formula(2, 1, "=Expenses!SUM(D:D)", money_fmt)
    
    summary_ws.write(4, 0, 'Net Profit / Loss', header_fmt)
    summary_ws.write_formula(4, 1, "=B2-B3", profit_fmt) # Simplified; formula will update based on content
    
    # Conditional Formatting for Profit/Loss
    summary_ws.conditional_format('B5', {
        'type':     'cell',
        'criteria': '>=',
        'value':    0,
        'format':   profit_fmt
    })
    summary_ws.conditional_format('B5', {
        'type':     'cell',
        'criteria': '<',
        'value':    0,
        'format':   loss_fmt
    })

    workbook.close()
    print(f"✅ {file_name} created successfully!")

if __name__ == "__main__":
    create_store_financials()
