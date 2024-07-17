/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
    "node_modules/flowbite-vue/**/*.{js,jsx,ts,tsx,vue}",
    "node_modules/flowbite/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bar: "rgb(30, 31, 34)",
        secondaryBar: "rgb(43,45,49)",
        background: "rgb(49, 51, 56)",
      },
    },
  },
  plugins: [require("flowbite/plugin")],
  darkMode: "class",
};
