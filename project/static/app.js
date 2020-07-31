window.setTimeout(function () {
    $(".alert").fadeTo(500, 0).slideUp(500, function () {
        $(this).remove();
    });
}, 2000);

$(window).on("load", function () {
    let timestamps = document.getElementById('timestamps')
    let listOfStamps = timestamps.value.split(',').map(Number).sort((a, b) => a - b);
    let stamps = (timestamps.value == '') ? [] : timestamps.value.split(',').map(Number).sort(function (a, b) {
        return b - a
    });
    const input = document.getElementById("v");
    const button = document.getElementById("v_btn");
    const addTimeStampBtn = document.getElementById("addTimeStamp");
    const stamp_display = document.getElementById('stamp_display')
    addTimeStampBtn.addEventListener("click", addTime);
    const player = new Plyr('#player', {
        settings: ['captions', 'quality', 'speed', 'loop']
    });
    let video_id = $("#video_id").val()
    let t;
    let hit = 0;
    window.player = player;

    listOfStamps.forEach(item => {
        if (item != '0') {
            let elem = document.createElement('span')
            elem.innerText = convertSecondsToHMmSs(item)
            elem.className = "badge badge-info"
            stamp_display.appendChild(elem)
        }
    });


    if (annyang) {
        var commands = {
            'play': play,
            'continue': play,
            'resume': play,
            'unpause': play
        };


        annyang.start({
            paused: true,
            autoRestart: false,
            continuous: false
        })

    }

    function addTime() {

        let timestamp = roundNumber(player.currentTime)

        if (!(stamps.includes(timestamp) || timestamp == 0)) {
            stamps.push(timestamp)
            timestamps.value = stamps.sort((a, b) => a - b).join()
            stamp_display.innerHTML = ''
            stamps.forEach(item => {
                let elem = document.createElement('span')
                elem.innerText = convertSecondsToHMmSs(item)
                elem.className = "badge badge-info"
                stamp_display.appendChild(elem)
            });
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

    if (!video_id) {
        document.querySelectorAll(".btn-d").forEach((i, j) => {
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
                    if (roundNumber(player.currentTime) === item && item !== 0 ) {
                        
                        hit++
                        pause()

                        if (hit == listOfStamps.length) {

                            $.ajax({
                                type: "post",
                                url: "/view_counter/",
                                data: {
                                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                                    video_id: document.getElementById('video_id').value,
                                    timestamps: timestamps.value
                                },
                                success: function (response) {
                                    console.log(response.message)

                                },
                                error: function (e) {
                                    console.log(e.error)
                                }
                            });

                        }
                    }
                });

            }, 1000);

        } else if (event.detail.code === 2) {
            clearInterval(t);
            annyang.addCommands(commands);
            annyang.resume();
        }
    })

    function zeroPad(numberStr) {
        return numberStr.padStart(2, "0");
    }

    function convertSecondsToHMmSs(seconds) {
        let s = zeroPad(roundNumber(seconds % 60).toString());
        let m = zeroPad(roundNumber((seconds / 60) % 60).toString());
        let h = zeroPad(roundNumber((seconds / (60 * 60)) % 24).toString());
        return `${h}:${m}:${s}`;
    }
});