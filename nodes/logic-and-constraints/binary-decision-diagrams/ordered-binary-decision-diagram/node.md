---
tag: 8Z0NZS
kind: data-structure
slug: ordered-binary-decision-diagram
name: Ordered binary decision diagram
aliases:
- OBDD
- ordered BDD
- π-OBDD
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: A BDD in which every path tests variables in one fixed global order.
model: word-ram
complexity:
  vars: {p: the number of nodes of the diagram, n: the number of variables}
  time: {evaluate: O(n), is_ordered: O(p), tree: O(2^n), reduce: O(p) expected}
  space: {nodes: O(p)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1986
  people: [Randal E. Bryant]
  note: Bryant required one variable order on all paths, and showed that with this rule the reduced diagram is canonical and the Boolean operations take polynomial time.
prereqs: [binary-decision-diagram, shannon-expansion, cofactor]
see_also: [binary-decision-diagram, reduced-ordered-bdd, bdd-reduction-rules, bdd-canonicity, variable-ordering, free-binary-decision-diagram, decision-tree, bdd-apply]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 2, Definition 1 (the index of a vertex increases along each path), Section 3, Figure 2 (two orders for x1x2 + x3x4 + x5x6), and Section 4.2, Reduce
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 3, OBDDs, and Chapter 5, The variable-ordering problem
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the ordering of the variables and the effect of the order on the size)
---

An ordered binary decision diagram (OBDD) is a [binary decision diagram](/binary-decision-diagram/) with one fixed order $\pi$ of the variables, such that each path from the root tests the variables in this order. It may skip variables, but it never tests a variable twice and never tests a variable above one that comes earlier in $\pi$. This one rule makes the children of each node the [cofactors](/cofactor/) of its function, so the algorithms of Bryant can recurse on the [Shannon expansion](/shannon-expansion/). An OBDD becomes the canonical [reduced ordered BDD](/reduced-ordered-bdd/) when the [reduction rules](/bdd-reduction-rules/) are applied, and its size depends strongly on the order; see [variable ordering](/variable-ordering/).

## In plain words

Take a flow chart of yes or no questions about some switches, as in a binary decision diagram. Now add one rule. Put the switches in a list, first, second, third and so on. On every route through the chart, the questions must come in the order of the list. A route may skip a switch, but it may not go back to an earlier one. So each switch is asked about at most once on each route. Each part of the chart below a question then only talks about later switches. Because of this, two charts with the same list can be compared and combined level by level. The list matters a lot: one list can give a small chart and another list a very large one for the same task.

## The abstract type

An OBDD over $x_1, \ldots, x_n$ with the order $\pi = (\pi_1, \ldots, \pi_n)$ stores Boolean functions in $B_n$, one for each root. Write $\mathrm{lev}(u) = k$ when $\mathrm{var}(u) = x_{\pi_k}$, and $\mathrm{lev}(u) = n + 1$ for the terminals 0 and 1. The diagram is **ordered** when

$$\mathrm{lev}(\mathrm{lo}(u)) > \mathrm{lev}(u) \quad \text{and} \quad \mathrm{lev}(\mathrm{hi}(u)) > \mathrm{lev}(u) \qquad \text{for each inner node } u.$$

The operations on this page are EVAL$(u, x)$, IS-ORDERED$(r)$, TREE$(T)$, which builds the decision tree of a truth table $T$, and REDUCE$(r)$, which returns the reduced ordered diagram of $f_r$. The other operations ([APPLY](/bdd-apply/), [ITE](/ite-operator/), restriction, [quantification](/bdd-quantification/)) are on the [reduced ordered BDD](/reduced-ordered-bdd/) page and on their own pages. They need the order, but most of them also keep the result reduced.

**Children are cofactors.** Let $u$ test $x_i$. Every node below $u$ has a larger level, so $f_{\mathrm{lo}(u)}$ and $f_{\mathrm{hi}(u)}$ do not depend on $x_i$. By part 5 of the [Shannon expansion](/shannon-expansion/), $f_{\mathrm{lo}(u)} = f_u|_{x_i=0}$ and $f_{\mathrm{hi}(u)} = f_u|_{x_i=1}$. In a general BDD this fails, and it is the property that each OBDD algorithm uses.

## Representation

The representation is the same as for a [binary decision diagram](/binary-decision-diagram/): the terminals have the ids 0 and 1, an inner node is a triple $(\mathrm{var}, \mathrm{lo}, \mathrm{hi})$, and a child has a smaller id than its parent. The store also keeps the order $\pi$ as an array $\mathrm{level}[v]$, so a level test is one array read. Several OBDDs can share nodes only when they use the same order.

REDUCE uses a hash table from triples to node ids, the unique table of the [reduced ordered BDD](/reduced-ordered-bdd/). All calls share it, so equal functions get the same id.

## Operations

```pseudo id=main
EVAL(u, x)
L1  while u is not a terminal do
L2      if x[var(u)] = 1 then u ← hi(u) else u ← lo(u)
L3  return the label of u

IS-ORDERED(r)
L4  for each inner node u reachable from r do
L5      for each child c of u do
L6          if lev(c) ≤ lev(u) then return false
L7  return true

TREE(T)  is  go(0, 0)                 ▷ T is a truth table of length 2^n
go(k, a)                              ▷ a fixes x_{π_1}, ..., x_{π_k}
L8  if k = n then return the terminal T[a]
L9  i ← π_{k+1}
L10 return NODE(i, lo = go(k + 1, a), hi = go(k + 1, a with x_i = 1))

REDUCE(r)
L11 for each node u reachable from r, children before parents do
L12     if u is a terminal then R[u] ← u
L13     else l ← R[lo(u)]; h ← R[hi(u)]
L14         if l = h then R[u] ← l                       ▷ remove a redundant test
L15         else if (var(u), l, h) is in the table H then R[u] ← H[var(u), l, h]   ▷ share a duplicate
L16         else R[u] ← NODE(var(u), l, h); H[var(u), l, h] ← R[u]
L17 return R[r]
```

TREE is the full decision tree with the two terminals shared: it has $2^n - 1$ inner nodes, one for each assignment to a prefix of $\pi$. REDUCE applies the two [reduction rules](/bdd-reduction-rules/) bottom-up in one pass. Bryant's version visits the nodes level by level and sorts the pairs $(\mathrm{lo}, \mathrm{hi})$ of each level. The version here uses the hash table in place of the sort.

## Example

**A small function.** Let $f = (x_1 \wedge x_2) \vee x_3$ with $\pi = (x_1, x_2, x_3)$. TREE makes 7 inner nodes, so the tree has 9 nodes with the terminals. REDUCE first merges the four nodes on $x_3$: two of them have the children $(0, 1)$ and become the node $c = (x_3, 0, 1)$, and two have the children $(1, 1)$ and are removed, since they test $x_3$ for nothing. On level 2, the node for $x_1 = 0$ has the children $(c, c)$ and is removed, and the node for $x_1 = 1$ becomes $b = (x_2, c, 1)$. The root becomes $a = (x_1, c, b)$. The result has 5 nodes: $a$, $b$, $c$, 0 and 1.

**The order matters.** Let $f = x_1 x_2 \vee x_3 x_4 \vee \cdots \vee x_{2k-1} x_{2k}$.

| $k$ | size with $\pi = (x_1, x_2, \ldots, x_{2k})$ | size with $\pi = (x_1, x_3, \ldots, x_{2k-1}, x_2, x_4, \ldots, x_{2k})$ |
|---|---|---|
| 1 | 4 | 4 |
| 2 | 6 | 8 |
| 3 | 8 | 16 |
| 4 | 10 | 32 |

With the first order the size is $2k + 2$: each pair is decided before the next one starts, so one node per variable and the two terminals suffice. With the second order the size is $2^{k+1}$. After the odd variables are read, the rest of the function is $\bigvee_{j \in S} x_{2j}$, where $S$ is the set of $j$ with $x_{2j-1} = 1$. The $2^k$ sets $S$ give $2^k$ different functions, and by [canonicity](/bdd-canonicity/) each needs its own node. Bryant used this example ($k = 3$, sizes 8 and 16) to show the effect of the order.

## Correctness

EVAL keeps the value $f_u(x)$ at each step. IS-ORDERED checks the level rule on every edge. TREE builds the cofactor of $f$ by each prefix assignment, by induction from the leaves and by the Shannon expansion. REDUCE keeps the function of each node: a node with equal children has the function of its child, and two nodes with the same triple have the same function. Each node that REDUCE makes has different children and a triple that no other made node has. The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

- EVAL makes at most $n$ steps, because the level grows at each step: $O(n)$ time. A general BDD only gives $O(p)$.
- IS-ORDERED reads each edge once: $O(p)$ time.
- TREE makes $2^n - 1$ inner nodes: $\Theta(2^n)$ time and space. It is a way to get a first OBDD from a table, not a practical way to build large OBDDs. [APPLY](/bdd-apply/) builds them from smaller ones.
- REDUCE makes one table lookup per node: $O(p)$ expected time with hashing. Bryant's version with a sort per level takes $O(p \log p)$. Sieling and Wegener (1993) gave a deterministic linear-time version.
- Satisfiability of $f_r$ is reachability of the terminal 1, in $O(p)$ time, because an OBDD is a [free BDD](/free-binary-decision-diagram/) and every path is consistent.
- Equivalence of two OBDDs with the same order takes $O(p)$ expected time: reduce both into one table and compare the ids. For two different orders the ids cannot be compared, and rebuilding one diagram in the order of the other can make it exponentially larger, as the example shows.

## Variants

- **[Reduced ordered BDD](/reduced-ordered-bdd/)**: an OBDD to which REDUCE has been applied. It is the minimum OBDD of its function for the order, and it is unique.
- **Quasi-reduced OBDD**: each path tests every variable, so no level is skipped, and duplicates are shared. It is also canonical. It has more nodes, but every edge goes down exactly one level, which suits level-by-level algorithms.
- **[Free BDD](/free-binary-decision-diagram/)**: each path tests each variable at most once, but different paths may use different orders. It can be exponentially smaller than every OBDD of the same function.
- **Shared OBDD**: one store with many roots and one order, as in BDD packages. All functions share the unique table.
- **[Zero-suppressed BDD](/zero-suppressed-bdd/)**: also ordered, with a different rule for removing nodes.

## When to use it

Use an OBDD when you need to combine functions and compare them, not only to evaluate them. The fixed order lets [APPLY](/bdd-apply/) walk two diagrams in step, and with the reduction rules each function has one form. Choose the order with care: variables that interact should be near each other, as the example shows. For some functions, such as the middle bit of integer multiplication, every order gives exponential size; see the [multiplier lower bound](/multiplier-bdd-lower-bound/).

In practice an OBDD is almost always kept reduced. The unreduced form appears as an input, for example a decision tree from a table, or as the output of an algorithm before REDUCE runs.

## Pitfalls

- **Two orders do not mix.** APPLY and the equality test by node ids need the same order for both arguments. To combine diagrams with different orders, first rebuild one in the order of the other.
- **Ordered is not reduced.** An OBDD can have redundant tests and duplicate nodes, so two OBDDs of one function can look different. Compare functions only after REDUCE, or keep every diagram reduced as it is built.
- **The level of a terminal.** A terminal must have a level larger than every variable, or the level test of IS-ORDERED and of APPLY gives wrong answers at the bottom.
- **The order changes the size by an exponential factor.** A bad order is the usual cause of a BDD that does not fit in memory. Finding the best order is hard; see [variable ordering](/variable-ordering/).

## Implementations

## History

Earlier binary decision diagrams, by Lee (1959) and Akers (1978), had no rule on the order of the tests. Bryant (1986) made the order a part of the definition. He showed that the reduced ordered diagram of a function is unique, gave the REDUCE procedure, and showed that the Boolean operations on two ordered diagrams with the same order take polynomial time. He also showed by examples that the order changes the size by an exponential factor. Wegener (2000) gives the theory of OBDDs, of their size for selected functions, and of the ordering problem.

## References
