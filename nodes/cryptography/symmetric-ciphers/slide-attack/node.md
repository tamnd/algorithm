---
tag: KDTCXR
kind: technique
slug: slide-attack
name: Slide attack
area: cryptography/symmetric-ciphers
level: research
summary: An attack on ciphers whose rounds all repeat the same keyed map. It finds pairs of texts one round apart, and its cost does not depend on the number of rounds.
prereqs: [block-cipher, known-plaintext-attack, birthday-paradox]
see_also: [related-key-attack, feistel-network, key-schedule, differential-cryptanalysis, gost-28147-89, blowfish, data-encryption-standard, meet-in-the-middle-attack]
sources:
  - paper: doi:10.1007/3-540-48519-8_18
    title: Alex Biryukov and David Wagner, Slide attacks, Fast Software Encryption 1999, LNCS 1636, Springer, 1999
    locator: pp. 245-259, Section 2 (the typical slide attack, slid pairs and weak permutations), Section 3 (the known-plaintext and chosen-plaintext attacks on Feistel ciphers), Table 1 (the attacks on 2K-DES, TREYFER, WAKE-ROFB and a variant of Blowfish) and Section 5 (TREYFER)
  - paper: doi:10.1007/3-540-45539-6_41
    title: Alex Biryukov and David Wagner, Advanced slide attacks, Eurocrypt 2000, LNCS 1807, Springer, 2000
    locator: pp. 589-606, the abstract, Table 1, the complementation slide, sliding with a twist, and the attacks on DESX and GOST
  - paper: doi:10.1007/3-540-48285-7_34
    title: Eli Biham, New types of cryptanalytic attacks using related keys, Eurocrypt 1993, LNCS 765, Springer, 1994
    locator: pp. 398-409, the related-key attacks with shifted subkeys that slide attacks extend to a single key
---

A slide attack is an attack on [block ciphers](/block-cipher/) whose rounds are all the same keyed map, or whose rounds repeat with a short period. The attacker lines up two encryptions one round apart. A pair of plaintexts that fits this pattern, a slid pair, gives two equations for one round, and one round is usually easy to solve for the key. Alex Biryukov and David Wagner introduced the attack in 1999. Its cost does not depend on the number of rounds, so adding rounds does not help.

**Notation.** $E_k = F_k \circ F_k \circ \cdots \circ F_k$ is a cipher made of $r$ copies of the same keyed map $F_k$ on $n$-bit blocks. A pair of known texts $(P, C)$ and $(P', C')$ is slid when $P' = F_k(P)$. $m$ is the number of known texts.

## In plain words

Some ciphers do the same step again and again with the same key. Picture two copies of the cipher at work, the second started one step after the first. If the second message is exactly the first message after one step, then the two copies stay one step apart to the end. So the second result is the first result after one step.

Such a pair gives the attacker the input and output of one step twice. One step on its own is weak, so this is enough to find the key. With a few hundred random messages, such a pair turns up by chance. This works the same for 16 steps or 500.

## When it applies

- **Self-similar rounds.** All rounds are the same function of the key, or the rounds repeat with a period $p$, so that $p$ rounds form one map $F_k$. This happens when the [key schedule](/key-schedule/) is periodic and the rounds have no constants or counters.
- **A weak round.** Biryukov and Wagner call $F_k$ a weak permutation if the key is easy to find from two equations $F_k(x_1) = y_1$ and $F_k(x_2) = y_2$. They show that even three rounds of [DES](/data-encryption-standard/) form a weak permutation.
- **Enough texts.** The attacker needs about $2^{n/2}$ known plaintexts, so that a slid pair is likely. For a [Feistel network](/feistel-network/), chosen plaintexts can lower this to about $2^{n/4}$.

## The template

If $P' = F_k(P)$, then

$$C' = E_k(P') = F_k^r(F_k(P)) = F_k(F_k^r(P)) = F_k(C).$$

So a slid pair satisfies two equations with the same unknown key: $F_k(P) = P'$ and $F_k(C) = C'$. In the toy cipher of this page, $F_k(x) = \mathrm{PERM}(\mathrm{SUB}(x \oplus k))$, so the first equation gives $k = P \oplus \mathrm{SUB}^{-1}(\mathrm{PERM}(P'))$ and the second checks it.

```pseudo id=main
SLIDE(known pairs (P_i, C_i), extra pairs for checking)
L1  cands ← ∅
L2  for each known pair (P, C) do
L3      for each known pair (P′, C′) do
L4          k ← the only key with F_k(P) = P′
L5          if F_k(C) = C′ then add k to cands
L6  for each k in cands do
L7      if E_k is right on the extra pairs then return k
L8  return failure
```

**Why it works.** There are $m^2$ ordered pairs, and each is slid with probability $2^{-n}$, so with $m = 2^{n/2}$ about one slid pair is expected, by the [birthday paradox](/birthday-paradox/). Every slid pair passes line L5 with the right key. A pair that is not slid passes with probability about $2^{-n}$, so about $m^2 \cdot 2^{-n}$ wrong candidates also pass, and lines L6 and L7 remove them with a few extra known pairs.

**Cost.** About $2^{n/2}$ known plaintexts and, for the simple loop above, $m^2 = 2^n$ steps of one round each, whatever the number of rounds. For a Feistel cipher, half of the block passes through a round unchanged, so a slid pair can be found by sorting the texts on these halves. This cuts the time to about $2^{n/2}$.

**About the code.** The Python code of this page attacks a toy cipher made for this page: a 16-bit block and a 16-bit key $k$, with every round equal to $F_k(x) = \mathrm{PERM}(\mathrm{SUB}(x \oplus k))$, where SUB applies the 4-bit S-box of the Heys tutorial to each nibble and PERM is the bit transpose of the same tutorial. It is for study only and is not constant time. Do not use any of it to protect real data. Use AES from a validated library such as OpenSSL instead.

## Classic examples

### The toy cipher

Take $k$ = 3A94 and 64 rounds. The plaintext $P$ = 1234 gives $P' = F_k(P)$ = 9B7C. Their ciphertexts are $C$ = 6523 and $C'$ = BECC, and indeed $F_k(C)$ = BECC. Line L4 gives $k$ = 3A94 from the plaintexts, and the same value from the ciphertexts.

The chance that $m$ random texts hold at least one slid pair is about $1 - e^{-m^2/2^{16}}$. Over 100 random keys at 16 rounds, the right key was among the candidates for 21 keys with $m = 128$, 64 keys with $m = 256$ and all 100 keys with $m = 1024$, against the predicted 22, 63 and 100. Over 200 keys with $m = 512$ and 16, 64 or 500 rounds, it was found for 197 keys, close to the predicted $1 - e^{-4} \approx 0.98$. Each run also gave on average 4.0 wrong candidates, as $m^2 \cdot 2^{-16} = 4$ predicts, and lines L6 and L7 removed them.

### TREYFER

TREYFER is a 64-bit cipher of Gideon Yuval for smart cards, presented at FSE 1997. Its key schedule uses the 64-bit key byte by byte in the same way in every round, so the cipher is 32 copies of one map. Biryukov and Wagner broke it, for any number of rounds and any S-box, with about $2^{32}$ known plaintexts and $2^{44}$ offline work.

### Other targets of 1999 and 2000

Table 1 of the 1999 paper lists these attacks:

| target | rounds | data | time |
|---|---|---|---|
| 2K-DES, a DES variant with two alternating 48-bit subkeys | 64 | $2^{32}$ known plaintexts | $2^{50}$ |
| 2K-DES | 64 | $2^{33}$ adaptive chosen plaintexts | $2^{33}$ |
| TREYFER | 32 | $2^{32}$ known plaintexts | $2^{44}$ |
| [Blowfish](/blowfish/) without round subkeys | 16 | $2^{27}$ chosen plaintexts | $2^{27}$ |

The Blowfish result shows that key-dependent S-boxes do not stop the attack. The full Blowfish has round subkeys and is not affected.

In 2000, Biryukov and Wagner attacked DESX with $2^{32.5}$ known plaintexts and $2^{87.5}$ time, and the last 20 rounds of GOST⊕, a variant of [GOST 28147-89](/gost-28147-89/) with XOR in place of addition, with $2^{33}$ known plaintexts and $2^{70}$ work. They also showed weak key classes for all 32 rounds of GOST⊕.

## Variations

- **Slides by several rounds.** If the key schedule has period $p$, slide by $p$ rounds and treat $p$ rounds as one map.
- **The complementation slide.** For a Feistel cipher whose subkeys alternate between two values, a fixed difference between the two copies can make them match even though the rounds differ.
- **Sliding with a twist.** Slide an encryption against a decryption. For a Feistel cipher with two alternating subkeys, this gives an attack with about $2^{n/2}$ known plaintexts and $2^{n/2}$ time.
- **Related keys.** The [related-key attack](/related-key-attack/) of Biham uses the same slid relation between two encryptions under two keys. The slide attack needs only one key and known or chosen plaintexts, so Biryukov and Wagner call it much more practical than most related-key attacks.

## Pitfalls

- **Many rounds do not help.** The attack is the same for 16 and for 500 rounds. A cipher with a simple, periodic key schedule needs another defense.
- **The defense is easy.** Add a round constant or a counter, as AES does in its key schedule, so that no two rounds are the same map.
- **Random pairs also pass.** About $m^2 \cdot 2^{-n}$ wrong keys pass line L5. Check each candidate on extra known pairs, as in line L7.
- **Real ciphers.** Run such experiments only on toy ciphers or reduced rounds that you are allowed to attack.

## Exercises

1. Prove by induction on $r$ that $F_k(P) = P'$ implies $E_k(P') = F_k(E_k(P))$.
2. Find the expected number of slid pairs, and of wrong keys that pass line L5, for $m = 512$ and $n = 16$.
3. Show that for a Feistel cipher with the same subkey in every round, the right half of $P$ equals the left half of $P'$ for a slid pair. Use this to find slid pairs with a hash table in time about $m$.
4. Change the toy cipher to XOR a different constant into each round, and explain why the attack fails.
5. Explain why a cipher whose subkeys repeat with period 2 needs a slide by two rounds, and what the weak map $F_k$ is then.

## References
