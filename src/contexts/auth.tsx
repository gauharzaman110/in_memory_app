import React, { createContext, useContext, useReducer, ReactNode, useEffect } from 'react';
import { authAPI } from '../services/api'; // Assuming api.ts exports authAPI

interface User {
  id: number; // Changed to number as per backend model
  email: string;
  is_active?: boolean; // Optional, as not always returned by all endpoints
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null; // Add error field to state
}

interface AuthAction {
  type: string;
  payload?: any;
}

interface AuthContextType {
  state: AuthState;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuthStatus: () => Promise<void>; // Make it async
}

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, isLoading: true, error: null };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'LOGIN_FAILURE':
      return { ...state, isLoading: false, error: action.payload.error };
    case 'LOGOUT':
      return { ...initialState, isLoading: false };
    case 'SET_AUTH_STATUS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: !!action.payload.token,
        isLoading: false,
        error: null,
      };
    default:
      return state;
  }
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const loginResponse = await authAPI.login(email, password);
      const { access_token, user } = loginResponse.data;
      localStorage.setItem('token', access_token);
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: { user, token: access_token },
      });
    } catch (loginError: any) {
      if (loginError.response?.status === 404 && loginError.response?.data?.detail === "User not found") {
        // If user not found, attempt to register
        try {
          const registerResponse = await authAPI.register(email, password);
          const { access_token, user } = registerResponse.data;
          localStorage.setItem('token', access_token);
          dispatch({
            type: 'LOGIN_SUCCESS',
            payload: { user, token: access_token },
          });
        } catch (registerError: any) {
          const errorMessage = registerError.response?.data?.detail || 'Registration failed';
          dispatch({ type: 'LOGIN_FAILURE', payload: { error: errorMessage } });
          throw new Error(errorMessage);
        }
      } else {
        // Handle other login errors (e.g., incorrect password)
        const errorMessage = loginError.response?.data?.detail || 'Login failed';
        dispatch({ type: 'LOGIN_FAILURE', payload: { error: errorMessage } });
        throw new Error(errorMessage);
      }
    }
  };

  const register = async (email: string, password: string) => {
    dispatch({ type: 'LOGIN_START' });
    try {
      const response = await authAPI.register(email, password);
      const { access_token, user } = response.data;
      localStorage.setItem('token', access_token);
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: { user, token: access_token },
      });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Registration failed';
      dispatch({ type: 'LOGIN_FAILURE', payload: { error: errorMessage } });
      throw new Error(errorMessage);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    dispatch({ type: 'LOGOUT' });
  };

  const checkAuthStatus = async () => {
    dispatch({ type: 'LOGIN_START' }); // Set loading state while checking
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await authAPI.getSessionInfo(token); // Assuming a getSessionInfo in authAPI
        dispatch({
          type: 'SET_AUTH_STATUS',
          payload: { user: response.data.user, token },
        });
      } catch (error) {
        console.error('Failed to verify token or fetch user session:', error);
        localStorage.removeItem('token');
        dispatch({
          type: 'SET_AUTH_STATUS',
          payload: { user: null, token: null },
        });
      }
    } else {
      dispatch({
        type: 'SET_AUTH_STATUS',
        payload: { user: null, token: null },
      });
    }
  };

  return (
    <AuthContext.Provider value={{ state, login, register, logout, checkAuthStatus }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};