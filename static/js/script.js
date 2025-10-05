// toggle menu script
const toggleMenuEl = document.getElementById('js-toggle-menu');
const toggleableMenuEl = document.getElementById('js-toggleable-menu');

toggleMenuEl?.addEventListener('click', function(){
    toggleableMenuEl?.classList.toggle('active');
})

const userName = document.getElementById('userName');
const hiddenInput = document.getElementById('hiddenName');
const confirmBtn = document.getElementById('confirm');

confirmBtn.addEventListener("click", ()=>{
    hiddenInput.value = userName.innerText.trim();
})