document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.header');
  if (!header) return;

  const headerOffsetTop = header.offsetTop;
  let isSticky = false;

  const onScroll = () => {
    if (window.scrollY > headerOffsetTop && !isSticky) {
      header.classList.add('sticky');
      const headerHeight = header.offsetHeight; // уже после фиксации
      document.body.style.paddingTop = `${headerHeight}px`;
      isSticky = true;
    } else if (window.scrollY <= headerOffsetTop && isSticky) {
      header.classList.remove('sticky');
      document.body.style.paddingTop = '';
      isSticky = false;
    }
  };

  window.addEventListener('scroll', onScroll);
  window.addEventListener('resize', () => {
    document.body.style.paddingTop = '';
    header.classList.remove('sticky');
    isSticky = false;
  });
});
