---
tag: X7XC7T
kind: problem
slug: pseudorandom-generation
name: Pseudorandom generation
aliases:
- PRG construction
area: randomized/derandomization
level: core
summary: Given a short seed, produce a long string that a stated class of tests cannot tell from uniform. The class of tests and the time the generator may use decide which constructions exist.
prereqs: [randomized-algorithm, bpp, boolean-circuit, total-variation-distance]
see_also: [pseudorandom-generator, computational-indistinguishability, hill-prg-from-one-way-functions, nisan-prg, nisan-wigderson-generator, hardness-versus-randomness, hitting-set-generator, cryptographically-secure-prng]
sources:
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 7, Pseudorandom Generators (the definition, cryptographic generators, hybrid arguments, generators from hardness), and Chapter 3 (pairwise independence and small sample spaces)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 9 (cryptographic pseudorandom generators), Chapter 20 (derandomization and the Nisan-Wigderson generator) and Chapter 21 (generators for space-bounded computation)
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Chapter 3, Pseudorandom Generators
  - paper: doi:10.1007/BF01305237
    title: Noam Nisan, Pseudorandom generators for space-bounded computation, Combinatorica 12(4), 1992
    locator: the main theorem (seed O(S log R) for space S and R random bits)
  - paper: doi:10.1016/S0022-0000(05)80043-1
    title: Noam Nisan and Avi Wigderson, Hardness vs randomness, Journal of Computer and System Sciences 49(2), 1994
    locator: the generator from a hard function and its use for derandomization
---

Pseudorandom generation is the problem of building a deterministic map $G : \{0,1\}^d \to \{0,1\}^m$ with $d < m$ whose output on a uniform seed passes every test of a stated class. The answer depends on two choices: who the adversary is (all efficient algorithms, circuits of a fixed size, small-space machines, linear tests) and how long the generator may run compared with the adversary. These choices give the cryptographic generators of [Yao](/yao-next-bit-unpredictability/) and [HILL](/hill-prg-from-one-way-functions/), the complexity-theoretic generators of [Nisan and Wigderson](/nisan-wigderson-generator/), the space-bounded generator of [Nisan](/nisan-prg/), and unconditional generators for weak tests such as [small-bias generators](/small-bias-generator/). This page is the map of these kinds. The object itself is defined on [pseudorandom generator](/pseudorandom-generator/), and the notion of "cannot tell apart" on [computational indistinguishability](/computational-indistinguishability/).

## In plain words

A program that flips coins needs many random bits. True random bits are expensive. A pseudorandom generator takes a few true random bits, the seed, and stretches them into many bits that look random.

"Look random" must be made exact, because no fixed output is random. We name a class of tests, for example all fast programs, or all programs with little memory. The output is good if no test in the class behaves differently on it than on true random bits, except with a tiny difference.

The weaker the tests, the easier the job. Against tests that only look at a few positions, simple algebra is enough, and nothing is assumed. Against all fast programs, we only know how to do it if some problem is hard to solve, for example if a one-way function exists.

## Definition

Notation: $U_m$ is the uniform distribution on $\{0,1\}^m$, and $\Pr$ and $E$ are probability and expectation. For a class $\mathcal{T}$ of tests $D : \{0,1\}^m \to \{0,1\}$ and an error $\varepsilon \ge 0$, a function $G : \{0,1\}^d \to \{0,1\}^m$ *$\varepsilon$-fools* $\mathcal{T}$ if

$$\big|\Pr[D(G(U_d)) = 1] - \Pr[D(U_m) = 1]\big| \le \varepsilon \quad \text{for every } D \in \mathcal{T}.$$

**Input.** The output length $m$, the error $\varepsilon$, and a class $\mathcal{T}$ (given by a size, time or space bound).

**Output.** An algorithm that computes $G(s)$ from $s \in \{0,1\}^d$, such that $G$ $\varepsilon$-fools $\mathcal{T}$.

**Goals.** Make the seed length $d$ small, and make $G$ fast or small-space. The quantity $m - d$ is the *stretch*.

A string has no randomness on its own, so the definition always speaks of the distribution $G(U_d)$, never of one output.

## Variants

The kinds differ in the adversary, in the time the generator may use, and in the assumption that they need.

| kind | the tests | time of $G$ | seed for output $m$ | assumption |
|---|---|---|---|---|
| cryptographic ([HILL](/hill-prg-from-one-way-functions/)) | every probabilistic polynomial-time algorithm, in the seed length | polynomial in $d$, less than the tests may use | $d = m^{c}$ for each constant $c > 0$ | one-way functions (equivalent) |
| complexity-theoretic ([NW](/nisan-wigderson-generator/)) | circuits of size $m$ | $2^{O(d)}$, so more than the tests | $O(\log m)$ | a function in E with circuit complexity $2^{\Omega(n)}$ |
| space-bounded ([Nisan](/nisan-prg/)) | read-once branching programs of width $w$ and length $m$ | space $O(d)$ | $O(\log m \cdot \log(mw/\varepsilon))$ | none |
| [small-bias](/small-bias-generator/) | parities of output bits | polynomial | $O(\log m + \log(1/\varepsilon))$ | none |
| [$k$-wise independent](/k-wise-independence/) | tests that read $k$ positions ($\varepsilon = 0$) | polynomial | $O(k \log m)$ | none |
| statistical ([PRNG](/pseudorandom-number-generator/)) | a fixed battery of statistical tests | very fast | a few hundred bits | no proof at all |

The first two rows are conditional and the next three are unconditional.

- **Who runs longer.** A cryptographic generator runs in less time than the adversary, because it must be secure against parties with more power than the honest user. For derandomization the test is a fixed algorithm that is known in advance, so the generator may run longer than the test. This is why the Nisan-Wigderson generator can use a hard function from E, while a cryptographic generator needs a one-way function.
- **Hitting-set generators.** A [hitting-set generator](/hitting-set-generator/) only promises that each test that accepts at least half of all strings accepts some output. This is the one-sided version, enough for [RP](/rp/).
- **Cryptographic practice.** A [cryptographically secure PRNG](/cryptographically-secure-prng/) such as [ChaCha20](/chacha20/) is a cryptographic generator in use. Its security is a conjecture about one fixed function, not a reduction to a one-way function. The [Blum-Micali](/blum-micali/) and [Blum-Blum-Shub](/blum-blum-shub/) generators are reductions, but slow.

## Examples

**A generator for 2-wise independence.** Take $q$ prime and the seed $(a, b) \in \mathbb{Z}_q^2$, that is $d = 2 \lceil \lg q \rceil$ bits. Output $G(a, b) = (a + b \cdot i \bmod q)_{i = 0, \ldots, q-1}$. For $i \ne j$, the map $(a, b) \mapsto (a + bi, a + bj)$ is a bijection of $\mathbb{Z}_q^2$, so each pair of outputs is uniform on $\mathbb{Z}_q^2$. With $q = 7$, a seed of 6 bits gives 7 values that fool every test that reads two values, with error 0. A test that reads three values breaks it: $x_2 - 2x_1 + x_0 = 0$ always holds.

**A seed against all fast tests needs an assumption.** If $G : \{0,1\}^d \to \{0,1\}^{d+1}$ is computable in time $T$, the test "is $z$ in the image of $G$?" runs in time $2^d T$ by trying all seeds. It accepts $G(U_d)$ always and $U_{d+1}$ with probability at most $1/2$. So a generator can only fool tests that run in less time than this search. Cryptographic generators make the search too expensive; complexity-theoretic generators make the tests smaller than the search.

**Derandomization by enumeration.** Let $A(x, r)$ be a [BPP](/bpp/) algorithm with error at most $1/3$ that uses $m$ random bits. Fix the input $x$, and let $D_x(r) = 1$ when $A(x, r)$ gives the right answer. If $G$ $\varepsilon$-fools $D_x$ with $\varepsilon < 1/6$, then $\Pr_s[D_x(G(s)) = 1] \ge 2/3 - \varepsilon > 1/2$. So the majority of $A(x, G(s))$ over all $2^d$ seeds is the right answer, and the time is $2^d$ times the time of $G$ and $A$. With $d = O(\log n)$ and $G$ computable in polynomial time, this is a deterministic polynomial-time algorithm. The test $D_x$ has $x$ built in and is a circuit of polynomial size, which is why complexity-theoretic generators fool circuits and not only uniform algorithms.

## Known algorithms

- [Blum-Micali](/blum-micali/) and the general one-way permutation construction: one hard-core bit per application of the permutation. See [HILL](/hill-prg-from-one-way-functions/), which also gives the general one-way function case.
- Stretch extension: a generator with stretch one bit gives any polynomial stretch ([pseudorandom generator](/pseudorandom-generator/)).
- [Nisan-Wigderson generator](/nisan-wigderson-generator/): a hard function evaluated on the sets of a combinatorial design. Seed $O(\log m)$ under exponential hardness ([Impagliazzo-Wigderson theorem](/impagliazzo-wigderson-theorem/)).
- [Nisan's generator](/nisan-prg/): recursive use of pairwise independent hash functions, seed $O(\log^2 m)$ for logspace tests.
- [Small-bias generators](/small-bias-generator/) and [$k$-wise independent](/k-wise-independence/) sample spaces: algebraic and unconditional.
- [Expander walks](/expander-walk-sampler/): generators for sampling, with fewer random bits than independent samples.

## Bounds

- **Counting gives short seeds.** A uniformly random function $G : \{0,1\}^d \to \{0,1\}^m$ $\varepsilon$-fools all circuits of size $t \ge m$ with high probability when $d = \lg t + \lg \lg t + 2 \lg(1/\varepsilon) + O(1)$. Reason: there are at most $2^{c\, t \log t}$ circuits of size $t$ for a constant $c$. For one fixed circuit, the [Hoeffding inequality](/hoeffding-inequality/) over the $2^d$ independent outputs gives failure probability at most $2e^{-2 \cdot 2^d \varepsilon^2}$. A [union bound](/union-bound/) over all circuits is below 1 for this $d$. Such a $G$ is not explicit, and it takes time about $2^{m}$ to find one.
- **The error is at least about $2^{-d}$.** If $m > d$, fix a seed $s_0$. The test $D(z) = [z = G(s_0)]$ is a circuit of size $O(m)$, and $\Pr[D(G(U_d)) = 1] - \Pr[D(U_m) = 1] \ge 2^{-d} - 2^{-m} \ge 2^{-d-1}$. So $d \ge \lg(1/\varepsilon) - 1$.
- **Exhaustive search breaks every generator.** As in the examples, a test with time $2^d T$ breaks a generator with time $T$. So any claim of pseudorandomness is relative to a bound on the tests.

## Reductions

- One-way functions exist if and only if cryptographic generators exist ([HILL](/hill-prg-from-one-way-functions/) and the converse there).
- Pseudorandomness is equivalent to next-bit unpredictability, with a loss of a factor $m$ in the advantage ([Yao](/yao-next-bit-unpredictability/)).
- A generator with stretch 1 gives stretch $\ell$ for each polynomial $\ell$, with the error multiplied by $\ell$ ([pseudorandom generator](/pseudorandom-generator/)).
- A cryptographic generator with stretch $2d$ gives a [pseudorandom function](/pseudorandom-function/) by the tree construction of Goldreich, Goldwasser and Micali.
- A complexity-theoretic generator with seed $O(\log m)$ that runs in time $2^{O(d)}$ gives a function in E with circuit complexity $2^{\Omega(n)}$, and the converse also holds ([hardness versus randomness](/hardness-versus-randomness/)).
- A generator that fools a class with error $\varepsilon < 1/2$ is also a [hitting-set generator](/hitting-set-generator/) for that class.

## Applications

- **Derandomization.** P = BPP under circuit lower bounds for E ([Impagliazzo-Wigderson theorem](/impagliazzo-wigderson-theorem/)), and unconditional results for space, such as the use of Nisan's generator in [RL versus L](/rl-versus-l/).
- **Cryptography.** Stream ciphers, encryption with short keys and [semantic security](/semantic-security/) all rest on generators that fool efficient adversaries.
- **Saving random bits.** Sampling, hashing and load balancing with $k$-wise independent or small-bias bits use $O(\log m)$ random bits instead of $m$.
- **Lower bounds.** A good generator for a class implies a function that the class cannot compute, so constructions and lower bounds are two views of the same question.

## References
