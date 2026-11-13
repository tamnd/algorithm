---
tag: YTWPC3
kind: problem
slug: bernstein-vazirani-problem
name: Bernstein-Vazirani problem
area: quantum/quantum-primitives
level: intro
summary: Recover a hidden bit string s from an oracle for f(x) = s . x mod 2. One quantum query is enough, and every classical algorithm with bounded error needs n queries.
prereqs: [quantum-oracle, query-complexity]
see_also: [bernstein-vazirani-algorithm, deutsch-jozsa-problem, simon-problem, hadamard-code, learning-parity-with-noise, quantum-query-complexity, randomized-query-complexity, yao-minimax-principle]
sources:
  - paper: doi:10.1145/167088.167097
    title: "Ethan Bernstein and Umesh Vazirani, Quantum complexity theory, Proceedings of the 25th Annual ACM Symposium on Theory of Computing (STOC 1993), pages 11-20, 1993"
    locator: the conference version; the problem of finding s from the function x -> s . x and its recursive form
  - paper: doi:10.1137/S0097539796300921
    title: "Ethan Bernstein and Umesh Vazirani, Quantum complexity theory, SIAM Journal on Computing 26(5):1411-1473, 1997"
    locator: the journal version, which this page follows; the section on the recursive Fourier sampling problem and the oracle separation (section number not checked)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 2 (the Bernstein-Vazirani problem, after the Deutsch-Jozsa problem)
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 6 (introductory quantum algorithms in the query model)
---

The Bernstein-Vazirani problem asks for a hidden string $s \in \{0,1\}^n$, given an oracle for the function $f(x) = s \cdot x \bmod 2$. Each classical query gives one bit of information about $s$, so every classical algorithm needs $n$ queries, even with randomness and bounded error. One quantum query is enough, with no error. A recursive form of the problem gave the first superpolynomial separation between bounded-error quantum and classical query complexity. This page is about the problem and its bounds; the one-query method is the [Bernstein-Vazirani algorithm](/bernstein-vazirani-algorithm/).

## In plain words

A box hides a secret string of bits. You give the box a string of the same length. The box looks at the places where both strings have a 1, counts them, and tells you only whether the count is odd or even. You must find the secret.

A classical program can ask with a string that has a single 1. The answer is then one bit of the secret. It asks once for each place, so it needs as many questions as the secret has bits. No classical trick does better, because each answer is only one bit, and guessing the rest is right only by luck.

A quantum program asks once, about all strings at the same time. The answers come back as signs, and one more step turns the pattern of signs into the secret itself.

## Definition

**Input.** An integer $n \ge 1$ and oracle access to a function $f : \{0,1\}^n \to \{0,1\}$.

**Promise.** There is a string $s \in \{0,1\}^n$ with $f(x) = s \cdot x$ for all $x$, where $s \cdot x = \sum_j s_j x_j \bmod 2$. In the variant with a constant, $f(x) = s \cdot x \oplus c$ for some $c \in \{0,1\}$.

**Output.** The string $s$.

**Access.** A classical query names $x$ and gets $f(x)$. A quantum query applies the bit oracle $U_f |x\rangle|b\rangle = |x\rangle|b \oplus f(x)\rangle$ or the phase oracle $O_f |x\rangle = (-1)^{f(x)} |x\rangle$; see [quantum oracle](/quantum-oracle/). They are equal in power up to one ancilla, by [phase kickback](/phase-kickback/). The cost is the number of queries in the classical [query model](/query-model/) or the [quantum query model](/quantum-query-model/).

**Strings.** We write $x = x_{n-1} \cdots x_0$, and qubit $j$ holds $x_j$, as on [quantum state](/quantum-state/). The string $e_j$ has a single $1$ at place $j$.

The truth table of $f$ is the codeword of $s$ in the [Hadamard code](/hadamard-code/): it lists $s \cdot x$ for all $2^n$ strings $x$. So the problem asks to decode a Hadamard codeword without errors, with as few looks at its positions as possible.

## Variants

- **With a constant.** For $f(x) = s \cdot x \oplus c$, the output is $s$ (and $c$ if wanted). One more classical query, $f(0) = c$, finds $c$.
- **Deciding $s = 0$.** The function $s \cdot x$ is constant when $s = 0$ and balanced when $s \ne 0$. So these inputs obey the promise of the [Deutsch-Jozsa problem](/deutsch-jozsa-problem/).
- **Other moduli.** For $f : \mathbb{Z}_d^n \to \mathbb{Z}_d$ with $f(x) = s \cdot x \bmod d$, the output is $s \in \mathbb{Z}_d^n$. A classical algorithm still needs $n$ queries, because each answer $s \cdot x$ is one linear equation in $s$ and $n$ unknowns need $n$ equations.
- **Recursive Fourier sampling.** Bernstein and Vazirani built a tree of instances of height $h$: the answer of each instance is the input of an instance one level up. The quantum cost grows like $2^h$ queries, and the classical cost grows like $n^{\Omega(h)}$. With $h$ about $\log n$, this gives a superpolynomial gap between bounded-error quantum and classical query complexity.
- **Random noisy examples.** If the solver gets random $x$ with $s \cdot x$ flipped with a fixed probability, instead of chosen queries, the problem is [learning parity with noise](/learning-parity-with-noise/). It is a different problem, believed to be hard for classical and quantum algorithms.

## Examples

**$n = 3$ and $s = 101$.** Then $f(x) = x_0 \oplus x_2$. For $x = 0, 1, \ldots, 7$ the truth table is $0, 1, 0, 1, 1, 0, 1, 0$. The classical queries $f(e_0) = f(001) = 1$, $f(e_1) = f(010) = 0$ and $f(e_2) = f(100) = 1$ give $s = 101$.

**Two queries for $n = 3$ leave two candidates.** Ask $f(011) = s_0 \oplus s_1$ and $f(110) = s_1 \oplus s_2$. For $s = 101$ the answers are $1$ and $1$. The strings $s$ with $s_0 \oplus s_1 = 1$ and $s_1 \oplus s_2 = 1$ are $010$ and $101$. Both remain, so a third query is needed to be sure. In general $q$ answers are $q$ linear equations over GF(2), and at least $2^{n-q}$ strings satisfy them.

**The Fourier view.** The Walsh-Hadamard coefficients $\hat{F}(y) = 2^{-n} \sum_x (-1)^{f(x) + x \cdot y}$ of $f(x) = s \cdot x$ are $\hat{F}(s) = 1$ and $\hat{F}(y) = 0$ for $y \ne s$. So the whole Fourier spectrum of $(-1)^f$ sits on the single point $s$. A quantum algorithm that samples from the squared spectrum finds $s$ with certainty. See the [Walsh-Hadamard transform](/walsh-hadamard-transform/).

## Known algorithms

- **Classical, deterministic.** Ask $f(e_j)$ for $j = 0, \ldots, n-1$; then $s_j = f(e_j)$. This uses $n$ queries, or $n + 1$ in the variant with a constant, where $s_j = f(e_j) \oplus f(0)$.
- **Classical, any $n$ independent queries.** Ask $n$ strings $x^{(1)}, \ldots, x^{(n)}$ that are linearly independent over GF(2), and solve the [linear system modulo 2](/linear-system-modulo-2/) $x^{(i)} \cdot s = f(x^{(i)})$ by [Gaussian elimination](/gaussian-elimination-modular/) in $O(n^3)$ time.
- **Quantum, exact.** The [Bernstein-Vazirani algorithm](/bernstein-vazirani-algorithm/) uses one query to the bit oracle, $n + 1$ qubits and $2n + 2$ one-qubit gates, and returns $s$ with probability $1$.

## Bounds

| model | queries | tight |
|---|---|---|
| classical, deterministic | $n$ | yes |
| classical, bounded error $1/3$ | $n$ | yes |
| classical, $q$ queries | success at most $2^{q-n}$ | yes |
| quantum, exact | $1$ | yes |

**Classical lower bound.** We use the [Yao minimax principle](/yao-minimax-principle/): the worst-case success of a randomized algorithm is at most the success of the best deterministic algorithm on a random input. Let $s$ be uniform on $\{0,1\}^n$, and fix a deterministic algorithm with $q$ queries. On each run, the algorithm sees answers $f(x^{(i)}) = x^{(i)} \cdot s$, so after $q$ queries the strings that agree with all answers form the solution set of $q$ linear equations in $s$. This set holds the true $s$, so it is an affine subspace of dimension at least $n - q$, with at least $2^{n-q}$ elements. Given the answers, $s$ is uniform on this set, because the prior is uniform and each consistent $s$ gives the same answers. So the output is right with probability at most $2^{-(n-q)}$ on each run, and at most $2^{q-n}$ in total. For $q \le n - 1$ this is at most $1/2$, which is less than $2/3$. So every bounded-error classical algorithm needs $n$ queries, and the deterministic algorithm shows that $n$ is enough.

**Quantum.** One query is enough by the [Bernstein-Vazirani algorithm](/bernstein-vazirani-algorithm/), and zero queries cannot find $s$ for $n \ge 1$. So the exact quantum query complexity is $1$. One query to the bit oracle on $n + 1$ qubits thus gives $n$ bits of information. This does not contradict the classical count, because a quantum query acts on a superposition of all $x$.

The gap is $n$ against $1$, so it is polynomial. It holds also against randomized algorithms, which is the difference from the [Deutsch-Jozsa problem](/deutsch-jozsa-problem/). For an exponential gap against randomized algorithms, see [Simon's problem](/simon-problem/).

## Reductions

- **To the Deutsch-Jozsa problem.** An instance $f(x) = s \cdot x \oplus c$ is constant if $s = 0$ and balanced otherwise. So a solver for this problem decides the Deutsch-Jozsa problem on affine inputs.
- **To linear algebra over GF(2).** Any $n$ answers at linearly independent strings fix $s$, through a system over GF(2).
- **To decoding.** The truth table is a Hadamard codeword, so the problem is query-efficient decoding of the [Hadamard code](/hadamard-code/) with no errors.
- **To Fourier sampling.** The spectrum of $(-1)^f$ is a single point, so one sample from the squared spectrum is the answer. This is the simplest case of [Fourier sampling](/fourier-sampling/).

## Applications

- **An oracle separation.** The recursive form of the problem gave an oracle relative to which bounded-error quantum polynomial time is not in bounded-error classical polynomial time. See [BQP](/bqp/), [BPP](/bpp/) and [relativization](/relativization/). Simon's problem later gave an exponential gap.
- **Learning parity functions.** In learning theory, the functions $s \cdot x$ are the parity functions. With membership queries a classical learner needs $n$ queries, and a quantum learner with a quantum membership oracle needs one.
- **A benchmark.** The circuit has one query and no rotations, so it is a common test of small quantum devices.

## References
