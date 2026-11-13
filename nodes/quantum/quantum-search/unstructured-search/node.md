---
tag: RSG7JK
kind: problem
slug: unstructured-search
name: Unstructured search
aliases:
- unordered search
- black-box search
- database search
area: quantum/quantum-search
level: intro
summary: Find an x with f(x) = 1, given f on N items only through an oracle. Classical algorithms need Θ(N) queries and quantum ones Θ(√N), both with bounded error.
prereqs: [quantum-oracle, quantum-query-model, search-in-unordered-array]
see_also: [grover-search, bbht-search, grover-optimality, counting-marked-items, minimum-finding, search-lower-bound, spatial-search, quantum-ordered-search]
sources:
  - paper: doi:10.1137/S0097539796300933
    title: "Charles H. Bennett, Ethan Bernstein, Gilles Brassard and Umesh Vazirani, Strengths and weaknesses of quantum computing, SIAM Journal on Computing 26(5), 1997, pages 1510-1523"
    locator: the lower bound Omega(sqrt N) for search relative to an oracle, and the remark that Grover's algorithm makes it tight
  - paper: doi:10.1145/502090.502097
    title: "Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4), 2001, pages 778-797"
    locator: Section 2, Table 1 (OR needs N queries in the exact and zero-error settings and Theta(sqrt N) with bounded error)
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Section 4 (search with an unknown number of solutions) and Section 7 (the lower bound for t solutions)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 6, Section 6.5 (quantum search of an unstructured database) and Section 6.6 (optimality of the search algorithm)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6
    locator: Chapter 7, Section 7.1 (the problem), and Chapter 11 (quantum query lower bounds, with the lower bound for search)
---

Unstructured search is the problem of finding an item $x$ with $f(x) = 1$ among $N$ items, when $f$ is given only as an oracle and has no structure to use. In the [query model](/query-model/), each classical algorithm needs $\Theta(N/M)$ queries when $M$ items are marked, and each quantum algorithm needs $\Theta(\sqrt{N/M})$ queries, both with bounded error. This page is the problem and its bounds. The algorithm that meets the quantum bound is [Grover's search algorithm](/grover-search/), and the lower bound is the [optimality theorem](/grover-optimality/).

## In plain words

You have a closed box with a button for each item. When you press a button, the box says yes or no. You must find an item with the answer yes. The box gives no other help: the yes items are not sorted, not grouped and not marked in any other way. So a normal computer must press the buttons one by one, and in the worst case it presses almost all of them.

A quantum computer may press the buttons in a superposition. It still cannot find the yes item at once, but it needs only about the square root of the number of items. No method can do better.

## Definition

**Input.** A number $N \ge 1$ and a function $f : \{0, 1, \ldots, N-1\} \to \{0, 1\}$, given as an oracle. Let $S = \{x : f(x) = 1\}$ be the set of *marked* items and $M = |S|$.

**Output.** The *search* version asks for one $x \in S$, or the answer "none" if $S$ is empty. The *decision* version asks whether $S$ is empty. The decision version is the function $\mathrm{OR}_N(f(0), \ldots, f(N-1))$.

**Access.** A classical algorithm asks for $f(x)$ at a chosen $x$. A quantum algorithm uses a [quantum oracle](/quantum-oracle/): the bit oracle $|x\rangle|b\rangle \mapsto |x\rangle|b \oplus f(x)\rangle$ or the phase oracle $|x\rangle \mapsto (-1)^{f(x)}|x\rangle$. One call of the bit oracle and one ancilla give one call of the phase oracle, by [phase kickback](/phase-kickback/), so query counts are the same for both.

**Cost.** The number of oracle calls, in the [quantum query model](/quantum-query-model/). Other work is free in this model. The error model must be stated: *exact* (always correct), *zero error* (may answer "do not know" with probability at most $1/2$, but is never wrong), or *bounded error* (wrong with probability at most $1/3$).

The word "database" in the alias "database search" is not exact. The input is an oracle that computes $f$, not a table in memory. To search a stored table of $N$ entries with a quantum algorithm, the table must first be made into an oracle, which costs $\Theta(N)$ operations unless a [quantum random access memory](/quantum-random-access-memory/) is assumed.

## Variants

- **Known $M$.** The algorithm knows $M$, or $M = 1$ is promised (*unique search*). This makes exact quantum search possible with $\Theta(\sqrt{N/M})$ queries.
- **Unknown $M$.** The usual case in practice. The quantum bound stays $\Theta(\sqrt{N/M})$ in expectation, and $\Theta(\sqrt{N})$ to answer "none" when $M = 0$.
- **Decision.** Is $M \ge 1$? This is $\mathrm{OR}_N$. Its threshold form asks whether $M \ge t$.
- **Counting.** Estimate $M$. This is the [counting problem](/counting-marked-items/).
- **Minimum.** Find the item with the smallest value of a function. This is [minimum finding](/minimum-finding/), which uses search with a moving threshold.
- **Structured search.** If the items are sorted, the problem is [search in a sorted array](/search-in-sorted-array/), and the quantum version is [quantum ordered search](/quantum-ordered-search/), with $\Theta(\log N)$ queries. If the items are the vertices of a graph and only local moves are allowed, the problem is [spatial search](/spatial-search/).

## Examples

- **A tiny instance.** $N = 8$ and $f(x) = 1$ only for $x = 5$. Then $S = \{5\}$, $M = 1$, and the answer is $5$. A classical algorithm may need 7 queries (after 7 answers "no", the last item is the marked one). Grover's algorithm with 2 queries succeeds with probability $121/128$.
- **The empty case.** $N = 8$ and $f = 0$. The search version must answer "none", and the decision version "no". An exact algorithm must make all 8 queries in the classical case, and also in the quantum case.
- **An unordered array.** For an array $A[0 \ldots N-1]$ and a key $v$, let $f(i) = 1$ if $A[i] = v$. This is [search in an unordered array](/search-in-unordered-array/), whose classical algorithm is [linear search](/linear-search/).
- **Satisfiability.** For a formula $\varphi$ on $n$ variables, let $N = 2^n$ and $f(x) = 1$ if the assignment $x$ satisfies $\varphi$. A circuit for $f$ is small, so the oracle is cheap. This instance ignores the structure of $\varphi$, which [SAT](/sat/) solvers use.
- **Key search.** For a cipher $E$, a known plaintext $p$ and ciphertext $c$, let $f(k) = 1$ if $E_k(p) = c$. This is [exhaustive key search](/exhaustive-key-search/).

## Known algorithms

- **Classical, deterministic.** Query the items in order: [linear search](/linear-search/). It makes at most $N$ queries for the decision version, and at most $N - M$ for the search version with a known $M \ge 1$.
- **Classical, randomized.** Query random items. The expected number of queries is $N/M$ with repetition, and $(N+1)/(M+1)$ without.
- **Quantum, known $M$.** [Grover's search algorithm](/grover-search/) makes $\lfloor \pi/(4\theta) \rfloor \le (\pi/4)\sqrt{N/M}$ queries, where $\sin\theta = \sqrt{M/N}$, and fails with probability at most $M/N$. The exact form of [amplitude amplification](/amplitude-amplification/) never fails.
- **Quantum, unknown $M$.** [BBHT search](/bbht-search/) makes $O(\sqrt{N/M})$ expected queries for $M \ge 1$. With a time-out after $O(\sqrt{N})$ queries, it answers "none" when $M = 0$, with bounded error.
- **Quantum, no overshoot.** [Fixed-point quantum search](/fixed-point-quantum-search/) needs only a lower bound on $M/N$, and more iterations never make it worse.

## Bounds

All bounds count oracle queries, for the worst input. $N$ is the number of items and $M \ge 1$ the number of marked items.

| model | error | search, known $M$ | decision ($\mathrm{OR}_N$) |
|---|---|---|---|
| classical deterministic | exact | $N - M$ | $N$ |
| classical randomized | bounded | $\Theta(N/M)$ | $\Theta(N)$ |
| quantum | exact | $\Theta(\sqrt{N/M})$ | $N$ |
| quantum | zero error | $\Theta(\sqrt{N/M})$ | $N$ |
| quantum | bounded | $\Theta(\sqrt{N/M})$ | $\Theta(\sqrt{N})$ |

- The classical deterministic bounds come from an adversary that answers "no" as long as it can. See the [search lower bound](/search-lower-bound/).
- The classical randomized bound $\Omega(N)$ for $M = 1$ follows from [Yao's minimax principle](/yao-minimax-principle/) with a uniformly random marked item.
- The quantum bounded-error lower bound $\Omega(\sqrt{N})$ is the theorem of Bennett, Bernstein, Brassard and Vazirani, on the page [optimality of Grover's search](/grover-optimality/). It also follows from the [polynomial method](/polynomial-method/), since $\mathrm{OR}_N$ has [approximate degree](/approximate-degree/) $\Theta(\sqrt{N})$, and from the [quantum adversary method](/quantum-adversary-method/). Boyer, Brassard, Høyer and Tapp extend it to $\Omega(\sqrt{N/M})$ for $M$ marked items.
- The exact and zero-error bound $N$ for $\mathrm{OR}_N$ is from Beals, Buhrman, Cleve, Mosca and de Wolf. The exact decision has no speedup, because the exact degree of $\mathrm{OR}_N$ as a polynomial is $N$.

So the [quantum query complexity](/quantum-query-complexity/) of unstructured search with bounded error is $\Theta(\sqrt{N/M})$, a square root of the classical $\Theta(N/M)$. These are query bounds. They are not bounds on time, and they do not compare a quantum query count with a classical running time.

## Reductions

- **Search to decision.** A search algorithm that checks its output with one more query decides $\mathrm{OR}_N$. So each lower bound for $\mathrm{OR}_N$ is a lower bound for search, up to one query.
- **Decision to search.** A decision algorithm finds a marked item by binary splitting of the index set. This costs a factor $O(\log N)$ in general. For quantum algorithms, a direct search avoids the factor.
- **Unknown $M$ to known $M$.** Try a random number of iterations from a range that grows by a constant factor. This is the idea of [BBHT search](/bbht-search/), with a constant factor in queries.
- **Other problems to search.** [Minimum finding](/minimum-finding/), [collision finding](/collision-finding/) and [element distinctness](/element-distinctness/) have quantum algorithms that call search as a subroutine. A problem in [NP](/np/) reduces to search over all certificates. This gives about $2^{n/2}$ queries for certificates of $n$ bits, so it does not put NP in [BQP](/bqp/).

## Applications

- Brute-force search of a large space, when no better structure is known: key search and the [security levels](/nist-security-levels/) of post-quantum cryptography, and the search over all assignments of a formula.
- A subroutine of other quantum algorithms: [quantum counting](/quantum-counting/), [Dürr-Høyer minimum finding](/durr-hoyer-minimum-finding/), [Brassard-Høyer-Tapp collision finding](/brassard-hoyer-tapp-collision/) and [triangle finding](/triangle-finding/).
- The standard example of a lower bound in [quantum query complexity](/quantum-query-complexity/): the [hybrid argument](/hybrid-argument/), the [polynomial method](/polynomial-method/) and the [adversary method](/quantum-adversary-method/) all prove $\Omega(\sqrt{N})$ for it first.

## References
