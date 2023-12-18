$form = $("form");
$wordInput = $("#word-guess");

function check_word(event) {
    // prevent form from refreshing page
    event.preventDefault();

    console.log("hello");
    console.log($wordInput.val());
}

$form.on("submit", check_word);
