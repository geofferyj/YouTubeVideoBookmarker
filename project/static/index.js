$(window).on("load", function () {

    var listOfStamps = document.getElementById('timestamps').value.split(',').map(Number).sort(function (a, b) {
        return b - a
    });
    var stamps = (document.getElementById('timestamps').value == '') ? [] : document.getElementById('timestamps').value.split(',').map(Number).sort(function (a, b) {
        return b - a
    });
    const input = document.getElementById("v");
    const button = document.getElementById("v_btn");
    const addTimeStampBtn = document.getElementById("addTimeStamp");
    addTimeStampBtn.addEventListener("click", addTime);
    const player = new Plyr('#player', {});
    let video = '{{video}}'
    let t;
    window.player = player;


    function addTime() {

        let timestamp = roundNumber(player.currentTime)

        if (!(stamps.includes(timestamp) || timestamp == 0)) {
            stamps.push(timestamp)
            document.getElementById("timestamps").value = stamps.sort(function (a, b) {
                return b - a
            }).join()
        }

    }

    function roundNumber(number, decimalPlaces = 0) {

        return Math.round(number * Math.pow(10, decimalPlaces)) /
            Math.pow(10, decimalPlaces);
    }

    // {% if not hidden_page %}
    input.addEventListener("keyup", stateHandle);
    button.addEventListener("click", fix_url);

    function fix_url() {
        input.value = input.value.slice(-11)
    }

    function stateHandle() {
        if (input.value === "") {
            button.disabled = true
        } else {
            button.disabled = false
        }
    }

    // {% endif %}

    if (annyang) {
        console.log(annyang);
        const commands = {
            'play': play(),
            'resume': play(),
            'continue': play(),
        }
        annyang.addCommands(commands);
        annyang.start({ paused: true });
    }

    if (video === 'None') {
        document.querySelectorAll(".btn").forEach((i, j) => {
            i.disabled = true
        })
    }

    function play() {player.play()  }
    player.on('statechange', (event) => {
        if (player.playing) {
            annyang.pause();
            var ts = roundNumber(listOfStamps.pop());
            t = setInterval(function () {

                if (roundNumber(player.currentTime) === ts) {
                    player.pause()
                }

            }, 500);

        } else if (player.paused) {
            clearInterval(t);
            annyang.resume();


        }
    })


});