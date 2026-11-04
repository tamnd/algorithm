---
tag: 89CWA1
kind: technique
slug: bitmask-dp
name: Bitmask dynamic programming
aliases:
- dynamic programming over subsets
- subset DP
area: techniques/dynamic-programming
level: core
summary: Represent subsets as integer bitmasks and use them as DP states.
prereqs: [bit-manipulation, tabulation, optimal-substructure]
see_also: [held-karp-algorithm, submask-enumeration, sum-over-subsets-dp, sos-dp, broken-profile-dp, assignment-problem, exact-exponential-algorithms, traveling-salesman-problem]
sources:
  - paper: doi:10.1137/0110015
    title: Michael Held and Richard M. Karp, A dynamic programming approach to sequencing problems, Journal of the SIAM 10(1), 196-210, 1962
    locator: the recurrence over subsets for sequencing and for the traveling salesman problem
  - paper: doi:10.1145/321105.321111
    title: Richard Bellman, Dynamic programming treatment of the travelling salesman problem, Journal of the ACM 9(1), 61-63, 1962
    locator: the whole paper
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 3, Dynamic Programming
  - paper: doi:10.1137/070683933
    title: Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 546-563, 2009
    locator: the O(2^n poly(n)) algorithms for set partition and the chromatic number
  - book: isbn:9780073523408
    title: Dasgupta, Papadimitriou and Vazirani, Algorithms
    locator: Chapter 6, Section 6.6, The traveling salesman problem
---

Bitmask dynamic programming uses a subset of a small ground set $\{0, \ldots, n-1\}$ as a state, and stores the subset as an $n$-bit integer whose bit $i$ is 1 when element $i$ is in the subset. The table has $2^n$ entries, or $2^n$ times a small extra index, and each entry is computed from the entries of smaller subsets. The method turns many problems that have $n!$ candidate orders or $n^n$ candidate maps into problems that take $O(2^n \operatorname{poly}(n))$ or $O(3^n)$ time, which is practical for $n$ up to about 20 to 25. The [Held-Karp algorithm](/held-karp-algorithm/) for the [traveling salesman problem](/traveling-salesman-problem/) is the classic example.

## In plain words

Some problems ask for the best order of a few items, or the best way to give each item to someone. Trying all orders is far too slow, even for 20 items.

But often the past matters only through the set of items already used, not through their order. Then you can remember one best answer for each set. A set of $n$ items is stored as a number with $n$ binary digits, one digit per item, so the sets are just the numbers from 0 to $2^n - 1$. Each set is solved from sets with one item fewer, or from smaller pieces. For 20 items there are about a million sets, which a computer handles quickly.

## When it applies

- The ground set is small: $n \le 20$ for $O(n^2 2^n)$, $n \le 25$ or so for $O(n 2^n)$, $n \le 15$ or 16 for $O(3^n)$.
- A partial solution can be summarized by the set of elements it has used, perhaps with one more small index such as the last element. The order inside the set does not matter for the rest of the solution.
- The value for a set follows from the values for its subsets by a fixed rule: add one element, or split the set into two parts.

Typical words: visit all, assign each, every subset, order of tasks, partition into groups, with $n \le 20$.

## The template

The holes are the meaning of $f(S)$, the base value and the transition. This is the form that adds one element at a time.

```pseudo id=main
BITMASK-DP(n)
L1  f[0] ← base                                          ▷ hole: the value of the empty set
L2  for S ← 1 to 2^n − 1 do f[S] ← +∞
L3  for S ← 0 to 2^n − 2 do                               ▷ increasing numbers: subsets come first
L4      if f[S] = +∞ then continue
L5      for each j ∉ S do                                 ▷ bit j of S is 0
L6          T ← S ∪ {j}                                   ▷ T = S OR 2^j
L7          f[T] ← min(f[T], f[S] + gain(S, j))           ▷ hole: the cost of adding j to S
L8  return f[2^n − 1]
```

**Why the order of line L3 is right.** If $S \subsetneq T$ then the number $S$ is less than the number $T$, because $T$ has all the 1 bits of $S$ and at least one more. So when line L3 reaches $S$, every update into $f[S]$ came from a smaller number and is already done, and $f[S]$ is final.

**Why line L7 gives the optimum.** By induction on $|T|$: an optimal solution for $T$ adds some last element $j$ to an optimal solution for $T \setminus \{j\}$ (this is the [optimal substructure](/optimal-substructure/) that the problem must have), and line L7 tries every such $j$.

**Cost.** Lines L5 to L7 run at most $n 2^n$ times, so the time is $O(n 2^n)$ and the space is $O(2^n)$. With an extra index, such as the last element in Held-Karp, the state count is $n 2^n$ and the time is $O(n^2 2^n)$.

### The split form

Some problems build a set from two disjoint parts instead of one element: $f(S) = \min_{\emptyset \ne A \subseteq S} \bigl( f(S \setminus A) + g(A) \bigr)$. The program runs over each $S$ and each nonempty submask $A$ of $S$ with the [submask enumeration](/submask-enumeration/) loop `A ← (A − 1) AND S`. Each element is in $S \setminus A$, in $A$, or outside $S$, so the number of pairs $(S, A)$ with $A \subseteq S$ is $3^n$, and the time is $O(3^n)$.

## Classic examples

### Assignment by bitmask

Give each of $n$ workers a different job and minimize the total cost $C[i][j]$. Let $f(S)$ be the least cost to give the jobs in $S$ to the first $|S|$ workers. The gain of line L7 is $C[|S|][j]$: the next worker, number $|S|$, gets job $j$.

For

$$C = \begin{pmatrix} 9 & 2 & 7 \\ 6 & 4 & 3 \\ 5 & 8 & 1 \end{pmatrix},$$

with bit $j$ for job $j$, the table is:

| $S$ (bits $2 1 0$) | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|---|---|---|---|---|---|---|---|---|
| $\lvert S \rvert$ | 0 | 1 | 1 | 2 | 1 | 2 | 2 | 3 |
| $f(S)$ | 0 | 9 | 2 | 8 | 7 | 12 | 5 | 9 |

For example, $f(011) = \min(f(001) + C[1][1], f(010) + C[1][0]) = \min(9 + 4, 2 + 6) = 8$, and $f(111) = \min(f(011) + C[2][2], f(101) + C[2][1], f(110) + C[2][0]) = \min(9, 20, 10) = 9$. The optimum 9 gives job 1 to worker 0, job 0 to worker 1 and job 2 to worker 2. The method takes $O(n 2^n)$ time against $n!$ for all permutations. For large $n$ the [assignment problem](/assignment-problem/) has polynomial algorithms, but the bitmask form extends to costs that depend on the whole set already used, where those algorithms do not apply.

### Other classic uses

- **[Held-Karp](/held-karp-algorithm/).** $C(S, j)$ is the shortest path from city 0 through the cities of $S$ that ends at $j$. Time $O(n^2 2^n)$.
- **Hamiltonian path.** A Boolean table $h(S, j)$: is there a path through exactly $S$ that ends at $j$? Same form as Held-Karp, with OR in place of min.
- **Sequencing with set-dependent costs.** Held and Karp's original setting: the cost of a job depends on the set of jobs done before it.
- **Partition into groups.** The least number of [bins](/bin-packing/) of total weight at most a capacity, or the [chromatic number](/chromatic-number/) of a graph with $g(A) = 0$ when $A$ is an independent set. These use the split form in $O(3^n)$, or inclusion and exclusion in $O(2^n \operatorname{poly}(n))$ as shown by Björklund, Husfeldt and Koivisto.
- **Grids.** When the state is the profile of one row of a grid, the bitmask is a row, and the method is [broken profile DP](/broken-profile-dp/).

## Variations

- **Sums over all subsets.** To compute $\sum_{T \subseteq S} a(T)$ for every $S$ in $O(n 2^n)$ instead of $O(3^n)$, use [sum over subsets DP](/sum-over-subsets-dp/), whose algorithm is on the [SOS DP](/sos-dp/) page.
- **Meet in the middle.** For $n$ up to about 40, split the ground set into two halves and combine a table for each half.
- **Smaller state spaces.** When only sets of a fixed size $k$ are reachable, iterate over the $\binom{n}{k}$ masks with $k$ bits, for example with [Gosper's hack](/gospers-hack/).
- **Bitset speedups.** When the table is Boolean, $h(S, \cdot)$ fits in one machine word for $n \le 64$, and a transition for all $j$ is a few word operations.

## Pitfalls

- **The order of the states is not the order of the elements.** The state must hold all the information that the future needs. In TSP the set of visited cities is not enough; the last city is also needed.
- **Memory.** $2^{25}$ entries of 8 bytes take 256 MiB. With an extra index of size $n$ the table grows by a factor $n$. Use the smallest type that fits, and drop states that cannot occur.
- **Operator precedence.** In C-like languages, `mask & 1 << j == 0` parses as `mask & ((1 << j) == 0)`. Write `(mask >> j & 1) == 0`.
- **Unreachable states.** Skip states with $f(S) = +\infty$, as line L4 does; adding a cost to $+\infty$ can overflow in fixed-width integers.
- **Using $3^n$ where $n 2^n$ is possible.** A split form that only ever moves one element is the one-element form and costs $O(n 2^n)$.

## Exercises

1. Prove that $\sum_{S \subseteq \{0, \ldots, n-1\}} 2^{|S|} = 3^n$.
2. Write a bitmask DP that counts the Hamiltonian paths of a graph on $n$ vertices in $O(n^2 2^n)$ time.
3. Given $n \le 16$ items with weights and a capacity $W$, find the least number of bins of capacity $W$ that hold all items, in $O(3^n)$ time. Then find an $O(n 2^n)$ method that stores, for each set, the pair (number of full bins, weight of the open bin).
   <details><summary>Hint</summary>For the second method, add items one at a time; a new item goes into the open bin if it fits, and otherwise opens a new bin. Compare pairs in the lexicographic order.</details>
4. Explain why the loop of line L3 may also run over the masks in order of their number of 1 bits, and when this order is useful.

## References
