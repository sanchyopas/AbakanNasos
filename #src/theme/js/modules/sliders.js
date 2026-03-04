import Swiper from "swiper";
import { Navigation, Pagination, Scrollbar, Thumbs, EffectFade, Zoom } from 'swiper/modules';


const heroSlider = new Swiper('.hero__slider', {
  modules: [Navigation, EffectFade],
  direction: 'horizontal',
  effect: 'fade',
  fade: {
    crossFade: true,
  },
  autoHeight: true,
  slidesPerView: 1,
  spaceBetween: 20,

  navigation: {
    nextEl: '.hero__arrow-next',
    prevEl: '.hero__arrow-prev',
  },
});

const clientsSlider = new Swiper('.clients__slider', {
  modules: [Navigation, Scrollbar],
  direction: 'horizontal',
  slidesPerView: 4.5,
  spaceBetween: 20,

  navigation: {
    nextEl: '',
    prevEl: '',
  },

  scrollbar: {
    el: '.swiper-scrollbar',
  },
});


document.addEventListener('DOMContentLoaded', () => {

  const infoSliderThumb = new Swiper('.info__slider-thumb', {
    slidesPerView: 3,
    breakpoints: {
      320: {
        slidesPerView: 3,
        direction: 'horizontal',
        spaceBetween: 10,
      },
      1200: {
        direction: 'vertical',
        slidesPerView: 3,
        spaceBetween: 10,
      }
    }
  });

  const infoSlider = new Swiper('.info__slider', {
    modules: [Scrollbar, Pagination, Thumbs, Zoom],
    direction: 'horizontal',
    spaceBetween: 20,
    slidesPerView: 1,

    thumbs: {
      swiper: infoSliderThumb,
    },
  });

});