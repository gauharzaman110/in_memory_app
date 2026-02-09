// frontend/src/services/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration and unauthorized access
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be expired, clear it and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    } else if (error.response?.status === 403) {
      // Unauthorized access - show error message to user
      alert('You are not authorized to access this resource');
    }
    return Promise.reject(error);
  }
);

export default api;

// Authentication API functions
export const authAPI = {
  login: (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    return api.post('/api/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  
  register: (email: string, password: string) => {
    return api.post('/api/auth/register', {
      email,
      password,
    });
  },
  
  logout: () => {
    return api.post('/api/auth/logout');
  },
  
  getSessionInfo: (token: string) => {
    return api.get('/api/auth/session');
  },
};

// Task API functions
export const taskAPI = {
  getTasks: () => {
    return api.get('/api/tasks');
  },
  
  createTask: (title: string, description?: string) => {
    return api.post('/api/tasks', {
      title,
      description,
    });
  },
  
  updateTask: (id: number, title?: string, description?: string, is_completed?: boolean) => {
    return api.put(`/api/tasks/${id}`, {
      title,
      description,
      is_completed,
    });
  },
  
  deleteTask: (id: number) => {
    return api.delete(`/api/tasks/${id}`);
  },
};