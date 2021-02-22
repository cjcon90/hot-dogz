module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      title: ['Lobster', 'cursive']
    },
    extend: {
      height: theme => ({
        "screen/2": "50vh",
        "screen-less-nav": 'calc(100vh - 5rem)'
      }),
      screens: {
        'landscape': {'raw': '(orientation: landscape)'},
      },
      colors: {
        primary: {
          '50': '#FDF8F8',
          '100': '#F8E6E5',
          '200': '#EFC2C1',
          '300': '#E59E9D',
          '400': '#DC7B78',
          '500': '#D25754',
          '600': '#C03633',
          '700': '#982B28',
          '800': '#701F1D',
          '900': '#471413'
        },
        secondary: {
          '50': '#F8FAFD',
          '100': '#E5EEF8',
          '200': '#C1D7EF',
          '300': '#9DC0E5',
          '400': '#78A8DC',
          '500': '#5491D2',
          '600': '#3377C0',
          '700': '#285E98',
          '800': '#1D4570',
          '900': '#132C47'
        },
        tertiary: {
          '50': '#F8FDFA',
          '100': '#E5F8EF',
          '200': '#C1EFD9',
          '300': '#9DE5C2',
          '400': '#78DCAC',
          '500': '#54D295',
          '600': '#33C07C',
          '700': '#289862',
          '800': '#1D7048',
          '900': '#13472E'
        }
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
