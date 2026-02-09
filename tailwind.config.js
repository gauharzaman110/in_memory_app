/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './src/**/*.{js,ts,jsx,tsx}', // Include src directory if components are there
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Add Inter font
      },
      colors: {
        primary: '#4F46E5', // A modern indigo
        'primary-dark': '#3730A3', // A slightly darker indigo for hover states
        secondary: '#6EE7B7', // A soft teal
        accent: '#FACC15', // A vibrant yellow
        neutral: '#F3F4F6', // Light gray for backgrounds
        'neutral-dark': '#1F2937', // Dark gray for text
      },
    },
  },
  plugins: [],
};