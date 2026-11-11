---
tag: 45XBR0
kind: problem
slug: collision-finding
name: Collision finding
aliases:
- finding hash collisions
- quantum collision problem
area: cryptography/hash-functions
level: core
summary: Given a hash function with n-bit output, find two different inputs with the same digest. Generic methods need about 2^(n/2) calls and differ in memory, from 2^(n/2) down to O(1).
prereqs: [collision-resistance, birthday-paradox]
see_also: [birthday-attack, pollard-rho-collision-search, distinguished-points, multicollision-attack, chosen-prefix-collision, preimage-finding, second-preimage-finding, wagners-algorithm]
sources:
  - paper: doi:10.1007/PL00003816
    title: "Paul C. van Oorschot and Michael J. Wiener, Parallel collision search with cryptanalytic applications, Journal of Cryptology 12(1), 1999, pages 1 to 28"
    locator: Section 4 (parallel collision search with distinguished points, run time about sqrt(pi N/2)/m + 2.5/theta) and Section 5 (applications to hash functions)
  - paper: "Gideon Yuval, How to swindle Rabin, Cryptologia 3(3), 1979, pages 187 to 190"
    locator: the attack with two sets of message variants, one fair and one not, and a birthday match between them
  - paper: "Xiaoyun Wang and Hongbo Yu, How to break MD5 and other hash functions, EUROCRYPT 2005, LNCS 3494, pages 19 to 35"
    locator: the differential path and message modification that give MD5 collisions in hours
  - paper: "Marc Stevens, Elie Bursztein, Pierre Karpman, Ange Albertini and Yarik Markov, The first collision for full SHA-1, CRYPTO 2017, LNCS 10401, pages 570 to 596"
    locator: the identical-prefix collision for SHA-1, about 2^63.1 calls of the compression function
  - paper: "Gilles Brassard, Peter Hoyer and Alain Tapp, Quantum cryptanalysis of hash and claw-free functions, LATIN 1998, LNCS 1380, pages 163 to 169"
    locator: the quantum algorithm that finds a collision with O(N^(1/3)) queries
  - paper: doi:10.1145/1008731.1008735
    title: "Scott Aaronson and Yaoyun Shi, Quantum lower bounds for the collision and the element distinctness problems, Journal of the ACM 51(4), 2004, pages 595 to 605"
    locator: the lower bound of order N^(1/3) quantum queries for the collision problem
  - paper: "Daniel J. Bernstein, Cost analysis of hash collisions: will quantum computers make SHARCS obsolete?, SHARCS 2009"
    locator: the comparison of quantum collision search with parallel classical search under a realistic cost model
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.7.1 (attacks on hash functions, the birthday and Yuval attacks)
---

Collision finding is the problem of finding two different inputs $x \ne x'$ with $H(x) = H(x')$ for a given hash function $H$ with $n$-bit output. A hash that resists it is [collision resistant](/collision-resistance/). For a random function, about $2^{n/2}$ calls of $H$ are needed and enough, by the [birthday paradox](/birthday-paradox/). The generic methods differ in memory. A table of all values needs about $2^{n/2}$ entries, cycle finding needs a constant number, and the distinguished points method of van Oorschot and Wiener sits between the two and runs on many machines at once. Cryptanalytic attacks beat the generic bound for broken designs, such as MD5 and SHA-1. With a quantum computer the query bound drops to about $2^{n/3}$, but the cost in hardware does not drop by as much.

## In plain words

A hash turns any message into a short fingerprint. Two different messages with the same fingerprint are a collision. They must exist, because there are more messages than fingerprints.

To find one, you hash many random messages and wait for a repeat. Because any two of them may match, a repeat comes much sooner than you might think: for fingerprints of $n$ bits, after about the square root of the number of fingerprints.

The simple way stores every fingerprint seen. Smarter ways walk in a loop from fingerprint to fingerprint and store almost nothing, at the cost of a few more steps.

## Definition

**Input.** Oracle access to a function $H : D \to \{0,1\}^n$, where $D$ is larger than $\{0,1\}^n$, or the code of $H$.

**Output.** A pair $x, x' \in D$ with $x \ne x'$ and $H(x) = H(x')$.

**Measure.** The number of calls of $H$ (time), the memory, and the success probability. For a generic algorithm, $H$ is modeled as a random function, and the bounds are over its choice.

**The keyed form.** For a fixed unkeyed hash such as SHA-256, a collision exists, so an algorithm with that pair built in succeeds with one step. Formal definitions avoid this in one of two ways. Either $H$ is drawn from a keyed family $\{H_s\}$ and the key $s$ is given to the finder only at the start, as in Katz and Lindell. Or the claim is made about a reduction that turns any explicit collision into a solution of another problem, as in Rogaway's human ignorance approach. See [cryptographic hash function](/cryptographic-hash-function/).

## Variants

- **Identical-prefix collisions.** Given a prefix $P$, find $M \ne M'$ with $H(P \,\|\, M) = H(P \,\|\, M')$. This is the usual form of a cryptanalytic attack on an iterated hash.
- **[Chosen-prefix collisions](/chosen-prefix-collision/).** Given two different prefixes $P$ and $P'$, find $M$ and $M'$ with $H(P \,\|\, M) = H(P' \,\|\, M')$. It is harder, and much more useful to an attacker.
- **Meaningful collisions.** Both inputs must come from a set of acceptable messages, such as two versions of a contract. Yuval (1979) solved it generically: make $2^{n/2}$ variants of each message by small changes, such as spaces or synonyms, and find a match between the two sets.
- **Claw finding.** Given two functions $f$ and $g$, find $x$ and $y$ with $f(x) = g(y)$. It reduces to collision finding on a function that applies $f$ or $g$ depending on one bit of its input, and it is the core of meet in the middle attacks.
- **Near collisions.** Find $x \ne x'$ with $H(x) \oplus H(x')$ of small Hamming weight. Cryptanalytic attacks use near collisions of the compression function as a step.
- **[Multicollisions](/multicollision-attack/).** Find $t$ inputs with one digest. Generic cost about $2^{n(t-1)/t}$, but only $\lceil \log_2 t \rceil \cdot 2^{n/2}$ for iterated hashes, by Joux.
- **The quantum collision problem.** The same problem when $H$ can be queried on a superposition of inputs. In query complexity it is often stated for a function that is either one-to-one or two-to-one.

## Examples

**Truncated SHA-256.** Let $f(x)$ be the top 24 bits of SHA-256 of a salt and the 8 bytes of $x$, with salt `cf`. Each generic method on this page finds a real collision, and the test checks $x \ne x'$ and $f(x) = f(x')$.

| Method | Collision found | Common value | Calls of $f$ | Items stored |
|---|---|---|---|---|
| table | `0x800533`, `0x59262d` | `0x86d078` | 5725 | 5724 |
| rho with Floyd, from 0 | `0x7c2a4c`, `0x2905b7` | `0xf2a9e2` | 10266 | 2 |
| distinguished points, $d = 6$ | `0x566bd5`, `0x8af83d` | `0xd090b0` | 2469 | 48 |

One run is noisy. Over 20 runs with 24 bits and $d = 6$, the averages are:

| Method | Mean calls | Mean stored | Model |
|---|---|---|---|
| table | 5113 | 5111 | $\sqrt{\pi N/2} = 5134$ for both |
| rho with Floyd | 13770 | 2 | about 3 times the table, constant memory |
| distinguished points | 5393 | 81.3 | about $\sqrt{\pi N/2} + 2 \cdot 2^d$ calls, $\text{calls}/2^d \approx 84$ stored |

The distinguished points method uses almost the same number of calls as the table, with 63 times less memory. The rho method saves a little more memory but pays about 2.7 times more calls, because Floyd's method walks the cycle several times. The code is for study only and not constant time, and it attacks only a truncated hash. For real hashing, use SHA-256 or SHA-3 from the standard library, a FIPS 140 validated module, or libsodium.

**Real collisions.** MD5: Wang and Yu (2005) found collisions in hours on a PC, and today they take seconds. SHA-1: Stevens and others (2017) found the first collision, at about $2^{63.1}$ calls, against the generic $2^{80}$. No collision is known for SHA-256, SHA-512, SHA-3 or BLAKE2.

## Known algorithms

| Algorithm | Calls of $H$ | Memory | Notes |
|---|---|---|---|
| [birthday attack](/birthday-attack/) with a table | $\sqrt{\pi N/2}$ on average | the same | simple; the memory is the limit |
| sort and scan | $q$ values, then sort | $q$ | the same, with no hash table |
| [Pollard rho](/pollard-rho-collision-search/) (Floyd or Brent) | a small multiple of $\sqrt{N}$ | $O(1)$ | the start must not be on the cycle |
| parallel search with [distinguished points](/distinguished-points/) | $\sqrt{\pi N/2}/m + 2.5 \cdot 2^d$ per machine | about $\sqrt{N}/2^d$ | van Oorschot and Wiener 1999; $m$ machines, no communication but the found points |
| Yuval's attack | $2 \cdot 2^{n/2}$ | $2^{n/2}$ or less with rho | meaningful collisions |
| differential cryptanalysis | from seconds (MD5) to $2^{63.1}$ (SHA-1) | small | specific to a design |
| Brassard, Hoyer and Tapp | $O(N^{1/3})$ quantum queries | $O(N^{1/3})$ quantum memory | Grover search on a table |

Here $N = 2^n$. The parallel method is the one used for large generic searches: each machine walks from random starts until a point with $d$ zero bits, and sends that point to a central list. Two walks that reach one point have merged, and replaying them gives the collision.

## Bounds

- **Classical upper bound.** $O(2^{n/2})$ calls and $O(1)$ memory, by the rho method, for any $H$ that behaves like a random function.
- **Classical lower bound.** With a random oracle, $q$ queries find a collision with probability at most $q(q-1)/2^{n+1}$. So $\Omega(2^{n/2})$ queries are needed for a constant success probability.
- **Quantum bounds.** Brassard, Hoyer and Tapp give $O(2^{n/3})$ queries. Aaronson and Shi show $\Omega(N^{1/3})$ queries for two-to-one functions, and Zhandry (2015) shows the same order for random functions. The algorithm needs $2^{n/3}$ memory with fast quantum access. Bernstein (2009) argued that, when hardware is counted, parallel classical rho with $2^{n/6}$ machines finds a collision in time about $2^{n/3}$ too, so the quantum advantage is small.
- **Specific functions.** No better general bound exists. A collision resistant function is assumed, not proven, and its existence implies that one-way functions exist.

## Reductions

- **From second preimages.** An algorithm for [second preimage finding](/second-preimage-finding/) gives a collision: pick a random $x$ and find $x' \ne x$ with $H(x') = H(x)$. So collision finding is never harder.
- **To the compression function.** By the Merkle-Damgard theorem, a collision in a [Merkle-Damgard](/merkle-damgard-construction/) hash with length padding gives a collision in its compression function. Attacks therefore aim at the compression function.
- **From claw finding.** Claw finding on $f$ and $g$ reduces to collision finding on $h(b, x) = f(x)$ if $b = 0$ and $g(x)$ if $b = 1$. Half of the collisions of $h$ are claws.
- **Related problems.** Collision finding is a special case of element distinctness, with the input given by a function. The [generalized birthday problem](/generalized-birthday-problem/) asks for $k$ values with XOR zero instead of two equal values.

## Applications

- **Breaking hash-then-sign.** A collision $H(x) = H(x')$ lets a signature on $x$ serve for $x'$. Yuval's attack and the rogue certificate built with MD5 (see [chosen-prefix collision](/chosen-prefix-collision/)) are examples.
- **Setting parameters.** The birthday bound is why a hash for signatures needs $n \ge 256$ for 128-bit security, and why block cipher modes with 64-bit blocks must change keys well before $2^{32}$ blocks.
- **Other cryptanalysis.** The same parallel search finds discrete logarithms with Pollard's rho, keys of double encryption by meet in the middle, and states of stream ciphers.
- **Testing designs.** Collision search on reduced-round or truncated versions measures the security margin of a new hash.

## References
