# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semistructured-merge/. The authors are listed in prov/30FJFE.jsonl.

import random

from semistructured_merge import Conflict, Node, line_merge, semistructured_merge, to_lines


def method(name: str, *lines: str) -> Node:
    return Node("method", name, body=tuple(lines))


def stack(*members: Node, name: str = "Stack") -> Node:
    return Node("class", name, tuple(members))


PUSH = method("push", "void push(T item) {", "    items.addFirst(item);", "}")
POP = method("pop", "T pop() {", "    return items.removeFirst();", "}")
TOP = method("top", "T top() {", "    return items.getFirst();", "}")
SIZE = method("size", "int size() {", "    return items.size();", "}")


def test_two_new_methods() -> None:
    o, a, b = stack(PUSH, POP), stack(PUSH, POP, TOP), stack(PUSH, POP, SIZE)
    merged, conflicts = semistructured_merge(a, o, b)
    assert conflicts == [] and merged == stack(PUSH, POP, TOP, SIZE)
    # A line merge of the same three files cannot order the two new methods.
    lines, k = line_merge(to_lines(a), to_lines(o), to_lines(b))
    assert k == 1
    assert lines[7:] == ["<<<<<<< A", *to_lines(TOP, 1), "||||||| O", "=======", *to_lines(SIZE, 1), ">>>>>>> B", "}"]


def test_order_does_not_matter() -> None:
    push2 = method("push", "void push(T item) {", "    items.addFirst(item);", "    count++;", "}")
    merged, conflicts = semistructured_merge(stack(POP, PUSH), stack(PUSH, POP), stack(push2, POP))
    assert conflicts == [] and merged == stack(POP, push2)


def test_deletions() -> None:
    o = stack(PUSH, POP)
    assert semistructured_merge(stack(PUSH), o, o) == (stack(PUSH), [])
    assert semistructured_merge(stack(PUSH), o, stack(PUSH)) == (stack(PUSH), [])
    pop2 = method("pop", "T pop() {", "    check();", "    return items.removeFirst();", "}")
    merged, conflicts = semistructured_merge(stack(PUSH), o, stack(PUSH, pop2))
    assert merged == stack(PUSH, pop2)
    assert conflicts == [Conflict(("Stack", "pop"), "deleted in A, changed in B")]
    merged, conflicts = semistructured_merge(stack(PUSH, pop2), o, stack(PUSH))
    assert conflicts == [Conflict(("Stack", "pop"), "deleted in B, changed in A")]


def test_renaming_is_a_delete_and_an_add() -> None:
    o = stack(PUSH, POP)
    remove = POP._replace(name="remove", body=("T remove() {",) + POP.body[1:])
    pop2 = method("pop", "T pop() {", "    check();", "    return items.removeFirst();", "}")
    merged, conflicts = semistructured_merge(stack(PUSH, remove), o, stack(PUSH, pop2))
    assert merged == stack(PUSH, remove, pop2)
    assert conflicts == [Conflict(("Stack", "pop"), "deleted in A, changed in B")]


def test_bodies_are_merged_by_lines() -> None:
    body = ("int f() {", "    int x = 1;", "    int y = 2;", "    int z = 3;", "    return x + y + z;", "}")
    o = stack(method("f", *body))
    a = stack(method("f", *body[:1], "    int x = 10;", *body[2:]))
    b = stack(method("f", *body[:4], "    return x * y * z;", *body[5:]))
    merged, conflicts = semistructured_merge(a, o, b)
    assert conflicts == []
    assert merged.children[0].body == (body[0], "    int x = 10;", body[2], body[3], "    return x * y * z;", body[5])
    c = stack(method("f", *body[:1], "    int x = 20;", *body[2:]))
    merged, conflicts = semistructured_merge(a, o, c)
    assert conflicts == [Conflict(("Stack", "f"), "lines")]
    assert merged.children[0].body[1:6] == ("<<<<<<< A", "    int x = 10;", "||||||| O", "    int x = 1;", "=======")
    # The same method added on both sides has no base: equal bodies merge, different ones conflict.
    assert semistructured_merge(stack(TOP), stack(), stack(TOP)) == (stack(TOP), [])
    top2 = method("top", "T top() {", "    return items.peek();", "}")
    merged, conflicts = semistructured_merge(stack(TOP), stack(), stack(top2))
    assert conflicts == [Conflict(("Stack", "top"), "added on both sides")]


def test_nested_and_bad_input() -> None:
    o = Node("package", "util", (stack(PUSH, POP),))
    a = Node("package", "util", (stack(PUSH, POP, TOP), stack(PUSH, name="Queue")))
    b = Node("package", "util", (stack(PUSH, POP, SIZE),))
    merged, conflicts = semistructured_merge(a, o, b)
    assert conflicts == []
    assert merged == Node("package", "util", (stack(PUSH, POP, TOP, SIZE), stack(PUSH, name="Queue")))
    try:
        semistructured_merge(stack(PUSH), stack(PUSH), stack(PUSH, name="Queue"))
    except ValueError:
        return
    raise AssertionError("different roots were accepted")


def _canonical(node: Node) -> Node:
    if node.terminal:
        return node
    return node._replace(children=tuple(sorted((_canonical(c) for c in node.children), key=lambda c: c.key)))


def _random_class(rng: random.Random) -> Node:
    names = rng.sample("fghijk", rng.randint(0, 4))
    return stack(*(method(n, *(rng.choice("pqr") for _ in range(rng.randint(1, 4)))) for n in names))


def _edit(rng: random.Random, node: Node) -> Node:
    members = list(node.children)
    for _ in range(rng.randint(0, 3)):
        r = rng.random()
        if members and r < 0.25:
            del members[rng.randrange(len(members))]
        elif r < 0.5:
            name = rng.choice("fghijk")
            if all(m.name != name for m in members):
                members.insert(rng.randint(0, len(members)), method(name, rng.choice("pqr")))
        elif members and r < 0.75:
            k = rng.randrange(len(members))
            body = list(members[k].body)
            body.insert(rng.randint(0, len(body)), rng.choice("pqrs"))
            members[k] = members[k]._replace(body=tuple(body))
        else:
            rng.shuffle(members)
    return node._replace(children=tuple(members))


def test_random_merges() -> None:
    rng = random.Random(30)
    for _ in range(300):
        o = _random_class(rng)
        a, b = _edit(rng, o), _edit(rng, o)
        assert semistructured_merge(a, o, o) == (a, [])
        merged, conflicts = semistructured_merge(o, o, b)
        assert conflicts == [] and _canonical(merged) == _canonical(b)
        merged, conflicts = semistructured_merge(a, o, b)
        # The members of A that stay come first, in the order of A; then the members that only B has.
        got = [c.name for c in merged.children]
        from_a = [c.name for c in a.children if c.name in got]
        assert got == from_a + [c.name for c in b.children if c.name in got and c.name not in from_a]
        # A member that one side deleted and the other did not change is gone.
        names_a, names_b = {x.name for x in a.children}, {x.name for x in b.children}
        for c in o.children:
            if (c in a.children and c.name not in names_b) or (c in b.children and c.name not in names_a):
                assert c.name not in got
        if not conflicts:
            back, more = semistructured_merge(b, o, a)
            assert more == [] and _canonical(back) == _canonical(merged)
