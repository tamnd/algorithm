# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/penn-treebank-tokenization/. The authors are listed in prov/BK6WGY.jsonl.

import random
import re
import shutil
import subprocess

import pytest

from penn_treebank_tokenization import ptb_stages, ptb_tokenize

# The substitutions of the tokenizer.sed script of Robert MacIntyre, in order.
SED_SCRIPT = [
    's=^"=`` =g',
    's=\\([ ([{<]\\)"=\\1 `` =g',
    "s=\\.\\.\\.= ... =g",
    "s=[,;:@#$%&]= & =g",
    "s=\\([^.]\\)\\([.]\\)\\([])}>\"']*\\)[ \t]*$=\\1 \\2\\3 =g",
    "s=[?!]= & =g",
    "s=[][(){}<>]= & =g",
    "s=--= -- =g",
    "s=$= =",
    "s=^= =",
    "s=\"= '' =g",
    "s=\\([^']\\)' =\\1 ' =g",
    "s='\\([sSmMdD]\\) = '\\1 =g",
    "s='ll = 'll =g",
    "s='re = 're =g",
    "s='ve = 've =g",
    "s=n't = n't =g",
    "s='LL = 'LL =g",
    "s='RE = 'RE =g",
    "s='VE = 'VE =g",
    "s=N'T = N'T =g",
    "s= \\([Cc]\\)annot = \\1an not =g",
    "s= \\([Dd]\\)'ye = \\1' ye =g",
    "s= \\([Gg]\\)imme = \\1im me =g",
    "s= \\([Gg]\\)onna = \\1on na =g",
    "s= \\([Gg]\\)otta = \\1ot ta =g",
    "s= \\([Ll]\\)emme = \\1em me =g",
    "s= \\([Mm]\\)ore'n = \\1ore 'n =g",
    "s= '\\([Tt]\\)is = '\\1 is =g",
    "s= '\\([Tt]\\)was = '\\1 was =g",
    "s= \\([Ww]\\)anna = \\1an na =g",
    "s=  *= =g",
    "s=^ *==g",
]

PIECES = [
    "the", "John", "can", "n't", "'s", "'re", "'ll", "'ve", "'d", "'M", "cannot", "Gonna", "wanna",
    "gotta", "lemme", "gimme", "'tis", "'Twas", "more'n", "d'ye", "don't", "I'm", "WON'T", "WE'LL",
    "Mr.", "3.5", "U.S.", "a.b", "x", ".", "...", "?", "!", ",", ";", ":", "@", "#", "$", "%", "&",
    "(", ")", "[", "]", "{", "}", "<", ">", "--", '"', "'",
]


def random_line(rng):
    k = rng.randint(0, 10)
    return "".join(rng.choice(PIECES) + rng.choice(["", " ", " ", "\t"]) for _ in range(k))


def test_page_example():
    x = 'He said, "I can\'t pay $3.50 for John\'s book."'
    assert ptb_tokenize(x) == [
        "He", "said", ",", "``", "I", "ca", "n't", "pay", "$", "3.50", "for", "John", "'s", "book", ".", "''",
    ]
    stages = ptb_stages(x)
    assert len(stages) == 9
    assert stages[3].endswith('book ." ')
    assert stages[6].endswith("book . ''   ")


def test_clitics_and_special_words():
    assert ptb_tokenize("They're late, aren't they?") == ["They", "'re", "late", ",", "are", "n't", "they", "?"]
    assert ptb_tokenize("I'm sure we'll go, I'd say.") == ["I", "'m", "sure", "we", "'ll", "go", ",", "I", "'d", "say", "."]
    assert ptb_tokenize("WE'VE WON'T") == ["WE", "'VE", "WO", "N'T"]
    assert ptb_tokenize("Mr. Smith gonna stay.") == ["Mr.", "Smith", "gon", "na", "stay", "."]
    assert ptb_tokenize("'Tis cannot.") == ["'T", "is", "can", "not", "."]
    assert ptb_tokenize("I wanna, gotta, lemme gimme") == [
        "I", "wan", "na", ",", "got", "ta", ",", "lem", "me", "gim", "me",
    ]
    assert ptb_tokenize("It's the students' book.") == ["It", "'s", "the", "students", "'", "book", "."]


def test_quotes_brackets_and_dots():
    assert ptb_tokenize('"Hi," she said.') == ["``", "Hi", ",", "''", "she", "said", "."]
    assert ptb_tokenize("They're (I think) late...") == ["They", "'re", "(", "I", "think", ")", "late", "..."]
    assert ptb_tokenize("a--b [c] {d} <e>") == ["a", "--", "b", "[", "c", "]", "{", "d", "}", "<", "e", ">"]
    assert ptb_tokenize("He came (late).") == ["He", "came", "(", "late", ")", "."]
    assert ptb_tokenize("U.S. officials met in the U.S.") == ["U.S.", "officials", "met", "in", "the", "U.S", "."]


def test_only_the_final_period_is_split():
    assert ptb_tokenize("I like it. You do too.") == ["I", "like", "it.", "You", "do", "too", "."]


def test_edge_cases():
    assert ptb_tokenize("") == []
    assert ptb_tokenize("   ") == []
    assert ptb_tokenize(".") == ["."]
    assert ptb_tokenize("word") == ["word"]
    with pytest.raises(ValueError):
        ptb_tokenize("two\nlines")


def test_random_invariants():
    rng = random.Random(1993)
    single = set(",;:@#$%&?!()[]{}<>")
    done = 0
    while done < 500:
        x = random_line(rng)
        if "''" in x:
            continue
        done += 1
        toks = ptb_tokenize(x)
        assert all(t and not re.search(r"\s", t) for t in toks)
        assert all(len(t) == 1 for t in toks if single & set(t))
        # Only spaces are added, and only double quotes change, into `` or ''.
        joined = "".join('"' if t in ("``", "''") else t for t in toks)
        assert joined == re.sub(r"\s", "", x)
        assert toks.count("``") + toks.count("''") == x.count('"')


@pytest.mark.skipif(shutil.which("sed") is None, reason="no sed program")
def test_random_against_the_sed_script():
    rng = random.Random(1995)
    lines = [random_line(rng) for _ in range(500)]
    args = ["sed"]
    for rule in SED_SCRIPT:
        args += ["-e", rule]
    res = subprocess.run(args, input="\n".join(lines) + "\n", capture_output=True, text=True,
                         env={"LC_ALL": "C"}, timeout=60)
    assert res.returncode == 0
    out = res.stdout.split("\n")
    for x, y in zip(lines, out):
        assert ptb_tokenize(x) == y.split()
