---
tag: RYEEVD
kind: problem
slug: quantum-ordered-search
name: Quantum ordered search
aliases: []
area: quantum/quantum-search
level: research
summary: Find the first 1 in a monotone string of N bits given by a quantum oracle. Binary search needs log2 N queries; quantum algorithms need Θ(log N), with a constant between 0.22 and 0.433.
prereqs: [search-in-sorted-array, quantum-query-model, quantum-oracle]
see_also: [hoyer-neerbek-shi-ordered-search, binary-search, search-lower-bound, unstructured-search, quantum-query-complexity, quantum-adversary-method, polynomial-method, grover-search]
sources:
  - paper: doi:10.1007/s00453-002-0976-3
    title: "Peter Høyer, Jan Neerbek and Yaoyun Shi, Quantum complexities of ordered searching, sorting, and element distinctness, Algorithmica 34(4), 2002, pages 429-448"
    locator: the journal version of the ICALP 2001 paper; this page uses the numbering of arXiv:quant-ph/0102078v2, Theorem 1 (the lower bound) and Theorem 13 (the exact algorithm)
  - paper: doi:10.1007/3-540-48224-5_29
    title: "Peter Høyer, Jan Neerbek and Yaoyun Shi, Quantum complexities of ordered searching, sorting, and element distinctness, Proceedings of ICALP 2001, LNCS 2076, pages 346-357"
    locator: Section 1 (the problem and the earlier bounds) and Section 3 (the lower bound)
  - paper: arxiv:quant-ph/9901059
    title: "Edward Farhi, Jeffrey Goldstone, Sam Gutmann and Michael Sipser, Invariant quantum algorithms for insertion into an ordered list, arXiv:quant-ph/9901059, 1999"
    locator: the whole paper (translation-invariant algorithms and the exact algorithm with about 0.526 log2 N queries)
  - paper: doi:10.1103/PhysRevA.75.032335
    title: "Andrew M. Childs, Andrew J. Landahl and Pablo A. Parrilo, Quantum algorithms for the ordered search problem via semidefinite programming, Physical Review A 75, 032335, 2007"
    locator: the abstract and the main result (an exact algorithm with 4 log_605 N, about 0.433 log2 N, queries)
  - paper: doi:10.1109/FOCS.2008.58
    title: "Michael Ben-Or and Avinatan Hassidim, The Bayesian learner is optimal for noisy binary search (and pretty good for quantum as well), Proceedings of the 49th IEEE FOCS, 2008, pages 221-230"
    locator: the quantum part (a zero-error algorithm with about 0.32 log2 N expected queries); section not checked
  - paper: arxiv:0708.3396
    title: "Andrew M. Childs and Troy Lee, Optimal quantum adversary lower bounds for ordered search, Proceedings of ICALP 2008, LNCS 5125, pages 869-880"
    locator: the abstract (the best adversary bound, also with negative weights, is (1/pi) ln N + O(1))
  - paper: arxiv:2609.34293
    title: "Joseph Carolan and Andrew M. Childs, Optimal quantum algorithms for ordered search, arXiv:2609.34293, 2026"
    locator: the abstract (a preprint; it claims algorithms with (1/pi) ln N + o(log N) queries)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6
    locator: Chapter 11 (quantum query lower bounds, the polynomial and adversary methods)
---

Quantum ordered search is the problem of finding a key in a sorted list of $N$ items, when the list can be read only through a [quantum oracle](/quantum-oracle/) and the cost is the number of queries. Classically, [binary search](/binary-search/) needs $\lceil \log_2 N \rceil$ queries, and the [search lower bound](/search-lower-bound/) shows that no comparison algorithm does better. A quantum algorithm also needs $\Theta(\log N)$ queries, so the quantum speedup is only a constant factor. The best constant is between about $0.221$ and $0.433$ for exact algorithms. This page is the problem and its bounds. The algorithm of Høyer, Neerbek and Shi, with $\log_3 N + O(1)$ queries, is on the page [Høyer-Neerbek-Shi ordered search](/hoyer-neerbek-shi-ordered-search/).

## In plain words

You have a sorted list and you want the place of a value in it. Binary search halves the list with each question, so a list of a million items takes twenty questions. No normal method can do better, because each answer is only yes or no.

A quantum computer can ask several questions at once. For a sorted list this helps less than for an unsorted one. The best quantum methods still need a number of questions that grows like the number of digits of the list size. They save a constant factor. A list of a million items may take about nine questions instead of twenty, but never one or two.

## Definition

The input is an integer $N \ge 1$ and a bit string $x = x_0 x_1 \cdots x_{N-1}$ that is monotone, $x_0 \le x_1 \le \cdots \le x_{N-1}$, with $x_{N-1} = 1$. The output is

$$f(x) = \min\{\, i : x_i = 1 \,\}.$$

There are exactly $N$ such strings, one for each answer $a$: the string $0^a 1^{N-a}$. The algorithm sees $x$ only through the bit oracle $O_x |i\rangle|b\rangle = |i\rangle|b \oplus x_i\rangle$, or through the phase oracle $|i\rangle \mapsto (-1)^{x_i}|i\rangle$. One call of the bit oracle on an ancilla in the state $(|0\rangle - |1\rangle)/\sqrt{2}$ gives the phase oracle by [phase kickback](/phase-kickback/), and the bit oracle is made from one controlled call of the phase oracle. So the query counts below hold for both oracles, up to one ancilla. The cost is the number of oracle calls in the [quantum query model](/quantum-query-model/). The page writes $\lg$ for $\log_2$ in the text where it helps.

This is the same problem as [search in a sorted array](/search-in-sorted-array/), seen through queries. For a sorted array $y_0 \le y_1 \le \cdots \le y_{N-2}$ and a key $z$, set $x_i = 1$ if $i = N-1$ or $y_i \ge z$, and $x_i = 0$ otherwise. Then $f(x)$ is the first position whose item is at least $z$, which is the insertion point of $z$. One comparison of $z$ with $y_i$ is one query of $x_i$. For a quantum algorithm the comparison must be a reversible oracle, so the key and the array must be available to the circuit, and the circuit must uncompute any work it does.

The algorithm is *exact* if it outputs $f(x)$ with probability 1 for every input. It has *bounded error* if it is correct with probability at least $2/3$ for every input. It has *zero error* if it either outputs $f(x)$ or says "do not know", and the cost then is the expected number of queries.

## Variants

- **Exact, zero-error and bounded-error search.** The constants differ. The known upper bounds for the exact case are the smallest that are proved; the zero-error case has a smaller expected count.
- **Membership.** Decide whether $z$ is in the list. This is one more query after the search: compare $z$ with the item at the found position.
- **Insertion.** Farhi, Goldstone, Gutmann and Sipser state the problem as the insertion of a new item into an ordered list. It is the same problem.
- **Comparison-based sorting and element distinctness.** Høyer, Neerbek and Shi prove the bounds for ordered search together with lower bounds for these two problems, when the only access to the items is by comparisons: $(1 - 2\sqrt{\varepsilon(1-\varepsilon)}) \frac{N}{2\pi}(H_N - 1)$ comparisons for sorting and $(1 - 2\sqrt{\varepsilon(1-\varepsilon)}) \frac{\sqrt{N}}{2\pi}(H_N - 1)$ for [element distinctness](/element-distinctness/), with error $\varepsilon$ (Theorems 2 and 3 of the arXiv version). So sorting has no quantum speedup beyond a constant factor.

## Examples

- **A small instance.** The sorted array $(2, 3, 5, 7, 11, 13, 17, 19)$ with the key $z = 11$ gives $N = 9$ and $x = 000011111$: positions 4 to 7 hold items at least 11, and position 8 is the sentinel. So $f(x) = 4$, the position of 11. With $z = 12$, $x = 000001111$ and $f(x) = 5$, the insertion point of 12.
- **Why classical search needs $\lceil \lg N \rceil$ queries.** Each classical query has two outcomes, so $q$ queries separate at most $2^q$ inputs, and there are $N$ inputs. For $N = 9$ this gives 4 queries.
- **Why one quantum query is not enough for large $N$.** The lower bound below is $\frac{1}{\pi}(\ln N - 1)$ for exact algorithms. It is larger than 1 when $\ln N > \pi + 1$, that is, for $N \ge 63$. For $N = 10^6$ it is about $4.08$, so every exact quantum algorithm needs at least 5 queries for a million items.

The information argument of the second item does not hold for quantum queries. A quantum query acts on a superposition of positions, and its answer is not a single bit. This is why the quantum count can be smaller than $\lceil \lg N \rceil$.

## Known algorithms

- [Binary search](/binary-search/), classical and exact: $\lceil \lg N \rceil$ queries.
- Farhi, Goldstone, Gutmann and Sipser (1999): exact quantum algorithms that are *translation invariant*, with $3 \log_{52} N \approx 0.526 \lg N$ queries.
- [Høyer-Neerbek-Shi ordered search](/hoyer-neerbek-shi-ordered-search/) (2001): exact, $\log_3 N + O(1) \approx 0.631 \lg N$ queries, with a construction that is easy to state and to check.
- Childs, Landahl and Parrilo (2007): exact, about $0.433 \lg N$ queries, found by a numerical search over translation-invariant algorithms with semidefinite programming.
- Ben-Or and Hassidim (2008): zero error, about $0.32 \lg N$ queries in expectation.
- Carolan and Childs (2026, preprint): algorithms with $\frac{1}{\pi}\ln N + o(\log N)$ queries, which would make the lower bound below tight. The claim is not yet in a refereed venue.

## Bounds

All bounds count oracle queries in the quantum query model, for the worst input, except that zero-error algorithms count the expected queries. $H_N = \sum_{k=1}^{N} 1/k$ is the $N$-th harmonic number, and $H_N - 1 > \ln N - 1$.

| model | error | lower bound | best proved upper bound |
|---|---|---|---|
| classical deterministic | exact | $\lceil \lg N \rceil$ | $\lceil \lg N \rceil$ (binary search) |
| classical randomized | bounded | $\Omega(\log N)$ | $\lceil \lg N \rceil$ |
| quantum | exact | $\frac{1}{\pi}(\ln N - 1) \approx 0.221 \lg N$ | $4 \log_{605} N \approx 0.433 \lg N$ |
| quantum | zero error (expected) | $\Omega(\log N)$ | about $0.32 \lg N$ |
| quantum | error $\varepsilon$ | $(1 - 2\sqrt{\varepsilon(1-\varepsilon)})\frac{1}{\pi}(H_N - 1)$ | the exact bound |

- The quantum lower bounds are Theorem 1 of Høyer, Neerbek and Shi. They prove it with a weighted all-pairs inner product argument, a form of the [quantum adversary method](/quantum-adversary-method/). Earlier lower bounds were $\Omega(\sqrt{\log N / \log\log N})$ by Buhrman and de Wolf, $\lg N / (2 \lg \lg N)$ by Farhi, Goldstone, Gutmann and Sipser, and $\frac{1}{12}\lg N - O(1)$ by Ambainis, as Høyer, Neerbek and Shi list them.
- Childs and Lee (2008) show that the adversary method, also with negative weights, cannot prove more than $\frac{1}{\pi} \ln N + O(1)$. So a better lower bound needs another method, or the bound is tight. The 2026 preprint of Carolan and Childs claims that it is tight.
- A zero-error algorithm with $T$ expected queries, stopped after $3T$ queries, has error at most $1/3$ by Markov's inequality. So the bounded-error bound gives $\Omega(\log N)$ for the zero-error case too.
- With bounded error, the classical randomized lower bound follows from [Yao's minimax principle](/yao-minimax-principle/) with a uniform answer: a decision tree of depth $q$ has at most $2^q$ leaves.

So the quantum speedup for ordered search is a constant factor, at most $\pi \lg e \approx 4.53$ by the lower bound. This contrasts with [unstructured search](/unstructured-search/), where the speedup is a square root. These are query counts. A quantum algorithm also needs gates between the queries, and it reads the array through an oracle, which for a stored array needs a [quantum random access memory](/quantum-random-access-memory/).

## Reductions

- **Search in a sorted array to this problem.** The map $x_i = [y_i \ge z]$ above. One comparison is one query.
- **Membership to search.** One more query after the search.
- **Recursion.** An exact algorithm that searches $m$ items with $q$ queries gives one for $m^k$ items with $kq$ queries: search the first level of a tree with fan-out $m$, then recurse into the found subtree. This is how a finite construction gives a constant $c$ in $c \lg N$: $m$ items in $q$ queries give $q \log_m N$ queries.
- **Ordered search to sorting.** Sort the array together with the key $z$; the position of $z$ in the output is the answer. So each lower bound for ordered search is a lower bound for comparison-based sorting, but a weak one; Theorem 2 of Høyer, Neerbek and Shi gives the stronger $\Omega(N \log N)$ directly.

## Applications

- The standard example of a problem where quantum queries give only a constant factor. Lower-bound methods are tested on it: the first bounds came from a reduction from parity, whose bounds come from the [polynomial method](/polynomial-method/), and the adversary method gives $\frac{1}{\pi}\ln N$.
- A subroutine where a sorted structure is searched inside a quantum algorithm, for example a sorted table of collision candidates in [Brassard-Høyer-Tapp collision finding](/brassard-hoyer-tapp-collision/). The constant factor matters there only in the gate count, not in the exponent.

## References
