// frontend/src/contexts/task.tsx
import React, { createContext, useContext, useReducer, ReactNode } from 'react';

interface Task {
  id: number;
  title: string;
  description: string;
  is_completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskState {
  tasks: Task[];
  loading: boolean;
}

interface TaskAction {
  type: string;
  payload?: any;
}

interface TaskContextType {
  state: TaskState;
  addTask: (task: Task) => void;
  updateTask: (task: Task) => void;
  deleteTask: (id: number) => void;
  fetchTasks: () => void;
}

const initialState: TaskState = {
  tasks: [],
  loading: false,
};

const TaskContext = createContext<TaskContextType | undefined>(undefined);

const taskReducer = (state: TaskState, action: TaskAction): TaskState => {
  switch (action.type) {
    case 'SET_TASKS':
      return { ...state, tasks: action.payload, loading: false };
    case 'ADD_TASK':
      return { ...state, tasks: [...state.tasks, action.payload] };
    case 'UPDATE_TASK':
      return {
        ...state,
        tasks: state.tasks.map(task =>
          task.id === action.payload.id ? action.payload : task
        ),
      };
    case 'DELETE_TASK':
      return {
        ...state,
        tasks: state.tasks.filter(task => task.id !== action.payload),
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    default:
      return state;
  }
};

export const TaskProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(taskReducer, initialState);

  const addTask = (task: Task) => {
    dispatch({ type: 'ADD_TASK', payload: task });
  };

  const updateTask = (task: Task) => {
    dispatch({ type: 'UPDATE_TASK', payload: task });
  };

  const deleteTask = (id: number) => {
    dispatch({ type: 'DELETE_TASK', payload: id });
  };

  const fetchTasks = () => {
    // This would typically fetch tasks from the API
    // For now, we'll just set loading to false
    dispatch({ type: 'SET_LOADING', payload: false });
  };

  return (
    <TaskContext.Provider
      value={{ state, addTask, updateTask, deleteTask, fetchTasks }}
    >
      {children}
    </TaskContext.Provider>
  );
};

export const useTask = () => {
  const context = useContext(TaskContext);
  if (context === undefined) {
    throw new Error('useTask must be used within a TaskProvider');
  }
  return context;
};