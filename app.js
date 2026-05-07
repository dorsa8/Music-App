const API_BASE = "https://yu7e9uylpa.execute-api.us-east-1.amazonaws.com/prod";

async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email,
            password
        })
    });

    const data = await response.json();

    if (response.status === 200) {

        localStorage.setItem("email", data.email);
        localStorage.setItem("user_name", data.user_name);

        window.location.href = "main.html";

    } else {
        document.getElementById("message").innerText = data.message;
    }
}

async function queryMusic() {

    const title = document.getElementById("title").value;
    const artist = document.getElementById("artist").value;
    const year = document.getElementById("year").value;
    const album = document.getElementById("album").value;

    let query = [];

    if (title) query.push(`title=${encodeURIComponent(title)}`);
    if (artist) query.push(`artist=${encodeURIComponent(artist)}`);
    if (year) query.push(`year=${encodeURIComponent(year)}`);
    if (album) query.push(`album=${encodeURIComponent(album)}`);

    const response = await fetch(
        `${API_BASE}/music?${query.join("&")}`
    );

    const data = await response.json();

    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "";

    if (data.items.length === 0) {
        resultsDiv.innerHTML = "<p>No result is retrieved. Please query again</p>";
        return;
    }

    data.items.forEach(song => {

        resultsDiv.innerHTML += `
            <div class="song-card">

                <h3>${song.title}</h3>

                <p>
                    ${song.artist} |
                    ${song.album} |
                    ${song.year}
                </p>

                <img src="${song.image_url}" width="150">

                <br><br>

                <button onclick='subscribe(${JSON.stringify(song)})'>
                    Subscribe
                </button>

                <hr>

            </div>
        `;
    });
}

async function subscribe(song) {

    const email = localStorage.getItem("email");

    const response = await fetch(`${API_BASE}/subscriptions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            song_key: song.song_key,
            title: song.title,
            artist: song.artist,
            year: song.year,
            album: song.album,
            image_url: song.image_url
        })
    });

    const data = await response.json();

    alert(data.message);

    loadSubscriptions();
}

async function loadSubscriptions() {

    const email = localStorage.getItem("email");

    const response = await fetch(
        `${API_BASE}/subscriptions?email=${email}`
    );

    const data = await response.json();

    const div = document.getElementById("subscriptions");

    div.innerHTML = "";

    data.items.forEach(song => {

        div.innerHTML += `
            <div class="song-card">

                <h3>${song.title}</h3>

                <p>
                    ${song.artist} |
                    ${song.album} |
                    ${song.year}
                </p>

                <img src="${song.image_url}" width="150">

                <br><br>

                <button onclick="removeSubscription('${song.song_key}')">
                    Remove
                </button>

                <hr>

            </div>
        `;
    });
}

async function removeSubscription(song_key) {

    const email = localStorage.getItem("email");

    const response = await fetch(
        `${API_BASE}/subscriptions?email=${email}&song_key=${encodeURIComponent(song_key)}`,
        {
            method: "DELETE"
        }
    );

    const data = await response.json();

    alert(data.message);

    loadSubscriptions();
}

function logout() {

    localStorage.clear();

    window.location.href = "login.html";
}

async function register() {

    const email = document.getElementById("registerEmail").value;
    const user_name = document.getElementById("registerUsername").value;
    const password = document.getElementById("registerPassword").value;

    const response = await fetch(`${API_BASE}/register`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            email,
            user_name,
            password
        })
    });

    const data = await response.json();

    if (response.status === 200) {

        alert("Registration successful");

        window.location.href = "login.html";

    } else {

        document.getElementById("registerMessage").innerText =
            data.message;
    }
}