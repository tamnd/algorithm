---
tag: DD8NX7
kind: definition
slug: minimal-change-ordering
name: Minimal change ordering
aliases:
- Gray-type ordering of permutations
- Minimal-change ordering
- adjacent-difference ordering
- adjacent-transposition ordering
- minimal change property
- combinatorial Gray code
area: combinatorics/gray-codes
level: intro
summary: An ordering of combinatorial objects in which consecutive objects differ by a single small change.
prereqs: [gray-code, combinatorial-generation]
see_also: [steinhaus-johnson-trotter, heaps-algorithm, revolving-door-ordering, chase-sequence, eades-mckay-algorithm, minimal-change-permutation-order, set-partition-generation, cool-lex-order]
sources:
  - paper: doi:10.37236/11023
    title: Torsten Mütze, Combinatorial Gray codes, an updated survey, Electronic Journal of Combinatorics, Dynamic Survey DS26, 2023
    locator: Section 2.1 (flip graphs), Section 2.2 (necessary conditions), Section 4.1 (transposition Gray codes for combinations), Section 5.1 (permutations by transpositions) and Section 6.1 (set partitions)
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 605 to 629, 1997
    locator: Section 1 (the general notion of a combinatorial Gray code)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (Gray codes for n-tuples), Section 7.2.1.2 (plain changes and Heap's method for permutations) and Section 7.2.1.3 (revolving door and homogeneous orders for combinations)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, 2nd edition, Academic Press, 1978
    locator: the chapters on subsets, k-subsets and permutations, which list these objects in minimal change order
---

A minimal change ordering of a family of combinatorial objects is a listing of all of them in which each object differs from the one before by a single elementary change, the smallest change that two different objects can show. Bit strings with one bit flipped, $k$-subsets with one element swapped for another, and permutations with one transposition are the standard cases. The term is the general form of a [Gray code](/gray-code/), and many authors call such a list a combinatorial Gray code. Such an ordering is a Hamiltonian path in the graph whose edges are the allowed changes, so it lets a program update a result in $O(1)$ work per object instead of building each object again.

## Definition

Let $S$ be a finite set of $N \ge 1$ combinatorial objects and let $\mathcal{C}$ be a set of *elementary changes*: operations that turn an object of $S$ into another object of $S$. Two objects are *neighbors* when one change turns one into the other. The *flip graph* $G(S, \mathcal{C})$ has vertex set $S$ and an edge between each pair of neighbors.

A *minimal change ordering* of $S$ under $\mathcal{C}$ is a list $x_1, x_2, \ldots, x_N$ that contains each object of $S$ exactly once, such that $x_{i+1}$ is a neighbor of $x_i$ for $1 \le i < N$. Equivalently, it is a Hamiltonian path of the flip graph. It is *cyclic* when $x_N$ and $x_1$ are also neighbors.

The word *minimal* refers to a lower bound on the difference of two distinct objects in the chosen representation. The list must reach that bound at every step:

| objects | representation | least difference of two distinct objects | elementary change |
|---|---|---|---|
| subsets of $[n]$, $N = 2^n$ | bit string $a_{n-1} \ldots a_0$ | 1 bit | flip one bit |
| $k$-subsets of $[n]$, $N = C(n, k)$ | bit string with $k$ ones | 2 bits, one 1 and one 0 | swap a 0 and a 1 |
| permutations of $[n]$, $N = n!$ | one-line form $p_1 \ldots p_n$ | 2 positions | swap two entries |
| $n$-tuples with digit $j$ in $\{0, \ldots, m_j - 1\}$ | digit string | 1 digit | change one digit, often by $\pm 1$ |

Here $[n] = \{1, \ldots, n\}$ and $k$ is the subset size. A minimal change ordering with a stronger restriction on the change is often named after it: *adjacent transposition* (swap two neighbor positions), *homogeneous* (swap a 1 with a 0 when only 0s lie between them), or *adjacent difference* (a digit changes by $\pm 1$).

**Necessary conditions.** The flip graph must be connected. If it has a vertex of degree 1, no cyclic ordering exists, and if it has more than two such vertices, no ordering exists. If it is bipartite with sides of sizes $A$ and $B$, an ordering needs $|A - B| \le 1$ and a cyclic ordering needs $A = B$. Mütze (Section 2.2) notes that for most flip graphs of interest these simple conditions are also sufficient, but there is no general theorem.

## Examples and non-examples

- **Bit strings.** The [binary reflected Gray code](/binary-reflected-gray-code/) for $n = 3$: 000, 001, 011, 010, 110, 111, 101, 100.
- **Permutations by adjacent transpositions.** The [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) order, also called plain changes, for $n = 3$: 123, 132, 312, 321, 231, 213. Each step swaps two neighbor entries, and the list is cyclic: 213 and 123 differ by a swap of the first two entries. See [minimal change permutation order](/minimal-change-permutation-order/).
- **Permutations by any transposition.** [Heap's algorithm](/heaps-algorithm/) for $n = 3$: 123, 213, 312, 132, 231, 321. Each step swaps two entries, but 213 to 312 swaps positions 1 and 3, which are not neighbors, so this is a minimal change ordering under transpositions and not under adjacent transpositions.
- **$k$-subsets, revolving door.** The [revolving door order](/revolving-door-ordering/) for $n = 4$, $k = 2$: $\{1,2\}, \{2,3\}, \{1,3\}, \{3,4\}, \{2,4\}, \{1,4\}$. At each step one element leaves and one enters.
- **$k$-subsets, homogeneous and near-perfect.** In the [Eades-McKay order](/eades-mckay-algorithm/) the moving 1 jumps over 0s only. In [Chase's sequence](/chase-sequence/) it moves by one or two places, 01 to 10 or 001 to 100.
- **$k$-subsets, adjacent transpositions only.** A list of all $k$-subsets of $[n]$ in which each step swaps two neighbor bits exists if and only if $k \in \{0, 1\}$, or $n - k \in \{0, 1\}$, or $k$ and $n - k$ are both odd (Buck and Wiedemann, and Eades, Hickey and Read, both 1984; Mütze, Section 4.1). For $n = 4$, $k = 2$ none exists. The strings 1100 and 0011 each have only one neighbor, so a list must start at one and end at the other. Color each string by the parity of the sum of the positions of its ones; an adjacent swap changes this sum by 1, so the flip graph is bipartite. Its two sides have sizes 4 and 2, which breaks the condition $|A - B| \le 1$.
- **Set partitions.** Kaye (1976) lists all set partitions of $[n]$ so that at each step one element moves to another block (Mütze, Section 6.1). See [set partition generation](/set-partition-generation/).
- **Non-example: lexicographic order.** For 3-bit strings, lexicographic order steps from 011 to 100, a change of three bits. For permutations it steps from 132 to 213, which changes all three entries. Lexicographic order is not a minimal change ordering.
- **Non-example: [cool-lex order](/cool-lex-order/).** Each step of cool-lex order rotates a prefix of the string by one place. This is one or two transpositions, so cool-lex is a minimal change ordering under prefix shifts but not under single transpositions.

## Related definitions

- **[Gray code](/gray-code/).** The original case, binary strings under one-bit flips. A [cyclic Gray code](/cyclic-gray-code/) is a cyclic minimal change ordering.
- **Flip graph.** The graph of the objects and the allowed changes. Examples: the $n$-cube for bit strings, the Johnson graph $J(n, k)$ for $k$-subsets under transpositions, and the Cayley graph of the symmetric group generated by the adjacent transpositions for permutations.
- **Genlex order.** An order in which all objects with a common prefix appear together. The revolving door, Eades-McKay and Chase orders are genlex, and so is the reflected Gray code.
- **Loopless and CAT generation.** A minimal change ordering lets a generator change $O(1)$ entries per step, so it can meet $O(1)$ time per object. See [loopless generation](/loopless-generation/) and [constant amortized time generation](/constant-amortized-time-generation/).

## References
