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

