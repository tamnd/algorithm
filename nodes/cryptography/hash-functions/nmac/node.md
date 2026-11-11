---
tag: 81YGXR
kind: algorithm
slug: nmac
name: NMAC
aliases:
- nested MAC
area: cryptography/hash-functions
level: advanced
summary: "The nested MAC NMAC(k1, k2, m) = F_k1(F_k2(m)), where F_k is a Merkle-Damgard hash with IV k. It is a PRF if the compression function is one, and it is the theory behind HMAC."
solves: [message-authentication]
model: word-ram
complexity:
  vars: {n: the message length in blocks of the compression function}
  time: {worst: Θ(n + 1), average: Θ(n + 1), best: Θ(n + 1)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1996
  people: [Mihir Bellare, Ran Canetti, Hugo Krawczyk]
  note: Bellare, Canetti and Krawczyk defined NMAC and HMAC together at CRYPTO 1996. Bellare (CRYPTO 2006) proved NMAC a PRF from the PRF property of the compression function alone.
prereqs: [compression-function, merkle-damgard-construction, pseudorandom-function, message-authentication-code]
see_also: [hmac, universal-hash-family, length-extension-attack, kmac, cbc-mac, prp-prf-switching-lemma]
sources:
  - paper: "Mihir Bellare, Ran Canetti and Hugo Krawczyk, Keying hash functions for message authentication, CRYPTO 1996, LNCS 1109, pages 1 to 15"
    locator: the definition of NMAC and its security from a MAC-secure compression function and a weakly collision resistant keyed iterated hash; HMAC as NMAC with derived keys
  - paper: "Mihir Bellare, New proofs for NMAC and HMAC: security without collision-resistance, CRYPTO 2006, LNCS 4117, pages 602 to 619"
    locator: computational almost universality of the keyed iterated hash from a PRF compression function, and NMAC as a PRF composed with an almost universal function
  - paper: "Peter Gaži, Krzysztof Pietrzak and Michal Rybár, The exact PRF-security of NMAC and HMAC, CRYPTO 2014, LNCS 8616, pages 113 to 130"
    locator: a tight bound for NMAC and HMAC with an ideal compression function, and a matching attack
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 6, Section 6.3 (HMAC and NMAC)
  - url: "https://csrc.nist.gov/pubs/fips/180-4/upd1/final"
    title: NIST FIPS 180-4, Secure Hash Standard, August 2015
    locator: Section 5.1.1 (padding), Section 5.3.3 (the SHA-256 IV), Section 6.2.2 (the SHA-256 compression function)
---

NMAC, the nested MAC, is a [message authentication code](/message-authentication-code/) that runs a [Merkle-Damgård](/merkle-damgard-construction/) hash twice, each time with a secret key in place of the initial value: $\mathrm{NMAC}(k_1, k_2, m) = F_{k_1}(F_{k_2}(m))$. Bellare, Canetti and Krawczyk defined it in 1996 as the clean form of [HMAC](/hmac/), and HMAC is NMAC with two keys derived from one. Bellare (2006) proved that NMAC is a [pseudorandom function](/pseudorandom-function/) whenever the [compression function](/compression-function/) is one, with no need for collision resistance. NMAC is rarely deployed, because it needs a hash whose initial value can be changed; it matters as the object of the proofs.

**Notation.** $f : \{0,1\}^c \times \{0,1\}^b \to \{0,1\}^c$ the compression function, with chaining length $c$ bits and block length $b$ bits ($c = 256$, $b = 512$ for SHA-256). $\mathrm{pad}(\ell)$ the Merkle-Damgård padding for an input of $\ell$ bits. $f^{*}(k, y_1 \cdots y_r)$ the iteration of $f$ from the chaining value $k$ over the blocks $y_i$. $F_k(x) = f^{*}(k, x \| \mathrm{pad}(|x|))$ the keyed iterated hash. $k_1, k_2$ two independent keys of $c$ bits. $A$ an adversary with $q$ queries of at most $\ell$ blocks each, $\mathrm{Adv}^{\mathrm{prf}}$ the advantage in the PRF game.

## In plain words

A hash function such as SHA-256 starts from a fixed public starting value and mixes in the message one block at a time. If you replace the public starting value with a secret one, you get a keyed hash. But that keyed hash alone is not a good MAC: from its output on one message, anyone can continue the mixing and get its output on a longer message.

NMAC uses two secret starting values. The inner keyed hash compresses the long message to a short value. The outer keyed hash, with a different key, processes that short value once more. The attacker sees only the outer result. The inner result stays hidden, so it cannot be continued, and the outer step on a short input acts like one call of a secret random function.

## The problem

[Message authentication](/message-authentication/) in the strong sense of a PRF: for keys $k_1, k_2$ chosen uniformly at random, the function $m \mapsto \mathrm{NMAC}(k_1, k_2, m)$ must be indistinguishable from a uniformly random function on messages, for any adversary with bounded time and queries. A PRF is a secure MAC (EUF-CMA), with an added loss of $2^{-c}$ per forgery attempt.

## The algorithm

```pseudo id=main
NMAC(k1, k2, m)                       ▷ k1, k2 are chaining values of c bits
L1  y ← F_k2(m)                       ▷ inner: iterate f from k2 over m ‖ pad(|m|)
L2  return F_k1(y)                    ▷ outer: one more short keyed hash

HMAC-AS-NMAC(K, m)                    ▷ the HMAC case, for a key of at most B bytes
L3  K' ← K ‖ 0x00^(B − |K|)
L4  k1 ← f(IV, K' ⊕ opad);  k2 ← f(IV, K' ⊕ ipad)
L5  return NMAC(k1, k2, m), with the padding of each layer counting B extra bytes
```

The output $y$ of line L1 has $c$ bits, which is less than one block, so line L2 is a single call of $f$: $F_{k_1}(y) = f(k_1, y \| \mathrm{pad}(c))$. Lines L3 to L5 show how HMAC fits: its first block $K' \oplus \mathrm{ipad}$ turns the public IV into the secret chaining value $k_2$, and the first block $K' \oplus \mathrm{opad}$ of the outer call gives $k_1$. The padding counts the extra block, because the hash saw it. The proof of this identity is Lemma 3 on the [HMAC](/hmac/) page.

**Why HMAC derives the keys from one key.** NMAC needs to set the initial value of the hash. Hash libraries and hardware of 1996 did not allow this, and they still mostly do not. HMAC calls the unchanged hash as a black box, takes one key of any length, and pays two extra compression calls per key (saved by precomputation). The price is one more assumption in the proof: the two values $f(\mathrm{IV}, K' \oplus \mathrm{ipad})$ and $f(\mathrm{IV}, K' \oplus \mathrm{opad})$ must look like two independent uniform keys. This is a PRF assumption on $f$ keyed through its message input under a related-key attack with the two fixed offsets ipad and opad.

**About the code.** The Python code is for study only, is not constant time, and must not protect real data. Use HMAC from the Python standard library or a FIPS 140 validated module. The code implements the SHA-256 compression function of FIPS 180-4 in pure Python, because `hashlib` does not let a caller set the IV, and checks it against `hashlib.sha256` on the full hash.

## Example

HMAC-SHA-256 with the key `Jefe` and the message `what do ya want for nothing?` (RFC 4231, Test Case 2), seen as NMAC.

| step | value |
|---|---|
| L4: $k_1 = f(\mathrm{IV}, K' \oplus \mathrm{opad})$ | `0eafe3d513412e6c6a6a2feb2d375acc51a4fd476db095e823bfa18a52f141d5` |
| L4: $k_2 = f(\mathrm{IV}, K' \oplus \mathrm{ipad})$ | `655da7facc434b375a1cd5cb0692ee0ea47a23d34c3af449dba21ae278c7500c` |
| L1: $y = F_{k_2}(m)$, padding for $64 + 28$ bytes | `a2e485863d27f9d864ac8d802432a1ed477d8c4c6f349d16d4e7e917c629cad7` |
| L2: $F_{k_1}(y)$, padding for $64 + 32$ bytes | `5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843` |

The value $y$ is the inner hash of HMAC, and the last row is the HMAC-SHA-256 tag of RFC 4231. With $k_1$ and $k_2$ fixed, the tag costs two compression calls, one per layer.

**The inner layer alone is not a MAC.** Let $t = F_{k_2}(m)$ for $m$ = `amount=10` (9 bytes). The padding of $m$ fills the block to 64 bytes. Then for any suffix $s$, the value $F_{k_2}(m \| \mathrm{pad} \| s)$ is the iteration of $f$ from $t$ over $s$ and its padding, which needs no key. The tests carry out this [length extension](/length-extension-attack/) on $F_{k_2}$ with $s$ = `&amount=1000000`, and show that the same step fails on the full NMAC, because the attacker sees $F_{k_1}(t)$ and not $t$.

## Correctness

NMAC computes $F_{k_1}(F_{k_2}(m))$ by lines L1 and L2, and with $k_2 = \mathrm{IV}$ the function $F_{\mathrm{IV}}$ is the hash $H$ itself; the tests check this against `hashlib.sha256`. The security results are as follows; all are in the standard model.

**Bellare, Canetti and Krawczyk (1996).** If $f$ is a secure MAC with forging probability $\varepsilon_f$, and the keyed iterated hash $F$ is weakly collision resistant with probability $\varepsilon_F$ (an adversary who sees no output and asks $F_{k}$ on chosen messages finds no collision), then NMAC is a secure MAC with forging probability at most $\varepsilon_f + \varepsilon_F$, for the same numbers of queries and similar time.

**Bellare (2006).** If $f$ is a PRF (keyed through the chaining input), then $F$ is computationally almost universal, and NMAC, as a PRF applied to the output of an almost universal function, is a PRF. The bound loses a factor of about $q^2 \ell$ with respect to the PRF advantage against $f$. No collision resistance is needed, which is why NMAC and HMAC with MD5 or SHA-1 were not broken by the collision attacks on those hashes.

**The composition step, proved in full below.** If $F_{k_2}$ is $\varepsilon$-almost universal (for all $m \neq m'$, $\Pr_{k_2}[F_{k_2}(m) = F_{k_2}(m')] \le \varepsilon$) and $g_{k_1}$ is a PRF on $c$-bit inputs, then for every adversary $A$ with $q$ queries there is an adversary $B$ with $q$ queries and about the same time as $A$ plus $q$ evaluations of $F$, such that
$$\mathrm{Adv}^{\mathrm{prf}}_{g \circ F}(A) \le \mathrm{Adv}^{\mathrm{prf}}_{g}(B) + \binom{q}{2} \varepsilon.$$

**Tight bounds.** With an ideal (random) compression function, Gaži, Pietrzak and Rybár (2014) showed that the PRF advantage of NMAC is about $\ell q^2 / 2^c$ up to lower order factors, and gave an attack that matches it. So the quadratic dependence on $q$ is real, and for $c = 256$ it allows about $2^{128}$ queries before the bound becomes weak.

## Complexity

For a message of $n$ blocks after padding, line L1 makes $n$ calls of $f$ and line L2 makes one, so NMAC makes $n + 1$ calls. HMAC makes $n + 3$ calls (one extra block in each layer) or $n + 1$ with precomputed keys. Extra space is $\Theta(1)$: one chaining value and one block buffer.

## Properties

- **Deterministic and stateless.** No nonce is needed.
- **Two keys of $c$ bits each**, so the key has $2c$ bits. Key recovery is not the weak point: the generic limit is the internal collision forgery after about $2^{c/2}$ queries, the same as for HMAC.
- **Not black-box in the hash.** It needs access to the IV of the iteration, which is the reason HMAC exists.
- **The outer call is on a short input.** It is one call of $f$ keyed through the chaining value, so its PRF security is the PRF security of $f$ directly.

## Variants and improvements

- **[HMAC](/hmac/).** NMAC with $k_1, k_2$ derived from one key through the hash, as above.
- **Cascade and "hash then PRF".** NMAC is an instance of the general pattern: compress with a keyed almost universal function, then apply a PRF to the short result. The same pattern gives Wegman-Carter style MACs and the encrypted [CBC-MAC](/cbc-mac/), where the outer layer is a second block cipher call with an independent key.
- **[KMAC](/kmac/)** for sponge hashes. A sponge does not need the nested form: its output is a truncated part of the state, and the hidden capacity part blocks length extension.
- **Envelope MAC and sandwich MAC.** Other one-key forms such as $H(K \| m \| K)$ with special padding; they have proofs too, but they are less used.

## When to use it

Use NMAC in proofs and in designs where the hash is built in house and the IV is accessible, for example in hardware with a custom compression core. For software with a standard hash, use HMAC, which gives the same security with one key and an unchanged hash.

## Pitfalls

- **Using $F_k$ alone as a MAC.** It falls to length extension, as in the example.
- **Equal keys.** With $k_1 = k_2$ the proof does not apply. The keys must be independent.
- **Short chaining values.** The security bound depends on $c$, not on the output length after truncation. A hash with $c = 128$, such as MD5, gives about $2^{64}$ queries before an internal collision forgery.
- **Assuming the proof covers SHA-3.** NMAC and Lemma 3 of the HMAC page are about Merkle-Damgård hashes. SHA-3 is a [sponge](/sponge-construction/), and its MAC is KMAC.

## Implementations

The Python code implements the SHA-256 compression function `compress` (FIPS 180-4, Section 6.2.2) with the padding `md_pad`, the keyed iteration `keyed_hash` with an offset for bytes hashed before the key, `nmac` (lines L1 and L2), `hmac_keys` (lines L3 and L4) and `hmac_via_nmac` (line L5). The tests check the two FIPS 180-4 example digests of `abc` and of the 448-bit message, the full hash against `hashlib.sha256` at the block boundaries, HMAC through NMAC against the standard `hmac` module and RFC 4231 Test Case 2, that a wrong or swapped key changes the tag, the length extension of the inner layer and its failure on NMAC, and that one changed bit changes about half of the output bits.

## History

Bellare, Canetti and Krawczyk introduced NMAC and HMAC at CRYPTO 1996, with NMAC as the form that their proof covers. After the MD5 and SHA-1 collisions of 2004 and 2005, the collision resistance assumption in that proof was no longer credible, and Bellare published a new proof at CRYPTO 2006 that needs only a PRF compression function. That reduction is not tight, and Gaži, Pietrzak and Rybár (CRYPTO 2014) gave tight bounds in the model where the compression function is ideal.

## References
