---
tag: WTPWQP
kind: problem
slug: k-ary-gray-code-generation
name: k-ary Gray code generation
aliases:
- radix-k Gray code generation
- mixed-radix Gray code generation
- n-ary Gray code generation
area: combinatorics/gray-codes
level: advanced
summary: Output all base-k strings so that consecutive strings differ by a unit change in one digit.
prereqs: [gray-code-generation, radix]
see_also: [k-ary-gray-code, gray-code-generation, cyclic-gray-code, loopless-gray-code-generation, factorial-number-system, hamiltonian-path, bipartite-graph, minimal-change-ordering]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (Gray codes for mixed-radix n-tuples, reflected and modular, and Algorithm H)
  - paper: doi:10.37236/11023
    title: Torsten Mütze, Combinatorial Gray codes, an updated survey, Electronic Journal of Combinatorics, Dynamic Survey DS26, 2023
    locator: Section 3.19 (larger alphabets, loopless b-ary Gray codes by Herter and Rote, balanced b-ary Gray codes by Flahive)
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 605 to 629, 1997
    locator: Section 2 (the reflected Gray code and its generalizations)
---

$k$-ary Gray code generation asks for a list of all $N = k^n$ strings of length $n$ over the digits $0, \ldots, k-1$ in which consecutive strings differ in a single digit, and in the strict form, by exactly $\pm 1$ in that digit. The reflected [k-ary Gray code](/k-ary-gray-code/) solves the strict form for every $k \ge 2$ and $n \ge 0$, and Knuth's Algorithm H outputs it in $O(1)$ worst-case time per string. Under the $\pm 1$ rule a cyclic solution exists for even $k$ and $n \ge 2$ but never for odd $k \ge 3$ and $n \ge 1$; with steps modulo $k$, the modular Gray code is cyclic for every $k$. For $k = 2$ the problem is [Gray code generation](/gray-code-generation/).

## In plain words

You have $n$ dials, and each dial shows a number from 0 to $k - 1$. You want to see every setting of all the dials exactly once. At each step you may turn one dial by one click, up or down. Gray code generation for $k$ digits asks for such a plan.

A plan always exists. Sweep the first dial up to its top, click the second dial, sweep the first dial back down, click the second dial again, and so on, like an odometer that never jumps. Whether you can also end one click away from the start depends on $k$. If dials may also click from the top value straight back to 0, a closed tour always exists.

## Definition

Let $n \ge 0$ be the number of digits, $k \ge 2$ the radix, and $N = k^n$.

- **Input:** $n$ and $k$, or more generally radices $m_0, \ldots, m_{n-1}$, each at least 2, with $N = m_0 \cdots m_{n-1}$.
- **Output:** a list $v_0, \ldots, v_{N-1}$ that contains each digit string $a_{n-1} \ldots a_0$ with $0 \le a_j < m_j$ exactly once, such that $v_{i-1}$ and $v_i$ differ in one digit for $1 \le i < N$, and in that digit by exactly 1.

Three closeness rules are in use, from weakest to strongest:

| rule | a step may change one digit | closeness graph |
|---|---|---|
| Hamming | to any other value | the Hamming graph $K_k^n$ |
| modular | by $\pm 1$ modulo $k$ | the torus $C_k^n$ |
| unit | by $\pm 1$, with no wrap | the grid $P_k^n$ |

A list for the unit rule is also a list for the other two. The output model is the same as in the binary case: one array, one digit changed in place per step, then a visit.

## Variants

- **Cyclic.** Also require that $v_{N-1}$ and $v_0$ are neighbors. Under the unit rule, the grid $P_k^n$ is bipartite by the parity of the digit sum, so for odd $k \ge 3$ and $n \ge 1$, with $N$ odd, no cyclic list exists. For even $k$ and $n \ge 2$, the grid has a Hamiltonian cycle: the reflected code is a Hamiltonian path of $P_k^{n-1}$ with $M = k^{n-1} \ge 2$ vertices, so $P_k^n$ contains the $M \times k$ rectangle grid as a spanning subgraph, and a rectangle grid with an even side of length at least 2 and the other side at least 2 has a Hamiltonian cycle. Under the modular rule, the modular Gray code is cyclic for every $k$. See [cyclic Gray code](/cyclic-gray-code/).
- **Mixed radix.** Digit $j$ has its own radix $m_j$. Both the reflected code and Algorithm H work unchanged. The case $m_j = j + 2$ covers the strings of the [factorial number system](/factorial-number-system/).
- **Balanced.** Each digit position changes about $N / n$ times. Flahive gave such codes with transition counts within 2 of the average (Mütze, Section 3.19).
- **Ranking.** Find the position of a string in a fixed solution, or the string at a given position. For the reflected and the modular codes this takes $O(n)$ arithmetic operations.

## Examples

For $n = 2$, $k = 3$, with strings written $a_1 a_0$:

- **Reflected (unit rule).** 00, 01, 02, 12, 11, 10, 20, 21, 22. Not cyclic: 22 and 00 differ in both digits.
- **Modular.** 00, 01, 02, 12, 10, 11, 21, 22, 20. Each step adds 1 modulo 3 to one digit, and the step from 20 back to 00 does too, so the list is cyclic under the modular rule. The steps 12 to 10 and 22 to 20 break the unit rule.
- **Even radix.** For $n = 2$, $k = 4$ the reflected list ends at 30, which differs from 00 by 3 in one digit. It is cyclic under the Hamming and the modular rules but not under the unit rule. A cyclic list under the unit rule exists for this grid, for example 00, 01, 02, 03, 13, 12, 11, 21, 22, 23, 33, 32, 31, 30, 20, 10.
- **Not a solution.** Counting order 00, 01, 02, 10, ... steps from 02 to 10, which changes both digits.

## Known algorithms

| algorithm | time per string | total time | extra space | notes |
|---|---|---|---|---|
| unrank $r = 0, 1, \ldots$ with the digit formula of the [k-ary Gray code](/k-ary-gray-code/) | $O(n)$ | $\Theta(nN)$ | $O(n)$ | random access |
| odometer with one direction per digit, scan for the lowest digit that can move | $O(1)$ amortized, $O(n)$ worst | $\Theta(N)$ | $O(n)$ | CAT |
| Algorithm H: focus pointers and directions (Knuth) | $O(1)$ worst case | $\Theta(N)$ | $O(n)$ | loopless, reflected code |
| modular code from a counter, digit $j$ is $(b_j - b_{j+1}) \bmod k$ | $O(1)$ amortized | $\Theta(N)$ | $O(n)$ | cyclic for all $k$ |

All bounds are on the word RAM with the array visited in place. Herter and Rote (2018) gave further loopless generators, based on generalizations of the Tower of Hanoi puzzle (Mütze, Section 3.19). The odometer is CAT because digit $j$ is reached by the scan only once in every $m_0 \cdots m_{j-1}$ steps, so the scans cost $O(N)$ in total, as in a [binary counter increment](/binary-counter-increment/).

## Bounds

- **Lower bound.** Any solution visits $N$ strings, so it takes $\Omega(N)$ time; with a copy of each string, $\Omega(nN)$.
- **Upper bound.** Algorithm H meets $O(1)$ worst-case time per string with $\Theta(n)$ extra space, so $\Theta(N)$ is tight.
- **Number of digit changes.** Every solution makes exactly $N - 1$ changes, one per step. In the reflected code digit $j$ changes $(m_j - 1) N / (m_0 \cdots m_j)$ times, so the lowest digit takes most of them.

## Reductions

- **To Hamiltonian paths.** A solution is a [Hamiltonian path](/hamiltonian-path/) of the closeness graph. The reflected construction is the general fact that if $G$ has a Hamiltonian path, then so does the product of $G$ with a path: walk $G$ forward, step once along the path, walk $G$ backward, and repeat.
- **From the binary case.** For $k = 2$ the three rules agree and the problem is [Gray code generation](/gray-code-generation/). Algorithm H with all radices 2 is the binary focus pointer method of [loopless Gray code generation](/loopless-gray-code-generation/).
- **Parity obstruction.** The cyclic question under the unit rule reduces to a [bipartite graph](/bipartite-graph/) count: a closed walk in a bipartite graph has even length, so $N$ must be even.
- **To other families.** A minimal change list of mixed-radix strings maps to a list of other objects whenever a bijection turns one unit change into one small change of the object. This is one route to [minimal change orderings](/minimal-change-ordering/) of permutations.

## Applications

- **Grid search with cheap updates.** When a cost is evaluated over all points of a grid of discrete parameters and a step to a neighbor point is cheap to update, the reflected order makes every step such a neighbor step.
- **Position codes with $k$ levels.** If a scale marks its positions with the strings of a $k$-ary Gray code, neighbor positions differ by one level in one track. A reading taken between two positions then gives one of the two, not a distant position.
- **Puzzles.** Herter and Rote derived loopless $k$-ary Gray code generators from generalizations of the Tower of Hanoi puzzle (Mütze, Section 3.19), as the binary reflected code follows the classic puzzle.

## References
