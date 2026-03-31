let lists = document.getElementsByClassName('task__list');
let ongoing = document.getElementById('ongoing');
let new_div = document.getElementById('new');
let complete = document.getElementById('complete');
let bins = document.querySelectorAll('.bins');

let dragged = null;
let offsetX = 0;
let offsetY = 0;

for(list of lists){
    list.addEventListener("dragstart", (e)=>{
        let selected = e.target;

        ongoing.addEventListener("dragover", (e)=>{
            e.preventDefault();
        });
        ongoing.addEventListener("drop", (e)=>{
            ongoing.appendChild(selected);
            updateTaskStatus(selected, "ongoing");
            selected = null;
        });

        new_div.addEventListener("dragover", (e)=>{
            e.preventDefault();
        });
        new_div.addEventListener("drop", (e)=>{
            new_div.appendChild(selected);
            updateTaskStatus(selected, "new");
            selected = null;
        });
        
        complete.addEventListener("dragover", (e)=>{
            e.preventDefault();
        });
        complete.addEventListener("drop", (e)=>{
            complete.appendChild(selected);
            updateTaskStatus(selected, "done");
            selected = null;
        });
    })
}


for (let list of lists) {
    list.addEventListener("touchstart", (e) => {
      dragged = e.target.closest('.task__list-card');
      if (!dragged) return;

      
      const touch = e.touches[0];
      const rect = dragged.getBoundingClientRect();
      
      offsetX = touch.clientX - rect.left;
      offsetY = touch.clientY - rect.top;
      
      dragged.classList.add('dragging');
      dragged.style.pointerEvents = "none";
      dragged.style.position = "fixed";
      dragged.style.left = `0`;
      dragged.style.top = `0`;
      dragged.style.margin = `0`;
      dragged.style.zIndex = "1000";
      dragged.style.width = `${rect.width}px`;
    }, { passive: false });

    list.addEventListener("touchmove", (e) => {
        if (!dragged) return;
      
        e.preventDefault(); // block web scrolling while dragging

        const touch = e.touches[0];
        const scrollZone = 80; // px from edge to start auto-scrolling
        const scrollSpeed = 10; // px per frame

        dragged.style.transform = `translate(${touch.clientX - offsetX}px, ${touch.clientY - offsetY}px)`;

        // Auto-scroll if near top or bottom edge
        if (touch.clientY > window.innerHeight - scrollZone) {
            window.scrollBy(0, scrollSpeed);
        }

        if (touch.clientY < scrollZone) {
            window.scrollBy(0, -scrollSpeed);
        }
    }, { passive: false });
  
    list.addEventListener("touchend", (e) => {
      if (!dragged) return;
      dragged.style.pointerEvents = "";
      dragged.classList.remove('dragging');

      dragged.style.position = "";
      dragged.style.left = "";
      dragged.style.top = "";
      dragged.style.margin = "";
      dragged.style.zIndex = "";
      dragged.style.width = "";
      dragged.style.transform = "";
  
      const touch = e.changedTouches[0];
      const elem = document.elementFromPoint(touch.clientX, touch.clientY);
      const dropZone = elem ? elem.closest("#new, #ongoing, #complete") : null;
  
      if (dropZone && !dragged.contains(dropZone)) {
        dropZone.appendChild(dragged);
  
        if (dropZone.id === "ongoing") updateTaskStatus(dragged, "ongoing");
        if (dropZone.id === "new") updateTaskStatus(dragged, "new");
        if (dropZone.id === "complete") updateTaskStatus(dragged, "done");
      }
  
      dragged = null;
    });
}

function updateTaskStatus(list, forcedStatus = null) {
    const id = list.getAttribute("data-id");
    const userID = list.getAttribute("userID");
    let status = forcedStatus;

    if (!status) {
        const section = list.closest("section").classList[0];
        if (section === "new") status = "new";
        if (section === "ongoing") status = "ongoing";
        if (section === "complete") status = "done";
    }

    fetch("/update_status", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: id, status: status,  userID: userID }),
    }).then(res => res.json())
      .then(data => {
          if (!data.success) {
              console.error("Error with update", data.error);
          }
      });
}

bins.forEach(bin =>{
    bin.addEventListener("click", (e)=>{
        let selected = e.target.closest(".task__list-card");
        const id = selected.getAttribute("data-id");
        const userName = selected.getAttribute("userName");
        const from = selected.getAttribute('from')

        fetch("/delete_task", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ id: id, userName: userName, from: from }),
        }).then(response => response.json())
          .then(data => {
            if(data.success){
                selected.remove();
                window.location.href = data.redirect;
            }
            else{console.log("Can't delete", data.error);}
          });
    })
});
