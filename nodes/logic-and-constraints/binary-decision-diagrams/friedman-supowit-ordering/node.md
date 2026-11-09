---
tag: T03ZRT
kind: algorithm
slug: friedman-supowit-ordering
name: Friedman-Supowit optimal ordering
aliases:
- Friedman-Supowit algorithm
- subset dynamic programming for OBDD ordering
area: logic-and-constraints/binary-decision-diagrams
level: research
summary: An exact method for the OBDD variable order. A dynamic program over the sets of bottom variables finds a smallest OBDD from the truth table in O(n^2 3^n) time (Friedman and Supowit 1990).
model: word-ram
complexity:
  vars: {n: the number of variables}
  time: {worst: O(n^2 3^n)}
  space: {extra: O(3^n)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1990
  people: [Steven J. Friedman, Kenneth J. Supowit]
  note: Friedman and Supowit replaced the search over all n! orders by a dynamic program over the 2^n sets of variables, with O(n^2 3^n) time.
prereqs: [variable-ordering, reduced-ordered-bdd, bitmask-dp, bdd-canonicity]
see_also: [variable-ordering, variable-ordering-np-hardness, bdd-sifting, window-permutation-reordering, held-karp-algorithm, bitmask-dp, best-first-branch-and-bound, sum-over-subsets-dp]
sources:
  - paper: doi:10.1109/12.53586
    title: Steven J. Friedman and Kenneth J. Supowit, Finding the optimal variable ordering for binary decision diagrams, IEEE Transactions on Computers 39(5), 1990, pages 710 to 713
    locator: the dynamic program over subsets of variables and the O(n^2 3^n) time bound
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 5, The variable-ordering problem (the exact algorithm of Friedman and Supowit)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (optimal orderings, and the count of subfunctions per level)
  - paper: doi:10.1109/12.537122
    title: Beate Bollig and Ingo Wegener, Improving the variable ordering of OBDDs is NP-complete, IEEE Transactions on Computers 45(9), 1996, pages 993 to 1002
    locator: main theorem (why an exact method takes exponential time unless P = NP)
---

The Friedman-Supowit algorithm finds a [variable order](/variable-ordering/) that gives the smallest [reduced ordered BDD](/reduced-ordered-bdd/) of a function, from its truth table. A search over all $n!$ orders is too slow even for small $n$. Friedman and Supowit (1990) observed that the number of nodes on a level depends only on the variable of that level and the set of variables below it, not on the order of those variables. So a [dynamic program over subsets](/bitmask-dp/) finds the optimum, in the same way as the [Held-Karp algorithm](/held-karp-algorithm/) for the traveling salesman problem. It runs in $O(n^2 3^n)$ time. The time is exponential, and by the [NP-completeness theorem](/variable-ordering-np-hardness/) no polynomial exact method is expected when the input is a BDD. The method is used for small $n$, and as a check on [heuristics](/bdd-sifting/).

## In plain words

A BDD asks yes or no questions in some order, and you want the order that gives the fewest nodes. Build the order from the bottom up. Suppose you have already chosen which questions go into the bottom part, but not their order. The key fact: the number of nodes for the next question placed directly above that part depends only on which questions are in the part, and not on their order. So for each set of bottom questions, you only need the best cost of that set. A bigger set is built from a smaller set plus one question on top. This tries each set once instead of each order once, which is far fewer. It is still slow for many variables, because there are very many sets.

## The problem

**Input:** the truth table of a function $f$ of the variables $x_1, \ldots, x_n$, with $2^n$ entries. The values can be 0 and 1, or any finite set of values, as for an [algebraic decision diagram](/algebraic-decision-diagram/).

**Output:** an order $\pi$ of the variables and the size $|G_\pi(f)|$, such that no order gives a smaller reduced OBDD. The size counts the inner nodes and the sinks.

## The algorithm

For a set $J$ of variables, think of $J$ as the set of variables on the bottom levels. Each assignment $b$ to the other variables gives the subfunction $f|_b$, a function of the variables in $J$. The table $T_J$ maps each $b$ to a name of $f|_b$, with equal names for equal subfunctions. The empty set has $T_\emptyset = $ the truth table, with one name per value.

**The level lemma.** Put the variable $x \notin J$ directly above $J$. The nodes of $x$ are the distinct subfunctions on $J \cup \{x\}$ that depend on $x$. Such a subfunction is fixed by its two halves $x = 0$ and $x = 1$, which are subfunctions on $J$. So the number of $x$-nodes is

$$\mathrm{cost}(J, x) = \#\{ (T_J[b], T_J[b + x]) : b \text{ assigns } x = 0, \ T_J[b] \ne T_J[b + x] \},$$

where $b + x$ is $b$ with $x = 1$. This number depends only on $J$ and $x$. The table of $J \cup \{x\}$ gives each distinct pair a new name, and a pair with two equal names keeps that name.

The smallest number of inner nodes on the levels of $K$, over all orders of $K$ on the bottom levels, is $\mathrm{best}(K)$, with $\mathrm{best}(\emptyset) = 0$ and

$$\mathrm{best}(K) = \min_{x \in K} \big( \mathrm{best}(K \setminus \{x\}) + \mathrm{cost}(K \setminus \{x\}, x) \big).$$

The program computes this layer by layer, with $|K| = 1, 2, \ldots, n$, and keeps only the tables of the current layer.

```pseudo id=main
FRIEDMAN-SUPOWIT(f, n)
L1  T[∅] ← the truth table of f, with one name for each value
L2  best[∅] ← 0
L3  for k ← 0 to n − 1 do
L4      for each set J of k variables do
L5          for each variable x not in J do
L6              c ← best[J] + cost(J, x), computed from T[J]
L7              if c < best[J ∪ {x}] then best[J ∪ {x}] ← c; choice[J ∪ {x}] ← x
L8              if x is the smallest variable of J ∪ {x} then T[J ∪ {x}] ← the table of J ∪ {x}, made from T[J]
L9      drop the tables and the values of layer k
L10 K ← all variables; while K ≠ ∅ do output choice[K] as the next level from the top; K ← K \ {choice[K]}
L11 return best[all variables] + the number of distinct values, and the order
```

Line L8 builds the table of $K$ only once, from one of its subsets. This is enough, because $T_K$ does not depend on the order inside $K$. The value `best[K]` for an unseen $K$ is $+\infty$.

## Example

Let $f = x_1 x_2 \vee x_3 x_4$. It has 2 values, so the BDD has 2 sinks. The table gives $\mathrm{best}(K)$ for each set and the variable that the program chose for the top of the block. These numbers come from the implementation.

| set $K$ | best | top of $K$ | set $K$ | best | top of $K$ |
|---|---|---|---|---|---|
| $\{x_1\}$ | 1 | $x_1$ | $\{x_2, x_4\}$ | 3 | $x_4$ |
| $\{x_2\}$ | 1 | $x_2$ | $\{x_3, x_4\}$ | 2 | $x_4$ |
| $\{x_3\}$ | 1 | $x_3$ | $\{x_1, x_2, x_3\}$ | 3 | $x_3$ |
| $\{x_4\}$ | 1 | $x_4$ | $\{x_1, x_2, x_4\}$ | 3 | $x_4$ |
| $\{x_1, x_2\}$ | 2 | $x_2$ | $\{x_1, x_3, x_4\}$ | 3 | $x_1$ |
| $\{x_1, x_3\}$ | 3 | $x_3$ | $\{x_2, x_3, x_4\}$ | 3 | $x_2$ |
| $\{x_2, x_3\}$ | 3 | $x_3$ | all four | 4 | $x_4$ |
| $\{x_1, x_4\}$ | 3 | $x_4$ | | | |

For example, $\mathrm{cost}(\{x_1\}, x_3) = 2$. With $x_2 = 0$ the subfunctions on $\{x_1, x_3\}$ are $0$ and $x_3$, and with $x_2 = 1$ they are $x_1$ and $x_1 \vee x_3$. Two of them depend on $x_3$. So $\mathrm{best}(\{x_1, x_3\}) = 1 + 2 = 3$: a pair of variables from different products costs one node more than a pair from the same product.

Line L10 reads the order from the top: $x_4$, then the top of $\{x_1, x_2, x_3\}$, which is $x_3$, then $x_2$, then $x_1$. The size is $4 + 2 = 6$. The worst order for this function, from the same program with max in place of min, has 8 nodes.

More results from the implementation, with the smallest and the largest size over all orders:

| function | $n$ | smallest | largest |
|---|---|---|---|
| $x_1 x_2 \vee x_3 x_4 \vee \cdots$ with $k$ products | $2k$ | $2k + 2$ | $2^{k+1}$ |
| middle bit of a product of two 4-bit numbers | 8 | 31 | 71 |
| middle bit of a product of two 5-bit numbers | 10 | 63 | 207 |
| [hidden weighted bit](/hidden-weighted-bit-lower-bound/) | 10 | 82 | 152 |

The values for the products of two variables were checked for $k = 1$ to 4.

## Correctness

The proof has three steps.

- **Size by levels.** In the reduced OBDD for an order $\pi$, the nodes on the level of $x$ are the distinct subfunctions $f|_b$, for the assignments $b$ to the variables above $x$, that depend on $x$. The sinks are the distinct values. This is the subfunction form of [canonicity](/bdd-canonicity/).
- **Level lemma.** The number of nodes on the level of $x$ depends only on $x$ and the set $J$ of variables below $x$, and it equals $\mathrm{cost}(J, x)$. The set of subfunctions does not depend on the order of the variables above $x$, and the names in $T_J$ do not depend on the order inside $J$.
- **Dynamic program.** So the size of an order is the number of values plus a sum of terms $\mathrm{cost}(J_k, x_k)$, one for each level, where $J_k$ is the set below level $k$. The recurrence for best takes the minimum over the top variable of each bottom block, so $\mathrm{best}(\text{all})$ is the minimum over all orders, and the choices give an order that reaches it.

The full proof is in [the proof file](proofs/correctness.md).

## Complexity

The layer $k$ has $\binom{n}{k}$ sets $J$, each table $T_J$ has $2^{n-k}$ entries, and each set is combined with at most $n - k$ variables. Line L6 reads the table once, so the work for layer $k$ is $O((n - k) \binom{n}{k} 2^{n-k})$ table operations, and line L8 adds the same amount. By the binomial theorem,

$$\sum_{k=0}^{n} \binom{n}{k} 2^{n-k} = 3^n,$$

so the program makes $O(n 3^n)$ operations on keys of $n$ bits. Friedman and Supowit state the time bound $O(n^2 3^n)$. The two counts agree if each operation on an $n$-bit assignment costs $O(n)$ time, and with hashing on a word RAM the count above is $O(n 3^n)$ expected time.

The memory holds the tables of two layers, at most $2 \max_k \binom{n}{k} 2^{n-k} \le 2 \cdot 3^n$ entries, plus one value and one choice per set, $O(2^n)$. The input itself has $2^n$ entries, so the time is $O(n^2 N^{\log_2 3})$ in the input size $N = 2^n$, which is polynomial in $N$.

The growth is steep: $3^{10}$ is about $59{,}000$, but $3^{20}$ is about $3.5 \cdot 10^9$. So the method is practical only for small $n$.

## Properties

- **Exact.** It returns a smallest OBDD over all $n!$ orders.
- **Polynomial in the truth table.** The time is polynomial in $N = 2^n$, the size of the input. This does not contradict [the NP-completeness theorem](/variable-ordering-np-hardness/), whose input is an OBDD, which can be exponentially smaller than the truth table.
- **Any number of values.** The same program works for functions with more than two values. For a list of functions and the size of the shared OBDD, index the tables $T_J$ by the output and the assignment; the level lemma holds with the same proof.
- **Max as well as min.** Replacing min by max gives the worst order.

## Variants and improvements

- **BDD input.** The tables $T_J$ can be replaced by shared BDDs of the subfunctions, so that the input can be a BDD. The time is still exponential in the worst case.
- **Branch and bound.** Later exact methods prune the search with lower bounds on the size of the rest of the order, in the style of [best-first branch and bound](/best-first-branch-and-bound/) and A*. Drechsler, Drechsler and Günther (1998) and Ebendt, Günther and Drechsler (2003 and 2005) took this approach, which handles larger $n$ on many functions.
- **Restricted windows.** The same level lemma justifies [window permutation](/window-permutation-reordering/) and [sifting](/bdd-sifting/): a swap of two adjacent levels changes only those two levels.

## When to use it

Use the exact method when $n$ is small, for example for a part of a larger circuit, to compute the true optimum as a reference for heuristics, or to study the order of a known function. For large functions use [sifting](/bdd-sifting/).

## Pitfalls

- **The table is exponential.** The input itself has $2^n$ entries. For $n = 30$ the method is impossible, even when the BDD is small.
- **Names must be canonical within a table.** Two entries of $T_J$ must get the same name if and only if their subfunctions are equal. New names must never equal old names.
- **Build each table once.** Line L8 builds $T_K$ from only one subset. Building it from every subset multiplies the work by $|K|$ and gives nothing new.
- **Sinks.** The sinks are counted once, by the number of distinct values in the table. A function that is constant has size 1.

## Implementations

## History

Bryant (1986) noted that the order can change the size of an OBDD by an exponential factor. Friedman and Supowit (1990) gave the first method better than the search of all $n!$ orders, the dynamic program over subsets with $O(n^2 3^n)$ time, based on the observation that the cost of a level depends only on the set of variables below it. Later exact methods added branch and bound and A* search. Bollig and Wegener (1996) showed that improving the order of a given OBDD is NP-complete, so an exact method with polynomial time in the size of an OBDD is not expected.

## References
