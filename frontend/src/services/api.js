// API service for making requests to the backend
const getApiBaseUrl = () => {
  // Get the hostname from the current URL
  const hostname = window.location.hostname;
  return `http://${hostname}:5000/api`;
};

const API_BASE_URL = getApiBaseUrl();

export const api = {
  // Student data
  fetchStudents: (branch = '', semester = '') => {
    const params = new URLSearchParams();
    if (branch) params.append('branch', branch);
    if (semester) params.append('semester', semester);
    
    return fetch(`${API_BASE_URL}/students?${params.toString()}`)
      .then(response => response.json());
  },
  
  // PDF Reports
  downloadIndividualReport: (regNo, includeCharts = false, templateStyle = 'classic') => {
    const params = new URLSearchParams();
    params.append('includeCharts', includeCharts);
    params.append('templateStyle', templateStyle);
    
    return `${API_BASE_URL}/reports/individual/${regNo}?${params.toString()}`;
  },
  
  previewIndividualReport: (regNo, includeCharts = false, templateStyle = 'classic') => {
    const params = new URLSearchParams();
    params.append('includeCharts', includeCharts);
    params.append('templateStyle', templateStyle);
    
    return `${API_BASE_URL}/reports/preview/${regNo}?${params.toString()}`;
  },
  
  downloadBulkReport: ({ selected, reportType, pdfType = 'individual', includeCharts = false, templateStyle = 'classic', selected_columns = [] }) => {
    const params = new URLSearchParams();
    params.append('students', selected.join(','));
    
    if (reportType === 'pdf') {
      params.append('includeCharts', includeCharts);
      params.append('templateStyle', templateStyle);
      return `${API_BASE_URL}/reports/pdf/${pdfType}?${params.toString()}`;
    } else if (reportType === 'excel') {
      if (selected_columns.length > 0) {
        params.append('columns', selected_columns.join(','));
      }
      return `${API_BASE_URL}/reports/excel?${params.toString()}`;
    }
    
    return '';
  },
  
  // Dashboard data
  getDashboardStats: () => {
    return fetch(`${API_BASE_URL}/dashboard/stats`)
      .then(response => response.json());
  }
};