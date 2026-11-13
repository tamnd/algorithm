---
tag: FEHRFQ
kind: algorithm
slug: simon-algorithm
name: Simon's algorithm
aliases:
- Simon's period-finding
area: quantum/quantum-primitives
level: core
summary: Finds the hidden XOR period s of a promised two-to-one function with fewer than n + 2.61 queries in expectation and no error. Classical algorithms need about 2^(n/2) queries.
solves: [simon-problem]
model: quantum-query-model
complexity:
  vars: {n: the number of input bits of f, m: the number of output bits of f}
  queries: {expected: Θ(n)}
  gates: {expected: O(n^2)}
  qubits: {worst: n + m}
  time: {expected: O(n^3)}
properties: {exact: false, randomized: true, recursive: false}
history:
  year: 1994
  people: [Daniel R. Simon]
  note: Simon presented the algorithm at FOCS 1994. The journal version appeared in SIAM Journal on Computing in 1997.
prereqs: [simon-problem, bernstein-vazirani-algorithm, linear-system-modulo-2, quantum-measurement]
see_also: [fourier-sampling, shor-algorithm, order-finding, gaussian-elimination-modular, birthday-paradox, quantum-fourier-transform]
sources:
  - paper: doi:10.1109/SFCS.1994.365701
    title: "Daniel R. Simon, On the power of quantum computation, Proceedings of the 35th Annual Symposium on Foundations of Computer Science (FOCS 1994), pages 116-123, 1994"
    locator: the conference version of the algorithm
  - paper: doi:10.1137/S0097539796298637
    title: "Daniel R. Simon, On the power of quantum computation, SIAM Journal on Computing 26(5):1474-1483, 1997"
    locator: the journal version, which this page follows; the quantum subroutine and the analysis of the number of runs
  - paper: arxiv:quant-ph/9704027
    title: "Gilles Brassard and Peter Høyer, An exact quantum polynomial-time algorithm for Simon's problem, Fifth Israeli Symposium on Theory of Computing and Systems (ISTCS 1997), pages 12-23, 1997"
    locator: the exact variant with O(n) queries
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 3 (Simon's algorithm and its analysis)
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 6 (Simon's algorithm)
  - paper: doi:10.1007/978-3-662-53008-5_8
    title: "Marc Kaplan, Gaëtan Leurent, Anthony Leverrier and María Naya-Plasencia, Breaking symmetric cryptosystems using quantum period finding, CRYPTO 2016, Lecture Notes in Computer Science 9815, pages 207-237, 2016"
    locator: uses of Simon's algorithm against modes of operation with quantum queries
---

Simon's algorithm solves [Simon's problem](/simon-problem/): given an oracle for $f$ on $n$ bits with $f(x) = f(y)$ exactly when $y \in \{x, x \oplus s\}$, it finds $s$. Each run of a short circuit with one query gives a uniformly random $y$ with $y \cdot s = 0$. After about $n$ runs the equations fix $s$, which [Gaussian elimination over GF(2)](/gaussian-elimination-modular/) finds. With a final check of two classical queries, the algorithm never gives a wrong answer, and it uses fewer than $n + 2.61$ queries in expectation. Every classical algorithm, even with bounded error, needs $\Omega(2^{n/2})$ queries. This was the first exponential gap between quantum and randomized classical query complexity, and Shor's [order finding](/order-finding/) follows the same pattern.

## In plain words

A box gives each string of bits a label, and two strings share a label exactly when they differ by a hidden key. The quantum program puts its input in a mix of all strings and asks the box once. The label it gets back leaves the input as a mix of just two strings: one string, and the same string changed by the key.

A second step mixes these two strings again. Because of the way they cancel, the result is a random string that has an even number of ones in common with the key. That is one clue, a simple equation about the key. The program repeats this until it has enough different clues, about as many as the key has bits. Then it solves the equations by ordinary school algebra with bits, and two plain questions to the box check the answer.

## The problem

The input is $n \ge 1$ and a bit oracle $U_f |x\rangle |b\rangle = |x\rangle |b \oplus f(x)\rangle$, with $x$ on $n$ qubits and $b$ on $m$ qubits. The promise is that some $s \in \{0,1\}^n$ has $f(x) = f(y) \iff y \in \{x, x \oplus s\}$. The output is $s$, where $s = 0$ means that $f$ is one-to-one. See [Simon's problem](/simon-problem/) for the classical bounds.

We use the qubit order of [quantum state](/quantum-state/): qubit $j$ holds bit $j$, and qubit $0$ is the least significant bit. The input register is qubits $0$ to $n - 1$, and the output register is qubits $n$ to $n + m - 1$. We write $N = 2^n$ and $y \cdot s = \sum_j y_j s_j \bmod 2$, and $s^\perp = \{y : y \cdot s = 0\}$.

## The algorithm

```pseudo id=main
SIMON(U_f, f, n, m)
L1  E ← an empty system of equations over GF(2)
L2  while rank(E) < n - 1 do
L3      prepare |0...0⟩ on all n + m qubits
L4      apply H to each of qubits 0 .. n-1
L5      apply U_f                        ▷ one query
L6      apply H to each of qubits 0 .. n-1
L7      measure qubits 0 .. n-1 and let y be the outcome
L8      add the equation y · s = 0 to E
L9  s' ← the unique nonzero solution of E
L10 if f(0) = f(s') then return s' else return 0    ▷ two classical queries
```

Lines L3 to L7 are one run of the quantum subroutine. After line L5 the state is $N^{-1/2} \sum_x |x\rangle |f(x)\rangle$. The output register is not measured, but each value $f(x)$ appears for exactly the pair $\{x, x \oplus s\}$. So the input register behaves as if it were in $(|x\rangle + |x \oplus s\rangle)/\sqrt{2}$ for a uniformly random $x$. Line L6 maps this to
$$\frac{1}{\sqrt{2N}} \sum_y (-1)^{x \cdot y} \big(1 + (-1)^{s \cdot y}\big) |y\rangle,$$
and the factor $1 + (-1)^{s \cdot y}$ is $0$ when $y \cdot s = 1$. So line L7 gives a uniformly random $y \in s^\perp$ when $s \ne 0$, and a uniformly random $y \in \{0,1\}^n$ when $s = 0$.

Line L8 keeps $E$ in echelon form, so the rank is known after each step; an equation that is a sum of earlier ones adds nothing. When the rank is $n - 1$, the solutions of $E$ are $0$ and one nonzero string $s'$, which line L9 finds by back substitution. If $s \ne 0$, then $s$ solves $E$, so $s' = s$. If $s = 0$, the samples were uniform on all strings, and $s'$ is some nonzero string. Line L10 tells the two cases apart: $f(0) = f(s')$ holds exactly when $s' = s \ne 0$.

## Example

Take $n = 3$, $s = 110$ and the function below, with labels on $m = 2$ bits.

| $x$ | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|---|---|---|---|---|---|---|---|---|
| $f(x)$ | 0 | 1 | 2 | 3 | 2 | 3 | 0 | 1 |

The set $s^\perp$ is $\{000, 001, 110, 111\}$, and the exact distribution of $y$ from the simulator gives each of these probability $1/4$ and the other four strings probability $0$. A run with `random.Random(7)` gave this trace:

| run | $y$ | new rank | why |
|---|---|---|---|
| 1 | 001 | 1 | the first nonzero equation: $s_0 = 0$ |
| 2 | 000 | 1 | the zero equation adds nothing |
| 3 | 110 | 2 | independent of $001$: $s_1 \oplus s_2 = 0$ |

The rank is $n - 1 = 2$, so the loop stops. The equations $s_0 = 0$ and $s_1 = s_2$ have the nonzero solution $s' = 110$. Line L10 asks $f(000) = 0$ and $f(110) = 0$, which agree, and returns $110$. The run used $3$ quantum queries and $2$ classical ones.

The expected number of runs of the loop for $s \ne 0$, from the formula in Complexity, is:

| $n$ | 2 | 3 | 4 | 5 | 6 | 20 |
|---|---|---|---|---|---|---|
| expected runs | 2.000 | 3.333 | 4.476 | 5.543 | 6.575 | 20.607 |

For $n = 3$, $400$ runs of the full algorithm in the simulator with seed $5$ used a mean number of runs within $0.43$ of $10/3$, and each returned the right $s$.

## Correctness

The algorithm never returns a wrong answer. Each run of lines L3 to L7 gives $y$ uniform on $s^\perp$ (or on all strings if $s = 0$), so every equation in $E$ is true for the hidden $s$. When the rank of $E$ is $n - 1$, its solution set is $\{0, s'\}$ for one nonzero $s'$. If $s \ne 0$, then $s' = s$ and $f(0) = f(s)$, so line L10 returns $s$. If $s = 0$, then $f$ is one-to-one, $f(0) \ne f(s')$, and line L10 returns $0$. The loop ends with probability $1$, because each run raises the rank with probability at least $1/2$ while the rank is below $n - 1$. The full proof is below.

## Complexity

**Runs.** Suppose $s \ne 0$, so each $y$ is uniform on $s^\perp$, a space of dimension $n - 1$. When $E$ has rank $r < n - 1$, its rows span a subspace with $2^r$ of the $2^{n-1}$ elements of $s^\perp$, so a new $y$ raises the rank with probability $1 - 2^{r - n + 1}$. The number of runs at rank $r$ is geometric, so the expected number of runs is
$$\sum_{r=0}^{n-2} \frac{1}{1 - 2^{r-n+1}} = \sum_{j=1}^{n-1} \frac{1}{1 - 2^{-j}} = n - 1 + \sum_{j=1}^{n-1} \frac{1}{2^j - 1} < n - 1 + 1.6067.$$
The constant $\sum_{j \ge 1} 1/(2^j - 1) = 1.60669\ldots$ is the Erdős-Borwein constant. For $s = 0$ the samples are uniform on all of $\{0,1\}^n$, and the expected number of runs is smaller: $\sum_{j=2}^{n} 1/(1 - 2^{-j})$.

**A tail bound.** If $k$ uniform vectors from a space of dimension $d$ do not span it, they all lie in one of its $2^d - 1$ hyperplanes, and each hyperplane holds all $k$ with probability $2^{-k}$. So the failure probability is at most $(2^d - 1) 2^{-k} < 2^{d-k}$. With $d = n - 1$ and $k = n - 1 + c$ runs, the loop has ended with probability more than $1 - 2^{-c}$. So a version that stops after $n + 9$ runs and reports failure fails with probability less than $2^{-10}$.

**Queries.** Fewer than $n + 0.61$ quantum queries in expectation, and $2$ classical queries in line L10, for fewer than $n + 2.61$ in total. If the promise $s \ne 0$ is given, line L10 is not needed. The bounded-error quantum query complexity of the problem is $\Theta(n)$ (Koiran, Nesme and Portier 2007), so the algorithm is optimal up to a constant factor.

**Gates and qubits.** Each run uses $2n$ Hadamard gates and one query, on $n + m$ qubits. The output register is reset to $|0\rangle$ for each run, so the qubits are reused. Over all runs, the expected count is $O(n^2)$ Hadamard gates plus the cost of the oracle.

**Classical work.** Each insertion in line L8 reduces $y$ against at most $n - 1$ rows of $n$ bits, which takes $O(n^2)$ bit operations, or $O(n)$ word operations with bit sets. Over about $n$ runs the total is $O(n^3)$ bit operations. Line L9 takes $O(n^2)$. See [linear system modulo 2](/linear-system-modulo-2/).

Against classical algorithms, in the query model, the gap is $O(n)$ against $\Omega(2^{n/2})$; the proof is on [Simon's problem](/simon-problem/). This is a separation relative to an oracle. It does not show that [BQP](/bqp/) differs from [BPP](/bpp/).

## Properties

- **Zero error (Las Vegas).** The output is always right. The number of runs is random, with the mean and tail above.
- **Adaptive only in when to stop.** Every run is the same circuit. The classical part decides only whether to run again. So the runs can be done in parallel: $n + 9$ runs at once, then the classical part, fail with probability less than $2^{-10}$.
- **The output register need not be measured.** The analysis is the same if it is measured before line L6, after it, or never, because it is not touched again. Measuring it only makes the collapse to one pair explicit.
- **Fourier sampling.** Each run samples from the squared Fourier transform over $\mathbb{Z}_2^n$ of a state that is constant on the cosets of $\{0, s\}$. The outcomes lie in $s^\perp$, the group of characters that are trivial on the hidden subgroup. See [Fourier sampling](/fourier-sampling/).

## Variants and improvements

- **The exact version.** Brassard and Høyer (1997) changed each run so that the new $y$ is independent of the earlier ones with certainty, with an amplitude amplification step. The result uses $O(n)$ queries in the worst case and never fails.
- **A promise of $s \ne 0$.** Drop line L10 and return $s'$. The query count is then fewer than $n + 0.61$ in expectation.
- **The decision version.** To decide only whether $f$ is one-to-one, run the algorithm and test whether the output is $0$.
- **Larger hidden subspaces.** If $f$ is constant on the cosets of a subspace $H$ of dimension $k$ and distinct on different cosets, each run gives a uniform $y$ in $H^\perp$, which has dimension $n - k$. Collect $n - k$ independent equations, which takes $n - k + O(1)$ runs in expectation, and solve for a basis of $H$. When $k$ is unknown, run a few more times than the rank needs, and check the result with classical queries.
- **Other abelian groups.** Replace $H^{\otimes n}$ by the [quantum Fourier transform](/quantum-fourier-transform/) of the group. Over $\mathbb{Z}_{2^t}$ with $f(x) = a^x \bmod N$ this is the core of [Shor's algorithm](/shor-algorithm/); the samples are then near multiples of $2^t/r$, and the classical part uses [continued fractions](/continued-fraction/) in place of linear algebra.

## When to use it

Use Simon's algorithm when the task has a hidden XOR period and quantum queries are available. The main examples are the study of query complexity, as the cleanest exponential separation against randomized algorithms, and attacks on symmetric cryptography in a model where the attacker can query the keyed function in superposition (Kuwakado and Morii 2010, Kaplan, Leurent, Leverrier and Naya-Plasencia 2016). When only classical queries to the keyed function are available, these attacks do not apply. When the period is over the integers, use [order finding](/order-finding/) instead.

## Pitfalls

- **Stopping at $n - 1$ samples.** Some samples are dependent, and $y = 0$ is a valid sample. Stop when the rank is $n - 1$, not after $n - 1$ runs. With exactly $n - 1$ runs, the rank is $n - 1$ only with probability $\prod_{j=1}^{n-1} (1 - 2^{-j})$, which is about $0.289$ for large $n$.
- **Forgetting the case $s = 0$.** For a one-to-one $f$, the rank of $E$ can still reach $n - 1$, and the solution $s'$ is then wrong. Line L10 is needed unless $s \ne 0$ is promised.
- **A promise that fails.** If $f$ has collisions with different differences, the samples are no longer confined to one $s^\perp$, and the system can have only the solution $0$, or a wrong $s'$. Line L10 catches a wrong $s'$ only if $f(0) \ne f(s')$. For functions that are only close to the promise, as in cryptographic uses, the analysis needs more care.
- **Too few output qubits.** The output register must hold all values of $f$. If labels are cut to fewer bits, new collisions appear, and the promise fails.
- **Bit order.** The equation of a sample $y$ uses $y_j$ from qubit $j$. Reading the bits in the other order gives the reversed $s$.

## Implementations

## History

Daniel Simon presented the algorithm at FOCS 1994 in a paper with the title "On the power of quantum computation". He showed that a quantum machine solves the problem in expected polynomial time with polynomially many queries, while a classical probabilistic machine needs exponentially many. The gap is relative to an oracle, but it was the first exponential one against bounded-error classical computation, after the exact gap of Deutsch and Jozsa and the superpolynomial gap of Bernstein and Vazirani. Peter Shor's 1994 paper on factoring and discrete logarithms used the same pattern over the integers. The journal version of Simon's paper appeared in 1997 in SIAM Journal on Computing, in the same issue as the journal versions of Shor's and of Bernstein and Vazirani's papers. In 1997 Brassard and Høyer gave an exact version.

## References
