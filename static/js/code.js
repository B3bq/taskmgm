const inputs = document.querySelectorAll(".code");

inputs.forEach((input, index)=>{
    input.addEventListener("input", ()=>{
        if(input.value.length === 1 && index < inputs.length -1){
            inputs[index+1].focus();
        }
    });

    input.addEventListener("keydown",(e)=>{
        if(e.key === "Backspace" && input.value === "" && index > 0){
            inputs[index-1].focus()
        }
    });

    input.addEventListener("paste", (e) => {
        e.preventDefault();
        const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 4);
        pasted.split("").forEach((char, i) => {
          if (inputs[i]) {
            inputs[i].value = char;
          }
        });
        if (inputs[pasted.length - 1]) {
          inputs[pasted.length - 1].focus();
        }
      });
});