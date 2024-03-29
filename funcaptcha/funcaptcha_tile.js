(async () => {
    function l(e, t = !1) {
        if (t)
            for (const i of e) {
                var a = document.querySelectorAll(i);
                if (6 === a.length) return a
            } else
                for (const o of e) {
                    var n = document.querySelector(o);
                    if (n) return n
                }
        return null
    }

    function r() {
        return null !== l(['button[aria-describedby="descriptionVerify"]', 'button[data-theme="home.verifyButton"]', "#wrong_children_button", "#wrongTimeout_children_button"])
    }

    function s() {
        try {
            var e = l(['button[aria-describedby="descriptionVerify"]', 'button[data-theme="home.verifyButton"]']),
                t = (e && (window.postMessage({
                    nopecha: !0,
                    action: "clear"
                }, "*"), window.parent.postMessage({
                    nopecha: !0,
                    action: "clear"
                }, "*"), Input.click(e)), document.querySelector("#wrong_children_button")),
                a = (t && (window.postMessage({
                    nopecha: !0,
                    action: "clear"
                }, "*"), window.parent.postMessage({
                    nopecha: !0,
                    action: "clear"
                }, "*"), Input.click(t)), document.querySelector("#wrongTimeout_children_button"));
            a && (window.postMessage({
                nopecha: !0,
                action: "clear"
            }, "*"), window.parent.postMessage({
                nopecha: !0,
                action: "clear"
            }, "*"), Input.click(a))
        } catch (e) {}
    }

    function u() {
        return l(["#game_children_text", ".challenge-instructions-container"])?.innerText?.trim()
    }

    function p() {
        let e = l(["img#game_challengeItem_image"]);
        var t;
        return e ? e.src?.split(";base64,")[1] : (e = l([".challenge-container button"])) && (t = window.getComputedStyle(e, null)?.backgroundImage?.trim()?.match(/(?!^)".*?"/g)) && 0 !== t.length ? (t = t[0].replaceAll('"', "")).startsWith("blob:") ? t : t.split(";base64,")[1] : null
    }
    let d = null;
    async function e(e) {
        t = 500;
        var t, {
            task: a,
            cells: n,
            image_data: i
        } = await new Promise(n => {
            let i = !1;
            const o = setInterval(async () => {
                if (!i) {
                    i = !0;
                    var t = await BG.exec("Settings.get");
                    if (t && t.enabled && t.funcaptcha_auto_solve) {
                        t.funcaptcha_auto_open && r() && await s();
                        t = u();
                        if (t) {
                            var a = l(["#game_children_challenge ul > li > a", ".challenge-container button"], !0);
                            if (6 === a.length) {
                                let e = p();
                                if (e && (e.startsWith("blob:") && (e = await Image.encode(e)), d !== e)) return d = e, clearInterval(o), i = !1, n({
                                    task: t,
                                    cells: a,
                                    image_data: [e]
                                })
                            }
                        }
                        i = !1
                    }
                }
            }, t)
        });
        if (null !== a && null !== n && 0 !== i.length && null !== i[0])
            if ("Pick any square" === a) o = (o = parseInt(e.funcaptcha_solve_delay_time)) || 1e3, await Time.sleep(o), d = null, Input.click(n[0]);
            else {
                var o = "funcaptcha",
                    {
                        start: a,
                        data: c
                    } = await NopeCHA.post({
                        settings: e,
                        type: o,
                        task: a,
                        image_data: i
                    });
                if (c) {
                    await NopeCHA.delay({
                        settings: e,
                        start: a,
                        type: o
                    });
                    for (let e = 0; e < c.length; e++)
                        if (!1 !== c[e]) {
                            Input.click(n[e]);
                            break
                        }
                }
                d = null
            }
    }
    if (setInterval(() => {
            document.dispatchEvent(new Event("mousemove"))
        }, 50), window.location.pathname.startsWith("/fc/assets/tile-game-ui/") || window.location.pathname.startsWith("/fc/assets/ec-game-core/"))
        for (;;) {
            await Time.sleep(1e3);
            var t, a = await BG.exec("Settings.get");
            a && a.enabled && (t = await Location.hostname(), a.disabled_hosts.includes(t) || (a.funcaptcha_auto_open && r() ? await s() : a.funcaptcha_auto_solve && null !== u() && null !== p() && await e(a)))
        }
})();