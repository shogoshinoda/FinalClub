const getCookie = (name) => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) {
                return decodeURIComponent(value);
            }
        }
    }
};
const csrftoken = getCookie('csrftoken');
console.log(csrftoken)

async function board_create(){
    const url = '/';
    let res = await fetch(url,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        },
    });
    console.log('done')
    let json = await res.json();

    return json.content;
}

async function board_create_post(form) {
    const url = '/';
    let res = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: form,
    });
    let json = await res.json();
    return json.content;        
}

// // 一覧画面→新規作成画面（新規作成フォーム取得）
// document.getElementById('create_boards_form').addEventListener('click', (event) => {
//     event.preventDefault();
//     window.scrollTo(0, 0);
//     board_create()
//     .then(response => {
//         // let list = document.getElementById("list");
//         // list.className = "list";
//         let content = document.getElementById("content");
//         content.innerHTML = response;
//         // create.className = "create current";
//     })
//     .then(() => {
//         // // 新規作成画面→一覧画面（戻る）
//         // document.getElementById('create_back_list').addEventListener('click', (event) => {
//         //     window.scrollTo(0, 0);
//         //     let create = document.getElementById("create");
//         //     create.innerHTML = '';
//         //     create.className = "create";
//         //     let list = document.getElementById("list");
//         //     list.className = "list current";
//         // });
//         // 新規作成画面→一覧画面（新規作成フォーム送信、一覧データ取得）
document.getElementById('create_boards_form').addEventListener('submit', (event) => {
    event.preventDefault();
    window.scrollTo(0, 0);
    const form = new FormData(document.forms[0]);
    menu_create_post(form)
    .then(response => {
        // let create = document.getElementById("create");
        // create.innerHTML = '';
        // create.className = "create";
        // let list = document.getElementById("list");
        // list.className = "list current";
        let list_container = document.getElementById("content");
        list_container.innerHTML = response;     
    });
});
//     });
// });
