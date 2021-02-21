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
        turquoise: {
          '50':  '#edf9f9',
          '100': '#d2f7f4',
          '200': '#a2f1e8',
          '300': '#64e6da',
          '400': '#21d4c4',
          '500': '#0abba7',
          '600': '#099f8a',
          '700': '#158e87',
          '800': '#116458',
          '900': '#115147',
        },
        sunset: {
          '50': '#FDF7F7',
          '100': '#F8E5E5',
          '200': '#EFC0C0',
          '300': '#E59C9C',
          '400': '#DC7777',
          '500': '#D25353',
          '600': '#BC3131',
          '700': '#8F2525',
          '800': '#631A1A',
          '900': '#360E0E'
        },
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
