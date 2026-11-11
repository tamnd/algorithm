---
tag: T3AHK6
kind: algorithm
slug: verifiable-secret-sharing
name: Verifiable secret sharing
aliases:
- VSS
- Feldman VSS
- Pedersen VSS
area: cryptography/protocols
level: advanced
summary: Secret sharing where shareholders can check that their shares are consistent with the dealer's commitments.
model: word-ram
complexity:
  vars: {n: the number of parties, t: the threshold, k: the number of binary digits of the modulus p}
  time: {worst: Θ(n t k^3), average: Θ(n t k^3), best: Θ(n t k^3)}
  space: {extra: Θ((n + t) k)}
properties: {deterministic: false, randomized: true}
history:
  year: 1985
  people: [Benny Chor, Shafi Goldwasser, Silvio Micali, Baruch Awerbuch, Paul Feldman, Torben Pryds Pedersen]
  note: Chor, Goldwasser, Micali and Awerbuch defined VSS in 1985. Feldman gave the non-interactive scheme with g^{a_j} in 1987, and Pedersen the perfectly hiding scheme with g^{a_j} h^{b_j} in 1991.
prereqs: [shamir-secret-sharing, pedersen-commitment, discrete-logarithm-problem]
see_also: [threshold-cryptography, threshold-signature, bgw-protocol, secure-multiparty-computation, byzantine-broadcast, malicious-adversary-model, commitment-scheme, feldman-micali-byzantine-agreement]
sources:
  - paper: "Benny Chor, Shafi Goldwasser, Silvio Micali and Baruch Awerbuch, Verifiable secret sharing and achieving simultaneity in the presence of faults, FOCS 1985, 383-395"
    title: Benny Chor, Shafi Goldwasser, Silvio Micali and Baruch Awerbuch, Verifiable secret sharing and achieving simultaneity in the presence of faults
    locator: the definition of verifiable secret sharing and its use for simultaneous broadcast
  - paper: doi:10.1109/SFCS.1987.4
    title: Paul Feldman, A practical scheme for non-interactive verifiable secret sharing, FOCS 1987, 427-437
    locator: the commitments g^{a_j} to the coefficients of Shamir's polynomial and the check g^{s_i} = prod C_j^{i^j}
  - paper: doi:10.1007/3-540-46766-1_9
    title: Torben Pryds Pedersen, Non-interactive and information-theoretic secure verifiable secret sharing, CRYPTO 1991, LNCS 576
    locator: the commitments g^{a_j} h^{b_j}, perfect secrecy of the secret, and binding under the discrete logarithm assumption
  - paper: "Rosario Gennaro, Stanislaw Jarecki, Hugo Krawczyk and Tal Rabin, Secure distributed key generation for discrete-log based cryptosystems, EUROCRYPT 1999, LNCS 1592, 295-310; Journal of Cryptology 20(1), 2007"
    title: Rosario Gennaro, Stanislaw Jarecki, Hugo Krawczyk and Tal Rabin, Secure distributed key generation for discrete-log based cryptosystems
    locator: the attack that biases the public key of the joint-Feldman DKG, and the fix with a Pedersen VSS phase
  - paper: "Torben Pryds Pedersen, A threshold cryptosystem without a trusted party, EUROCRYPT 1991, LNCS 547, 522-526"
    title: Torben Pryds Pedersen, A threshold cryptosystem without a trusted party
    locator: the distributed key generation in which every party deals a Feldman sharing and the key is the sum
  - paper: doi:10.1145/359168.359176
    title: Adi Shamir, How to share a secret, Communications of the ACM 22(11), 1979, 612-613
    locator: the threshold scheme that VSS makes verifiable
---

Verifiable secret sharing (VSS) is [Shamir's secret sharing](/shamir-secret-sharing/) with a public check: the dealer publishes commitments to the coefficients of its polynomial, and each party checks that its private share is a point on the committed polynomial. A dealer who hands out inconsistent shares is caught, and at reconstruction a party who brings a wrong share is caught too. Feldman's scheme commits with $C_j = g^{a_j}$ and needs one broadcast; Pedersen's scheme commits with $C_j = g^{a_j} h^{b_j}$ and also hides the secret perfectly. VSS is the step that turns secret sharing into a tool against active cheaters: it is used in [threshold cryptography](/threshold-cryptography/), distributed key generation, [Byzantine agreement](/feldman-micali-byzantine-agreement/) and [multiparty computation](/secure-multiparty-computation/).

**Notation.** $p = 2q + 1$ is a safe prime and $G = \langle g \rangle \subset \mathbb{Z}_p^*$ the subgroup of prime order $q$. $h \in G$ is a second generator whose discrete logarithm to the base $g$ nobody knows. The secret is $s \in \mathbb{Z}_q$, the threshold is $t$, and $f(X) = a_0 + a_1 X + \cdots + a_{t-1} X^{t-1}$ with $a_0 = s$. Pedersen's scheme also uses $r(X) = b_0 + \cdots + b_{t-1} X^{t-1}$. Party $i \in \{1, \ldots, n\}$ gets $s_i = f(i)$ (and $r_i = r(i)$). $k$ is the bit length of $p$.

## In plain words

In Shamir's scheme the parties must trust the dealer: a bad dealer can give out values on no common polynomial, so different groups of parties recover different secrets. Nobody can tell a real share from a fake one.

VSS adds a public "fingerprint" of the polynomial. The dealer puts each coefficient in the exponent of $g$ and broadcasts the results. Because exponents add when powers multiply, anyone can compute $g^{f(i)}$ from these values without knowing $f$. Party $i$ raises $g$ to its share and compares. If the two numbers differ, party $i$ complains in public.

Feldman's fingerprint starts with $g^s$, which gives the secret away to anyone who can take discrete logarithms. Pedersen adds a second random polynomial in the exponent of $h$, which makes every fingerprint a uniform group element whatever the secret.

## The problem

Let a dealer share $s$ among $n$ parties, of which up to $t - 1$ (and possibly the dealer) are actively dishonest. VSS asks for:

1. **Verifiability.** After the sharing phase, either the dealer is disqualified, or there is a unique value $s^*$ such that every set of $t$ honest parties reconstructs $s^*$, whatever the dishonest parties do. If the dealer is honest, $s^* = s$ and it is never disqualified.
2. **Secrecy.** If the dealer is honest, the dishonest parties learn nothing about $s$ in the sharing phase: computationally for Feldman, perfectly for Pedersen.

The protocols here assume a broadcast channel and private channels from the dealer to each party.

## The algorithm

```pseudo id=main
DEAL(s, t, n)
L1  f(X) ← s + a_1 X + ... + a_{t-1} X^{t-1} with uniform a_j;  (Pedersen: r(X) ← uniform, degree < t)
L2  broadcast C_j ← g^{a_j}   (Pedersen: C_j ← g^{a_j} h^{b_j})   for j = 0 .. t-1
L3  send party i the share s_i ← f(i)   (Pedersen: also r_i ← r(i))   privately

VERIFY(i, s_i [, r_i])                       // run by party i, and by all at reconstruction
L4  accept iff g^{s_i} [h^{r_i}] = Π_{j=0}^{t-1} C_j^{(i^j)}
    otherwise party i broadcasts a complaint; the dealer must broadcast s_i [, r_i],
    and it is disqualified if that fails L4 or if t or more parties complain

RECONSTRUCT(shares from the parties)
L5  keep the shares that pass L4
L6  s ← Σ_j λ_j s_j over any t of them   (Lagrange at 0, as in Shamir's scheme)
```

## Example

Take $p = 23$, $q = 11$, $g = 4$, $h = 9$, $t = 2$, $n = 3$, and $s = 7$. In a group this small, anybody can find $\log_4 9 = 8$, so the example only shows the arithmetic.

**Feldman.** With $a_1 = 3$, $f(X) = 7 + 3X$. The dealer broadcasts $C_0 = 4^7 = 8$ and $C_1 = 4^3 = 18$ (mod 23) and sends the shares $f(1) = 10$, $f(2) = 2$, $f(3) = 5$ (mod 11). Party 2 checks $4^2 = 16$ against $C_0 C_1^{2} = 8 \cdot 18^2 = 8 \cdot 2 = 16$, and accepts. Had the dealer sent 3 instead, party 2 would compare $4^3 = 18 \ne 16$ and complain. Everybody can also try the 11 exponents and find $4^7 = 8 = C_0$, so the secret 7 is public in this tiny group.

**Pedersen.** With $b(X) = 5 + 2X$ as well, the dealer broadcasts $C_0 = 4^7 \cdot 9^5 = 18$ and $C_1 = 4^3 \cdot 9^2 = 9$, and sends party 2 the pair $(f(2), b(2)) = (2, 9)$. Party 2 checks $4^2 \cdot 9^9 = 9$ against $C_0 C_1^2 = 18 \cdot 12 = 9$, and accepts. Now $C_0 = 18$ fits every secret: for each $s'$ there is a $b_0'$ with $4^{s'} 9^{b_0'} = 18$.

## Correctness

The check works because exponentiation turns the polynomial into a product: $\prod_j C_j^{i^j} = g^{\sum_j a_j i^j} = g^{f(i)}$, and for Pedersen $\prod_j C_j^{i^j} = g^{f(i)} h^{r(i)}$. So honest shares pass. Since $g$ has prime order $q$, $g^{x} = g^{f(i)}$ only for $x = f(i) \bmod q$, so a wrong Feldman share always fails. If all honest parties accept, their shares lie on the committed polynomial, so any $t$ honest shares give the same value. For Pedersen this needs binding: a wrong pair that passes, together with the right one, gives $\log_g h$. Pedersen's commitments are perfectly hiding, and with $t - 1$ shares the view of the parties is independent of $s$. The full proofs are below.

## Complexity

- **Dealer**: $t$ exponentiations for Feldman, $2t$ for Pedersen, plus $\Theta(n t)$ operations mod $q$ for the shares. Broadcast: $t$ group elements.
- **Each party**: one check of $t$ exponentiations, or one multi-exponentiation of length $t$. The exponents $i^j \bmod q$ have $k$ bits, so with schoolbook arithmetic one check costs $\Theta(t k^3)$, and all $n$ checks $\Theta(n t k^3)$.
- **Reconstruction**: one check per share received, then $\Theta(t^2)$ operations mod $q$.
- **Rounds**: one round of dealing and broadcast, plus one round of complaints and answers if a party complains. That is why Feldman called the scheme non-interactive.

## Properties

- **Feldman: perfectly binding, computationally hiding.** The dealer cannot change the shared secret after broadcasting, even with unbounded power. But $C_0 = g^s$ reveals $g^s$, so secrecy needs the [discrete logarithm problem](/discrete-logarithm-problem/) to be hard, and only in the sense that $s$ cannot be computed. When the secret is a private key whose public key $g^s$ is public anyway, this costs nothing.
- **Pedersen: perfectly hiding, computationally binding.** The commitments are uniform in $G$ whatever $s$ is. A dealer who knows $\log_g h$ could open differently, so $h$ must be generated so that nobody knows it, for example by hashing to the group.
- **Homomorphic.** The product of the commitments of two dealings commits to the sum of the polynomials, and the sum of the shares verifies against it. This is what DKG and threshold protocols use.
- **Threshold on cheaters.** With $n \ge 2t - 1$ the honest parties hold at least $t$ valid shares, so reconstruction succeeds. VSS without computational assumptions needs $n \ge 3t' + 1$ for $t'$ cheaters with perfect security (BGW), and $n \ge 2t' + 1$ with a broadcast channel and a small error probability (Rabin and Ben-Or).

## Variants and improvements

- **Distributed key generation (DKG).** Pedersen's DKG (1991): each party $i$ deals a Feldman sharing of a random $z_i$; the parties disqualify dealers that draw valid complaints; the key is $x = \sum_{i \in \mathrm{QUAL}} z_i$, party $j$ holds $\sum_{i} s_{i,j}$, and the public key is $y = \prod_{i \in \mathrm{QUAL}} C_{i,0}$. Nobody ever knows $x$. Gennaro, Jarecki, Krawczyk and Rabin (1999) showed that $y$ is not uniform: a dishonest party sees the others' $C_{i,0}$ first and then decides whether to make its own dealing fail, which removes its $z_i$ from the sum and lets it choose between two public keys. With one such party it can, for example, make $y$ even with probability about $3/4$. Their fix runs a Pedersen VSS first, which hides the $z_i$ until QUAL is fixed, and publishes the $g^{a_{ij}}$ only after that.
- **Publicly verifiable secret sharing.** Shares are encrypted under each party's public key with proofs of correctness, so anybody can check the dealing (Stadler 1996; Schoenmakers 1999).
- **Proactive VSS.** Shares are refreshed with verifiable sharings of 0, as in proactive [Shamir sharing](/shamir-secret-sharing/).
- **Information-theoretic VSS.** BGW and Rabin-Ben-Or VSS use bivariate polynomials and need no assumption, at the cost of more rounds and an honest majority or two-thirds majority.
- **Asynchronous and high-threshold VSS**, with polynomial commitments such as KZG (see [zk-SNARK](/zk-snark/)) to make the broadcast constant-size.

## When to use it

Use VSS whenever the dealer or the shareholders may be dishonest: in threshold signing and decryption, in distributed key generation, and as a step of MPC protocols for the [malicious model](/malicious-adversary-model/). Use Feldman when $g^s$ is public anyway, for example when $s$ is a signing key, and Pedersen when the secret itself must stay hidden even from unbounded adversaries in the long term. For new threshold signature systems, follow a specified protocol such as FROST rather than combining pieces.

## Pitfalls

- **Feldman reveals $g^s$.** A secret from a small set, such as a PIN, is found by trying every value.
- **A known $\log_g h$.** If the dealer knows $\log_g h$, Pedersen's binding fails and the dealer can give consistent-looking shares of two secrets.
- **Missing the degree check.** The broadcast must have exactly $t$ commitments; extra commitments let the dealer use a polynomial of higher degree, so that $t$ shares no longer fix the secret.
- **Weak complaint handling.** Without a reliable broadcast channel, a dealer can show different commitments to different parties.
- **Biased DKG.** The joint-Feldman DKG gives a non-uniform public key, as above. Use the GJKR protocol when the analysis needs a uniform key.
- **Small subgroups.** The checks only work in a group of prime order; values from outside the subgroup must be rejected.

## Implementations

The Python code on this page implements Feldman and Pedersen VSS with complaints, reconstruction that drops shares that fail the check, the joint-Feldman DKG, and the GJKR bias attack. It uses the toy groups $p = 23$ and $p = 2039$, where anybody can compute discrete logarithms. The tests check the example; that honest shares verify and reconstruct; that every one of the $q - 1$ wrong values of each Feldman share fails; that a bad share is dropped at reconstruction while plain Shamir reconstruction with it gives a wrong secret; that a dealer who knows $\log_g h$ can open Pedersen commitments two ways; that Feldman's $C_0$ gives the secret by search; by enumeration of all randomness in the group of order 11, that one party's view of a Pedersen dealing, with all commitments, is independent of the secret; and that the DKG key matches the shares, while one corrupt dealer makes $y$ even in about $3/4$ of runs against about $1/2$ honestly. There are no official test vectors for VSS, because dealings are random. The code is for study only, is not constant time, and must not be used to protect real data; use a reviewed threshold library built on libsodium or a FIPS 140 validated module.

## History

Chor, Goldwasser, Micali and Awerbuch introduced verifiable secret sharing at FOCS 1985, as a tool for simultaneous broadcast with faulty processors; their scheme was interactive and computational. Ben-Or, Goldwasser and Wigderson (1988) gave information-theoretic VSS for multiparty computation. Paul Feldman's FOCS 1987 paper gave the practical scheme with commitments $g^{a_j}$ and a single round of broadcast. Torben Pryds Pedersen's CRYPTO 1991 paper replaced them with $g^{a_j} h^{b_j}$ for perfect secrecy, and his EUROCRYPT 1991 paper used Feldman sharings to generate threshold keys without a trusted dealer. Gennaro, Jarecki, Krawczyk and Rabin found the bias in that DKG and fixed it at EUROCRYPT 1999.

## References
