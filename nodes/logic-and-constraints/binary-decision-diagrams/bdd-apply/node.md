---
tag: 5A7H4K
kind: algorithm
slug: bdd-apply
name: BDD apply algorithm
aliases:
- Bryant apply
- apply operation
- APPLY
- BDD synthesis
area: logic-and-constraints/binary-decision-diagrams
level: core
summary: Combines two BDDs with a binary boolean operator in time proportional to the product of their sizes.
solves: [boolean-equivalence-checking]
model: word-ram
complexity:
  vars: {f: the number of nodes of the BDD of f, g: the number of nodes of the BDD of g}
  time: {worst: O(f·g) expected}
  space: {extra: O(f·g)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1986
  people: [Randal E. Bryant]
  note: Bryant gave APPLY with a table of computed pairs and proved the bound of the product of the two sizes.
prereqs: [reduced-ordered-bdd, shannon-expansion, cofactor, hash-table]
see_also: [ite-operator, computed-table, reduced-ordered-bdd, bdd-quantification, bdd-compose, boolean-equivalence-checking, memoization, dag-dynamic-programming]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 4.3 (Apply, its table of computed pairs, and the bound of the product of the sizes), Table 1, and the example of the sums of disjoint products that reaches half of this bound
  - paper: doi:10.1109/DAC.1990.114826
    title: Karl S. Brace, Richard L. Rudell and Randal E. Bryant, Efficient implementation of a BDD package, Proceedings of the 27th ACM/IEEE Design Automation Conference, 1990, pages 40 to 45
    locator: Section 4.3 (the unique table, which keeps the result reduced while it is built), Section 4.5 (the computed table) and Section 5.2 (the remark that Apply does not detect equivalent calls)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the synthesis of f op g, and Algorithm S)
  - paper: doi:10.1016/j.ipl.2012.05.007
    title: Ryo Yoshinaka, Jun Kawahara, Shuhei Denzumi, Hiroki Arimura and Shin-ichi Minato, Counterexamples to the long-standing conjecture on the complexity of BDD binary operations, Information Processing Letters 112(16), 2012, pages 636 to 640
    locator: the main result (functions for which the time of Apply is quadratic in the sizes of the input and the output)
---

APPLY computes the [reduced ordered BDD](/reduced-ordered-bdd/) of $f \circ g$ from the BDDs of $f$ and $g$, for any binary Boolean operator $\circ$ such as AND, OR or XOR. It splits both arguments on their top variable by the [Shannon expansion](/shannon-expansion/), solves the two halves, and joins them with the node constructor MK. A [computed table](/computed-table/) stores the result for each pair of nodes, so there are at most $|f| \cdot |g|$ pairs that do real work, and Bryant (1986) showed that this product bound is tight up to a factor of 2. The [ITE operator](/ite-operator/) is the three-argument form that handles all operators with one cache.

## In plain words

You have two diagrams of yes or no questions, and you want the diagram for "both", "either" or "exactly one". Look at the first question in the fixed order that either diagram asks. Answer it with no and solve the smaller problem that is left. Then answer it with yes and solve that problem. Join the two answers under one question box, and drop the box if both answers are the same. Each small problem is one place in the first diagram together with one place in the second. Write down each answer when you find it. Then no pair is solved twice, and the work is at most the number of places in the first diagram times the number in the second.

## The problem

**Input:** a store of reduced ordered BDDs with the order $x_1 < \cdots < x_n$, a binary operator $\circ$ given by its four values, and two nodes $f$ and $g$ of the store.

**Output:** the node of the store for $f \circ g$. Since the store is canonical, this node is unique, so the result can be compared with any other node by id.

## The algorithm

```pseudo id=main
APPLY(op, f, g)
L1  if f and g are terminals then return the terminal op(f, g)
L2  if one argument is a terminal that fixes the result then return it
L3  if the computed table holds (op, f, g) then return it
L4  x_i ← the top variable of f and g (the smallest index)
L5  (f0, f1) ← the cofactors of f by x_i = 0 and x_i = 1
L6  (g0, g1) ← the cofactors of g by x_i = 0 and x_i = 1
L7  r ← MK(i, APPLY(op, f0, g0), APPLY(op, f1, g1))
L8  store r in the computed table under (op, f, g)
L9  return r
```

At line L5, if $f$ tests $x_i$ its cofactors are its low and high child, and otherwise both cofactors are $f$ itself, since $f$ does not depend on $x_i$. Line L2 is the early stop: if $f$ is the terminal $a$, the map $b \mapsto a \circ b$ is $0$, $1$, $b$ or $\neg b$. In the first two cases the result is that constant, for example $0 \wedge g = 0$, and in the third it is $g$, for example $1 \wedge g = g$. A value that fixes the result in this way is a controlling value. Line L2 is an optimization; without it, the recursion goes on to the terminals and the result is the same.

MK is the node constructor of the [reduced ordered BDD](/reduced-ordered-bdd/): MK$(i, l, h)$ returns $l$ if $l = h$, and otherwise the unique node with the triple $(i, l, h)$, which it makes if needed. So the result is reduced as soon as it is built.

## Example

Let $f = x_1 \wedge x_3$ and $g = x_2 \wedge x_3$, and compute $r = f \vee g$. The BDD of $f$ has a node $a = (x_1, 0, c)$ with $c = (x_3, 0, 1)$, and the BDD of $g$ has the node $b = (x_2, 0, c)$, which shares $c$ through the unique table.

| call | top | low call | high call | result |
|---|---|---|---|---|
| $(a, b)$ | $x_1$ | $(0, b)$ | $(c, b)$ | MK$(1, b, c)$ |
| $(0, b)$ | | | | $b$, since $0 \vee g = g$ (line L2) |
| $(c, b)$ | $x_2$ | $(c, 0)$ | $(c, c)$ | MK$(2, c, c) = c$ |
| $(c, 0)$ | | | | $c$ (line L2) |
| $(c, c)$ | $x_3$ | $(0, 0)$ | $(1, 1)$ | MK$(3, 0, 1) = c$ |

In the call $(c, b)$, $c$ does not test $x_2$, so both of its cofactors are $c$. MK$(2, c, c)$ applies the elimination rule. The result is the node $(x_1, b, c)$, "if $x_1$ then $x_3$ else $x_2 \wedge x_3$", with 5 nodes including the two terminals. It is $(x_1 \vee x_2) \wedge x_3$, as expected.

## Correctness

A cofactor commutes with every operator: $(f \circ g)|_{x_i = b} = f|_{x_i = b} \circ g|_{x_i = b}$. Line L7 computes the two cofactors of $f \circ g$ by $x_i$ by induction, and MK joins them by the Shannon expansion. The induction is on the sum of the levels of the two arguments, which grows in each call, because at least one argument tests $x_i$ and is replaced by a child. Every new node comes from MK, so the store stays reduced, and by the [canonicity theorem](/bdd-canonicity/) the result is the one node of $f \circ g$. The full proof is in [the proof file](proofs/correctness.md).

## Complexity

**Theorem (Bryant 1986).** With the computed table, APPLY on $f$ and $g$ does real work (passes line L3 without a hit) at most $|f| \cdot |g|$ times and makes at most $2|f| \cdot |g| + 1$ calls. With hash tables, it takes $O(|f| \cdot |g|)$ expected time, and the result has at most $|f| \cdot |g|$ nodes.

*Proof sketch.* The arguments of every call are a node reachable from $f$ and a node reachable from $g$, since line L5 only moves to a child or stays. A pair that misses the cache stores its result before any later call with the same pair, so each of the $|f| \cdot |g|$ pairs misses at most once. Each miss makes two calls and $O(1)$ other work. Each node of the result is made by one miss, which bounds the size. $\square$

**The bound is tight up to a factor of 2.** Bryant's example: with the order $x_1 < \cdots < x_{2n+2m}$, let

$$f = x_1 x_{n+m+1} \vee \cdots \vee x_n x_{2n+m}, \qquad g = x_{n+1} x_{2n+m+1} \vee \cdots \vee x_{n+m} x_{2n+2m}.$$

The BDD of $f$ reads $x_1, \ldots, x_n$ first and must remember which of them are 1, so it has $2^{n+1}$ nodes, and $g$ has $2^{m+1}$ nodes. The BDD of $f \vee g$ must remember $n + m$ such values and has $2^{n+m+1} = |f| \cdot |g| / 2$ nodes. The tests check this for $1 \leq n, m \leq 3$.

**Without the computed table** the recursion follows the paths of the BDDs, not their nodes, and the number of calls can be exponential in $n$. For the AND of the parity of $x_1, \ldots, x_n$ (with $2n + 1$ nodes) and the parity of the odd-indexed variables (with $n + 1$ nodes), APPLY without line L2 makes these numbers of calls:

| $n$ | calls with the table | calls without the table |
|---|---|---|
| 4 | 23 | 31 |
| 10 | 71 | 2047 |
| 16 | 119 | 131071 |

Without the table the count is $2^{n+1} - 1$, the size of the full decision tree.

## Properties

- **Exact and canonical.** The result is the unique node of $f \circ g$, so an equivalence test of two results is one comparison of ids.
- **Recursive, with depth at most $n + 1$.** Each call moves the top variable down by one level or more.
- **Persistent.** APPLY only adds nodes, so all earlier nodes keep their meaning.
- **Output size.** $|f \circ g| \leq |f| \cdot |g|$ for every operator. Repeated APPLY calls can still grow sizes fast: $k$ calls can give a BDD of size up to the product of $k + 1$ input sizes.

## Variants and improvements

- **ITE.** The [ITE operator](/ite-operator/) computes $\mathrm{ite}(f, g, h)$, which covers all 16 binary operators with one cache, at the cost of a three-part key. Many packages use ITE, plus a fast AND.
- **Complemented edges.** With [complemented edges](/complemented-edges/), negation takes $O(1)$ time, and $f \wedge g$, $\neg f \vee \neg g$ and similar calls share cache entries.
- **Breadth-first synthesis.** A breadth-first version treats all pairs of one level together and then the next level. It uses memory in a more regular way. Knuth's Algorithm S in Section 7.1.4 is of this kind.
- **AND with quantification.** The relational product $\exists X\,(f \wedge g)$ is one recursion that quantifies while it computes the AND; see [BDD quantification](/bdd-quantification/).
- **Many arguments.** An $n$-ary APPLY splits all arguments at once. Its pairs become tuples, and its bound is the product of all sizes.

## When to use it

Use APPLY to build the BDD of a formula or a circuit gate by gate, and to combine constraints. It is the core of [boolean equivalence checking](/boolean-equivalence-checking/) with BDDs: build both functions and compare the two root ids. For a package with many operators, use the [ITE operator](/ite-operator/) as the core and keep APPLY for the most frequent operator, usually AND.

## Pitfalls

- **No computed table.** Without it APPLY takes time exponential in $n$ on BDDs with $O(n)$ nodes, as the table above shows.
- **A cache key without the operator.** The key must include $\circ$, or a result of AND can be returned for an OR call on the same pair.
- **The wrong top variable.** The split must use the smaller index of the two top variables. If it uses the top variable of $f$ only, the cofactor of $g$ is wrong when $g$ tests that variable below its top.
- **The order of the children in MK.** MK takes the low child first. Swapping them computes a different function.
- **Stale cache entries.** After nodes are freed, the cache must drop entries that name them.
- **Size growth.** The product bound is an upper bound, and real results can reach a large part of it. A chain of APPLY calls on a bad [variable ordering](/variable-ordering/) can run out of memory.

## Implementations

## History

Bryant (1986) gave APPLY together with REDUCE and RESTRICT, and proved that APPLY runs in time $O(|G_1| \cdot |G_2|)$ with a table of the pairs already computed. His APPLY built the result graph first and then called REDUCE. He also gave the sums of disjoint products above as a case where the result has half of this many nodes. He conjectured that the time of APPLY is linear in the sizes of the two inputs and the result. Yoshinaka, Kawahara, Denzumi, Arimura and Minato (2012) disproved this conjecture. For AND and OR they gave inputs where the result has constant size but APPLY takes time quadratic in the input size. Bollig (2014) gave simpler counterexamples in which the inputs have BDDs of optimal size up to a constant factor. Brace, Rudell and Bryant (1990) kept the result reduced while it is built, with a unique table in MK, and used a hash-based computed table, as most packages do today. Knuth (2011, Section 7.1.4) treats the synthesis of $f \circ g$ in depth.

## References
