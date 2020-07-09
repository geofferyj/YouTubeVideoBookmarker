! function (e) {
    if ("object" == typeof exports && "undefined" != typeof module) module.exports = e();
    else if ("function" == typeof define && define.amd) define([], e);
    else {
        ("undefined" != typeof window ? window : "undefined" != typeof global ? global : "undefined" != typeof self ? self : this).ytPlayer = e()
    }
}(function () {
    return function () {
        return function e(t, n, r) {
            function i(o, a) {
                if (!n[o]) {
                    if (!t[o]) {
                        var l = "function" == typeof require && require;
                        if (!a && l) return l(o, !0);
                        if (s) return s(o, !0);
                        var u = new Error("Cannot find module '" + o + "'");
                        throw u.code = "MODULE_NOT_FOUND", u
                    }
                    var h = n[o] = {
                        exports: {}
                    };
                    t[o][0].call(h.exports, function (e) {
                        return i(t[o][1][e] || e)
                    }, h, h.exports, e, t, n, r)
                }
                return n[o].exports
            }
            for (var s = "function" == typeof require && require, o = 0; o < r.length; o++) i(r[o]);
            return i
        }
    }()({
        1: [function (e, t, n) {
            var r = Object.create || function (e) {
                    var t = function () {};
                    return t.prototype = e, new t
                },
                i = Object.keys || function (e) {
                    var t = [];
                    for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && t.push(n);
                    return n
                },
                s = Function.prototype.bind || function (e) {
                    var t = this;
                    return function () {
                        return t.apply(e, arguments)
                    }
                };

            function o() {
                this._events && Object.prototype.hasOwnProperty.call(this, "_events") || (this._events = r(null), this._eventsCount = 0), this._maxListeners = this._maxListeners || void 0
            }
            t.exports = o, o.EventEmitter = o, o.prototype._events = void 0, o.prototype._maxListeners = void 0;
            var a, l = 10;
            try {
                var u = {};
                Object.defineProperty && Object.defineProperty(u, "x", {
                    value: 0
                }), a = 0 === u.x
            } catch (e) {
                a = !1
            }

            function h(e) {
                return void 0 === e._maxListeners ? o.defaultMaxListeners : e._maxListeners
            }

            function d(e, t, n, i) {
                var s, o, a;
                if ("function" != typeof n) throw new TypeError('"listener" argument must be a function');
                if ((o = e._events) ? (o.newListener && (e.emit("newListener", t, n.listener ? n.listener : n), o = e._events), a = o[t]) : (o = e._events = r(null), e._eventsCount = 0), a) {
                    if ("function" == typeof a ? a = o[t] = i ? [n, a] : [a, n] : i ? a.unshift(n) : a.push(n), !a.warned && (s = h(e)) && s > 0 && a.length > s) {
                        a.warned = !0;
                        var l = new Error("Possible EventEmitter memory leak detected. " + a.length + ' "' + String(t) + '" listeners added. Use emitter.setMaxListeners() to increase limit.');
                        l.name = "MaxListenersExceededWarning", l.emitter = e, l.type = t, l.count = a.length, "object" == typeof console && console.warn && console.warn("%s: %s", l.name, l.message)
                    }
                } else a = o[t] = n, ++e._eventsCount;
                return e
            }

            function p() {
                if (!this.fired) switch (this.target.removeListener(this.type, this.wrapFn), this.fired = !0, arguments.length) {
                    case 0:
                        return this.listener.call(this.target);
                    case 1:
                        return this.listener.call(this.target, arguments[0]);
                    case 2:
                        return this.listener.call(this.target, arguments[0], arguments[1]);
                    case 3:
                        return this.listener.call(this.target, arguments[0], arguments[1], arguments[2]);
                    default:
                        for (var e = new Array(arguments.length), t = 0; t < e.length; ++t) e[t] = arguments[t];
                        this.listener.apply(this.target, e)
                }
            }

            function y(e, t, n) {
                var r = {
                        fired: !1,
                        wrapFn: void 0,
                        target: e,
                        type: t,
                        listener: n
                    },
                    i = s.call(p, r);
                return i.listener = n, r.wrapFn = i, i
            }

            function f(e, t, n) {
                var r = e._events;
                if (!r) return [];
                var i = r[t];
                return i ? "function" == typeof i ? n ? [i.listener || i] : [i] : n ? function (e) {
                    for (var t = new Array(e.length), n = 0; n < t.length; ++n) t[n] = e[n].listener || e[n];
                    return t
                }(i) : _(i, i.length) : []
            }

            function c(e) {
                var t = this._events;
                if (t) {
                    var n = t[e];
                    if ("function" == typeof n) return 1;
                    if (n) return n.length
                }
                return 0
            }

            function _(e, t) {
                for (var n = new Array(t), r = 0; r < t; ++r) n[r] = e[r];
                return n
            }
            a ? Object.defineProperty(o, "defaultMaxListeners", {
                enumerable: !0,
                get: function () {
                    return l
                },
                set: function (e) {
                    if ("number" != typeof e || e < 0 || e != e) throw new TypeError('"defaultMaxListeners" must be a positive number');
                    l = e
                }
            }) : o.defaultMaxListeners = l, o.prototype.setMaxListeners = function (e) {
                if ("number" != typeof e || e < 0 || isNaN(e)) throw new TypeError('"n" argument must be a positive number');
                return this._maxListeners = e, this
            }, o.prototype.getMaxListeners = function () {
                return h(this)
            }, o.prototype.emit = function (e) {
                var t, n, r, i, s, o, a = "error" === e;
                if (o = this._events) a = a && null == o.error;
                else if (!a) return !1;
                if (a) {
                    if (arguments.length > 1 && (t = arguments[1]), t instanceof Error) throw t;
                    var l = new Error('Unhandled "error" event. (' + t + ")");
                    throw l.context = t, l
                }
                if (!(n = o[e])) return !1;
                var u = "function" == typeof n;
                switch (r = arguments.length) {
                    case 1:
                        ! function (e, t, n) {
                            if (t) e.call(n);
                            else
                                for (var r = e.length, i = _(e, r), s = 0; s < r; ++s) i[s].call(n)
                        }(n, u, this);
                        break;
                    case 2:
                        ! function (e, t, n, r) {
                            if (t) e.call(n, r);
                            else
                                for (var i = e.length, s = _(e, i), o = 0; o < i; ++o) s[o].call(n, r)
                        }(n, u, this, arguments[1]);
                        break;
                    case 3:
                        ! function (e, t, n, r, i) {
                            if (t) e.call(n, r, i);
                            else
                                for (var s = e.length, o = _(e, s), a = 0; a < s; ++a) o[a].call(n, r, i)
                        }(n, u, this, arguments[1], arguments[2]);
                        break;
                    case 4:
                        ! function (e, t, n, r, i, s) {
                            if (t) e.call(n, r, i, s);
                            else
                                for (var o = e.length, a = _(e, o), l = 0; l < o; ++l) a[l].call(n, r, i, s)
                        }(n, u, this, arguments[1], arguments[2], arguments[3]);
                        break;
                    default:
                        for (i = new Array(r - 1), s = 1; s < r; s++) i[s - 1] = arguments[s];
                        ! function (e, t, n, r) {
                            if (t) e.apply(n, r);
                            else
                                for (var i = e.length, s = _(e, i), o = 0; o < i; ++o) s[o].apply(n, r)
                        }(n, u, this, i)
                }
                return !0
            }, o.prototype.addListener = function (e, t) {
                return d(this, e, t, !1)
            }, o.prototype.on = o.prototype.addListener, o.prototype.prependListener = function (e, t) {
                return d(this, e, t, !0)
            }, o.prototype.once = function (e, t) {
                if ("function" != typeof t) throw new TypeError('"listener" argument must be a function');
                return this.on(e, y(this, e, t)), this
            }, o.prototype.prependOnceListener = function (e, t) {
                if ("function" != typeof t) throw new TypeError('"listener" argument must be a function');
                return this.prependListener(e, y(this, e, t)), this
            }, o.prototype.removeListener = function (e, t) {
                var n, i, s, o, a;
                if ("function" != typeof t) throw new TypeError('"listener" argument must be a function');
                if (!(i = this._events)) return this;
                if (!(n = i[e])) return this;
                if (n === t || n.listener === t) 0 == --this._eventsCount ? this._events = r(null) : (delete i[e], i.removeListener && this.emit("removeListener", e, n.listener || t));
                else if ("function" != typeof n) {
                    for (s = -1, o = n.length - 1; o >= 0; o--)
                        if (n[o] === t || n[o].listener === t) {
                            a = n[o].listener, s = o;
                            break
                        } if (s < 0) return this;
                    0 === s ? n.shift() : function (e, t) {
                        for (var n = t, r = n + 1, i = e.length; r < i; n += 1, r += 1) e[n] = e[r];
                        e.pop()
                    }(n, s), 1 === n.length && (i[e] = n[0]), i.removeListener && this.emit("removeListener", e, a || t)
                }
                return this
            }, o.prototype.removeAllListeners = function (e) {
                var t, n, s;
                if (!(n = this._events)) return this;
                if (!n.removeListener) return 0 === arguments.length ? (this._events = r(null), this._eventsCount = 0) : n[e] && (0 == --this._eventsCount ? this._events = r(null) : delete n[e]), this;
                if (0 === arguments.length) {
                    var o, a = i(n);
                    for (s = 0; s < a.length; ++s) "removeListener" !== (o = a[s]) && this.removeAllListeners(o);
                    return this.removeAllListeners("removeListener"), this._events = r(null), this._eventsCount = 0, this
                }
                if ("function" == typeof (t = n[e])) this.removeListener(e, t);
                else if (t)
                    for (s = t.length - 1; s >= 0; s--) this.removeListener(e, t[s]);
                return this
            }, o.prototype.listeners = function (e) {
                return f(this, e, !0)
            }, o.prototype.rawListeners = function (e) {
                return f(this, e, !1)
            }, o.listenerCount = function (e, t) {
                return "function" == typeof e.listenerCount ? e.listenerCount(t) : c.call(e, t)
            }, o.prototype.listenerCount = c, o.prototype.eventNames = function () {
                return this._eventsCount > 0 ? Reflect.ownKeys(this._events) : []
            }
        }, {}],
        2: [function (e, t, n) {
            const r = e("events").EventEmitter,
                i = e("load-script2"),
                s = "https://www.youtube.com/iframe_api",
                o = {
                    "-1": "unstarted",
                    0: "ended",
                    1: "playing",
                    2: "paused",
                    3: "buffering",
                    5: "cued"
                },
                a = {
                    INVALID_PARAM: 2,
                    HTML5_ERROR: 5,
                    NOT_FOUND: 100,
                    UNPLAYABLE_1: 101,
                    UNPLAYABLE_2: 150
                },
                l = [];
            t.exports = class extends r {
                constructor(e, t) {
                    super();
                    const n = "string" == typeof e ? document.querySelector(e) : e;
                    n.id ? this._id = n.id : this._id = n.id = "ytplayer-" + Math.random().toString(16).slice(2, 8), this._opts = Object.assign({
                        width: 640,
                        height: 360,
                        autoplay: !1,
                        captions: void 0,
                        controls: !0,
                        keyboard: !0,
                        fullscreen: !0,
                        annotations: !0,
                        modestBranding: !1,
                        related: !0,
                        timeupdateFrequency: 1e3,
                        playsInline: !0
                    }, t), this.videoId = null, this.destroyed = !1, this._api = null, this._autoplay = !1, this._player = null, this._ready = !1, this._queue = [], this._interval = null, this._startInterval = this._startInterval.bind(this), this._stopInterval = this._stopInterval.bind(this), this.on("playing", this._startInterval), this.on("unstarted", this._stopInterval), this.on("ended", this._stopInterval), this.on("paused", this._stopInterval), this.on("buffering", this._stopInterval), this._loadIframeAPI((e, t) => {
                        if (e) return this._destroy(new Error("YouTube Iframe API failed to load"));
                        this._api = t, this.videoId && this.load(this.videoId, this._autoplay)
                    })
                }
                load(e, t = !1) {
                    this.destroyed || (this.videoId = e, this._autoplay = t, this._api && (this._player ? this._ready && (t ? this._player.loadVideoById(e) : this._player.cueVideoById(e)) : this._createPlayer(e)))
                }
                play() {
                    this._ready ? this._player.playVideo() : this._queueCommand("play")
                }
                pause() {
                    this._ready ? this._player.pauseVideo() : this._queueCommand("pause")
                }
                stop() {
                    this._ready ? this._player.stopVideo() : this._queueCommand("stop")
                }
                seek(e) {
                    this._ready ? this._player.seekTo(e, !0) : this._queueCommand("seek", e)
                }
                setVolume(e) {
                    this._ready ? this._player.setVolume(e) : this._queueCommand("setVolume", e)
                }
                getVolume() {
                    return this._ready && this._player.getVolume() || 0
                }
                mute() {
                    this._ready ? this._player.mute() : this._queueCommand("mute")
                }
                unMute() {
                    this._ready ? this._player.unMute() : this._queueCommand("unMute")
                }
                isMuted() {
                    return this._ready && this._player.isMuted() || !1
                }
                setSize(e, t) {
                    this._ready ? this._player.setSize(e, t) : this._queueCommand("setSize", e, t)
                }
                setPlaybackRate(e) {
                    this._ready ? this._player.setPlaybackRate(e) : this._queueCommand("setPlaybackRate", e)
                }
                setPlaybackQuality(e) {
                    this._ready ? this._player.setPlaybackQuality(e) : this._queueCommand("setPlaybackQuality", e)
                }
                getPlaybackRate() {
                    return this._ready && this._player.getPlaybackRate() || 1
                }
                getAvailablePlaybackRates() {
                    return this._ready && this._player.getAvailablePlaybackRates() || [1]
                }
                getDuration() {
                    return this._ready && this._player.getDuration() || 0
                }
                getProgress() {
                    return this._ready && this._player.getVideoLoadedFraction() || 0
                }
                getState() {
                    return this._ready && o[this._player.getPlayerState()] || "unstarted"
                }
                getCurrentTime() {
                    return this._ready && this._player.getCurrentTime() || 0
                }
                destroy() {
                    this._destroy()
                }
                _destroy(e) {
                    this.destroyed || (this.destroyed = !0, this._player && (this._player.stopVideo && this._player.stopVideo(), this._player.destroy()), this.videoId = null, this._id = null, this._opts = null, this._api = null, this._player = null, this._ready = !1, this._queue = null, this._stopInterval(), this.removeListener("playing", this._startInterval), this.removeListener("paused", this._stopInterval), this.removeListener("buffering", this._stopInterval), this.removeListener("unstarted", this._stopInterval), this.removeListener("ended", this._stopInterval), e && this.emit("error", e))
                }
                _queueCommand(e, ...t) {
                    this.destroyed || this._queue.push([e, t])
                }
                _flushQueue() {
                    for (; this._queue.length;) {
                        const e = this._queue.shift();
                        this[e[0]].apply(this, e[1])
                    }
                }
                _loadIframeAPI(e) {
                    if (window.YT && "function" == typeof window.YT.Player) return e(null, window.YT);
                    l.push(e), Array.from(document.getElementsByTagName("script")).some(e => e.src === s) || i(s).catch(e => {
                        for (; l.length;) l.shift()(e)
                    }), "function" != typeof window.onYouTubeIframeAPIReady && (window.onYouTubeIframeAPIReady = (() => {
                        for (; l.length;) l.shift()(null, window.YT)
                    }))
                }
                _createPlayer(e) {
                    if (this.destroyed) return;
                    const t = this._opts;
                    this._player = new this._api.Player(this._id, {
                        width: t.width,
                        height: t.height,
                        videoId: e,
                        playerVars: {
                            autoplay: t.autoplay ? 1 : 0,
                            cc_load_policy: null != t.captions ? !1 !== t.captions ? 1 : 0 : void 0,
                            hl: null != t.captions && !1 !== t.captions ? t.captions : void 0,
                            cc_lang_pref: null != t.captions && !1 !== t.captions ? t.captions : void 0,
                            controls: t.controls ? 2 : 0,
                            disablekb: t.keyboard ? 0 : 1,
                            enablejsapi: 1,
                            fs: t.fullscreen ? 1 : 0,
                            iv_load_policy: t.annotations ? 1 : 3,
                            modestbranding: t.modestBranding ? 1 : 0,
                            origin: window.location.origin,
                            playsinline: t.playsInline ? 1 : 0,
                            rel: t.related ? 1 : 0,
                            wmode: "opaque"
                        },
                        events: {
                            onReady: () => this._onReady(e),
                            onStateChange: e => this._onStateChange(e),
                            onPlaybackQualityChange: e => this._onPlaybackQualityChange(e),
                            onPlaybackRateChange: e => this._onPlaybackRateChange(e),
                            onError: e => this._onError(e)
                        }
                    })
                }
                _onReady(e) {
                    this.destroyed || (this._ready = !0, this.load(this.videoId, this._autoplay), this._flushQueue())
                }
                _onStateChange(e) {
                    if (this.destroyed) return;
                    const t = o[e.data];
                    if (!t) throw new Error("Unrecognized state change: " + e);
                    ["paused", "buffering", "ended"].includes(t) && this._onTimeupdate(), this.emit(t), ["unstarted", "playing", "cued"].includes(t) && this._onTimeupdate()
                }
                _onPlaybackQualityChange(e) {
                    this.destroyed || this.emit("playbackQualityChange", e.data)
                }
                _onPlaybackRateChange(e) {
                    this.destroyed || this.emit("playbackRateChange", e.data)
                }
                _onError(e) {
                    if (this.destroyed) return;
                    const t = e.data;
                    return t !== a.HTML5_ERROR ? t === a.UNPLAYABLE_1 || t === a.UNPLAYABLE_2 || t === a.NOT_FOUND || t === a.INVALID_PARAM ? this.emit("unplayable", this.videoId) : void this._destroy(new Error("YouTube Player Error. Unknown error code: " + t)) : void 0
                }
                _onTimeupdate() {
                    this.emit("timeupdate", this.getCurrentTime())
                }
                _startInterval() {
                    this._interval = setInterval(() => this._onTimeupdate(), this._opts.timeupdateFrequency)
                }
                _stopInterval() {
                    clearInterval(this._interval), this._interval = null
                }
            }
        }, {
            events: 1,
            "load-script2": 3
        }],
        3: [function (e, t, n) {
            t.exports = function (e, t, n) {
                return new Promise((r, i) => {
                    const s = document.createElement("script");
                    s.async = !0, s.src = e;
                    for (const [e, n] of Object.entries(t || {})) s.setAttribute(e, n);
                    s.onload = (() => {
                        s.onerror = s.onload = null, r(s)
                    }), s.onerror = (() => {
                        s.onerror = s.onload = null, i(new Error(`Failed to load ${e}`))
                    }), (n || document.head || document.getElementsByTagName("head")[0]).appendChild(s)
                })
            }
        }, {}]
    }, {}, [2])(2)
});