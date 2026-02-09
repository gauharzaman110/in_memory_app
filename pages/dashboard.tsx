// frontend/src/pages/dashboard.tsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../src/contexts/auth';
import { useRouter } from 'next/router';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import { taskAPI } from '../src/services/api';

const DashboardPage: React.FC = () => {
  const { state, logout } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await taskAPI.getTasks();
      setTasks(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask: any) => {
    setTasks([...tasks, newTask]);
  };

  const handleTaskUpdated = (updatedTask: any) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId: number) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral">
        <div className="flex items-center space-x-2 text-primary">
          <div className="w-8 h-8 border-4 border-t-4 border-primary border-opacity-20 rounded-full animate-spin"></div>
          <p className="text-lg font-medium text-neutral-dark">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral font-sans">
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-neutral-dark">Todo Dashboard</h1>
            </div>
            <div className="flex items-center">
              <span className="text-neutral-dark mr-4">Welcome, {state.user?.email}</span>
              <button
                onClick={handleLogout}
                className="ml-4 px-3 py-2 rounded-md text-sm font-medium text-white bg-primary hover:bg-primary-dark transition-colors duration-300"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <TaskForm onTaskCreated={handleTaskCreated} />
            <TaskList
              tasks={tasks}
              onTaskUpdated={handleTaskUpdated}
              onTaskDeleted={handleTaskDeleted}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;