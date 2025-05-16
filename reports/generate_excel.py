import os
import pandas as pd
import tempfile
from database.mysql_data_handler import get_students_by_reg_nos

def generate_excel_report(selected_students, selected_columns=None):
    """Generates an Excel report based on selected students and columns."""
    # Validate selected columns
    allowed_columns = [
        'registered_no', 'name', 'curr_semester', 'branch',
        'no_of_failed_subjects', 'cgpa'
    ]
    
    if not selected_columns:
        selected_columns = allowed_columns
    else:
        # Filter out any invalid columns
        selected_columns = [col for col in selected_columns if col in allowed_columns]
        if not selected_columns:
            print("⚠️ No valid columns selected. Using all available columns.")
            selected_columns = allowed_columns
    
    # Fetch data
    students, records, summaries = get_students_by_reg_nos(selected_students)
    print(f'Students from database: {len(students)}')
    
    # Check if data was fetched successfully
    if not students:
        print("⚠️ No student data available for the selected filters.")
        return None
    
    # Convert data to Pandas DataFrames
    df_students = pd.DataFrame(students)
    df_records = pd.DataFrame(records)
    df_summaries = pd.DataFrame(summaries)
    
    # Ensure DataFrames are not empty before processing
    if df_students.empty:
        print("⚠️ No student data available for the selected filters.")
        return None
    
    # Compute `no_of_failed_subjects` dynamically
    if 'no_of_failed_subjects' in selected_columns:
        # Group by registration number and count failed subjects
        if not df_records.empty:
            df_failures = df_records[df_records["result"] == "FAIL"].groupby("registered_no").size().reset_index(name="no_of_failed_subjects")
            df_students = df_students.merge(df_failures, on="registered_no", how="left")
            df_students["no_of_failed_subjects"] = df_students["no_of_failed_subjects"].fillna(0).astype(int)
        else:
            df_students["no_of_failed_subjects"] = 0
    
    # Compute `cgpa` dynamically (average SGPA across semesters)
    if 'cgpa' in selected_columns:
        if not df_summaries.empty:
            # Calculate average SGPA for each student
            df_cgpa = df_summaries.groupby("registered_no")["sgpa"].mean().reset_index(name="cgpa")
            df_students = df_students.merge(df_cgpa, on="registered_no", how="left")
            df_students["cgpa"] = df_students["cgpa"].fillna(0).round(2)
        else:
            df_students["cgpa"] = 0
    
    # Select only the requested columns
    df_report = df_students[selected_columns]
    
    # Create Excel file
    temp_dir = tempfile.gettempdir()
    excel_path = os.path.join(temp_dir, "Student_Report.xlsx")
    
    # Write to Excel with formatting
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df_report.to_excel(writer, sheet_name='Student Report', index=False)
        
        # Get the workbook and the worksheet
        workbook = writer.book
        worksheet = writer.sheets['Student Report']
        
        # Format headers
        for col_num, column_title in enumerate(df_report.columns, 1):
            cell = worksheet.cell(row=1, column=col_num)
            cell.font = workbook.create_font(bold=True)
    
    print(f"✅ Excel report generated: {excel_path}")
    return excel_path

if __name__ == "__main__":
    # Example Usage:
    selected_students = ["22A91A6101", "22A91A6102"]
    selected_columns = ["registered_no", "name", "branch", "curr_semester", "cgpa"]
    excel_path = generate_excel_report(selected_students, selected_columns)
    print(f"Excel report saved to: {excel_path}")