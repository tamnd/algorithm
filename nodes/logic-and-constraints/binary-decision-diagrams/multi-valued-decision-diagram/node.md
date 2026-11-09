---
tag: C9XT2M
kind: data-structure
slug: multi-valued-decision-diagram
name: Multi-valued decision diagram
aliases:
- MDD
- multi-valued BDD
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: An ordered decision diagram whose nodes branch on variables with finite domains of any size. Reduced MDDs are canonical, and they store the solution sets of finite-domain constraints.
model: word-ram
complexity:
  vars: {f: the number of nodes of the first argument, g: the number of nodes of the second argument, d: the largest domain size, n: the number of variables}
  time: {mk: O(d) expected, apply: O(f g d) expected, evaluate: O(n), count: O(f d)}
  space: {nodes: O(f d)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1990
  people: [Arvind Srinivasan, Timothy Kam, Sharad Malik, Robert K. Brayton]
  note: Srinivasan, Kam, Malik and Brayton extended BDD algorithms to discrete functions of multi-valued variables; Kam and others later gave the theory of MDDs.
prereqs: [reduced-ordered-bdd, bdd-apply, constraint-satisfaction-problem]
see_also: [reduced-ordered-bdd, algebraic-decision-diagram, zero-suppressed-bdd, constraint-satisfaction-problem, bdd-apply, model-counting, decision-diagram, generating-all-permutations]
sources:
  - paper: "Arvind Srinivasan, Timothy Kam, Sharad Malik, Robert K. Brayton, Algorithms for discrete function manipulation, Proceedings of the IEEE International Conference on Computer-Aided Design (ICCAD), 1990, pages 92 to 95"
    title: Algorithms for discrete function manipulation
    locator: the multi-valued decision diagram, its reduction and the apply algorithm
  - paper: "Timothy Kam, Tiziano Villa, Robert K. Brayton, Alberto L. Sangiovanni-Vincentelli, Multi-valued decision diagrams, theory and applications, Multiple-Valued Logic 4(1/2), 1998, pages 9 to 62"
    title: Multi-valued decision diagrams, theory and applications
    locator: the canonical form, the operations, and the encoding by BDDs
  - paper: "Henrik Reif Andersen, Tarik Hadzic, John N. Hooker, Peter Tiedemann, A constraint store based on multivalued decision diagrams, Principles and Practice of Constraint Programming (CP 2007), LNCS 4741, pages 118 to 132"
    title: A constraint store based on multivalued decision diagrams
    locator: relaxed MDDs as a constraint store and propagation through MDDs
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the encoding of multi-valued variables by bits, in the text and exercises)
---

A multi-valued decision diagram (MDD) is an ordered [decision diagram](/decision-diagram/) in which a node tests a variable with a finite domain $\{0, 1, \ldots, d_i - 1\}$ and has one outgoing edge for each value. Its sinks hold the values of the function, so it represents a function $f : D_1 \times \cdots \times D_n \to R$. With $d_i = 2$ and $R = \{0, 1\}$ it is a [reduced ordered BDD](/reduced-ordered-bdd/), and with $d_i = 2$ and many sink values it is an [algebraic decision diagram](/algebraic-decision-diagram/). The two reduction rules of BDDs carry over: drop a node whose children are all equal, and merge equal nodes. Reduced MDDs are canonical for a fixed order, and apply, counting and evaluation work as for BDDs, with a factor $d$ for the branching. MDDs represent the solution sets of [constraint satisfaction problems](/constraint-satisfaction-problem/) over finite domains, configuration spaces, and the states of systems with multi-valued components.

## In plain words

Picture a guide that asks multiple-choice questions in a fixed order, such as "which colour is item 1: red, green or blue?". Each answer leads to the next question, and the last step gives the result. Two questions that would lead to the same result for every answer are merged into one, and a question whose answers all lead to the same place is skipped. Then each function has exactly one guide. A diagram of all ways to give three items three different colours needs only one box for each set of colours used so far, not one for each partial colouring. Counting the solutions, combining two diagrams, and checking whether two diagrams are equal all take time in the size of the diagrams.

## The abstract type

Variable $x_i$ has the domain $D_i = \{0, \ldots, d_i - 1\}$ with $d_i \ge 1$, and the order is $x_1, \ldots, x_n$. A node $u$ stands for a function $f_u : D_1 \times \cdots \times D_n \to R$.

| operation | result |
|---|---|
| CONST$(c)$ | the constant function $c$ |
| MK$(v, (c_0, \ldots, c_{d_v - 1}))$ | the function equal to $f_{c_j}$ where $x_v = j$ |
| APPLY$(\mathrm{op}, f, g)$ | $x \mapsto \mathrm{op}(f(x), g(x))$ |
| EVALUATE$(f, x)$ | $f(x)$ |
| COUNT$(f, r)$ | $\lvert \{ x : f(x) = r \} \rvert$ |
| FROM-TABLE$(T)$ | the node of the function with the value table $T$ |
| EQUAL$(f, g)$ | whether $f = g$, by comparing ids |

The decomposition is the multi-valued Shannon expansion

$$f = \sum_{j=0}^{d_v - 1} [x_v = j] \cdot f|_{x_v = j},$$

where $[x_v = j]$ is 1 if $x_v = j$ and 0 otherwise. Exactly one term is active for each input.

## Representation

A sink $(n + 1, c)$ stores one value $c$. An inner node $(v, (c_0, \ldots, c_{d_v - 1}))$ has one child per value, and every child tests a later variable or is a sink. MK enforces two rules with a unique table, a [hash table](/hash-table/) keyed by the variable and the tuple of children:

- **Elimination.** If all children are equal, return that child.
- **Merging.** If the key is stored, return the stored node.

An MDD can also be encoded as a BDD by writing each $x_i$ with $\lceil \log_2 d_i \rceil$ bits. The BDD needs extra nodes for the binary choices inside one variable, and codes outside the domain must be given a value; native MDDs avoid both issues.

## Operations

Let $\mathrm{child}(u, v, j)$ be the $j$-th child of $u$ if $u$ tests $x_v$, and $u$ itself if $u$ tests a later variable or is a sink.

```pseudo id=main
MK(v, (c_0, ..., c_{d_v − 1}))
L1  if c_0 = c_1 = ... = c_{d_v − 1} then return c_0        ▷ elimination
L2  if U holds (v, c) then return U[v, c]                    ▷ merging
L3  otherwise make a new node u with U[v, c] ← u, and return u

EVALUATE(u, x)
L4  while u is not a sink do
L5      u ← the child of u for the value x[var(u)]
L6  return the value of u

APPLY(op, f, g)                  ▷ results are cached under (op, f, g)
L7  if f and g are sinks then return CONST(op(value(f), value(g)))
L8  v ← min(var(f), var(g))
L9  for j ← 0 to d_v − 1: r_j ← APPLY(op, child(f, v, j), child(g, v, j))
L10 return MK(v, (r_0, ..., r_{d_v − 1}))
```

**COUNT$(u, r)$** goes up from the sinks. A sink gets $\prod_i d_i$ if its value is $r$ and 0 otherwise. An inner node of $x_v$ gets $\frac{1}{d_v} \sum_j c(\text{child}_j)$. The division is exact, because the children do not depend on $x_v$, so each child's count splits evenly over the $d_v$ values of $x_v$. FROM-TABLE builds the diagram bottom-up, one variable per round, as BUILD does for ROBDDs.

## Example

Let $n = 3$ with $d_1 = d_2 = d_3 = 3$, and let $f(x) = 1$ if $x_1, x_2, x_3$ are all different, and 0 otherwise. The solutions are the 6 permutations of $\{0, 1, 2\}$. A node is fixed by the set of values used so far:

| level | nodes | children |
|---|---|---|
| $x_1$ | $N_\emptyset$ | $N_{\{0\}}, N_{\{1\}}, N_{\{2\}}$ |
| $x_2$ | $N_{\{0\}}, N_{\{1\}}, N_{\{2\}}$ | for $N_{\{0\}}$: $0, N_{\{0,1\}}, N_{\{0,2\}}$ |
| $x_3$ | $N_{\{0,1\}}, N_{\{0,2\}}, N_{\{1,2\}}$ | for $N_{\{0,1\}}$: $0, 0, 1$ |

That is 7 inner nodes and 2 sinks, so 9 nodes. In general the all-different function of $k$ variables with $k$ values has $2^k + 1$ nodes for $k > 1$, one per proper subset of the values plus the sinks, while its decision tree has $k!$ leaves; see [generating all permutations](/generating-all-permutations/).

**COUNT$(N_\emptyset, 1)$.** The sink 1 gets $27$. Each node on level $x_3$ gets $(0 + 0 + 27)/3 = 9$. $N_{\{0\}}$ gets $(0 + 9 + 9)/3 = 6$, and so do the other two. The root gets $(6 + 6 + 6)/3 = 6$.

**APPLY trace.** Let $g = [x_1 = 0]$, the node $(x_1, (1, 0, 0))$, and compute APPLY$(\min, f, g)$, the permutations with $x_1 = 0$.

- Line L8 takes $v = 1$. For $j = 0$ it calls APPLY$(\min, N_{\{0\}}, 1)$. That call takes $v = 2$, and the minimum with the constant 1 leaves each child unchanged: the calls on $N_{\{0,1\}}$ and $N_{\{0,2\}}$ rebuild these nodes, and line L2 finds them. So it returns $N_{\{0\}}$.
- For $j = 1, 2$ the calls APPLY$(\min, N_{\{j\}}, 0)$ return the sink 0, by line L1 at every level.
- Line L10 returns the new node $(x_1, (N_{\{0\}}, 0, 0))$. COUNT gives $(6 + 0 + 0)/3 = 2$: the permutations 012 and 021.

## Correctness

The proofs are those of ROBDDs and ADDs, with $d_v$ children. **Canonicity**: going up from the sinks, every inner node depends on its variable, since its children are not all equal and, by induction, distinct nodes have distinct functions; and two nodes with the same function start on the same level and have the same children, so the merging rule makes them one node. **APPLY** is correct by the expansion: at $x_v = j$, the result is $\mathrm{op}(f|_{x_v = j}, g|_{x_v = j})$, which line L9 computes. **COUNT** is correct because the children of a node of $x_v$ do not depend on $x_v$. The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| CONST | $O(1)$ expected | one hash lookup |
| MK | $O(d_v)$ expected | hashing the tuple of children |
| APPLY$(\mathrm{op}, f, g)$ | $O(\lvert f \rvert \cdot \lvert g \rvert \cdot d)$ expected | each pair of nodes once, each with up to $d$ children |
| EVALUATE | $O(n)$ | one path |
| COUNT | $O(\lvert f \rvert \cdot d)$ arithmetic operations | the numbers have up to $\sum_i \log_2 d_i$ bits |
| FROM-TABLE | $O(\prod_i d_i)$ expected | linear in the table |
| space | $O(\lvert f \rvert \cdot d)$ | the child tuples |

Here $d = \max_i d_i$, and $\lvert f \rvert$ counts the nodes reachable from $f$.

## Variants

- **[ROBDDs](/reduced-ordered-bdd/) and [ADDs](/algebraic-decision-diagram/)** are the binary cases.
- **MDDs with edge labels on sets of values.** In constraint programming, an edge may carry a set or an interval of values, which shortens wide nodes.
- **Relaxed and restricted MDDs.** A relaxed MDD merges nodes that are not equal, so it over-approximates the solution set within a width limit; a restricted MDD drops nodes, so it under-approximates it. Andersen, Hadzic, Hooker and Tiedemann (2007) used relaxed MDDs as a constraint store, and they are the basis of decision-diagram methods for discrete optimization.
- **Multi-valued [ZDDs](/zero-suppressed-bdd/)** suppress nodes whose non-zero values all lead to the empty set.
- **Encoded MDDs.** Store each variable with $\lceil \log_2 d_i \rceil$ bits in a BDD package, which reuses the tools of BDDs at the cost of extra nodes.

## When to use it

Use MDDs when the variables have natural finite domains: product configuration, where the MDD of all valid configurations answers queries in time linear in its size; [CSPs](/constraint-satisfaction-problem/), where an MDD can store a table constraint compactly or propagate several constraints together; the reachable states of systems with multi-valued components, as in symbolic model checking of Petri nets with saturation; and multi-valued logic synthesis. If the domains are small and a BDD package is at hand, an encoding into bits can be enough.

## Pitfalls

- **Wide nodes.** A node of a variable with a large domain stores $d_i$ children even if most go to the sink 0. Sparse child lists or edge labels with value sets save space.
- **Elimination needs all children equal.** A node in which only some children are equal must stay; this is the only redundancy rule.
- **Skipped levels in counting.** An edge can skip variables. The method above handles this because each sink starts with the full product $\prod_i d_i$ and each node divides by its own domain only. A method that multiplies by $d_i$ for each skipped level, as in [BDD satisfy-count](/bdd-satisfy-count/), gives the same result, but mixing the two methods counts wrong.
- **The order.** As for BDDs, the size can change by an exponential factor with the variable order.

## Implementations

## History

Srinivasan, Kam, Malik and Brayton (1990) extended the algorithms of BDDs to discrete functions of multi-valued variables, with the MDD as the data structure. Kam, Villa, Brayton and Sangiovanni-Vincentelli (1998) gave the theory of MDDs, their canonical form and their operations. Miner and Ciardo used MDDs for the state spaces of Petri nets, with the saturation method for reachability. In constraint programming, Andersen, Hadzic, Hooker and Tiedemann (2007) introduced relaxed MDDs as a constraint store, and Bergman, Ciré, van Hoeve and Hooker developed MDD-based methods for discrete optimization in the following years.

## References
