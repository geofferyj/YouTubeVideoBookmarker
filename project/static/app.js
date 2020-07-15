$(window).on("load", function () {

    var listOfStamps = document.getElementById('timestamps').value.split(',').map(Number).sort(function (a,
        b) {
        return b - a
    });
    var stamps = (document.getElementById('timestamps').value == '') ? [] : document.getElementById(
        'timestamps').value.split(',').map(Number).sort(function (a, b) {
        return b - a
    });
    const input = document.getElementById("v");
    const button = document.getElementById("v_btn");
    const addTimeStampBtn = document.getElementById("addTimeStamp");
    addTimeStampBtn.addEventListener("click", addTime);
    const player = new Plyr('#player', {});
    let video_id = $("#video_id").val()
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

    if (video_id === 'None') {
        document.querySelectorAll(".btn").forEach((i, j) => {
            i.disabled = true
        })

        $("#blocked").attr("disabled", true)
    }

    function play() {
        player.play()
    }

    function pause() {
        player.pause();
    }

    player.on('statechange', (event) => {
        if (event.detail.code === 1) {
            console.log(`listOfStamps ${listOfStamps}`)
            var ts = roundNumber(listOfStamps.pop());
            console.log(`ts ${ts}`)

            t = setInterval(function () {

                if (roundNumber(player.currentTime) === ts && ts !== 0) {
                    pause()
                }

            }, 500);

        } else if (event.detail.code === 2) {
            clearInterval(t);
        }
    })



});