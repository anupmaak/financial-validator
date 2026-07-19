import csv
from ftplib import all_errors
import json
from datetime import datetime

def validation_transaction(row, line_number):
    # Example validation logic
    "returns error message if validation fails"
    errors = []

    #check for missing values
    required_fields = ['date', 'amount', 'description', 'account']
    for field in required_fields:
        if not row.get(field) or row.get(field).strip() == "":
            errors.append(f"Missing or empty value for field: {field}")

    # check for valid date format
    if row.get('date'):
        try:
            datetime.strptime(row.get('date'), "%Y-%m-%d")
        except ValueError:
            errors.append(f"line {line_number}: Invalid date format. Expected: YYYY-MM-DD")

    # check for valid amount
    if row.get('amount'):
        try:
            amount = float(row['amount'].strip())
            if amount < 0:
                errors.append(f"line {line_number}: Negative amount '{row['amount']}'. Amount must be positive.")
        except ValueError:
            errors.append(f"line {line_number}: Invalid amount. Must be a number.")

    if row.get('account'):
        if not row['account'].strip().startswith("GL-"):
            errors.append(f"line {line_number}: Invalid account format '{row['account']}'. Must start with 'GL-'.")
                
    return errors

def validate_csv(filepath):
    "Reads a CSV file and validates every transaction row."
    "Returns valid rows and a list of all errors found."
    valid_rows = []
    all_errors =[]

    try:
        with open(filepath, newline = "", encoding = "utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for line_number, row in enumerate(reader, start=2):
                errors = validation_transaction(row, line_number)

                if errors:
                    all_errors.extend(errors)
                else:
                    valid_rows.append(row)

    except FileNotFoundError:
       print(f"File not found: {filepath}")
       return [], []
    
    return valid_rows, all_errors

def print_report(valid_rows, all_errors):
     """
    Prints a clean validation report to the terminal.
    """
     print("\n" + "="*50)
     print("Validation Report")
     print("="*50)

     print(f"Total valid rows: {len(valid_rows)}")
     print(f"Total errors found: {len(all_errors)}") 
    
     if all_errors:
         print("Errors found:")
         for error in all_errors:
             print(f" - {error}")
     else:
         print("\n✓ All transactions passed validation.")

     if valid_rows:
         print("\n--- VALID TRANSACTIONS ---")
         for row in valid_rows:
            print(f"  ✓ {row['date']} | {row['account']} | {row['amount']} | {row['description']}")
     print("\n" + "=" * 50)

def main():
    filepath = "transactions.csv"
    print(f"Validating CSV file: {filepath}")

    valid_rows, all_errors = validate_csv(filepath)
    print_report(valid_rows, all_errors)

if __name__ == "__main__":
    main()
     