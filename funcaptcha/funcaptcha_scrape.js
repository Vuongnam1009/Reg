(async () => {
    const t = {
        match: "https://captcha69.com/upload/funcaptcha_match",
        tile: "https://captcha69.com/upload/funcaptcha_tile"
    };
    for (const n of Object.keys(t)) window[n] = [];
    var e = window.addEventListener ? "addEventListener" : "attachEvent";
    for (window[e]("attachEvent" == e ? "onmessage" : "message", async e => {
            e = e[e.message ? "message" : "data"];
            if (e && !0 === e.nopecha_funcaptcha)
                if ("append" === e.action) window[e.type].push(e.data);
                else if ("clear" === e.action)
                for (const e of Object.keys(t)) window[e] = [];
            else "reload" === e.action && (window.parent.postMessage({
                nopecha_funcaptcha: !0,
                action: "reload"
            }, "*"), window.location.reload(!0))
        }, !1);;) {
        await Time.sleep(1e3);
        try {
            if (function(e, t = !1) {
                    if (t)
                        for (const n of e) {
                            var o = document.querySelectorAll(n);
                            if (6 === o.length) return o
                        } else
                            for (const c of e) {
                                var a = document.querySelector(c);
                                if (a) return a
                            }
                    return null
                }([".victory-container", ".victory"])) {
                var o = [];
                for (const [n, c] of Object.entries(t)) {
                    for (const i of window[n]) {
                        var a = Net.fetch(c, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify(i)
                        });
                        o.push(a)
                    }
                    window[n] = []
                }
                await Promise.all(o)
            }
        } catch (e) {}
    }
})();