import os
import pandas as pd
from database.fetch_data import fetch_filtered_student_data, fetch_students_by_reg_nos

def generate_excel_report(selected_students, selected_columns=None):
    """Generates an Excel report based on selected students, semester, and columns."""

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

    # Fetch filtered data from MySQL
    students, records = fetch_students_by_reg_nos(selected_students)
    print(f'Students from database:{students}')
    
    # Check if data was fetched successfully
    if students is None:
        print("⚠️ No student data available for the selected filters.")
        return None
    
    # Convert data to Pandas DataFrames
    df_students = pd.DataFrame(students)
    df_records = pd.DataFrame(records)

    # Ensure DataFrames are not empty before processing
    if df_students.empty:
        print("⚠️ No student data available for the selected filters.")
        return None

    # Compute `no_of_failed_subjects` dynamically
    df_failures = df_records[df_records["result"] == "Fail"].groupby("registered_no").size().reset_index(name="no_of_failed_subjects")

    # Compute `cgpa` dynamically (average SGPA across semesters)
    df_sgpa = df_records.groupby("registered_no")["grade_points"].mean().reset_index(name="cgpa")

    # Merge students with computed columns
    df_report = df_students.merge(df_failures, on="registered_no", how="left")
    df_report = df_report.merge(df_sgpa, on="registered_no", how="left")

    # Fill NaN values (if no failed subjects, set to 0; if no semesters, set CGPA to 0)
    df_report["no_of_failed_subjects"] = df_report["no_of_failed_subjects"].fillna(0).astype(int)
    df_report["cgpa"] = df_report["cgpa"].fillna(0).round(2)
    
    # Select only the requested columns
    
    df_report = df_report[selected_columns]
    # print(f'df_report: {df_report}')

    # Generate unique filename based on filters
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    
    
    filename = f"Student_Report_{timestamp}.xlsx"
    excel_path = os.path.join("output", filename)

    # Write to Excel
    df_report.to_excel(excel_path, index=False, engine="openpyxl")

    # print(f"✅ Excel Report Generated: {excel_path}")
    return excel_path

if __name__ == "__main__":
    # Example Usage:
    selected_columns = ['registered_no', 'name', 'curr_semester', 'branch']
    selected_students = ['23A95A6102', '23A95A6104'] # Example: ["23A95A6102", "CHINTHA SITAMAHALAKSHMI"]
    
    
    generate_excel_report(selected_students, selected_columns)
