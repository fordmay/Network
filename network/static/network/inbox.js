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
    console.log(post_id);
}
