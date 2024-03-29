const VERSION = chrome.runtime.getManifest().version;
class BG {
    static exec() {
        return new Promise(t => {
            try {
                chrome.runtime.sendMessage([...arguments], t)
            } catch (e) {
                Time.sleep(1e3).then(() => {
                    t(null)
                })
            }
        })
    }
}
class Net {
    static async fetch(e, t) {
        return BG.exec("Net.fetch", {
            url: e,
            options: t
        })
    }
}
class Script {
    static inject_file(a) {
        return new Promise(e => {
            var t = document.createElement("script");
            t.src = chrome.runtime.getURL(a), t.onload = e, (document.head || document.documentElement).appendChild(t)
        })
    }
}
class Location {
    static info() {
        return BG.exec("Tab.info")
    }
    static url() {
        return BG.exec("Tab.url")
    }
    static hostname() {
        return BG.exec("Tab.hostname")
    }
    static subframe() {
        try {
            return window.self !== window.top
        } catch (e) {
            return !0
        }
    }
}
class Image {
    static encode(t) {
        return new Promise(a => {
            if (null === t) return a(null);
            const e = new XMLHttpRequest;
            e.onload = () => {
                const t = new FileReader;
                t.onloadend = () => {
                    let e = t.result;
                    if (e.startsWith("data:text/html;base64,")) return a(null);
                    e = e.split(";base64,")[1], a(e)
                }, t.readAsDataURL(e.response)
            }, e.onerror = () => {
                a(null)
            }, e.onreadystatechange = () => {
                4 == this.readyState && 200 != this.status && a(null)
            }, e.open("GET", t), e.responseType = "blob";
            try {
                e.send()
            } catch (e) {
                a(null)
            }
        })
    }
    static encode_image(e) {
        "string" == typeof e && (e = document.querySelector(e));
        try {
            var t = document.createElement("canvas");
            return t.width = e.naturalWidth, t.height = e.naturalHeight, t.getContext("2d").drawImage(e, 0, 0), Image.encode_canvas(t)
        } catch (e) {
            return null
        }
    }
    static encode_canvas(e) {
        "string" == typeof e && (e = document.querySelector(e));
        try {
            return e.toDataURL("image/jpeg").split(";base64,")[1]
        } catch (e) {
            return null
        }
    }
    static encode_element(e) {
        var t, a;
        return (e = "string" == typeof e ? document.querySelector(e) : e) instanceof HTMLCanvasElement ? Image.encode_canvas(e) : e instanceof HTMLImageElement ? Image.image(e) : e instanceof HTMLElement ? ((t = document.createElement("canvas")).width = e.clientWidth, t.height = e.clientHeight, a = t.getContext("2d"), e = e.computedStyleMap().get("background-image"), a.drawImage(e, 0, 0), Image.encode_canvas(t)) : null
    }
}
class Input {
    static click(e) {
        var t, a;
        (e = "string" == typeof e ? document.querySelector(e) : e) && (t = (a = e.getBoundingClientRect()).left + a.width / 2, a = a.top + a.height / 2, Input.point(e, t, a))
    }
    static point(t, a, r, n = "click") {
        if (t = "string" == typeof t ? document.querySelector(t) : t) {
            var i, s;
            let e = ["mouseover", "mouseenter", "mousedown", "mouseup", "click", "mouseout"];
            for (i of e = "click" !== n ? [n] : e) t.dispatchEvent((s = i, new MouseEvent(s, {
                bubbles: !0,
                cancelable: !0,
                view: window,
                detail: 1,
                screenX: a,
                screenY: r,
                clientX: a,
                clientY: r,
                ctrlKey: !1,
                altKey: !1,
                shiftKey: !1,
                metaKey: !1,
                button: 0,
                relatedTarget: null
            })))
        }
    }
}
class NopeCHA {
    static MAX_WAIT_POST = 60;
    static MAX_WAIT_GET = 60;
    static RATE_LIMITED_WAIT = 3;
    static INCOMPLETE_JOB_WAIT = 1;
    static ERRORS = {
        UNKNOWN: 9,
        INVALID_REQUEST: 10,
        RATE_LIMITED: 11,
        BANNED_USER: 12,
        NO_JOB: 13,
        INCOMPLETE_JOB: 14,
        INVALID_KEY: 15,
        NO_CREDIT: 16,
        UPDATE_REQUIRED: 17,
        UNAVAILABLE_FEATURE: 18
    };
    static default_headers(e) {
        var t = {};
        return e.key && "undefined" !== e.key && (t.Authorization = "Bearer " + e.key), t
    }
    static async post({
        settings: e,
        type: t,
        audio_data: a,
        image_urls: r,
        image_url: n,
        image_data: i,
        grid: s,
        task: c,
        choices: o
    }) {
        var l = Time.time(),
            u = await Location.url(),
            d = {
                key: 'point_42221bc0893e417991a3902114bb0bdc',
                type: t,
                url: u,
                v: VERSION
            };
        for (a && (d.audio_data = a), r && (d.image_urls = r), n && (d.image_url = n), i && (d.image_data = i), s && (d.grid = s), c && (d.task = c), o && (d.choices = o);;) {
            if (Time.time() - l > 1e3 * NopeCHA.MAX_WAIT_POST) break;
            try {
                var m, p = NopeCHA.default_headers(e),
                    _ = (p["Content-Type"] = "application/json", JSON.parse(await Net.fetch(BASE_API+"/funcaptcha", {
                        headers: p,
                        method: "POST",
                        body: JSON.stringify(d)
                    })));
				//console.log("========= _ ============");
				//console.log(_);
                if (null === _) break;
				//console.log("debug 2");
				//console.log(_.data);
                if (!("error" in _)) return m = _.data, await NopeCHA.get({
                    settings: e,
                    start: l,
                    id: m
                });
				//console.log("debug 3");
                if (_.error !== NopeCHA.ERRORS.RATE_LIMITED) break;
				//console.log("debug 4");
                await Time.sleep(1e3 * NopeCHA.RATE_LIMITED_WAIT)
				//console.log("debug 5");
            } catch (e) {
                break
            }
        }
        return {
            start: l,
            id: null,
            data: null,
            metadata: null,
			kkm_debug: 1
        }
    }
    static async get({
        settings: e,
        start: t,
        id: a
    }) {
        for (var r = Time.time(); !(Time.time() - r > 1e3 * NopeCHA.MAX_WAIT_GET);) try {
            var n = NopeCHA.default_headers(e),
                i = JSON.parse(await Net.fetch(`${BASE_API}/funcaptcha?key=${'point_42221bc0893e417991a3902114bb0bdc'}&action=get&id=` + a, {
                    headers: n
                }));
			//console.log("========= i =========");
			//console.log(i);
            if (null === i) break;
            if (!("error" in i)) return {
                start: t,
                data: i.data,
                metadata: i.metadata
            };
            if (i.error === NopeCHA.ERRORS.RATE_LIMITED) await Time.sleep(1e3 * NopeCHA.RATE_LIMITED_WAIT);
            else {
                if (i.error !== NopeCHA.ERRORS.INCOMPLETE_JOB) break;
                await Time.sleep(500 * NopeCHA.INCOMPLETE_JOB_WAIT)
            }
        } catch (e) {
            break
        }
        return {
            start: t,
            data: null,
            metadata: null,
			kkm_debug: 2
        }
    }
    static async delay({
        settings: e,
        type: t
    }) {
        e = e[t + "_solve_delay"] ? parseInt(e[t + "_solve_delay_time"]) || 100 : 0;
        0 < e && await Time.sleep(e)
    }
}