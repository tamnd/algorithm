---
tag: N0CYS5
kind: algorithm
slug: quine-mccluskey
name: Quine-McCluskey algorithm
aliases:
- method of prime implicants
- tabulation method
area: eda/logic-synthesis
level: intro
summary: Finds all prime implicants by merging minterms that differ in one bit, level by level, then chooses a minimum cover with a prime implicant table.
solves: [two-level-logic-minimization]
model: word-ram
complexity:
  vars: {n: the number of variables, p: the number of prime implicants, m: the number of on-set minterms}
  time: {worst: "O(n^2 3^n + p^m poly(p, m))", best: "O(n^2 2^n)"}
  space: {extra: O(n 3^n)}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 1956
  people: [Willard Van Orman Quine, Edward J. McCluskey]
  note: Quine defined prime implicants and the reduction to them in 1952 and 1955. McCluskey gave the tabular method for finding them, and the prime implicant table, in 1956.
prereqs: [prime-implicant, dont-care-condition, set-cover]
see_also: [petricks-method, karnaugh-map, espresso, two-level-logic-minimization, depth-first-branch-and-bound, greedy-set-cover, implicant, sum-of-products]
sources:
  - paper: doi:10.1080/00029890.1952.11988183
    title: W. V. Quine, The problem of simplifying truth functions, American Mathematical Monthly 59(8), 521 to 531, 1952
    locator: prime implicants and the theorem that a shortest normal formula is a sum of prime implicants
  - paper: doi:10.1080/00029890.1955.11988710
    title: W. V. Quine, A way to simplify truth functions, American Mathematical Monthly 62(9), 627 to 631, 1955
    locator: the consensus method for listing the prime implicants
  - paper: doi:10.1002/j.1538-7305.1956.tb03835.x
    title: E. J. McCluskey, Minimization of Boolean functions, Bell System Technical Journal 35(6), 1417 to 1444, 1956
    locator: the tabular method for the prime implicants, grouped by the number of ones, and the prime implicant table
  - book: isbn:9780792397465
    title: Gary D. Hachtel and Fabio Somenzi, Logic Synthesis and Verification Algorithms, Kluwer, 1996
    locator: Chapter 4, Synthesis of Two-Level Circuits (Quine's theorem, the Quine-McCluskey procedure and the covering table)
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 7, Two-Level Combinational Logic Optimization (exact minimization, the covering matrix and its reductions)
  - paper: doi:10.1016/0167-9260(94)00007-7
    title: Olivier Coudert, Two-level logic minimization, an overview, Integration, the VLSI Journal 17(2), 97 to 140, 1994
    locator: the cyclic core and the reductions of the covering matrix by essentiality and dominance
---

The Quine-McCluskey algorithm finds a minimum [sum of products](/sum-of-products/) of a Boolean function given by its minterms and its [don't-cares](/dont-care-condition/). It solves [two-level logic minimization](/two-level-logic-minimization/) exactly, in two phases. Phase 1 lists all [prime implicants](/prime-implicant/): it merges pairs of cubes that differ in one variable, level by level, and the cubes that never merge are the primes. Phase 2 builds the prime implicant table, with one row for each minterm of the on-set and one column for each prime, and chooses a cheapest set of columns that covers every row. This is a [set cover](/set-cover/) problem. Phase 1 takes time $O(n^2 3^n)$ in the worst case. Phase 2 is exponential in the worst case, since the table problem is NP-hard. The method is the textbook exact algorithm and the reference that heuristics such as [Espresso](/espresso/) are tested against.

## In plain words

Write each input where the function is 1, or where you do not care, as a string of bits. Look for two strings that differ in one place only, such as 1000 and 1001. Together they make the shorter rule 100-, where the dash means "either". Do this for every pair, then do it again with the new strings, and so on. A string that never joins a partner is a prime: it cannot grow any larger.

Then make a table. Each row is an input where the function must be 1, and each column is a prime. Some rows have one prime only, so you must take it. After that, take the cheapest set of the other primes that covers the rows that are left. When the choice is not forced, try the options and keep the best.

## The problem

The input is $n$, the on-set $F \subseteq \{0, \ldots, 2^n - 1\}$ and the don't-care set $D$, both as lists of minterm numbers. The output is a set $C$ of cubes with $F \subseteq \bigcup C \subseteq F \cup D$ of least cost (number of cubes, number of literals), compared in this order. A cube is a string over $\{0, 1, -\}$, and the minterm numbers use $x_1$ as the high bit.

## The algorithm

```pseudo id=main
PRIMES(n, F, D)                     ▷ phase 1
L1  level ← { the minterm cube of m : m ∈ F ∪ D }
L2  while level ≠ ∅ do
L3      next ← ∅, merged ← ∅
L4      for each cube c ∈ level and each position i with c[i] = 0 do
L5          d ← c with c[i] set to 1
L6          if d ∈ level then add c with c[i] set to - to next
L7              add c and d to merged
L8      add every cube of level - merged to primes
L9      level ← next
    return primes

COVER(F, primes)                    ▷ phase 2, weight(p) = (1, literals of p)
L10 SOLVE(F, primes, ∅, (0, 0)); return the best set found
SOLVE(left, cols, chosen, spent)
    repeat
L11     if left = ∅ then record chosen if spent < best; return
L12     if spent ≥ best then return
L13     for each row m ∈ left with exactly one prime p in cols: move p to chosen, remove its rows
L14     drop a column j if some other column k covers every row of j in left and weight(k) ≤ weight(j)
L15     drop a row m if some other row's set of primes is a subset of the set of m
    until L13 to L15 change nothing
L16 m ← the row of left with the fewest primes in cols
    for each prime p of row m, cheapest first do
        SOLVE(left minus the rows of p, cols - {p}, chosen + {p}, spent + weight(p))
```

Phase 1 keeps one level of cubes at a time. Level $k$ holds the implicants with $k$ dashes. Line L5 builds the partner $d$ of $c$ across position $i$, and line L6 merges the two into a cube with one more dash. Because $d$ is made from $c$ by changing one bit, the two always have their dashes in the same places. A cube that merges with no partner is prime, and line L8 keeps it. A cube can be made from more than one pair, as 10-- is made from 10-0 with 10-1 and from 100- with 101-, and the set next keeps it once.

Phase 2 is a branch and bound on the prime table. Lines L13 to L15 are the classic reductions. An essential row forces its prime. A column that covers no more rows than another, at no lower weight, can go. A row that every cover of another row also covers can go. When none of them applies, what is left is the cyclic core, and line L16 branches on its hardest row. When two columns cover the same rows at the same weight, line L14 drops only one of them, the one with the larger index.

## Example

Take $F = \{4, 8, 10, 11, 12, 15\}$ and $D = \{9, 14\}$ over $x_1 x_2 x_3 x_4$.

Phase 1, level by level:

| level | cubes | merges | primes kept by L8 |
|---|---|---|---|
| 0 | 0100, 1000, 1001, 1010, 1100, 1011, 1110, 1111 | 10 pairs, for example 0100 + 1100 = -100 | none |
| 1 | -100, 1-00, 10-0, 100-, 1-10, 10-1, 101-, 11-0, 1-11, 111- | 1--0, 1-1- and 10--, each from two pairs | -100 |
| 2 | 1--0, 1-1-, 10-- | none | 1--0, 1-1-, 10-- |

So the primes are -100, 1--0, 1-1- and 10--. The prime table has the rows of $F$ only, not of $D$:

| prime | 4 | 8 | 10 | 11 | 12 | 15 |
|---|---|---|---|---|---|---|
| -100 | x | | | | x | |
| 1--0 | | x | x | | x | |
| 1-1- | | | x | x | | x |
| 10-- | | x | x | x | | |

Phase 2:

| step | line | action | left |
|---|---|---|---|
| 1 | L13 | row 4 has only -100, and row 15 has only 1-1-: take both | {8} |
| 2 | L14 | 1--0 and 10-- both cover row 8 with weight (1, 2): drop 10-- | {8} |
| 3 | L13 | row 8 now has only 1--0: take it | ∅ |
| 4 | L11 | record the cover with cost (3, 7) | |

The result is $x_2 \bar{x}_3 \bar{x}_4 + x_1 \bar{x}_4 + x_1 x_3$. The cover with 10-- in place of 1--0 has the same cost. No branch was needed, because the table had no cyclic core.

## Correctness

Phase 1 is correct by induction on the level: level $k$ is exactly the set of implicants with $k$ dashes. A cube with $k + 1$ dashes lies in $F \cup D$ exactly when its two halves across any one dash do, and lines L4 to L6 build it from those halves. A cube is not prime exactly when one of its literals can be removed, that is, when it is one half of an implicant at the next level, which is the test of lines L6 and L7. So the cubes kept by line L8 are all the primes, and only them.

Phase 2 is correct because each reduction keeps the optimum of the current subproblem: a row with one prime must use it, a dominated column can be swapped for its dominator in any solution at no extra cost, and a dominated row is covered whenever the smaller row is. The branch of line L16 tries every prime of a row that some prime must cover, and the bound of line L12 cuts only branches that cannot beat the best cover found. By Quine's theorem every minimum cover is made of primes, so the best prime cover is a minimum cover. The [full proof](proofs/correctness.md) gives the details.

## Complexity

**Phase 1.** Level $k$ holds at most $\binom{n}{k} 2^{n-k}$ cubes, the number of cubes with $k$ dashes, and the sum over $k$ is $3^n$. Each cube is handled once at its level. Line L4 tries at most $n$ positions, and lines L5 and L6 build a string and look it up in a hash set in $O(n)$ time. So phase 1 takes $O(n^2 3^n)$ time and $O(n 3^n)$ space in the worst case, on the word RAM with hashing in expected $O(n)$ time per string. In terms of the truth table size $N = 2^n$, this is $O(N^{\log_2 3} \log^2 N)$, and $\log_2 3 \approx 1.585$. When no two minterms of $F \cup D$ merge, only level 0 is built, which takes $O(n^2 2^n)$ time.

**Phase 2.** Each pass of lines L11 to L15 takes time polynomial in $p$ and $m$, and each pass removes a row or a column, so a node of the search tree costs $\mathrm{poly}(p, m)$. Each branch adds one prime and covers at least one more row, so the tree has depth at most $m$ and at most $p$ children per node, and at most $p^m$ leaves. This bound is exponential. No polynomial bound is expected, because the table problem is [set cover](/set-cover/), which is NP-hard, and the number of primes $p$ can be of order $3^n / n$ by the result of Chandra and Markowsky.

## Properties

- **Exact.** The output is a minimum cover for the cost (number of cubes, number of literals).
- **Deterministic.** The order of the primes and the tie rules of lines L14 and L16 fix the output.
- **Lists all primes.** Phase 1 builds every implicant of $F \cup D$ on the way, which is the main cost for functions with many don't-cares.
- **Needs minterms.** The input is a list of minterms, so the method needs time at least proportional to $|F \cup D|$, which can be $2^n$ even when the function has a short SOP.

## Variants and improvements

- **McCluskey's grouping.** Sort the cubes of a level by their number of ones. Two cubes can merge only if their counts differ by one, so only neighbor groups are compared. This is the form of the 1956 paper and of most textbooks. A hash set, as in line L6, does the same job.
- **The consensus method.** Quine (1955) builds the primes from any SOP of $f$, not from the minterms: add the consensus of two cubes and remove cubes that other cubes contain, until nothing changes.
- **Recursive prime generation.** Split $f$ by the [Shannon expansion](/shannon-expansion/) and build the primes of $f$ from the primes of its two cofactors. This avoids the minterm list.
- **Implicit methods.** Coudert and Madre store the set of primes and the table as BDDs or [ZDDs](/zero-suppressed-bdd/), and so handle functions with far more primes than one can list. Coudert (1994) surveys them.
- **Other table solvers.** [Petrick's method](/petricks-method/) lists every irredundant cover of the table. A [pseudo-Boolean](/pseudo-boolean-sat/) or integer program solves it with one 0-1 variable per prime. [Greedy set cover](/greedy-set-cover/) gives a cover within a factor $1 + \ln m$ of the fewest cubes, with no search.
- **Multiple outputs.** Give each cube a tag with the set of outputs whose on-set or don't-care set holds it. Two cubes merge when they differ in one bit, and the tag of the result is the intersection of the tags.

## When to use it

Use Quine-McCluskey when the function has few variables, up to about 10 to 15 with a moderate number of primes, and you need a proved minimum, or a reference to test a heuristic against. For larger functions, the number of primes and the cyclic core grow too fast. Then use [Espresso](/espresso/), which does not list the primes and gives a prime and irredundant cover, or an exact implicit method. For hand work on four variables, a [Karnaugh map](/karnaugh-map/) shows the same primes as rectangles.

## Pitfalls

- **Merging cubes with different dashes.** The cubes 1-0 and 10- differ in one bit if one ignores the dashes, but they do not merge: their union is not a cube. Line L5 avoids this, because it builds the partner from $c$ itself.
- **Keeping only the last level.** Primes come from every level. A version that returns only the cubes of the last level, in place of line L8, misses -100 in the example.
- **Don't-cares in the wrong phase.** Line L1 must use $F \cup D$, or the primes are too small. The table of line L13 must use $F$ only, or the cover pays to cover points that need no cover.
- **Stopping after the essential primes.** After line L13, a greedy choice of the rest is not exact. The cyclic function $\sum m(1, 2, 3, 4, 5, 6)$ has no essential prime at all.
- **Dropping both of two equal columns.** If line L14 drops each column that another one dominates, two equal columns drop each other and a row can lose all its primes. Drop one at a time, with a tie rule.

## Implementations

## History

Quine (1952) asked for the shortest normal formula of a truth function and showed that it is a sum of prime implicants. In 1955 he gave the consensus method for finding them. McCluskey (1956) gave the tabular method that merges minterms grouped by their number of ones, and the prime implicant table for the choice of primes. The same year, Petrick gave an algebraic method for solving the table. The method was the standard way to minimize switching circuits on early computers, and it is still the exact method in textbooks.

## References
