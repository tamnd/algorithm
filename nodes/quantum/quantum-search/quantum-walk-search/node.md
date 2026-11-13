---
tag: ARW077
kind: algorithm
slug: quantum-walk-search
name: Quantum walk search
aliases:
- Szegedy walk search
- Ambainis quantum walk search
area: quantum/quantum-search
level: advanced
summary: Finds a marked state of a Markov chain with a quantum walk. Cost O(S + (U/sqrt(delta) + C)/sqrt(epsilon)), a square-root gain over a classical random walk (MNRS).
solves: [spatial-search]
model: quantum-query-model
complexity:
  vars: {S: the setup cost, U: the cost of one walk step, C: the checking cost, d: the spectral gap delta of the chain, e: the lower bound epsilon on the stationary probability of the marked set}
  queries: {worst: O(S + (1/sqrt(e)) (U/sqrt(d) + C))}
properties: {deterministic: false, exact: false, one_sided_error: true, oracle: phase}
history:
  year: 2004
  people: [Mario Szegedy, Frédéric Magniez, Ashwin Nayak, Jérémie Roland, Miklos Santha]
  note: Szegedy defined the walk of a Markov chain at FOCS 2004, after Ambainis's walk for element distinctness. Magniez, Nayak, Roland and Santha gave the search with phase estimation at STOC 2007 (SICOMP 2011).
prereqs: [spatial-search, markov-chain, spectral-gap, amplitude-amplification, quantum-phase-estimation]
see_also: [ambainis-element-distinctness, magniez-santha-szegedy-triangle, stationary-distribution, mixing-time, walk, grover-search, quantum-query-complexity, belovs-k-distinctness]
sources:
  - paper: doi:10.1109/FOCS.2004.53
    title: "Mario Szegedy, Quantum speed-up of Markov chain based algorithms, Proceedings of the 45th IEEE FOCS, 2004, pages 32-41"
    locator: the whole paper (the walk W(P) built from two reflections, its spectrum, and detection with the square root of the hitting time)
  - paper: doi:10.1137/090745854
    title: "Frédéric Magniez, Ashwin Nayak, Jérémie Roland and Miklos Santha, Search via quantum walk, SIAM Journal on Computing 40(1), 2011, pages 142-164"
    locator: with the numbering of arXiv:quant-ph/0608026, Theorem 3 (the cost S + (1/sqrt(eps))(U/sqrt(delta) + C)), Theorem 4 (Szegedy's spectral theorem), Theorem 6 (the approximate reflection with phase estimation, error 2^(1-k)), Theorem 7 (the version with a logarithmic factor) and Section 4 (recursive amplitude amplification removes it)
  - paper: doi:10.1145/1250790.1250874
    title: "Frédéric Magniez, Ashwin Nayak, Jérémie Roland and Miklos Santha, Search via quantum walk, Proceedings of the 39th ACM STOC, 2007, pages 575-584"
    locator: the conference version; this page follows the arXiv numbering
  - paper: doi:10.1137/S0097539705447311
    title: "Andris Ambainis, Quantum walk algorithm for element distinctness, SIAM Journal on Computing 37(1), 2007, pages 210-239"
    locator: with the numbering of arXiv:quant-ph/0311001, Algorithm 2 and Lemma 3 (the first walk with a marked set, on the Johnson graph)
  - paper: arxiv:1002.2419
    title: "Hari Krovi, Frédéric Magniez, Maris Ozols and Jérémie Roland, Quantum walks can find a marked element on any graph, Algorithmica 74(2), 2016"
    locator: the main theorem (finding with interpolated walks in the square root of the extended hitting time); a general locator
  - paper: doi:10.1145/3357713.3384252
    title: "Andris Ambainis, András Gilyén, Stacey Jeffery and Martins Kokainis, Quadratic speedup for finding marked vertices by quantum walks, Proceedings of the 52nd ACM STOC, 2020, pages 412-424"
    locator: the main theorem (finding in the square root of the hitting time, up to a logarithmic factor, for any reversible chain and any marked set)
---

Quantum walk search finds a *marked* state of a [Markov chain](/markov-chain/) $P$ faster than a classical random walk. A classical search that walks on $P$ and checks the current state needs about $S + (1/\varepsilon)(U/\delta + C)$, where $S$ is the cost to sample from the [stationary distribution](/stationary-distribution/) $\pi$, $U$ the cost of one step, $C$ the cost to check a state, $\delta$ the [spectral gap](/spectral-gap/) of $P$, and $\varepsilon \le \pi(M)$ a lower bound on the weight of the marked set $M$. The quantum version of Magniez, Nayak, Roland and Santha (MNRS) needs $O(S + (1/\sqrt{\varepsilon})(U/\sqrt{\delta} + C))$. It uses Szegedy's walk, [quantum phase estimation](/quantum-phase-estimation/) and [amplitude amplification](/amplitude-amplification/). The costs are counted as queries in the [quantum query model](/quantum-query-model/) or as gates, depending on the application. This page is the algorithm; the problem of finding a marked vertex of a graph is [spatial search](/spatial-search/). It also covers the basic discrete-time quantum walk, which has no page of its own.

## In plain words

A random walker on a graph finds a marked spot by moving around and looking. It needs many steps when the marked spots are rare or when the walk spreads slowly. A quantum walker moves along all paths at once, as a wave. The method keeps a wave spread evenly over the graph and repeats two moves. First it flips the sign of the marked spots. Then it flips the sign of everything that is not the even spread, with a measure of the "frequency" of the wave. Each repeat turns the wave a little toward the marked spots, as in Grover search. The number of repeats is about the square root of the classical number of looks, and each repeat needs about the square root of the classical number of steps. At the end, a measurement gives a spot, and one look tells whether it is marked.

## The problem

The input is a reversible, ergodic Markov chain $P$ on a finite set $X$ of size $n$, with stationary distribution $\pi$ and spectral gap $\delta$ (one minus the largest absolute value of the other eigenvalues), and a set $M \subseteq X$ of marked states with $\pi(M) \ge \varepsilon$ whenever $M$ is not empty. The output is an element of $M$, or "none" if $M$ is empty. The algorithm reaches the chain and the marked set through three operations, with costs:

- **Setup**, cost $S$: prepare $|\pi\rangle = \sum_x \sqrt{\pi_x}\,|x\rangle|p_x\rangle$, where $|p_x\rangle = \sum_y \sqrt{P_{xy}}\,|y\rangle$.
- **Update**, cost $U$: apply $|x\rangle|0\rangle \mapsto |x\rangle|p_x\rangle$, its inverse, or the same on the second register.
- **Check**, cost $C$: apply $|x\rangle \mapsto -|x\rangle$ for $x \in M$, the phase oracle of $M$. A bit oracle gives it with one query and [phase kickback](/phase-kickback/).

In the query model, the input is reached only through these operations, and their query costs add up. The result has bounded error, and the error is one-sided: a returned state is checked and is always marked. The bound counts queries; the gates of the walk are a separate cost, and data structures such as the stored values of Ambainis's walk may need a [quantum random access memory](/quantum-random-access-memory/).

## The algorithm

Szegedy's walk lives on $\mathbb{C}^X \otimes \mathbb{C}^X$. Let $A = \mathrm{span}\{|x\rangle|p_x\rangle\}$ and $B = \mathrm{SWAP}(A) = \mathrm{span}\{|p_y\rangle|y\rangle\}$, and let $\mathrm{ref}_A = 2\Pi_A - I$ and $\mathrm{ref}_B = 2\Pi_B - I$. One *walk step* is $W = \mathrm{ref}_B\,\mathrm{ref}_A$, with cost $O(U)$. The state $|\pi\rangle$ is in $A \cap B$, so $W|\pi\rangle = |\pi\rangle$.

```pseudo id=main
QUANTUM-WALK-SEARCH(P, M, ε, t)   ▷ t = ⌈lg(1/Δ)⌉ + O(1) ancilla qubits, Δ ≥ 2 √δ
L1  prepare |π⟩ = Σ_x √π_x |x⟩|p_x⟩, with t ancilla qubits in |0⟩     ▷ cost S
L2  repeat T1 = ⌊π / (4 arcsin √ε)⌋ times:
L3      flip the sign of every state with x ∈ M                      ▷ cost C
L4      phase estimation of W on the ancilla                          ▷ 2^t - 1 walk steps
L5      flip the sign if the ancilla is not 0
L6      undo the phase estimation of L4                               ▷ 2^t - 1 walk steps
L7  measure x; if x ∈ M return x                                      ▷ cost C
L8  return "none"
```

Lines L4 to L6 approximate the reflection $2|\pi\rangle\langle\pi| - I$ on $A + B$: they leave $|\pi\rangle$ unchanged and, up to a small error, change the sign of every other eigenvector of $W$. Lines L3 to L6 form one round of amplitude amplification from $|\pi\rangle$ toward the marked states. When $\varepsilon$ is not known, choose $T_1$ at random as in [BBHT](/bbht-search/). MNRS use $k$ copies of the phase estimation to make the error $2^{1-k}$, and a recursive form of amplitude amplification so that the errors do not add a logarithmic factor.

## Example

Take the lazy walk on the 3-dimensional hypercube, $n = 8$: stay with probability $1/2$, or flip one of the three bits. Its eigenvalues are $1, 2/3, 1/3, 0$, so $\delta = 1/3$, and the phase gap of $W$ is $\Delta = 2\arccos(2/3) \approx 1.68 \ge 2\sqrt{\delta} \approx 1.15$. Mark the vertex $5$, so $\varepsilon = 1/8$ and $T_1 = \lfloor \pi/(4 \cdot 0.3614) \rfloor = 2$.

1. Line L1 gives $|\pi\rangle$. A measurement now would find the vertex $5$ with probability $1/8$.
2. Each of the 2 rounds makes one check and, with $t = 3$ ancilla qubits, $2 \cdot 7 = 14$ walk steps.
3. After the rounds, the probability that line L7 measures $5$ is $0.9399$.

With exact reflections, amplitude amplification gives $\sin^2(5 \arcsin\sqrt{1/8}) = 0.9453$. The simulation gives $0.9399$, $0.9404$ and $0.9452$ for $t = 3, 4, 6$, so the error of the approximate reflection goes down as $t$ grows. The lazy cycle on 8 vertices has a smaller gap, $\delta = (1 - \cos(\pi/4))/2 \approx 0.146$, and needs more precision: $0.8590$ with $t = 3$ and $0.9448$ with $t = 6$. The total cost here is 1 setup, 3 checks and 28 walk steps, more than reading all 8 vertices; the gain shows only for large $n$.

For element distinctness, Ambainis's walk is this framework on $r$-subsets of the $N$ inputs: $S = r$ queries, $U = O(1)$ queries, $C = 0$, $\delta \approx 1/r$ and $\varepsilon \approx (r/N)^2$. The quantum cost $r + N/\sqrt{r}$ is $O(N^{2/3})$ at $r = N^{2/3}$, while the classical walk needs $r + N^2/r \ge N$.

The Python file builds the state vector of all three registers with the qsim helper: qubits $0$ to $m - 1$ hold $x$, qubits $m$ to $2m - 1$ hold $y$, and the higher qubits are the ancilla, with qubit 0 the least significant bit. The tests check that $W$ is unitary (lazy cycle on 4 vertices, full matrix), and Szegedy's spectral theorem in closed form on the lazy hypercube, the lazy 8-cycle and the complete graph with loops: for every eigenvector $v$ of $P$ with eigenvalue $\lambda$, the vectors $a = \sum_x v_x|x\rangle|p_x\rangle$ and $b = \mathrm{SWAP}\,a$ satisfy $Wa = 2\lambda b - a$ and $Wb = (4\lambda^2 - 1)b - 2\lambda a$ to within $10^{-9}$. They check that lines L4 to L6 fix $|\pi\rangle$ exactly and change the sign of the other eigenvectors to within the phase estimation bound, that the success probability matches exact amplitude amplification to within $10^{-9}$ on the complete graph and $10^{-3}$ on the hypercube with $t = 6$, and that the count of walk steps is $2T_1(2^t - 1)$. With seed 2026 they run 45 searches on random marked sets of size 0 to 3 and compare with a scan of all vertices: a returned vertex is always marked, an empty marked set always gives "none", and at least 80% of the other runs find a marked vertex. Last, they check the cost formula for the Johnson graph at $N = 10^4$ and $10^6$.

## Correctness

The proof page has the details. Three facts give the result.

1. **The spectrum of $W$** (Szegedy; Theorem 4 of MNRS). Let $D_{xy} = \sqrt{P_{xy}P_{yx}}$, which has the same eigenvalues as $P$ when $P$ is reversible. For an eigenvector $v$ of $D$ with eigenvalue $\cos\theta$, the plane spanned by $a = \sum_x v_x|x\rangle|p_x\rangle$ and $b = \mathrm{SWAP}\,a$ is invariant under $W$, and $W$ has the eigenvalues $e^{\pm 2i\theta}$ on it. The eigenvalue 1 of $P$ gives $|\pi\rangle$, the only eigenvector of $W$ in $A + B$ with eigenvalue 1, since $P$ is ergodic. Every other eigenvalue $\lambda = \cos\theta$ of $P$ has $|\lambda| \le 1 - \delta$, so $e^{\pm 2i\theta}$ is at an angle of at least $\Delta = 2\arccos(1 - \delta)$ from 1, and $\Delta \ge 2\sqrt{2\delta} \ge 2\sqrt{\delta}$ because $\cos u \ge 1 - u^2/2$.
2. **The approximate reflection** (Theorem 6 of MNRS). Phase estimation with $t = \lceil \lg(1/\Delta) \rceil + O(1)$ ancilla qubits outputs 0 on $|\pi\rangle$ with certainty, and outputs 0 with probability at most a small constant on every eigenvector with phase at least $\Delta$. So L4 to L6 fix $|\pi\rangle$ and change the sign of the rest of $A + B$, up to an error that $k$ copies make $2^{1-k}$. They use $2(2^t - 1) = O(1/\Delta) = O(1/\sqrt{\delta})$ walk steps.
3. **Amplitude amplification.** Let $|\mu\rangle$ be the normalized part of $|\pi\rangle$ on marked $x$, so $\langle \mu|\pi\rangle = \sqrt{\pi(M)} \ge \sqrt{\varepsilon}$. Line L3 is the reflection about the unmarked part, L4 to L6 the reflection about $|\pi\rangle$, and their product rotates the plane of $|\pi\rangle$ and $|\mu\rangle$ by $2\arcsin\sqrt{\pi(M)}$, as in [Grover search](/grover-search/). After $T_1 = O(1/\sqrt{\varepsilon})$ rounds the measurement of L7 gives a marked state with constant probability.

## Complexity

- **Cost:** $O(S + (1/\sqrt{\varepsilon})(U/\sqrt{\delta} + C))$, by Theorem 3 of MNRS. A simpler analysis with $k = O(\log(1/\varepsilon))$ copies gives an extra factor $\log(1/\varepsilon)$ on the $U$ term (Theorem 7); recursive amplitude amplification removes it.
- **Classical comparison:** the random walk search costs $O(S + (1/\varepsilon)(U/\delta + C))$, so both the number of checks and the number of steps between checks get a square root.
- **Hitting time:** Szegedy's own algorithm detects a marked state with $O(\sqrt{HT})$ walk steps for a symmetric chain, where $HT$ is the classical hitting time of $M$. Finding with $\tilde{O}(\sqrt{HT})$ for every reversible chain and marked set is the 2020 result of Ambainis, Gilyén, Jeffery and Kokainis.
- **Space:** two registers for states of $X$, plus $O(k\log(1/\Delta))$ ancilla qubits.

## Properties

- **One-sided error:** the returned state is checked, so "none" is the only wrong answer.
- **Bounded error, not exact:** the success probability is a constant below 1 unless $\varepsilon$ is known and the angles fit, and the approximate reflection adds a small error.
- **Model:** the check is a phase oracle on the marked set, equivalent to a bit oracle by phase kickback.
- **Reversible chains:** the cost uses the spectral gap of $P$. For a chain that is not reversible, the singular value gap of $D$ takes its place.
- **Coined walks:** a walk on a graph with a coin register, as used for grids, is a related form; Szegedy's form needs no coin because the second register plays its role.

## Variants and improvements

- **Ambainis's walk** on the Johnson graph of $r$-subsets came first and gives [element distinctness](/ambainis-element-distinctness/) in $O(N^{2/3})$ queries. It is the case of this framework where $|\mu\rangle$ and $|\pi\rangle$ stay in a small invariant subspace.
- **Szegedy's detection** uses $O(\sqrt{HT})$ steps but only decides whether $M$ is empty.
- **Interpolated walks** (Krovi, Magniez, Ozols and Roland) find a marked state in the square root of the extended hitting time; Ambainis, Gilyén, Jeffery and Kokainis (STOC 2020) find one in $\tilde{O}(\sqrt{HT})$ for any marked set.
- **Nested walks.** [Triangle finding](/magniez-santha-szegedy-triangle/) runs a walk whose check is itself a walk.
- **Spatial search on grids.** On a $\sqrt{N} \times \sqrt{N}$ grid the hitting time is $O(N\log N)$, and walks find a unique marked vertex with $O(\sqrt{N}\log N)$ steps (Ambainis, Kempe and Rivosh) and $O(\sqrt{N\log N})$ steps (Tulsi); see [spatial search](/spatial-search/).

## When to use it

Use it when a classical algorithm searches by a random walk with a cheap step and an expensive or rare check, and the quantum operations $S$, $U$ and $C$ can be built. It is the standard tool for query upper bounds on subset problems: element distinctness, [k-distinctness](/k-distinctness/) up to Ambainis's bound, triangle finding, matrix product verification and group commutativity. For plain unstructured search, [Grover search](/grover-search/) is the case $\delta = 1$ and needs no walk. For $k$-distinctness with $k \ge 3$, [Belovs's algorithm](/belovs-k-distinctness/) has a better query bound.

## Pitfalls

- The cost depends on $\sqrt{\delta}$ of the chain, not of the graph. A bipartite walk has the eigenvalue $-1$, which $W$ turns into a second eigenvalue 1; use a lazy walk, as in the example.
- Too few ancilla qubits make the reflection about $|\pi\rangle$ inexact, and the error grows with the number of rounds; the 8-cycle needs $t = 6$ to come close to the ideal value.
- The update must prepare $|p_x\rangle$ coherently, with no garbage, and the setup must prepare $|\pi\rangle$, not a mixed state. For Ambainis's walk the data register is part of the state.
- A query bound is not a time bound: stored data such as the values of a subset may need quantum random access memory.
- Grover search over pairs gives only $O(N^{3/4})$ for element distinctness; the walk is needed for $O(N^{2/3})$.

## Implementations

## History

Aharonov, Ambainis, Kempe and Vazirani studied discrete-time quantum walks on graphs in 2001. Shenvi, Kempe and Whaley used a coined walk for search on the hypercube in 2003. Ambainis's walk for element distinctness (2003) was the first walk to beat Grover search on a natural problem. Szegedy (FOCS 2004) defined the walk of any Markov chain as a product of two reflections and related its spectrum to the chain. Magniez, Nayak, Roland and Santha (STOC 2007, SICOMP 2011) combined it with phase estimation and amplitude amplification and gave the general cost $S + (1/\sqrt{\varepsilon})(U/\sqrt{\delta} + C)$. Krovi, Magniez, Ozols and Roland and then Ambainis, Gilyén, Jeffery and Kokainis (2020) extended finding to the square root of the hitting time.

## References
