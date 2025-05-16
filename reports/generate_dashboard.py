import matplotlib.pyplot as plt
import numpy as np
import os
import base64
from io import BytesIO

def generate_histogram(student_name, sgpa_list, current_semester):
    """Generate a line chart of SGPA values for the student."""
    if not sgpa_list:
        return ""
    
    plt.figure(figsize=(10, 5))
    
    # Create x-axis labels (semesters)
    semesters = [f"Sem {i+1}" for i in range(len(sgpa_list))]
    
    # Set up the line chart
    plt.plot(semesters, sgpa_list, marker='o', linestyle='-', color='#4568dc', linewidth=2, markersize=8)
    
    # Add a horizontal line for the average SGPA
    avg_sgpa = sum(sgpa_list) / len(sgpa_list)
    plt.axhline(y=avg_sgpa, color='#b06ab3', linestyle='--', label=f'Average SGPA: {avg_sgpa:.2f}')
    
    # Add data labels above each point
    for i, sgpa in enumerate(sgpa_list):
        plt.text(i, sgpa + 0.1, f'{sgpa:.2f}', ha='center', va='bottom', fontsize=9)
    
    # Set chart title and labels
    plt.title(f'Semester-wise SGPA Trend for {student_name}', fontsize=12, fontweight='bold')
    plt.xlabel('Semester', fontsize=10)
    plt.ylabel('SGPA', fontsize=10)
    
    # Set y-axis limits
    plt.ylim(0, 10.5)  # SGPA is typically on a scale of 0-10
    
    # Add grid lines for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add legend
    plt.legend(fontsize=9)
    
    # Make it look nice
    plt.tight_layout()
    
    # Save to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    
    # Convert to base64 for embedding in HTML
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Return HTML with embedded image
    return f'<img src="data:image/png;base64,{image_base64}" alt="SGPA Chart" style="max-width:100%;">'

if __name__ == "__main__":
    # Test the function
    student_name = "Test Student"
    sgpa_list = [8.5, 9.0, 8.7, 9.2, 9.5]
    current_semester = 6
    
    html = generate_histogram(student_name, sgpa_list, current_semester)
    
    # Save the HTML to a file for testing
    with open("test_chart.html", "w") as f:
        f.write(f"<html><body>{html}</body></html>")