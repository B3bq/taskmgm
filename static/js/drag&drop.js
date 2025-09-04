let lists = document.getElementsByClassName('task__list');
let ongoing = document.getElementById('ongoing');
let new_div = document.getElementById('new');
let complete = document.getElementById('complete');
let bins = document.querySelectorAll('.bins');

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
    })
}

bins.forEach(bin =>{
    bin.addEventListener("click", (e)=>{
        let selected = e.target.closest(".task__list-card");
        const id = selected.getAttribute("data-id");
        const userName = selected.getAttribute("userName");

        fetch("/delete_task", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ id: id, userName: userName }),
        }).then(response => response.json())
          .then(data => {
            if(data.success){
                selected.remove();
            }
            else{console.log("Can't delete", data.error);}
          });
    })
});
