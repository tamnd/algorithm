---
tag: 5EDMDS
kind: algorithm
slug: durr-hoyer-minimum-finding
name: Dürr-Høyer minimum finding
aliases:
- Dürr-Høyer algorithm
- quantum minimum finding algorithm
area: quantum/quantum-search
level: advanced
summary: Repeated BBHT search for an entry below the current threshold. It finds an index of the minimum of N values with O(√N) queries and probability at least 1/2.
solves: [minimum-finding]
model: quantum-query-model
complexity:
  vars: {N: the number of entries in the table}
  queries: {expected: O(N^(1/2)), worst: O(N^(1/2))}
  time: {worst: O(N^(1/2) log N)}
  space: {extra: O(log N)}
properties: {deterministic: false, exact: false, oracle: comparison with a threshold, success_probability: at least 1/2, monte_carlo: true}
history:
  year: 1996
  people: [Christoph Dürr, Peter Høyer]
  note: The algorithm is in "A quantum algorithm for finding the minimum", on arXiv in July 1996, shortly after the BBHT search that it uses.
prereqs: [minimum-finding, bbht-search]
see_also: [grover-adaptive-search, grover-search, find-maximum, max-finding-lower-bound, minimum-and-maximum-finding, markov-inequality, grover-optimality, monte-carlo-algorithm]
sources:
  - paper: arxiv:quant-ph/9607014
    title: Christoph Dürr and Peter Høyer, A quantum algorithm for finding the minimum, arXiv:quant-ph/9607014, 1996
    locator: "Section 2 (the algorithm with the time-out 22.5 sqrt(N) + 1.4 lg^2 N, Theorem 1, Lemma 1 on the probability 1/r, Lemma 2 on the expected time m0 = (45/4) sqrt(N) + (7/10) lg^2 N) and Section 3 (repetition, and values that are not distinct)"
  - paper: doi:10.1137/050644719
    title: "Christoph Dürr, Mark Heiligman, Peter Høyer and Mehdi Mhalla, Quantum query complexity of some graph problems, SIAM Journal on Computing 35(6), 2006, pages 1310-1328 (arXiv:quant-ph/0401091)"
    locator: "Section 3 (Theorem 3, the same algorithm with a short proof, and Theorem 6, the d smallest values with O(sqrt(dN)) queries)"
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Section 4 (the search with an unknown number of solutions that each phase runs)
---

Dürr-Høyer minimum finding is a quantum algorithm that finds an index of a smallest entry of a table $T[0], \ldots, T[N-1]$ with $O(\sqrt N)$ queries and probability at least $1/2$. It keeps a threshold index $y$ and runs [BBHT search](/bbht-search/) for an entry with $T[x] < T[y]$; each entry it finds becomes the new threshold. This page is the algorithm; the problem it solves is [quantum minimum finding](/minimum-finding/). Every classical algorithm needs $\Omega(N)$ queries, and by the [optimality of Grover's search](/grover-optimality/) no quantum algorithm can do better than $\Omega(\sqrt N)$.

## In plain words

You want the smallest number in a long list. Pick one number at random as the current best. Then use a quantum search to find any number that is smaller. When you find one, it becomes the new best, and you search again for a number below it.

Each search returns a random smaller number, not the next smaller one. So the best number usually drops by a large step, and only a few searches are needed. The first searches are cheap, because many numbers are smaller. The last ones are slower, because few numbers are left below the best. All together, the work is about the square root of the list length. After a fixed amount of work you stop and return the best number so far.

## The problem

The input is a table $T$ of $N$ values from an ordered set. The algorithm reads $T$ in two ways: a classical query returns one entry $T[x]$, and for a threshold index $y$ the phase oracle $|x\rangle \mapsto (-1)^{[T[x] < T[y]]}|x\rangle$ marks the entries below $T[y]$. Each call of either kind counts as one query in the [quantum query model](/quantum-query-model/). The output is an index $y$ with $T[y] = \min_x T[x]$; if several entries hold the minimum, each of them is correct. Qubit 0 is the least significant bit of $x$, as on [quantum state](/quantum-state/).

## The algorithm

```pseudo id=main
DURR-HOYER-MINIMUM(T, N, B)                  ▷ B is a budget of queries
L1  y ← an index chosen uniformly at random; used ← 1     ▷ read T[y]
L2  m ← 1; λ ← 6/5
L3  while used < B
L4      choose j uniformly at random from {0, 1, ..., ⌈m⌉ - 1}
L5      prepare |s⟩, apply G^j for the marking T[x] < T[y], and measure x   ▷ j queries
L6      used ← used + j + 1
L7      if T[x] < T[y] then y ← x; m ← 1                   ▷ one classical query
L8      else m ← min(λm, √N)
L9  return y
```

$G = D\,O$ is the Grover iteration with the threshold oracle $O$ and the [Grover diffusion operator](/grover-diffusion-operator/) $D$. Between two changes of $y$, lines L4 to L8 are exactly the rounds of BBHT search, from $m = 1$. Dürr and Høyer call BBHT search as a whole and measure the time against the budget; the loop above writes the rounds out, so that every query is counted. The budget proved on this page is

$$B = 2Q(N), \qquad Q(N) = 1 + 18\sqrt N + \ln N\left(\log_{6/5}\sqrt N + 5\right).$$

## Example

Take $N = 16$ and

$$T = (52, 17, 93, 41, 8, 66, 30, 75, 23, 88, 5, 61, 47, 12, 99, 36).$$

The minimum is $T[10] = 5$. A run with the seed 6 of the implementation picks $y = 2$ with $T[2] = 93$ in line L1. Here $t$ is the number of entries below the threshold, and $\Pr$ is the probability $\sin^2((2j+1)\theta)$, with $\sin^2\theta = t/16$, that line L5 gives one of them:

| round | $T[y]$ | $t$ | $m$ | $j$ | $\Pr$ | $x$ | $T[x]$ | line L7 | queries so far |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 93 | 14 | 1 | 0 | 0.875 | 12 | 47 | new threshold | 2 |
| 2 | 47 | 8 | 1 | 0 | 0.5 | 0 | 52 | no | 3 |
| 3 | 47 | 8 | 1.2 | 1 | 0.5 | 15 | 36 | new threshold | 5 |
| 4 | 36 | 6 | 1 | 0 | 0.375 | 5 | 66 | no | 6 |
| 5 | 36 | 6 | 1.2 | 0 | 0.375 | 4 | 8 | new threshold | 7 |
| 6 | 8 | 1 | 1 | 0 | 0.0625 | 11 | 61 | no | 8 |
| 7 | 8 | 1 | 1.2 | 1 | 0.4727 | 13 | 12 | no | 10 |
| 8 | 8 | 1 | 1.44 | 0 | 0.0625 | 3 | 41 | no | 11 |
| 9 | 8 | 1 | 1.728 | 1 | 0.4727 | 10 | 5 | new threshold | 13 |

The thresholds are $93, 47, 36, 8, 5$: four improvements, and the minimum after 13 queries. The run then goes on without a change until the budget $B = 216$ is used, and returns $y = 10$. The exact expected number of queries until the minimum is found, over all random choices, is $9.1$ for 16 distinct values.

## Correctness

Line L7 changes $y$ only to an entry with a smaller value, so $T[y]$ never increases, and each returned $y$ is a valid index. Between two changes of $y$ the loop is a fresh BBHT run with $t$ marked entries, which costs fewer than $9\sqrt{N/t}$ iterations and $\log_{6/5}\sqrt N + 5$ rounds in expectation; for $t > 3N/4$ each round succeeds with probability at least $1/4$. The Grover state gives the same amplitude to every marked entry, so each new threshold is uniform among the entries below the old one. As in Lemma 1 of Dürr and Høyer, the value $v_k$ is then ever the threshold with probability $n_k/R_k$, where $n_k$ entries have the value $v_k$ and $R_k$ entries have a value at most $v_k$. Summing over the values gives $\mathbb{E}[C] \le Q(N)$ for the queries $C$ until the minimum, and [Markov's inequality](/markov-inequality/) gives success with probability at least $1/2$ for $B \ge 2Q(N)$. The full proof is in proofs/correctness.md.

## Complexity

In the [quantum query model](/quantum-query-model/), a run makes fewer than $B + \sqrt N + 2$ queries. The expected number $C$ of queries until $y$ holds a minimum is at most $Q(N) = 1 + 18\sqrt N + \ln N(\log_{6/5}\sqrt N + 5)$, so $O(\sqrt N)$, and the default budget $2Q(N)$ gives success with probability at least $1/2$. The exact values, computed from the closed form of one BBHT round, are much smaller:

| $N$ | exact $\mathbb{E}[C]$ | $\mathbb{E}[C]/\sqrt N$ | $Q(N)$ | budget $2Q(N)$ | Dürr-Høyer time-out | classical $N - 1$ |
|---|---|---|---|---|---|---|
| 16 | 9.1 | 2.27 | 107.9 | 216 | 112.4 | 15 |
| 64 | 20.6 | 2.57 | 213.2 | 427 | 230.4 | 63 |
| 256 | 44.6 | 2.79 | 401.1 | 803 | 449.6 | 255 |
| 1024 | 92.9 | 2.90 | 743.4 | 1487 | 860.0 | 1023 |
| 4096 | 187.6 | 2.93 | 1384.3 | 2769 | 1641.6 | 4095 |
| 16384 | 371.6 | 2.90 | 2611.8 | 5224 | 3154.4 | 16383 |

These values are for distinct entries. Ties change them little: over 40 random patterns of ties for each $N \le 64$, the largest increase was $0.05$. Dürr and Høyer use the time-out $22.5\sqrt N + 1.4\lg^2 N$. It comes from the bound $\frac{9}{2}\sqrt{N/t}$ that Boyer, Brassard, Høyer and Tapp state for one search, and it counts $\lg N$ time steps for each preparation. The [BBHT page](/bbht-search/) proves only $9\sqrt{N/t}$, which is why the proved budget here has $36\sqrt N$ in place of $22.5\sqrt N$. With the exact means above, Markov's inequality still gives success with probability at least $0.88$ under the time-out of Dürr and Høyer for these $N$.

The gates per query are those of [Grover's search](/grover-search/): $O(\log N)$ for the diffusion besides the oracle, so the time is $O(\sqrt N\log N)$. The extra space is $O(\log N)$ qubits and the classical values $y$, $T[y]$, $m$ and the counter.

## Properties

- **Bounded error, never an invalid output.** The output is always an index, and its value is the minimum with probability at least $1/2$. Repetition makes the error smaller.
- **Monotone threshold.** $T[y]$ never increases. A run stopped early returns the best entry found so far.
- **No knowledge of the values.** The algorithm uses only comparisons with the current threshold, so it works for any ordered set.
- **Ties.** Entries with equal values are allowed; the proof covers them, and any minimum index can be the output.
- **Quadratic speedup.** $O(\sqrt N)$ queries against $N - 1$ classical comparisons, and this is optimal up to a constant.

## Variants and improvements

- **Repetition.** Dürr and Høyer note that $c$ independent runs, followed by the smallest of the outputs, fail with probability at most $2^{-c}$. One run with $c$ times the budget is at least as good, because it keeps the threshold it has found.
- **Maximum finding.** Reverse the comparison in lines L5 and L7.
- **The $d$ smallest values.** Dürr, Heiligman, Høyer and Mhalla keep a set of $d$ indices and replace its worst element with each improvement. They find the $d$ smallest values, also under a condition of different types, with $O(\sqrt{dN})$ queries, and use this for graph problems such as the [minimum spanning tree](/minimum-spanning-tree/).
- **Stopping at a target.** If a target value is known, stop as soon as $T[y]$ is at or below it. The implementation offers this, and the tests use it to measure $C$.
- **Optimization of cost functions.** [Grover adaptive search](/grover-adaptive-search/) runs the same loop on a cost function given as a circuit, often with other rules for the number of iterations.

## When to use it

Use it when the entries are expensive to compute, the table has no structure to exploit, and $N$ is large. The expected cost is about $2.9\sqrt N$ queries, so it beats the classical $N - 1$ comparisons in expectation from $N = 6$ on, but the proved budget for success $1/2$ is larger, and a gain over a classical scan with the proved guarantee needs $N$ in the thousands. For sorted or otherwise structured data, a classical method is faster. For a minimum within a tolerance, or for the $d$ smallest entries, use the variants above.

## Pitfalls

- **Taking the measured entry without a check.** "L7 $y \leftarrow x$" accepts an entry that the measurement gives even when it is not below the threshold, so the threshold can rise. Use "L7 if $T[x] < T[y]$ then $y \leftarrow x$".
- **Marking equal values.** "L5 ... for the marking $T[x] \le T[y]$" marks $y$ itself and its ties, so many rounds measure an entry that is no improvement, and at the minimum the search never runs dry. Use the strict marking $T[x] < T[y]$ of line L5.
- **Stopping at the first failure.** "L8 else return $y$" stops when one round fails, but a round with a small $m$ fails often even when better entries exist. Keep "L8 else $m \leftarrow \min(\lambda m, \sqrt N)$" and stop only on the budget.
- **A fixed number of Grover iterations.** "L4 $j \leftarrow \lfloor \pi/4 \cdot \sqrt N \rfloor$" uses the count for one marked entry, which overshoots when many entries are below the threshold. Keep the random $j$ of line L4 from BBHT search.
- **A budget that ignores the classical checks.** "L6 used $\leftarrow$ used $+ j$" counts only the oracle calls in line L5, and the run can make $O(\log^2 N)$ more queries than the budget says. Use "L6 used $\leftarrow$ used $+ j + 1$".

## Implementations

## History

Grover gave his search algorithm in 1996, and Boyer, Brassard, Høyer and Tapp extended it in May 1996 to an unknown number of solutions. Dürr and Høyer used that search in July 1996 to find the minimum of a table with $O(\sqrt N)$ queries, which the lower bound for search shows to be optimal up to a constant. Dürr, Heiligman, Høyer and Mhalla gave a short proof of the same bound in 2004 and extended the method to the $d$ smallest values and to graph problems. The loop is also the basis of Grover adaptive search for optimization.

## References
