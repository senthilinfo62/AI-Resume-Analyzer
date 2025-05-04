import api from './api';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: {
    id: number;
    username: string;
    email: string;
    firstName: string;
    lastName: string;
  };
}

const AuthService = {
  /**
   * Login a user
   * @param credentials User credentials
   * @returns Promise with auth response
   */
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    try {
      // In a real app, this would be a real API call
      // const response = await api.post('/auth/login', credentials);
      // return response.data;
      
      // Mock response for now
      return new Promise((resolve) => {
        setTimeout(() => {
          const mockResponse: AuthResponse = {
            token: 'mock-jwt-token',
            user: {
              id: 1,
              username: credentials.email.split('@')[0],
              email: credentials.email,
              firstName: 'John',
              lastName: 'Doe',
            },
          };
          
          // Store token in localStorage
          localStorage.setItem('token', mockResponse.token);
          localStorage.setItem('user', JSON.stringify(mockResponse.user));
          
          resolve(mockResponse);
        }, 1000);
      });
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Register a new user
   * @param data User registration data
   * @returns Promise with auth response
   */
  register: async (data: RegisterData): Promise<AuthResponse> => {
    try {
      // In a real app, this would be a real API call
      // const response = await api.post('/auth/register', data);
      // return response.data;
      
      // Mock response for now
      return new Promise((resolve) => {
        setTimeout(() => {
          const mockResponse: AuthResponse = {
            token: 'mock-jwt-token',
            user: {
              id: 1,
              username: data.email.split('@')[0],
              email: data.email,
              firstName: data.firstName,
              lastName: data.lastName,
            },
          };
          
          resolve(mockResponse);
        }, 1000);
      });
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Logout the current user
   */
  logout: (): void => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
  
  /**
   * Check if a user is authenticated
   * @returns Boolean indicating if user is authenticated
   */
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('token');
  },
  
  /**
   * Get the current user
   * @returns User object or null
   */
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      return JSON.parse(userStr);
    }
    return null;
  },
};

export default AuthService;
