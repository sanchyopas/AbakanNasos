import Swiper from "swiper";
import {Navigation, Pagination, Scrollbar, Thumbs, EffectFade} from "swiper/modules";


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

const thumbEl = document.querySelector('.info__slider-thumb');
const mainEl = document.querySelector('.info__slider');

let infoSliderThumb = null;

if (thumbEl) {
  infoSliderThumb = new Swiper(thumbEl, {
    spaceBetween: 10,
    slidesPerView: 3,
    watchSlidesProgress: true,
    breakpoints: {
      320: {
        direction: 'horizontal',
      },
      1200: {
        direction: 'vertical',
      }
    }
  });
}

if (mainEl) {
  new Swiper(mainEl, {
    loop: false,
    spaceBetween: 20,
    slidesPerView: 1,
    thumbs: infoSliderThumb
      ? { swiper: infoSliderThumb }
      : undefined,
  });
}