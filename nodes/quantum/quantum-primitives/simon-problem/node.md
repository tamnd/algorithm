---
tag: X2QXN4
kind: problem
slug: simon-problem
name: Simon's problem
area: quantum/quantum-primitives
level: intro
summary: Find the hidden string s of a function on n bits with f(x) = f(y) exactly when y = x or y = x XOR s. Quantum algorithms need Θ(n) queries and classical ones Θ(2^(n/2)).
prereqs: [quantum-oracle, query-complexity, birthday-paradox]
see_also: [simon-algorithm, bernstein-vazirani-problem, deutsch-jozsa-problem, order-finding, linear-system-modulo-2, randomized-query-complexity, yao-minimax-principle, simon-cipher]
sources:
  - paper: doi:10.1109/SFCS.1994.365701
    title: "Daniel R. Simon, On the power of quantum computation, Proceedings of the 35th Annual Symposium on Foundations of Computer Science (FOCS 1994), pages 116-123, 1994"
    locator: the conference version; the problem, the quantum algorithm and the classical lower bound
  - paper: doi:10.1137/S0097539796298637
    title: "Daniel R. Simon, On the power of quantum computation, SIAM Journal on Computing 26(5):1474-1483, 1997"
    locator: the journal version, which this page follows; the classical lower bound of order 2^(n/2) queries for a probabilistic machine
  - paper: doi:10.1016/j.tcs.2007.02.057
    title: "Pascal Koiran, Vincent Nesme and Natacha Portier, The quantum query complexity of the abelian hidden subgroup problem, Theoretical Computer Science 380(1-2):115-126, 2007"
    locator: the Omega(n) lower bound on the bounded-error quantum query complexity of Simon's problem (conference version at ICALP 2005)
  - paper: arxiv:quant-ph/9704027
    title: "Gilles Brassard and Peter Høyer, An exact quantum polynomial-time algorithm for Simon's problem, Fifth Israeli Symposium on Theory of Computing and Systems (ISTCS 1997), pages 12-23, 1997"
    locator: an exact quantum algorithm with O(n) queries
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 3 (Simon's problem), Section 3.3 (the classical lower bound)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.4.3 (the hidden subgroup problem, with Simon's problem as a case)
---

Simon's problem asks for a hidden string $s \in \{0,1\}^n$, given an oracle for a function $f$ on $n$ bits with the promise that $f(x) = f(y)$ if and only if $y = x$ or $y = x \oplus s$. So $f$ is two-to-one with "period" $s$ under XOR when $s \ne 0$, and one-to-one when $s = 0$. A quantum algorithm needs $\Theta(n)$ queries, and every classical algorithm, even with randomness and bounded error, needs $\Theta(2^{n/2})$. This was the first exponential separation between quantum and randomized classical query complexity, and it led Shor to his period-finding algorithm. This page is about the problem and its bounds; the quantum method is [Simon's algorithm](/simon-algorithm/). The problem has nothing to do with the [SIMON block cipher](/simon-cipher/).

## In plain words

A box turns each string of bits into a label. There is a hidden string, the key. Two different inputs get the same label exactly when you get one from the other by flipping the bits where the key has a 1. You must find the key.

A classical program learns something only when it finds two inputs with the same label. Then the key is the set of places where the two inputs differ. With random tries, a match takes about as many tries as the square root of the number of possible inputs. No classical program does much better.

A quantum program asks about all inputs at once. Each question gives a random clue that says some places of the key have an even number of ones. A few dozen clues fix the key, so the count grows only like the length of the key.

## Definition

**Input.** An integer $n \ge 1$ and oracle access to $f : \{0,1\}^n \to R$, where $R$ is a finite set, for example $\{0,1\}^m$ with $m \ge n - 1$.

**Promise.** There is $s \in \{0,1\}^n$ such that for all $x, y$:
$$f(x) = f(y) \iff y \in \{x, x \oplus s\}.$$
If $s = 0$, $f$ is one-to-one. If $s \ne 0$, $f$ is two-to-one, and each label is taken by exactly one pair $\{x, x \oplus s\}$.

**Output.** The string $s$.

**Access.** A classical query names $x$ and gets $f(x)$. A quantum query applies the bit oracle $U_f |x\rangle |b\rangle = |x\rangle |b \oplus f(x)\rangle$, with an output register of $m$ qubits; see [quantum oracle](/quantum-oracle/). There is no phase oracle form, because $f$ has more than one output bit. The cost is the number of queries in the classical [query model](/query-model/) or the [quantum query model](/quantum-query-model/).

**The group view.** The set $H = \{0, s\}$ is a subgroup of the group $\mathbb{Z}_2^n$ under XOR. The promise says that $f$ is constant on each coset $x \oplus H$ and takes different values on different cosets. So the problem is the hidden subgroup problem for $\mathbb{Z}_2^n$, with a subgroup of order $1$ or $2$. Shor's [order finding](/order-finding/) is the same pattern for the group $\mathbb{Z}$.

**Strings.** We write $x = x_{n-1} \cdots x_0$ and $x \cdot y = \sum_j x_j y_j \bmod 2$. Qubit $j$ holds bit $x_j$, as on [quantum state](/quantum-state/).

## Variants

- **The decision version.** Decide whether $f$ is one-to-one ($s = 0$) or two-to-one ($s \ne 0$). The bounds below hold for it too. Simon's paper used this form.
- **$s \ne 0$ promised.** Some texts promise $s \ne 0$. Then a solver need not check the case $s = 0$.
- **Larger hidden subgroups.** Let $f$ be constant on the cosets of a subspace $H$ of $\mathbb{Z}_2^n$ of any dimension $k$, and distinct on different cosets. The output is a basis of $H$. The same quantum method finds it with $O(n)$ queries, and classical algorithms need about $2^{(n-k)/2}$ queries.
- **Other abelian groups.** Over $\mathbb{Z}_N$ the hidden subgroup is $r \mathbb{Z}_N$, and the problem is period finding. Over $\mathbb{Z}_N \times \mathbb{Z}_N$ with the right function it is the discrete logarithm; see [quantum discrete logarithm](/quantum-discrete-logarithm/).

## Examples

**$n = 3$ and $s = 110$.** One function that obeys the promise, with labels in $\{0, 1, 2, 3\}$:

| $x$ | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|---|---|---|---|---|---|---|---|---|
| $f(x)$ | 0 | 1 | 2 | 3 | 2 | 3 | 0 | 1 |

The pairs with equal labels are $\{000, 110\}$, $\{001, 111\}$, $\{010, 100\}$ and $\{011, 101\}$. In each pair the two strings differ by $110$. A classical algorithm that sees $f(010) = f(100) = 2$ gets $s = 010 \oplus 100 = 110$.

**How many functions obey the promise.** For $n = 2$ and labels in $\{0,1\}^2$, there are $4^4 = 256$ functions. Of these, $4! = 24$ are one-to-one ($s = 0$). For each of the $3$ nonzero $s$ there are $2$ pairs, which get $2$ different labels out of $4$ in $4 \cdot 3 = 12$ ways. So $24 + 36 = 60$ functions obey the promise. For $n = 3$ and labels in $\{0,1\}^2$, there are no one-to-one functions, and each of the $7$ nonzero $s$ gives $4! = 24$ functions, so $168$ in total.

**The birthday count.** For $n = 20$, a classical algorithm that asks $q$ random different strings finds a pair with equal labels with probability about $1 - e^{-q^2/2^{21}}$ for $s \ne 0$. For probability $1/2$ that is about $q = 1206$ queries, against about $2^{10} = 1024$ for the square root. [Simon's algorithm](/simon-algorithm/) uses about $22.6$ queries in expectation: $20.6$ quantum runs and $2$ classical checks.

## Known algorithms

- **Classical, randomized.** Ask random different strings until two labels agree; then $s$ is their XOR. With $q$ queries and $s \ne 0$, the chance of a match is about $1 - e^{-q^2/2^{n+1}}$, as in the [birthday paradox](/birthday-paradox/). So $O(2^{n/2})$ queries find $s$ with constant probability, and if no match is found the algorithm answers $s = 0$.
- **Classical, deterministic.** Ask all strings whose upper $\lceil n/2 \rceil$ bits are $0$ and all strings whose lower $\lfloor n/2 \rfloor$ bits are $0$. Every nonzero $s$ is the XOR of one string of each set, so if $s \ne 0$ some pair of asked strings has equal labels. This uses at most $2^{\lceil n/2 \rceil} + 2^{\lfloor n/2 \rfloor}$ queries, which is $O(2^{n/2})$.
- **Quantum, zero error.** [Simon's algorithm](/simon-algorithm/) repeats a short circuit with one query until it has $n - 1$ linearly independent equations $y \cdot s = 0$, solves them over GF(2), and checks the candidate with two classical queries. It uses fewer than $n + 2.61$ queries in expectation, $O(n)$ qubits and $O(n^3)$ classical time for the [linear system modulo 2](/linear-system-modulo-2/).
- **Quantum, exact.** Brassard and Høyer (1997) gave a variant with $O(n)$ queries that is always right after a fixed number of queries. It changes the last steps with amplitude amplification so that each new equation is independent of the old ones with certainty.

## Bounds

| model | queries | tight |
|---|---|---|
| classical, deterministic | $\Theta(2^{n/2})$ | yes |
| classical, bounded error | $\Theta(2^{n/2})$ | yes |
| quantum, bounded error | $\Theta(n)$ | yes |
| quantum, exact | $O(n)$ | yes |

**Classical lower bound.** We use the [Yao minimax principle](/yao-minimax-principle/). Choose $s$ uniformly among the $N - 1$ nonzero strings, where $N = 2^n$, and choose $f$ by giving the $N/2$ pairs $\{x, x \oplus s\}$ distinct labels in a uniformly random way. Fix a deterministic algorithm with $q$ queries. Call it a *collision* when two asked strings $x_i, x_j$ have $x_i \oplus x_j = s$.

Before the first collision, the asked strings lie in different pairs, so the answers are distinct labels chosen uniformly at random. Their distribution does not depend on $s$. So, given that no collision has happened after $k$ queries, $s$ is uniform on the nonzero strings that are not the XOR of two asked strings. There are at least $N - 1 - \binom{k}{2}$ of them. Query $k + 1$ makes a collision only if $s$ is one of the $k$ strings $x_{k+1} \oplus x_i$, which has probability at most $k/(N - 1 - \binom{k}{2})$. Summing over $k < q$, the probability of any collision is at most $\binom{q}{2}/(N - 1 - \binom{q}{2})$. Without a collision, the output is one guess, and it is right with probability at most $1/(N - 1 - \binom{q}{2})$. So
$$\Pr[\text{success}] \le \frac{\binom{q}{2} + 1}{N - 1 - \binom{q}{2}}.$$
For $n \ge 3$ and $q \le 2^{n/2}/2$, we have $\binom{q}{2} \le N/8$, and the bound is at most $(N/8 + 1)/(7N/8 - 1) \le 1/3$. So a bounded-error algorithm needs more than $2^{n/2}/2$ queries. The same argument, with $s = 0$ allowed, bounds the decision version. Simon's paper proves a bound of this kind for probabilistic machines.

**Quantum upper bound.** [Simon's algorithm](/simon-algorithm/) uses $O(n)$ queries with zero error, and the algorithm of Brassard and Høyer uses $O(n)$ queries with no error at all.

**Quantum lower bound.** Koiran, Nesme and Portier (2007) proved that every bounded-error quantum algorithm needs $\Omega(n)$ queries. So the quantum query complexity is $\Theta(n)$, and the gap against classical algorithms is $\Theta(n)$ against $\Theta(2^{n/2})$.

The separation holds in the query model, relative to an oracle. It does not prove that [BQP](/bqp/) differs from [BPP](/bpp/): an explicit, efficiently computable $f$ might have structure that a classical algorithm can use.

## Reductions

- **Quantum sampling to linear algebra.** Each quantum sample is a uniform $y$ with $y \cdot s = 0$. With $n - 1$ independent samples, $s$ is the unique nonzero solution of a [linear system modulo 2](/linear-system-modulo-2/), found by [Gaussian elimination](/gaussian-elimination-modular/).
- **To the hidden subgroup problem.** Simon's problem is the hidden subgroup problem in $\mathbb{Z}_2^n$. Period finding in $\mathbb{Z}_N$, which is the core of [order finding](/order-finding/) and [Shor's algorithm](/shor-algorithm/), is the same problem in a cyclic group.
- **From collision finding.** A classical solver must find a collision of $f$, so its cost is a [birthday attack](/birthday-attack/) cost. The promise makes the collision structure rigid, which is what the quantum algorithm uses.

## Applications

- **The first exponential separation against randomized algorithms.** Simon's problem gave an oracle relative to which bounded-error quantum polynomial time is not in bounded-error classical polynomial time, with an exponential gap. See [relativization](/relativization/).
- **The path to Shor's algorithm.** Shor's period finding over $\mathbb{Z}$ follows the pattern of Simon's algorithm, with the quantum Fourier transform over $\mathbb{Z}_{2^t}$ in place of the Hadamard transform; see [Shor's algorithm](/shor-algorithm/).
- **Attacks on symmetric cryptography with quantum queries.** If an attacker can query a keyed function in superposition, Simon's algorithm can find a hidden XOR period built into some constructions. Kuwakado and Morii (2010) used it to distinguish the three-round Feistel cipher from a random permutation. Kaplan, Leurent, Leverrier and Naya-Plasencia (2016) used it against several modes of operation and message authentication codes. These attacks need quantum access to the keyed function, which is a strong model; with classical queries only they do not apply.

## References
