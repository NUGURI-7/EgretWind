// tailwind.config.js
import PrimeUI from 'tailwindcss-primeui'

export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: ['selector', '[class="p-dark"]'],
  theme: {
    extend: {
      colors: {
        'app-bg': '#faf8f4',
      },
    },
  },
  plugins: [PrimeUI],
}
