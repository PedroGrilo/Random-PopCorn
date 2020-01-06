const API_URL = 'http://127.0.0.1:8000/api/account/';

function changeDialog(movie) {

    /* limpar texto anterior, para n incrementar em cima e aparecer valores repetidos*/
    document.getElementById("genre-text").innerText = ""
    document.getElementById("languages-text").innerText = ""

    //Change text Modal
    document.getElementById("titleRandomModal").innerText = "Details: " +movie.title;

    document.getElementById("plot-text").innerText = movie.plot;


    for (i in movie.genre)
        document.getElementById("genre-text").innerText += movie.genre[i].name + " ";

    document.getElementById("release-text").innerText = movie.release_date;
    document.getElementById("runtime-text").innerText = movie.runtime + " minutes";

    for (i in movie.languages)
        document.getElementById("languages-text").innerText += movie.languages[i].language + ";  ";

    document.getElementById("ratingimdb-text").innerText = movie.rating_imdb;

    document.getElementById('close1').setAttribute('hidden','True')
    document.getElementById('close2').setAttribute('hidden','True')

}

function getRandomMovie() {
    document.getElementById("blockRandom").style.visibility = "visible";

    var req = new XMLHttpRequest();
    req.open("GET", "/api/movie/random/");
    req.addEventListener("load", function () {
        let movie = JSON.parse(this.responseText);

        //Change text index
        document.getElementById("titleRandom").innerText = movie.title;
        document.getElementById("imgRandom").src = movie.poster;

        //Change text dialog
        changeDialog(movie)
    });
    req.send();
}

