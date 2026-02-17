import Swiper from "swiper";
import {Navigation, Pagination, Scrollbar, Thumbs, EffectFade} from "swiper/modules";


const heroSlider = new Swiper('.hero__slider', {
  modules: [Navigation],
  direction: 'horizontal',
  autoHeight: true,
  slidesPerView: 1,
  spaceBetween: 20,

  navigation: {
    nextEl: '.hero__arrow-next',
    prevEl: '.hero__arrow-prev',
  },
});