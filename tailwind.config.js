/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "neon-blue": "#00e6ff",
        "neon-cyan": "#00f2ff",
        "dark-bg": "#050510",
        "dark-surface": "#0a0a1a",
        "dark-accent": "#101025",
        "neon-purple": "#8a2be2"
      },
    },
  },
  plugins: [],
}
