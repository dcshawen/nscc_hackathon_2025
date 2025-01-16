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
        try:       
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            y1 = 100 - y1
            y2 = 100 - y2
            
            c.line(x1 + x_offset, y1 + y_offset, x2 + x_offset, y2 + y_offset)
        except:
            continue

# insert data into a table, taking in the table and some data format as input
def loadData (table):
    for i in len(table):
        pass

# convert json signature data to work with this script
def convertSignature (signature):
    newSignature = []
    for i in signature:
        if signature.newStroke == True:
            newSignature.push(0)
        else:
            newSignature.push([signature[i].x, signature[i].y])
    return newSignature

def create_pdf_with_table(output_filename, employee_data, pay_period_data, fund_dept_data, hourly_rate_data, casual_auxiliary_data, table_data, table_data_week2, spSignature, empSignature, font_size=10):
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
    
    draw_line_through_points(c, spSignature, x_manager_signature, y_signature)
    draw_line_through_points(c, empSignature, x_employee_signature, y_signature)

    c.save()

    print("PDF Created")



# TABLE DATA
# # Original signatures
spSignatureOrig = []
empSignatureOrig = []
# conver signatures to correct format
spSignature = convertSignature(spSignatureOrig)
empSignature = convertSignature(empSignatureOrig)

# example signatures
#spSignature = [0,[55,66],[53,65],[51,65],[47,64],[42,62],[38,58],[36,58],[33,55],[30,50],[27,48],[26,45],[26,44],[26,43],[26,42],[28,41],[33,36],[41,28],[51,22],[57,18],[61,17],[65,16],[67,16],[69,16],[71,17],[77,20],[82,25],[85,28],[91,36],[93,42],[94,46],[94,48],[93,53],[89,60],[81,72],[77,80],[74,86],[73,88],[71,88],[69,91],[63,92],[59,93],[51,94],[47,94],[43,94],[43,94],[42,94],[41,94],[39,92],[36,86],[34,80],[33,74],[32,72],[32,72],[34,70],[43,66],[55,60],[73,51],[87,46],[103,40],[107,40],[109,40],[111,40],[113,41],[113,42],[114,43],[115,48],[115,49],[115,50],[115,51],[115,52],[114,54],[113,55],[113,56],[112,56],[112,57],[112,59],[113,61],[114,68],[117,74],[119,76],[120,78],[124,78],[129,76],[140,60],[147,51],[148,48],[148,46],[149,46],[149,46],[147,46],[147,46],[145,46],[145,46],[145,46],[149,45],[154,45],[156,45],[157,46],[159,49],[159,52],[159,56],[159,57],[159,60],[159,60],[161,61],[162,62],[191,62],[209,68],[213,71],[217,78],[219,85],[219,86],[216,86],[215,80],[217,72],[225,64],[233,62],[243,62],[245,62],-1]
#empSignature = [0,[87,31],[87,33],[87,39],[87,45],[87,51],[87,54],[88,56],[88,58],[88,59],[88,60],[88,60],[88,61],0,[143,40],[143,42],[143,42],[143,44],[143,45],[144,46],[144,47],[145,48],[145,50],[147,52],[147,52],[149,54],[149,56],[149,57],[149,58],[149,58],0,[74,72],[75,72],[77,72],[80,73],[82,74],[84,74],[86,74],[87,74],[89,74],[90,74],[93,75],[95,75],[100,76],[101,76],[103,76],[105,76],[106,78],[107,78],[109,78],[111,78],[112,78],[113,78],[115,78],[115,78],[117,78],[118,78],[119,78],[120,78],[122,78],[123,78],[124,78],[126,78],[127,78],[129,78],[131,78],[133,78],[139,76],[142,76],[145,76],[147,75],[149,75],[149,75],[150,74],[151,74],[151,74],[152,74],[153,73],[155,72],[155,71],[157,71],[157,71],[158,71],[159,71],[160,71],-1]

employee_data = [
    ["Employee Name", ""],
    ["w#", ""]
]

pay_period_data = [
    ["PAY PERIOD START DATE", "PAY PERIOD END DATE"],
    ["", ""]
]

fund_dept_data = [
    ["Fund", "Dept", "Program", "Acct", "Project"],
    ["", "", "", "", ""]
]

hourly_rate_data = [
    ["Hourly Rate"],
    [""]
]

casual_auxiliary_data = [
    ["Casual", "Auxiliary"],
    ["", ""]
]

table_data = [
    ["WEEK 1", "DATE", "HOURS WORKED", "OTHER INFORMATION"],
    ["Sunday", "", "", ""],
    ["Monday", "", "", ""],
    ["Tuesday", "", "", ""],
    ["Wednesday", "", "", ""],
    ["Thursday", "", "", ""],
    ["Friday", "", "", ""],
    ["Saturday", "", "", ""],
    ["Total", "", "", ""], 
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
    ["Total", "", "", ""], 
]


#loadData(table_data)

create_pdf_with_table("PDFCreation/timesheet.pdf", employee_data, pay_period_data, fund_dept_data, hourly_rate_data, casual_auxiliary_data, table_data, table_data_week2, spSignature, empSignature, font_size=10)