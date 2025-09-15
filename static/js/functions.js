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

function inputEdit(input, btns, edit){
    input = document.getElementById(input);
    const buttons = document.getElementById(btns);
    const pen = document.getElementById(edit);
    if(input.name == "mail"){
        defaultValue = input.value;
        input.disabled = false;
        buttons.style.visibility = 'visible';
        pen.hidden = true;
    }else{
        input.disabled = false;
        input.value = '';
        input.type = "text";
        document.getElementById('repass').hidden = false;
        document.getElementById('repass').type = 'text';
        buttons.style.visibility = 'visible';
        pen.hidden = true;
    }
}

function defaultInput(input, btns, edit){
    input = document.getElementById(input);
    const buttons = document.getElementById(btns);
    const pen = document.getElementById(edit);
    if(input.name == "mail"){
        input.value = defaultValue;
        input.disabled = true;
        buttons.style.visibility = "hidden";
        pen.hidden = false;
    }else{
        input.disabled = true;
        input.type = "password";
        document.getElementById('repass').value = '';
        document.getElementById('repass').hidden = true;
        buttons.style.visibility = "hidden";
        pen.hidden = false;
    }
}

// taking verifiction code
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

// showing password
let isShowing = true;

function showPass(input){
    const pass = document.getElementById(input);
    const where = pass.getAttribute('where');

    if(where == "index"){
        if(isShowing){
            pass.type = 'text';
        }else{
            pass.type = 'password';
        }
    }else{
        if(isShowing){
            pass.type = 'text';
            document.getElementById('repass').type = 'text';
        }else{
            pass.type = 'password';
            document.getElementById('repass').type = 'password';
        }
    }
    isShowing = !isShowing;
}