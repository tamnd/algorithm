---
tag: PHQYF3
kind: problem
slug: deutsch-jozsa-problem
name: Deutsch-Jozsa problem
area: quantum/quantum-primitives
level: intro
summary: Decide whether a Boolean function on n bits, promised to be constant or balanced, is constant or balanced, with as few queries to an oracle for it as possible.
prereqs: [quantum-oracle, query-complexity]
see_also: [deutsch-jozsa-algorithm, bernstein-vazirani-problem, simon-problem, quantum-query-model, quantum-query-complexity, randomized-query-complexity, walsh-hadamard-transform, unstructured-search]
sources:
  - paper: doi:10.1098/rspa.1992.0167
    title: "David Deutsch and Richard Jozsa, Rapid solution of problems by quantum computation, Proceedings of the Royal Society of London A 439(1907):553-558, 1992"
    locator: the problem statement (constant or balanced) and the comparison with classical deterministic computation
  - paper: doi:10.1098/rspa.1998.0164
    title: "Richard Cleve, Artur Ekert, Chiara Macchiavello and Michele Mosca, Quantum algorithms revisited, Proceedings of the Royal Society of London A 454(1969):339-354, 1998"
    locator: the Deutsch problem and the Deutsch-Jozsa problem with one query
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 1.4.3 (Deutsch's problem) and Section 1.4.4 (the Deutsch-Jozsa problem and the classical cost)
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 6 (introductory quantum algorithms, the Deutsch and the Deutsch-Jozsa problems)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 2 (the Deutsch-Jozsa problem and its classical query cost)
---

The Deutsch-Jozsa problem asks whether a function $f : \{0,1\}^n \to \{0,1\}$ is constant or balanced, when one of the two is promised. The function is given only as an oracle, and the cost is the number of queries. It was the first problem with an exponential gap between exact quantum and exact classical query complexity: one quantum query is enough, but a deterministic classical algorithm needs $2^{n-1} + 1$ queries. A classical randomized algorithm with bounded error needs only $2$ queries, so the gap is against exact classical algorithms only. This page is about the problem and its bounds; the one-query method is the [Deutsch-Jozsa algorithm](/deutsch-jozsa-algorithm/).

## In plain words

A box hides a rule that turns each string of bits of a fixed length into one bit. You may ask the box about one string at a time. You are told that the rule is one of two kinds. Either it gives the same bit for every string, or it gives 0 for exactly half of the strings and 1 for the other half. You must say which kind it is.

A classical program that must always be right can need just over half of all strings. The first half of the answers can all agree, and then both kinds are still possible. A quantum program can ask one question about many strings at once, and it is always right after one question. A classical program that may be wrong with a small chance needs only two questions.

## Definition

**Input.** An integer $n \ge 1$ and oracle access to a function $f : \{0,1\}^n \to \{0,1\}$. Write $N = 2^n$ and $|f| = |\{x : f(x) = 1\}|$ for the number of ones of $f$.

**Promise.** $f$ is *constant* ($|f| = 0$ or $|f| = N$) or *balanced* ($|f| = N/2$).

**Output.** The word "constant" or the word "balanced".

**Access.** A classical query names a string $x$ and gets $f(x)$. A quantum query applies one of two unitaries, which are equal in power up to one [ancilla qubit](/ancilla-qubits/) and one query:

- the bit oracle $U_f |x\rangle |b\rangle = |x\rangle |b \oplus f(x)\rangle$, and
- the phase oracle $O_f |x\rangle = (-1)^{f(x)} |x\rangle$.

The bit oracle on the ancilla state $|-\rangle = (|0\rangle - |1\rangle)/\sqrt{2}$ acts as the phase oracle, by [phase kickback](/phase-kickback/). The [quantum oracle](/quantum-oracle/) page gives both forms. The cost is the number of queries in the [quantum query model](/quantum-query-model/) or the classical [query model](/query-model/). Other gates are free in this count. We say which error is allowed each time: *exact* (error 0), *zero error* (the algorithm may stop without an answer, or its number of queries is random, but a given answer is always right), or *bounded error* (error at most $1/3$ on each input).

The problem is a *partial* function. Only $2 + \binom{N}{N/2}$ of the $2^N$ functions obey the promise. On the other functions any answer is allowed.

**Strings and bits.** We write a string as $x = x_{n-1} \cdots x_1 x_0$ and also as the integer $\sum_j x_j 2^j$. This matches the qubit order of [quantum state](/quantum-state/): qubit $j$ holds bit $x_j$, and qubit $0$ is the least significant bit. For two strings, $x \cdot y = \sum_j x_j y_j \bmod 2$.

## Variants

- **Deutsch's problem ($n = 1$).** Decide whether $f(0) = f(1)$, that is, compute $f(0) \oplus f(1)$. All four functions on one bit obey the promise: two are constant and two are balanced. A classical algorithm needs both values, even with randomness: one query sees one value, and the other value is free. Deutsch posed this case in 1985.
- **Error models.** The exact, zero-error and bounded-error versions have very different classical costs. The table in Bounds gives each one.
- **No promise.** Without the promise, the question "is $f$ constant?" is a total function. It is as hard as [unstructured search](/unstructured-search/) on $N - 1$ items (see Reductions), so its bounded-error quantum query complexity is $\Theta(2^{n/2})$, and the gap to classical algorithms becomes only quadratic.
- **Affine functions.** If $f$ is promised to be $f(x) = s \cdot x \oplus c$, then $f$ is constant when $s = 0$ and balanced when $s \ne 0$. Finding all of $s$ is the [Bernstein-Vazirani problem](/bernstein-vazirani-problem/).

## Examples

**All functions for $n = 2$.** There are $16$ functions. Of them, $2$ are constant and $\binom{4}{2} = 6$ are balanced, so $8$ obey the promise. In the order $f(00), f(01), f(10), f(11)$:

| truth table | kind | a formula |
|---|---|---|
| 0000 | constant | $0$ |
| 1111 | constant | $1$ |
| 0101 | balanced | $x_0$ |
| 0011 | balanced | $x_1$ |
| 0110 | balanced | $x_0 \oplus x_1$ |
| 1010 | balanced | $1 \oplus x_0$ |
| 1100 | balanced | $1 \oplus x_1$ |
| 1001 | balanced | $1 \oplus x_0 \oplus x_1$ |

For $n = 2$ every balanced function is affine. This is not true for larger $n$: for $n = 3$ there are $\binom{8}{4} = 70$ balanced functions, but only $14$ affine ones with $s \ne 0$. For $n = 4$ there are $12870$ balanced functions.

**Why two classical queries are not enough for $n = 2$.** A deterministic algorithm asks $f(00)$ and gets $0$, then asks $f(01)$ and gets $0$. The constant function $0000$ and the balanced function $0011$ both agree with these answers. So the algorithm must ask a third time. A third answer decides it: three equal values rule out a balanced function, and two different values rule out a constant one. This is the case $n = 2$ of the bound $2^{n-1} + 1 = 3$.

**The Fourier view.** For each $f$, define its Walsh-Hadamard coefficients
$$\hat{F}(y) = \frac{1}{N} \sum_{x} (-1)^{f(x) + x \cdot y}, \qquad y \in \{0,1\}^n.$$
This is the [Walsh-Hadamard transform](/walsh-hadamard-transform/) of the $\pm 1$ form of $f$. Then $\hat{F}(0) = (N - 2|f|)/N$, so $\hat{F}(0) = \pm 1$ for a constant $f$ and $\hat{F}(0) = 0$ for a balanced $f$. For $f = x_0 \oplus x_1$ the only nonzero coefficient is $\hat{F}(11) = 1$. The quantum algorithm uses exactly this difference.

## Known algorithms

- **Classical, deterministic.** Ask $2^{n-1} + 1$ different strings. Answer "constant" if all values agree, and "balanced" otherwise. This costs $2^{n-1} + 1$ queries in the worst case, and it is optimal.
- **Classical, bounded error.** Ask two different random strings. If the values differ, answer "balanced". If they agree, answer "constant" with probability $p = (N - 1)/(3N/2 - 2)$ and "balanced" otherwise. The error is less than $1/3$ on each input (see Bounds). With $k$ independent uniform strings and the simple rule "constant if all agree", the error is one-sided and at most $2^{1-k}$.
- **Quantum, exact.** The [Deutsch-Jozsa algorithm](/deutsch-jozsa-algorithm/) uses one query to the bit oracle, $n + 1$ qubits and $O(n)$ other gates, and it is always right.

## Bounds

| model | queries | tight |
|---|---|---|
| classical, deterministic (exact) | $2^{n-1} + 1$ | yes |
| classical, zero error | $2^{n-1} + 1$ on each constant input | yes |
| classical, bounded error $1/3$ | $2$ for $n \ge 2$ | yes |
| quantum, exact | $1$ | yes |

**Deterministic lower bound.** An adversary answers $0$ to each of the first $2^{n-1}$ queries to different strings. After these answers, the constant function $0$ and the balanced function that is $1$ on all strings not yet asked both agree with what the algorithm saw. A deterministic algorithm that stops now gives the same answer on both, so it is wrong on one of them. So it needs at least $2^{n-1} + 1$ queries. The algorithm above shows that this is enough, because $2^{n-1} + 1$ equal values are more than a balanced function has.

**Zero-error lower bound.** Take any zero-error randomized algorithm and run it on the constant function $0$. When it answers "constant", it must have seen more than $2^{n-1}$ different strings, or the same adversary argument gives a balanced function that it also answers "constant" on with positive probability. So on each constant input it makes at least $2^{n-1} + 1$ queries on every run, not only on average. Randomness helps only if errors are allowed.

**Bounded error with two queries.** Let the algorithm ask two different uniform random strings. On a constant input the values agree, and the error is the probability $1 - p$ of the answer "balanced". On a balanced input the values agree with probability
$$e = \frac{2 \binom{N/2}{2}}{\binom{N}{2}} = \frac{N/2 - 1}{N - 1} < \frac{1}{2},$$
and then the algorithm errs with probability $p$, so the error is $e p$. With $p = 1/(1 + e)$ both errors are $e/(1 + e)$, which is less than $1/3$ because $e < 1/2$. This $p$ is $(N-1)/(3N/2 - 2)$. For $N = 4$ the error is $1/4$.

**One classical query is not enough.** Let an algorithm with one query (and any randomness) ask the string $x$ with probability $q(x)$, and answer "constant" with probability $r_b(x)$ when it sees the value $b$. For $f = 0$ and $f = 1$ to have error at most $1/3$, we need $\sum_x q(x) r_0(x) \ge 2/3$ and $\sum_x q(x) r_1(x) \ge 2/3$. For a uniform random balanced $f$, each $f(x)$ is $0$ or $1$ with probability $1/2$, so the mean probability of the answer "constant" is $\sum_x q(x) (r_0(x) + r_1(x))/2 \ge 2/3$. So some balanced $f$ gets the wrong answer with probability at least $2/3$. With the two-query algorithm above, the bounded-error cost is exactly $2$ for $n \ge 2$. For $n = 1$ it is also $2$, and then the two queries are exact.

**Quantum.** Zero queries cannot tell $f = 0$ from a balanced $f$, and one query is enough by the [Deutsch-Jozsa algorithm](/deutsch-jozsa-algorithm/). So the exact quantum query complexity is $1$ for every $n$. The ratio of $2^{n-1} + 1$ to $1$ is the exponential separation; the ratio of $2$ to $1$ against bounded-error algorithms is a constant. See [quantum query complexity](/quantum-query-complexity/) and [randomized query complexity](/randomized-query-complexity/) for the general definitions.

## Reductions

- **From Deutsch's problem.** The case $n = 1$ is Deutsch's problem. Conversely, for $n \ge 2$, the value $f(0) \oplus f(1)$ alone does not decide the problem.
- **From OR, for the total version.** Given bits $z_1, \ldots, z_{N-1}$, define $f(0) = 0$ and $f(x) = z_x$ for $x \ne 0$. Then $f$ is constant if and only if all $z_x$ are $0$. So deciding whether an arbitrary $f$ is constant is at least as hard as the OR of $N - 1$ bits, which needs $\Omega(\sqrt{N})$ bounded-error quantum queries. The promise is what makes one query enough.
- **To the Bernstein-Vazirani problem.** An affine function $s \cdot x \oplus c$ obeys the promise, and it is constant if and only if $s = 0$. So an algorithm for the [Bernstein-Vazirani problem](/bernstein-vazirani-problem/) decides the Deutsch-Jozsa problem on affine inputs.

## Applications

- **The first exact separation.** The problem shows that an exact quantum algorithm can use exponentially fewer queries than any deterministic classical algorithm. It does not give a separation against randomized classical algorithms, and it does not show that [BQP](/bqp/) is larger than [BPP](/bpp/).
- **Teaching and tests of hardware.** The problem is small, the answer is known, and the quantum circuit is short. So it is a common first example in courses and a common first test of small quantum devices.
- **A start for later problems.** The [Bernstein-Vazirani problem](/bernstein-vazirani-problem/) and [Simon's problem](/simon-problem/) keep the same oracle model and add structure to the promise. Simon's problem gives a gap against randomized algorithms too.

## References
