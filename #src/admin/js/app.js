import("./modules/dropdownMenu.js");
import("./modules/uploadFileInput.js");
import("./modules/notice.js");
import ("./modules/mask.js");
import ("./modules/uploadImage.js");
import ("./modules/slugify.js");

/**
 * Переключение вкладок на страницах продуктов, категорий
 */


const tabButton = document.querySelectorAll('[data-name]');
const pageEditButton = document.querySelectorAll('.page-content');

tabButton?.forEach(btn => {
  btn.addEventListener('click', function (e) {
    tabButton.forEach(item => item.classList.remove('_active'));
    pageEditButton.forEach(item => item.classList.remove('_show'));

    let bodyTabBody = document.getElementById(this.dataset.name);

    btn.classList.add('_active');
    bodyTabBody.classList.add('_show');

    const newUrl = window.location.pathname + '?tab=' + this.dataset.name;
    window.history.pushState({}, '', newUrl);
  })

  const urlParams = new URLSearchParams(window.location.search);
  const activeTab = urlParams.get('tab');
  if (activeTab && btn.dataset.name === activeTab) {
    btn.click();
  }
})


/**
 * Подсчет и отображение количества символов в meta-полях
 */

const numberSymbols = {
  'title': 50,
  'description': 140
}

const metaFields = document.querySelectorAll('.meta_field');

metaFields?.forEach(item => {
  let parentItem = item.closest('.form__group').querySelector('.meta-length');
  if (item.value <= 0 && parentItem) {
    parentItem.innerText = 0;
  } else {
    parentItem.innerText = item.value.length;
  }

  item.addEventListener('input', (e) => {
    checkLengthSymbol(numberSymbols, e.currentTarget);
  })
})


function checkLengthSymbol(lengthSymbol, item) {
  item.previousElementSibling.innerText = item.value.length;
  if (item.value.length > numberSymbols.title) {
    item.previousElementSibling.classList.add("_red");
  }

  if (item.value.length > numberSymbols.description) {
    item.previousElementSibling.classList.add("_red");
  }
};


const addPropertyBtn = document.getElementById("add-property");
addPropertyBtn?.addEventListener("click", (e) => {
  const blockPasteChar = document.getElementById('paste-char');

  let newCharGroup = document.createElement("div");
  newCharGroup.classList.add("form__group-char");
  newCharGroup.innerHTML = `
      <label for="id_new_name" class="form__controls-label">Название характеристики <span>:</span></label>
      <input name="new_name" class="form__controls" id="id_new_name" value="">

      <label for="">Значение:</label>
      <input type="text" name="new_value" class="form__controls" required id="" />

      <button type="button" class="form__remove">Удалить</button>
  `;

  blockPasteChar.appendChild(newCharGroup)
})


document.querySelector('#myForm')?.addEventListener('change', function (event) {
  console.log('Изменение в:', event.target.name);
});

document.addEventListener('keydown', function (event) {
  if ((event.ctrlKey || event.metaKey) && event.key === 's') {
    event.preventDefault();

    const form = document.getElementById('myForm');
    console.log(form)
    form.submit();
  }
});

const charAddBtn = document.getElementById("char-add");

charAddBtn?.addEventListener("click", (e) => {
  e.preventDefault();

  const selectChar = document.getElementById("select-char"); // скрытый блок
  if (selectChar) {
    const charBody = document.getElementById('char__paste');

    const clone = selectChar.querySelector('.char-row').cloneNode(true);
    // назначаем name ТОЛЬКО клону
    const select = clone.querySelector("select");
    const input = clone.querySelector("input");

    select.setAttribute("name", "characteristic");
    input.setAttribute("name", `value_${select.value}`);
    input.setAttribute("required", "required");

    select.addEventListener("change", () => {
      input.setAttribute("name", `value_${select.value}`);
    });

    charBody.appendChild(clone);

    const charDeleteBtns = clone.querySelectorAll(".char-delete");

    charDeleteBtns?.forEach((item) => {

      item.addEventListener("click", () => {
        const parent = item.closest(".char-row");
        if (parent) {
          parent.remove();
        }
      });
    });

  }
});





