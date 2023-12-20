// get elements we'll be working with
const $form = $("form");
const $formFields = $("fieldset");
const $wordInput = $("#word-guess");
const $resultContainer = $("#result");
const $score = $("#score");
const $time = $("#time");
const $highScore = $("#high-score");
const $timesPlayed = $("#times-played");

// Q: OK to use global variables like this? If not, how to avoid?
let score = 0;
let timesPlayed = 0;
let gameActive = true;
let foundWords = [];

let timeLeft = 30; // game duration in seconds

/* When page loads, get the user's stats from the session */
async function getStats() {
    // make a POST request to /check-word with the word as
    const response = await axios.get("/stats");

    console.log(`getStats() response.data: ${JSON.stringify(response.data)}`);

    $highScore.text(response.data["high_score"]);
    $timesPlayed.text(response.data["times_played"]);
}

getStats();

// make a request to the server to see if the word is valid
async function checkWord(word) {
    // make a request to /check-word with the word as
    const response = await axios.get("/check-word", { params: { "word-guess": word } });

    console.log(`checkWord() response.data: ${JSON.stringify(response.data)}`);

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
    } else if (result === "already-found") {
        $resultContainer.html(`Nice try! <b>${word}</b> has already been found`);
        $resultContainer.addClass("alert-danger");
    }
}

function updateScore(word, score) {
    score += word.length;

    // Q: Should I update the display in a separate function if it's just one line like this?
    $score.text(score);
    return score;
}

function checkFoundWords(word) {
    if (foundWords.includes(word)) {
        return "already-found";
    } else {
        foundWords.push(word);
        return "ok";
    }
}

async function processWordSubmission(event) {
    // prevent form from refreshing page
    event.preventDefault();

    let word = $wordInput.val();
    word = word.toLowerCase();

    // if game is active
    if (gameActive) {
        // make a request to the server to see if word is valid
        let result = await checkWord(word);

        // if valid word, check if word has alread been found
        if (result === "ok") {
            result = checkFoundWords(word);
        }

        // update & show score based on the result
        if (result === "ok") {
            score = updateScore(word, score);
        }

        // show the result to the user in the DOM
        showResult(result, word);
    }

    // reset the word input
    $wordInput.val("");
}

$form.on("submit", processWordSubmission);

/* Timer Code */
function countdown() {
    // Decrement timer
    --timeLeft;

    // Update display
    // TODO: Show time left in badge. Change badge color when <10s.
    $time.text(timeLeft);

    // Check if timer has reached 0
    if (timeLeft === 0) {
        clearInterval(timerInterval); // Stop the interval
        gameActive = false;
        disableForm();
        submitScore(score);
    }
}

// Set up the interval
const timerInterval = setInterval(countdown, 1000); // Execute countdown every second

/* Disable the form when the timer is done */
function disableForm() {
    // update messaging
    $resultContainer.removeClass("alert-success alert-danger alert-warning alert-info");
    $resultContainer.text("Time's up!");
    $resultContainer.addClass("alert-dark");

    // disable form
    $formFields.prop("disabled", true);
}

/* Submit score to server once time runs out */
async function submitScore(score) {
    // make a POST request to /check-word with the word as
    const response = await axios.post("/update-stats", { score: score });

    console.log(`submitScore() response.data: ${JSON.stringify(response.data)}`);

    $highScore.text(response.data["high_score"]);
    $timesPlayed.text(response.data["times_played"]);

    return response.data["result"];
}
