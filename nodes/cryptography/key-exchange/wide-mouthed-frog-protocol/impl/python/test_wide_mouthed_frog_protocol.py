# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wide-mouthed-frog-protocol/. The authors are listed in prov/CYAP9N.jsonl.

import secrets

from wide_mouthed_frog_protocol import Server, ding_dong, message1, receive

WINDOW = 30


def setup(tagged: bool):
    keys = {b"A": secrets.token_bytes(32), b"B": secrets.token_bytes(32)}
    return keys, Server(keys, WINDOW, tagged)


def test_honest_run() -> None:
    for tagged in (False, True):
        keys, s = setup(tagged)
        a, box, k = message1(b"A", keys[b"A"], b"B", 1000, tagged)
        peer, box2 = s.forward(a, box, 1003)
        assert peer == b"B"
        assert receive(keys[b"B"], box2, 1005, WINDOW, tagged) == (b"A", k)


def test_late_message_is_rejected() -> None:
    keys, s = setup(False)
    a, box, _ = message1(b"A", keys[b"A"], b"B", 1000)
    assert s.forward(a, box, 1000 + 3600) is None
    _, box2 = s.forward(a, box, 1001)
    assert receive(keys[b"B"], box2, 1000 + 3600, WINDOW) is None


def test_ding_dong_keeps_an_old_key_alive() -> None:
    keys, s = setup(False)
    a, box, k = message1(b"A", keys[b"A"], b"B", 1000)
    _, box2 = s.forward(a, box, 1001)
    assert receive(keys[b"B"], box2, 1002, WINDOW) == (b"A", k)
    # One day later, after bouncing the message off the server every 20 seconds:
    end = 1001 + 86400
    holder, old = ding_dong(s, box2, b"A", b"B", 1001, end, 20)
    later = receive(keys[holder], old, end, WINDOW)
    assert later is not None and later[1] == k  # the day-old key looks fresh


def test_tags_stop_the_ding_dong() -> None:
    keys, s = setup(True)
    a, box, _ = message1(b"A", keys[b"A"], b"B", 1000, tagged=True)
    _, box2 = s.forward(a, box, 1001)
    assert ding_dong(s, box2, b"A", b"B", 1001, 1001 + 86400, 20) is None
