import("./modules/dorpdownMenu.js");
import("./modules/generateSlug.js");
import("./modules/uploadFileInput.js");

/**
 * Переключение вкладок на страницах продуктов, категорий
 */

const pageEditButton1 = document.querySelectorAll('.page-content');
const tabButton1 = document.querySelectorAll('[data-tab]');
tabButton1?.forEach(btn => {
  btn.addEventListener('click', function (e) {
    tabButton1.forEach(item => item.classList.remove('_active'));
    pageEditButton1.forEach(item => item.classList.remove('_show'));


    let bodyTabBody = document.getElementById(this.dataset.tab);

    btn.classList.add('_active');
    bodyTabBody.classList.add('_show');
  })
})

const tabButton = document.querySelectorAll('[data-name]');
const pageEditButton = document.querySelectorAll('.tab-content');

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
  if(activeTab && btn.dataset.name === activeTab) {
    btn.click();
  }
})

document.addEventListener('DOMContentLoaded', () => {
  const newUrl = window.location.pathname + '?tab=' + this.dataset.name;
  window.history.pushState({}, '', newUrl);
})






// const ctx = document.getElementById('myChart');

// const no_register = document.getElementById('no_register');
// if(no_register){

// }

var ctx = document.getElementById('myChart');
if (ctx) {
  ctx.getContext('2d');
  var salesChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'],
      datasets: [
        {
          label: 'Зарегистрировались и купили',
          data: [12, 19, 3, 5, 2, 3, 8, 12, 13, 14, 5, 9, 11, 6, 8, 10, 15, 18, 16, 10, 12, 17, 19, 21, 20, 18, 16, 14, 12, 10],
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderWidth: 1
        },
        {
          label: 'Не зарегистрировались',
          data: [10, 15, 6, 8, 5, 4, 7, 9, 11, 12, 6, 8, 10, 9, 7, 5, 12, 14, 13, 9, 10, 13, 15, 16, 14, 13, 11, 9, 8, 7],
          borderColor: 'rgba(153, 102, 255, 1)',
          backgroundColor: 'rgba(153, 102, 255, 0.2)',
          borderWidth: 1
        }
      ]
    },
    options: {
      scales: {
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Дни месяца'
          }
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Количество продаж'
          }
        }
      }
    }
  });
}


/**
 * Подсчет и отображение количества символов в meta-полях
 */

const numberSymbols = {
  'title': 50,
  'description': 140
}

const metaFields = document.querySelectorAll('.meta_field');

metaFields?.forEach(item => {
  let parentItem = item.closest('.form__group').querySelector('.meta-lenght');
  if (item.value <= 0 && parentItem) {
    parentItem.innerText = 0;
  } else {
    parentItem.innerText = item.value.length;
  }

  item.addEventListener('input', (e) => {
    checkLengthSymbol(numberSymbols, e.currentTarget);
  })
})

// document.querySelector('.product-block__plus').addEventListener('click', function (event) {
//   var image = '<div class="form__group  form__group-image"><input type="file" multiple="multiple" name="src" accept="image/*" required="" id="id_src"><div class="product-block__minus form__remove">Удалить</div></div>';
//   document.querySelector('.product-field').insertAdjacentHTML('beforeend', image);
// })


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


