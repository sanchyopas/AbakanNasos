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

    console.log(btn)

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


document.querySelector('#myForm')?.addEventListener('change', function(event) {
  console.log('Изменение в:', event.target.name);
});

document.addEventListener('keydown', function(event) {
  if ((event.ctrlKey || event.metaKey) && event.key === 's') {
    event.preventDefault();

    const form = document.getElementById('myForm');
    console.log(form)
    form.submit();
  }
});

const charAddBtn = document.getElementById("char-add");

charAddBtn?.addEventListener("click", (e) => {
  const charBody = document.getElementById('char-body');

  const html = `
    <div class="char-block">
    <input type="hidden" name="characteristics-4-id" value="" id="id_characteristics-4-id">  <!-- важно для редактирования -->
    <p><label for="id_characteristics-4-characteristic">Characteristic:</label> 
    <select name="characteristics-4-characteristic" id="id_characteristics-4-characteristic">
      <option value="" selected>---------</option>
    
      <option value="1">Мощность, кВт</option>
    
      <option value="2">Напряжение, В</option>
    
      <option value="3">Подача</option>
    
      <option value="4">Напор</option>
    
      <option value="5">Подключение</option>
    
      <option value="6">Максимальная глубина всасывания (м)</option>
    
      <option value="7">Напряжение</option>
    
      <option value="8">Наличие</option>
    
      <option value="9">Мощность</option>
    
      <option value="10">Монтажная длина (мм)</option>
    
      <option value="11">Максимальная глубина всасывания</option>
    
      <option value="12">Unnamed: 13</option>
    
      <option value="13">Unnamed: 14</option>
    
      <option value="14">Unnamed: 15</option>
    
      <option value="15">Unnamed: 16</option>
    
      <option value="16">Unnamed: 17</option>
    
      <option value="17">Unnamed: 18</option>
    
      <option value="18">Unnamed: 19</option>
    
      <option value="19">Unnamed: 20</option>
    
      <option value="20">Unnamed: 21</option>
    
      <option value="21">Unnamed: 22</option>
    
      <option value="22">Unnamed: 23</option>
    
      <option value="23">Unnamed: 24</option>
    </select>
</p>
  <p><label for="id_characteristics-4-value">Value:</label> <input type="text" name="characteristics-4-value" value="3/4&quot; (дюйм)" maxlength="250" id="id_characteristics-4-value"></p>
<p><label for="id_characteristics-4-DELETE">Удалить:</label> <input type="checkbox" name="characteristics-4-DELETE" id="id_characteristics-4-DELETE"><input type="hidden" name="characteristics-4-id" value="1158" id="id_characteristics-4-id"><input type="hidden" name="characteristics-4-model" value="192" id="id_characteristics-4-model"></p>
  </div>
  `

  charBody.insertAdjacentHTML('afterend', html)
})

