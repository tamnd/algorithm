# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/challenge-response-authentication/. The authors are listed in prov/53493G.jsonl.
"""Challenge-response authentication with a shared key.

* HOTP, the event based one-time password of RFC 4226 (December 2005),
  Section 5.
* TOTP, the time based variant of RFC 6238 (May 2011), Section 4.
* A naive symmetric challenge-response, in which the answer is
  MAC_K(challenge). It falls to a reflection attack.
* The fixed form, in which the answer is MAC_K(challenge || identity of the
  prover), as in ISO/IEC 9798-4. The reflection attack fails on it.
* A timestamp based one-pass form with a window and a cache of seen answers.

The MAC is HMAC from the Python standard library.

For study only. The code is not constant time (except where it uses
hmac.compare_digest), and it must not protect real data. Use a maintained
library or a FIPS 140 validated module, and the standard library's hmac
module, for real authentication.
"""

import hashlib
import hmac
import secrets
from typing import Optional, Set, Tuple

# ---------------------------------------------------------------- HOTP and TOTP


def dynamic_truncation(mac: bytes) -> int:
    """RFC 4226 Section 5.3: 31 bits taken at the offset in the low nibble of the last byte."""
    offset = mac[-1] & 0x0F
    return int.from_bytes(mac[offset:offset + 4], "big") & 0x7FFFFFFF


def hotp(key: bytes, counter: int, digits: int = 6, digest: str = "sha1") -> str:
    """HOTP(K, C) = Truncate(HMAC(K, C)) mod 10^digits, with C as 8 bytes big endian."""
    mac = hmac.new(key, counter.to_bytes(8, "big"), getattr(hashlib, digest)).digest()
    return str(dynamic_truncation(mac) % 10**digits).zfill(digits)


def totp(key: bytes, unix_time: int, step: int = 30, t0: int = 0, digits: int = 8, digest: str = "sha1") -> str:
    """TOTP = HOTP(K, T) with T = floor((time - T0) / step), RFC 6238 Section 4."""
    return hotp(key, (unix_time - t0) // step, digits, digest)


class HotpVerifier:
    """A server that accepts the next HOTP value within a look-ahead window (RFC 4226 Section 7.4)."""

    def __init__(self, key: bytes, window: int = 3, digits: int = 6) -> None:
        self.key, self.window, self.digits, self.counter = key, window, digits, 0

    def check(self, otp: str) -> bool:
        for c in range(self.counter, self.counter + self.window + 1):
            if hmac.compare_digest(hotp(self.key, c, self.digits), otp):
                self.counter = c + 1  # resynchronize, and never accept c again
                return True
        return False


class TotpVerifier:
    """A server that accepts TOTP values from the current step and one step before, once each."""

    def __init__(self, key: bytes, step: int = 30, digits: int = 8) -> None:
        self.key, self.step, self.digits, self.last_used = key, step, digits, -1

    def check(self, otp: str, now: int) -> bool:
        t = now // self.step
        for s in (t, t - 1):
            if s > self.last_used and hmac.compare_digest(hotp(self.key, s, self.digits), otp):
                self.last_used = s  # RFC 6238 Section 5.2: do not accept the same step twice
                return True
        return False


# ---------------------------------------------------------------- symmetric challenge-response


def mac(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()


class NaiveParty:
    """Answers any challenge c with MAC_K(c). Both parties share K and play both roles."""

    def __init__(self, name: bytes, key: bytes) -> None:
        self.name, self.key = name, key
        self.pending: Optional[bytes] = None

    def respond(self, challenge: bytes) -> bytes:
        return mac(self.key, challenge)

    def start(self) -> bytes:
        self.pending = secrets.token_bytes(16)
        return self.pending

    def finish(self, answer: bytes) -> bool:
        ok = self.pending is not None and hmac.compare_digest(answer, mac(self.key, self.pending))
        self.pending = None
        return ok


class FixedParty(NaiveParty):
    """Answers c with MAC_K(c || own name), and expects MAC_K(c || peer name)."""

    def __init__(self, name: bytes, key: bytes, peer: bytes) -> None:
        super().__init__(name, key)
        self.peer = peer

    def respond(self, challenge: bytes) -> bytes:
        return mac(self.key, challenge + b"|" + self.name)

    def finish(self, answer: bytes) -> bool:
        ok = self.pending is not None and hmac.compare_digest(answer, mac(self.key, self.pending + b"|" + self.peer))
        self.pending = None
        return ok


def reflection_attack(victim: NaiveParty) -> bool:
    """The intruder poses as the peer of victim, with no key.

    Session 1: the victim sends a challenge c. Session 2: the intruder sends
    the same c back to the victim as a challenge, gets the answer, and returns
    it in session 1. Returns True when session 1 accepts.
    """
    c = victim.start()  # session 1, victim is the verifier
    answer = victim.respond(c)  # session 2, victim is the prover
    return victim.finish(answer)


# ---------------------------------------------------------------- one-pass, timestamp based


def timestamp_token(key: bytes, sender: bytes, receiver: bytes, now: int) -> Tuple[int, bytes]:
    return now, mac(key, now.to_bytes(8, "big") + b"|" + sender + b"|" + receiver)


class TimestampVerifier:
    """Accepts (t, MAC_K(t || A || B)) when |now - t| <= window and the answer is new."""

    def __init__(self, key: bytes, me: bytes, window: int = 120) -> None:
        self.key, self.me, self.window = key, me, window
        self.seen: Set[Tuple[bytes, int]] = set()

    def check(self, sender: bytes, token: Tuple[int, bytes], now: int) -> bool:
        t, tag = token
        if abs(now - t) > self.window:
            return False
        expected = mac(self.key, t.to_bytes(8, "big") + b"|" + sender + b"|" + self.me)
        if not hmac.compare_digest(tag, expected):
            return False
        if (sender, t) in self.seen:
            return False  # a replay inside the window
        self.seen = {(s, u) for (s, u) in self.seen if now - u <= self.window}
        self.seen.add((sender, t))
        return True
