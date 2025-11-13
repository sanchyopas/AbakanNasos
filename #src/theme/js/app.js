import * as functions from './modules/functions.js';

functions.isWebp();

import Swiper from "swiper";
import {Navigation, Pagination, Scrollbar, Thumbs, EffectFade} from "swiper/modules";

const heroSlider = new Swiper('.hero__slider', {
    modules: [Navigation, Scrollbar, EffectFade],
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

    scrollbar: {
        el: '.swiper-scrollbar',
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

const infoSliderThumb = new Swiper('.info__slider-thumb', {

    direction: 'vertical',
    loop: false,
    autoHeight: true,
    spaceBetween: 10,
    slidesPerView: 3,

    // scrollbar: {
    //   el: '.swiper-scrollbar',
    //   draggable: true,
    // },

    // breakpoints: {
    //   320: {
    //     scrollbar: {
    //       enabled: true
    //     },
    //     slidesPerView: 1,
    //   },
    //   992: {
    //     slidesPerView: 3,
    //     scrollbar: {
    //       enabled: false
    //     },
    //   }
    // }

});

const infoSlider = new Swiper('.info__slider', {
    modules: {Scrollbar, Pagination, Thumbs},
    direction: 'horizontal',
    loop: false,
    autoHeight: true,
    spaceBetween: 20,
    slidesPerView: 1,

    pagination: {
        nextEl: '.project__slider-next',
        prevEl: '.project__slider-prev',
    },

    scrollbar: {
        el: '.swiper-scrollbar',
        draggable: true,
    },

    thumbs: {
        swiper: infoSliderThumb,
    },

    // breakpoints: {
    //   320: {
    //     scrollbar: {
    //       enabled: true
    //     },
    //     slidesPerView: 1,
    //   },
    //   992: {
    //     slidesPerView: 3,
    //     scrollbar: {
    //       enabled: false
    //     },
    //   }
    // }

});

const inputSearch = document.querySelector('.form-search__input');

inputSearch?.addEventListener('focus', (e) => {
    inputSearch.parentElement.classList.add('focused');
});

inputSearch?.addEventListener('blur', (e) => {
    inputSearch.parentElement.classList.remove('focused');
});
