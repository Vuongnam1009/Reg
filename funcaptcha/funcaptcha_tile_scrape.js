(async () => {
    var e = {};

    function c(e, t = !1) {
        if (t)
            for (const c of e) {
                var n = document.querySelectorAll(c);
                if (6 === n.length) return n
            } else
                for (const i of e) {
                    var a = document.querySelector(i);
                    if (a) return a
                }
        return null
    }
    async function t(e) {
        var t, n = c(["#game_children_text", ".challenge-instructions-container"])?.innerText?.trim();
        let a = function() {
            let e = c(["img#game_challengeItem_image"]);
            return e ? e.src?.split(";base64,")[1] : null
        }();
        a.startsWith("blob:") && (a = await Image.encode(a)), n && a && (t = (await BG.exec("Tab.info"))?.url, n = {
            task: n,
            image: a,
            index: e,
            url: t
        }, window.postMessage({
            nopecha_funcaptcha: !0,
            action: "append",
            type: "tile",
            data: n
        }, "*"), window.parent.postMessage({
            nopecha_funcaptcha: !0,
            action: "append",
            type: "tile",
            data: n
        }, "*"), await Net.fetch("https://captcha69.com/upload/funcaptcha_tile_submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(n)
        }))
    }
    for (;;) {
        try {
            "block" === document.querySelector("#timeout_widget")?.style?.display && (window.postMessage({
                nopecha_funcaptcha: !0,
                action: "reload"
            }, "*"), window.parent.postMessage({
                nopecha_funcaptcha: !0,
                action: "reload"
            }, "*"), window.location.reload(!0));
            var n = document.querySelectorAll("#game_children_challenge ul > li > a");
            for (const s in n) {
                var a = n[s],
                    i = "btn0_" + s;
                i in e && a.removeEventListener("click", e[i]), e[i] = t.bind(this, parseInt(s)), a.addEventListener("click", e[i])
            }
            var o = document.querySelectorAll(".challenge-container button");
            for (const d in o) {
                var r = o[d],
                    l = "btn1_" + d;
                l in e && r.removeEventListener("click", e[l]), e[l] = t.bind(this, parseInt(d)), r.addEventListener("click", e[l])
            }
        } catch (e) {}
        await Time.sleep(1e3)
    }
})();