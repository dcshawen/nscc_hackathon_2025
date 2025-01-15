from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def draw_table(c, data, x, y, col_widths, row_height, font_size, other_info_font_size=7):
    num_cols = len(col_widths)
    num_rows = len(data)
    
    for row in range(num_rows):
        for col in range(num_cols):
            c.setStrokeColor(colors.black)
            c.setFillColor(colors.white)
            c.rect(x + sum(col_widths[:col]), y - row * row_height, col_widths[col], row_height, fill=1)
            c.setFillColor(colors.black)
            text = data[row][col]
            current_font_size = other_info_font_size if col == 3 else font_size
            c.setFont("Helvetica", current_font_size)
            wrapped_text = wrap_text(text, col_widths[col] - 4, current_font_size)
            text_height = len(wrapped_text) * current_font_size
            draw_wrapped_text(c, x + sum(col_widths[:col]) + col_widths[col] / 2, y - row * row_height + (row_height + text_height) / 2 - current_font_size, wrapped_text, current_font_size)

def wrap_text(text, max_width, font_size):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if pdfmetrics.stringWidth(current_line + " " + word, "Helvetica", font_size) <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    lines.append(current_line.strip())
    return lines

def draw_wrapped_text(c, x, y, wrapped_text, font_size):
    for line in wrapped_text:
        text_width = pdfmetrics.stringWidth(line, "Helvetica", font_size)
        c.drawString(x - text_width / 2, y, line)
        y -= font_size

def draw_line_through_points(c, points, x_offset, y_offset):
    if len(points) < 2:
        return  # Need at least two points to draw a line



    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]


        #  MIRROR ON Y AXIS
        # if y1 > 50:
        #     y1 = y1 - 50
        # elif y1 < 50:
        #     y1 = y1 + 50
        # else:
        #     y1 = y1

        # if y2 > 50:
        #     y2 = y1 - 50
        # elif y2 < 50:
        #     y2 = y1 + 50
        # else:
        #     y2 = y2

        c.line(x1 + x_offset, y1 + y_offset, x2 + x_offset, y2 + y_offset)

def create_pdf_with_table(output_filename, employee_data, pay_period_data, fund_dept_data, hourly_rate_data, casual_auxiliary_data, table_data, table_data_week2, font_size=10):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    # Define table position and size for employee info
    col_widths_employee = [150, 300]  # Width of each column for employee info
    row_height_employee = 20  # Height of each row for employee info
    table_width_employee = sum(col_widths_employee)
    x_employee = 35  # Center the table horizontally
    y_employee = height - 100  # Position at the top of the page

    draw_table(c, employee_data, x_employee, y_employee, col_widths_employee, row_height_employee, font_size)

    # Define table position and size for fund/dept info
    col_widths_fund_dept = [50, 50, 50, 50, 50]  # Width of each column for fund/dept info
    row_height_fund_dept = 20  # Height of each row for fund/dept info
    table_width_fund_dept = sum(col_widths_fund_dept)
    x_fund_dept = 35  # Align with employee info table
    y_fund_dept = y_employee - (len(employee_data) + 1) * row_height_employee + 15   # Adjust y position below employee info

    draw_table(c, fund_dept_data, x_fund_dept, y_fund_dept, col_widths_fund_dept, row_height_fund_dept, font_size)

    # Define table position and size for pay period info
    col_widths_pay_period = [140, 140]  # Width of each column for pay period info
    row_height_pay_period = 20  # Height of each row for pay period info
    table_width_pay_period = sum(col_widths_pay_period)
    x_pay_period = x_fund_dept + table_width_fund_dept + 10  # Position to the right of fund/dept table
    y_pay_period = y_fund_dept  # Align vertically with fund/dept table

    draw_table(c, pay_period_data, x_pay_period, y_pay_period, col_widths_pay_period, row_height_pay_period, font_size)

    # Define table position and size for hourly rate info
    col_widths_hourly_rate = [150]  # Width of each column for hourly rate info
    row_height_hourly_rate = 20  # Height of each row for hourly rate info
    table_width_hourly_rate = sum(col_widths_hourly_rate)
    x_hourly_rate = 35  # Position to the left side
    y_hourly_rate = y_fund_dept - (len(fund_dept_data) + 1) * row_height_fund_dept + 15  # Adjust y position below fund/dept info

    draw_table(c, hourly_rate_data, x_hourly_rate, y_hourly_rate, col_widths_hourly_rate, row_height_hourly_rate, font_size)

    # Define table position and size for casual/auxiliary info
    col_widths_casual_auxiliary = [150, 150]  # Width of each column for casual/auxiliary info
    row_height_casual_auxiliary = 20  # Height of each row for casual/auxiliary info
    table_width_casual_auxiliary = sum(col_widths_casual_auxiliary)
    x_casual_auxiliary = (width / 2) - 110  # Position to the right side
    y_casual_auxiliary = y_hourly_rate   # Align vertically with hourly rate info

    draw_table(c, casual_auxiliary_data, x_casual_auxiliary, y_casual_auxiliary, col_widths_casual_auxiliary, row_height_casual_auxiliary, font_size)

    # Define table position and size for week tables
    col_widths = [80, 100, 110, 250]  # Width of each column
    row_height = 20  # Height of each row
    table_width = sum(col_widths)
    x = (width - table_width) / 2  # Center the table horizontally
    y = y_casual_auxiliary - len(casual_auxiliary_data) * row_height_casual_auxiliary - 20  # Adjust y position below casual/auxiliary info

    draw_table(c, table_data, x, y, col_widths, row_height, font_size)
    
    # Draw second table for Week 2 below the first table
    y -= (len(table_data) + 1) * row_height  # Adjust y position for the second table
    draw_table(c, table_data_week2, x, y, col_widths, row_height, font_size)

    # Define table position and size for notes/comments
    col_widths_notes = [100, 400]  # Two columns for notes/comments
    row_height_notes = 40  # Height of the notes/comments row
    y_notes = 125  # Position above the signature boxes

    notes_data = [["Notes/Comments", ""]]
    draw_table(c, notes_data, x, y_notes, col_widths_notes, row_height_notes, font_size)

    # Define position and size for signature boxes
    signature_box_width = 260
    signature_box_height = 100
    x_manager_signature = x
    x_employee_signature = x + signature_box_width + 20
    y_signature = y_notes - signature_box_height - 10

    c.rect(x_manager_signature, y_signature, signature_box_width, signature_box_height)
    c.rect(x_employee_signature, y_signature, signature_box_width, signature_box_height)

    c.drawString(x_manager_signature + 5, y_signature + signature_box_height - 15, "Supervisor's Signature")
    c.drawString(x_employee_signature + 5, y_signature + signature_box_height - 15, "Employee's Signature")

    # Example points to draw a line through in the Supervisor's signature box
    spSignature = [(0, 0), (50, 30), (100, 50), (150, 70), (260, 100)]
    empSignature = [[31,44.125],[31,33.125],[36,26.125],[44,20.125],[53,17.125],[63,18.125],[68,27.125],[69,38.125],[67,48.125],[62,58.125],[56,67.125],[49,73.125],[39,79.125],[29,85.125],[21,88.125],[26,78.125],[32,69.125],[39,62.125],[46,58.125],[55,55.125],[65,54.125],[76,54.125],[87,54.125],[87,57.125],[78,61.125],[71,67.125],[64,72.125],[67,79.125],[76,77.125],[84,73.125],[92,70.125],[100,66.125],[108,58.125],[108,51.125],[101,55.125],[94,62.125],[92,72.125],[99,76.125],[108,79.125],[119,78.125],[128,75.125],[136,69.125],[141,63.125],[142,53.125],[143,47.125],[137,54.125],[130,63.125],[128,73.125],[129,83.125],[136,88.125],[147,88.125],[159,87.125],[172,83.125],[184,79.125],[194,74.125],[200,67.125]]
    draw_line_through_points(c, spSignature, x_manager_signature, y_signature)
    draw_line_through_points(c, empSignature, x_employee_signature, y_signature)

    c.save()

    print("PDF Created")

# Example usage
employee_data = [
    ["Employee Name", "John Doe"],
    ["w#", "w123456"]
]

pay_period_data = [
    ["PAY PERIOD START DATE", "PAY PERIOD END DATE"],
    ["Sunday", "Saturday"]
]

fund_dept_data = [
    ["Fund", "Dept", "Program", "Acct", "Project"],
    ["", "", "", "", ""]
]

hourly_rate_data = [
    ["Hourly Rate"],
    ["$20.00"]
]

casual_auxiliary_data = [
    ["Casual", "Auxiliary"],
    ["X", ""]
]

table_data = [
    ["WEEK 1", "DATE", "HOURS WORKED", "OTHER INFORMATION"],
    ["Sunday", "December 29", "24", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim "],
    ["Monday", "", "", ""],
    ["Tuesday", "", "", ""],
    ["Wednesday", "", "", ""],
    ["Thursday", "", "", ""],
    ["Friday", "", "", ""],
    ["Saturday", "", "", ""],
    ["Total", "", "", ""],  # Add the "Total" row at the bottom
]

table_data_week2 = [
    ["WEEK 2", "DATE", "HOURS WORKED", "OTHER INFORMATION"],
    ["Sunday", "", "", ""],
    ["Monday", "", "", ""],
    ["Tuesday", "", "", ""],
    ["Wednesday", "", "", ""],
    ["Thursday", "", "", ""],
    ["Friday", "", "", ""],
    ["Saturday", "", "", ""],
    ["Total", "", "", ""],  # Add the "Total" row at the bottom
]

create_pdf_with_table("c:/Users/Mrmic/Documents/nscc_hackathon_2025/PDFCreation/output.pdf", employee_data, pay_period_data, fund_dept_data, hourly_rate_data, casual_auxiliary_data, table_data, table_data_week2, font_size=10)