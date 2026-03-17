import * as functions from './modules/functions.js';

functions.isWebp();

import "./modules/sliders.js";
import "./modules/callBackForm.js";
import "./modules/mask.js";
import "./modules/menu/mobileMenu.js";
import "./modules/popup/popup.js";
import "./modules/normalizeFormatPhoneLink.js";
import "./modules/font-awesome.js";
import "./modules/notice.js";
import "./modules/stickyMenu.js";
import {Fancybox} from "@fancyapps/ui"

Fancybox.bind("[data-fancybox]", {
  theme: "light",
});

const socialBtn = document.querySelector('.social__mobile-btn');
socialBtn?.addEventListener('click', (e) => {
  e.currentTarget.classList.toggle('active');
  document.querySelector('.social__mobile-cnt').classList.toggle('active');
})


const inputSearch = document.querySelector('.form-search__input');

inputSearch?.addEventListener('focus', (e) => {
    inputSearch.parentElement.classList.add('focused');
});

inputSearch?.addEventListener('blur', (e) => {
    inputSearch.parentElement.classList.remove('focused');
});


document.querySelectorAll('.accordion__title')?.forEach(title => {
  title.addEventListener('click', () => {
    const item = title.parentElement;
    const body = title.nextElementSibling;

    if (item.classList.contains('active')) {
      body.style.maxHeight = body.scrollHeight + 'px';
      requestAnimationFrame(() => body.style.maxHeight = '0');
      item.classList.remove('active');
    } else {
      // закрываем все остальные
      document.querySelectorAll('.accordion__item').forEach(i => {
        i.classList.remove('active');
        i.querySelector('.accordion__body').style.maxHeight = '0';
      });

      item.classList.add('active');
      body.style.maxHeight = body.scrollHeight + 'px';
    }
  });
});
