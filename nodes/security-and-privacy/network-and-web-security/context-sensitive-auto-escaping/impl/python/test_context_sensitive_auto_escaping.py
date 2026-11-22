# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/context-sensitive-auto-escaping/. The authors are listed in prov/ZZYC2R.jsonl.

import random
import re

import pytest

from context_sensitive_auto_escaping import (
    TEXT,
    Context,
    EscapeError,
    auto_escape,
    escape_html,
    filter_url,
    render,
    transition,
)

# ------------------------------------------------------------ an independent parser
# The oracle parses the rendered output with its own small tokenizer (regular
# expressions, written apart from the state machine of the code under test). It
# turns a document into tokens with decoded data: text runs, start tags with
# decoded attribute values, end tags, script code runs and decoded script strings.

START_TAG = re.compile(r"<([a-z][a-z0-9]*)((?: +[a-z][a-z-]*(?:=\"[^\"]*\"|='[^']*')?)*) *>")
ATTR = re.compile(r" +([a-z][a-z-]*)(?:=\"([^\"]*)\"|='([^']*)')?")
END_TAG = re.compile(r"</([a-z][a-z0-9]*)>")


def html_unescape(s: str) -> str:
    return (
        s.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
        .replace("&amp;", "&")
    )


def js_decode(body: str) -> str:
    units: list[int] = []
    k = 0
    while k < len(body):
        if body[k] == "\\":
            if body[k + 1] == "u":
                units.append(int(body[k + 2 : k + 6], 16))
                k += 6
            else:
                units.append(ord(body[k + 1]))
                k += 2
        else:
            raw16 = body[k].encode("utf-16-be")
            units.extend(int.from_bytes(raw16[j : j + 2], "big") for j in range(0, len(raw16), 2))
            k += 1
    raw = b"".join(u.to_bytes(2, "big") for u in units)
    return raw.decode("utf-16-be", "surrogatepass")


def parse_script(src: str) -> list:
    toks = []
    code = []
    k = 0
    while k < len(src):
        ch = src[k]
        if ch in "\"'":
            if code:
                toks.append(("js_code", "".join(code)))
                code = []
            j = k + 1
            while src[j] != ch:
                j += 2 if src[j] == "\\" else 1
            toks.append(("js_str", js_decode(src[k + 1 : j])))
            k = j + 1
        else:
            code.append(ch)
            k += 1
    if code:
        toks.append(("js_code", "".join(code)))
    return toks


def parse(doc: str) -> list:
    toks = []
    k = 0
    while k < len(doc):
        if doc.startswith("</", k):
            m = END_TAG.match(doc, k)
            assert m, doc[k:]
            toks.append(("end", m.group(1)))
            k = m.end()
        elif doc[k] == "<":
            m = START_TAG.match(doc, k)
            assert m, doc[k:]
            attrs = tuple(
                (a.group(1), html_unescape(a.group(2) if a.group(2) is not None else (a.group(3) or "")))
                for a in ATTR.finditer(m.group(2))
            )
            toks.append(("start", m.group(1), attrs))
            k = m.end()
            if m.group(1) == "script":
                j = doc.index("</script>", k)
                toks.extend(parse_script(doc[k:j]))
                toks.append(("end", "script"))
                k = j + len("</script>")
        else:
            j = doc.find("<", k)
            j = len(doc) if j < 0 else j
            toks.append(("text", html_unescape(doc[k:j])))
            k = j
    return toks


# ------------------------------------------------------------ the oracle

SENTINEL = "\u00a7"


def pct(v: str) -> str:
    keep = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")
    return "".join(chr(b) if chr(b) in keep else "%{:02X}".format(b) for b in v.encode())


def expected_url_start(v: str) -> str:
    m = re.match(r"([^/?#:]*):", v)
    if m and m.group(1).lower() not in ("http", "https", "mailto"):
        return "about:invalid"
    return v


def print_sequence(template: list, env: dict) -> list:
    seq = []
    for t in template:
        if t[0] == "print":
            seq.append(env[t[1]])
        elif t[0] == "if":
            seq.extend(print_sequence(t[2] if env[t[1]] else t[3], env))
        elif t[0] == "loop":
            for _ in range(env[t[1]]):
                seq.extend(print_sequence(t[2], env))
    return seq


def expected_tokens(sentinel_toks: list, values: list) -> list:
    """Put the expected decoded value of each hole where its sentinel is."""
    vals = iter(values)

    def sub(s: str, url: bool) -> str:
        if url:  # after the start of a URL the sentinel is percent-encoded
            s = s[:1] + s[1:].replace(pct(SENTINEL), SENTINEL)
        out = []
        for pos, ch in enumerate(s):
            if ch != SENTINEL:
                out.append(ch)
                continue
            v = next(vals)
            if url:
                out.append(expected_url_start(v) if pos == 0 else pct(v))
            else:
                out.append(v)
        return "".join(out)

    res = []
    for tok in sentinel_toks:
        if tok[0] == "start":
            res.append(("start", tok[1], tuple((a, sub(v, a in ("href", "src"))) for a, v in tok[2])))
        elif tok[0] == "text":
            s = sub(tok[1], False)
            if s:  # a text run of empty values leaves no text in the output
                res.append(("text", s))
        elif tok[0] == "js_str":
            res.append(("js_str", sub(tok[1], False)))
        elif tok[0] == "js_code":
            assert SENTINEL not in tok[1]
            res.append(tok)
        else:
            res.append(tok)
    assert next(vals, None) is None
    return res


def check_template(template: list, env: dict, escaped: list) -> None:
    """Data stays data: the rendered output parses to the same tokens as the
    sentinel rendering, and each hole decodes back to its value."""
    sentinel_env = {k: (SENTINEL if isinstance(v, str) else v) for k, v in env.items()}
    sentinel_toks = parse(render(escaped, sentinel_env))
    real_toks = parse(render(escaped, env))
    assert real_toks == expected_tokens(sentinel_toks, print_sequence(template, env))


# ------------------------------------------------------------ generators

TEXT_WORDS = ["ab", " ", "x > y", "1 2", "Q:", '"q"', "it's", "a/b"]
VALUE_WORDS = ["ab", " ", "c d", "1-2", "x/y"]
URL_WORDS = ["/a", "/p?q=", "#top", "http://example.com/"]
JS_WORDS = ["ab", " ", "c d"]
ALPHABET = "ab01<>&\"' \\:/=?#"


def gen_value(rng: random.Random) -> str:
    r = rng.random()
    if r < 0.15:
        return rng.choice(["http://example.org/a", "mailto:a", "ab:c", "/x?y=1", "HTTPS:b", ""])
    return "".join(rng.choice(ALPHABET) for _ in range(rng.randrange(6)))


def gen_attr_value(rng: random.Random, name: str, quote: str) -> list:
    nodes: list = []
    words = URL_WORDS if name in ("href", "src") else VALUE_WORDS
    for _ in range(rng.randrange(3)):
        if rng.random() < 0.5:
            nodes.append(("print", rng.choice("xyz")))
        else:
            nodes.append(("text", rng.choice(words)))
    return [("text", f" {name}={quote}")] + nodes + [("text", quote)]


def gen_script(rng: random.Random) -> list:
    nodes: list = [("text", "<script>")]
    for _ in range(rng.randrange(1, 3)):
        if rng.random() < 0.5:
            nodes += [("text", "var a = "), ("print", rng.choice("xyz")), ("text", "; ")]
        else:
            q = rng.choice("\"'")
            nodes.append(("text", "var b = " + q))
            for _ in range(rng.randrange(3)):
                nodes.append(("print", rng.choice("xyz")) if rng.random() < 0.5 else ("text", rng.choice(JS_WORDS)))
            nodes.append(("text", q + "; "))
    nodes.append(("text", "</script>"))
    return nodes


def gen_element(rng: random.Random, depth: int) -> list:
    if rng.random() < 0.2:
        return gen_script(rng)
    tag = rng.choice(["p", "div", "a", "span"])
    nodes: list = [("text", "<" + tag)]
    for name in rng.sample(["title", "href", "class", "src"], rng.randrange(3)):
        nodes += gen_attr_value(rng, name, rng.choice("\"'"))
    nodes.append(("text", ">"))
    nodes += gen_content(rng, depth - 1)
    nodes.append(("text", f"</{tag}>"))
    return nodes


def gen_content(rng: random.Random, depth: int) -> list:
    nodes: list = []
    for _ in range(rng.randrange(4 if depth > 0 else 2)):
        r = rng.random()
        if r < 0.3:
            nodes.append(("text", rng.choice(TEXT_WORDS)))
        elif r < 0.55:
            nodes.append(("print", rng.choice("xyz")))
        elif r < 0.8 and depth > 0:
            nodes += gen_element(rng, depth)
        elif r < 0.9 and depth > 0:
            nodes.append(("if", rng.choice("pq"), gen_content(rng, depth - 1), gen_content(rng, depth - 1)))
        elif depth > 0:
            nodes.append(("loop", "n", gen_content(rng, depth - 1)))
    return nodes


def gen_env(rng: random.Random) -> dict:
    env = {v: gen_value(rng) for v in "xyz"}
    env.update({b: rng.random() < 0.5 for b in "pq"})
    env["n"] = rng.randrange(3)
    return env


# ------------------------------------------------------------ tests

EXAMPLE = [
    ("text", "<p title=\""),
    ("print", "name"),
    ("text", "\">Hello, "),
    ("print", "name"),
    ("text", "</p><a href=\""),
    ("print", "link"),
    ("text", "?ref="),
    ("print", "name"),
    ("text", "\">home</a><script>var n = "),
    ("print", "name"),
    ("text", "; var s = 'Hi "),
    ("print", "name"),
    ("text", "';</script>"),
]


def test_page_example() -> None:
    escaped = auto_escape(EXAMPLE)
    assert [t[2] for t in escaped if t[0] == "print"] == [
        "html",
        "html",
        "url_filter",
        "url_encode",
        "js_value",
        "js_string",
    ]
    env = {"name": "O'Neil & <Co>", "link": "/u"}
    out = render(escaped, env)
    assert out == (
        '<p title="O&#39;Neil &amp; &lt;Co&gt;">Hello, O&#39;Neil &amp; &lt;Co&gt;</p>'
        '<a href="/u?ref=O%27Neil%20%26%20%3CCo%3E">home</a>'
        '<script>var n = "O\\u0027Neil \\u0026 \\u003cCo\\u003e"; '
        "var s = 'Hi O\\u0027Neil \\u0026 \\u003cCo\\u003e';</script>"
    )
    check_template(EXAMPLE, env, escaped)
    out2 = render(escaped, {"name": "a", "link": "ab:c"})
    assert 'href="about:invalid?ref=a"' in out2


def test_transition_trace() -> None:
    c = transition(TEXT, "<a href=\"")
    assert c == Context("URL_START", "a", "href", '"')
    assert transition(c, "/x") == Context("URL_REST", "a", "href", '"')
    assert transition(TEXT, "<script>var s = '") == Context("JS_STRING", "script", "", "'")
    assert transition(TEXT, "<script>x</script>") == TEXT


def test_escapers() -> None:
    assert escape_html("") == ""
    assert escape_html("a\\b") == "a\\b"
    assert escape_html("<&>\"'") == "&lt;&amp;&gt;&quot;&#39;"
    assert filter_url("/a:b") == "/a:b"
    assert filter_url("Http://h") == "Http://h"
    assert filter_url("ab:c") == "about:invalid"
    assert filter_url(":x") == "about:invalid"
    assert filter_url("plain") == "plain"


def test_empty_and_plain() -> None:
    assert auto_escape([]) == []
    assert render(auto_escape([("print", "x")]), {"x": ""}) == ""
    t = [("text", "<p>"), ("print", "x"), ("text", "</p>")]
    assert render(auto_escape(t), {"x": "\\\\"}) == "<p>\\\\</p>"


@pytest.mark.parametrize(
    "template",
    [
        [("text", "<p "), ("print", "x"), ("text", ">")],  # attribute name position
        [("text", "<p class="), ("print", "x"), ("text", ">")],  # unquoted value
        [("text", "<p onclick=\""), ("print", "x"), ("text", "\">")],  # script in an attribute
        [("text", "<p style='"), ("print", "x"), ("text", "'>")],  # style attribute
        [("text", "<"), ("print", "x"), ("text", ">")],  # tag name position
        [("if", "p", [("text", "<p title=\"")], []), ("print", "x"), ("text", "\">")],  # branches differ
        [("loop", "n", [("text", "<b title='")]), ("text", "'>")],  # loop body changes the context
        [("text", "<p title=\"a")],  # template ends inside a tag
        [("text", "<script>var s = '\\"), ("print", "x"), ("text", "';</script>")],  # hole after a backslash
    ],
)
def test_rejects_unsafe_templates(template: list) -> None:
    with pytest.raises(EscapeError):
        auto_escape(template)


def test_random_templates_against_parser() -> None:
    rng = random.Random(20111017)
    checked = 0
    for _ in range(600):
        template = gen_content(rng, 3)
        escaped = auto_escape(template)  # the generator makes only safe templates
        for _ in range(2):
            check_template(template, gen_env(rng), escaped)
            checked += 1
    assert checked == 1200


def test_html_escaping_everywhere_is_wrong() -> None:
    """A single escaper for all contexts breaks the decoding in scripts and URLs."""
    rng = random.Random(7)
    failures = 0
    for _ in range(300):
        template = gen_content(rng, 3)
        escaped = auto_escape(template)

        def naive(nodes: list) -> list:
            out = []
            for t in nodes:
                if t[0] == "print":
                    out.append(("print", t[1], "html"))
                elif t[0] == "if":
                    out.append(("if", t[1], naive(t[2]), naive(t[3])))
                elif t[0] == "loop":
                    out.append(("loop", t[1], naive(t[2])))
                else:
                    out.append(t)
            return out

        env = gen_env(rng)
        try:
            check_template(template, env, naive(escaped))
        except AssertionError:
            failures += 1
    assert failures > 30
