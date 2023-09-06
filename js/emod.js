var id = document.querySelector("#module_details").getAttribute("data-id");
var data = new FormData();
data.append("module_id", id);

document.querySelector(".topic-container#topic_1").childNodes.forEach(node => {
    if (!node.classList?.contains("slide")) return; 
    data.append("slide_ids[]", node.getAttribute("data-reference"));
});

fetch("https://training.scouts.com.au/progress/", {
    body: new URLSearchParams(data),
    method: "post",
}).then(console.log);

var resp = await fetch("https://training.scouts.com.au/user_details/");
var user_details = await resp.json();

fetch("https://training.scouts.com.au/completed/", {
    method: "post",
    body: new URLSearchParams({
        username: `${user_details.branch}-${user_details.membership_number}`,
        id: id,
        narration: false,
        user_agent: navigator.userAgent,
    }),
}).then(console.log);
