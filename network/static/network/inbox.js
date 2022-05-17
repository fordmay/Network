document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like').forEach(item => {
        item.onclick = () => {
            like(item);
        }
    });
    document.querySelectorAll('.edit').forEach(item => {
        item.onclick = () => {
            edit(item);
        }
    });
});

function like(item) {
    const post_id = item.id.replace('like', '');

    fetch(`/posts/${post_id}`, {
        method: 'PUT'
    }).then(result => {
        if (result.ok) {
            // if database changed, change data in DOM
            if (item.children[0].innerHTML === '🤍') {
                item.children[0].innerHTML = '❤';
                item.children[1].innerHTML++;
            } else {
                item.children[0].innerHTML = '🤍';
                item.children[1].innerHTML--;
            }
        }
    })
        // Catch any errors and log them to the console
        .catch(error => {
            console.log('Error:', error);
        });
}

function edit(item) {
    const post_id = item.id.replace('edit', '');
    const editable_item = item.nextElementSibling;
    const old_value = editable_item.innerHTML;
    
    item.style.display = "none";
    editable_item.innerHTML = "";
    // create textarea with 2 buttons "ok" and "cancel"
    const div = document.createElement('div');
    const textarea = document.createElement('textarea');
    textarea.rows = "2";
    textarea.className = "form-control";
    textarea.value = old_value;
    const div_buttons = document.createElement('div');
    const button_ok = document.createElement('button');
    button_ok.className = "btn btn-primary btn-sm m-1";
    button_ok.innerText = "ok";
    const button_cancel = document.createElement('button');
    button_cancel.className = "btn btn-primary btn-sm m-1";
    button_cancel.innerText = "cancel";
    div_buttons.append(button_ok, button_cancel);
    div.append(textarea, div_buttons);
    editable_item.append(div);
    // if textarea empty, disable button "ok"
    textarea.onkeyup = () => {
        if (textarea.value.trim().length > 0) {
            button_ok.disabled = false;
        } else {
            button_ok.disabled = true;
        }
    }

    button_ok.onclick = () => {
        const new_value = textarea.value.trim();
        if (new_value === old_value) {
            editable_item.innerHTML = old_value;
            item.style.display = "block";
        } else {
            fetch(`/posts/${post_id}`, {
                method: 'POST',
                body: new_value
            }).then(result => {
                if (result.ok) {
                    editable_item.innerHTML = new_value;
                    item.style.display = "block";
                }
            })
                // Catch any errors and log them to the console
                .catch(error => {
                    console.log('Error:', error);
                });
        }
    }
    
    button_cancel.onclick = () => {
        editable_item.innerHTML = old_value;
        item.style.display = "block";
    }
}
