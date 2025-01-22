from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import pyodbc


employee_data = [
    ["Employee Name", "w#"],
    ["John Doe", "w0000001"]
]

pay_period_data = [
    ["PAY PERIOD START DATE", "PAY PERIOD END DATE"],
    ["January 19th, 2025", "Febuary 1st, 2025"]
]

fund_dept_data = [
    ["Fund", "Dept", "Program", "Acct", "Project"],
    ["Fund A", "Dept A", "Program A", "Acct a", "Project A"]
]

hourly_rate_data = [
    ["Hourly Rate"],
    ["$20"]
]

casual_auxiliary_data = [
    ["Casual", "Auxiliary"],
    ["X", ""]
]

table_data = [
    ["WEEK 1", "DATE", "HOURS WORKED", "OTHER INFORMATION"],
    ["Sunday", "January 19th", "6", ""],
    ["Monday", "January 20th", "2", ""],
    ["Tuesday", "January 21st", "4", ""],
    ["Wednesday", "January 22nd", "0", ""],
    ["Thursday", "January 23rd", "2", ""],
    ["Friday", "January 24th", "4", ""],
    ["Saturday", "January 25th", "4", ""],
    ["Total", "", "22", ""], 
]

table_data_week2 = [
    ["WEEK 2", "DATE", "HOURS WORKED", "OTHER INFORMATION"],
    ["Sunday", "January 26th", "6", ""],
    ["Monday", "January 27th", "4", ""],
    ["Tuesday", "January 28th", "3", ""],
    ["Wednesday", "January 29th", "0", ""],
    ["Thursday", "January 30th", "4.5", ""],
    ["Friday", "January 31st", "2", ""],
    ["Saturday", "Febuary 1st", "0", ""],
    ["Total", "", "19.5", ""], 
]

# # ------------------------------------------VARIABLES------------------------------------------
# # VARIABLES FOR WEEKLY DATA
# # First index
# sun = 1
# mon = 2
# tue = 3
# wed = 4
# thu = 5
# fri = 6
# sat = 7
# total = 8
# # second index
# date = 1
# hours = 2
# otherInfo = 3

# # VARIABLES FOR EMPLOYEE DATA
# # First index
# fund = 0
# dept = 1
# program = 2
# acct = 3
# project = 4
# empName = 0
# wNumber = 1


# # ------------------------------------------EXAMPLE DATA------------------------------------------
# # FIRST INDEX DEFAULTS TO 1
# # EMPLOYEE EXAMPLE DATA
# fund_dept_data[1][fund] = "Fund A"
# fund_dept_data[1][dept] = "Dept A"
# fund_dept_data[1][program] = "Program A"
# fund_dept_data[1][acct] = "Acct A"
# fund_dept_data[1][project] = "Project A"
# employee_data[1][empName] = "John Doe"
# employee_data[1][wNumber] = "W0000001"

# # WEEK 1 EXAMPLE DATA
# table_data[sun][date] = "1: Date sunday"
# table_data[mon][date] = "1: Date monday"
# table_data[tue][date] = "1: Date tuesday"
# table_data[wed][date] = "1: Date wednesday"
# table_data[thu][date] = "1: Date thursday"
# table_data[fri][date] = "1: Date friday"
# table_data[sat][date] = "1: Date saturday"

# table_data[sun][hours] = "1: hours sunday"
# table_data[mon][hours] = "1: hours monday"
# table_data[tue][hours] = "1: hours tuesday"
# table_data[wed][hours] = "1: hours wednesday"
# table_data[thu][hours] = "1: hours thursday"
# table_data[fri][hours] = "1: hours friday"
# table_data[sat][hours] = "1: hours saturday"
# table_data[total][hours] = "1: hours total"

# table_data[sun][otherInfo] = "1: other information sunday"
# table_data[mon][otherInfo] = "1: other information monday"
# table_data[tue][otherInfo] = "1: other information tuesday"
# table_data[wed][otherInfo] = "1: other information wednesday"
# table_data[thu][otherInfo] = "1: other information thursday"
# table_data[fri][otherInfo] = "1: other information friday"
# table_data[sat][otherInfo] = "1: other information saturday"

# # WEEK 2 EXAMPLE DATA
# table_data_week2[1][date] = "2: Date sunday"
# table_data_week2[2][date] = "2: Date monday"
# table_data_week2[3][date] = "2: Date tuesday"
# table_data_week2[4][date] = "2: Date wednesday"
# table_data_week2[5][date] = "2: Date thursday"
# table_data_week2[6][date] = "2: Date friday"
# table_data_week2[7][date] = "2: Date saturday"

# table_data_week2[1][hours] = "2: hours sunday"
# table_data_week2[2][hours] = "2: hours monday"
# table_data_week2[3][hours] = "2: hours tuesday"
# table_data_week2[4][hours] = "2: hours wednesday"
# table_data_week2[5][hours] = "2: hours thursday"
# table_data_week2[6][hours] = "2: hours friday"
# table_data_week2[7][hours] = "2: hours saturday"
# table_data_week2[8][hours] = "2: hours total"

# table_data_week2[1][otherInfo] = "2: other information sunday"
# table_data_week2[2][otherInfo] = "2: other information monday"
# table_data_week2[3][otherInfo] = "2: other information tuesday"
# table_data_week2[4][otherInfo] = "2: other information wednesday"
# table_data_week2[5][otherInfo] = "2: other information thursday"
# table_data_week2[6][otherInfo] = "2: other information friday"
# table_data_week2[7][otherInfo] = "2: other information saturday"

# # CAUSAL/AUXILIARY EXAMPLE DATA (ONE MUST CONTAIN AN X WITH THE OTHER EMPTY)
# casual_auxiliary_data[1][0] = "casual"
# casual_auxiliary_data[1][1] = "auxiliary"

# # PAY PERIOD EXAMPLE DATA
# pay_period_data[1][0] = "start date"
# pay_period_data[1][1] = "end date"

# # HOURLY RATE EXAMPLE DATA
# hourly_rate_data[1][0] = "hourly rate"





# ------------------------------------------DRAWING TABLES------------------------------------------
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
            newSignature.push([signature.x, signature.y])
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
# my signature
spSignature = [0,[55,66],[53,65],[51,65],[47,64],[42,62],[38,58],[36,58],[33,55],[30,50],[27,48],[26,45],[26,44],[26,43],[26,42],[28,41],[33,36],[41,28],[51,22],[57,18],[61,17],[65,16],[67,16],[69,16],[71,17],[77,20],[82,25],[85,28],[91,36],[93,42],[94,46],[94,48],[93,53],[89,60],[81,72],[77,80],[74,86],[73,88],[71,88],[69,91],[63,92],[59,93],[51,94],[47,94],[43,94],[43,94],[42,94],[41,94],[39,92],[36,86],[34,80],[33,74],[32,72],[32,72],[34,70],[43,66],[55,60],[73,51],[87,46],[103,40],[107,40],[109,40],[111,40],[113,41],[113,42],[114,43],[115,48],[115,49],[115,50],[115,51],[115,52],[114,54],[113,55],[113,56],[112,56],[112,57],[112,59],[113,61],[114,68],[117,74],[119,76],[120,78],[124,78],[129,76],[140,60],[147,51],[148,48],[148,46],[149,46],[149,46],[147,46],[147,46],[145,46],[145,46],[145,46],[149,45],[154,45],[156,45],[157,46],[159,49],[159,52],[159,56],[159,57],[159,60],[159,60],[161,61],[162,62],[191,62],[209,68],[213,71],[217,78],[219,85],[219,86],[216,86],[215,80],[217,72],[225,64],[233,62],[243,62],[245,62],-1]
# messed up signature
empSignature = [0,[31,58],[31,58],[30,57],[29,55],[29,54],[29,52],[28,51],[27,50],[27,49],[27,48],[27,47],[27,46],[27,46],[28,45],[29,45],[29,44],[32,42],[36,40],[41,39],[43,38],[46,38],[47,38],[47,38],[48,40],[48,41],[49,45],[49,48],[49,51],[47,56],[47,58],[45,60],[43,64],[41,68],[40,70],[39,71],[37,74],[36,76],[35,78],[33,80],[32,82],[32,82],[31,83],[31,84],[30,84],[29,84],[28,84],[27,84],[26,82],[25,81],[25,80],[25,79],[25,78],[25,77],[26,76],[27,76],[28,74],[30,71],[31,69],[33,67],[34,65],[35,64],[39,62],[40,62],[42,62],[45,61],[46,60],[48,60],[49,60],[50,60],[50,61],[50,62],[51,62],[51,64],[51,65],[51,67],[51,69],[51,70],[51,72],[51,74],[51,75],[49,76],[49,77],[48,78],[47,80],[47,80],[47,80],[47,81],[47,82],[47,82],[48,81],[49,81],[50,80],[51,78],[55,74],[59,69],[61,66],[63,63],[63,62],[64,61],[64,60],[65,59],[65,57],[66,56],[67,56],[67,56],[67,56],[68,56],[69,57],[69,58],[70,59],[70,60],[71,62],[71,62],[71,63],[72,63],[72,64],[73,64],[73,64],[73,63],[73,62],[74,62],[78,58],[81,56],[81,56],[84,55],[85,55],[87,56],[87,56],[87,58],[88,60],[88,61],[88,62],[89,62],[89,62],[90,62],[91,62],[91,62],[93,64],[93,64],[93,65],[95,66],[96,67],[97,70],[98,71],[101,72],[103,74],[110,77],[119,80],[125,83],[129,86],[129,86],[130,87],[131,87],[132,87],[133,86],[133,86],[133,85],[133,85],[133,84],[134,84],[135,84],[136,83],[139,80],[145,72],[147,69],[149,68],[150,67],[151,66],[153,66],[153,65],[155,64],[159,64],[159,64],[160,64],[161,65],[163,67],[166,70],[167,72],[169,72],[170,73],[174,72],[181,66],[185,66],[187,65],[188,65],[189,65],[189,65],[191,64],[191,64],[193,59],[195,57],[200,54],[203,53],[205,53],[209,56],[209,58],[210,60],[211,60],[214,60],[233,54],[247,52]]
# smile face signature
#empSignature = [0,[87,31],[87,33],[87,39],[87,45],[87,51],[87,54],[88,56],[88,58],[88,59],[88,60],[88,60],[88,61],0,[143,40],[143,42],[143,42],[143,44],[143,45],[144,46],[144,47],[145,48],[145,50],[147,52],[147,52],[149,54],[149,56],[149,57],[149,58],[149,58],0,[74,72],[75,72],[77,72],[80,73],[82,74],[84,74],[86,74],[87,74],[89,74],[90,74],[93,75],[95,75],[100,76],[101,76],[103,76],[105,76],[106,78],[107,78],[109,78],[111,78],[112,78],[113,78],[115,78],[115,78],[117,78],[118,78],[119,78],[120,78],[122,78],[123,78],[124,78],[126,78],[127,78],[129,78],[131,78],[133,78],[139,76],[142,76],[145,76],[147,75],[149,75],[149,75],[150,74],[151,74],[151,74],[152,74],[153,73],[155,72],[155,71],[157,71],[157,71],[158,71],[159,71],[160,71],-1]
# cat signature
#empSignature = [0,[73,17],[72,18],[72,20],[72,22],[72,23],[71,24],[71,25],[71,27],[71,28],[71,29],[71,30],[71,30],[71,31],[71,32],[71,33],0,[151,17],[151,18],[151,20],[151,22],[152,23],[152,24],[152,25],[152,27],[152,28],[152,28],[153,29],[153,30],[153,30],[153,31],0,[95,52],[96,52],[97,52],[101,52],[103,52],[104,52],[107,52],[109,52],[109,52],[110,52],[111,52],[111,52],[113,52],[113,52],[114,52],[115,52],[115,52],[116,52],[116,52],[117,52],[117,52],[118,52],[119,52],[119,53],[120,53],[121,53],[121,53],[122,53],[123,53],[124,53],0,[98,54],[99,54],[99,55],[100,57],[101,58],[103,60],[105,62],[106,64],[107,65],[108,67],[109,68],[110,69],[111,70],[111,71],[111,72],[112,72],[113,72],[113,73],0,[125,53],[124,54],[123,55],[123,56],[122,58],[121,58],[121,59],[119,60],[118,61],[117,62],[116,63],[114,64],[113,64],[113,65],[112,66],[111,67],[110,67],[109,68],[108,69],[107,70],[107,70],[107,71],[106,71],[105,72],[105,72],[104,73],[102,74],[101,75],[101,76],[100,76],[99,76],[98,77],[97,77],[96,78],[95,78],[93,78],[93,78],[91,78],[90,77],[89,76],[89,76],[88,76],[87,74],[85,72],[84,71],[84,70],[83,70],[83,70],[83,68],[83,68],[82,68],0,[112,72],[113,72],[113,73],[114,73],[115,73],[115,74],[115,74],[116,74],[117,74],[117,74],[118,74],[119,74],[119,74],[120,75],[121,75],[121,75],[123,75],[123,75],[124,75],[125,75],[125,75],[126,75],[127,75],[127,75],[129,75],[129,75],[130,75],[131,75],[131,75],[132,75],[133,75],[133,74],[133,74],[133,74],[135,74],[135,73],[135,73],[135,72],[136,72],[136,71],[137,70],[137,70],[137,70],0,[172,41],[174,41],[180,39],[184,38],[191,36],[197,33],[201,32],[203,32],[205,31],[205,31],[207,30],[209,30],[209,30],[210,30],[211,28],[211,28],0,[180,55],[182,55],[186,56],[189,56],[190,56],[193,56],[196,56],[198,56],[202,57],[205,57],[207,58],[209,58],[211,58],[213,59],[214,59],[215,60],[217,61],[217,61],[218,61],[217,60],[215,60],0,[185,74],[187,74],[190,75],[190,76],[191,76],[193,76],[196,77],[198,77],[203,79],[205,80],[209,80],[211,81],[212,81],[214,82],[215,82],[216,82],[217,82],[217,82],0,[49,48],[48,47],[43,46],[39,45],[37,44],[35,44],[33,42],[31,40],[29,39],[27,38],[25,36],[24,35],[23,34],[22,33],[21,33],[21,32],[21,33],[23,34],[23,34],[25,36],[25,37],0,[52,61],[51,61],[49,61],[46,61],[43,61],[40,61],[37,61],[33,61],[31,61],[29,61],[27,61],[26,61],[25,61],[24,61],[23,61],[22,61],[21,62],[21,62],[21,62],[21,63],0,[57,74],[49,76],[47,77],[45,78],[43,79],[40,80],[38,81],[37,82],[35,83],[33,84],[32,84],[30,84],[29,86],[29,86],[29,86],[28,86],[28,87],[27,87],[26,87],-1]

# Database connection
def get_db_connection():
    try:
        connection = pyodbc.connect(
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"JG-07\MSSQLSERVER2022;"  # Replace with your server name
            r"DATABASE=EMPTIMESHEET;"  # Replace with your database name
            r"Trusted_Connection=yes;"
        )
        return connection
    except Exception as error:
        print(f"Database connection failed: {error}")
        return None

# Fetch data from the database
def fetch_data(TABLE):
    connection = get_db_connection()
    if connection is None:
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM " + TABLE)  # Replace with your query
            data = cursor.fetchall()
            return data
    except Exception as error:
        print(f"Data fetching failed: {error}")
        return None

# Example usage
if __name__ == "__main__":
    data = fetch_data("EMP_DETAIL") # replace with table name to fetch
    if data:
        for row in data:
            fund_dept_data[1][program] = row[2]
            fund_dept_data[1][dept] = row[3]
            fund_dept_data[1][fund] = row[4]
            fund_dept_data[1][acct] = row[5]
            fund_dept_data[1][project] = row[6]
            employee_data[1][wNumber] = row[1]
            employee_data[1][empName] = row[0]
    else:
        print("Failed to fetch data from the database.")

# loadData(table_data)

create_pdf_with_table("D:\\NSCC\\Winter2025_2ndSem_1stYr\\Hackathon\\Final Hack\\FinalWebPortal-version2 (upto employeesheet fillable)\\timesheet.pdf", employee_data, pay_period_data, fund_dept_data, hourly_rate_data, casual_auxiliary_data, table_data, table_data_week2, spSignature, empSignature, font_size=10)