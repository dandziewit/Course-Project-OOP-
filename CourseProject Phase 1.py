
from datetime import datetime
import os


DATA_FILE = os.path.join(os.path.dirname(__file__), 'employees.txt')


def parse_tax_rate(s: str) -> float:
    s = s.strip()
    if s.endswith('%'):
        s = s[:-1]
    v = float(s)
    if v > 1:
        v = v / 100.0
    return v


def money(v: float) -> str:
    return f"${v:,.2f}"


def get_employee_name() -> str:
    return input("Employee name: ").strip()


def get_hours() -> float:
    while True:
        s = input("Hours worked: ").strip()
        try:
            val = float(s)
            if val < 0:
                print("Hours cannot be negative.")
                continue
            return val
        except ValueError:
            print("Please enter a valid number for hours (e.g. 40 or 12.5).")


def get_hourly_rate() -> float:
    while True:
        s = input("Hourly rate: ").strip()
        try:
            val = float(s)
            if val < 0:
                print("Hourly rate cannot be negative.")
                continue
            return val
        except ValueError:
            print("Please enter a valid hourly rate (e.g. 12.50).")


def get_income_tax_rate() -> float:
    while True:
        s = input("Income tax rate (e.g. 20 or 0.2 or 20%): ").strip()
        try:
            r = parse_tax_rate(s)
            if r < 0 or r > 1:
                print("Please enter a reasonable tax rate between 0 and 100%.")
                continue
            return r
        except Exception:
            print("Please enter a valid tax rate (percent or decimal).")


def get_date_range():
    """Prompt for From and To dates in mm/dd/yyyy and return them as strings.
    This function validates the format and will re-prompt on invalid input.
    """
    while True:
        frm = input("From date (mm/dd/yyyy): ").strip()
        to = input("To date (mm/dd/yyyy): ").strip()
        try:
            
            datetime.strptime(frm, "%m/%d/%Y")
            datetime.strptime(to, "%m/%d/%Y")
            return frm, to
        except Exception:
            print("Please enter dates in mm/dd/yyyy format. Try again.")


def calculate_pay(hours: float, rate: float, tax_rate: float):
    gross = hours * rate
    taxes = gross * tax_rate
    net = gross - taxes
    return gross, taxes, net


def display_employee(name: str, hours: float, rate: float, gross: float, tax_rate: float, taxes: float, net: float):
    print()
    print(f"Employee: {name}")
    print(f"Hours worked: {hours}")
    print(f"Hourly rate: {money(rate)}")
    print(f"Gross pay: {money(gross)}")
    print(f"Income tax rate: {tax_rate:.2%}")
    print(f"Income taxes: {money(taxes)}")
    print(f"Net pay: {money(net)}")
    print("-" * 40)


def process_records(records: list) -> dict:
    
    totals = {
        'employees': 0,
        'hours': 0.0,
        'gross': 0.0,
        'taxes': 0.0,
        'net': 0.0,
    }
    for rec in records:
        gross, taxes, net = calculate_pay(rec['hours'], rec['rate'], rec['tax_rate'])
        print()
        print(f"From date: {rec['from']}")
        print(f"To date:   {rec['to']}")
        display_employee(rec['name'], rec['hours'], rec['rate'], gross, rec['tax_rate'], taxes, net)

        totals['employees'] += 1
        totals['hours'] += rec['hours']
        totals['gross'] += gross
        totals['taxes'] += taxes
        totals['net'] += net

    return totals


def append_record_to_file(frm: str, to: str, name: str, hours: float, rate: float, tax_rate: float):
    """Append a single record to the data file in pipe-delimited format.
    Format: from|to|name|hours|rate|tax_rate
    """
    # Normalize the dates to mm/dd/YYYY to ensure consistent storage
    try:
        frm_dt = datetime.strptime(frm, "%m/%d/%Y")
        to_dt = datetime.strptime(to, "%m/%d/%Y")
        frm_s = frm_dt.strftime("%m/%d/%Y")
        to_s = to_dt.strftime("%m/%d/%Y")
    except Exception:
        # If parsing fails, fall back to the raw strings provided
        frm_s = frm
        to_s = to

    line = f"{frm_s}|{to_s}|{name}|{hours}|{rate}|{tax_rate}\n"
    with open(DATA_FILE, 'a', encoding='utf-8') as f:
        f.write(line)


def run_report():
    """Prompt for a From date (or 'All') and read the data file, printing
    the records that match. Compute gross, taxes and net for each and a final
    totals summary.
    """
    
    while True:
        choice = input("Enter From date to report on (mm/dd/yyyy) or 'All': ").strip()
        if choice.lower() == 'all':
            filter_all = True
            break
        try:
            parsed = datetime.strptime(choice, "%m/%d/%Y")
            # Normalize the choice string to the same format we store in the file
            choice = parsed.strftime("%m/%d/%Y")
            filter_all = False
            break
        except Exception:
            print("Please enter dates in mm/dd/yyyy format or 'All'.")

    
    totals = {
        'employees': 0,
        'hours': 0.0,
        'gross': 0.0,
        'taxes': 0.0,
        'net': 0.0,
    }

    if not os.path.exists(DATA_FILE):
        print("No employee records file found.")
        return totals

    with open(DATA_FILE, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                
                continue
            frm, to, name, hours_s, rate_s, tax_rate_s = parts
            if (not filter_all) and (frm != choice):
                continue
            try:
                hours = float(hours_s)
                rate = float(rate_s)
                tax_rate = float(tax_rate_s)
            except Exception:
                
                continue

            gross, taxes, net = calculate_pay(hours, rate, tax_rate)
            print()
            print(f"From date: {frm}")
            print(f"To date:   {to}")
            display_employee(name, hours, rate, gross, tax_rate, taxes, net)

            totals['employees'] += 1
            totals['hours'] += hours
            totals['gross'] += gross
            totals['taxes'] += taxes
            totals['net'] += net

   
    display_summary(totals)
    return totals


def display_summary(totals: dict):
    """Display totals read from the totals dictionary.
    Expected keys: 'employees', 'hours', 'gross', 'taxes', 'net'.
    """
    print()
    print("Summary for all employees:")
    print(f"Total employees: {totals.get('employees', 0)}")
    print(f"Total hours worked: {totals.get('hours', 0.0)}")
    print(f"Total gross pay: {money(totals.get('gross', 0.0))}")
    print(f"Total income taxes: {money(totals.get('taxes', 0.0))}")
    print(f"Total net pay: {money(totals.get('net', 0.0))}")


def main():
    print("Payroll entry - enter employee data. Type 'End' for the name to finish.")
    
    records = []

    while True:
<<<<<<< HEAD
        
=======
       
>>>>>>> 0c47ea6488dd2fd766bf60e81260a928fb8c6c5e
        name = get_employee_name()
        if name.lower() == 'end':
            break
        if name == '':
            print("Name cannot be empty. Try again.")
            continue

        
        frm, to = get_date_range()
        # Normalize the dates immediately so both the in-memory record
        # and the file use the same mm/dd/YYYY format.
        try:
            frm_dt = datetime.strptime(frm, "%m/%d/%Y")
            to_dt = datetime.strptime(to, "%m/%d/%Y")
            frm = frm_dt.strftime("%m/%d/%Y")
            to = to_dt.strftime("%m/%d/%Y")
        except Exception:
            # If parsing fails, leave the original strings
            pass

        hours = get_hours()
        rate = get_hourly_rate()
        tax_rate = get_income_tax_rate()

        records.append({
            'from': frm,
            'to': to,
            'name': name,
            'hours': hours,
            'rate': rate,
            'tax_rate': tax_rate,
        })
        
        try:
            append_record_to_file(frm, to, name, hours, rate, tax_rate)
        except Exception as e:
            print(f"Warning: could not write record to file: {e}")

    # After data entry is finished, run the report prompt so the user
    # can view the saved records. This will ask for a From date or 'All'.
    print()
    run_report()
    
<<<<<<< HEAD
=======
    totals = process_records(records)
    
    display_summary(totals)
>>>>>>> 0c47ea6488dd2fd766bf60e81260a928fb8c6c5e
if __name__ == '__main__':
    main()
