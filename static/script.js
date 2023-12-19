// get elements we'll be working with
const $form = $("form");
const $wordInput = $("#word-guess");
const $resultContainer = $("#result");
const $score = $("#score");

let score = 0;

// make a request to the server to see if the word is valid
async function checkWord(word) {
    // make a request to /check-word with the word as
    const response = await axios.get("/check-word", { params: { "word-guess": word } });

    console.log(`check_word() response.data: ${JSON.stringify(response.data)}`);

    return response.data["result"];
}

function showResult(result, word) {
    // depending on the result, update the class and text of the container

    // Remove all alert classes so that we can add the class that we're updating to
    $resultContainer.removeClass("alert-success alert-danger alert-warning alert-info");

    word = word.toUpperCase();

    if (result === "ok") {
        $resultContainer.html(`Count it! <b>${word}</b> is in the board`);
        $resultContainer.addClass("alert-success");
    } else if (result === "not-on-board") {
        $resultContainer.html(`Nice try! <b>${word}</b> isn't on the board`);
        $resultContainer.addClass("alert-danger");
    } else if (result === "not-word") {
        $resultContainer.html(`Sorry. <b>${word}</b> isn't in our dictionary`);
        $resultContainer.addClass("alert-danger");
    }
}

function updateScore(result, word, score) {
    if (result === "ok") {
        score += word.length;
        showNewScore(score);
        console;
    }

    return score;
}

function showNewScore(score) {
    $score.text(score);
}

async function processWordSubmission(event) {
    // prevent form from refreshing page
    event.preventDefault();

    console.log("hello");
    console.log($wordInput.val());

    let word = $wordInput.val();
    word = word.toLowerCase();

    // make a request to the server to see if word is valid
    let result = await checkWord(word);

    // update & show score based on the result
    score = updateScore(result, word, score);

    // show the result to the user in the DOM
    showResult(result, word);

    // reset the word input
    $wordInput.val("");
}

$form.on("submit", processWordSubmission);
