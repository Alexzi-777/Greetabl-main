import requests
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib import styles
from reportlab.lib.pagesizes import landscape
import io
from reportlab.lib import colors
import os
import pandas as pd
import constants
import util_functions as uf


def download_and_overlay_file(url, id, order_number, build_number, gift_sku, addon_sku):
    try:
        #url = str(url)
        local_filename = url.split('/')[-1]
        local_filename = os.path.join(constants.unprocessed_folder, local_filename)

        if not os.path.isfile(local_filename):
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

        # Create new PDF with Reportlab
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=landscape((936, 1368)))
        # Adjust coordinates for proper positioning within the canvas
        text_x = 713
        text_y = 149

        # Check if addon_sku is not None or empty and add asterisks if needed
        if addon_sku:
            # Add a trailing dash if addon_sku exists
            text = f"{id}-{order_number}-{build_number}-{gift_sku}-({addon_sku})"
        else: 
            # Remove the trailing dash if addon_sku doesn't exist
            text = f"{id}-{order_number}-{build_number}-{gift_sku}"

        fontsize = 5
        c.setFont(styles.getSampleStyleSheet().get('Normal').fontName, fontsize)  # Increase font size for better visibility

        # Draw the white box with opacity
        box_width = 204
        box_height = 10
        box_opacity = 0.98 
        box_color = colors.white

        c.saveState()  # Save the current graphics state

        # Set the opacity using transparency group
        c.setFillColor(box_color)
        c.setFillAlpha(box_opacity)

        # Draw the white box without a stroke (line)
        c.rect(text_x - box_width / 2, text_y - box_height / 2, box_width, box_height, fill=True, stroke=False)

        c.restoreState()  # Restore the previous graphics state

        # Draw the centered text inside the white box
        text_color = colors.black

        c.setFillColor(text_color)
        c.setFontSize(fontsize)  # Adjust the font size as needed

        text_width = c.stringWidth(text)  # Get the width of the text
        text_x_centered = text_x - text_width / 2
        text_y_centered = text_y - box_height / 4  # Adjust the y-coordinate if needed

        c.drawString(text_x_centered, text_y_centered, text)
        c.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)

        # Read existing PDF and add overlay
        reader = PdfReader(local_filename)
        merger = PageMerge(reader.pages[0])  # change this to choose the page
        merger.add(new_pdf.pages[0]).render()

        # Save modified PDF
        writer = PdfWriter()
        for page in reader.pages:
            writer.addPage(page)
        writer.write(local_filename)

        return reader
    
    except Exception as e:
        print(f"Error occurred while processing PDF: {local_filename}")
        print(f"Error details: {e}")

def group_pdf_files(query_type, current_date, current_day):
    if query_type == "daily":
        df = uf.load_data(constants.daily_csv_path)
    elif query_type == "target":
        df = uf.load_data(constants.target_csv_path)
    else:
        print(e)
        exit

    df_sorted = df.sort_values('gift_sku', ignore_index=True)  # Sort the DataFrame by 'gift_sku' and ignore the original index
    df_sorted['id'] = df_sorted.index + 1  # Use the index values as the 'id' column

    try:
        df_sorted.to_csv(constants.export_csv_path, index=False)
    except Exception as e:
        print("Error occurred while creating the CSV file:")
        print(e)

    grouped_pdfs = []

    for index, row in df_sorted.iterrows():
        id = row['id']
        pdf_url = row['pdf_url']
        order_number = row['order_number']
        build_number = row['build_number']
        gift_sku = row['gift_sku']
        addon_sku = row['addon_sku'] if pd.notna(row['addon_sku']) else ''  # Handle NaN values in addon_sku
        existing_pdf = download_and_overlay_file(pdf_url, id, order_number, build_number, gift_sku, addon_sku)
        grouped_pdfs.append(existing_pdf)
        if len(grouped_pdfs) == constants.VAR: 
            if query_type == "daily":
                if (index // constants.VAR) == 0:
                    group_filename = os.path.join(constants.unprocessed_folder, f"{current_day.lower()}_{current_date}.pdf")
                else:
                    group_filename = os.path.join(constants.unprocessed_folder, f"{current_day.lower()}({index // constants.VAR})_{current_date}.pdf")
            else:
                if (index // constants.VAR) == 0:
                    group_filename = os.path.join(constants.unprocessed_folder, f"target_{current_date}.pdf")
                else:
                    group_filename = os.path.join(constants.unprocessed_folder, f"target({index // constants.VAR})_{current_date}.pdf")
                writer = PdfWriter()
                for pdf in grouped_pdfs:
                    for page in pdf.pages:
                        writer.addPage(page)
                writer.write(group_filename)
                grouped_pdfs = []

    # This will handle any remaining PDFs that didn't form a group of VAR
    if len(grouped_pdfs) > 0:
        if query_type == "daily":
            if (index // constants.VAR) == 0:
                group_filename = os.path.join(constants.unprocessed_folder, f"{current_day.lower()}_{current_date}.pdf")
            else:
                group_filename = os.path.join(constants.unprocessed_folder, f"{current_day.lower()}({index // constants.VAR})_{current_date}.pdf")
        else:
            if (index // constants.VAR) == 0:
                group_filename = os.path.join(constants.unprocessed_folder, f"target_{current_date}.pdf")
            else:
                group_filename = os.path.join(constants.unprocessed_folder, f"target({index // constants.VAR})_{current_date}.pdf")
        writer = PdfWriter()
        for pdf in grouped_pdfs:
            for page in pdf.pages:
                writer.addPage(page)
        writer.write(group_filename)

def overlay_regmark_on_pdfs(current_day):
    grouped_pdf_files = os.listdir(constants.unprocessed_folder)

    for file in grouped_pdf_files:
        if file.startswith(f"{current_day.lower()}") or file.startswith(f"target"):
            group_pdf_path = os.path.join(constants.unprocessed_folder, file)
            merged_pdf_path = os.path.join(constants.processed_folder, file)

            with open(group_pdf_path, "rb") as group_pdf_file, open(constants.regmark_pdf_path, "rb") as regmark_pdf_file:
                group_pdf = PdfReader(group_pdf_file)
                regmark_pdf = PdfReader(regmark_pdf_file)

                writer = PdfWriter()

                # Iterate through the pages and overlay REGMARK.pdf on odd-numbered pages
                for i, page in enumerate(group_pdf.pages):
                    if i % 2 == 0:  # Check if the page number is odd
                        regmark_page = regmark_pdf.pages[0]
                        PageMerge(page).add(regmark_page).render()

                    writer.addPage(page)

                # Write the merged PDF with REGMARK to the output file
                with open(merged_pdf_path, "wb") as merged_pdf_file:
                    writer.write(merged_pdf_file)