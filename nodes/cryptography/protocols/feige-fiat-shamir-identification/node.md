---
tag: TZZGFT
kind: algorithm
slug: feige-fiat-shamir-identification
name: Feige-Fiat-Shamir identification scheme
aliases:
- FFS identification
area: cryptography/protocols
level: advanced
summary: Zero-knowledge identification based on the hardness of computing square roots modulo a composite.
model: word-ram
complexity:
  vars: {n: the number of binary digits of the modulus, k: the number of secrets, t: the number of rounds}
  time: {worst: Θ(k t n^2), average: Θ(k t n^2), best: Θ(t n^2)}
  space: {extra: Θ(k n)}
properties: {deterministic: false, randomized: true}
history:
  year: 1986
  people: [Amos Fiat, Adi Shamir, Uriel Feige]
  note: Fiat and Shamir gave the identification scheme and its signature form at CRYPTO 1986. Feige, Fiat and Shamir added the signs and proved it a zero-knowledge proof of knowledge in 1987, in the Journal of Cryptology in 1988.
prereqs: [zero-knowledge-proof, quadratic-residuosity-problem, modular-square-root]
see_also: [schnorr-identification-protocol, sigma-protocol, proof-of-knowledge, rabin-cryptosystem, fiat-shamir-heuristic, jacobi-symbol, entity-authentication, integer-factorization]
sources:
  - paper: "Amos Fiat and Adi Shamir, How to prove yourself, practical solutions to identification and signature problems, CRYPTO 1986, LNCS 263, 186-194"
    title: Amos Fiat and Adi Shamir, How to prove yourself, practical solutions to identification and signature problems
    locator: the identity-based identification scheme with k square roots and t rounds, and the signature obtained by hashing the commitments with the message
  - paper: doi:10.1007/BF02351717
    title: Uriel Feige, Amos Fiat and Adi Shamir, Zero-knowledge proofs of identity, Journal of Cryptology 1(2), 1988, 77-94
    locator: the scheme with v_j = ±s_j^-2 over a Blum integer, the definition of a zero-knowledge proof of knowledge, and the proof that the scheme is one
  - url: https://cacr.uwaterloo.ca/hac/
    title: Alfred Menezes, Paul van Oorschot and Scott Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 10, Section 10.4.2, the Feige-Fiat-Shamir identification protocol and its parameters
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Section 4.7, proofs of knowledge and their use for identification schemes
  - paper: doi:10.1137/0218012
    title: Shafi Goldwasser, Silvio Micali and Charles Rackoff, The knowledge complexity of interactive proof systems, SIAM Journal on Computing 18(1), 1989, 186-208
    locator: the zero-knowledge proof for quadratic residuosity, the protocol that the scheme extends to k secrets
---

The Feige-Fiat-Shamir (FFS) identification scheme lets a prover show that it knows square roots modulo a composite $n$ whose factors nobody else knows. The prover holds $k$ secrets $s_j$ and publishes $v_j = \pm s_j^{-2} \bmod n$. In each of $t$ rounds it sends $x = \pm r^2$, gets $k$ random challenge bits, and answers $y = r \prod_{e_j = 1} s_j$. A prover without the secrets passes with probability $2^{-kt}$. Computing square roots modulo $n$ is as hard as factoring $n$ ([Rabin](/rabin-cryptosystem/)), so the scheme is secure if factoring is hard, and it reveals nothing to an honest verifier.

**Notation.** $n = pq$ is a Blum integer: $p$ and $q$ are distinct primes with $p \equiv q \equiv 3 \pmod 4$. $\mathbb{Z}_n^*$ is the group of units mod $n$. $(a / n)$ is the [Jacobi symbol](/jacobi-symbol/). $k$ is the number of secrets, $t$ the number of rounds, and $e = (e_1, \ldots, e_k) \in \{0,1\}^k$ a challenge. All arithmetic is mod $n$.

## In plain words

The prover has $k$ secret numbers. For each one it publishes a lock: one over the square of the secret, with a random sign. Only someone who knows the secret, or the factors of $n$, can open a lock, because finding square roots modulo $n$ is as hard as factoring $n$.

In each round the prover sends the square of a fresh random number, again with a random sign. The verifier picks a random subset of the locks. The prover multiplies its random number by the secrets of that subset. When the verifier squares the answer and multiplies by the chosen locks, the secrets cancel and the prover's square comes back, up to sign. A prover who does not know the secrets can prepare an answer for only one subset, so it must guess the subset in advance: it is right with probability $2^{-k}$ in each round.

## The problem

This is [entity authentication](/entity-authentication/) with a public key: the verifier knows $(n, v_1, \ldots, v_k)$ and wants to check that the party it talks to holds $s_1, \ldots, s_k$. FFS also wanted a proof of knowledge that is zero knowledge, so that many runs with a dishonest verifier teach the verifier nothing that helps it impersonate the prover.

## The algorithm

```pseudo id=main
KEYGEN(k)
    n ← p·q for random primes p ≡ q ≡ 3 (mod 4); p and q may be thrown away
L1  for j = 1 to k:  s_j ← uniform in Z_n^*;  b_j ← uniform bit
L2      v_j ← (−1)^b_j · s_j^(−2) mod n
    publish (n, v_1..v_k); keep s_1..s_k

ROUND (repeat t times; the verifier accepts if every round accepts)
L3  prover:   r ← uniform in Z_n^*;  b ← uniform bit;  x ← (−1)^b · r^2 mod n;  send x
L4  verifier: e ← uniform in {0, 1}^k;  send e
L5  prover:   y ← r · Π_{e_j = 1} s_j mod n;  send y
L6  verifier: if x = 0 then reject
L7  verifier: w ← y^2 · Π_{e_j = 1} v_j mod n;  accept the round iff w = x or w = n − x
```

A trusted center that knows $p$ and $q$ can instead give each user secrets for public values derived from the user's identity, as in the identity-based form of Fiat and Shamir (1986): it picks $v_j$ from a hash of the identity and computes the roots with the factors.

## Example

Take $n = 499 \cdot 547 = 272953$, with $499 \equiv 547 \equiv 3 \pmod 4$. This modulus is far too small to be secure.

| step | value |
| --- | --- |
| secrets $s = (5, 7, 11)$, signs $b = (0, 1, 0)$ | |
| public $v_1 = 5^{-2}$, $v_2 = -7^{-2}$, $v_3 = 11^{-2}$ | $87345$, $178255$, $225581$ |
| $r = 1000$, $b = 1$: $x = -1000^2 \bmod n$ | $-181141 \equiv 91812$ |
| challenge $e$ | $(1, 0, 1)$ |
| answer $y = 1000 \cdot 5 \cdot 11$ | $55000$ |
| check $y^2 v_1 v_3 \bmod n$ | $181141 = n - x$, so $w = -x$: accept |

If the prover answers two challenges for one $x$, for example $e = (1, 0, 1)$ with $y = 55000$ and $e' = (0, 0, 1)$ with $y' = 11000$, then $y / y' = 5 = s_1$.

## Correctness

An honest round is accepted: $y^2 \prod_{e_j=1} v_j = r^2 \prod s_j^2 \prod (\pm s_j^{-2}) = \pm r^2 = \pm x$. Two accepted answers $y, y'$ for one $x$ and challenges that differ only in bit $j$ give $u = y/y'$ with $u^2 v_j = \pm 1$, a secret. A prover that guesses $e$ in advance passes with probability exactly $2^{-k}$. And for each fixed $e$ the pair $(\pm y^2 \prod_{e_j=1} v_j, y)$ with uniform $y$ and sign has the same distribution as a real round. The proofs are below.

## Complexity

- **Per round**: the prover does one squaring and at most $k$ multiplications mod $n$; the verifier the same, plus a comparison. There are no exponentiations, which was the point of the design for smart cards in 1986.
- **Total**: $t(k + 1)$ multiplications for each side. With schoolbook arithmetic on $n$-bit numbers, each costs $\Theta(n^2)$, so the time is $\Theta(k t n^2)$; if the challenge is all zero, $\Theta(t n^2)$.
- **Sizes**: a public key of $k$ numbers mod $n$, a secret key of $k$ numbers, and per round $2n + k$ bits of messages. Space is $\Theta(k n)$.
- **Trade-off**: the soundness error $2^{-kt}$ depends on the product $kt$. More secrets mean fewer rounds and a larger key.

## Properties

- **Soundness error $2^{-k}$ per round, $2^{-kt}$ in total.** A prover that can answer two challenges for one $x$ can compute a square root of $\pm \prod v_j^{d_j}$ for some nonzero $d \in \{-1, 0, 1\}^k$. Such a root is as hard to find as factoring $n$, for random keys.
- **Proof of knowledge.** Rewinding a prover that passes with probability above $2^{-k}$ gives two answers for one $x$ and so a secret, as in the example. FFS defined proofs of knowledge for this purpose.
- **Zero knowledge.** For each fixed challenge there is an exact simulator, so each round is honest-verifier zero knowledge. Against a malicious verifier the rewinding simulator guesses $e$, which takes about $2^k$ tries, so the sequential protocol is zero knowledge when $2^k$ is bounded by a polynomial; with large $k$ only the honest-verifier property is known.
- **The signs hide the residuosity of the keys.** For a Blum integer, $-1$ is a non-square with Jacobi symbol $+1$, and every unit of Jacobi symbol $+1$ is $\pm a^2$ for some $a$. With random signs, each $v_j$ and each $x$ is uniform over the units of Jacobi symbol $+1$, whether or not it is a square. Without signs, $v_j$ would always be a square, and the original Fiat-Shamir scheme reveals that fact; FFS added the signs to make the protocol a proof of knowledge that leaks no such bit.

## Variants and improvements

- **Fiat-Shamir identity-based scheme (1986).** A trusted center derives the $v_j$ from a hash of the user's identity and hands out the roots, so no public key directory is needed.
- **Signatures.** Replace the verifier by a hash of the message and the commitments $x_1, \ldots, x_t$, which gives $kt$ challenge bits. This is the origin of the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/).
- **One round, large $k$.** With $t = 1$ and $k$ near the security level the scheme becomes a sigma protocol with challenge set $\{0,1\}^k$, at the cost of a long public key.
- **Guillou-Quisquater (1988).** Replaces squares by $e$-th powers for a large prime $e$, so one secret and one round give soundness error $1/e$.
- **[Schnorr identification](/schnorr-identification-protocol/).** The same three moves in a group of prime order, with one secret and a long challenge.

## When to use it

Use it to study zero-knowledge identification: it shows soundness, extraction and simulation with only multiplications mod $n$. For new systems, prefer a signature-based [challenge-response](/challenge-response-authentication/), for example with Ed25519 through libsodium, or a scheme in a FIPS 140 validated module. Elliptic curve schemes give the same security with much smaller keys and messages.

## Pitfalls

- **A reused $r$.** Two answers for one $x$ to different challenges give a secret by one division, as in the example.
- **Leaking the factors.** Whoever knows $p$ and $q$ can compute every secret key from the public key, by taking square roots mod $p$ and mod $q$ with $a^{(p+1)/4}$ and joining them by the [Chinese remainder theorem](/chinese-remainder-theorem/). In a multi-user system with a center, the center can impersonate every user.
- **Not checking $x \ne 0$.** A prover that sends $x = 0$ and $y = 0$ passes line L7 for each challenge. More generally, the verifier should reject an $x$ or $y$ that shares a factor with $n$.
- **Too few rounds.** The error is $2^{-kt}$. Implementations that cut $t$ for speed lose security linearly in the exponent.
- **Relay attacks.** As with any identification protocol, an attacker can relay messages between a real prover and a verifier.

## Implementations

The Python code on this page implements key generation, rounds, a guessing cheater, the simulator, square roots with the factors, and extraction from two answers, over the toy Blum integer above. It includes a local Jacobi symbol. The tests check the example, completeness, that the guessing prover passes exactly $1/8$ of all (guess, challenge) pairs for $k = 3$, that whoever holds the factors finds working secrets from the public key, and that two answers that differ in one bit give back the secret. For the tiny Blum integer $77 = 7 \cdot 11$ they check by enumeration that the signed keys $\pm s^{-2}$ are uniform over all 30 units of Jacobi symbol $+1$ (without signs only the 15 squares occur), and that simulated rounds equal real rounds for each challenge. There are no official test vectors for this scheme. The code is for study only, is not constant time, and must not be used to protect real data. Use libsodium or a FIPS 140 validated module for real authentication.

## History

Amos Fiat and Adi Shamir presented "How to prove yourself" at CRYPTO 1986: an identification scheme for smart cards with $k$ square roots and $t$ rounds, an identity-based version with a trusted center, and a signature made by hashing, which became the Fiat-Shamir heuristic. Uriel Feige, Fiat and Shamir then gave a formal definition of zero-knowledge proofs of knowledge and showed that the scheme, with the sign change, is one. Their paper "Zero-knowledge proofs of identity" appeared at STOC 1987 and in the first volume of the Journal of Cryptology in 1988. The protocol extends the zero-knowledge proof for quadratic residuosity of Goldwasser, Micali and Rackoff to many secrets at once. Later schemes, from Guillou-Quisquater to the [Schnorr protocol](/schnorr-identification-protocol/), kept its three moves and reduced the number of rounds.

## References
