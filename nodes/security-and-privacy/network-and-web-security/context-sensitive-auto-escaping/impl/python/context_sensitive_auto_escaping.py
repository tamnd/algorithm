# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/context-sensitive-auto-escaping/. The authors are listed in prov/ZZYC2R.jsonl.

"""Context-sensitive auto-escaping for a toy HTML template language.

A template is a list of nodes:
  ("text", s)            static text written by the template author
  ("print", name)        a hole filled at render time with the value env[name]
  ("if", name, T1, T2)   T1 when env[name] is true, else T2
  ("loop", name, B)      B repeated env[name] times

auto_escape walks the template once with a small HTML state machine. It
gives each hole the escaper that matches the parsing context at that point,
and it rejects a template whose context at a hole has no safe escaper, or
whose branches or loop bodies end in different contexts. This is the core of
the type inference of Samuel, Saxena and Song (CCS 2011), on a toy subset of
HTML: elements, quoted attributes, URL attributes and script elements with
string literals. It is a teaching model, not a full HTML parser.
"""

from typing import NamedTuple, Union

Node = tuple
Template = list


class EscapeError(ValueError):
    """The template has a hole in an unsafe context, or its contexts do not join."""


class Context(NamedTuple):
    """A parsing context: the state of the toy HTML machine and its fields."""

    state: str
    tag: str = ""
    attr: str = ""
    quote: str = ""


TEXT = Context("TEXT")
URL_ATTRS = frozenset({"href", "src"})
SAFE_SCHEMES = frozenset({"http", "https", "mailto"})
INVALID_URL = "about:invalid"


def _after_tag(tag: str) -> Context:
    return Context("SCRIPT", tag) if tag == "script" else TEXT


def transition(c: Context, s: str) -> Context:
    """Run the toy HTML state machine from context c over the static text s.

    Raises EscapeError on text outside the toy subset. Cost: O(len(s)).
    """
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        st = c.state
        if st == "TEXT":
            if ch == "<":
                c = Context("TAG_OPEN")
        elif st == "TAG_OPEN":
            if ch.isascii() and ch.isalpha():
                c = Context("TAG_NAME", ch.lower())
            elif ch == "/":
                c = Context("END_TAG_OPEN")
            else:
                raise EscapeError("bad character after '<'")
        elif st == "TAG_NAME":
            if ch.isascii() and ch.isalnum():
                c = Context("TAG_NAME", c.tag + ch.lower())
            elif ch == " ":
                c = Context("TAG", c.tag)
            elif ch == ">":
                c = _after_tag(c.tag)
            else:
                raise EscapeError("bad character in a tag name")
        elif st == "TAG":
            if ch == " ":
                pass
            elif ch.isascii() and ch.isalpha():
                c = Context("ATTR_NAME", c.tag, ch.lower())
            elif ch == ">":
                c = _after_tag(c.tag)
            else:
                raise EscapeError("bad character in a tag")
        elif st == "ATTR_NAME":
            if (ch.isascii() and ch.isalpha()) or ch == "-":
                c = Context("ATTR_NAME", c.tag, c.attr + ch.lower())
            elif ch == "=":
                c = Context("BEFORE_VALUE", c.tag, c.attr)
            elif ch == " ":
                c = Context("TAG", c.tag)
            elif ch == ">":
                c = _after_tag(c.tag)
            else:
                raise EscapeError("bad character in an attribute name")
        elif st == "BEFORE_VALUE":
            if ch in "\"'":
                kind = "URL_START" if c.attr in URL_ATTRS else "VALUE"
                c = Context(kind, c.tag, c.attr, ch)
            else:
                raise EscapeError("the toy subset needs quoted attribute values")
        elif st in ("VALUE", "URL_START", "URL_REST"):
            if ch == c.quote:
                c = Context("TAG", c.tag)
            elif st == "URL_START":
                c = Context("URL_REST", c.tag, c.attr, c.quote)
        elif st == "END_TAG_OPEN":
            if ch.isascii() and ch.isalpha():
                c = Context("END_TAG_NAME")
            else:
                raise EscapeError("bad character after '</'")
        elif st == "END_TAG_NAME":
            if ch == ">":
                c = TEXT
            elif not (ch.isascii() and ch.isalnum()):
                raise EscapeError("bad character in an end tag")
        elif st == "SCRIPT":
            if s.startswith("</script>", i):
                c = TEXT
                i += len("</script>")
                continue
            if ch in "\"'":
                c = Context("JS_STRING", "script", "", ch)
            elif ch == "<":
                raise EscapeError("the toy subset allows '<' in a script only in '</script>'")
        elif st == "JS_STRING":
            if ch == "\\":
                c = Context("JS_ESCAPE", "script", "", c.quote)
            elif ch == c.quote:
                c = Context("SCRIPT", "script")
            elif ch in "\n<":
                raise EscapeError("bad character in a script string")
        elif st == "JS_ESCAPE":
            if ch == "\n":
                raise EscapeError("bad escape in a script string")
            c = Context("JS_STRING", "script", "", c.quote)
        else:  # pragma: no cover
            raise EscapeError("unknown state " + st)
        i += 1
    return c


def escaper_for(c: Context) -> Union[str, None]:
    """The name of the escaper for a hole in context c, or None if no escaper is safe."""
    st = c.state
    if st == "TEXT":
        return "html"
    if st == "VALUE":
        if c.attr.startswith("on") or c.attr == "style":
            return None  # script or style inside an attribute: not in the toy subset
        return "html"
    if st == "URL_START":
        return "url_filter"
    if st == "URL_REST":
        return "url_encode"
    if st == "SCRIPT":
        return "js_value"
    if st == "JS_STRING":
        return "js_string"
    return None


def after_print(c: Context) -> Context:
    """The context after a hole. Escaped output never leaves its context,
    except that a URL is no longer at its start."""
    if c.state == "URL_START":
        return Context("URL_REST", c.tag, c.attr, c.quote)
    return c


def escape_nodes(nodes: Template, c: Context) -> tuple[Template, Context]:
    """AUTO-ESCAPE of the page: annotate each hole of nodes, started in context c.

    Returns the annotated nodes and the context at the end. Raises EscapeError.
    Cost: O(n) for a template of total size n (characters of text plus nodes).
    """
    out: Template = []
    for t in nodes:  # @line L1
        kind = t[0]
        if kind == "text":  # @line L2
            c = transition(c, t[1])  # @line L3
            out.append(t)
        elif kind == "print":  # @line L4
            esc = escaper_for(c)
            if esc is None:
                raise EscapeError(f"no safe escaper for a hole in state {c.state}")  # @line L5
            out.append(("print", t[1], esc))  # @line L6
            c = after_print(c)  # @line L7
        elif kind == "if":  # @line L8
            t1, c1 = escape_nodes(t[2], c)  # @line L9
            t2, c2 = escape_nodes(t[3], c)
            if c1 != c2:  # @line L10
                raise EscapeError("the branches of an if end in different contexts")
            out.append(("if", t[1], t1, t2))
            c = c1  # @line L11
        elif kind == "loop":  # @line L12
            body, cb = escape_nodes(t[2], c)
            if cb != c:  # @line L13
                raise EscapeError("a loop body does not end in the context where it starts")
            out.append(("loop", t[1], body))
        else:
            raise EscapeError("unknown node " + repr(kind))
    return out, c  # @line L14


def auto_escape(template: Template) -> Template:
    """Annotate a whole template. It starts and must end in HTML text."""
    out, c = escape_nodes(template, TEXT)
    if c != TEXT:
        raise EscapeError(f"the template ends in state {c.state}, not in text")
    return out


# ---------------------------------------------------------------- escapers


def escape_html(v: str) -> str:
    """Escape the five HTML special characters. Safe in text and in quoted values."""
    return (
        v.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def filter_url(v: str) -> str:
    """Keep a relative URL or one with an allowed scheme; else return a harmless URL."""
    for k, ch in enumerate(v):
        if ch in "/?#":
            return v  # no scheme: a relative URL
        if ch == ":":
            return v if v[:k].lower() in SAFE_SCHEMES else INVALID_URL
    return v


_UNRESERVED = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")


def percent_encode(v: str) -> str:
    """Percent-encode every UTF-8 byte that is not an unreserved URL character."""
    out = []
    for b in v.encode("utf-8"):
        ch = chr(b)
        out.append(ch if ch in _UNRESERVED else "%%%02X" % b)
    return "".join(out)


def escape_js_string(v: str) -> str:
    """Write each character that is not a letter, a digit or a space as a \\uXXXX escape."""
    out = []
    for ch in v:
        if (ch.isascii() and ch.isalnum()) or ch == " ":
            out.append(ch)
        else:
            units = ch.encode("utf-16-be")
            for k in range(0, len(units), 2):
                out.append("\\u%04x" % int.from_bytes(units[k : k + 2], "big"))
    return "".join(out)


ESCAPERS = {
    "html": escape_html,
    "url_filter": lambda v: escape_html(filter_url(v)),
    "url_encode": percent_encode,
    "js_string": escape_js_string,
    "js_value": lambda v: '"' + escape_js_string(v) + '"',
}


def render(template: Template, env: dict) -> str:
    """Render an annotated template. env maps hole names to strings, if names
    to booleans and loop names to repeat counts. Cost: linear in the output."""
    parts: list[str] = []
    stack = [iter(template)]
    while stack:
        t = next(stack[-1], None)
        if t is None:
            stack.pop()
            continue
        kind = t[0]
        if kind == "text":
            parts.append(t[1])
        elif kind == "print":
            if len(t) < 3:
                raise EscapeError("render needs an annotated template")
            parts.append(ESCAPERS[t[2]](str(env[t[1]])))
        elif kind == "if":
            stack.append(iter(t[2] if env[t[1]] else t[3]))
        elif kind == "loop":
            stack.append(iter([node for _ in range(int(env[t[1]])) for node in t[2]]))
    return "".join(parts)
