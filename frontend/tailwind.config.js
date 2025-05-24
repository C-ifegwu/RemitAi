/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fff9db',
          100: '#fff3b0',
          200: '#ffec85',
          300: '#ffe65a',
          400: '#ffdf2f',
          500: '#ffd60a', // Primary yellow
          600: '#e6c000',
          700: '#b39500',
          800: '#806a00',
          900: '#4d4000',
        },
        secondary: {
          50: '#e6f7ec',
          100: '#c3ecd4',
          200: '#9fe0ba',
          300: '#7bd4a0',
          400: '#57c886',
          500: '#34bd6c', // Secondary green
          600: '#2e9d5c',
          700: '#287c4b',
          800: '#225c3a',
          900: '#1c3c29',
        },
        neutral: {
          50: '#f8f9fa',
          100: '#f1f3f5',
          200: '#e9ecef',
          300: '#dee2e6',
          400: '#ced4da',
          500: '#adb5bd',
          600: '#868e96',
          700: '#495057',
          800: '#343a40',
          900: '#212529',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
      },
      boxShadow: {
        'card': '0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03)',
        'button': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      },
    },
  },
  plugins: [],
}
