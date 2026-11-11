# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mix-network/. The authors are listed in prov/571HZE.jsonl.
#
# Re-encryption mixes have no official test vectors. The tests check the
# multiset of plaintexts, the hiding of one mix's permutation against simple
# linkers, the proof of shuffle, and the n - 1 attack on a threshold mix,
# all on a toy group with simulated local parties.

from collections import Counter

from mix_network import (
    G,
    P,
    Q,
    ThresholdMix,
    Trustee,
    cascade,
    decrypt_batch,
    encode,
    decode,
    encrypt,
    joint_key,
    mix,
    prove_shuffle,
    reencrypt,
)


def is_probable_prime(n: int) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def setup(n_trustees=3):
    trustees = [Trustee() for _ in range(n_trustees)]
    return trustees, joint_key(trustees)


def test_group_and_encoding():
    assert P == 2 * Q + 1 and is_probable_prime(P) and is_probable_prime(Q)
    assert G != 1 and pow(G, Q, P) == 1
    for m in (1, 2, 5, Q - 1, Q):
        assert pow(encode(m), Q, P) == 1 and decode(encode(m)) == m


def test_outputs_equal_inputs_as_a_multiset():
    trustees, y = setup()
    votes = [3, 1, 2, 3, 3, 1, 7, 2]  # repeated values on purpose
    board = cascade(y, [encrypt(y, v) for v in votes], k=4)
    assert Counter(decrypt_batch(trustees, board[-1])) == Counter(votes)
    for batch in board:  # every intermediate batch holds the same plaintexts
        assert Counter(decrypt_batch(trustees, batch)) == Counter(votes)


def test_reencryption_keeps_the_plaintext_and_changes_both_parts():
    trustees, y = setup()
    c = encrypt(y, 42)
    d = reencrypt(y, c, 12345)
    assert decrypt_batch(trustees, [d]) == [42]
    assert d[0] != c[0] and d[1] != c[1]


def test_no_ciphertext_component_is_shared():
    _, y = setup()
    inp = [encrypt(y, m) for m in range(1, 17)]
    out, _, _ = mix(y, inp)
    parts_in = {a for a, _ in inp} | {b for _, b in inp}
    parts_out = {a for a, _ in out} | {b for _, b in out}
    assert not parts_in & parts_out


def _identity_linker(inp, out):
    return list(range(len(inp)))


def _rank_linker(inp, out):
    """Guess that the k-th smallest first part of the input went to the k-th smallest of the output."""
    rin = sorted(range(len(inp)), key=lambda i: inp[i][0])
    rout = sorted(range(len(out)), key=lambda j: out[j][0])
    guess = [0] * len(inp)
    for i, j in zip(rin, rout):
        guess[i] = j
    return guess


def _linking_rate(y, linker, reorder, trials=100, n=8):
    hits = 0
    for _ in range(trials):
        inp = [encrypt(y, m) for m in range(1, n + 1)]
        out, pi, _ = mix(y, inp, reorder=reorder)
        guess = linker(inp, out)
        hits += sum(guess[i] == pi[i] for i in range(n))
    return hits / (trials * n)


def test_naive_linkers_do_no_better_than_chance():
    _, y = setup()
    # Against a mix that does not reorder, linking by position always works.
    assert _linking_rate(y, _identity_linker, reorder=False) == 1.0
    # Against a mix that reorders, each linker finds about 1 link in 8 (chance is 0.125).
    for linker in (_identity_linker, _rank_linker):
        assert _linking_rate(y, linker, reorder=True) < 0.2


def test_proof_of_shuffle_accepts_an_honest_mix():
    _, y = setup()
    inp = [encrypt(y, m) for m in range(1, 9)]
    out, pi, s = mix(y, inp)
    assert prove_shuffle(y, inp, out, pi, s, rounds=20)


def test_proof_of_shuffle_catches_a_replaced_ciphertext():
    _, y = setup()
    inp = [encrypt(y, m) for m in range(1, 9)]
    out, pi, s = mix(y, inp)
    cheat = list(out)
    cheat[pi[0]] = encrypt(y, 99)  # the mix drops a vote and adds its own
    # Each round catches the cheat with probability 1/2; 40 rounds miss it with probability 2^-40.
    assert not prove_shuffle(y, inp, cheat, pi, s, rounds=40)


def test_n_minus_1_attack_on_a_threshold_mix():
    trustees, y = setup()
    size = 8
    m1 = ThresholdMix(y, size)
    honest = {f"user{i}": 100 + i for i in range(size)}
    target = "user3"
    # The attacker controls the network in front of the mix: it holds back all
    # honest messages but the target's, and fills the batch with its own.
    own = [500 + k for k in range(size - 1)]
    outputs = m1.submit(encrypt(y, honest[target]))
    for v in own:
        outputs = m1.submit(encrypt(y, v))
    assert outputs is not None and len(outputs) == size
    rest = cascade(y, outputs, k=2)[-1]  # later honest mixes do not help
    plain = decrypt_batch(trustees, rest)
    left = Counter(plain) - Counter(own)
    assert list(left) == [honest[target]]  # the target's message is exposed


def test_a_full_honest_batch_hides_the_sender():
    trustees, y = setup()
    size = 8
    m1 = ThresholdMix(y, size)
    honest = [100 + i for i in range(size)]
    outputs = None
    for v in honest:
        outputs = m1.submit(encrypt(y, v))
    plain = decrypt_batch(trustees, outputs)
    # The attacker learns the set of messages, but each could be from any sender.
    assert Counter(plain) == Counter(honest)
