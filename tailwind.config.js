/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh",
      },
      minHeight: {
        "50vh" : "50vh",
        "65vh" : "65vh",
        "75vh" : "75vh"
      }
    },
  },
  plugins: [],
  variants: {
    extend: {
      backgroundColor: ['even','odd'],
    }
  },
}
