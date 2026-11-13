---
tag: XD74ZG
kind: algorithm
slug: grover-search
name: Grover's search algorithm
aliases:
- Grover's algorithm
- quantum database search
area: quantum/quantum-search
level: intro
summary: Finds one of M marked items among N with about (π/4)√(N/M) oracle queries, against Θ(N/M) classical queries. The speedup is a square root and no more.
solves: [unstructured-search]
model: quantum-query-model
complexity:
  vars: {N: the number of items, M: the number of marked items}
  queries: {worst: Θ((N/M)^(1/2))}
  time: {worst: O((N/M)^(1/2) log N)}
  space: {extra: O(log N)}
properties: {deterministic: false, exact: false, one_sided_error: true, needs_m: true, oracle: phase}
history:
  year: 1996
  people: [Lov K. Grover]
  note: Grover presented the algorithm at STOC 1996. Boyer, Brassard, Høyer and Tapp gave the exact analysis and the version for an unknown number of solutions in 1996.
prereqs: [unstructured-search, quantum-oracle, grover-diffusion-operator, quantum-superposition]
see_also: [amplitude-amplification, bbht-search, grover-optimality, quantum-counting, durr-hoyer-minimum-finding, fixed-point-quantum-search, quantum-walk-search, exhaustive-key-search]
sources:
  - paper: doi:10.1145/237814.237866
    title: "Lov K. Grover, A fast quantum mechanical algorithm for database search, Proceedings of the 28th Annual ACM Symposium on Theory of Computing (STOC 1996), pages 212-219"
    locator: the whole paper (the algorithm and its O(sqrt N) analysis)
  - paper: doi:10.1103/PhysRevLett.79.325
    title: "Lov K. Grover, Quantum mechanics helps in searching for a needle in a haystack, Physical Review Letters 79(2), 1997, pages 325-328"
    locator: the whole paper (the journal version, with the inversion about the mean)
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Sections 2 and 3 (the exact amplitudes after j iterations, the choice floor(pi/(4 theta)) with failure at most t/N, and the case t = N/4)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 6, Section 6.1 (the quantum search algorithm, with Section 6.1.4 on its performance) and Section 6.5 (quantum search of an unstructured database)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6
    locator: Chapter 7, Sections 7.1 (the problem) and 7.2 (Grover's algorithm)
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 8, Section 8.1 (Grover's quantum search algorithm)
---

Grover's search algorithm finds a marked item among $N$ items when the only access to the items is an oracle that recognizes the marked ones. With $M$ marked items and $M$ known, it makes $\lfloor \pi/(4\theta) \rfloor \le (\pi/4)\sqrt{N/M}$ queries to a phase oracle, where $\sin\theta = \sqrt{M/N}$, and it fails with probability at most $M/N$. A classical algorithm needs $\Theta(N/M)$ queries, so the speedup is a square root, and the [optimality theorem](/grover-optimality/) shows that no quantum algorithm does better. This page is the algorithm; the problem, with its classical and quantum bounds, is [unstructured search](/unstructured-search/).

## In plain words

You have a box that answers yes or no about each item, and you want an item with the answer yes. A normal computer asks about the items one at a time. With one good item among a million, it asks about half a million times on average.

A quantum computer can ask about all items at once, in a superposition. But a measurement then gives a random item, and that alone is no better than a guess. Grover's method adds a second step after each question. The question puts a minus sign on the good items. The second step flips every value about the average value. After each round the good items are a little larger and the others a little smaller. After about eight hundred rounds for a million items, a measurement gives a good item almost surely. More rounds are bad: the good items then shrink again.

## The problem

The input is a number $N$, the number $M \ge 1$ of marked items, and a function $f : \{0, 1, \ldots, N-1\} \to \{0, 1\}$ with exactly $M$ items $x$ such that $f(x) = 1$. The algorithm sees $f$ only through a [quantum oracle](/quantum-oracle/). The output is one $x$ with $f(x) = 1$. The cost is the number of oracle calls, in the [quantum query model](/quantum-query-model/). This is [unstructured search](/unstructured-search/) with a known $M$. When $M$ is not known, use [BBHT search](/bbht-search/).

The algorithm uses the phase oracle $O_f |x\rangle = (-1)^{f(x)} |x\rangle$. The bit oracle $|x\rangle|b\rangle \mapsto |x\rangle|b \oplus f(x)\rangle$ gives the phase oracle with one call and one ancilla in the state $(|0\rangle - |1\rangle)/\sqrt{2}$, by [phase kickback](/phase-kickback/). So the query counts below hold for both oracles. The items are stored in $n = \lceil \lg N \rceil$ qubits, and qubit 0 is the least significant bit of $x$.

The name "quantum database search" is misleading. The algorithm searches no stored table. Its input is an oracle that computes $f$. A table in classical memory must first be made into such an oracle, and that costs $\Theta(N)$ operations unless a [quantum random access memory](/quantum-random-access-memory/) is assumed.

## The algorithm

Let $|s\rangle = N^{-1/2} \sum_{x=0}^{N-1} |x\rangle$ be the uniform [superposition](/quantum-superposition/), and let $D = 2|s\rangle\langle s| - I$ be the [Grover diffusion operator](/grover-diffusion-operator/). One *Grover iteration* is $G = D\,O_f$.

```pseudo id=main
GROVER-SEARCH(O_f, N, M)                   ▷ O_f is the phase oracle, 1 ≤ M ≤ N
L1  k ← ⌊π / (4θ)⌋, where sin θ = sqrt(M / N)
L2  prepare |s⟩ = N^(-1/2) Σ_x |x⟩
L3  repeat k times
L4      apply O_f                          ▷ |x⟩ → (-1)^f(x) |x⟩, one query
L5      apply D = 2|s⟩⟨s| - I              ▷ inversion about the mean
L6  measure the register; let x be the result
L7  if f(x) = 1 then return x              ▷ one classical query
L8  return FAIL
```

Line L1 is the only place where $M$ is used. Line L2 is $n$ Hadamard gates on $|0\rangle$ when $N = 2^n$. For other $N$, any unitary $A$ with $A|0\rangle = |s\rangle$ works. Line L5 is $D = H^{\otimes n}(2|0\rangle\langle 0| - I)H^{\otimes n}$, and $2|0\rangle\langle 0| - I$ puts the phase $-1$ on each basis state except $|0\rangle$. On amplitudes, $D$ maps $\sum_x a_x |x\rangle$ to $\sum_x (2\bar a - a_x)|x\rangle$, where $\bar a$ is the mean of the $a_x$. So $D$ is an inversion about the mean. Line L7 checks the result with one classical evaluation of $f$, so the algorithm never returns an unmarked item.

## Example

Take $N = 8$ ($n = 3$ qubits), $M = 1$, and the marked item $x = 5$. Then $\sin\theta = 1/\sqrt{8}$, $\theta \approx 0.3614$, and line L1 gives $k = \lfloor 2.173 \rfloor = 2$. All amplitudes are real. The table gives the amplitude of the marked item, the amplitude of each of the 7 other items, and the probability that a measurement gives item 5.

| iterations | marked | each other | P(measure 5) | $\sin^2((2k+1)\theta)$ |
|---|---|---|---|---|
| 0 | 0.3536 | 0.3536 | 0.1250 | 1/8 |
| 1 | 0.8839 | 0.1768 | 0.7813 | 25/32 |
| 2 | 0.9723 | -0.0884 | 0.9453 | 121/128 |
| 3 | 0.5745 | -0.3094 | 0.3301 | 169/512 |
| 4 | -0.1105 | -0.3757 | 0.0122 | |

The first iteration in detail: line L4 makes the marked amplitude $-0.3536$. The mean of the eight amplitudes is then $(7 \cdot 0.3536 - 0.3536)/8 = 0.2652$. Line L5 maps each other amplitude to $2 \cdot 0.2652 - 0.3536 = 0.1768$ and the marked one to $2 \cdot 0.2652 + 0.3536 = 0.8839$. After $k = 2$ iterations the algorithm succeeds with probability $121/128 \approx 0.945$, with 2 quantum queries and 1 classical check. A third iteration overshoots, and the probability falls to $0.330$.

## Correctness

Let $|g\rangle$ be the uniform superposition of the $M$ marked items and $|b\rangle$ that of the $N - M$ others. Then $|s\rangle = \sin\theta\,|g\rangle + \cos\theta\,|b\rangle$. In the plane of $|g\rangle$ and $|b\rangle$, the oracle is a reflection about $|b\rangle$ and $D$ is a reflection about $|s\rangle$. Two reflections about axes at angle $\theta$ make a rotation by $2\theta$. So, by induction on $k$,

$$G^k|s\rangle = \sin((2k+1)\theta)\,|g\rangle + \cos((2k+1)\theta)\,|b\rangle,$$

and the measurement gives a marked item with probability $\sin^2((2k+1)\theta)$. The choice of line L1 puts $(2k+1)\theta$ within $\theta$ of $\pi/2$, so this probability is at least $\cos^2\theta = 1 - M/N$. The full proof is in proofs/correctness.md.

## Complexity

All counts are in the [quantum query model](/quantum-query-model/), for a known $M$ with $1 \le M \le N$, and the same for the phase oracle and the bit oracle.

- **Queries.** $k = \lfloor \pi/(4\theta) \rfloor \le (\pi/4)\sqrt{N/M}$ quantum queries, plus one classical query in line L7. This is a worst-case count: it does not depend on the input.
- **Error.** One-sided. The algorithm never returns an unmarked item, and it returns FAIL with probability at most $M/N$. For $M \le N/4$ this is at most $1/4$, so the bound is a bounded-error bound. For $M = N/4$, one iteration succeeds with certainty. For $M > N/4$, a classical random sample already succeeds with probability above $1/4$ per query.
- **Zero error.** With $M$ known, a small change of the last iteration gives success with probability 1 and $\Theta(\sqrt{N/M})$ queries. See [amplitude amplification](/amplitude-amplification/).
- **Gates.** One diffusion uses $2n$ Hadamard gates, a few $X$ gates and one $Z$ gate with $n - 1$ controls. The controlled $Z$ needs $O(n)$ Toffoli and one-qubit gates with $n - 2$ ancillas that are returned clean. So the total is $k$ oracle calls plus $O(k \log N)$ gates. The oracle cost must be counted too: if one call costs $c$ gates, the total is $O(\sqrt{N/M}\,(c + \log N))$.
- **Qubits.** $n = \lceil \lg N \rceil$ data qubits, one ancilla for a bit oracle, and the ancillas of the oracle and of the diffusion.

In the same query model, a deterministic classical algorithm needs $N - M$ queries in the worst case, and a randomized one needs $\Theta(N/M)$ expected queries. By the [optimality theorem](/grover-optimality/), each quantum algorithm with error at most $1/3$ needs $\Omega(\sqrt{N/M})$ queries. So Grover's algorithm is optimal up to a constant factor in the [quantum query complexity](/quantum-query-complexity/) of the problem, and for $M = 1$ Zalka showed that it is optimal exactly.

## Properties

- **Bounded error, one-sided.** A returned item is always marked. Repeat the run to make the failure probability smaller: $r$ runs fail with probability at most $(M/N)^r$.
- **Not monotone in $k$.** The success probability is periodic in $k$ with period about $\pi/(2\theta)$. More iterations can make it worse, as the table shows.
- **Needs $M$.** Line L1 needs $M$, or an estimate within a constant factor. [BBHT search](/bbht-search/) removes this need at a constant factor in queries, and [quantum counting](/quantum-counting/) estimates $M$.
- **Uses only the oracle.** The algorithm uses no structure of $f$. This makes it general, and it is also the reason that the speedup is only a square root.
- **Small memory.** The state has $n$ qubits. No classical table of size $N$ is stored.

## Variants and improvements

- **Unknown number of solutions.** [BBHT search](/bbht-search/) picks a random iteration count from a range that grows by a constant factor. Its expected query count is $O(\sqrt{N/M})$ for each $M \ge 1$.
- **Any start procedure.** [Amplitude amplification](/amplitude-amplification/) replaces $|s\rangle$ by $A|0\rangle$ for any quantum algorithm $A$. It boosts a success probability $a$ to a constant with $O(1/\sqrt{a})$ calls of $A$.
- **Counting.** [Quantum counting](/quantum-counting/) applies [phase estimation](/quantum-phase-estimation/) to the Grover iteration to estimate $M$. It solves the [counting problem](/counting-marked-items/).
- **No overshoot.** [Fixed-point quantum search](/fixed-point-quantum-search/) changes the phases of the two reflections, so that more iterations never make the result worse.
- **Minimum.** [Dürr-Høyer minimum finding](/durr-hoyer-minimum-finding/) finds the minimum of $N$ values with $O(\sqrt{N})$ queries, and [Grover adaptive search](/grover-adaptive-search/) uses the same loop for optimization.
- **Search on a graph.** When the items are the vertices of a graph and only local moves are allowed, use [quantum walk search](/quantum-walk-search/) for [spatial search](/spatial-search/).

## When to use it

Use Grover's algorithm when $f$ has no structure that a classical algorithm can use, when $f$ can be computed by a reversible circuit, and when $N/M$ is large. The speedup is quadratic, not exponential. For [SAT](/sat/) on $n$ variables it gives about $2^{n/2}$ queries in place of $2^n$, which is still exponential, so it does not solve [NP-complete](/np-complete/) problems in polynomial time. In [exhaustive key search](/exhaustive-key-search/) on a $128$-bit key it needs about $(\pi/4) 2^{64} \approx 1.4 \cdot 10^{19}$ sequential iterations, each one a full cipher circuit. The iterations are sequential: $P$ quantum machines that split the space cut the time only by a factor $\sqrt{P}$. For these reasons the [security levels](/nist-security-levels/) of post-quantum standards count Grover with a limit on circuit depth.

Do not use it when $M > N/4$: classical random sampling then finds a marked item with a few queries. Do not use it to search a table that is stored in classical memory: reading the table already costs $\Theta(N)$.

## Pitfalls

- **Too many iterations.** "Repeat lines L4 and L5 until success" or $k \leftarrow \lfloor \sqrt{N} \rfloor$ in line L1 is wrong. With $N = 64$ and $M = 1$, $k = 6$ gives success $0.9966$, and $k = 12$ gives $0.0001$. Use $k \leftarrow \lfloor \pi/(4\theta) \rfloor$.
- **The wrong $M$.** Line L1 with $M = 1$ when $M = 4$ gives $k = 6$ for $N = 64$, and the success probability is $0.0204$. With the true $M$, $k = 3$ gives $0.9613$. If $M$ is not known, use [BBHT search](/bbht-search/), not a guess.
- **No check of the result.** Returning $x$ after line L6 without line L7 returns an unmarked item with probability up to $M/N$. Keep the classical check.
- **Padding without care.** When $N$ is not a power of two, $H^{\otimes n}$ prepares the uniform state on $2^n$ items, not $N$. Then line L1 must use $2^n$ in place of $N$, and $f$ must be 0 on the items $x \ge N$. Otherwise the angle is wrong.
- **The oracle is free.** A query count hides the cost of one oracle call. Compare total gate counts, and say so when a query bound is compared with a classical time bound.

## Implementations

## History

Lov Grover presented the algorithm at STOC in May 1996, and a longer version appeared in Physical Review Letters in 1997. In 1996 Boyer, Brassard, Høyer and Tapp gave the exact formula $\sin^2((2k+1)\theta)$ for $M$ marked items, showed the overshoot, and gave the version for an unknown $M$. Bennett, Bernstein, Brassard and Vazirani had already shown that $\Omega(\sqrt{N})$ queries are necessary, so the algorithm was optimal up to a constant factor from the start; Zalka proved exact optimality in 1999. Brassard, Høyer, Mosca and Tapp made the method general as amplitude amplification.

## References
