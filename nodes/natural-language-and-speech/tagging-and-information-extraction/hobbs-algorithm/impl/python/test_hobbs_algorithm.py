# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hobbs-algorithm/. The authors are listed in prov/3QNB55.jsonl.

import random

from hobbs_algorithm import Node, agrees, bfs, parents, proposals, resolve


def name(w, g):
    return Node("NP", [Node("NNP", word=w)], gender=g, number="sg", person=3)


def pron(w, g, num="sg"):
    return Node("NP", [Node("PRP", word=w)], gender=g, number=num, person=3)


def common(det, noun, *pps, num="sg"):
    """NP -> Det Nominal, Nominal -> N PP*. Common nouns here are neuter."""
    kids = [Node("Det", [Node("DT", word=det)])] if det else []
    kids.append(Node("Nominal", [Node("N", word=noun)] + list(pps)))
    return Node("NP", kids, gender="n", number=num, person=3)


def pp(p, np):
    return Node("PP", [Node("P", word=p), np])


def s(subj, verb, *rest):
    return Node("S", [subj, Node("VP", [Node("V", word=verb)] + list(rest))])


def jm_text(subj2="John", g2="m"):
    """Jurafsky and Martin's example: Bob opened up a new dealership last week.
    John took a look at the Fords in his lot. He ended up buying one."""
    bob = name("Bob", "m")
    s1 = s(bob, "opened up", common("a", "new dealership"), common("", "last week"))
    his = pron("his", "m")
    his_lot = Node("NP", [Node("Det", [his]), Node("Nominal", [Node("N", word="lot")])],
                   gender="n", number="sg", person=3)
    fords = common("the", "Fords", pp("in", his_lot), num="pl")
    subj = name(subj2, g2)
    s2 = s(subj, "took", common("a", "look"), pp("at", fords))
    he = pron("He", "m")
    s3 = s(he, "ended up", Node("VP", [Node("V", word="buying"), pron("one", "n")]))
    return bob, s1, subj, his, fords, s2, he, s3


def test_jm_example():
    bob, s1, john, his, fords, s2, he, s3 = jm_text()
    assert resolve(he, s3, [s1, s2]) is john
    assert resolve(his, s2, [s1]) is john
    # "the Fords in his lot" is never proposed for "his": the path passes its Nominal.
    assert fords not in list(proposals(his, s2, [s1]))


def test_agreement_moves_to_earlier_sentence():
    bob, s1, mary, his, fords, s2, he, s3 = jm_text("Mary", "f")
    order = list(proposals(his, s2, [s1]))
    assert [n.text() for n in order[:3]] == ["Mary", "a look", "Bob"]
    assert resolve(his, s2, [s1]) is bob


def test_object_pronoun_skips_subject():
    bill = name("Bill", "m")
    s1 = Node("S", [bill, Node("VP", [Node("V", word="arrived")])])
    john = name("John", "m")
    him = pron("him", "m")
    s2 = s(john, "likes", him)
    # Step 3 needs an NP or S between the candidate and X, so John is not proposed.
    assert john not in list(proposals(him, s2, [s1]))
    assert resolve(him, s2, [s1]) is bill


def test_possessive_inside_subject():
    john = name("John", "m")
    mother = Node("NP", [Node("Det", [john, Node("POS", word="'s")]),
                         Node("Nominal", [Node("N", word="mother")])], gender="f", number="sg", person=3)
    him = pron("him", "m")
    s1 = s(mother, "likes", him)
    order = list(proposals(him, s1, []))
    assert order == [john]
    assert resolve(him, s1) is john


def test_step_8_right_of_path():
    him = pron("him", "m")
    picture = common("the", "picture", pp("of", him))
    john = name("John", "m")
    s1 = s(picture, "pleased", john)
    assert list(proposals(him, s1, [])) == [john]
    assert resolve(him, s1) is john


def test_no_antecedent():
    she = pron("she", "f")
    s1 = Node("S", [she, Node("VP", [Node("V", word="left")])])
    assert resolve(she, s1, [s(name("Tom", "m"), "slept")]) is None


def test_agreement():
    assert agrees(pron("it", "n"), common("a", "car"))
    assert not agrees(pron("they", None, "pl"), common("a", "car"))
    assert agrees(Node("NP"), pron("she", "f"))


def level_order(root):
    """An independent breadth-first order: sort by depth, then by preorder position."""
    out = []
    stack = [(root, 0)]
    while stack:
        n, d = stack.pop()
        out.append((d, len(out), n))
        for c in reversed(n.children):
            stack.append((c, d + 1))
    return [n for d, k, n in sorted(out, key=lambda t: (t[0], t[1])) if n is not root]


def random_tree(rng, depth=0):
    labels = ["S", "NP", "VP", "PP", "Nominal", "Det"]
    if depth >= 4 or rng.random() < 0.3:
        return Node("NP", [Node("N", word="w")], gender=rng.choice("mfn"))
    k = rng.randint(1, 3)
    return Node(rng.choice(labels), [random_tree(rng, depth + 1) for _ in range(k)],
                gender=rng.choice("mfn"))


def test_breadth_first_order_and_uniqueness():
    rng = random.Random(7)
    for _ in range(300):
        t = random_tree(rng)
        t = Node("S", [t, random_tree(rng)])
        assert [id(n) for n in bfs(t)] == [id(n) for n in level_order(t)]
        prev = Node("S", [random_tree(rng), random_tree(rng)])
        nps = [n for n in level_order(t) if n.label == "NP" and n.children and n.children[0].label == "N"]
        p = rng.choice(nps)
        got = list(proposals(p, t, [prev]))
        ids = [id(n) for n in got]
        assert len(ids) == len(set(ids))
        assert all(n.label == "NP" for n in got)
        assert p not in got
        # Step 4 lists the earlier sentence in breadth-first order.
        tail = [n for n in level_order(prev) if n.label == "NP"]
        assert [id(n) for n in got[-len(tail):]] == [id(n) for n in tail]
        # Every proposal from the current sentence is a node of it.
        inside = {id(n) for n in level_order(t)}
        assert all(id(n) in inside for n in got[:len(got) - len(tail)])
        par = parents(t)
        assert id(p) in par
