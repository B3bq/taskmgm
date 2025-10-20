// toggle menu script
const toggleMenuEl = document.getElementById('js-toggle-menu');
const toggleableMenuEl = document.getElementById('js-toggleable-menu');

toggleMenuEl?.addEventListener('click', function(){
    toggleableMenuEl?.classList.toggle('active');
})

window.addEventListener("scroll", () => {
    const header = document.getElementById('onTop');
    const triggerPoint = header.offsetTop + header.offsetHeight;
  
    if (window.scrollY > triggerPoint) {
      header.style.background = '#141414';
      header.style.boxShadow = '1px 2px 10px #5e5e5e';
    } else {
      header.style.background = '#242424';
      header.style.boxShadow = 'none';
    }
});

const userName = document.getElementById('userName');
const hiddenInput = document.getElementById('hiddenName');
const confirmBtn = document.getElementById('confirm');

confirmBtn.addEventListener("click", ()=>{
    hiddenInput.value = userName.innerText.trim();
})
