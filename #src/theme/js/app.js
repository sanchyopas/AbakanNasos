import * as functions from './modules/functions.js';
// import { Fancybox } from "@fancyapps/ui/dist/fancybox/";

functions.isWebp();

import "./modules/sliders.js";
import "./modules/menu/mobileMenu.js";
import "./modules/popup/popup.js";
import "./modules/normalizeFormatPhoneLink.js";
import "./modules/font-awesome.js";


//
// Fancybox.bind("[data-fancybox]", {
//
// });

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

const modelName = document.querySelectorAll('.model-name')

modelName?.forEach((el) => {
  const text = el.innerText.trim()

  // Проверяем, начинается ли строка с ENSI или ensi (без учёта регистра)
  if (!/^ensi\b/i.test(text)) {
    el.innerText = `ENSI ${text}`
  }
})