/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./SportsArbitrageApp.jsx",
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          750: '#334155',
        },
      },
    },
  },
  plugins: [],
}

