
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#121212',
        secondary: '#1A1A2E',
        text: '#FAFAFA',
        accent: '#FF2A6D',
        'accent-secondary': '#05D9E8',
      },
      fontFamily: {
        sans: ['Open Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
