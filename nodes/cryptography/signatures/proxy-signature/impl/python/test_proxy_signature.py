# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proxy-signature/. The authors are listed in prov/HJZ5RV.jsonl.
"""Tests for the Schnorr warrant proxy signature on the toy group p = 2039."""

import random
from dataclasses import replace

import pytest

from proxy_signature import (
    G,
    P,
    Q,
    Delegation,
    ProxySignature,
    Warrant,
    delegate,
    h_m,
    keygen,
    proxy_key,
    proxy_sign,
    public_proxy_key,
    verify,
)

X_A, Y_A = keygen(random.Random(1))
X_B, Y_B = keygen(random.Random(2))
X_C, Y_C = keygen(random.Random(3))
W = Warrant(Y_A, Y_B, b"purchase order:", expires=100)


def test_group() -> None:
    assert P == 2 * Q + 1 and pow(G, Q, P) == 1 and G != 1


def test_proxy_signs_within_the_warrant() -> None:
    d = delegate(X_A, W)
    x_p = proxy_key(X_B, d)
    assert pow(G, x_p, P) == public_proxy_key(W, d.K)
    rng = random.Random(4)
    for i in range(10):
        msg = b"purchase order: %d units" % i
        sig = proxy_sign(x_p, d, msg, now=50, r=rng.randrange(1, Q))
        assert verify(Y_A, msg, sig, now=50)
        assert not verify(Y_A, msg + b"0", sig, now=50)
        assert not verify(Y_C, msg, sig, now=50)


def test_proxy_cannot_sign_outside_the_warrant() -> None:
    d = delegate(X_A, W)
    x_p = proxy_key(X_B, d)
    with pytest.raises(ValueError):
        proxy_sign(x_p, d, b"sell the house", now=50)
    with pytest.raises(ValueError):
        proxy_sign(x_p, d, b"purchase order: 1", now=101)
    # A proxy that skips its own check still fails at the verifier.
    msg = b"sell the house"
    r = 77
    R = pow(G, r, P)
    forced = ProxySignature(W, d.K, R, (r + h_m(W, d.K, R, msg) * x_p) % Q)
    assert not verify(Y_A, msg, forced, now=50)
    late = proxy_sign(x_p, d, b"purchase order: 2", now=100)
    assert verify(Y_A, b"purchase order: 2", late, now=100)
    assert not verify(Y_A, b"purchase order: 2", late, now=101)


def test_proxy_cannot_widen_the_warrant() -> None:
    d = delegate(X_A, W)
    wide = replace(W, scope=b"", expires=10**6)
    with pytest.raises(ValueError):
        proxy_key(X_B, Delegation(wide, d.K, d.s_w))
    x_p = proxy_key(X_B, d)
    msg = b"sell the house"
    r = 55
    R = pow(G, r, P)
    forged = ProxySignature(wide, d.K, R, (r + h_m(wide, d.K, R, msg) * x_p) % Q)
    assert not verify(Y_A, msg, forged, now=50)


def test_only_the_named_proxy_can_use_the_delegation() -> None:
    d = delegate(X_A, W)
    with pytest.raises(ValueError):
        proxy_key(X_C, d)
    # The delegator alone lacks x_b; with s_w only, its signatures fail.
    msg = b"purchase order: 9"
    assert not verify(Y_A, msg, proxy_sign(d.s_w, d, msg, now=1, r=9), now=1)
    # The proxy's ordinary key alone also fails.
    assert not verify(Y_A, msg, proxy_sign(X_B, d, msg, now=1, r=9), now=1)


def test_bad_delegation_is_rejected() -> None:
    d = delegate(X_A, W)
    with pytest.raises(ValueError):
        proxy_key(X_B, replace(d, s_w=(d.s_w + 1) % Q))
    with pytest.raises(ValueError):
        delegate(X_C, W)
