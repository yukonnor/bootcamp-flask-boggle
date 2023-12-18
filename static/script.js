$form = $("form");
$wordInput = $("#word-guess");

// make a request to the server to see if the word is valid
async function check_word(word) {
    // make a request to /check-word with the word as
    const response = await axios.get("/check-word", { params: { "word-guess": word } });

    console.log(`check_word() response.data: ${JSON.stringify(response.data)}`);

    return response.data["result"];
}

async function process_word_submission(event) {
    // prevent form from refreshing page
    event.preventDefault();

    console.log("hello");
    console.log($wordInput.val());

    let word = $wordInput.val();

    // make a request to the server to see if word is valid
    let result = await check_word(word);

    // show the result to the user in the DOM
    show_result(result, word);
}

$form.on("submit", process_word_submission);
