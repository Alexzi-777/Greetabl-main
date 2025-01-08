import os
import subprocess
from datetime import datetime, timedelta
import pandas as pd
import constants  
import shutil
from pdfrw import PdfReader, PdfWriter, PageMerge
import pdf_processing

def get_dates():
    today = datetime.now()
    date = today.strftime('%m-%d-%Y')
    day_of_week = today.weekday()
    if day_of_week == 0:  # Monday
        yesterday = today - timedelta(days=3)
    else:
        yesterday = today - timedelta(days=1)
    date_str = yesterday.strftime('%Y-%m-%d')
    today_str = today.strftime('%m-%d-%Y')

    # Calculate the target date range for the new program
    if day_of_week == 1:  # If today is Tuesday
        start_date = today - timedelta(days=4)  # Last Friday
        end_date = today - timedelta(days=1)    # Last Sunday
    elif day_of_week == 0: # If today is Monday
        start_date = today - timedelta(days=4)  # Last Friday
        end_date = today - timedelta(days=3)    # Last Sunday
    else:
        start_date = today - timedelta(days=2)  # Day before yesterday
        end_date = today - timedelta(days=1)    # Day before yesterday

        start_date = start_date.strftime('%m-%d-%Y')
        end_date = end_date.strftime('%m-%d-%Y')

    return today_str, date_str, day_of_week, date, start_date, end_date


def is_valid_date(input_date):
    try:
        # Try to parse the input date
        date_obj = datetime.strptime(input_date, "%m-%d-%Y")
    except ValueError:
        # If parsing fails, it's not a valid date
        return False
    
    # Check if the parsed date is a valid calendar date
    try:
        # Try to create a new date object to ensure it's a valid date
        datetime(date_obj.year, date_obj.month, date_obj.day)
    except ValueError:
        return False
    
    return True

def main_prompt():
    print("Choose an option:")
    print("1.) Run daily query")
    print("2.) Update statuses before a given date")
    print("3.) Process individual orders")
    print("4.) Process individual builds")
    print("5.) Group PDFs and overlay regmarks")
    print("6.) Exit")

    selection = input("Enter your choice: ")
    return selection

def get_current_dates():
    current_date = datetime.now().strftime("%m-%d-%Y")
    current_day = datetime.now().strftime("%A")
    
    return current_date, current_day

def create_daily_csv():
    # Check if daily.csv exists, create an empty file if not
    if not os.path.exists(constants.daily_csv_path):
        #print("daily.csv does not exist. \nCreating an empty file...")
        with open(constants.daily_csv_path, 'w') as empty_csv:
            # Write an empty line to create the file
            empty_csv.write("")
'''
def delete_sql_files():
    for file_name in os.listdir(constants.sql_folder):
        if file_name in ["query.sql", "select.sql", "drop_command.sql", "copy_command.sql"]:
            file_path = os.path.join(constants.sql_folder, file_name)
            if os.path.isfile(file_path):  # To ensure we are only deleting files and not directories
                os.remove(file_path)
'''
def combine_csv_files():
    csv_files = os.listdir(constants.temp_csv_folder)
    dataframes = []

    # Read each CSV file
    for file in csv_files:
        df = pd.read_csv(os.path.join(constants.temp_csv_folder, file))
        dataframes.append(df)

    # Concatenate all DataFrames
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Save the combined DataFrame to the output CSV file
    combined_df.to_csv(constants.target_csv_path, index=False)

def is_valid_order_number(order_number):
    if order_number.startswith('R'):
        order_number = order_number[1:]  # Remove the 'R' if it's the first character

    # Check if the remaining part of the order number contains only digits and has a length of 9
    if order_number.isdigit() and len(order_number) == 9: 
        return True
    return False

def is_valid_build_number(build_number):
    if build_number.startswith('H'):
        build_number = build_number[1:]  # Remove the 'H' if it's the first character

    # Check if the remaining part of the order number contains only digits and has a length of 9
    if build_number.isdigit() and len(build_number) == 11: 
        return True
    return False 

def query_execution(query, csv_name):
    if csv_name == "daily":
        csv_path = constants.daily_csv_path
    elif csv_name == "target":
        index = 1
        csv_path =  os.path.join(constants.temp_csv_folder, f"target{index}.csv")
        while os.path.exists(csv_path):
            index += 1
            csv_path = os.path.join(constants.temp_csv_folder, f"target{index}.csv")
    else:
        raise ValueError("Invalid CSV type provided")
    

    # Generate SQL query
    copy_command = r"\copy (SELECT * FROM persist_view) To '" + csv_path + "' With CSV HEADER;"
    drop_command = "DROP VIEW persist_view;"

     # Write SQL query, copy command, and drop view command to files
    with open(constants.select_query_path, 'w') as f:
        f.write(query)

    # Write the copy command to the file
    with open(constants.copy_command_path, 'w') as f:
        f.write(copy_command)

    # Write the copy command to the file
    with open(constants.drop_command_path, 'w') as f:
        f.write(drop_command)

    # Heroku CLI Execution 
    powershell_command = f'Get-Content "{constants.select_query_path}" |***redacted***'
    subprocess.run(["powershell", "-Command", powershell_command], check=True)

    # Execute copy command using Heroku CLI
    powershell_command = f'Get-Content "{constants.copy_command_path}" |***redacted***'
    subprocess.run(["powershell", "-Command", powershell_command], check=True)

    # Execute drop view command using Heroku CLI
    powershell_command = f'Get-Content "{constants.drop_command_path}" |***redacted***'
    subprocess.run(["powershell", "-Command", powershell_command], check=True)

def update_status_execution(select_query, update_query):
    # Write SQL query to file
    with open(constants.select_query_path, 'w') as f:
        f.write(select_query)

    # Execute SQL query using Heroku CLI to display rows that will be updated
    powershell_command = f'Get-Content {constants.select_query_path} |***redacted***'
    subprocess.run(["powershell", "-Command", powershell_command], check=True)

    # Check user confirmation
    while True:
        confirmation = input("Above are the rows that will be updated. Do you want to proceed? (yes/no): ").lower()
        if confirmation == 'yes':
            # Write SQL query to file
            with open(constants.update_query_path, 'w') as f:
                f.write(update_query)

            # Execute SQL query using Heroku CLI
            powershell_command = f'Get-Content {constants.update_query_path} |***redacted***'
            subprocess.run(["powershell", "-Command", powershell_command], check=True)
            break
        elif confirmation == 'no':
            print("Update operation cancelled.")
            break
        else:
            print("Invalid choice. Please enter 'yes' to proceed or 'no' to cancel.")


# ***** From 2-batch-print ***** #

def load_data(file_path):
    return pd.read_csv(file_path)

def generate_pdfs(query_type):
    current_date, current_day = get_current_dates()

    print("Downloading and grouping PDFs...")

    pdf_processing.group_pdf_files(query_type, current_date, current_day)

    print("Merging...")

    pdf_processing.overlay_regmark_on_pdfs(current_day)

    print("PDF generation is complete! :)\n")


# ***** From scripts ***** #

def move_files_to_archive(source_folder, archive_folder):
    # Move files from source folder to archive folder
    for filename in os.listdir(source_folder):
        source_file_path = os.path.join(source_folder, filename)
        archive_file_path = os.path.join(archive_folder, filename)
        if os.path.isfile(source_file_path):
            os.rename(source_file_path, archive_file_path)

def delete_files_in_folder(folder_path):
    # Delete files in folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def daily_csv_archive(formatted_date):
    csv_archive_file = os.path.join(constants.csv_archive_folder, f"{formatted_date}_daily.csv")

    # Check if archive_file_path already exists, skip archiving if it does
    if not os.path.exists(csv_archive_file):
        os.rename(constants.daily_csv_path, csv_archive_file)

def export_archive(formatted_date, query_type):
    destination_path = os.path.join(constants.export_csv_archive_folder, f'{formatted_date}_export-to-sheets.csv')

    # Check if the destination file already exists
    index = 0
    while os.path.exists(destination_path):
        index += 1
        name, extension = os.path.splitext(f'{formatted_date}_export-to-sheets.csv')
        if query_type == "daily":
            destination_path = os.path.join(constants.export_csv_archive_folder, f"{name}({index}){extension}")
        elif query_type == "target":
            destination_path = os.path.join(constants.export_csv_archive_folder, f"{name}(target-{index}){extension}")

    shutil.copy2(constants.export_csv_path, destination_path)

def pdf_archive():
    source_path = os.listdir(constants.processed_folder)
    current_day_of_week = datetime.now().strftime("%A").lower()
    for file in source_path:
        if file.startswith(f"{current_day_of_week}"):
            source_path = os.path.join(constants.processed_folder, file)
            destination_path = os.path.join(constants.pdf_archive_folder, file)
            if not os.path.exists(destination_path):
                shutil.copy2(source_path, destination_path)

def update_order_completed_date(order_number):
    update_query = f"""UPDATE spree_orders
    SET completed_at = CURRENT_DATE
    WHERE number = '{order_number}';
    """

    with open(constants.update_query_path, 'w') as f:
        f.write(update_query)

    powershell_command = f'Get-Content {constants.update_query_path} |***redacted***'
    subprocess.run(["powershell", "-Command", powershell_command], check=True)

def update_order_status(order_number, state):
    update_query = ""
    if state == "shipped":
        update_query = f"""UPDATE spree_shipments
        SET state = 'shipped'
        FROM spree_orders o
        JOIN spree_builds sb ON o.id = sb.order_id
        JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
        WHERE ss.id = spree_shipments.id
            AND o.number = '{order_number}'
        """
    elif state == "ready":
        update_query = f"""UPDATE spree_shipments
        SET state = 'ready'
        FROM spree_orders o
        JOIN spree_builds sb ON o.id = sb.order_id
        JOIN spree_shipments ss ON sb.ship_address_id = ss.address_id
        WHERE ss.id = spree_shipments.id
            AND o.number = '{order_number}'
        """

    with open(constants.update_query_path, 'w') as f:
        f.write(update_query)

    powershell_command = f'Get-Content {constants.update_query_path} |***redacted***'
    subprocess.run(["powershell", "-Command", powershell_command], check=True)

def update_build_completed_date(build_number):
    update_query = f"""UPDATE spree_builds
    SET completed_at = CURRENT_DATE
    WHERE number = '{build_number}';
    """

    with open(constants.update_query_path, 'w') as f:
        f.write(update_query)

    powershell_command = f'Get-Content {constants.update_query_path} |***redacted***'
    subprocess.run(["powershell", "-Command", powershell_command], check=True)

def update_build_status(build_number, state):
    update_query = ""
    if state == "shipped":
        update_query = f"""
        UPDATE spree_shipments ss
        SET state = 'shipped'
        FROM spree_builds sb, spree_orders o
        WHERE o.id = sb.order_id
        AND sb.ship_address_id = ss.address_id
        AND ss.number = '{build_number}'
        """
    elif state == "ready":
        update_query = f"""
        UPDATE spree_shipments ss
        SET state = 'ready'
        FROM spree_builds sb, spree_orders o
        WHERE o.id = sb.order_id
        AND sb.ship_address_id = ss.address_id
        AND ss.number = '{build_number}'
        """

    with open(constants.update_query_path, 'w') as f:
        f.write(update_query)

    powershell_command = f'Get-Content {constants.update_query_path} |***redacted***'
    subprocess.run(["powershell", "-Command", powershell_command], check=True)

def combine_pdfs():
    ''' Function to combine all PDFs in a folder into a single PDF. '''
    pdf_writer = PdfWriter()

    for pdf_file in sorted(os.listdir(constants.ungrouped_folder)):  # Loops through folder containing PDFs to combine.
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(constants.ungrouped_folder, pdf_file)
            pdf_reader = PdfReader(pdf_path)
            print(f"Processing {pdf_path}")  # Debug print

            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.addpage(pdf_reader.pages[page_num])

    with open(constants.grouped_pdfs, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    print(f"Combined PDF saved as {constants.grouped_pdfs}")  # Debug print

def add_reg_marks():
    ''' Function to add reg marks to odd-numbered pages of a PDF. '''
    pdf_reader = PdfReader(constants.grouped_pdfs)  # Path to the PDF to be modified.
    regmark_reader = PdfReader(constants.regmark_pdf_path)  # Path to the PDF containing the reg marks.
    pdf_writer = PdfWriter()

    # Ensure regmark PDF is read correctly
    if not regmark_reader.pages:
        print(f"Error: Regmark PDF {constants.regmark_pdf_path} could not be read or is empty.")
        return

    for page_num, page in enumerate(pdf_reader.pages):
        # Adding reg marks to odd-numbered pages (1-indexed)
        if (page_num + 1) % 2 == 1:
            regmark_page = regmark_reader.pages[0]
            print(f"Adding reg mark to page {page_num + 1}")  # Debug print
            PageMerge(page).add(regmark_page, prepend=False).render()  # Ensure regmark is added on top

        pdf_writer.addpage(page)

    with open(constants.grouped_pdfs_with_regmarks, 'wb') as modified_pdf:
        pdf_writer.write(modified_pdf)
    print(f"Reg marks added and saved as {constants.grouped_pdfs_with_regmarks}")  # Debug print



    print("PDF grouping and regmark overlay is complete! :)\n")



def run_commands():
    ''' Funciton to restart Heroku and clear the sidekiq queue '''
    heroku_path = r"C:\Program Files\herokuCLI\bin\heroku.exe"

    # Restart Heroku app
    subprocess.run([heroku_path, "restart", "-a", "greetabl"], shell=True)

    # Run Rails console on Heroku
    subprocess.run([heroku_path, "run", "rails", "console", "-a", "greetabl"], shell=True)

    # Clear Sidekiq queue
    subprocess.run(["rails", "runner", "-e", "production", 'queue = Sidekiq::Queue.new("printer")', "queue.clear"], shell=True)