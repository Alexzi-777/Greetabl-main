import os

# Get the current working directory (where the script is located)
scripts_dir = os.path.dirname(__file__)
main_dir = os.path.join(scripts_dir, '..')

archive_folder = os.path.join(main_dir, "Archives")
csv_archive_folder = os.path.join(archive_folder, "csv-archive")
export_csv_archive_folder = os.path.join(archive_folder, "export-archive")
pdf_archive_folder = os.path.join(archive_folder, "pdf-archive")

# Relative paths to the folders and CSV file
pdf_folder = os.path.join(main_dir, 'PDFs')
processed_folder = os.path.join(pdf_folder, 'processed')
unprocessed_folder = os.path.join(pdf_folder, 'unprocessed')
ungrouped_folder = os.path.join(pdf_folder, 'ungrouped')
grouped_pdfs = os.path.join(pdf_folder, "grouped.pdf")
grouped_pdfs_with_regmarks = os.path.join(processed_folder, "grouped_with_regmarks.pdf")
regmark_pdf_path = os.path.join(pdf_folder, 'REGMARK.pdf')


csv_folder = os.path.join(main_dir, 'CSVs')
temp_csv_folder = os.path.join(csv_folder, 'temp-target')
export_csv_path = os.path.join(csv_folder, 'export_to_sheets.csv')
daily_csv_path = os.path.join(csv_folder, 'daily.csv')
target_csv_path = os.path.join(csv_folder, 'target.csv')

# Define the relative path for the SQL files
sql_folder = os.path.join(main_dir, 'SQLs')
select_query_path = os.path.join(sql_folder, "select.sql")
update_query_path = os.path.join(sql_folder, "update.sql")
copy_command_path = os.path.join(sql_folder, "copy_command.sql")
drop_command_path = os.path.join(sql_folder, "drop_command.sql")

script_folder = os.path.join(main_dir, 'Scripts')


# Set constant literals
VAR = 150

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

create_folder_if_not_exists(archive_folder)
create_folder_if_not_exists(csv_archive_folder)
create_folder_if_not_exists(export_csv_archive_folder)
create_folder_if_not_exists(pdf_archive_folder)
create_folder_if_not_exists(pdf_folder)
create_folder_if_not_exists(processed_folder)
create_folder_if_not_exists(unprocessed_folder)
create_folder_if_not_exists(ungrouped_folder)
create_folder_if_not_exists(csv_folder)
create_folder_if_not_exists(temp_csv_folder)
create_folder_if_not_exists(sql_folder)
create_folder_if_not_exists(script_folder)