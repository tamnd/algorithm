---
tag: YY3W21
kind: data-structure
slug: decision-diagram
name: Decision diagram
aliases:
- Multi-valued decision diagram
- reduced ordered decision diagram
- multi-terminal decision diagram
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: Compact graph representation of Boolean or finite-domain functions used for symbolic state sets.
model: word-ram
complexity:
  vars: {f: the number of nodes of the first argument, g: the number of nodes of the second argument, d: the largest domain size, n: the number of variables}
  time: {mk: O(d) expected, evaluate: O(n), apply: O(d·f·g) expected}
  space: {nodes: O(f)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1986
  people: [Randal E. Bryant]
  note: Bryant's reduced ordered BDDs of 1986 were extended in the early 1990s to more edges per node, more terminal values and other decomposition rules.
prereqs: [reduced-ordered-bdd, bdd-canonicity, shannon-expansion]
see_also: [binary-decision-diagram, reduced-ordered-bdd, multi-valued-decision-diagram, algebraic-decision-diagram, zero-suppressed-bdd, kronecker-functional-decision-diagram, binary-moment-diagram, symbolic-reachability]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 2 (reduced function graphs and Theorem 1) and Section 4.3 (Apply), the Boolean case that this page extends
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 8, Decision diagrams based on other decomposition rules, and Chapter 9, Integer-valued decision diagrams
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (BDD bases, ZDDs and multiterminal diagrams)
---

A decision diagram is a rooted [directed acyclic graph](/directed-acyclic-graph/) that represents a function of several discrete variables: each inner node tests one variable and has one edge per value of it, and each terminal holds an output value. The [binary decision diagram](/binary-decision-diagram/) is the case of two-valued variables and the outputs 0 and 1. With a fixed variable order and the two reduction rules, every member of the family is canonical, by the same argument as the [canonicity of reduced ordered BDDs](/bdd-canonicity/), and the same APPLY algorithm combines two diagrams in time proportional to the product of their sizes. The family includes [multi-valued decision diagrams](/multi-valued-decision-diagram/) for finite-domain variables, [algebraic decision diagrams](/algebraic-decision-diagram/) for numeric outputs, and diagrams with other node rules, such as [zero-suppressed BDDs](/zero-suppressed-bdd/).

## In plain words

A decision diagram is a flow chart for looking up an answer. Each box asks the value of one input. An input may have two values, like a switch, or more, like a dial with several positions. Each box has one arrow for each possible value. You follow the arrows for your inputs until you reach an end box, which holds the answer. The answer can be yes or no, or a number, or any other label. Equal parts of the chart are drawn once and shared. If you fix the order of the questions, remove boxes where all arrows go to the same place, and share all equal boxes, then each lookup task has exactly one chart.

## The abstract type

Let $x_1, \ldots, x_n$ be variables with finite domains $D_i = \{0, \ldots, d_i - 1\}$, and let $T$ be a set of values. A decision diagram stores functions

$$f : D_1 \times \cdots \times D_n \to T,$$

one for each root. The operations on this page are:

- TERMINAL$(t)$: the constant function with value $t$.
- MK$(i, c_0, \ldots, c_{d_i - 1})$: the function that equals $c_v$ when $x_i = v$.
- EVAL$(u, x)$: the value $f_u(x)$.
- APPLY$(\mathrm{op}, f, g)$: the function $x \mapsto \mathrm{op}(f(x), g(x))$, for any $\mathrm{op} : T \times T \to T$.
- EQUAL$(f, g)$: a comparison of two ids, by canonicity.

The members of the family differ in $D_i$, in $T$, and in the rule that says what a node means:

| diagram | domains | values $T$ | node rule |
|---|---|---|---|
| [ROBDD](/reduced-ordered-bdd/) | $\{0, 1\}$ | $\{0, 1\}$ | Shannon: $f = \bar{x} f_0 + x f_1$ |
| [MDD](/multi-valued-decision-diagram/) | finite | $\{0, 1\}$ | one child per value |
| [ADD](/algebraic-decision-diagram/), MTBDD | $\{0, 1\}$ | numbers, or any set | Shannon |
| [ZDD](/zero-suppressed-bdd/) | $\{0, 1\}$ | $\{0, 1\}$ | Shannon, but a node with $\mathrm{hi} = 0$ is removed |
| [KFDD](/kronecker-functional-decision-diagram/) | $\{0, 1\}$ | $\{0, 1\}$ | Shannon or a Davio rule, chosen per variable |
| [BMD](/binary-moment-diagram/) | $\{0, 1\}$ | integers | $f = f_0 + x (f_1 - f_0)$ |

This page and its code cover the first three rows in one structure: any finite domains, any values, and the Shannon rule with one child per value.

## Representation

A terminal is a node with a value. An inner node is a pair $(i, (c_0, \ldots, c_{d_i - 1}))$ in an array, and each child has a smaller id than its parent. A unique table maps each key to its node, as in a [BDD package](/reduced-ordered-bdd/): the key of a terminal is its value, and the key of an inner node is its variable and its tuple of children. MK applies the two rules of [reduction](/bdd-reduction-rules/), extended to many children:

- **elimination**: if all children are the same node, return that node;
- **merging**: if a node with the same key exists, return it.

A [computed table](/computed-table/) caches the results of APPLY under the key $(\mathrm{op}, f, g)$.

A variable with $d$ values can also be stored as $\lceil \log_2 d \rceil$ Boolean variables in an ordinary ROBDD. The multi-way node is the same function, but it keeps one node where the binary encoding has a small tree of nodes, and it has no codes outside the domain to handle.

## Operations

```pseudo id=main
MK(i, c_0, ..., c_{d_i − 1})
L1  if c_0 = c_1 = ... = c_{d_i − 1} then return c_0       ▷ elimination
L2  if U holds the key (i, c) then return U[i, c]          ▷ merging
L3  u ← a new node (i, c)
L4  U[i, c] ← u
L5  return u

EVAL(u, x)
L6  while u is not a terminal do
L7      u ← c_{x[var(u)]}(u)
L8  return the value of u

APPLY(op, f, g)
L9  if f and g are terminals then return TERMINAL(op(value(f), value(g)))
L10 if the cache holds (op, f, g) then return it
L11 i ← the smaller of the levels of f and g
L12 for each value v of x_i do
L13     c_v ← APPLY(op, f|x_i=v, g|x_i=v)   ▷ a child if the node tests x_i, else the node
L14 r ← MK(i, c_0, ..., c_{d_i − 1})
L15 store r in the cache under (op, f, g)
L16 return r
```

APPLY is Bryant's [APPLY](/bdd-apply/) with one recursive call per value in place of two. Since the operator acts on the terminal values only, one procedure gives sums, products, maxima and comparisons of numeric diagrams, and AND and OR of Boolean ones.

## Example

Let $x_1 \in \{0, 1, 2\}$ and $x_2 \in \{0, 1\}$, in this order, and let $f = x_1 + x_2$ and $g = \max(x_1, x_2)$, with integer values.

- $f$: the root tests $x_1$ and has three children on $x_2$, with the terminal pairs $(0, 1)$, $(1, 2)$ and $(2, 3)$. With the four terminals 0, 1, 2, 3, the diagram has 8 nodes.
- $g$: for $x_1 = 0$ the child is the node $(x_2; 0, 1)$. For $x_1 = 1$ both values of $x_2$ give 1, so the elimination rule replaces the child by the terminal 1. For $x_1 = 2$ the child is the terminal 2. So the root of $g$ has the children $(x_2; 0, 1)$, 1 and 2.
- APPLY$(+, f, g)$ splits on $x_1$. For $x_1 = 1$ it combines $(x_2; 1, 2)$ with the terminal 1 and gets $(x_2; 2, 3)$. The result has the table $0, 2, 4$ for $x_2 = 0$ and $2, 3, 5$ for $x_2 = 1$.
- APPLY$(=, f, f)$ gives the value true at every pair of terminals that it meets. The elimination rule then removes every inner node, and the result is the terminal true.

With $D_i = \{0, 1\}$ and $T = \{0, 1\}$ the structure is a ROBDD: parity of 4 variables gets $2 \cdot 4 + 1 = 9$ nodes, and $x_1 x_2 \vee x_3 x_4$ gets 6.

## Correctness

MK keeps an invariant: no inner node has all its children equal, the order goes down on each edge, and no two nodes have the same key. EVAL keeps the value $f_u(x)$ at each step. APPLY is correct by induction on the levels, because a cofactor commutes with a pointwise operator. Canonicity holds by the proof of the Boolean case: a node on level $m$ has two different children, so its function depends on $x_m$, and two nodes with the same function are on the same level, have equal cofactors, so equal children by induction, so the same key. The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

- MK hashes a key of $d_i + 1$ numbers: $O(d)$ expected time.
- EVAL makes at most $n$ steps: $O(n)$.
- APPLY runs its body at most once per pair of nodes of $f$ and $g$, thanks to the cache, and each run makes $d_i$ calls: $O(d \cdot |f| \cdot |g|)$ expected time. The result has at most $|f| \cdot |g|$ inner nodes.
- The size depends on the order, as for BDDs. For numeric values it also depends on how many distinct values occur: a diagram has one terminal for each value of the function. The function $x_1 + 2 x_2 + \cdots + 2^{n-1} x_n$ takes $2^n$ values, so its ADD has at least $2^n$ terminals for every order, while its [binary moment diagram](/binary-moment-diagram/) has $O(n)$ nodes.

## Variants

- **[Multi-valued decision diagram](/multi-valued-decision-diagram/)** (MDD): finite domains and Boolean values. Used to store sets of states whose components are small integers.
- **[Algebraic decision diagram](/algebraic-decision-diagram/)** (ADD) or multi-terminal BDD (MTBDD): Boolean variables and values in a set with operations, often the reals. Used for matrices, probabilities and costs.
- **[Zero-suppressed BDD](/zero-suppressed-bdd/)**: a different elimination rule, suited to sparse families of sets.
- **Functional decision diagrams** and **[Kronecker functional decision diagrams](/kronecker-functional-decision-diagram/)**: nodes that use the Davio expansions of the [Shannon expansion](/shannon-expansion/) page.
- **[Binary moment diagrams](/binary-moment-diagram/)**: a node splits $f$ into $f_0$ and the linear moment $f_1 - f_0$, with weights on the edges. Used to verify arithmetic circuits.
- **Edge-valued diagrams**: values on the edges are added or multiplied along the path, which shares nodes whose functions differ by a constant.

## When to use it

Use a multi-way diagram when the natural variables have more than two values, for example the local state of each component of a system. [Symbolic reachability](/symbolic-reachability/) with MDDs then keeps one level per component. Use numeric terminals when the function is a cost, a probability or a matrix entry, and the number of distinct values is small. Use a binary encoding into an ordinary [ROBDD](/reduced-ordered-bdd/) when a mature BDD package is available and the domains are powers of two.

## Pitfalls

- **Many distinct values.** An ADD has a terminal for each value of its function, so a function with many values has a large diagram, whatever the order.
- **Operator identity in the cache.** The cache key holds the operator. Two different operators with one name, or an operator with hidden state, give wrong cache hits.
- **Floating-point values.** Two values that differ by rounding error make two terminals, and canonicity is lost for the intended function. Round values to a fixed precision before TERMINAL.
- **Codes outside the domain.** In a binary encoding of a domain of size 3, the fourth code must be made a don't care or excluded, or quantifiers and counts include it.

## Implementations

## History

Bryant (1986) defined reduced ordered BDDs and the APPLY algorithm for Boolean functions. In the early 1990s several groups extended the idea. Srinivasan, Kam, Malik and Brayton (1990) used multi-valued diagrams for discrete functions. Clarke and coauthors (1993) introduced multi-terminal BDDs, and Bahar and coauthors (1993) the algebraic decision diagrams with an algebra on the values. Minato (1993) introduced zero-suppressed BDDs, Kebschull, Schubert and Rosenstiel (1992) functional decision diagrams, and Bryant and Chen (1995) binary moment diagrams. Wegener (2000, Chapters 8 and 9) surveys the decision diagrams based on other decomposition rules and the integer-valued ones.

## References
