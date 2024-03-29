(async () => {
    var t, e;

    function n() {
        try {
            return window.self !== window.top
        } catch (t) {
            return 1
        }
    }
    t = self, e = () => (() => {
        "use strict";
        var r, c, t, i = {
                d: (t, e) => {
                    for (var n in e) i.o(e, n) && !i.o(t, n) && Object.defineProperty(t, n, {
                        enumerable: !0,
                        get: e[n]
                    })
                },
                o: (t, e) => Object.prototype.hasOwnProperty.call(t, e),
                r: t => {
                    "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, {
                        value: "Module"
                    }), Object.defineProperty(t, "__esModule", {
                        value: !0
                    })
                }
            },
            e = {};

        function l(t) {
            return t && t instanceof Element
        }
        i.r(e), i.d(e, {
            default: () => V,
            getCssSelector: () => L
        }), (t = r = r || {}).NONE = "none", t.DESCENDANT = "descendant", t.CHILD = "child", (t = c = c || {}).id = "id", t.class = "class", t.tag = "tag", t.attribute = "attribute", t.nthchild = "nthchild", t.nthoftype = "nthoftype";
        const h = {
            selectors: [c.id, c.class, c.tag, c.attribute],
            includeTag: !1,
            whitelist: [],
            blacklist: [],
            combineWithinSelector: !0,
            combineBetweenSelectors: !0,
            root: null,
            maxCombinations: Number.POSITIVE_INFINITY,
            maxCandidates: Number.POSITIVE_INFINITY
        };

        function o(t) {
            return t instanceof RegExp
        }

        function n(t) {
            return ["string", "function"].includes(typeof t) || o(t)
        }

        function u(t) {
            return Array.isArray(t) ? t.filter(n) : []
        }

        function s(t) {
            var e = [Node.DOCUMENT_NODE, Node.DOCUMENT_FRAGMENT_NODE, Node.ELEMENT_NODE];
            return t instanceof Node && e.includes(t.nodeType)
        }

        function p(t, e) {
            return s(t) ? (t.contains(e), t) : s(t = e.getRootNode({
                composed: !1
            })) ? (document, t) : e.ownerDocument.querySelector(":root")
        }

        function f(t) {
            return "number" == typeof t ? t : Number.POSITIVE_INFINITY
        }

        function m(t = []) {
            var [t = [], ...e] = t;
            return 0 === e.length ? t : e.reduce((t, e) => t.filter(t => e.includes(t)), t)
        }

        function g(t) {
            return [].concat(...t)
        }

        function E(t) {
            const n = t.map(e => {
                if (o(e)) return t => e.test(t);
                if ("function" == typeof e) return t => {
                    t = e(t);
                    return "boolean" == typeof t && t
                };
                if ("string" != typeof e) return () => !1;
                {
                    const n = new RegExp("^" + e.replace(/[|\\{}()[\]^$+?.]/g, "\\$&").replace(/\*/g, ".+") + "$");
                    return t => n.test(t)
                }
            });
            return e => n.some(t => t(e))
        }

        function _(t, e, n) {
            const i = Array.from(p(n, t[0]).querySelectorAll(e));
            return i.length === t.length && t.every(t => i.includes(t))
        }

        function b(t, e) {
            e = null != e ? e : t.ownerDocument.querySelector(":root");
            var n = [];
            let i = t;
            for (; l(i) && i !== e;) n.push(i), i = i.parentElement;
            return n
        }
        const a = {
                [r.NONE]: {
                    type: r.NONE,
                    value: ""
                },
                [r.DESCENDANT]: {
                    type: r.DESCENDANT,
                    value: " > "
                },
                [r.CHILD]: {
                    type: r.CHILD,
                    value: " "
                }
            },
            d = new RegExp(["^$", "\\s"].join("|")),
            A = new RegExp(["^$"].join("|")),
            $ = [c.nthoftype, c.tag, c.id, c.class, c.attribute, c.nthchild],
            y = E(["class", "id", "ng-*"]);

        function x({
            nodeName: t
        }) {
            return `[${t}]`
        }

        function S({
            nodeName: t,
            nodeValue: e
        }) {
            return `[${t}='${T(e)}']`
        }

        function w(n) {
            var t = Array.from(n.attributes).filter(t => {
                var [t, e] = [t.nodeName, n];
                return e = e.tagName.toLowerCase(), !(["input", "option"].includes(e) && "value" === t || y(t))
            });
            return [...t.map(x), ...t.map(S)]
        }

        function N(t) {
            return (t.getAttribute("class") || "").trim().split(/\s+/).filter(t => !A.test(t)).map(t => "." + T(t))
        }

        function v(t) {
            var e = t.getAttribute("id") || "",
                n = "#" + T(e),
                i = t.getRootNode({
                    composed: !1
                });
            return !d.test(e) && _([t], n, i) ? [n] : []
        }

        function C(t) {
            var e = t.parentNode;
            if (e) {
                e = Array.from(e.childNodes).filter(l).indexOf(t);
                if (-1 < e) return [`:nth-child(${e+1})`]
            }
            return []
        }

        function M(t) {
            return [T(t.tagName.toLowerCase())]
        }

        function P(t) {
            t = [...new Set(g(t.map(M)))];
            return 0 === t.length || 1 < t.length ? [] : [t[0]]
        }

        function O(t) {
            const e = P([t])[0],
                n = t.parentElement;
            if (n) {
                t = Array.from(n.children).filter(t => t.tagName.toLowerCase() === e).indexOf(t);
                if (-1 < t) return [e + `:nth-of-type(${t+1})`]
            }
            return []
        }

        function k(e = [], {
            maxResults: t = Number.POSITIVE_INFINITY
        } = {}) {
            var n = [];
            let i = 0,
                r = I(1);
            for (; r.length <= e.length && i < t;) i += 1, n.push(r.map(t => e[t])), r = function(t = [], e) {
                var n = t.length;
                if (0 === n) return [];
                var i = [...t];
                i[n - 1] += 1;
                for (let t = n - 1; 0 <= t; t--)
                    if (i[t] > e) {
                        if (0 === t) return I(n + 1);
                        i[t - 1]++, i[t] = i[t - 1] + 1
                    } return e < i[n - 1] ? I(n + 1) : i
            }(r, e.length - 1);
            return n
        }

        function I(t = 1) {
            return Array.from(Array(t).keys())
        }
        const R = ":".charCodeAt(0).toString(16).toUpperCase(),
            D = /[ !"#$%&'()\[\]{|}<>*+,./;=?@^`~\\]/;

        function T(t = "") {
            var e;
            return null != (e = null == (e = null === CSS || void 0 === CSS ? void 0 : CSS.escape) ? void 0 : e.call(CSS, t)) ? e : ([e = ""] = [t], e.split("").map(t => ":" === t ? `\\${R} ` : D.test(t) ? "\\" + t : escape(t).replace(/%/g, "\\")).join(""))
        }
        const j = {
                tag: P,
                id: function(t) {
                    return 0 === t.length || 1 < t.length ? [] : v(t[0])
                },
                class: function(t) {
                    return m(t.map(N))
                },
                attribute: function(t) {
                    return m(t.map(w))
                },
                nthchild: function(t) {
                    return m(t.map(C))
                },
                nthoftype: function(t) {
                    return m(t.map(O))
                }
            },
            H = {
                tag: M,
                id: v,
                class: N,
                attribute: w,
                nthchild: C,
                nthoftype: O
            };

        function B(t) {
            return t.includes(c.tag) || t.includes(c.nthoftype) ? [...t] : [...t, c.tag]
        }

        function U(e = {}) {
            var t = [...$];
            return e[c.tag] && e[c.nthoftype] && t.splice(t.indexOf(c.tag), 1), t.map(t => {
                return e[t = t] ? e[t].join("") : ""
            }).join("")
        }

        function J(t, e, n = "", i) {
            var r, o, s, a, d;
            i.root, s = function(a, n) {
                const {
                    blacklist: t,
                    whitelist: e,
                    combineWithinSelector: d,
                    maxCombinations: c
                } = n, l = E(t), h = E(e);
                return function() {
                    var {
                        selectors: t,
                        includeTag: e
                    } = n, t = [].concat(t);
                    return e && !t.includes("tag") && t.push("tag"), t
                }().reduce((t, e) => {
                    o = a, s = e;
                    var n, i, r, o, s = (null != (s = j[s]) ? s : () => [])(o),
                        s = ([o = [], i, r] = [s, l, h], o.filter(t => r(t) || !i(t))),
                        s = ([o = [], n] = [s, h], o.sort((t, e) => {
                            t = n(t), e = n(e);
                            return t && !e ? -1 : !t && e ? 1 : 0
                        }));
                    return t[e] = d ? k(s, {
                        maxResults: c
                    }) : s.map(t => [t]), t
                }, {})
            }(t, o = i), a = s, d = o, s = g(function() {
                var {
                    selectors: t,
                    combineBetweenSelectors: e,
                    includeTag: n,
                    maxCandidates: i
                } = d, e = e ? k(t, {
                    maxResults: i
                }) : t.map(t => [t]);
                return n ? e.map(B) : e
            }().map(t => {
                {
                    var n = a;
                    const i = {};
                    return t.forEach(t => {
                            var e = n[t];
                            0 < e.length && (i[t] = e)
                        }),
                        function(t = {}) {
                            let i = [];
                            return Object.entries(t).forEach(([n, t]) => {
                                i = t.flatMap(e => 0 === i.length ? [{
                                    [n]: e
                                }] : i.map(t => Object.assign(Object.assign({}, t), {
                                    [n]: e
                                })))
                            }), i
                        }(i).map(U)
                }
            }).filter(t => 0 < t.length)), o = [...new Set(s)];
            for (const e of "" === n ? o : (r = n, [...(o = o).map(t => r + " " + t), ...o.map(t => r + " > " + t)]))
                if (_(t, e, i.root)) return e;
            return null
        }

        function z(t) {
            return {
                value: t,
                include: !1
            }
        }

        function G({
            selectors: e,
            operator: t
        }) {
            let n = [...$],
                i = (e[c.tag] && e[c.nthoftype] && (n = n.filter(t => t !== c.tag)), "");
            return n.forEach(t => {
                (e[t] || []).forEach(({
                    value: t,
                    include: e
                }) => {
                    e && (i += t)
                })
            }), t.value + i
        }

        function F(t) {
            return [":root", ...b(t).reverse().map(t => {
                t = function(n, t, e = r.NONE) {
                    const i = {};
                    return t.forEach(t => {
                        var e;
                        Reflect.set(i, t, (e = n, t = t, H[t](e).map(z)))
                    }), {
                        element: n,
                        operator: a[e],
                        selectors: i
                    }
                }(t, [c.nthchild], r.DESCENDANT);
                return t.selectors.nthchild.forEach(t => {
                    t.include = !0
                }), t
            }).map(G)].join("")
        }

        function L(t, e = {}) {
            const o = function(t) {
                    t = (Array.isArray(t) ? t : [t]).filter(l);
                    return [...new Set(t)]
                }(t),
                s = ([t, e = {}] = [o[0], e], e = Object.assign(Object.assign({}, h), e), {
                    selectors: (n = e.selectors, Array.isArray(n) ? n.filter(t => {
                        return e = c, t = t, Object.values(e).includes(t);
                        var e
                    }) : []),
                    whitelist: u(e.whitelist),
                    blacklist: u(e.blacklist),
                    root: p(e.root, t),
                    combineWithinSelector: !!e.combineWithinSelector,
                    combineBetweenSelectors: !!e.combineBetweenSelectors,
                    includeTag: !!e.includeTag,
                    maxCombinations: f(e.maxCombinations),
                    maxCandidates: f(e.maxCandidates)
                });
            var n;
            let a = "",
                d = s.root;

            function i() {
                var [t, e, n = "", i] = [o, d, a, s];
                if (0 !== t.length) {
                    var r, e = [1 < t.length ? t : [], ...(r = e, m(t.map(t => b(t, r))).map(t => [t]))];
                    for (const t of e) {
                        const e = J(t, 0, n, i);
                        if (e) return {
                            foundElements: t,
                            selector: e
                        }
                    }
                }
                return null
            }
            let r = i();
            for (; r;) {
                const {
                    foundElements: t,
                    selector: c
                } = r;
                if (_(o, c, s.root)) return c;
                d = t[0], a = c, r = i()
            }
            return (1 < o.length ? o.map(t => L(t, s)) : o.map(F)).join(", ")
        }
        const V = L;
        return e
    })(), "object" == typeof exports && "object" == typeof module ? module.exports = e() : "function" == typeof define && define.amd ? define([], e) : "object" == typeof exports ? exports.CssSelectorGenerator = e() : t.CssSelectorGenerator = e();
    class r {
        constructor(t, e = !1) {
            this.NAMESPACE = "__NOPECHA__", this.MARK_RADIUS = 5, this.window_id = Util.generate_id(8), this.locate = t, this.draw_mark = e, this.update_timer, this.css_selector, this.$last, this.initialize_style(), this.initialize_elements()
        }
        initialize_style() {
            var t = [`#${this.NAMESPACE}_wrapper {
                    position: fixed;
                    top: 0;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    background-color: transparent;
                    pointer-events: none;
                    z-index: 10000000;
                }`, `.${this.NAMESPACE}_textbox {
                    display: flex;
                    flex-direction: row;
                    flex-wrap: wrap;

                    position: absolute;
                    left: 0;
                    right: 0;

                    background-color: #222;
                    color: #fff;
                    font: normal 12px/12px Helvetica, sans-serif;
                    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.3);
                    border: 1px solid #fff;
                    overflow: hidden;
                }`, `.${this.NAMESPACE}_textbox.${this.NAMESPACE}_header {
                    top: 0;
                }`, `.${this.NAMESPACE}_textbox.${this.NAMESPACE}_header > div {
                    padding: 4px 8px;
                }`, `.${this.NAMESPACE}_textbox.${this.NAMESPACE}_header > div:first-child {
                    flex-grow: 1;
                }`, `.${this.NAMESPACE}_textbox.${this.NAMESPACE}_footer {
                    bottom: 0;
                }`, `.${this.NAMESPACE}_textbox.${this.NAMESPACE}_footer > div {
                    padding: 4px 8px;
                }`, `.${this.NAMESPACE}_textbox.${this.NAMESPACE}_footer > div:first-child {
                    flex-grow: 1;
                }`, `.${this.NAMESPACE}_highlight {
                    position: absolute;
                    opacity: 0.4;
                }`, `.${this.NAMESPACE}_highlight.${this.NAMESPACE}_margin {
                    background-color: rgb(230, 165, 18);
                }`, `.${this.NAMESPACE}_highlight.${this.NAMESPACE}_border {
                    background-color: rgb(255, 204, 121);
                }`, `.${this.NAMESPACE}_highlight.${this.NAMESPACE}_padding {
                    background-color: rgb(50, 255, 50);
                }`, `.${this.NAMESPACE}_highlight.${this.NAMESPACE}_content {
                    background-color: rgb(0, 153, 201);
                }`, `.${this.NAMESPACE}_mark {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;

                    width: ${parseInt(2*this.MARK_RADIUS)}px;
                    height: ${parseInt(2*this.MARK_RADIUS)}px;
                    background-color: #f44;
                    border-radius: 50%;
                    z-index: 2;
                }`];
            n() || t.push(`.${this.NAMESPACE}_shadow {
                    position: fixed;
                    top: 0;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    background-color: rgba(255, 255, 255, 0.1);
                    pointer-events: none;
                    z-index: 1;
                }`), this.$style = document.createElement("style"), this.$style.type = "text/css", this.$style.styleSheet ? this.$style.styleSheet.cssText = t.join("\n") : this.$style.innerHTML = t.join("\n"), document.getElementsByTagName("head")[0].appendChild(this.$style)
        }
        initialize_elements() {
            var t;
            this.$wrapper = document.createElement("div"), this.$wrapper.id = this.NAMESPACE + "_wrapper", document.body.append(this.$wrapper), this.$shadow = document.createElement("div"), this.$shadow.classList.add(this.NAMESPACE + "_shadow"), this.$wrapper.append(this.$shadow), this.$margin_box = document.createElement("div"), this.$margin_box.classList.add(this.NAMESPACE + "_highlight", this.NAMESPACE + "_margin"), this.$wrapper.append(this.$margin_box), this.$border_box = document.createElement("div"), this.$border_box.classList.add(this.NAMESPACE + "_highlight", this.NAMESPACE + "_border"), this.$wrapper.append(this.$border_box), this.$padding_box = document.createElement("div"), this.$padding_box.classList.add(this.NAMESPACE + "_highlight", this.NAMESPACE + "_padding"), this.$wrapper.append(this.$padding_box), this.$content_box = document.createElement("div"), this.$content_box.classList.add(this.NAMESPACE + "_highlight", this.NAMESPACE + "_content"), this.$wrapper.append(this.$content_box), n() || (this.$header = document.createElement("div"), this.$header.classList.add(this.NAMESPACE + "_textbox", this.NAMESPACE + "_header"), t = "textcaptcha_image_selector" === this.locate ? "<b>Image</b>" : "<b>Input</b>", this.$header.innerHTML = `
                    <div>
                        <div>Click on the CAPTCHA ${t} element to generate a CSS selector.</div>
                        <div>Press <b>ESC</b> to cancel.</div>
                    </div>
                    <div><b>CaptCha69</b></div>
                `, this.$wrapper.append(this.$header), this.$footer = document.createElement("div"), this.$footer.classList.add(this.NAMESPACE + "_textbox", this.NAMESPACE + "_footer"), this.$wrapper.append(this.$footer)), this.draw_mark && (this.$mark = document.createElement("div"), this.$mark.classList.add(this.NAMESPACE + "_mark"), this.$wrapper.append(this.$mark))
        }
        clip(t) {
            var e = {
                top: Math.max(0, t.top),
                left: Math.max(0, t.left),
                width: t.width + t.left > window.innerWidth ? window.innerWidth - t.left : t.width,
                height: t.height + t.top > window.innerHeight ? window.innerHeight - t.top : t.height
            };
            return t.top < 0 && (e.height += t.top), t.left < 0 && (e.width += t.left), e.width < 0 && (e.width = 0), e.height < 0 && (e.height = 0), e
        }
        computed_style(t, e) {
            let n = window.getComputedStyle(t).getPropertyValue(e);
            for (const i in n = n.match(/[\-]?[\d\.]+px/g)) n[i] = parseFloat(n[i].replace("px", ""));
            return 1 === n.length && n.push(n[0], n[0], n[0]), 2 === n.length && n.push(n[0], n[1]), 3 === n.length && n.push(n[1]), n
        }
        add_dim(t, e) {
            for (const n of e) t.top -= n[0], t.left -= n[3], t.width += n[1] + n[3], t.height += n[0] + n[2];
            return t
        }
        sub_dim(t, e) {
            for (const n of e) t.top += n[0], t.left += n[3], t.width -= n[1] + n[3], t.height -= n[0] + n[2];
            return t
        }
        set_dim(t, e) {
            e = this.clip(e);
            t.style.top = e.top + "px", t.style.left = e.left + "px", t.style.width = e.width + "px", t.style.height = e.height + "px"
        }
        get_center(t) {
            t = t.getBoundingClientRect();
            return {
                x: t.left + t.width / 2,
                y: t.top + t.height / 2
            }
        }
        get_css() {
            return window.CssSelectorGenerator.getCssSelector(this.$t)
        }
        clear() {
            this.$t = null;
            var t = {
                top: 0,
                left: 0,
                width: 0,
                height: 0
            };
            this.set_dim(this.$margin_box, t), this.set_dim(this.$border_box, t), this.set_dim(this.$padding_box, t), this.set_dim(this.$content_box, t), this.draw_mark && (this.$mark.style.top = "0px", this.$mark.style.left = "0px")
        }
        update(a, t = 0) {
            const d = this;
            d.$last && d.$last === a || (a && (d.$t = a), d.$t && (clearTimeout(d.update_timer), d.update_timer = setTimeout(() => {
                var t, e, n, i, r, o, s;
                d.$t?.getBoundingClientRect && (r = d.$t.getBoundingClientRect(), o = d.computed_style(d.$t, "margin"), s = d.computed_style(d.$t, "border-width"), t = d.computed_style(d.$t, "padding"), r = {
                    top: r.top,
                    left: r.left,
                    width: r.width,
                    height: r.height
                }, e = JSON.parse(JSON.stringify(r)), n = JSON.parse(JSON.stringify(r)), i = JSON.parse(JSON.stringify(r)), r = JSON.parse(JSON.stringify(r)), d.add_dim(e, [o]), d.sub_dim(i, [s]), d.sub_dim(r, [s, t]), d.set_dim(d.$margin_box, e), d.set_dim(d.$border_box, n), d.set_dim(d.$padding_box, i), d.set_dim(d.$content_box, r), o = d.get_css(d.$t), d.update_css_selector(d.window_id, o), BG.exec("Relay.send", {
                    data: {
                        action: "update_locate",
                        window_id: d.window_id,
                        css_selector: o
                    }
                }), d.draw_mark) && (s = d.get_center(a), d.$mark.style.top = parseInt(s.y - d.MARK_RADIUS) + "px", d.$mark.style.left = parseInt(s.x - d.MARK_RADIUS) + "px")
            }, t)))
        }
        update_css_selector(t, e) {
            this.window_id !== t && this.clear(), n() || (this.$footer.innerHTML = `<div>${e}</div>`)
        }
        terminate() {
            clearTimeout(this.update_timer), this.$style.remove(), this.$wrapper.remove()
        }
    }
    let o = null;

    function s(t) {
        t = t.target, t = o.get_css(t);
        BG.exec("Settings.set", {
            id: o.locate,
            value: t
        }), l(!0)
    }

    function a(t) {
        t = t.target;
        o.update(t)
    }

    function d(t) {
        o.update()
    }

    function c(t) {
        t = t || window.event;
        let e = !1;
        (e = "key" in t ? "Escape" === t.key || "Esc" === t.key : 27 === t.keyCode) && l(!0)
    }

    function l(t) {
        try {
            document.body.removeEventListener("click", s), document.body.removeEventListener("mousemove", a), document.body.removeEventListener("mousewheel", d), document.body.removeEventListener("keydown", c), o.terminate(), o = null
        } catch (t) {}
        t && BG.exec("Relay.send", {
            data: {
                action: "stop_locate"
            }
        })
    }
    chrome.runtime.onMessage.addListener((t, e, n) => {
        var i;
        "start_locate" === t.action ? (i = t.locate, o = new r(i), document.body.addEventListener("click", s), document.body.addEventListener("mousemove", a), document.body.addEventListener("mousewheel", d), document.body.addEventListener("keydown", c)) : "stop_locate" === t.action ? l(!1) : "update_locate" === t.action && o.update_css_selector(t.window_id, t.css_selector)
    })
})();