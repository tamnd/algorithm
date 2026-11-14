---
tag: P7JR23
kind: algorithm
slug: petricks-method
name: Petrick's method
aliases:
- Petrick function
area: eda/logic-synthesis
level: intro
summary: Solves the prime implicant covering table exactly by writing it as a product of sums of primes, expanding to a sum of products and taking the cheapest term.
solves: [two-level-logic-minimization]
model: word-ram
complexity:
  vars: {m: the number of rows (on-set minterms), p: the number of primes, T: "the largest number of products after a row, at most 2^p"}
  time: {worst: O(m p^2 T^2), best: O(m p)}
  space: {extra: O(p T)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1956
  people: [Stanley R. Petrick]
  note: Petrick gave the method in a 1956 report of the Air Force Cambridge Research Center, as a direct way to find all irredundant forms of a function from its prime implicants.
prereqs: [prime-implicant, set-cover]
see_also: [quine-mccluskey, minimal-transversal-enumeration, hitting-set, two-level-logic-minimization, conjunctive-normal-form, sum-of-products, binate-covering-problem, espresso]
sources:
  - paper: "S. R. Petrick, A direct determination of the irredundant forms of a Boolean function from the set of prime implicants, Technical Report AFCRC-TR-56-110, Air Force Cambridge Research Center, 1956"
    title: A direct determination of the irredundant forms of a Boolean function from the set of prime implicants
    locator: the product of sums of the prime implicant table and its expansion into the irredundant forms
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 7, Two-Level Combinational Logic Optimization (exact minimization and the covering problem)
  - book: isbn:9780792397465
    title: Gary D. Hachtel and Fabio Somenzi, Logic Synthesis and Verification Algorithms, Kluwer, 1996
    locator: Chapter 4, Synthesis of Two-Level Circuits (the covering table and its exact solution)
  - paper: doi:10.1016/0167-9260(94)00007-7
    title: Olivier Coudert, Two-level logic minimization, an overview, Integration, the VLSI Journal 17(2), 97 to 140, 1994
    locator: exact solution of the covering problem and the limits of explicit enumeration
---

Petrick's method solves the prime implicant table of [Quine-McCluskey](/quine-mccluskey/) exactly. Give each prime a Boolean variable that is true when the prime is in the cover. A row of the table, one minterm of the on-set, is covered when at least one of its primes is chosen, so it becomes a sum of variables. The table is covered when every row is, so the condition is a product of these sums, the Petrick function. Multiply it out into a sum of products and remove each product that contains another one. Each product that is left is an irredundant cover, and the cheapest one is a minimum cover. The method is simple and exact, but the number of products can grow exponentially, so it suits small tables and the cyclic core that is left after the essential primes are taken.

## In plain words

Write a list of choices for each row of the table, such as "prime A or prime B". To cover all rows, you need one choice from every list. Go through the lists one at a time and keep every way of choosing so far. When a way already covers the new row, keep it as it is. When it does not, make one new way for each prime of that row. Throw out a way when a smaller way uses only some of its primes. At the end, each way is a cover that has no extra prime, and you take the cheapest.

## The problem

The input is a covering table: rows $r_1, \ldots, r_m$, where row $r_i$ is the set of primes that contain the $i$-th minterm of the on-set, and a weight $w(j) = (1, \text{literals of prime } j)$ for each of the $p$ primes. A set $S$ of primes is a cover when it meets every row. The output is a cover of least total weight, with weights added coordinatewise and compared lexicographically. When the primes are all the primes of $f$, such a cover is a minimum [sum of products](/sum-of-products/) of $f$. The problem is the unate case of [set cover](/set-cover/), and the covers that have no extra prime are the minimal [hitting sets](/hitting-set/) of the rows.

## The algorithm

```pseudo id=main
PETRICK(rows)                       ▷ a product is a set of primes
L1  products ← { ∅ }                ▷ the empty product is 1
L2  for each row r do
L3      if r = ∅ then return ∅      ▷ an empty sum is 0: no cover exists
        step ← ∅
L4      for each product t ∈ products do
L5          if t meets r then add t to step                ▷ t (t + y) = t
L6          else for each prime j ∈ r do add t ∪ {j} to step
L7      products ← the sets of step that contain no other set of step
    return products

CHEAPEST(products, w)
L8  return the product t of least total weight, ties by the sorted list of t
```

The loop of line L2 multiplies the sums of the rows into the running sum of products, one row at a time. Line L5 is the absorption law: when the product $t$ already has a prime of the row, the factor $(t + y)$ adds nothing. Line L6 is the distributive law for the other products. Line L7 is absorption between products, $X + XY = X$, and it also removes repeated products. The products that line L7 keeps are the inclusion-minimal sets of primes that cover the rows seen so far. Line L8 picks the cheapest of them. Every weight is positive, so a cheapest cover never has an extra prime, and line L8 never misses it.

## Example

Take $f = \sum m(0, 1, 2, 5, 6, 7)$ over $x_1 x_2 x_3$. It has six primes and no essential one, so the whole table is a cyclic core:

| prime | cube | minterms |
|---|---|---|
| A | 00- | 0, 1 |
| B | 0-0 | 0, 2 |
| C | -01 | 1, 5 |
| D | -10 | 2, 6 |
| E | 1-1 | 5, 7 |
| F | 11- | 6, 7 |

The Petrick function is $(A + B)(A + C)(B + D)(C + E)(D + F)(E + F)$. Lines L2 to L7 multiply it out:

| row | sum | size of step | products after L7 |
|---|---|---|---|
| 0 | A + B | 2 | A, B |
| 1 | A + C | 3 | A, BC |
| 2 | B + D | 3 | AB, AD, BC |
| 5 | C + E | 5 | BC, ABE, ACD, ADE |
| 6 | D + F | 6 | ACD, ADE, BCD, BCF, ABEF |
| 7 | E + F | 7 | ADE, BCF, ABEF, ACDF, BCDE |

At row 1, A meets the row and stays, and B becomes BA and BC. Then BA contains A, and line L7 removes it. The five final products are the five irredundant covers. ADE and BCF have three cubes and six literals each, and the other three have four cubes. Line L8 picks ADE by the tie rule, so the result is $\bar{x}_1 \bar{x}_2 + x_2 \bar{x}_3 + x_1 x_3$.

## Correctness

The products after row $t$ are exactly the inclusion-minimal sets of primes that meet the first $t$ rows. This holds for $t = 0$, where the only minimal set is the empty set. Each set that line L5 or line L6 adds meets the new row. Each minimal set $S$ for the first $t$ rows contains a minimal set $T$ for the first $t - 1$ rows. If $T$ meets row $t$, line L5 adds $T$, and so $S = T$. If not, $S$ holds a prime $j$ of row $t$, line L6 adds $T \cup \{j\} \subseteq S$, and so $S = T \cup \{j\}$. Line L7 then keeps exactly the minimal sets of step. Since every weight is positive, a cheapest cover has no extra prime, so it is among the final products. The [full proof](proofs/correctness.md) gives the details.

## Complexity

Let $T$ be the largest number of products after any row. A row turns each product into at most $p$ sets, so step has at most $pT$ sets of at most $p$ primes each. The absorption of line L7 compares each set of step with the kept sets, in $O(p^2 T^2)$ time when sets are bit vectors or hash sets of $O(p)$ words. Over $m$ rows this is $O(m p^2 T^2)$ time and $O(pT)$ extra space. In the best case one prime is in every row, $T = 1$, and the time is $O(mp)$.

$T$ can be exponential. With $k$ rows that are pairwise disjoint pairs $\{a_i, b_i\}$, every choice of one prime from each pair is a minimal cover, so $T = 2^k$. The final count is the number of minimal transversals of the rows, and $T$ can be much larger, since a prefix of the rows can have many more minimal covers than the whole table. If the $k$ pairs above come first and are followed by the $k$ rows $\{a_1\}, \ldots, \{a_k\}$, the middle list has $2^k$ products and the final list has one. In general $T \le 2^p$, and $T$ is at most the product of the row sizes.

## Properties

- **Exact.** It returns a minimum cover for any positive weights.
- **Lists all irredundant covers.** The final products are all covers with no extra prime, which is useful when a second cost decides among the minimum ones.
- **Not output-sensitive.** The middle steps can hold far more products than the final answer.
- **Simple.** It needs only sets and the two laws of absorption, which makes it a good hand method for small cyclic cores.

## Variants and improvements

- **Reduce first.** Take the essential primes and remove the dominated rows and columns before the expansion, as [Quine-McCluskey](/quine-mccluskey/) does in phase 2. Only the cyclic core needs Petrick's method.
- **Bound the products.** Drop a product as soon as its weight is not less than the weight of a known cover. This turns the method into a [branch and bound](/depth-first-branch-and-bound/) search and loses the list of all irredundant covers.
- **Row order.** Process rows with few primes first. This keeps the middle steps small in many tables, but it does not change the worst case.
- **Implicit products.** Store the set of products as a [ZDD](/zero-suppressed-bdd/), where the multiplication and the absorption become set operations on the diagram. This can handle far more products than an explicit list.
- **Minimal transversal enumeration.** The final list is the set of minimal transversals of the rows. Algorithms for [minimal transversal enumeration](/minimal-transversal-enumeration/) list them with better bounds on the time per output.
- **Binate covering.** When a choice of one column forces or forbids others, the condition is no longer a product of positive sums. The [binate covering problem](/binate-covering-problem/) handles this case.

## When to use it

Use Petrick's method for a small cyclic core, when you want every irredundant cover or a proof by hand that a cover is minimum. For large tables, a branch and bound on the table, or a [pseudo-Boolean](/pseudo-boolean-sat/) solver, finds the minimum without the full list. When an exact answer is not needed, a greedy choice or [Espresso](/espresso/) is much faster.

## Pitfalls

- **Forgetting absorption.** If line L7 keeps every set of step, the list holds every cover, including covers with extra primes, and it can grow by a factor $p$ at every row.
- **Expanding a covered product.** If line L5 is left out, a product that already meets the row is still multiplied by each prime of the row. The result is correct after absorption, but the middle lists are larger.
- **Absorbing the wrong product.** The law $X + XY = X$ removes the larger product $XY$. If line L7 keeps the superset and removes the subset, the result has extra primes and can miss the minimum.
- **Rows for don't-cares.** The rows of line L2 are the minterms of the on-set only. A row for a don't-care minterm forces the cover to contain it, and the answer can cost more than the minimum.
- **Using it on the whole table.** Running it before the essential primes are taken makes the lists larger for no gain.

## Implementations

## History

Petrick (1956) gave the method in a report of the Air Force Cambridge Research Center, the same year as McCluskey's tabular method for the primes. The two together became the standard exact procedure taught for two-level minimization: Quine-McCluskey for the primes and the table, and Petrick's method for the cyclic part. The same algebra appears in later work on covering and on the enumeration of minimal transversals of hypergraphs.

## References
