---
tag: TE4YP7
kind: algorithm
slug: bbht-search
name: BBHT search
aliases:
- Boyer-Brassard-Høyer-Tapp search
- search with unknown number of solutions
area: quantum/quantum-search
level: advanced
summary: Grover search with a random iteration count from a range that grows by 6/5 each round. It finds a marked item with O(√(N/M)) expected queries when M is not known.
solves: [unstructured-search]
model: quantum-query-model
complexity:
  vars: {N: the number of items, M: the number of marked items}
  queries: {expected: O((N/M)^(1/2))}
  time: {expected: O((N/M)^(1/2) log N)}
  space: {extra: O(log N)}
properties: {deterministic: false, exact: false, one_sided_error: true, needs_m: false, oracle: phase, las_vegas: true}
history:
  year: 1996
  people: [Michel Boyer, Gilles Brassard, Peter Høyer, Alain Tapp]
  note: The algorithm is in Section 4 of "Tight bounds on quantum searching", on arXiv in May 1996 and in Fortschritte der Physik in 1998.
prereqs: [grover-search]
see_also: [amplitude-amplification, quantum-counting, durr-hoyer-minimum-finding, fixed-point-quantum-search, grover-optimality, las-vegas-algorithm, markov-inequality, geometric-distribution]
sources:
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Section 3 (the probability sin^2((2j+1) theta) for t solutions) and Section 4 (the overshoot example with N = 2^20, Lemma 1, Lemma 2, the algorithm with lambda = 6/5, and Theorem 3)
  - paper: arxiv:quant-ph/0005055
    title: "Gilles Brassard, Peter Høyer, Michele Mosca and Alain Tapp, Quantum amplitude amplification and estimation, in Quantum Computation and Information, Contemporary Mathematics 305, American Mathematical Society, 2002"
    locator: Section 2, Theorem 3 (the algorithm QSearch, the same method for amplitude amplification with an unknown success probability)
  - paper: arxiv:quant-ph/9607014
    title: Christoph Dürr and Peter Høyer, A quantum algorithm for finding the minimum, arXiv:quant-ph/9607014, 1996
    locator: the minimum-finding algorithm, which calls this search as a subroutine
---

BBHT search finds a marked item among $N$ items when the number $M$ of marked items is not known. Each round runs [Grover's search](/grover-search/) with a random number $j$ of iterations, drawn uniformly below a bound $m$, and the bound grows by the factor $6/5$ after each failed round. The expected number of oracle queries is $O(\sqrt{N/M})$ for every $M \ge 1$, the same order as Grover's algorithm with $M$ known. The algorithm is the one of Section 4 of Boyer, Brassard, Høyer and Tapp; it solves [unstructured search](/unstructured-search/) with no promise on $M$.

## In plain words

Grover's method needs the right number of rounds. Too few rounds and the good items are still rare; too many and they become rare again. The right number depends on how many good items there are. If you do not know that, a guess can fail almost surely.

BBHT search does not guess one number. It picks a random number of rounds below a limit, runs Grover's method, and looks at the result. If the result is not good, it raises the limit a little and tries again. Once the limit is near the right size, a random choice below it works at least one time in four. Because the limit grows slowly, the total work stays close to the work of Grover's method with the right number.

## The problem

The input is a number $N$ and a function $f : \{0, 1, \ldots, N-1\} \to \{0, 1\}$, given as a [quantum oracle](/quantum-oracle/). The number $M$ of items $x$ with $f(x) = 1$ is not known, and it can be 0. The output is one $x$ with $f(x) = 1$, or NO SOLUTION. The cost is the number of oracle calls in the [quantum query model](/quantum-query-model/). Qubit 0 is the least significant bit of $x$.

The algorithm uses the Grover iteration $G = D\,O_f$, where $O_f|x\rangle = (-1)^{f(x)}|x\rangle$ is the phase oracle and $D$ is the [Grover diffusion operator](/grover-diffusion-operator/). After $j$ iterations from the uniform state $|s\rangle$, a measurement gives a marked item with probability $\sin^2((2j+1)\theta)$, where $\sin^2\theta = M/N$.

## The algorithm

```pseudo id=main
BBHT-SEARCH(O_f, N, B)                     ▷ B is a limit on the iterations, or ∞
L1  m ← 1; λ ← 6/5; used ← 0               ▷ any λ with 1 < λ < 4/3 works
L2  while used < B
L3      choose j uniformly at random from {0, 1, ..., ⌈m⌉ - 1}
L4      prepare |s⟩ and apply G^j          ▷ j queries
L5      measure the register; let x be the result
L6      if f(x) = 1 then return x          ▷ one classical query
L7      used ← used + j; m ← min(λ m, sqrt N)
L8  return NO SOLUTION
```

Line L3 is the key step: $j$ is random, not fixed. The mean of $\sin^2((2j+1)\theta)$ over $0 \le j < c$ is $\frac{1}{2} - \frac{\sin(4c\theta)}{4c\sin 2\theta}$ (Lemma 2 of the paper), and this is at least $1/4$ as soon as $c \ge 1/\sin(2\theta)$. So a random $j$ cannot land on a bad iteration count again and again. Line L7 grows the range slowly and caps it at $\sqrt{N}$, because no useful $j$ is larger than about $(\pi/4)\sqrt{N}$. With $B = \infty$ and $M = 0$ the loop never ends; the limit $B$ is the time-out of the paper. The implementation uses $B = 18\sqrt{N}$.

Round 1 has $m = 1$, so $j = 0$: it measures $|s\rangle$, which is a classical random sample. This handles the case $M > 3N/4$, where a sample succeeds with probability above $3/4$.

## Example

Take $N = 64$ and $M = 2$, so $\sin^2\theta = 1/32$ and $1/\sin(2\theta) \approx 2.87$. The table follows the first rounds. The column "success" is the probability that the round finds a marked item, given that it starts.

| round | $m$ | choices of $j$ | mean of $j$ | success | P(round starts) |
|---|---|---|---|---|---|
| 1 | 1 | {0} | 0 | 0.0313 | 1 |
| 2 | 1.2 | {0, 1} | 0.5 | 0.1448 | 0.9688 |
| 3 | 1.44 | {0, 1} | 0.5 | 0.1448 | 0.8285 |
| 4 | 1.728 | {0, 1} | 0.5 | 0.1448 | 0.7086 |
| 5 | 2.074 | {0, 1, 2} | 1 | 0.2973 | 0.6060 |
| 6 | 2.488 | {0, 1, 2} | 1 | 0.2973 | 0.4258 |
| 7 | 2.986 | {0, 1, 2} | 1 | 0.2973 | 0.2992 |
| 8 | 3.583 | {0, ..., 3} | 1.5 | 0.4472 | 0.2102 |
| 9 | 4.300 | {0, ..., 4} | 2 | 0.5576 | 0.1162 |

From round 8 on, the number of choices is at least $2.87$ and each round succeeds with probability above $1/4$, as Lemma 2 says. The exact expectation is $3.37$ Grover iterations and $5.25$ rounds, so $8.62$ queries in all. Grover's algorithm with $M = 2$ known uses $4$ iterations and one check, and succeeds with probability $0.9992$. For small $N$ the classical checks dominate; for large $N$ the iterations do. For $N = 2^{20}$ and $M = 1$ the exact expectation is $1454$ iterations and $34$ rounds, against $804$ iterations for Grover's algorithm with $M$ known.

Why not simply run Grover's algorithm with $804$ iterations? For $N = 2^{20}$ it succeeds with probability $0.99999976$ if $M = 1$, but with probability $9.8 \cdot 10^{-7}$ if $M = 4$. BBHT search has no such bad case.

## Correctness

Line L6 checks each candidate, so a returned item is always marked. For the cost, let $m_0 = 1/\sin(2\theta)$. If $1 \le M \le 3N/4$, then $m_0 \le \sqrt{N/M}$. Call a round *critical* if it has at least $m_0$ choices of $j$. Before the first critical round, the ranges grow geometrically and stay below $m_0$, so those rounds make fewer than $3m_0$ iterations in all. From the first critical round on, each round succeeds with probability at least $1/4$, so round $u$ after it starts with probability at most $(3/4)^u$, while its range is at most $(6/5)^u \cdot (6/5)m_0$. The sum of $(3/4 \cdot 6/5)^u = 0.9^u$ converges to $10$, so these rounds make fewer than $6m_0$ iterations in expectation. The total is less than $9m_0 \le 9\sqrt{N/M}$. The full proof is in proofs/correctness.md.

## Complexity

In the [quantum query model](/quantum-query-model/), with $1 \le M \le 3N/4$:

- **Expected iterations.** Less than $9/\sin(2\theta) \le 9\sqrt{N/M}$, proved on this page. The paper states $\frac{9}{2}/\sin(2\theta)$, about $\frac{9}{4}\sqrt{N/M}$ for $M \ll N$. The exact expectation, computed for every $N \le 1024$ and every such $M$, is at most $2.32/\sin(2\theta)$ and at most $1.16\sqrt{N/M}$.
- **Expected rounds.** Less than $\log_{6/5}\sqrt{N/M} + 5$. Each round makes one classical query, so the total is $O(\sqrt{N/M})$ queries in expectation.
- **Large $M$.** For $M > 3N/4$ the first round is a classical sample with success above $3/4$. The exact expectation of iterations plus rounds is at most $2.01$ for every $N \le 256$.
- **No solution.** With the limit $B$, the run makes fewer than $B + \sqrt{N}$ iterations when $M = 0$. When $M \ge 1$, it returns NO SOLUTION with probability less than $9\sqrt{N/M}/B$ by [Markov's inequality](/markov-inequality/), so $B = 18\sqrt{N}$ gives an error below $1/2$, and in fact below $0.07$ by the exact values. Repeat the run to make the error smaller.
- **Gates and qubits.** As for Grover's algorithm: $O(\log N)$ gates per iteration besides the oracle, and $\lceil \lg N \rceil$ data qubits. The classical control keeps $m$ and a counter.

By the [optimality theorem](/grover-optimality/), each algorithm needs $\Omega(\sqrt{N/M})$ queries for bounded error, so BBHT search is optimal up to a constant factor without knowing $M$.

## Properties

- **Las Vegas.** With $B = \infty$ it is a [Las Vegas algorithm](/las-vegas-algorithm/): it never returns a wrong item, and its expected cost is $O(\sqrt{N/M})$. It does not stop when $M = 0$.
- **One-sided error with a time-out.** With a finite $B$, it never returns an unmarked item, and it can return NO SOLUTION wrongly.
- **No knowledge of $M$.** The only parameter is $\lambda$. Any $\lambda$ with $1 < \lambda < 4/3$ gives the same order of cost; the proof needs $3\lambda/4 < 1$.
- **Independent rounds.** Each round prepares a fresh state, so no quantum state is kept between rounds. A round needs at most $\sqrt{N}$ iterations in sequence.

## Variants and improvements

- **Amplitude amplification with unknown success probability.** Brassard, Høyer, Mosca and Tapp state the same method for [amplitude amplification](/amplitude-amplification/) with any start algorithm (the algorithm QSearch). Its expected cost is $O(1/\sqrt{a})$ calls for success probability $a$.
- **Count first.** Estimate $M$ with [quantum counting](/quantum-counting/), then run Grover's algorithm with the estimate. This costs $O(\sqrt{N})$ queries for the count, so it pays only when the count is needed anyway.
- **No overshoot.** [Fixed-point quantum search](/fixed-point-quantum-search/) needs only a lower bound on $M/N$, uses one run with no measurement in between, and never overshoots.
- **Minimum finding.** [Dürr-Høyer minimum finding](/durr-hoyer-minimum-finding/) calls BBHT search with a moving threshold. [Grover adaptive search](/grover-adaptive-search/) does the same for optimization problems.

## When to use it

Use BBHT search whenever the number of solutions is not known, which is the usual case: the number of satisfying assignments of a [SAT](/sat/) formula, or of keys that match a known plaintext in [exhaustive key search](/exhaustive-key-search/). Set a limit $B$ when there may be no solution. Do not use it when $M$ is known: plain Grover search is about two times cheaper. Do not use it when $M > N/4$ is likely: classical random sampling is as good. As for every Grover method, the speedup is only a square root, and it holds only when $f$ has no structure that a classical algorithm can use.

## Pitfalls

- **A fixed iteration count.** "L3 $j \leftarrow \lfloor (\pi/4)\sqrt{N} \rfloor$" is wrong when $M$ is not known: for $N = 2^{20}$ and $M = 4$ it fails with probability $1 - 10^{-6}$. Use "L3 choose $j$ uniformly at random from $\{0, \ldots, \lceil m \rceil - 1\}$".
- **A deterministic $j$ from the range.** "L3 $j \leftarrow \lceil m \rceil - 1$" can land on bad values of $\sin^2((2j+1)\theta)$ in several rounds in a row, and Lemma 2 no longer applies. Keep $j$ random.
- **Growth that is too fast.** "L1 $\lambda \leftarrow 2$" breaks the proof: the bound $\sum_u (3\lambda/4)^u$ diverges for $\lambda \ge 4/3$. Use "L1 $\lambda \leftarrow 6/5$", or any $\lambda$ with $1 < \lambda < 4/3$.
- **No cap.** "L7 $m \leftarrow \lambda m$" without the minimum lets $m$ grow past $\sqrt{N}$, and when $M = 0$ a single round can then be very long. Use "L7 $m \leftarrow \min(\lambda m, \sqrt{N})$".
- **No time-out.** "L2 loop forever" never stops when $M = 0$. Use "L2 while used $< B$" with $B = c\sqrt{N}$, and say what error that gives.
- **Forgetting the checks.** Each round makes one classical query in line L6. Count it: for small $N$ the checks are most of the cost.

## Implementations

## History

Boyer, Brassard, Høyer and Tapp posted "Tight bounds on quantum searching" in May 1996, a few weeks after Grover's STOC paper, and it appeared in Fortschritte der Physik in 1998. The paper gave the exact success probability for $M$ marked items, the algorithm on this page for an unknown $M$, a first sketch of quantum counting, and a sharper lower bound. Dürr and Høyer used the algorithm for minimum finding later in 1996, and Brassard, Høyer, Mosca and Tapp made it general in their work on amplitude amplification (2000, published 2002).

## References
