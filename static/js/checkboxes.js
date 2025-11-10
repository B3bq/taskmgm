async function updateCheckboxStatus(detailsId, isChecked, element) {
    try{
        const response = fetch("{{ url_for('update_details') }}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id: detailsId,
                checked: isChecked
            })
        });


        const container = element.closest('.checkbox-item');
        if (isChecked) {
            container.classList.remove('checkboxes__normal');
            container.classList.add('checkboxes__checked');
        } else {
            container.classList.remove('checkboxes__checked');
            container.classList.add('checkboxes__normal');
        }

    } catch (err){
        console.error("Error:", err);
    }
}