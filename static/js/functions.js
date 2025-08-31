let defaultValue = '';
//chnage name
function enableEditing(){
    const userName =  document.getElementById('userName');
    defaultValue = userName.innerText.trim();
    userName.contentEditable = true;
    userName.focus();
    document.getElementById('buttons').style.visibility = 'visible';
    document.getElementById('edit').hidden = true;
}

function resetValue(){
    document.getElementById('userName').innerText = defaultValue;
    document.getElementById('buttons').style.visibility = 'hidden';
    document.getElementById('edit').hidden = false;
}