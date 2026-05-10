/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#010A13",
        line: "#ded4c3",
        brand: "#497683",
        accent: "#8AB0A5",
        cream: "#F5E9D4",
        muted: "#82797A",
        mint: "#e4efeb"
      },
      boxShadow: {
        panel: "0 18px 50px rgba(1, 10, 19, 0.08)",
        soft: "0 8px 24px rgba(1, 10, 19, 0.06)"
      }
    }
  },
  plugins: []
};
