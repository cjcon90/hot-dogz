module.exports = {
  purge: {
    enabled: false,
    content: ['../templates/**/*.html']
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      welcome: ['lobster', 'cursive'],
      title: ['Crete Round', 'serif'],
      body: ['Lato', 'sans-serif']
    },
    extend: {
      backgroundImage: {
        'dog1': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog1_crop.jpg')",
        'dog2': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog2_crop.jpg')",
        'dog3': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog3.jpg')",
        'dog4': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog4_crop.jpg')",
        'dog5': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog5.jpg')",
        'dog6': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog6_up.jpg')",
       },
      minHeight: {
        "screen/2": "50vh",
        "screen-less-nav": "calc(100vh - 4rem)",
        "screen-less-both-nav": "calc(100vh - 120px)"
      },
      maxHeight: {
        "screen/2": "50vh",
        "screen-less-nav": "calc(100vh - 4rem)"
      },
      width: {
        "screen/2": "calc(100vw / 2)",
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
    extend: {
      // Add font style to focus variant for text change on Gallery screen
      fontStyle: ['hover', 'focus'],
      opacity: ['disabled']
    },
  },
  plugins: [],
}
