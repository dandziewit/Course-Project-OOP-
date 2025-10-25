
"""
Payroll proof-of-concept (refactored to meet assignment function requirements)

Requirements implemented:
 - Loop until user types 'End'
 - Separate functions for: name, hours, hourly rate, tax rate input
 - calculate_pay(hours, rate, tax_rate) returns gross, taxes, net
 - display_employee(...) to show per-employee results
 - display_summary(...) to show totals at the end
"""

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


def display_summary(total_employees: int, total_hours: float, total_gross: float, total_taxes: float, total_net: float):
    print()
    print("Summary for all employees:")
    print(f"Total employees: {total_employees}")
    print(f"Total hours worked: {total_hours}")
    print(f"Total gross pay: {money(total_gross)}")
    print(f"Total income taxes: {money(total_taxes)}")
    print(f"Total net pay: {money(total_net)}")


def main():
    print("Payroll entry - enter employee data. Type 'End' for the name to finish.")

    total_employees = 0
    total_hours = 0.0
    total_gross = 0.0
    total_taxes = 0.0
    total_net = 0.0

    while True:
        name = get_employee_name()
        if name.lower() == 'end':
            break
        if name == '':
            print("Name cannot be empty. Try again.")
            continue

        hours = get_hours()
        rate = get_hourly_rate()
        tax_rate = get_income_tax_rate()

        gross, taxes, net = calculate_pay(hours, rate, tax_rate)

        total_employees += 1
        total_hours += hours
        total_gross += gross
        total_taxes += taxes
        total_net += net

        display_employee(name, hours, rate, gross, tax_rate, taxes, net)

    display_summary(total_employees, total_hours, total_gross, total_taxes, total_net)
if __name__ == '__main__':
    main()
