import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default settings
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000, // 10 second timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: false // Set to true if using cookies/sessions
});

// Add request interceptor for logging
apiClient.interceptors.request.use(config => {
  console.log('Sending request to:', config.url);
  return config;
}, error => {
  console.error('Request error:', error);
  return Promise.reject(error);
});

// Add response interceptor
apiClient.interceptors.response.use(response => {
  console.log('Received response from:', response.config.url);
  return response;
}, error => {
  if (error.response) {
    // Server responded with a status code outside 2xx
    console.error('API Error Response:', {
      status: error.response.status,
      data: error.response.data,
      headers: error.response.headers
    });
  } else if (error.request) {
    // Request was made but no response received
    console.error('API No Response:', error.request);
  } else {
    // Something happened in setting up the request
    console.error('API Setup Error:', error.message);
  }
  
  return Promise.reject(error);
});

const apiMethods = {
  analyzeSong: async (songData) => {
    try {
      const response = await apiClient.post('/analyze', songData);
      return response.data;
    } catch (error) {
      // Enhanced error handling
      const apiError = new Error(error.response?.data?.message || 'Analysis failed');
      apiError.status = error.response?.status;
      apiError.details = error.response?.data?.errors;
      throw apiError;
    }
  },
  
  getSavedAnalyses: async () => {
    try {
      const response = await apiClient.get('/analyses');
      return response.data;
    } catch (error) {
      const apiError = new Error(error.response?.data?.message || 'Failed to fetch analyses');
      apiError.status = error.response?.status;
      throw apiError;
    }
  },
  
  // Health check endpoint
  checkAPIHealth: async () => {
    try {
      await apiClient.get('/health');
      return true;
    } catch {
      return false;
    }
  }
};

// Optional: Add a method to verify CORS is working
apiMethods.testCORS = async () => {
  try {
    const response = await fetch(`${API_URL}/analyses`, {
      method: 'OPTIONS'
    });
    console.log('CORS Headers:', {
      allowOrigin: response.headers.get('Access-Control-Allow-Origin'),
      allowMethods: response.headers.get('Access-Control-Allow-Methods'),
      allowHeaders: response.headers.get('Access-Control-Allow-Headers')
    });
    return response.ok;
  } catch (error) {
    console.error('CORS Test Failed:', error);
    return false;
  }
};

export default apiMethods;