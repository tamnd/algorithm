# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-composability/. The authors are listed in prov/R8F0AW.jsonl.
"""A toy model of the UC experiment: environment, dummy adversary, ideal
functionality and simulator, for one-byte secure message transmission.

The ideal functionality F_SMT: on input (sid, m) from the sender, it gives the
adversary (sid, len(m)) and gives the receiver (sid, m).

Two real protocols, both in the F_KEY-hybrid model (F_KEY hands a uniform
one-byte key to sender and receiver):
  * otp_fresh: each session asks F_KEY for a fresh key k_sid, and the sender
    puts c = m XOR k_sid on a public channel that the adversary reads;
  * otp_shared: all sessions use the same key k (joint state).

The dummy adversary forwards every message it sees to the environment Z.
The simulator S, in the ideal world, gets only (sid, len(m)) and must make a
ciphertext that looks right to Z; it outputs a uniform byte.

The functions compute Pr[Z outputs 1] exactly, by running over every key and
every simulator coin. A test can only try a finite list of environments; UC
security quantifies over all of them, so the code illustrates the definition
and finds attacks, but it cannot prove security. For study only.
"""

import itertools
from fractions import Fraction
from typing import Callable, Sequence

# An environment gets, for each session, the message it chose, what the
# receiver output, and what the adversary forwarded; it returns 0 or 1.
Env = Callable[[Sequence[int], Sequence[int], Sequence[int]], int]


def real_world(messages: Sequence[int], keys: Sequence[int], shared_key: bool) -> tuple[list[int], list[int]]:
    """Run the OTP protocol for each session. Returns (receiver outputs, what
    the dummy adversary forwards to Z). keys come from F_KEY."""
    outputs, leaked = [], []
    for sid, m in enumerate(messages):
        k = keys[0] if shared_key else keys[sid]
        c = m ^ k                  # the sender's only message, on a public channel
        leaked.append(c)           # the dummy adversary forwards it to Z
        outputs.append(c ^ k)      # the receiver decrypts
    return outputs, leaked


def ideal_world(messages: Sequence[int], sim_coins: Sequence[int]) -> tuple[list[int], list[int]]:
    """F_SMT delivers each message and leaks its length; S answers each leak
    with a fresh uniform byte (its coin)."""
    outputs, leaked = [], []
    for sid, m in enumerate(messages):
        length = 1                 # F_SMT leaks (sid, len(m)) to S, and nothing else
        outputs.append(m)
        leaked.append(sim_coins[sid] % (256 ** length))
    return outputs, leaked


def prob_real(env: Env, messages: Sequence[int], shared_key: bool) -> Fraction:
    """Pr[Z outputs 1] in the real world, over the keys of F_KEY."""
    sessions = len(messages)
    key_count = 1 if shared_key else sessions
    hits = total = 0
    for keys in itertools.product(range(256), repeat=key_count):
        out, leak = real_world(messages, keys, shared_key)
        hits += env(messages, out, leak)
        total += 1
    return Fraction(hits, total)


def prob_ideal(env: Env, messages: Sequence[int]) -> Fraction:
    """Pr[Z outputs 1] in the ideal world, over the simulator's coins."""
    hits = total = 0
    for coins in itertools.product(range(256), repeat=len(messages)):
        out, leak = ideal_world(messages, coins)
        hits += env(messages, out, leak)
        total += 1
    return Fraction(hits, total)


def advantage(env: Env, messages: Sequence[int], shared_key: bool) -> Fraction:
    """|Pr[Z -> 1 | real] - Pr[Z -> 1 | ideal]| for this environment."""
    return abs(prob_real(env, messages, shared_key) - prob_ideal(env, messages))


# A few environments.

def env_xor(messages: Sequence[int], outputs: Sequence[int], leaked: Sequence[int]) -> int:
    """Output 1 if the first two ciphertexts XOR to the XOR of the messages."""
    return int(leaked[0] ^ leaked[1] == messages[0] ^ messages[1])


def env_low_bit(messages: Sequence[int], outputs: Sequence[int], leaked: Sequence[int]) -> int:
    """Output 1 if the low bit of the ciphertext equals the low bit of m."""
    return int(leaked[0] & 1 == messages[0] & 1)


def env_correct(messages: Sequence[int], outputs: Sequence[int], leaked: Sequence[int]) -> int:
    """Output 1 if the receiver got every message right."""
    return int(list(outputs) == list(messages))
