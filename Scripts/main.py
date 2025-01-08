from datetime import datetime
import util_functions as uf
import sql_queries as sq
import constants as c

def main():

    #uf.run_commands()

    # Get Dates 
    today_str, date_str, day_of_week, date, start_date, end_date = uf.get_dates()


    # Skip weekends
    if day_of_week == 5 or day_of_week == 6:
        print("This script should not be run on Saturday or Sunday. Aborting...")
        exit()

    uf.delete_files_in_folder(c.processed_folder)
    uf.delete_files_in_folder(c.unprocessed_folder)

    while True:
        selection = uf.main_prompt()

        if selection == "1":  # Run daily query
            uf.create_daily_csv()
            uf.query_execution(sq.daily_query(today_str), "daily")
            uf.generate_pdfs("daily")

            # Archive necessary files
            uf.daily_csv_archive(date)
            uf.pdf_archive()
            uf.export_archive(date, "daily")

            # Update Status to Shipped
            uf.update_status_execution(sq.select_daily(today_str), sq.update_daily(today_str))
            uf.update_status_execution(sq.select_scheduled(today_str), sq.update_scheduled(today_str))
            uf.delete_files_in_folder(c.sql_folder)
            break

        elif selection == "2":  # Update statuses before a given date
            while True:
                date = input("Enter a date (ex. '12-1-2023'): ")

                if uf.is_valid_date:
                    uf.update_status_execution(sq.select_daily(date), sq.update_daily(date))
                    uf.update_status_execution(sq.select_scheduled(date), sq.update_scheduled(date))
                    uf.delete_files_in_folder(c.sql_folder)
                    break
                else:
                    print("Invalid date. Please enter a valid date ('mm-dd-yyyy' format).")

        elif selection == "3": # Process individual orders
            while True:
                print("\nChoose an option:")
                print("1.) Generate order PDF")
                print("2.) Update order completed at date")
                print("3.) Update order status")
                print("4.) Exit")

                selection = input("Enter your choice: ")

                if selection == "1":  # Generate order PDF
                    uf.delete_files_in_folder(c.processed_folder)
                    while True:
                        order_numbers = input("\nEnter the order numbers separated by commas (or 'exit' to quit): ")
                        if order_numbers.lower() == 'exit':
                            break
                        uf.delete_files_in_folder(c.temp_csv_folder)
                        order_numbers_list = order_numbers.split(",")
                        for order_number in order_numbers_list:
                            order_number = order_number.strip() # Remove any extra spaces
                            if uf.is_valid_order_number(order_number):
                                uf.query_execution(sq.target_order(order_number), "target")
                            else:
                                print(f"Invalid order number: {order_number}")
                        uf.combine_csv_files()
                        uf.generate_pdfs("target")
                        for order_number in order_numbers_list:
                            order_number = order_number.strip()
                            if uf.is_valid_order_number(order_number):
                                uf.update_status_execution(sq.select_target_order(order_number), sq.update_target_order(order_number))
                        uf.export_archive(date, "target")
                        break
                    break

                elif selection == "2":  # Update order completed at date
                    while True:
                        order_numbers = input("Enter the order numbers separated by commas (or 'exit' to quit): ")
                        if order_numbers.lower() == 'exit':
                            break
                        order_numbers_list = order_numbers.split(",")
                        for order_number in order_numbers_list:
                            order_number = order_number.strip() 
                            if uf.is_valid_order_number(order_number):
                                uf.update_order_completed_date(order_number)
                            else: 
                                print(f"Invalid order number: {order_number}")
                        break
                    break

                elif selection == "3":  # Update order status
                    while True:
                        order_numbers = input("Enter the order numbers separated by commas (or 'exit' to quit): ")
                        if order_numbers.lower() == 'exit':
                            break
                        order_numbers_list = order_numbers.split(",")
                        while True:
                            status = input("Set order to shipped or ready? (shipped/ready): ")
                            if status not in ["shipped", "ready"]:
                                print("Invalid status. Please enter a valid status ('shipped' or 'ready').")
                            else:
                                for order_number in order_numbers_list:
                                    order_number = order_number.strip()
                                    if uf.is_valid_order_number(order_number):
                                        uf.update_order_status(order_number, status)
                                    else: 
                                        print(f"Invalid order number: {order_number}")
                            break
                        break
                    break

                elif selection == "4":
                    print("Operation cancled.\n")
                    break

                else:
                    print("Invalid option!")
            break


        elif selection == "4": # Process individual builds
            while True:
                print("Choose an option:")
                print("1.) Generate build PDF")
                print("2.) Update build completed at date")
                print("3.) Update build status")

                selection = input("Enter your choice: ")

                if selection == "1":  # Generate build PDF
                    uf.delete_files_in_folder(c.processed_folder)
                    while True:
                        build_numbers = input("\nEnter the build numbers separated by commas (or 'exit' to quit): ")
                        if build_numbers.lower() == 'exit':
                            break 
                        uf.delete_files_in_folder(c.temp_csv_folder) 
                        build_numbers_list = build_numbers.split(",")
                        for build_number in build_numbers_list:
                            build_number = build_number.strip()
                            if uf.is_valid_build_number(build_number):
                                uf.query_execution(sq.target_build(build_number), "target")
                            else: 
                                print(f"Invalid build number: {build_number}")
                        uf.combine_csv_files()
                        uf.generate_pdfs("target")
                        for build_number in build_numbers_list:
                            build_number = build_number.strip()
                            if uf.is_valid_order_number(build_number):
                                uf.update_status_execution(sq.select_target_build(build_number), sq.update_target_build(build_number))
                        uf.export_archive(date, "target")
                        break
                    break

                elif selection == "2":  # Update build completed at date
                    while True:
                        build_numbers = input("Enter the build numbers separated by commas (or 'exit' to quit): ")
                        if build_numbers.lower() == 'exit':
                            break
                        build_numbers_list = build_numbers.split(",")
                        for build_number in build_numbers_list:
                            build_number = build_number.strip() 
                            if uf.is_valid_build_number(build_number):
                                uf.update_build_completed_date(build_number)
                            else: 
                                print(f"Invalid build number: {build_number}")
                        break
                    break

                elif selection == "3":  # Update build status
                    while True:
                        build_numbers = input("Enter the build numbers separated by commas (or 'exit' to quit): ")
                        if build_numbers.lower() == 'exit':
                            break
                        build_numbers_list = build_numbers.split(",")
                        while True:
                            status = input("Set build to shipped or ready? (shipped/ready): ")
                            if status not in ["shipped", "ready"]:
                                print("Invalid status. Please enter a valid status ('shipped' or 'ready').")
                            else:
                                for build_number in build_numbers_list:
                                    build_number = build_number.strip()
                                    if uf.is_valid_build_number(build_number):
                                        uf.update_build_status(build_number, status)
                                    else: 
                                        print(f"Invalid build number: {build_number}")
                            break
                        break
                    break

                elif selection == "4":
                    print("Operation cancled.\n")
                    break

                else:
                    print("Invalid option!\n")

        elif selection == "5":
            while True:
                confirmation = input("Place all necesary PDFs in the ungrouped folder. Are you ready to proceed? (y/n): ").lower()
                if confirmation == 'yes' or confirmation == 'y':
                    uf.combine_pdfs()
                    uf.add_reg_marks()
                    break
                elif confirmation == 'no' or confirmation == 'n':
                    print("Operation cancelled.\n")
                    break
                else: 
                    print("Invalid choice. Please enter 'yes' to proceed or 'no' to cancel.")

        elif selection == "6":
            print("Operation cancled.\n")
            break

        else:
            print("Invalid option!\n")

    uf.delete_files_in_folder(c.sql_folder)
    uf.delete_files_in_folder(c.unprocessed_folder)


if __name__ == '__main__':
    main()
