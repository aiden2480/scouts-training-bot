var answersElems = document.querySelector(".public-exam-block").children;
var result = arguments[0];

console.log(JSON.parse(JSON.stringify(result)));

for (let i = 0; i < answersElems.length; i++) {
    let questionElem = answersElems[i].children[0];
    let questionId = questionElem.getAttribute("id");
    let selectedElem = questionElem.querySelector("[checked]");
    let selectedId = selectedElem.getAttribute("value");

    if (questionElem.classList.contains("right-answer")) {
        // Correct answer - return selection option
        result[questionId] = [selectedId];
    } else {
        // Incorrect answer - strike out selected option
        result[questionId] = result[questionId].filter(i => i !== selectedId);
    }
}

var completedElem = document.querySelector(".exam-results-summary");
var completed = completedElem.innerText.includes("Congratulations");

console.log(JSON.parse(JSON.stringify(result)));
return [completed, result];
