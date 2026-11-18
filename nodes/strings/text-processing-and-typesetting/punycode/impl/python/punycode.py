# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/punycode/. The authors are listed in prov/S9VM2F.jsonl.

"""Punycode, the instance of Bootstring in RFC 3492 (Costello, March 2003).

encode and decode follow the procedures of RFC 3492 section 6.2 and 6.3, with the overflow
checks of section 6.4 for 32-bit unsigned integers. Mixed-case annotation (Appendix A) is
not done: the encoder writes lowercase digits and the decoder accepts both cases.
"""

BASE = 36
TMIN = 1
TMAX = 26
SKEW = 38
DAMP = 700
INITIAL_BIAS = 72
INITIAL_N = 128
DELIMITER = "-"
MAXINT = 2**32 - 1  # the integers of the RFC sample code are 32-bit unsigned


class PunycodeError(ValueError):
    pass


def adapt(delta: int, numpoints: int, firsttime: bool) -> int:
    """Bias adaptation, RFC 3492 section 6.1."""
    delta = delta // DAMP if firsttime else delta // 2
    delta += delta // numpoints
    k = 0
    while delta > ((BASE - TMIN) * TMAX) // 2:
        delta //= BASE - TMIN
        k += BASE
    return k + (BASE - TMIN + 1) * delta // (delta + SKEW)


def digit_value(ch: str) -> int:
    o = ord(ch)
    if 0x30 <= o <= 0x39:
        return o - 0x30 + 26  # 0..9 have the values 26..35
    if 0x41 <= o <= 0x5A:
        return o - 0x41
    if 0x61 <= o <= 0x7A:
        return o - 0x61
    raise PunycodeError(f"bad digit {ch!r}")


def digit_char(d: int) -> str:
    return chr(d + 0x61) if d < 26 else chr(d - 26 + 0x30)


def threshold(k: int, bias: int) -> int:
    return TMIN if k <= bias else TMAX if k >= bias + TMAX else k - bias


def encode(s: str) -> str:
    """Encode a str of code points as Punycode (no "xn--" prefix)."""
    cps = [ord(ch) for ch in s]
    out = [ch for ch in s if ord(ch) < 0x80]  # @line L1
    b = h = len(out)  # @line L2
    if b > 0:
        out.append(DELIMITER)
    n, delta, bias = INITIAL_N, 0, INITIAL_BIAS  # @line L3
    while h < len(cps):  # @line L4
        m = min(c for c in cps if c >= n)  # @line L5
        if (m - n) * (h + 1) > MAXINT - delta:
            raise PunycodeError("overflow")
        delta += (m - n) * (h + 1)  # @line L6
        n = m
        for c in cps:  # @line L7
            if c < n:  # @line L8
                delta += 1
                if delta > MAXINT:
                    raise PunycodeError("overflow")
            if c == n:  # @line L9
                q = delta  # @line L10
                k = BASE
                while True:
                    t = threshold(k, bias)
                    if q < t:
                        break
                    out.append(digit_char(t + (q - t) % (BASE - t)))  # @line L11
                    q = (q - t) // (BASE - t)
                    k += BASE
                out.append(digit_char(q))  # @line L12
                bias = adapt(delta, h + 1, h == b)  # @line L13
                delta = 0
                h += 1
        delta += 1  # @line L14
        n += 1
    return "".join(out)


def decode(p: str) -> str:
    """Decode Punycode (no "xn--" prefix) to a str. Raises PunycodeError on bad input."""
    j = p.rfind(DELIMITER)
    basic = p[:j] if j > 0 else ""  # @line L15
    if any(ord(ch) >= 0x80 for ch in basic):
        raise PunycodeError("non-basic code point before the delimiter")
    out = [ord(ch) for ch in basic]
    pos = j + 1 if j > 0 else 0
    n, i, bias = INITIAL_N, 0, INITIAL_BIAS  # @line L16
    while pos < len(p):  # @line L17
        oldi, w, k = i, 1, BASE  # @line L18
        while True:
            if pos >= len(p):
                raise PunycodeError("truncated input")
            digit = digit_value(p[pos])  # @line L19
            pos += 1
            if digit > (MAXINT - i) // w:
                raise PunycodeError("overflow")
            i += digit * w  # @line L20
            t = threshold(k, bias)
            if digit < t:  # @line L21
                break
            if w > MAXINT // (BASE - t):
                raise PunycodeError("overflow")
            w *= BASE - t
            k += BASE
        bias = adapt(i - oldi, len(out) + 1, oldi == 0)  # @line L22
        if i // (len(out) + 1) > MAXINT - n:
            raise PunycodeError("overflow")
        n += i // (len(out) + 1)  # @line L23
        i %= len(out) + 1
        if n < 0x80 or 0xD800 <= n <= 0xDFFF or n > 0x10FFFF:
            raise PunycodeError(f"decoded value {n:#x} is basic or not a scalar value")
        out.insert(i, n)  # @line L24
        i += 1
    return "".join(map(chr, out))


def to_ascii_label(label: str) -> str:
    """The ACE form of one label: "xn--" plus Punycode when the label is not all ASCII.

    This is only the encoding step. IDNA2008 (RFC 5891) and UTS 46 also map and check the
    label before this step; this function does neither.
    """
    if all(ord(ch) < 0x80 for ch in label):
        return label
    return "xn--" + encode(label)
