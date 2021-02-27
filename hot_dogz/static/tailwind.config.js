module.exports = {
  purge: {
    enabled: false,
    content: ['../templates/**/*.html']
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      title: ['Lobster', 'cursive']
    },
    extend: {
      backgroundImage: {
        'dog1': "url('https://res.cloudinary.com/cjcon90/image/upload/v1614203125/hot_dogz/wallpapers/dog1.jpg')",
        'dog5': "url('https://res.cloudinary.com/cjcon90/image/upload/v1614203125/hot_dogz/wallpapers/dog5.jpg')",
       },
      minHeight: {
        "screen/2": "50vh"
      },
      screens: {
        'landscape': {'raw': '(orientation: landscape)'},
      },
      colors: {
        primary: {
          '50': '#FEFAFA',
          '100': '#F8E7E6',
          '200': '#ECC0BF',
          '300': '#E09998',
          '400': '#D57270',
          '500': '#C94B49',
          '600': '#AC3533',
          '700': '#852927',
          '800': '#5D1D1C',
          '900': '#361110'
        },
        secondary: {
          '50': '#9DE6DD',
          '100': '#88E1D6',
          '200': '#60D6C8',
          '300': '#37CCBA',
          '400': '#2AA697',
          '500': '#207D72',
          '600': '#16544D',
          '700': '#0B2C28',
          '800': '#010303',
          '900': '#000000'
        },
        tertiary: {
          '50': '#F3FAF0',
          '100': '#E5F5DF',
          '200': '#CAEABC',
          '300': '#AEDF99',
          '400': '#93D476',
          '500': '#77C953',
          '600': '#5DB138',
          '700': '#488B2B',
          '800': '#34641F',
          '900': '#203D13'
        }
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
