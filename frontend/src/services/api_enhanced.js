// Enhanced API service for frontend with authentication and new features
import axios from 'axios';

const getApiBaseUrl = () => {
  // Get the hostname from the current URL
  const hostname = window.location.hostname;
  return `http://${hostname}:5000/api`;
};

const API_URL = getApiBaseUrl();

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
    config => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Add response interceptor to handle token refresh
apiClient.interceptors.response.use(
    response => {
        return response;
    },
    async error => {
        const originalRequest = error.config;
        
        // If error is 401 and not already retrying
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            
            try {
                // Try to refresh token
                const refreshToken = localStorage.getItem('refresh_token');
                if (!refreshToken) {
                    // No refresh token, redirect to login
                    window.location.href = '/login';
                    return Promise.reject(error);
                }
                
                const response = await axios.post(`${API_URL}/auth/refresh`, {}, {
                    headers: {
                        'Authorization': `Bearer ${refreshToken}`
                    }
                });
                
                // Get new token
                const { access_token } = response.data;
                
                // Update token in localStorage
                localStorage.setItem('access_token', access_token);
                
                // Update header and retry
                originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
                return axios(originalRequest);
            } catch (refreshError) {
                // Refresh failed, redirect to login
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }
        
        return Promise.reject(error);
    }
);

// Create API object with methods
const api = {
    // Student data
    fetchStudents: (branch = '', semester = '') => {
        const params = new URLSearchParams();
        if (branch) params.append('branch', branch);
        if (semester) params.append('semester', semester);
        
        return apiClient.get(`/students?${params.toString()}`)
            .then(response => response.data);
    },
    
    // Dashboard data
    getDashboardStats: () => {
        return apiClient.get('/dashboard/stats')
            .then(response => response.data);
    }
};

export { apiClient, API_URL, api };