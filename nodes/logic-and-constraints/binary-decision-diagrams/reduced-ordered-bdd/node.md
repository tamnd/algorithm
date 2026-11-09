---
tag: 4A6P2D
kind: data-structure
slug: reduced-ordered-bdd
name: Reduced ordered binary decision diagram
aliases:
- ROBDD
- reduced OBDD
- BDD package
- shared ROBDD
area: logic-and-constraints/binary-decision-diagrams
level: core
summary: An OBDD with no redundant tests and no duplicate nodes; canonical for a fixed order.
model: word-ram
complexity:
  vars: {f: the number of nodes of the ROBDD of the argument, n: the number of variables}
  time: {mk: O(1) expected, evaluate: O(n), restrict: O(f) expected, equal: O(1), build: O(2^n) expected}
  space: {nodes: O(f)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1986
  people: [Randal E. Bryant]
  note: Bryant defined reduced function graphs with a fixed variable order, proved them canonical and gave Reduce, Apply, Restrict, Compose and Satisfy.
prereqs: [ordered-binary-decision-diagram, bdd-reduction-rules, hash-table]
see_also: [bdd-canonicity, bdd-apply, ite-operator, computed-table, complemented-edges, bdd-satisfy-count, variable-ordering, hash-consing]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 2 (Definition 5, reduced function graphs, and Theorem 1, canonicity), Section 4, Table 1 (the cost of each operation), and Sections 4.4 and 4.6 (Restrict and Satisfy)
  - paper: doi:10.1109/DAC.1990.114826
    title: Karl S. Brace, Richard L. Rudell and Randal E. Bryant, Efficient implementation of a BDD package, Proceedings of the 27th ACM/IEEE Design Automation Conference, 1990, pages 40 to 45
    locator: the unique table as a hash table that makes a strong canonical form, the computed table as a hash cache, and the ITE interface
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (beads, the size B(f), and BDD bases with shared nodes)
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 3, OBDDs (the reduction rules, the uniqueness of the reduced OBDD and the operations)
---

A reduced ordered binary decision diagram (ROBDD) is an [ordered BDD](/ordered-binary-decision-diagram/) that has no node with two equal children and no two nodes with the same variable and the same children. For a fixed variable order, each [Boolean function](/boolean-function/) has exactly one ROBDD, and it is the smallest ordered BDD of the function; this is the [canonicity theorem](/bdd-canonicity/). A BDD package keeps all its functions in one shared ROBDD and makes every node through a unique table, a [hash table](/hash-table/) from triples to nodes, so two functions are equal exactly when their root pointers are equal. Most texts say "BDD" and mean this structure.

## In plain words

Draw a flow chart of yes or no questions with the questions in a fixed list order, as in an ordered BDD. Then clean it up with two rules. If a question sends both answers to the same place, remove the question. If two questions ask the same thing and send their answers to the same places, keep one of them. When neither rule can be used any more, the chart is reduced. The main fact is that the reduced chart depends only on the task, not on how it was built. So a program that keeps every chart reduced can tell whether two tasks are the same by checking whether they are the same chart. A small table of all boxes made so far lets it reuse a box in place of making a copy.

## The abstract type

A ROBDD manager with $n$ variables and a fixed order $x_1 < x_2 < \cdots < x_n$ stores a set of functions in $B_n$. Each function is a node id. The operations and their costs, for arguments with $|f|$, $|g|$ and $|h|$ nodes:

| operation | result | time | page |
|---|---|---|---|
| EQUAL$(f, g)$ | is $f = g$? | $O(1)$ | this page |
| EVAL$(f, x)$ | $f(x)$ | $O(n)$ | this page |
| MK$(i, l, h)$ | the node $(\neg x_i \wedge l) \vee (x_i \wedge h)$ | $O(1)$ expected | this page |
| BUILD$(T)$ | the node of a truth table $T$ | $O(2^n)$ expected | this page |
| RESTRICT$(f, i, b)$ | the [cofactor](/cofactor/) $f\vert_{x_i=b}$ | $O(\vert f\vert)$ expected | this page |
| APPLY$(\circ, f, g)$ | $f \circ g$ for a binary operator | $O(\vert f\vert \cdot \vert g\vert)$ | [BDD apply](/bdd-apply/) |
| ITE$(f, g, h)$ | $(f \wedge g) \vee (\neg f \wedge h)$ | $O(\vert f\vert \cdot \vert g\vert \cdot \vert h\vert)$ | [ITE operator](/ite-operator/) |
| EXISTS$(f, X)$ | $\exists X\, f$ | see the page | [BDD quantification](/bdd-quantification/) |
| COMPOSE$(f, i, g)$ | $f\vert_{x_i=g}$ | $O(\vert f\vert^2 \cdot \vert g\vert)$ | [BDD compose](/bdd-compose/) |
| SATCOUNT$(f)$ | $\vert S_f\vert$ | $O(\vert f\vert)$ additions | [satisfy-count](/bdd-satisfy-count/) |
| SAT-ONE$(f)$ | one model, if $f \ne 0$ | $O(n)$ | this page |

The times assume a [computed table](/computed-table/) for APPLY, ITE and COMPOSE. Negation costs $O(|f|)$ with APPLY, or $O(1)$ with [complemented edges](/complemented-edges/).

## Representation

**Node store.** The terminals 0 and 1 have the ids 0 and 1 and the level $n + 1$. An inner node is a triple $(i, \mathrm{lo}, \mathrm{hi})$ in an array. A child is made before its parent, so it has a smaller id. Nodes are never changed, so the structure is persistent: a function, once built, stays valid while later functions are built, and functions share their common subfunctions.

**Unique table.** A hash table $U$ maps each triple $(i, \mathrm{lo}, \mathrm{hi})$ to the node with this triple. Every node is made by MK, which first applies the elimination rule ($\mathrm{lo} = \mathrm{hi}$) and then looks up the triple. This is [hash consing](/hash-consing/). It keeps the invariant that the whole store is one reduced ordered diagram with many roots. Packages often keep one table per variable, which makes it cheap to change the order.

**Computed table.** A second hash table, the [computed table](/computed-table/), stores the results of recent APPLY or ITE calls, keyed by the operator and the argument ids. It is a cache: a lost entry costs time but not correctness. Without it, APPLY can take exponential time.

**Memory.** Real packages keep a [reference count](/reference-counting/) in each node and free the nodes that no root reaches, then remove their entries from both tables. Many also use [complemented edges](/complemented-edges/), which store $f$ and $\neg f$ as one node.

## Operations

The variables are numbered from 1 to $n$, entry $a$ of a truth table is $f(x)$ for $a = \sum_j x_j 2^{j-1}$, and $\mathrm{lev}(u)$ is the index of the variable of $u$, or $n + 1$ for a terminal.

```pseudo id=main
MK(i, l, h)                          ▷ the node (¬x_i ∧ l) ∨ (x_i ∧ h)
L1  if l = h then return l                       ▷ elimination rule
L2  if U holds the key (i, l, h) then return U[i, l, h]   ▷ merging rule
L3  u ← a new node with the triple (i, l, h)
L4  U[i, l, h] ← u
L5  return u

BUILD(T)                             ▷ T[0 .. 2^n − 1] is a truth table
L6  for each a: c[a] ← the terminal T[a]
L7  for i ← n downto 1 do
L8      for p ← 0 to 2^{i−1} − 1 do
L9          c[p] ← MK(i, c[p], c[p + 2^{i−1}])
L10 return c[0]

EVAL(u, x)
L11 while u is not a terminal do
L12     if x[var(u)] = 1 then u ← hi(u) else u ← lo(u)
L13 return the label of u

RESTRICT(f, i, b)  is  go(f), with an empty memo   ▷ f|x_i=b
go(u)
L14 if lev(u) > i then return u
L15 if lev(u) = i then return hi(u) if b = 1, else lo(u)
L16 if memo holds u then return memo[u]
L17 r ← MK(var(u), go(lo(u)), go(hi(u)))
L18 memo[u] ← r; return r
L19 (the first call is go(f))

EQUAL(f, g)
L20 return f = g                                 ▷ compare two ids
```

SAT-ONE follows any path to the terminal 1: at a node, go to a child that is not the terminal 0. In a reduced diagram every inner node has the terminal 1 below it (Bryant's Lemma 3), so this walk never has to go back, and it makes at most $n$ steps.

## Example

Let $f = (x_1 \wedge x_2) \vee x_3$. Its truth table is $T = 00011111$, since $f = 1$ for $a = 3, 4, 5, 6, 7$.

- Round $i = 3$ pairs $c[p]$ with $c[p + 4]$. The first three pairs are $(0, 1)$: the first call makes the node $c = (x_3, 0, 1)$, and the next two find it in $U$. The pair $(1, 1)$ is removed by line L1. Now $c[0..3] = (c, c, c, 1)$.
- Round $i = 2$ pairs $c[p]$ with $c[p + 2]$: MK$(2, c, c)$ returns $c$, and MK$(2, c, 1)$ makes $b = (x_2, c, 1)$.
- Round $i = 1$: MK$(1, c, b)$ makes the root $a = (x_1, c, b)$.

The ROBDD has 5 nodes: $a$, $b$, $c$ and the two terminals. If we build the same function in another way, for example as the OR of its five minterms with APPLY, every MK call meets the same triples in $U$, and the result is the same id $a$. So EQUAL returns true.

RESTRICT$(a, 2, 1)$ computes $f|_{x_2=1} = x_1 \vee x_3$. At $a$, which tests $x_1 < x_2$, line L17 recurses: $\mathrm{go}(c) = c$ by line L14, and $\mathrm{go}(b) = \mathrm{hi}(b) = 1$ by line L15. The result is the new node $(x_1, c, 1)$. SATCOUNT$(a) = 5$, and SAT-ONE$(a)$ follows $a \to c \to 1$ and returns $x_1 = 0$, $x_3 = 1$, with $x_2$ free.

## Correctness

MK keeps an invariant: no node has two equal children, each edge goes down in the order, and the unique table holds exactly one node for each triple. BUILD applies the [Shannon expansion](/shannon-expansion/) bottom-up, one variable per round. RESTRICT replaces each node on $x_i$ by one of its children, which are the cofactors because the order puts $x_i$ above all variables below the node. EQUAL is correct because of canonicity: in a store with the invariant, two nodes with the same function are the same node. The proof goes down by levels. A node that tests $x_m$ depends on $x_m$, so two equal functions start at the same level, have equal cofactors, and by induction equal children. The full proofs are in [the proof file](proofs/correctness.md), and the [canonicity](/bdd-canonicity/) page adds that the ROBDD is the smallest ordered BDD of its function.

## Complexity

- MK is one hash lookup and at most one insertion: $O(1)$ expected time.
- BUILD calls MK $2^n - 1$ times: $O(2^n)$ expected time, linear in the size of the table.
- RESTRICT calls MK at most once per node of $f$: $O(|f|)$ expected time, and the result has at most $|f|$ nodes. Bryant gives $O(|f| \log |f|)$ because he runs his Reduce after the redirect step; with the unique table no separate Reduce is needed.
- EVAL and SAT-ONE take $O(n)$ time, and EQUAL takes $O(1)$.

**Size.** The nodes on level $k$ are the distinct subfunctions $f|_{x_1=a_1, \ldots, x_{k-1}=a_{k-1}}$ that depend on $x_k$. There are at most $2^{k-1}$ such restrictions, and at most $2^{2^{n-k+1}} - 2^{2^{n-k}}$ functions of $x_k, \ldots, x_n$ that depend on $x_k$. So level $k$ has at most the smaller of the two numbers. With the split at the level $k$ where $2^{n-k+1}$ is about $n - \log_2 n$, the first bound sums to $O(2^n / n)$ above the split and the second sums to $O(2^n / n)$ below it. So every function in $B_n$ has a ROBDD with $O(2^n / n)$ nodes for every order. Many functions in practice have far smaller ROBDDs: parity has $2n + 1$ nodes, and a sum of products over disjoint pairs has $2k + 2$ with a good order. Some have exponential size for every order, such as the middle output bit of a multiplier ([multiplier lower bound](/multiplier-bdd-lower-bound/)).

## Variants

- **[Complemented edges](/complemented-edges/)**: an edge can carry a negation bit. Negation is $O(1)$, and the size can drop by a factor of up to 2.
- **[Zero-suppressed BDD](/zero-suppressed-bdd/)**: a different elimination rule, which removes nodes whose high edge goes to 0. Better for sparse sets of combinations.
- **[Algebraic decision diagram](/algebraic-decision-diagram/)**: many terminal values, for functions into numbers.
- **Quasi-reduced OBDD**: only the merging rule, so every path tests all variables. Also canonical, and its levels are complete.
- **Dynamic reordering**: the order changes while the package runs, by swapping adjacent levels in place. See [sifting](/bdd-sifting/) and [variable ordering](/variable-ordering/).

## When to use it

Use a ROBDD when a program must build many Boolean functions from smaller ones and ask whether two are equal, whether one implies another, or how many models one has. Typical uses are [symbolic model checking](/symbolic-model-checking/) and [symbolic reachability](/symbolic-reachability/), [equivalence checking](/boolean-equivalence-checking/) of circuits, and counting combinatorial objects, as in Knuth's Section 7.1.4. After the ROBDD is built, many questions take linear time or less.

Do not use it when the functions have no small ROBDD for any order, as for multipliers, or when the only question is one satisfiability test. For one test, a [SAT](/sat/) solver on a CNF formula usually uses far less memory.

## Pitfalls

- **Skipping MK.** A node made without MK can duplicate a node that exists, and then EQUAL gives false for equal functions. Every node must come from MK.
- **The computed table after garbage collection.** A cache entry can point to a freed node, or a key can name a freed id that is later reused. Clear the entries that name freed nodes, or clear the whole cache, at each collection.
- **Skipped levels in counting.** An edge from level $k$ to level $k' > k + 1$ skips $k' - k - 1$ free variables. SATCOUNT must multiply by $2^{k' - k - 1}$; see [satisfy-count](/bdd-satisfy-count/).
- **Two managers.** Ids from two stores, or from two orders, cannot be compared or combined.
- **Recursion depth.** The recursive operations go down one level per call, so their depth is at most $n + 1$. With many variables, use an explicit stack.
- **A bad order.** The size can change by an exponential factor with the order. The usual cause of a BDD that does not fit in memory is the order, not the function.

## Implementations

## History

Bryant (1986) defined reduced function graphs with a fixed order of the variables. He proved that each function has a unique reduced graph, up to isomorphism, and that it has the fewest vertices among the ordered graphs of the function. He gave Reduce, Apply, Restrict, Compose and the Satisfy operations, with the costs of his Table 1. His count formula for Satisfy-count missed the factors for skipped levels; a later note on the paper gives the corrected formula. Brace, Rudell and Bryant (1990) described the package design that most later packages follow: a unique table that keeps the graph reduced at all times, so that equal functions have equal pointers, a computed table as a hash cache, the ITE operator as the main interface, and complemented edges. Rudell (1993) added dynamic reordering by sifting. Knuth (2011, Section 7.1.4) presents ROBDDs as a tool for combinatorics and gives algorithms for reduction, synthesis and counting.

## References
