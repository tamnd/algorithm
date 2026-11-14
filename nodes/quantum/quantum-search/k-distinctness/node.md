---
tag: C2HKQ4
kind: problem
slug: k-distinctness
name: k-distinctness
aliases:
- quantum k-distinctness
area: quantum/quantum-search
level: research
summary: Decide whether k of N oracle values are equal. For constant k, quantum algorithms need O(N^(3/4 - 1/(4(2^k - 1)))) queries, tight for large alphabets by a 2026 preprint; classical ones need Θ(N).
prereqs: [element-distinctness, quantum-query-model, quantum-oracle]
see_also: [ambainis-element-distinctness, belovs-k-distinctness, quantum-query-complexity, quantum-adversary-method, polynomial-method, collision-finding, brassard-hoyer-tapp-collision, quantum-walk-search]
sources:
  - paper: doi:10.1137/S0097539705447311
    title: "Andris Ambainis, Quantum walk algorithm for element distinctness, SIAM Journal on Computing 37(1), 2007, pages 210-239"
    locator: with the numbering of arXiv:quant-ph/0311001, Theorem 3 (O(N^(k/(k+1))) queries) and Section 7, open problem 2 (the reduction that gives Omega(N^(2/3)))
  - paper: doi:10.1109/FOCS.2012.18
    title: "Aleksandrs Belovs, Learning-graph-based quantum algorithm for k-distinctness, Proceedings of the 53rd IEEE FOCS, 2012, pages 207-216"
    locator: with the numbering of arXiv:1205.1534, Theorem 8 (O(N^(1 - 2^(k-2)/(2^k - 1))) queries)
  - paper: doi:10.1145/1008731.1008735
    title: "Scott Aaronson and Yaoyun Shi, Quantum lower bounds for the collision and the element distinctness problems, Journal of the ACM 51(4), 2004, pages 595-605"
    locator: the main theorems (Omega(N^(1/3)) for collision and Omega(N^(2/3)) for element distinctness)
  - paper: doi:10.1145/3188745.3188784
    title: "Mark Bun, Robin Kothari and Justin Thaler, The polynomial method strikes back: tight quantum query bounds via dual polynomials, Proceedings of the 50th ACM STOC, 2018, pages 297-310"
    locator: the k-distinctness lower bound (Omega(N^(3/4 - 1/(2k))) up to a logarithmic factor), arXiv:1710.09079
  - paper: doi:10.4230/LIPIcs.TQC.2020.2
    title: "Nikhil S. Mande, Justin Thaler and Shuchen Zhu, Improved approximate degree bounds for k-distinctness, Proceedings of TQC 2020, LIPIcs 158, pages 2:1-2:22"
    locator: the main result (Omega(N^(3/4 - 1/(4k))) for k at least 4), arXiv:2002.08389
  - paper: arxiv:2604.05133
    title: "Aleksandrs Belovs, Tight quantum lower bound for k-distinctness, arXiv:2604.05133, version 2, 2026"
    locator: Theorem 1.1 (Omega(N^(3/4 - 1/(4(2^k - 1)))) with bounded error, for k = O(1) and an alphabet of size Omega(N^2)), and Section 1 (the history of the bounds); a preprint
  - paper: doi:10.1007/978-3-642-39206-1_10
    title: "Aleksandrs Belovs, Andrew M. Childs, Stacey Jeffery, Robin Kothari and Frédéric Magniez, Time-efficient quantum walks for 3-distinctness, Proceedings of ICALP 2013, LNCS 7965, pages 105-122"
    locator: the main result (3-distinctness in time close to the query bound O(N^(5/7)))
  - paper: doi:10.1145/3564246.3585158
    title: "Stacey Jeffery and Sebastian Zur, Multidimensional quantum walks, Proceedings of the 55th ACM STOC, 2023, pages 1125-1130"
    locator: the application to k-distinctness (time close to Belovs's query bound for every constant k)
---

The $k$-distinctness problem asks whether a list of $N$ values, read through a [quantum oracle](/quantum-oracle/), contains $k$ equal values. For $k = 2$ it is [element distinctness](/element-distinctness/). In the [quantum query model](/quantum-query-model/) with bounded error and constant $k$, Belovs's algorithm of 2012 needs $O(N^{3/4 - 1/(4(2^k - 1))})$ queries, and a 2026 preprint of his proves a matching lower bound for alphabets of size $\Omega(N^2)$. For $k = 2$ this is $\Theta(N^{2/3})$, for $k = 3$ it is $N^{5/7}$, and as $k$ grows it tends to $N^{3/4}$. A classical algorithm needs $\Theta(N)$ queries for every $k \ge 2$. This page is the problem and its bounds; the algorithms are on [Ambainis element distinctness](/ambainis-element-distinctness/) and [Belovs's k-distinctness algorithm](/belovs-k-distinctness/).

## In plain words

You have a long list of numbers and can look at one entry at a time. The question is whether some number appears at least $k$ times. For $k = 2$ the question is whether any number repeats.

A classical program must look at almost every entry, because one unseen entry could be the missing copy. A quantum program can ask about many entries in one superposed question, and it can answer with far fewer questions, about $N^{2/3}$ for pairs. Finding three or more equal entries is harder, because the program must collect a pair first and then look for a third copy that matches it. The exact cost for each $k$ was an open question for almost twenty years.

## Definition

**Input.** Integers $N$ and $k \ge 2$, and a list $x = (x_1, \ldots, x_N)$ with $x_i \in [M]$, given by the bit oracle $O_x|i\rangle|b\rangle = |i\rangle|b \oplus x_i\rangle$ on an index register and a register of $\lceil \lg M \rceil$ bits. The phase form of the oracle is equivalent, with one query, by [phase kickback](/phase-kickback/).

**Output.** "Yes" if there are $k$ distinct indices $i_1, \ldots, i_k$ with $x_{i_1} = \cdots = x_{i_k}$, a *$k$-collision*, and "no" otherwise. The search version asks for the indices of a $k$-collision.

**Cost.** The number of oracle calls, with bounded error (success probability at least $2/3$ on every input). The value of $k$ is usually a constant, and bounds are stated for $N \to \infty$ with $k$ fixed.

## Variants

- **Element distinctness**, $k = 2$, has its own page in the foundations area, with the classical $\Omega(N \log N)$ bound for algebraic computation trees. That is a bound in another model.
- **Search versus decision.** The known algorithms find a $k$-collision, and the lower bounds hold already for the decision version.
- **The size of the alphabet.** If $M < N/(k-1)$, the pigeonhole principle forces a $k$-collision, so the problem is only interesting for $M \ge N/(k-1)$. The 2026 lower bound assumes $M = \Omega(N^2)$; for $k = 2$, Ambainis showed that $\Omega(N^{2/3})$ holds already for $M = N$.
- **The promise of at most one $k$-collision.** Some algorithms are first analyzed under this promise and then made general.
- **Time complexity.** Counting all gates, not only queries, the time-efficient algorithms need random access to a quantum memory, a [quantum random access memory](/quantum-random-access-memory/).
- **Random inputs.** If $x$ is uniformly random, the problem changes: Liu and Zhandry found matching bounds for finding $k$ equal values in a random function. Those bounds are for an average case and do not apply to the worst case of this page.
- **Collision finding** is the case where $x$ is known to be two-to-one or one-to-one; see [collision finding](/collision-finding/).

## Examples

- $N = 11$, $k = 3$ and $x = (3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5)$, indexed from 0. The value 5 appears at positions 4, 8 and 10, so the answer is "yes", with the 3-collision $\{4, 8, 10\}$. The values 1 and 3 appear only twice, so they give 2-collisions but no 3-collision.
- $N = 6$, $k = 2$ and $x = (2, 7, 1, 8, 4, 5)$: all values differ and the answer is "no". A classical algorithm can be sure of this only after reading all 6 values.
- $N = 9$, $k = 3$ and $x = (1, 1, 2, 2, 3, 3, 4, 4, 5)$: every value appears at most twice, so the answer is "no", even though there are 4 pairs.

## Known algorithms

| algorithm | queries | notes |
|---|---|---|
| classical sort or hash table | $N$ | reads every value; time $O(N \log N)$ with a sort |
| Grover-type search (Buhrman et al.) | $O(N^{3/4})$ for $k = 2$ | amplitude amplification only |
| [Ambainis](/ambainis-element-distinctness/) | $O(N^{k/(k+1)})$ | quantum walk on $r$-element subsets; also time-efficient with quantum random access memory |
| [Belovs](/belovs-k-distinctness/) | $O(N^{1 - 2^{k-2}/(2^k - 1)})$ | learning graph; the query bound only |
| Belovs, Childs, Jeffery, Kothari and Magniez | $\tilde{O}(N^{5/7})$ time for $k = 3$ | time-efficient form of Belovs's bound |
| Jeffery and Zur | near Belovs's bound, in time, for constant $k$ | multidimensional quantum walks |

All quantum entries are bounded-error query counts or time counts as marked. The two forms of the exponent are equal: $1 - 2^{k-2}/(2^k - 1) = 3/4 - 1/(4(2^k - 1))$. For $k = 2, 3, 4$ Ambainis gives $2/3, 3/4, 4/5$ and Belovs gives $2/3, 5/7, 11/15$.

## Bounds

| bound | source | model and error |
|---|---|---|
| $\Theta(N)$ | adversary argument | classical queries, deterministic or randomized |
| $\Omega(N^{2/3})$ for $k = 2$ | Aaronson and Shi (2002, JACM 2004) | quantum queries, bounded error, $M = \Omega(N^2)$ |
| $\Omega(N^{2/3})$ for every $k \ge 2$ | Aaronson's reduction, in Ambainis's paper | quantum queries, bounded error |
| $\tilde{\Omega}(N^{3/4 - 1/(2k)})$ | Bun, Kothari and Thaler (STOC 2018) | quantum queries, bounded error |
| $\Omega(N^{3/4 - 1/(4k)})$ for $k \ge 4$ | Mande, Thaler and Zhu (TQC 2020) | quantum queries, bounded error |
| $\Omega(N^{3/4 - 1/(4(2^k-1))})$, tight | Belovs (arXiv 2026, preprint) | quantum queries, bounded error, $k = O(1)$, $M = \Omega(N^2)$ |

The 2018 and 2020 bounds use the [polynomial method](/polynomial-method/) with dual polynomials. They tend to $N^{3/4}$ for large $k$ but give nothing better than $N^{2/3}$ for $k = 3$. Belovs's 2026 lower bound uses a new method that combines the polynomial method with ideas from Zhandry's compressed oracle; it is a preprint at the time of writing. The general form of the [quantum adversary method](/quantum-adversary-method/) is tight for every problem, so a matching lower bound always existed; the difficulty was to find one.

## Reductions

- **Element distinctness to $k$-distinctness.** Repeat each value of an element distinctness input $k - 1$ times. A list of $N$ distinct values gives $(k-1)N$ values with no $k$-collision, and one repeated value gives $2k - 2 \ge k$ equal values. So $k$-distinctness on $(k-1)N$ values is at least as hard as element distinctness on $N$ values. This is the remark of Aaronson in Section 7 of Ambainis's paper.
- **Collision finding.** A two-to-one function contains $N/2$ collisions, so finding one is easier: $\Theta(N^{1/3})$ queries, by [Brassard-Høyer-Tapp](/brassard-hoyer-tapp-collision/) and Aaronson and Shi.
- **Triangle finding.** The first quantum triangle algorithms run an element distinctness walk on the vertices; see [triangle finding](/triangle-finding/).

## Applications

- A test problem for quantum query methods. The algorithms led to quantum walks with a marked set and to learning graphs, and the lower bounds led to the method of dual polynomials and to the 2026 method of Belovs.
- Subproblems of other searches: triangle finding and other subgraph searches, and the search for multicollisions (several inputs with one hash value) in the cryptanalysis of hash functions.

## References
