module.exports = {
  purge: {
    enabled: true,
    content: ['../templates/**/*.html']
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      welcome: ['lobster', 'cursive'],
      title: ['Crete Round', 'serif'],
      body: ['Lato', 'sans-serif']
    },
    backgroundSize: {
      'auto': 'auto',
      'cover': 'cover',
      'contain': 'contain',
      '50%': '50%',
      '40%': '40%',
    },
    extend: {
      backgroundImage: {
        'dog1': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog1_crop.jpg')",
        'dog2': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog2_crop.jpg')",
        'dog3': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog3.jpg')",
        'dog4': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog4_crop.jpg')",
        'dog5': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog5.jpg')",
        'dog6': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog6_up.jpg')",
        'dog7': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog7_crop.jpg')",
        'dog8': "url('https://res.cloudinary.com/cjcon90/image/upload/w_700,c_scale,q_auto,f_jpg/v1614203125/hot_dogz/wallpapers/dog8.jpg')",
      },
      minHeight: {
        "screen/2": "50vh",
        "screen-less-nav": "calc(calc(var(--vh, 1vh) * 100) - 4rem)",
        "screen-less-both-nav": "calc(calc(var(--vh, 1vh) * 100) - 8rem)"
      },
      maxHeight: {
        "screen/2": "50vh",
        "screen-less-nav": "calc(calc(var(--vh, 1vh) * 100) - 4rem)"
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
