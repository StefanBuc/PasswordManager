let dataBaseServer = "http://127.0.0.1";
let loggedIn = false;
let jwtToken = "";

async function getCurrentTab() {
    let queryOptions = { active: true, currentWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}

function login() {
    let user = window.prompt("Enter your username", "");
    let pass = window.prompt("Enter your password", "");

    let data = {
        username: user,
        password: pass
    };

    $.ajax({
        type: 'POST',
        url: dataBaseServer + "/login",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (response) {
            console.log("Logged in successfully");
            jwtToken = response.access_token;
            loggedIn = true;
        },
        error: function (err) {
            console.error("Login failed: ", err.responseJSON.msg);
            alert("Login failed: " + err.responseJSON.msg);
        }
    });
}

document.getElementById('savePass').addEventListener('click', async () => {
    if (!loggedIn) {
        login(); 
    } else {
        let tab = await getCurrentTab();
        let hostName = new URL(tab.url).hostname;
        let user = window.prompt("Enter your username", "");
        let pass = window.prompt("Enter your password", "");

        let data = {
            host: hostName,
            username: user,
            password: pass
        };

        $.ajax({
            type: 'POST',
            url: dataBaseServer + "/saveCredentials",
            headers: { 'Authorization': 'Bearer ' + jwtToken }, 
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (response) {
                console.log("Password saved:", response);
            },
            error: function (err) {
                console.error("Error saving password:", err.responseJSON);
            }
        });
    }
});


document.getElementById('getPass').addEventListener('click', async () => {
    if (!loggedIn) {
        login(); 
    } else {

        let tab = await getCurrentTab();
        let hostName = new URL(tab.url).hostname;
        
        $.ajax({
            type: 'POST',
            url: dataBaseServer + "/searchUsername",
            headers: { 'Authorization': 'Bearer ' + jwtToken }, 
            data: JSON.stringify(hostName),
            contentType: 'application/json',
            success: function (data) {
                if (data.username) {
                    alert("Username: " + data.username);
                }
            },
            error: function (err) {
                console.error("Error fetching credentials:", err.responseJSON);
                if (err.status === 404) {
                    alert("No credentials found for this website.");
                }
            }
        });

        $.ajax({
            type: 'POST',
            url: dataBaseServer + "/searchPass",
            headers: { 'Authorization': 'Bearer ' + jwtToken }, 
            data: JSON.stringify(hostName),
            contentType: 'application/json',
            success: function (data) {
                console.log("Found credentials:", data);
                if (data.password) {
                    alert("Password: " + data.password);
                }
            },
            error: function (err) {
                console.error("Error fetching credentials:", err.responseJSON);
                if (err.status === 404) {
                    alert("No credentials found for this website.");
                }
            }
        });
    }
});
