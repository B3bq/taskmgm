

let lists = document.getElementsByClassName('task__list');
let ongoing = document.getElementById('ongoing');
let new_div = document.getElementById('new');
let complete = document.getElementById('complete');

for(list of lists){
    list.addEventListener("dragstart", (e)=>{
        let selected = e.target;

        ongoing.addEventListener("dragover", (e)=>{
            e.preventDefault();
        });
        ongoing.addEventListener("drop", (e)=>{
            ongoing.appendChild(selected);
            selected = null;
        });

        new_div.addEventListener("dragover", (e)=>{
            e.preventDefault();
        });
        new_div.addEventListener("drop", (e)=>{
            new_div.appendChild(selected);
            selected = null;
        });
        
        complete.addEventListener("dragover", (e)=>{
            e.preventDefault();
        });
        complete.addEventListener("drop", (e)=>{
            complete.appendChild(selected);
            selected = null;
        });
    })
}