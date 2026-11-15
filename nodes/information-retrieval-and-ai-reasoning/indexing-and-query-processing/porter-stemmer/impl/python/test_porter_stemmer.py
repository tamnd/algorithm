# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/porter-stemmer/. The authors are listed in prov/MAYHA4.jsonl.

import random
import re

import irtoy
from porter_stemmer import (
    consonant_flags,
    ends_cvc,
    ends_double_consonant,
    has_vowel,
    measure,
    porter_stem,
    step_1a,
    step_1b,
    step_1c,
    step_2,
    step_3,
    step_4,
    step_5a,
    step_5b,
)

# ---------------------------------------------------------------------------
# The examples printed in Porter (1980), as in the copy of the paper on
# tartarus.org/martin/PorterStemmer/def.txt. Each step example is the effect
# of that step alone on the word given.
# ---------------------------------------------------------------------------

STEP_EXAMPLES = {
    step_1a: [("caresses", "caress"), ("ponies", "poni"), ("ties", "ti"), ("caress", "caress"), ("cats", "cat")],
    step_1b: [
        ("feed", "feed"), ("agreed", "agree"), ("plastered", "plaster"), ("bled", "bled"),
        ("motoring", "motor"), ("sing", "sing"),
        ("conflated", "conflate"), ("troubled", "trouble"), ("sized", "size"), ("hopping", "hop"),
        ("tanned", "tan"), ("falling", "fall"), ("hissing", "hiss"), ("fizzed", "fizz"),
        ("failing", "fail"), ("filing", "file"),
    ],
    step_1c: [("happy", "happi"), ("sky", "sky")],
    step_2: [
        ("relational", "relate"), ("conditional", "condition"), ("rational", "rational"),
        ("valenci", "valence"), ("hesitanci", "hesitance"), ("digitizer", "digitize"),
        ("conformabli", "conformable"), ("radicalli", "radical"), ("differentli", "different"),
        ("vileli", "vile"), ("analogousli", "analogous"), ("vietnamization", "vietnamize"),
        ("predication", "predicate"), ("operator", "operate"), ("feudalism", "feudal"),
        ("decisiveness", "decisive"), ("hopefulness", "hopeful"), ("callousness", "callous"),
        ("formaliti", "formal"), ("sensitiviti", "sensitive"), ("sensibiliti", "sensible"),
    ],
    step_3: [
        ("triplicate", "triplic"), ("formative", "form"), ("formalize", "formal"),
        ("electriciti", "electric"), ("electrical", "electric"), ("hopeful", "hope"), ("goodness", "good"),
    ],
    step_4: [
        ("revival", "reviv"), ("allowance", "allow"), ("inference", "infer"), ("airliner", "airlin"),
        ("gyroscopic", "gyroscop"), ("adjustable", "adjust"), ("defensible", "defens"),
        ("irritant", "irrit"), ("replacement", "replac"), ("adjustment", "adjust"),
        ("dependent", "depend"), ("adoption", "adopt"), ("homologou", "homolog"),
        ("communism", "commun"), ("activate", "activ"), ("angulariti", "angular"),
        ("homologous", "homolog"), ("effective", "effect"), ("bowdlerize", "bowdler"),
    ],
    step_5a: [("probate", "probat"), ("rate", "rate"), ("cease", "ceas")],
    step_5b: [("controll", "control"), ("roll", "roll")],
}


def test_measure_examples_of_the_paper():
    for w in ["tr", "ee", "tree", "y", "by"]:
        assert measure(w) == 0, w
    for w in ["trouble", "oats", "trees", "ivy"]:
        assert measure(w) == 1, w
    for w in ["troubles", "private", "oaten", "orrery"]:
        assert measure(w) == 2, w
    assert measure("") == 0
    assert measure("replac") == 2


def test_consonants_of_toy_and_syzygy():
    assert [c for c, f in zip("toy", consonant_flags("toy")) if f] == ["t", "y"]
    assert [c for c, f in zip("syzygy", consonant_flags("syzygy")) if f] == ["s", "z", "g"]


def test_conditions():
    assert ends_cvc("wil") and ends_cvc("hop")
    assert not ends_cvc("sow") and not ends_cvc("box") and not ends_cvc("say")
    assert ends_double_consonant("hiss") and not ends_double_consonant("bee")
    # In "syy" the last y is a consonant and the y before it is a vowel.
    assert consonant_flags("syy") == [True, False, True]
    assert not ends_double_consonant("syy") and not ends_double_consonant("yy")
    assert has_vowel("plaster") and not has_vowel("bl")


def test_longest_match_in_step_1a():
    assert step_1a("caresses") == "caress"
    assert step_1a("caress") == "caress"
    assert step_1a("cares") == "care"


def test_step_examples_of_the_paper():
    for step, pairs in STEP_EXAMPLES.items():
        for w, want in pairs:
            assert step(w) == want, (step.__name__, w)


def test_whole_words_of_the_paper():
    chain = ["generalizations", "generalization", "generalize", "general", "gener"]
    assert step_1a(chain[0]) == chain[1]
    assert step_2(chain[1]) == chain[2]
    assert step_3(chain[2]) == chain[3]
    assert step_4(chain[3]) == chain[4]
    assert porter_stem("generalizations") == "gener"
    assert step_1a("oscillators") == "oscillator"
    assert step_2("oscillator") == "oscillate"
    assert step_4("oscillate") == "oscill"
    assert step_5b("oscill") == "oscil"
    assert porter_stem("oscillators") == "oscil"
    for w in ["connect", "connected", "connecting", "connection", "connections"]:
        assert porter_stem(w) == "connect"


def test_lists_a_and_b_of_the_paper():
    for w in ["relate", "probate", "conflate", "pirate", "prelate"]:
        assert step_4(w) == w
    for w in ["derivate", "activate", "demonstrate", "necessitate", "renovate"]:
        assert step_4(w) == w[:-3]
    assert porter_stem("archprelate") == "archprel"
    assert porter_stem("probe") != porter_stem("probate")


def test_relate_and_relativity_by_the_printed_rules():
    # The paper says that the two words conflate, but the printed rules give two stems.
    assert porter_stem("relate") == "relat"
    assert porter_stem("relativity") == "rel"


def test_the_definitive_version():
    assert porter_stem("archaeology") != porter_stem("archaeological")
    assert porter_stem("archaeology", True) == porter_stem("archaeological", True) == "archaeolog"
    assert porter_stem("possibly") != porter_stem("possible")
    assert porter_stem("possibly", True) == porter_stem("possible", True) == "possibl"
    assert porter_stem("as") == "a" and porter_stem("is") == "i" and porter_stem("s") == ""
    assert porter_stem("as", True) == "as" and porter_stem("s", True) == "s"


def test_edge_cases():
    assert porter_stem("") == ""
    assert porter_stem("a") == "a"
    assert porter_stem("eeee") == "eeee"
    assert porter_stem("sss") == "sss"
    assert porter_stem("yyyy") == "yyyi"


def test_toy_collection():
    vocab = sorted({t for d in irtoy.DOCS for t in irtoy.tokenize(irtoy.DOCS[d])})
    assert len(vocab) == 50
    stems = {porter_stem(t) for t in vocab}
    assert len(stems) == 46
    # "lists" (d5) and "document" (d4) match the other form only after stemming.
    assert porter_stem("lists") == porter_stem("list") == "list"
    assert porter_stem("document") == porter_stem("documents") == "document"
    assert porter_stem("sorted") == porter_stem("sort")
    assert porter_stem("merges") == porter_stem("merge")


# ---------------------------------------------------------------------------
# An independent oracle: the rule tables written as in the paper, with the
# conditions read by a small evaluator, and m found from the collapsed C and V
# pattern of the stem.
# ---------------------------------------------------------------------------

TABLES = {
    "1a": "SSES -> SS; IES -> I; SS -> SS; S ->",
    "1b": "(m>0) EED -> EE; (*v*) ED ->; (*v*) ING ->",
    "1b2": "AT -> ATE; BL -> BLE; IZ -> IZE; (*d and not (*L or *S or *Z)) -> single; (m=1 and *o) -> E",
    "1c": "(*v*) Y -> I",
    "2": "(m>0) ATIONAL -> ATE; (m>0) TIONAL -> TION; (m>0) ENCI -> ENCE; (m>0) ANCI -> ANCE;"
    " (m>0) IZER -> IZE; (m>0) ABLI -> ABLE; (m>0) ALLI -> AL; (m>0) ENTLI -> ENT; (m>0) ELI -> E;"
    " (m>0) OUSLI -> OUS; (m>0) IZATION -> IZE; (m>0) ATION -> ATE; (m>0) ATOR -> ATE;"
    " (m>0) ALISM -> AL; (m>0) IVENESS -> IVE; (m>0) FULNESS -> FUL; (m>0) OUSNESS -> OUS;"
    " (m>0) ALITI -> AL; (m>0) IVITI -> IVE; (m>0) BILITI -> BLE",
    "3": "(m>0) ICATE -> IC; (m>0) ATIVE ->; (m>0) ALIZE -> AL; (m>0) ICITI -> IC; (m>0) ICAL -> IC;"
    " (m>0) FUL ->; (m>0) NESS ->",
    "4": "(m>1) AL ->; (m>1) ANCE ->; (m>1) ENCE ->; (m>1) ER ->; (m>1) IC ->; (m>1) ABLE ->;"
    " (m>1) IBLE ->; (m>1) ANT ->; (m>1) EMENT ->; (m>1) MENT ->; (m>1) ENT ->;"
    " (m>1 and (*S or *T)) ION ->; (m>1) OU ->; (m>1) ISM ->; (m>1) ATE ->; (m>1) ITI ->;"
    " (m>1) OUS ->; (m>1) IVE ->; (m>1) IZE ->",
    "5a": "(m>1) E ->; (m=1 and not *o) E ->",
    "5b": "(m>1 and *d and *L) -> single",
}


def parse(table):
    rules = []
    for part in table.split(";"):
        part = part.strip()
        cond = "True"
        if part.startswith("("):
            depth = 0
            for i, ch in enumerate(part):
                depth += ch == "("
                depth -= ch == ")"
                if depth == 0:
                    cond, part = part[1:i], part[i + 1 :].strip()
                    break
        left, right = [x.strip() for x in part.split("->")]
        rules.append((left.lower(), right.lower(), cond))
    return rules


def oracle_is_consonant(w, i):
    if w[i] in "aeiou":
        return False
    if w[i] == "y":
        return i == 0 or not oracle_is_consonant(w, i - 1)
    return True


def oracle_m(stem):
    cv = "".join("c" if oracle_is_consonant(stem, i) else "v" for i in range(len(stem)))
    form = re.sub("v+", "V", re.sub("c+", "C", cv))
    m = form.count("VC")
    assert re.fullmatch("C?(VC){%d}V?" % m, form)
    return m


def holds(cond, stem):
    if cond == "True":
        return True
    cv = [oracle_is_consonant(stem, i) for i in range(len(stem))]
    expr = cond.replace("=", "==").replace(">==", ">=")
    expr = re.sub(r"\bm\b", str(oracle_m(stem)), expr)
    expr = expr.replace("*v*", str(not all(cv)))
    expr = expr.replace("*d", str(len(stem) >= 2 and stem[-1] == stem[-2] and cv[-1] and cv[-2]))
    o = len(stem) >= 3 and cv[-3] and not cv[-2] and cv[-1] and stem[-1] not in "wxy"
    expr = expr.replace("*o", str(o))
    expr = re.sub(r"\*([A-Z])", lambda g: str(stem.endswith(g.group(1).lower())), expr)
    return eval(expr, {"__builtins__": {}})


def oracle_step(table, w):
    rules = parse(table)
    matching = [r for r in rules if r[0] and w.endswith(r[0])]
    if not matching:
        return w, None
    longest = max(len(r[0]) for r in matching)
    for s1, s2, cond in matching:
        if len(s1) == longest:
            stem = w[: len(w) - len(s1)]
            if holds(cond, stem):
                return stem + s2, s1
    return w, None


def oracle_conditional_rules(table, w):
    # Rules with an empty S1: the first one whose condition holds on the whole word.
    for s1, s2, cond in parse(table):
        if s1 == "" and holds(cond, w):
            return w[:-1] if s2 == "single" else w + s2
        if s1 and w.endswith(s1) and holds(cond, w[: len(w) - len(s1)]):
            return w[: len(w) - len(s1)] + s2
    return w


def oracle_stem(w, definitive=False):
    if definitive and len(w) <= 2:
        return w
    w, _ = oracle_step(TABLES["1a"], w)
    w, fired = oracle_step(TABLES["1b"], w)
    if fired in ("ed", "ing"):
        w = oracle_conditional_rules(TABLES["1b2"], w)
    w, _ = oracle_step(TABLES["1c"], w)
    t2 = TABLES["2"]
    if definitive:
        t2 = t2.replace("(m>0) ABLI -> ABLE", "(m>0) BLI -> BLE") + "; (m>0) LOGI -> LOG"
    for name in [t2, TABLES["3"], TABLES["4"], TABLES["5a"]]:
        w, _ = oracle_step(name, w)
    return oracle_conditional_rules(TABLES["5b"], w)


def test_oracle_on_the_paper_examples():
    assert oracle_stem("generalizations") == "gener"
    assert oracle_stem("oscillators") == "oscil"
    assert oracle_stem("hopping") == "hop"


def test_random_words_against_the_oracle():
    rng = random.Random(1980)
    suffixes = sorted({r[0] for t in TABLES.values() for r in parse(t) if r[0]} | {"bli", "logi", "ed", "ing", "y", "ll"})
    letters = "abcdefghijklmnopqrstuvwxyz" + "aeiouy" * 3 + "lstn" * 2
    for _ in range(3000):
        stem = "".join(rng.choice(letters) for _ in range(rng.randint(0, 6)))
        w = stem + "".join(rng.choice(suffixes) for _ in range(rng.randint(0, 3)))
        for definitive in (False, True):
            got = porter_stem(w, definitive)
            assert got == oracle_stem(w, definitive), (w, definitive)
            assert len(got) <= max(len(w), 2)
