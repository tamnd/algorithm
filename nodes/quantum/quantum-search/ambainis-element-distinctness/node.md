---
tag: VT4428
kind: algorithm
slug: ambainis-element-distinctness
name: Ambainis element distinctness
aliases:
- quantum walk element distinctness
area: quantum/quantum-search
level: research
summary: A quantum walk on r-element subsets of the input. It decides element distinctness with O(N^(2/3)) queries and k-distinctness with O(N^(k/(k+1))), with bounded error.
solves: [element-distinctness, k-distinctness]
model: quantum-query-model
complexity:
  vars: {N: the number of input values, k: the number of equal values to find, M: the size of the value alphabet}
  queries: {worst: O(N^(k/(k+1)))}
  space: {extra: O(N^(k/(k+1)) (log N + log M))}
properties: {deterministic: false, exact: false, one_sided_error: true, oracle: bit}
history:
  year: 2003
  people: [Andris Ambainis]
  note: First posted as arXiv:quant-ph/0311001 in 2003, presented at FOCS 2004 and published in SIAM Journal on Computing in 2007.
prereqs: [element-distinctness, grover-search, amplitude-amplification, quantum-query-model]
see_also: [k-distinctness, quantum-walk-search, belovs-k-distinctness, brassard-hoyer-tapp-collision, element-distinctness-lower-bound, collision-finding, quantum-query-complexity, quantum-random-access-memory]
sources:
  - paper: doi:10.1137/S0097539705447311
    title: "Andris Ambainis, Quantum walk algorithm for element distinctness, SIAM Journal on Computing 37(1), 2007, pages 210-239"
    locator: with the numbering of arXiv:quant-ph/0311001, Algorithm 1 (one walk step), Algorithm 2 (one k-collision), Theorems 3 and 4, Lemmas 1 to 3, Algorithm 3 and Theorem 9 (any number of k-collisions), Section 6 (comparison model and running time), Section 7 (open problems)
  - paper: doi:10.1109/FOCS.2004.54
    title: "Andris Ambainis, Quantum walk algorithm for element distinctness, Proceedings of the 45th IEEE FOCS, 2004, pages 22-31"
    locator: the conference version; this page follows the arXiv numbering
  - paper: doi:10.1137/S0097539702402780
    title: "Harry Buhrman, Christoph Dürr, Mark Heiligman, Peter Høyer, Frédéric Magniez, Miklos Santha and Ronald de Wolf, Quantum algorithms for element distinctness, SIAM Journal on Computing 34(6), 2005, pages 1324-1330"
    locator: the main result (O(N^(3/4)) queries with amplitude amplification)
  - paper: doi:10.1145/1008731.1008735
    title: "Scott Aaronson and Yaoyun Shi, Quantum lower bounds for the collision and the element distinctness problems, Journal of the ACM 51(4), 2004, pages 595-605"
    locator: the main theorems (Omega(N^(2/3)) for element distinctness)
  - paper: arxiv:quant-ph/0311038
    title: "Andrew M. Childs and Jason M. Eisenberg, Quantum algorithms for subset finding, Quantum Information and Computation 5(7), 2005"
    locator: the whole paper (the success probability 1 - o(1) of the walk)
---

Ambainis's algorithm solves [element distinctness](/element-distinctness/): given $N$ values $x_1, \ldots, x_N$ through a quantum oracle, decide whether two of them are equal. It uses $O(N^{2/3})$ queries in the [quantum query model](/quantum-query-model/), with bounded one-sided error, and this is optimal by the lower bound of Aaronson and Shi. The same algorithm solves [k-distinctness](/k-distinctness/), which asks for $k$ equal values, with $O(N^{k/(k+1)})$ queries. It was the first algorithm built on a quantum walk with a marked set, and it is the model for the general [quantum walk search](/quantum-walk-search/) of Szegedy and of Magniez, Nayak, Roland and Santha.

## In plain words

A classical computer must read almost all of the list to be sure that no two values are equal. Grover-style search over all pairs is faster, but not the fastest.

This method keeps a bag of about $N^{2/3}$ positions together with their values. A bag that holds both copies of a repeated value is "good". The bag moves slowly: each step takes out one position and puts in another, which costs only two reads. The quantum computer moves all possible bags at the same time, in superposition, and from time to time it marks the good bags with a sign. The moves spread the sign in a controlled way, so the weight of the good bags grows, much as in Grover search. At the end, a measurement gives a bag, and a check of its stored values shows the repeated value.

## The problem

The input is $x = (x_1, \ldots, x_N)$ with $x_i \in [M]$, given by the bit oracle $O_x|i\rangle|b\rangle = |i\rangle|b \oplus x_i\rangle$, where $b$ is a string of $\lceil \lg M \rceil$ bits. The phase form $(-1)^{\langle b, x_i \rangle}$ is equivalent, with one query and [phase kickback](/phase-kickback/). The output is a $k$-collision, a set of $k$ distinct indices $i_1, \ldots, i_k$ with $x_{i_1} = \cdots = x_{i_k}$, or the answer that there is none. Element distinctness is the case $k = 2$. The cost is the number of oracle calls. The result has bounded error, and the error is one-sided: a reported collision is always correct.

Algorithm 2 of the paper, given below, needs the promise that there is at most one $k$-collision. Algorithm 3 removes the promise (see Variants).

## The algorithm

Fix a size $r$ with $k \le r < N - k$. The state space $\mathcal{H}$ has the basis states $|S, y\rangle$, where $S \subseteq [N]$ has $|S| = r$ and $y \notin S$, together with a data register that holds the values $x_i$ for $i \in S$. The space $\mathcal{H}'$ is the same with $|S| = r + 1$ and $y \in S$. Up to the data register, $S$ is a vertex of the Johnson graph on $r$-subsets, and one walk step replaces one element of $S$.

```pseudo id=main
AMBAINIS-K-DISTINCTNESS(O_x, N, k, r)   ▷ promise: at most one k-collision
L1  prepare the uniform superposition of |S⟩|y⟩ over |S| = r, y ∉ S
L2  query x_i for all i ∈ S into the data register      ▷ r queries
L3  repeat t1 times:
L4      flip the phase if the stored values of S hold k equal values   ▷ no query
L5      repeat t2 = ⌈π √r / (3 √k)⌉ times:            ▷ one walk step
L6          reflect y about the uniform state on [N] \ S
L7          add y to S and query x_y into its slot    ▷ 1 query
L8          reflect y about the uniform state on S
L9          erase the slot of y with a query and remove y from S   ▷ 1 query
L10 measure S; if the stored values hold k equal values, return their indices
L11 return "no k-collision"
```

Lines L6 to L9 are Algorithm 1 of the paper. The reflection of L6 maps $|S\rangle|y\rangle$ to $|S\rangle\big((-1 + \frac{2}{N-r})|y\rangle + \frac{2}{N-r}\sum_{y' \notin S, y' \ne y}|y'\rangle\big)$, and L8 is the same with $r + 1$ in place of $N - r$ and $y' \in S$. These reflections make no query. The paper sets $t_1 = O((N/r)^{k/2})$; the exact constant comes from Lemma 3 and the implementation computes it (see Example). The choice $r = \lfloor N^{k/(k+1)} \rfloor$ balances the setup cost against the walk.

## Example

Take $N = 8$, $k = 2$ and $x = (3, 1, 4, 1, 5, 9, 2, 6)$, indexed from 0, so the only collision is $\{1, 3\}$. With $r = \lfloor 8^{2/3} \rfloor = 4$, $t_2 = \lceil 2\pi/(3\sqrt{2}) \rceil = 2$ and $t_1 = 1$:

1. Line L1 gives the uniform superposition of $\binom{8}{4} \cdot 4 = 280$ states $|S, y\rangle$. In 60 of them $S$ contains both 1 and 3, so a measurement now would find the collision with probability $60/280 = 3/14 \approx 0.214$.
2. Line L2 makes 4 queries. The phase flip of L4 then acts on these 60 states.
3. The two walk steps make 4 queries. The probability that the measured $S$ contains $\{1, 3\}$ is now $0.7574$, and line L10 then returns $(1, 3)$.

In total the run makes $r + 2 t_1 t_2 = 8$ queries. At this size there is no saving over reading the input; the table shows the growth. The numbers come from the reduced simulation below, with no randomness. For each $N$ the program takes $r = \lfloor N^{2/3} \rfloor$ and the $t_1 \le 1.5/\alpha$ with the highest success probability, where $\alpha^2 = \binom{N-2}{r-2}/\binom{N}{r}$.

| $N$ | $2^6$ | $2^{10}$ | $2^{16}$ | $2^{20}$ |
|---|---|---|---|---|
| $r$ | 16 | 101 | 1625 | 10321 |
| $t_1, t_2$ | 4, 3 | 8, 8 | 36, 30 | 92, 76 |
| queries $r + 2t_1t_2$ | 40 | 229 | 3785 | 24305 |
| success probability | 0.733 | 0.804 | 0.753 | 0.759 |
| $N^{3/4}$ (Buhrman et al., up to constants) | 23 | 181 | 4096 | 32768 |

The count is about $2.35\,N^{2/3}$ at these sizes. The constant of the $O(N^{3/4})$ algorithm is not part of the table, so the two rows compare only growth rates.

The Python file has two simulations. The full one stores the state vector on $N + \lceil \lg N \rceil$ qubits with the qsim helper: qubit $i < N$ is 1 when $i \in S$, and the higher qubits hold $y$. The data register is a function of $S$, so the program does not store it, but it counts the two queries of every walk step. The reduced one works in the $(2k+1)$-dimensional subspace of Lemma 1 and runs for $N$ up to $2^{20}$. The tests check that the two give the same success probability to within $10^{-9}$ for $N = 6, 7, 8$ with $k = 2$ and $k = 3$, that the state stays normalized, that the query count is $r + 2t_1t_2$, and the worked example (seed 1). They check Lemma 2 for $N = 10^6$, $r = 1000$, $k = 2$: the walk fixes the start state, and its other eigenphases are $2\sqrt{j/r}$ to within $0.1\%$. They check that the success probability is above $0.7$ and the count below $3N^{k/(k+1)}$ for $k = 2, 3$ and $N$ from $2^6$ to $2^{16}$. Last, with seed 2026, they compare the outputs with a brute-force search on 40 random inputs with $N \le 8$ (full simulation) and 60 random inputs with $N = 1000$ (reduced simulation): every reported collision is correct, and inputs with no collision always give "no k-collision".

## Correctness

Line L10 checks the stored values classically, so every reported $k$-collision is real, and an input with no $k$-collision always gives "no k-collision". The rest is the bound on the success probability under the promise of exactly one $k$-collision $K = \{i_1, \ldots, i_k\}$.

- **Lemma 1 (the invariant subspace).** Sort the states $|S, y\rangle$ by the type $(j, l)$, with $j = |S \cap K|$ and $l = 1$ if $y \in K$. There are $2k + 1$ types in $\mathcal{H}$ and in $\mathcal{H}'$. For a fixed $S$, the reflection of L6 acts on the uniform states on $K \setminus S$ and on the rest of $[N] \setminus S$ as a $2 \times 2$ real matrix that depends only on $j$. Lines L7 and L9 move whole types to whole types. So the span of the $2k+1$ uniform type states is invariant.
- **Lemma 2 (the spectrum).** In this subspace one walk step has the eigenvalue 1, with the start state as its eigenvector, and the eigenvalues $e^{\pm i\theta_j}$ with $\theta_j = (2\sqrt{j} + o(1))/\sqrt{r}$ for $j = 1, \ldots, k$. After $t_2$ steps, every eigenphase other than $0$ is at least a constant away from $0$.
- **Lemma 3 (abstract search).** If $U_1$ flips the sign of the good state, $U_2$ fixes the start state and has all other eigenphases in $[\epsilon, 2\pi - \epsilon]$, and $\alpha$ is the overlap of the start and good states, then some $t = O(1/\alpha)$ gives $|\langle \psi_{\mathrm{good}}|(U_2U_1)^t|\psi_{\mathrm{start}}\rangle| = \Omega(1)$.
- **The overlap.** $\alpha^2 = \Pr[K \subseteq S] = \binom{N-k}{r-k}/\binom{N}{r} = (1 - o(1)) (r/N)^k$, so $t_1 = O((N/r)^{k/2})$.

The [correctness proof](proofs/correctness.md) gives the details of the one-sided error and of Lemma 1, and states which parts it takes from the paper.

## Complexity

- **Queries.** The setup makes $r$ queries and each walk step makes 2, so the total is $r + 2t_1t_2 = O(r + (N/r)^{k/2}\sqrt{r})$ (Theorem 4). With $r = N^{k/(k+1)}$ both terms are $O(N^{k/(k+1)})$: $O(N^{2/3})$ for element distinctness (Theorem 3). These are bounded-error query counts in the quantum query model with the bit oracle.
- **Memory.** $O(r(\log N + \log M))$ qubits for the set and its values.
- **Time.** Section 6 builds a data structure, a hash table with a skip list, in which each set has one unique representation. With gates for random access to a quantum memory (a [quantum random access memory](/quantum-random-access-memory/)), the running time is $O(N^{k/(k+1)} \log^c(N + M))$ for a constant $c$, and the memory grows to $O(r \log^3(N + M))$ qubits. Without such gates, one update of $S$ costs $\Omega(r)$ gates.
- **Comparison model.** If the oracle only compares $x_i$ with $x_j$, a binary search inserts each new element, and the count becomes $O(N^{k/(k+1)} \log N)$ (Section 6.1).
- **Time and space together.** With room for only $r$ values, the query count is $O(N/\sqrt{r})$ for element distinctness. Section 7 of the paper asks whether this is optimal.

## Properties

- One-sided error: a "no" input never gives a wrong collision, and a "yes" input gives a correct one with constant probability, which repetition raises to $1 - \delta$ with $O(\log(1/\delta))$ runs.
- Optimal for element distinctness: Aaronson and Shi proved that every bounded-error quantum algorithm needs $\Omega(N^{2/3})$ queries. The page [element distinctness lower bound](/element-distinctness-lower-bound/) is a different result: $\Omega(N \log N)$ for classical algebraic computation trees.
- For $k \ge 3$ it is not optimal: Belovs found a smaller exponent (see [Belovs's k-distinctness algorithm](/belovs-k-distinctness/)).
- The walk acts on the data register through queries only. Between queries the algorithm uses only reflections and data structure updates that do not depend on $x$.

## Variants and improvements

- **Any number of collisions (Algorithm 3, Theorem 9).** The paper runs Algorithm 2 on a sequence of smaller random subsets $T_1 = [N], T_2, \ldots$ of the input, each about $2k/(2k+1)$ times the size of the last. With probability at least $1/2$ one of them holds exactly one $k$-collision. The subsets come from almost $2k\lg N$-wise independent permutations, so that they need little memory. The query count stays $O(N^{k/(k+1)})$, and the success probability is at least $(1 - o(1))p/2$, with $p$ the success probability of Algorithm 2.
- **Szegedy's framework.** Szegedy (FOCS 2004) recast the walk as the quantum form of a Markov chain. His analysis handles any number of marked sets at once, so the general case needs no random subsets. See [quantum walk search](/quantum-walk-search/).
- **A better constant.** Childs and Eisenberg showed that the success probability of the walk is $1 - o(1)$ with suitable parameters, and extended it to the search for a subset with a given property.
- **Uses of the walk.** Magniez, Santha and Szegedy used it for [triangle finding](/magniez-santha-szegedy-triangle/), and Buhrman and Špalek used Szegedy's version for matrix product checking.

## When to use it

- To find a repeated value, a repeated $k$-tuple of values, or a subset with a property that can be checked from stored data, when the cost is the number of queries.
- For collisions of a function that is known to be two-to-one, the [Brassard-Høyer-Tapp algorithm](/brassard-hoyer-tapp-collision/) needs only $O(N^{1/3})$ queries; this algorithm does not use the promise.
- For $k \ge 3$ with constant $k$, [Belovs's algorithm](/belovs-k-distinctness/) has a smaller query exponent, but this one gives an explicit and time-efficient walk.

## Pitfalls

- **Grover search alone is not enough.** A search over all pairs needs $O(N)$ queries. The best Grover-type method, the algorithm of Buhrman et al., needs $O(N^{3/4})$. The walk is what brings the count down to $O(N^{2/3})$.
- **Query bound versus time bound.** $O(N^{2/3})$ counts queries. The time bound of Section 6 needs random access to a quantum memory and a set representation that is independent of the history. A classical sort decides element distinctness in $O(N \log N)$ time; that is a time bound in another model, so the two numbers do not compare directly.
- **Unique representation.** If the data structure for $S$ depends on the order of the updates, two paths to the same $S$ give different basis states, and the interference that the analysis needs is lost.
- **The promise of Algorithm 2.** With several $k$-collisions, the analysis of Algorithm 2 does not apply as written. Use Algorithm 3 or Szegedy's analysis.
- **Fixed run time.** A classical subroutine inside the walk must stop after a fixed number of steps; a subroutine that is only fast on average cannot be made reversible at the same cost.

## Implementations

## History

Buhrman, Dürr, Heiligman, Høyer, Magniez, Santha and de Wolf gave an $O(N^{3/4})$-query algorithm in 2001, and Aaronson and Shi proved the $\Omega(N^{2/3})$ lower bound in 2002. Ambainis closed the gap with this quantum walk, first posted in November 2003, presented at FOCS 2004 and published in SIAM Journal on Computing in 2007. The same paper gave $O(N^{k/(k+1)})$ for $k$-distinctness and asked whether it is optimal; Belovs showed in 2012 that it is not. Szegedy turned the method into a general speedup of Markov chain search in 2004, and Magniez, Nayak, Roland and Santha gave the framework its standard form in 2007.

## References
