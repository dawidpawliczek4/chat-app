/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx,vue}"],
  theme: {
    extend: {
      colors: {
        bar: "rgb(30, 31, 34)",
        secondaryBar: "rgb(43,45,49)",
        background: "rgb(49, 51, 56)",
      },
    },
  },
  plugins: [],
};
