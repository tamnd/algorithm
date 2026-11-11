---
tag: VBNYFB
kind: algorithm
slug: pedersen-commitment
name: Pedersen commitment
aliases:
- Pedersen commitment scheme
area: cryptography/protocols
level: advanced
summary: "Commit to m as C = g^m h^r in a prime order group. Perfectly hiding, binding if discrete log is hard, and additively homomorphic. Nobody may know log_g h."
solves: [commitment-scheme]
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 1991
  people: [Torben Pryds Pedersen]
  note: Introduced at CRYPTO 1991 as the building block of a verifiable secret sharing scheme with information-theoretic secrecy.
prereqs: [commitment-scheme, discrete-logarithm-problem, cyclic-group]
see_also: [verifiable-secret-sharing, sigma-protocol, safe-prime, modular-exponentiation, homomorphic-encryption, elgamal-encryption, zk-snark, fair-coin-flipping]
sources:
  - paper: doi:10.1007/3-540-46766-1_9
    title: Torben Pryds Pedersen, Non-interactive and information-theoretic secure verifiable secret sharing, CRYPTO 1991, LNCS 576, Springer, 1992, pages 129 to 140
    locator: the commitment E(s, t) = g^s h^t, its hiding and binding properties, and its use in the verifiable secret sharing scheme
  - paper: "Benedikt Bunz, Jonathan Bootle, Dan Boneh, Andrew Poelstra, Pieter Wuille and Greg Maxwell, Bulletproofs: short proofs for confidential transactions and more, IEEE Symposium on Security and Privacy 2018, pages 315 to 334"
    locator: the vector Pedersen commitment and the inner product argument over it, used for range proofs
  - paper: doi:10.1109/SFCS.1987.4
    title: Paul Feldman, A practical scheme for non-interactive verifiable secret sharing, 28th IEEE Symposium on Foundations of Computer Science (FOCS), 1987, pages 427 to 437
    locator: the commitments g^(a_j) to the coefficients, which reveal g^s
  - url: "https://cs.au.dk/~ivan/ComZK06.pdf"
    title: Ivan Damgard and Jesper Buus Nielsen, Commitment schemes and zero-knowledge protocols, lecture notes, Aarhus University
    locator: the section on commitment schemes from the discrete logarithm problem (the scheme g^m h^r, unconditionally hiding and computationally binding)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: the chapters on number theory and cryptographic hardness assumptions (prime order subgroups of Z_p^* and the discrete logarithm problem)
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: the chapters on protocols for identification and on zero knowledge, where Pedersen commitments and their homomorphism are used
---

A Pedersen commitment to a number $m$ is the group element $C = g^m h^r$, where $g$ and $h$ are two generators of a group of prime order $q$ and $r$ is a uniform random exponent. It solves the [commitment problem](/commitment-scheme/) with *perfect* hiding: $C$ is uniform in the group whatever $m$ is. It is *computationally* binding: a committer who opens $C$ two ways has found $\log_g h$, so binding holds if the [discrete logarithm problem](/discrete-logarithm-problem/) is hard. Commitments multiply to a commitment of the sum, which makes the scheme the base of [verifiable secret sharing](/verifiable-secret-sharing/), of many [sigma protocols](/sigma-protocol/) and of range proofs such as Bulletproofs.

**Notation.** $G$ is a [cyclic group](/cyclic-group/) of prime order $q$ with generators $g$ and $h$; $t = \log_g h$ is the *trapdoor*, which nobody may know. Here $G$ is the subgroup of squares of $\mathbb{Z}_p^*$ for a [safe prime](/safe-prime/) $p = 2q + 1$. Messages and randomness are in $\mathbb{Z}_q$. $\lambda$ is the security parameter, $A$ an adversary with running time $t_A$.

## In plain words

Take two fixed public numbers that nobody can relate to each other. To commit to a value, raise the first number to the value, raise the second number to a fresh random exponent, and multiply. The random part spreads the result evenly over all possible outputs, so the commitment says nothing about the value, even to someone with unlimited computing power.

To cheat, the committer would need a second value and a second random exponent that give the same product. Doing that is the same as finding how the two public numbers relate, which is the hard discrete logarithm problem.

Two commitments multiplied together are a commitment to the sum of the values. This lets others check sums and other linear facts about hidden values.

## The problem

The scheme solves the [commitment scheme](/commitment-scheme/) problem: commit to $m \in \mathbb{Z}_q$ so that the commitment hides $m$ and the committer cannot later open it to another value. Pedersen's choice is perfect hiding with computational binding; the commitment problem page shows that the two cannot both be perfect.

## The algorithm

```pseudo id=main
SETUP(λ)
L1  choose a safe prime p = 2q + 1 with q prime;  g ← a square mod p other than 1
L2  h ← HASH-TO-GROUP("generator h")         ▷ nobody learns log_g h

COMMIT(m)
L3  r ← uniform in Z_q;  C ← g^m · h^r mod p;  return (C, r)

OPEN(C, m, r)
L4  if not (0 < C < p) then return false
L5  if C^q mod p ≠ 1 then return false        ▷ C must be in the subgroup of order q
L6  return C = g^m · h^r mod p
```

HASH-TO-GROUP hashes the seed with a counter, reduces mod $p$ and squares, until the result is not 0 or 1. Squaring lands in the subgroup of order $q$, because the squares of $\mathbb{Z}_p^*$ form the unique subgroup of index 2. The seed is public, so anyone can check that $h$ came from it, and nobody chose $h$ with a known logarithm.

**Homomorphism.** $\mathrm{COMMIT}(m_1; r_1) \cdot \mathrm{COMMIT}(m_2; r_2) = \mathrm{COMMIT}(m_1 + m_2; r_1 + r_2)$, and $C^k$ is a commitment to $k m$ with randomness $k r$.

**Vector form.** With independent generators $g_1, \ldots, g_n, h$ (all from hashing), $C = h^r \prod_{i=1}^n g_i^{m_i}$ commits to the vector $(m_1, \ldots, m_n)$ with one group element. It is still perfectly hiding, and binding holds if no one can find a non-trivial discrete log relation among the generators, which is as hard as discrete log. Bulletproofs (Bunz et al. 2018) commit to the binary digits of a value in this way and prove with an inner product argument of $O(\log n)$ group elements that the committed vector satisfies a relation, for example that a hidden amount lies in $[0, 2^{64})$.

## Example

Take $p = 2039$, $q = 1019$. The code hashes the seeds to get $g = 1280$ and $h = 1926$. In this tiny group a search finds $\log_g h = 772$, but nobody chose $h$ that way, and in a real group the search is infeasible.

| step | value |
|---|---|
| commit to $m_1 = 5$ with $r_1 = 77$ | $C_1 = 1280^5 \cdot 1926^{77} \bmod 2039 = 823$ |
| commit to $m_2 = 8$ with $r_2 = 100$ | $C_2 = 836$ |
| product | $C_1 C_2 \bmod 2039 = 885$ |
| commit to $13$ with $r = 177$ | $885$, the same value |

For every $m$, the 1019 values of $r$ give the 1019 elements of the group, each exactly once, so $C$ carries no information on $m$.

**The trapdoor attack.** Now let the committer choose $h = g^{777} = 725$ itself. It commits to $m = 10$ with $r = 20$ and gets $C = 1285$. Later it opens $C$ to $m' = 500$ with $r' = 20 + (10 - 500) \cdot 777^{-1} \bmod 1019 = 561$, and indeed $1280^{500} \cdot 725^{561} \bmod 2039 = 1285$. This is why $h$ must come from a public hash or a trusted setup, never from the committer.

## Correctness

OPEN accepts an honest $(C, m, r)$ because line L6 recomputes the product of line L3. Perfect hiding holds because $r \mapsto g^m h^r = g^{m + t r}$ is a bijection from $\mathbb{Z}_q$ onto $G$ when $t \ne 0$. Binding reduces tightly to discrete log: two openings $(m, r) \ne (m', r')$ give $t = (m - m')/(r' - r) \bmod q$. The full proof, with the homomorphism, the trapdoor and the vector form, is below.

## Complexity

Let $n$ be the number of binary digits of $q$ (and about of $p$).

- **Commit and open**: two modular exponentiations with exponents of $n$ binary digits, or one double exponentiation $g^m h^r$ by Shamir's trick, which shares the squarings. With schoolbook multiplication each exponentiation costs $\Theta(n)$ multiplications of $\Theta(n^2)$ word operations, so $\Theta(n^3)$ in total.
- **Membership check** (line L5): one more exponentiation $C^q$. On an elliptic curve of prime order it is a cheap point check instead.
- **Vector form**: one multi-exponentiation of $k + 1$ terms for a vector of length $k$. Done term by term it costs $k + 1$ exponentiations; multi-exponentiation methods share the squarings and do better.
- **Sizes**: one group element per commitment, and one element of $\mathbb{Z}_q$ of randomness to keep.

## Properties

- **Perfectly hiding.** Even a receiver with unlimited time, and even one who knows $t$, learns nothing about $m$ from $C$.
- **Computationally binding, with a tight reduction.** An adversary that opens two ways with probability $\varepsilon$ in time $t_A$ gives a discrete log solver with probability $\varepsilon$ and time $t_A + O(1)$ group operations.
- **Additively homomorphic** in $m$ and $r$.
- **Equivocal with the trapdoor.** Whoever knows $t$ can open to anything. Simulators in zero-knowledge proofs use this, and it is fatal if the committer knows $t$.
- **Not non-malleable.** From $C$ anyone can make $C \cdot g$, a commitment to $m + 1$ that opens when the original does. Protocols that need non-malleability add a proof of knowledge of the opening.

## Variants and improvements

- **Elliptic curve form.** $C = mG + rH$ on a curve of prime order such as Ristretto255 or secp256k1. This is what real systems use: elements are 32 bytes.
- **Vector Pedersen commitment.** One element commits to a whole vector; see above.
- **[Verifiable secret sharing](/verifiable-secret-sharing/).** Pedersen's 1991 scheme commits to each coefficient of the sharing polynomial with $g^{a_j} h^{b_j}$, so that the shares can be checked while the secret stays perfectly hidden.
- **ElGamal-type commitment.** $(g^r, g^m h^r)$ adds one element and swaps the guarantees: perfectly binding, and hiding only under [decisional Diffie-Hellman](/decisional-diffie-hellman/).
- **[Sigma protocols](/sigma-protocol/) on commitments.** Proofs that a commitment opens to 0 or 1, that two commitments hold equal values, or that a hidden value lies in a range all use the homomorphism.

## When to use it

Use a Pedersen commitment when the hidden value must stay secret forever, even against future computers, and when protocols must compute on committed values: confidential amounts, range proofs, verifiable secret sharing, voting. Binding then rests on discrete log, and it falls to a quantum computer that runs Shor's algorithm, which can open old commitments to other values. If long-term binding matters more than hiding, use a hash commitment or an ElGamal-type commitment. In practice use a reviewed library on a prime order curve (for example Ristretto255 in libsodium), not hand-written group code.

## Pitfalls

- **A known trapdoor.** If the committer can choose $h$ or knows $\log_g h$, it can open to any value (shown above and in the tests). Derive $h$ from a public seed by hashing, and publish the seed.
- **$h$ derived as a power of $g$.** Setting $h = g^{H(\text{seed})}$ looks random but has a known logarithm. The hash must map to a group element directly.
- **No membership check.** In $\mathbb{Z}_p^*$ an element outside the subgroup of order $q$ (for example $p - 1$, of order 2) can leak information or break proofs. Check $C^q = 1$ (line L5) or use a prime order curve.
- **Reused randomness.** Two commitments with the same $r$ give $C_1 / C_2 = g^{m_1 - m_2}$, which reveals $m_1 - m_2$ for small values and equality in general.
- **Small message spaces and exposed $r$.** Hiding protects $m$ only while $r$ stays secret; once $r$ is known, a small $m$ follows by search over $g^m$.
- **Messages larger than $q$.** $m$ and $m + q$ give the same commitment. Fix the encoding into $\mathbb{Z}_q$.

## Implementations

The Python code on this page implements the scheme, the homomorphism, the vector form and the trapdoor attack in the subgroup of a toy safe prime ($p = 2039$) and of a 128-bit safe prime. The tests check opening, perfect hiding by enumeration of all $r$ in the toy group, the homomorphism, the attack with a known trapdoor, the recovery of $\log_g h$ from two openings, and the vector form. There are no official test vectors for Pedersen commitments; the tests check algebraic properties instead. The code is for study only, is not constant time, uses groups far too small for real use, and must not be used to protect real data. Use libsodium (Ristretto255) or a FIPS 140 validated module.

## History

Torben Pryds Pedersen gave the commitment at CRYPTO 1991 in the paper "Non-interactive and information-theoretic secure verifiable secret sharing". Feldman's verifiable secret sharing of 1987 had published $g^s$ and so revealed some information on the secret; Pedersen's commitments made the scheme perfectly hiding. The same commitment later became a standard tool in sigma protocols, electronic cash and voting. Bunz, Bootle, Boneh, Poelstra, Wuille and Maxwell used the vector form for Bulletproofs (IEEE Symposium on Security and Privacy 2018), short range proofs that hide transaction amounts.

## References
