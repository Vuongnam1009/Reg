import {
    BASE_API,
    deep_copy,
    SettingsManager,
    Time,
    Util
} from "./utils.mjs";
const is_firefox = chrome.runtime.getURL("").startsWith("moz-extension://"),
    is_chrome = chrome.runtime.getURL("").startsWith("chrome-extension://"),
    bapi = {
        VERSION: null,
        browser: null,
        reconnect_scripts: null,
        register_language: null
    };
is_firefox ? (bapi.VERSION = "firefox", bapi.browser = browser, bapi.reconnect_scripts = () => {
    browser.runtime.onInstalled.addListener(async () => {
        for (const a of browser.runtime.getManifest().content_scripts) browser.tabs.query({
            url: a.matches
        }, e => {
            for (const t of e) browser.scripting.executeScript({
                target: {
                    tabId: t.id
                },
                files: a.js
            })
        })
    })
}, bapi.register_language = () => {
    browser.webRequest.onBeforeSendHeaders.addListener(e => {
        e = new URL(e.url);
        if ("en-US" !== e.searchParams.get("hl")) return e.searchParams.set("hl", "en-US"), {
            redirectUrl: e.toString()
        }
    }, {
        urls: ["*://*.google.com/recaptcha/*", "*://*.recaptcha.net/recaptcha/*"],
        types: ["sub_frame"]
    }, ["blocking"]), browser.webRequest.onBeforeSendHeaders.addListener(e => {
        e = new URL(e.url);
        if ("en" !== e.searchParams.get("lang")) return e.searchParams.set("lang", "en"), {
            redirectUrl: e.toString()
        }
    }, {
        urls: ["*://*.funcaptcha.co/*", "*://*.funcaptcha.com/*", "*://*.arkoselabs.com/*", "*://*.arkoselabs.cn/*", "*://*.arkose.com.cn/*"],
        types: ["sub_frame"]
    }, ["blocking"])
}) : is_chrome && (bapi.VERSION = "chrome", bapi.browser = chrome, bapi.reconnect_scripts = () => {
    chrome.runtime.onInstalled.addListener(async () => {
        for (const e of chrome.runtime.getManifest().content_scripts)
            for (const t of await chrome.tabs.query({
                    url: e.matches
                })) chrome.scripting.executeScript({
                target: {
                    tabId: t.id
                },
                files: e.js
            })
    })
}, bapi.register_language = () => {
    chrome.declarativeNetRequest.updateDynamicRules({
        addRules: [{
            id: 1,
            priority: 1,
            action: {
                type: "redirect",
                redirect: {
                    transform: {
                        queryTransform: {
                            addOrReplaceParams: [{
                                key: "hl",
                                value: "en-US"
                            }]
                        }
                    }
                }
            },
            condition: {
                regexFilter: "^(http|https)://[^\\.]*\\.(google\\.com|recaptcha\\.net)/recaptcha",
                resourceTypes: ["sub_frame"]
            }
        }, {
            id: 2,
            priority: 1,
            action: {
                type: "redirect",
                redirect: {
                    transform: {
                        queryTransform: {
                            addOrReplaceParams: [{
                                key: "lang",
                                value: "en"
                            }]
                        }
                    }
                }
            },
            condition: {
                regexFilter: "^(http|https)://[^\\.]*\\.(funcaptcha\\.(co|com)|arkoselabs\\.(com|cn)|arkose\\.com\\.cn)",
                resourceTypes: ["sub_frame"]
            }
        }],
        removeRuleIds: [1, 2]
    })
});
class API {
    static endpoints = {};
    static register(e, t) {
        var a = e.name + "." + t;
        const r = e[t];
        this.endpoints[a] = function() {
            return r.apply(e, [{
                tab_id: arguments[0].tab_id,
                frame_id: arguments[0].frame_id,
                ...arguments[0].data
            }])
        }
    }
}
class Cache {
    static cache = {};
    static async set({
        tab_id: e,
        name: t,
        value: a,
        tab_specific: r = !1
    } = {}) {
        return r && (t = e + "_" + t), Cache.cache[t] = a, Cache.cache[t]
    }
    static async get({
        tab_id: e,
        name: t,
        tab_specific: a = !1
    } = {}) {
        return a && (t = e + "_" + t), Cache.cache[t]
    }
    static async remove({
        tab_id: e,
        name: t,
        tab_specific: a = !1
    } = {}) {
        a && (t = e + "_" + t);
        a = Cache.cache[t];
        return delete Cache.cache[t], a
    }
    static async append({
        tab_id: e,
        name: t,
        value: a,
        tab_specific: r = !1
    } = {}) {
        return (t = r ? e + "_" + t : t) in Cache.cache || (Cache.cache[t] = []), Cache.cache[t].push(a), Cache.cache[t]
    }
    static async empty({
        tab_id: e,
        name: t,
        tab_specific: a = !1
    } = {}) {
        a && (t = e + "_" + t);
        a = Cache.cache[t];
        return Cache.cache[t] = [], a
    }
    static async inc({
        tab_id: e,
        name: t,
        tab_specific: a = !1
    } = {}) {
        return (t = a ? e + "_" + t : t) in Cache.cache || (Cache.cache[t] = 0), Cache.cache[t]++, Cache.cache[t]
    }
    static async dec({
        tab_id: e,
        name: t,
        tab_specific: a = !1
    } = {}) {
        return (t = a ? e + "_" + t : t) in Cache.cache || (Cache.cache[t] = 0), Cache.cache[t]--, Cache.cache[t]
    }
    static async zero({
        tab_id: e,
        name: t,
        tab_specific: a = !1
    } = {}) {
        return a && (t = e + "_" + t), Cache.cache[t] = 0, Cache.cache[t]
    }
}
API.register(Cache, "set"), API.register(Cache, "get"), API.register(Cache, "remove"), API.register(Cache, "append"), API.register(Cache, "empty"), API.register(Cache, "inc"), API.register(Cache, "dec"), API.register(Cache, "zero");
class TC {
    static working = {};
    static data = {};
    static metrics = {
        hit: {},
        miss: {}
    };
    static get(e) {
        if (e in TC.data) {
            var t = TC.data[e];
            if (Time.time() / 1e3 - t.t < t.lifespan) return {
                s: !0,
                v: t.v
            };
            delete TC.data[e]
        }
        return {
            s: !1
        }
    }
    static set(e, t, a) {
        var r = Time.time() / 1e3;
        return TC.data[e] = {
            t: r,
            v: t,
            lifespan: a
        }, t
    }
    static purge(e) {
        delete TC.data[e], delete TC.working[e]
    }
    static ready(t) {
        return new Promise(async e => {
            for (; TC.working[t];) await Time.sleep(10);
            e()
        })
    }
    static async getset(e, t, a = 1) {
        await TC.ready(e);
        var r = TC.get(e);
        if (r.s) return e in TC.metrics.hit || (TC.metrics.hit[e] = 0), TC.metrics.hit[e]++, r.v;
        TC.working[e] = !0;
        try {
            e in TC.metrics.miss || (TC.metrics.miss[e] = 0), TC.metrics.miss[e]++;
            var s = await Promise.resolve(t());
            return TC.set(e, s, a), s
        } finally {
            delete TC.working[e]
        }
    }
}
setInterval(() => {
    TC.metrics = {
        hit: {},
        miss: {}
    };
    for (const e of Object.keys(TC.data)) TC.get(e)
}, 1e4);
class Settings {
    static data = {};
    static async _save() {
        try {
            await bapi.browser.storage.sync.set({
                settings: Settings.data
            })
        } catch (e) {
            return e
        }
    }
    static _get() {
        return TC.getset("Settings._get()", () => new Promise(t => {
            bapi.browser.storage.sync.get(["settings"], ({
                settings: e
            }) => {
                chrome.runtime.lastError;
                t(e)
            })
        }))
    }
    static async load() {
        Settings.data = await Settings._get() || await Settings.reset(), Settings.data.version !== SettingsManager.DEFAULT.version && await Settings.reset()
    }
    static get() {
        return Settings.data
    }
    static async set({
        id: e,
        value: t
    }) {
        Settings.data[e] = t, await Settings._save()
    }
    static async update({
        settings: e
    }) {
        for (var [t, a] of Object.entries(e)) Settings.data[t] = a;
        await Settings._save()
    }
    static async replace({
        settings: e
    }) {
        Settings.data = e, await Settings._save()
    }
    static async reset() {
        var e = Settings.data.key || "";
        return Settings.data = deep_copy(SettingsManager.DEFAULT), Settings.data.key = e, await Settings._save(), Settings.data
    }
}
API.register(Settings, "get"), API.register(Settings, "set"), API.register(Settings, "update"), API.register(Settings, "replace"), API.register(Settings, "reset");
class Net {
    static async fetch({
        url: e,
        options: t
    } = {
        options: {}
    }) {
        try {
			//console.log("========== e Net fetch ==========");
			//console.log(e);
			//console.log("========== t Net fetch ==========");
			//console.log(t);
            return await (await fetch(e, t)).text()
        } catch (e) {
            return null
        }
    }
}
API.register(Net, "fetch");
class Tab {
    static reloads = {};
    static _reload({
        tab_id: t
    }) {
        return new Promise(e => bapi.browser.tabs.reload(t, {
            bypassCache: !0
        }, e))
    }
    static async reload({
        tab_id: e,
        delay: t,
        overwrite: a
    } = {
        delay: 0,
        overwrite: !0
    }) {
        t = parseInt(t);
        var r = Tab.reloads[e]?.delay - (Date.now() - Tab.reloads[e]?.start),
            r = isNaN(r) || r < 0 ? 0 : r;
        return !!(a || 0 == r || t <= r) && (clearTimeout(Tab.reloads[e]?.timer), Tab.reloads[e] = {
            delay: t,
            start: Date.now(),
            timer: setTimeout(() => Tab._reload({
                tab_id: e
            }), t)
        }, !0)
    }
    static close({
        tab_id: t
    }) {
        return new Promise(e => bapi.browser.tabs.remove(t, e))
    }
    static open({
        url: t
    } = {
        url: null
    }) {
        return new Promise(e => bapi.browser.tabs.create({
            url: t
        }, e))
    }
    static navigate({
        tab_id: t,
        url: a
    }) {
        return new Promise(e => bapi.browser.tabs.update(t, {
            url: a
        }, e))
    }
    static active() {
        return new Promise(async t => {
            var e;
            if ("firefox" !== bapi.VERSION) return [e] = await bapi.browser.tabs.query({
                active: !0,
                lastFocusedWindow: !0
            }), t(e);
            bapi.browser.tabs.query({
                active: !0,
                lastFocusedWindow: !0
            }, ([e]) => {
                bapi.browser.runtime.lastError, t(e)
            })
        })
    }
    static _info({
        tab_id: a
    }) {
        return new Promise(async t => {
            if ("firefox" === bapi.VERSION) try {
                var e = await bapi.browser.tabs.get(a);
                t(e)
            } catch (e) {
                t(null)
            } else try {
                bapi.browser.tabs.get(a, e => t(e))
            } catch (e) {
                t(null)
            }
        })
    }
    static info({
        tab_id: e
    }) {
        return TC.getset(`Tab.info(${e})`, () => Tab._info({
            tab_id: e
        }))
    }
    static url({
        tab_id: t
    }) {
        return TC.getset(`Tab.url(${t})`, async () => {
            var e = await Tab.info({
                tab_id: t
            });
            return e && e.url ? e.url : null
        })
    }
    static hostname({
        tab_id: t
    }) {
        return TC.getset(`Tab.hostname(${t})`, async () => {
            var e = await Tab.url({
                tab_id: t
            }) || "Unknown Host";
            return Util.parse_hostname(e)
        })
    }
}
API.register(Tab, "reload"), API.register(Tab, "close"), API.register(Tab, "open"), API.register(Tab, "navigate"), API.register(Tab, "active"), API.register(Tab, "info"), API.register(Tab, "url"), API.register(Tab, "hostname");
class Inject {
    static async _inject(t) {
        t.target.tabId || (e = await Tab.active(), t.target.tabId = e.id);
        var e = new Promise(e => bapi.browser.scripting.executeScript(t, e));
        return e
    }
    static async func({
        tab_id: e,
        func: t,
        args: a
    } = {
        args: []
    }) {
        e = {
            target: {
                tabId: e,
                allFrames: !0
            },
            world: "MAIN",
            injectImmediately: !0,
            func: t,
            args: a
        };
        return Inject._inject(e)
    }
    static async files({
        tab_id: e,
        frame_id: t,
        files: a
    }) {
        e = {
            target: {
                tabId: e,
                frameIds: [t]
            },
            world: "MAIN",
            injectImmediately: !0,
            files: a
        };
        return "firefox" === bapi.VERSION && delete e.world, Inject._inject(e)
    }
    static async register({
        scripts: e
    }) {
        await chrome.scripting.registerContentScripts(e)
    }
    static async unregister() {
        await chrome.scripting.unregisterContentScripts()
    }
}
API.register(Inject, "func"), API.register(Inject, "files"), API.register(Inject, "register"), API.register(Inject, "unregister");
class Server {
    static ENDPOINT = BASE_API + "/status?v=" + bapi.browser.runtime.getManifest().version;
    static is_fetching_plan = !1;
    static async get_plan({
        key: e
    }) {
        if (Server.is_fetching_plan) return !1;
        Server.is_fetching_plan = !0;
        let t = {
            plan: "Unknown",
            credit: 0
        };
        try {
            "undefined" === e && (e = "");
            var a = await fetch(Server.ENDPOINT + "&key=" + e);
            t = JSON.parse(await a.text())
        } catch {}
        return Server.is_fetching_plan = !1, t
    }
}
API.register(Server, "get_plan");
class Image {
    static encode({
        url: e
    }) {
        return new Promise(a => {
            fetch(e).then(e => e.blob()).then(e => {
                const t = new FileReader;
                t.onload = () => a(t.result), t.readAsDataURL(e)
            })
        })
    }
}
API.register(Image, "encode");
class Relay {
    static async send({
        tab_id: e,
        data: t
    }) {
        e = e || (await Tab.active()).id, bapi.browser.tabs.sendMessage(e, t)
    }
}
API.register(Relay, "send");
class Icon {
    static set({
        status: a
    }) {
        return new Promise(e => {
            var t = "firefox" === bapi.VERSION ? bapi.browser.browserAction : bapi.browser.action;
            "on" === a ? t.setIcon({
                path: {
                    16: "/icon/16.png",
                    32: "/icon/32.png",
                    48: "/icon/48.png",
                    128: "/icon/128.png"
                }
            }, e) : "off" === a ? t.setIcon({
                path: {
                    16: "/icon/16g.png",
                    32: "/icon/32g.png",
                    48: "/icon/48g.png",
                    128: "/icon/128g.png"
                }
            }, e) : e(!1)
        })
    }
    static set_badge_text({
        tab_id: a,
        data: r
    }) {
        return new Promise(e => {
            var t = {
                text: r
            };
            a && (t.tabId = a), bapi.browser.action.setBadgeText(t, e)
        })
    }
    static set_badge_color({
        tab_id: a,
        data: r
    }) {
        return new Promise(e => {
            var t = {
                color: r
            };
            a && (t.tabId = a), bapi.browser.action.setBadgeBackgroundColor(t, e)
        })
    }
    static async set_badge({
        tab_id: e,
        data: {
            global: t,
            text: a,
            color: r
        }
    }) {
        e || t || (e = (await Tab.active()).id), t && (e = null);
        t = [Icon.set_badge_text({
            tab_id: e,
            data: a
        })];
        return r && t.push(Icon.set_badge_color({
            tab_id: e,
            data: r
        })), Promise.all(t)
    }
}
API.register(Icon, "set");
class Browser {
    static dl_options = null;
    static async version() {
        return bapi.VERSION
    }
    static async log() {}
    static async upload({
        data: e
    }) {
        Browser.dl_options = e
    }
    static async download({
        frame_id: e
    }) {
        if (0 === e) return Browser.dl_options
    }
}
API.register(Browser, "version"), API.register(Browser, "log"), API.register(Browser, "upload"), API.register(Browser, "download");
class ContextMenu {
    static listen() {
        bapi.browser.contextMenus.onClicked.addListener(function(t, e) {
            if ("nopecha_disable_host" === t.menuItemId) {
                t = t.pageUrl;
                if (t) {
                    t = Util.parse_hostname(t);
                    let e = new Set;
                    for (const a of Settings.data.disabled_hosts) e.add(a.trim());
                    e.add(t), e = [...e], Settings.set({
                        id: "disabled_hosts",
                        value: e
                    })
                }
            }
        })
    }
    static create() {
        bapi.browser.contextMenus.create({
            title: "Disable CaptCha69 on this site",
            id: "nopecha_disable_host"
        })
    }
}
bapi.browser.runtime.onInstalled.addListener(ContextMenu.create), ContextMenu.listen();
class Debugger {
    static VERSION = "1.3";
    static tabs = [];
    static initialized = !1;
    static _initialize() {
        Debugger.initialized || (chrome.debugger.onEvent.addListener((e, t, a) => {}), Debugger.initialized = !0)
    }
    static _on_detach(e) {
        e = Debugger.tabs.indexOf(e); - 1 !== e && Debugger.tabs.splice(e, 1)
    }
    static attach({
        tab_id: t
    }) {
        return Debugger._initialize(), new Promise(e => {
            if (Debugger.tabs.includes(t)) return e(!1);
            Debugger.tabs.push(t), chrome.debugger.attach({
                tabId: t
            }, Debugger.VERSION, async () => {
                e(!0)
            })
        })
    }
    static detach({
        tab_id: t
    }) {
        return new Promise(e => {
            if (!Debugger.tabs.includes(t)) return e(!1);
            chrome.debugger.detach({
                tabId: t
            }, () => {
                Debugger._on_detach(t), e(!0)
            })
        })
    }
    static command({
        tab_id: t,
        method: a,
        params: r
    } = {
        params: null
    }) {
        return new Promise(e => {
            chrome.debugger.sendCommand({
                tabId: t
            }, a, r, e)
        })
    }
}

function listen_setup() {
    bapi.browser.webRequest.onBeforeRequest.addListener(e => {
        try {
            var t, a, r = e.url.split("#");
            2 <= r.length && (r.shift(), t = "#" + r.join("#"), a = SettingsManager.import(t), Settings.update({
                settings: a
            }))
        } catch (e) {}
    }, {
        urls: ["*://*.captcha69.com/setup*"]
    })
}
API.register(Debugger, "attach"), API.register(Debugger, "detach"), API.register(Debugger, "command"), (async () => {
    listen_setup(), bapi.register_language(), await Settings.load(), await Icon.set({
        status: Settings.data.enabled ? "on" : "off"
    }), bapi.browser.runtime.onMessage.addListener((e, t, a) => {
        const r = e[0];
        let s = null;
        e = (s = 1 < e.length ? 2 === e.length ? e[1] : e.slice(1) : s) && "tab_id" in s ? s.tab_id : t?.tab?.id, t = t?.frameId;
        try {
            Promise.resolve(API.endpoints[r]({
                tab_id: e,
                frame_id: t,
                data: s
            })).then(e => {
                ["Browser.log", "Settings.get", "Settings.set", "Cache.get", "Cache.set", "Tab.info", "Tab.hostname"].includes(r);
                try {
                    a(e)
                } catch (e) {}
            }).catch(e => {})
        } catch (e) {}
        return !0
    })
})();