// toggle menu script
const toggleMenuEl = document.getElementById('js-toggle-menu');
const toggleableMenuEl = document.getElementById('js-toggleable-menu');

toggleMenuEl?.addEventListener('click', function(){
    toggleableMenuEl?.classList.toggle('active');
})

const checkBoxes = document.querySelectorAll('input[type="checkbox"][name="option"]');
const dateOnce = document.getElementById('dateonce');
const dateRnage = document.getElementById('daterange');


checkBoxes.forEach(cb =>{
    cb.addEventListener('change', () => {
        if(cb.checked){
            checkBoxes.forEach(other => {
                if(other !== cb) other.checked = false;
            })
        }
        
        dateOnce.disabled = !document.getElementById('once').checked;
        dateRnage.disabled = !document.getElementById('range').checked;
        if (!daysCheckbox.checked){
            week.classList.remove("active");
        };
    })
})

const daysCheckbox = document.getElementById("days");
const week = document.getElementById("week");
const buttons = week.querySelectorAll("button");

daysCheckbox.addEventListener("change", () => {
    if (daysCheckbox.checked) {
        week.classList.add("active");
    } else {
        week.classList.remove("active");
        buttons.forEach(btn => btn.classList.remove("selected")); 
    }
});

const selected = new Set();
document.querySelectorAll('#week button').forEach(btn=>{
    btn.addEventListener('click', ()=>{
        const day = btn.dataset.day;
        if (selected.has(day)){
            selected.delete(day);
            btn.classList.remove('selected');
        } else {
            selected.add(day);
            btn.classList.add('selected');
        }
        document.getElementById('daysInput').value = Array.from(selected).join(',');
    })
})

const quest = document.getElementById("quest");
const quest_name = document.getElementById("quest_name");
const quest_btn = document.getElementById("quest_btn");

quest.addEventListener("change", ()=>{
    quest_name.disabled ? quest_name.disabled = false : quest_name.disabled = true;
    quest_btn.disabled ? quest_btn.disabled = false : quest_btn.disabled = true;
})

const userName = document.getElementById('userName');
const hiddenInput = document.getElementById('hiddenName');
const confirmBtn = document.getElementById('confirm');

confirmBtn.addEventListener("click", ()=>{
    hiddenInput.value = userName.innerText.trim();
})
