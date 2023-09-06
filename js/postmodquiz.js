const rand = items => items[Math.floor(Math.random() * items.length)];
const submit_url = document.querySelector("form").action;
const tokenElem = document.querySelector("[name=authenticity_token]");
const questionsElems = document.querySelectorAll("[name='questions[]']");
const data = new FormData();

data.append("utf8", "\u2713");
data.append("commit", "Submit Answer");
data.append("authenticity_token", tokenElem.getAttribute("value"));

// Generate random answers
for (let i = 0; i < questionsElems.length; i++) {
    let questionId = questionsElems[i].getAttribute("value");
    let random_answer = rand(arguments[0][questionId]);

    data.append("questions[]", questionId);
    data.append(`${questionId}_answer_id`, random_answer);
}

// Submit
var resp = await fetch(submit_url, {
    body: new URLSearchParams(data),
    method: "post",
});

return resp.url;
