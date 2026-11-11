# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/registers-have-consensus-number-one/. The authors are listed in prov/3WR03W.jsonl.

import pytest

from explorer import Found
from registers_consensus import protocol_family, verify, wait_for_other, write_then_read


def test_write_then_read_fails_agreement() -> None:
    with pytest.raises(Found) as e:
        verify([write_then_read, write_then_read])
    assert e.value.msg == "agreement fails on inputs (0, 1)"
    # p1 writes 1 and reads nothing: it decides 1. p0 writes 0, reads 1: it decides min = 0.
    assert e.value.schedule == (1, 1, 0, 0)


def test_wait_for_other_fails_wait_freedom() -> None:
    with pytest.raises(Found) as e:
        verify([wait_for_other, wait_for_other])
    assert "cycle" in e.value.msg
    # p0 writes, then reads an empty register again and again: p1 never moves.
    assert e.value.schedule == (0, 0, 0)


def test_no_one_round_protocol_works() -> None:
    pairs, kinds = protocol_family()
    assert pairs == 64 * 64
    assert "correct" not in kinds
    assert kinds == {"validity fails": 2820, "agreement fails": 1276}
