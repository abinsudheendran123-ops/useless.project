/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        minecraft: ["'Minecraft'", "'Courier New'", "monospace"],
      },
      colors: {
        minecraft: {
          stone: "#c6c6c6",
          dark: "#141110",
          yellow: "#ffff55",
          red: "#ff5555",
          green: "#55ff55",
          orange: "#ffaa00",
          darkred: "#aa0000",
          dred: "#8b0000",
        },
      },
    },
  },
  plugins: [],
};
