---
tag: GC27AH
kind: problem
slug: combination-gray-code-generation
name: Combination Gray code generation
aliases:
- fixed-size subset Gray code
- combinations with minimal change
- k-subset Gray code
- Gray code for combinations
area: combinatorics/gray-codes
level: advanced
summary: Output all k-element subsets so that consecutive subsets differ by one swap.
prereqs: [k-subset-enumeration, fixed-weight-binary-strings, gray-code-generation]
see_also: [revolving-door-ordering, eades-mckay-algorithm, chase-sequence, ehrlich-loopless-combinations, cool-lex-order, minimal-change-ordering, hamiltonian-path, combinatorial-ranking-and-unranking]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3 (the revolving door Gray code and Algorithm R, homogeneous and near-perfect schemes, Algorithm C, and the comparison of orders in Fig. 26)
  - paper: doi:10.37236/11023
    title: Torsten Mütze, Combinatorial Gray codes, an updated survey, Electronic Journal of Combinatorics, Dynamic Survey DS26, 2023
    locator: Section 4.1 (combinations under transpositions, homogeneous, near-perfect and adjacent transpositions, and the Johnson graph)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Chapter 5, Section 5.3 (Gray codes for combinations under the closeness conditions Trans, H-Trans, 2-Trans and A-Trans)
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 605 to 629, 1997
    locator: the section on combinations (revolving door, homogeneous and adjacent transposition Gray codes)
---

Combination Gray code generation asks for a list of all $N = C(n, k)$ subsets of size $k$ of an $n$-element set in which each two neighbors differ by one swap: one element leaves and one element enters. A swap is the smallest possible change, because two different subsets of the same size differ in at least one element each way. The [revolving door ordering](/revolving-door-ordering/) solves the problem for all $n$ and $k$, and loopless generators output a solution in $O(1)$ worst-case time per subset, which is optimal. Stronger forms limit how far the moving element may travel; the strongest form, with moves to a neighbor value only, has a solution exactly when $k \le 1$, $n - k \le 1$, or both $k$ and $n - k$ are odd.

## In plain words

You have $n$ players and must try every team of $k$ of them. Between two tries you may send one player off the team and bring one other player in. A list of all teams with this property is a Gray code for combinations.

Such a list always exists. Extra rules make the task harder. You may ask that the player who comes in stands next to the one who leaves, as on a bench, or that the new player stands at most two seats away, or that no team member sits between them. Some of these rules can always be met, and one of them only for some team sizes.

## Definition

Let $n \ge 0$ and $0 \le k \le n$. A $k$-subset $S$ of $\{0, \ldots, n-1\}$ is stored as a bit string $a_{n-1} \ldots a_0$ with $a_j = 1$ when $j \in S$, which has exactly $k$ ones.

- **Input:** $n$ and $k$.
- **Output:** a list $S_0, \ldots, S_{N-1}$ that contains each $k$-subset exactly once, such that $|S_{i-1} \setminus S_i| = 1$ for $1 \le i < N$.

In bit string form each step exchanges a 1 and a 0. The rules below limit which exchanges are allowed, from the weakest to the strongest. Write $s = n - k$ for the number of zeros.

| rule | allowed step | always possible |
|---|---|---|
| transposition | any $1$ and $0$ exchange | yes |
| homogeneous | $10^p \leftrightarrow 0^p1$, only zeros between them | yes |
| near-perfect | $01 \leftrightarrow 10$ or $001 \leftrightarrow 100$ | yes |
| adjacent | $01 \leftrightarrow 10$ only | only if $k \le 1$, $s \le 1$, or $k$ and $s$ both odd |

In the index form $c_k > \cdots > c_1$, a homogeneous step changes exactly one index, and a near-perfect step changes one index by 1 or 2. The output model is one array changed in place, with a visit after each step.

## Variants

- **Cyclic.** Also require that $S_{N-1}$ and $S_0$ differ by one swap. The revolving door list is cyclic for $0 < k < n$. Under the adjacent rule the ends of any solution must be $1^k0^s$ and $0^s1^k$, since each of these strings allows only one adjacent exchange, so no cyclic solution exists for $0 < k < n$ and $N \ge 3$. Allowing the exchange of $a_{n-1}$ and $a_0$ as a neighbor pair gives the circular adjacent rule. Enns showed that a list under this rule exists if and only if at least one of $k$ and $n - k$ is odd (Mütze, Section 4.1).
- **Genlex.** Require that subsets with the same largest elements appear together. The revolving door order, the Eades-McKay order and Chase's sequence are all genlex.
- **Prefix shifts.** [Cool-lex order](/cool-lex-order/) changes each bit string by rotating a prefix one place, which is one or two transpositions per step, and it is cyclic.
- **Loopless.** Require $O(1)$ worst-case time between two visits, not only on average. See [loopless generation](/loopless-generation/).
- **Ranking.** Find the position of a subset in a fixed solution, or the subset at a given position. See [combinatorial ranking and unranking](/combinatorial-ranking-and-unranking/).

## Examples

For $n = 4$ and $k = 2$, with subsets of $\{1, 2, 3, 4\}$:

- **Revolving door.** 12, 23, 13, 34, 24, 14. Each step swaps one element, and the last subset 14 is one swap from 12, so the list is cyclic. The swap from 13 to 34 moves element 1 past element 3, so the list is not homogeneous.
- **Homogeneous.** In bit strings $a_4a_3a_2a_1$ (element $j$ at bit $a_j$), the Eades-McKay list $K_{22}$ is 0011, 0101, 0110, 1010, 1001, 1100, that is 12, 13, 23, 24, 14, 34. Every element moves over free values only.
- **Not a solution.** Lexicographic order 12, 13, 14, 23, 24, 34 steps from 14 to 23, which changes both elements.
- **No adjacent solution.** Under the adjacent rule each step changes the sum of the elements by exactly 1, so the sums alternate between odd and even. The six subsets have sums 3, 4, 5, 5, 6, 7 for 12, 13, 14, 23, 24, 34: four odd and two even. A list that alternates can hold at most one more odd sum than even sums, so no list exists. This is the case $k = s = 2$ of the theorem of Buck and Wiedemann and of Eades, Hickey and Read.

## Known algorithms

| algorithm | rule | time per subset | extra space | notes |
|---|---|---|---|---|
| [revolving door ordering](/revolving-door-ordering/), recursive | transposition | $O(1)$ amortized, $O(n)$ worst | $O(n)$ | cyclic, simple rank formula |
| [Ehrlich's loopless combination generation](/ehrlich-loopless-combinations/), and Knuth's Algorithm R | transposition | $O(1)$ worst case | $O(n)$ | loopless revolving door |
| [Eades-McKay algorithm](/eades-mckay-algorithm/) | homogeneous | $O(1)$ amortized | $O(n)$ | genlex |
| [Chase's sequence](/chase-sequence/), Knuth's Algorithm C | near-perfect | $O(1)$ amortized | $O(n)$ | genlex |
| [cool-lex order](/cool-lex-order/) | one or two transpositions | $O(1)$ worst case | $O(n)$ | cyclic, loopless |

All bounds are on the word RAM with the array visited in place. For the adjacent rule, Eades, Hickey and Read gave a list whenever one exists, and Hough and Ruskey (1988) gave an efficient algorithm for it (Mütze, Section 4.1).

## Bounds

- **Lower bound on time.** Any solution visits $N$ subsets, so it takes $\Omega(N)$ time, and $\Omega(kN)$ if each subset is copied out.
- **Upper bound on time.** Loopless revolving door generators and cool-lex order meet $O(1)$ worst-case time per subset, so $\Theta(N)$ total time is tight.
- **Size of a step.** Two different $k$-subsets differ in at least two bits, so a transposition is the least possible change. Under the transposition rule, every solution changes exactly $2(N - 1)$ bits in total.
- **Length of a move.** Under the homogeneous rule a move may still cover many positions; the Eades-McKay list has a move over $s - 1$ zeros. The near-perfect rule caps every move at two positions, and the adjacent rule at one.

## Reductions

- **To Hamiltonian paths.** A solution under the transposition rule is a [Hamiltonian path](/hamiltonian-path/) of the Johnson graph $J(n, k)$, whose vertices are the $k$-subsets and whose edges join subsets that differ by one swap. Jiang and Ruskey and, independently, Knor showed that $J(n, k)$ has a Hamiltonian path between any two vertices (Mütze, Section 4.1).
- **From Gray codes for all subsets.** The strings with $k$ ones in the [binary reflected Gray code](/binary-reflected-gray-code/), in that order, form a solution. This is the revolving door order (Tang and Liu, 1973).
- **Complement and reversal.** Replacing each subset by its complement maps a solution for $(n, k)$ to a solution for $(n, n - k)$ under the transposition and the adjacent rules, since an exchange of a 1 and a 0 stays an exchange at the same positions. It does not keep the homogeneous and near-perfect rules, because the zeros between the exchanged bits become ones. Reversing the bit order, $j \mapsto n - 1 - j$, keeps all four rules.
- **Parity obstruction.** The adjacent rule is a Hamiltonian path question in a [bipartite graph](/bipartite-graph/), split by the parity of the sum of the elements, and a path needs the two sides to differ in size by at most 1. This is the argument in the example above.

## Applications

- **Exhaustive search with cheap updates.** When a value is computed for every $k$-subset and adding or removing one element updates it in $O(1)$ time, such as a sum of weights or a count of edges inside the subset, a Gray code makes each step cost two updates instead of $k$. This speeds up exact permutation tests that compare the sum of one group of $k$ values with the rest.
- **Keyboards and moving parts.** A homogeneous list plays all $k$-note chords on an $n$-key keyboard while moving one finger at a time, without crossing fingers (Knuth, Section 7.2.1.3). A near-perfect list also keeps each finger move short.
- **Other objects.** A combination Gray code maps to Gray codes for compositions and for combinations with repetition, where a homogeneous step changes only two neighbor parts (Knuth, Section 7.2.1.3). See [combinations with repetition](/combinations-with-repetition/).

## References
