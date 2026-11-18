# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/punycode/. The authors are listed in prov/S9VM2F.jsonl.

# The oracle is Python's "punycode" codec (RFC 3492). Written against Python 3.14.
# Never use the "idna" codec as an oracle: it implements IDNA2003, not IDNA2008.

import random

from punycode import PunycodeError, adapt, decode, encode, to_ascii_label

# RFC 3492, section 7.1 (Sample strings), samples (A) to (C) and (G) to (S), in the format
# "label: code points: Punycode". The ACE prefix is omitted, as in the RFC.
RFC_SAMPLES = """\
(A) Arabic (Egyptian): u+0644 u+064A u+0647 u+0645 u+0627 u+0628 u+062A u+0643 u+0644 u+0645 u+0648 u+0634 u+0639 u+0631 u+0628 u+064A u+061F: egbpdaj6bu4bxfgehfvwxn
(B) Chinese (simplified): u+4ED6 u+4EEC u+4E3A u+4EC0 u+4E48 u+4E0D u+8BF4 u+4E2D u+6587: ihqwcrb4cv8a8dqg056pqjye
(C) Chinese (traditional): u+4ED6 u+5011 u+7232 u+4EC0 u+9EBD u+4E0D u+8AAA u+4E2D u+6587: ihqwctvzc91f659drss3x8bo0yb
(G) Japanese (kanji and hiragana): u+306A u+305C u+307F u+3093 u+306A u+65E5 u+672C u+8A9E u+3092 u+8A71 u+3057 u+3066 u+304F u+308C u+306A u+3044 u+306E u+304B: n8jok5ay5dzabd5bym9f0cm5685rrjetr6pdxa
(L) 3<nen>B<gumi><kinpachi><sensei>: u+0033 u+5E74 U+0042 u+7D44 u+91D1 u+516B u+5148 u+751F: 3B-ww4c5e180e575a65lsy2b
(M) <amuro><namie>-with-SUPER-MONKEYS: u+5B89 u+5BA4 u+5948 u+7F8E u+6075 u+002D u+0077 u+0069 u+0074 u+0068 u+002D U+0053 U+0055 U+0050 U+0045 U+0052 u+002D U+004D U+004F U+004E U+004B U+0045 U+0059 U+0053: -with-SUPER-MONKEYS-pc58ag80a8qai00g7n9n
(N) Hello-Another-Way-<sorezore><no><basho>: U+0048 u+0065 u+006C u+006C u+006F u+002D U+0041 u+006E u+006F u+0074 u+0068 u+0065 u+0072 u+002D U+0057 u+0061 u+0079 u+002D u+305D u+308C u+305E u+308C u+306E u+5834 u+6240: Hello-Another-Way--fc4qua05auwb3674vfr0b
(O) <hitotsu><yane><no><shita>2: u+3072 u+3068 u+3064 u+5C4B u+6839 u+306E u+4E0B u+0032: 2-u9tlzr9756bt3uc0v
(P) Maji<de>Koi<suru>5<byou><mae>: U+004D u+0061 u+006A u+0069 u+3067 U+004B u+006F u+0069 u+3059 u+308B u+0035 u+79D2 u+524D: MajiKoi5-783gue6qz075azm5e
(Q) <pafii>de<runba>: u+30D1 u+30D5 u+30A3 u+30FC u+0064 u+0065 u+30EB u+30F3 u+30D0: de-jg4avhby1noc0d
(R) <sono><supiido><de>: u+305D u+306E u+30B9 u+30D4 u+30FC u+30C9 u+3067: d9juau41awczczp
(S) -> $1.00 <-: u+002D u+003E u+0020 u+0024 u+0031 u+002E u+0030 u+0030 u+0020 u+003C u+002D: -> $1.00 <--
"""


def parse_samples():
    for line in RFC_SAMPLES.splitlines():
        head, rest = line.split(": u+", 1) if ": u+" in line else line.split(": U+", 1)
        cps, puny = ("u+" + rest).rsplit(": ", 1)
        yield head, "".join(chr(int(x[2:], 16)) for x in cps.split()), puny


def test_rfc_samples() -> None:
    samples = list(parse_samples())
    assert len(samples) == 12
    for head, s, puny in samples:
        assert encode(s) == puny, head
        assert decode(puny) == s, head


def test_check_values() -> None:
    for word, puny in [("bücher", "bcher-kva"), ("münchen", "mnchen-3ya"), ("ü", "tda"), ("mañana", "maana-pta")]:
        assert encode(word) == puny
        assert decode(puny) == word
    assert to_ascii_label("mañana") == "xn--maana-pta"
    assert to_ascii_label("example") == "example"


def test_decoder_accepts_uppercase_digits() -> None:
    assert decode("maana-PTA") == "mañana"
    # The basic code points keep their case; the inserted one is the code point of the delta.
    assert decode("MAANA-pta") == "MA" + "ñ" + "ANA"


def test_adapt_first_steps() -> None:
    # "ü" alone: delta = (0xFC - 0x80) * 1 = 124, so the bias after the first insertion is
    # adapt(124, 1, True) = 0 + 36 * 0 // 38 = 0.
    assert adapt(124, 1, True) == 0
    assert adapt(0, 1, False) == 0


def test_round_trip_against_codec() -> None:
    rng = random.Random(1)
    pools = [range(0x61, 0x7B), range(0xC0, 0x180), range(0x3040, 0x30A0), range(0x4E00, 0x4F00),
             range(0x1F600, 0x1F650), range(0x30, 0x3A)]
    for _ in range(1500):
        s = "".join(chr(rng.choice(rng.choice(pools))) for _ in range(rng.randrange(1, 15)))
        p = encode(s)
        assert p == s.encode("punycode").decode("ascii")
        assert decode(p) == s
        assert all(ch.isascii() and (ch.isalnum() or ch == "-") for ch in p) or not s.isalnum()


def test_bad_input() -> None:
    # A non-basic code point, a lone delimiter (decoded as a digit), and two inputs that end
    # inside a variable-length integer (the last digit is not below its threshold).
    for bad in ["a-é", "-", "abc-9", "b-z"]:
        try:
            decode(bad)
            raise AssertionError(f"{bad!r} must be rejected")
        except PunycodeError:
            pass


def test_overflow_is_detected() -> None:
    try:
        decode("99999999999999")
        raise AssertionError("expected overflow")
    except PunycodeError:
        pass
