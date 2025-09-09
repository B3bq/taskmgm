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

function takeCode(){
    const code = document.querySelectorAll('.code');
    const response = document.getElementById('response');

    let userCode = '';
    code.forEach(e=>{
        userCode += e.value;
    });

    fetch("/verification", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ userCode: userCode }),
    }).then(res => res.json())
      .then(data=>{
        if(!data.success){
            response.innerHTML = data.error;
            response.hidden = false;
        }else{
            window.location.href = data.redirect;
        }
      })
}