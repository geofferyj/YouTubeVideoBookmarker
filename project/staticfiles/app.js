$(window).on("load", function () {
    let timestamps = document.getElementById('timestamps')
    let listOfStamps = timestamps.value.split(',').map(Number).sort((a, b) => a - b);
    let stamps = (timestamps.value == '' )? [] : timestamps.value.split(',').map(Number).sort(function (a, b) {
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

    if (annyang) {
        var commands = {
            'play': play,
            'continue': play,
            'resume': play,
            'unpause': play
        };

        
        annyang.start()
        
    }

    function addTime() {

        let timestamp = roundNumber(player.currentTime)

        if (!(stamps.includes(timestamp) || timestamp == 0)) {
            stamps.push(timestamp)
            timestamps.value = stamps.sort((a, b) => a - b).join()
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
            annyang.abort()
            t = setInterval(function () {
                listOfStamps.forEach(function (item, index) {
                    if (roundNumber(player.currentTime) === item && item !== 0) {
                        pause()
                    }
                });

            }, 1000);

        } else if (event.detail.code === 2) {
            clearInterval(t);
            annyang.addCommands(commands);
            annyang.resume();
        }
    })

});