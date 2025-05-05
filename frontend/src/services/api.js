import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export const api = {

    
    fetchStudents: (filters = {}) => {
        const params = new URLSearchParams(filters).toString();
        return axios.get(`${API_BASE_URL}/students${params ? `?${params}` : ''}`);
    },


    generatePdfReport: async ({ selected_students, generation_type }) => {
        const response = await axios.post(
            `${API_BASE_URL}/generate-pdf-report`,
            { selected_students, generation_type },
            { responseType: 'blob' }
        );

        if (response.status !== 200) {
            let errMsg = 'Failed to download report';
            try {
                // Attempt to parse JSON error
                const text = await new Response(response.data).text();
                const json = JSON.parse(text);
                errMsg = json.error || errMsg;
            } catch (_) { }
            throw new Error(errMsg);
        }

        const disposition = response.headers['content-disposition'] || '';
        const match = disposition.match(/filename="?(.+)"?/);
        const filename = match
            ? match[1]
            : generation_type === 'combined'
                ? 'Combined_Student_Report.pdf'
                : 'Student_Reports.zip';

        // Trigger browser download
        const blob = new Blob([response.data]);
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);

        return true;
    },

    // Generate and download Excel report
    generateExcelReport: async ({ selected_students, selected_columns }) => {
        const response = await axios.post(
            `${API_BASE_URL}/generate-excel-report`,
            { selected_students, selected_columns },
            { responseType: 'blob' }
        );

        // Create a download link and trigger it
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'Student_Report.xlsx');
        document.body.appendChild(link);
        link.click();
        link.remove();
    },
    downloadIndividualReport: (regNo) =>
        `${API_BASE_URL}/download-pdf/${regNo}`
};
