---
tag: 73ZZQJ
kind: data-structure
slug: zero-suppressed-bdd
name: Zero-suppressed binary decision diagram
aliases:
- ZDD
- zero-suppressed decision diagram
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: An ordered decision diagram that removes nodes whose high edge goes to the empty family. It stores families of sets canonically and is small for sparse families.
model: word-ram
complexity:
  vars: {P: the number of nodes of the first argument, Q: the number of nodes of the second argument, n: the number of elements}
  time: {getnode: O(1) expected, union: O(P Q) expected, intersect: O(P Q) expected, diff: O(P Q) expected, subset0: O(P) expected, subset1: O(P) expected, change: O(P) expected, count: O(P)}
  space: {nodes: O(P)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1993
  people: [Shin-ichi Minato]
  note: Minato replaced the elimination rule of BDDs by the zero-suppression rule and gave the family algebra for combinatorial sets.
prereqs: [reduced-ordered-bdd, bdd-reduction-rules, bdd-canonicity]
see_also: [reduced-ordered-bdd, bdd-reduction-rules, bdd-canonicity, bdd-apply, exact-cover, set-cover, hypergraph, model-counting]
sources:
  - paper: doi:10.1145/157485.164890
    title: Shin-ichi Minato, Zero-suppressed BDDs for set manipulation in combinatorial problems, Proceedings of the 30th ACM/IEEE Design Automation Conference, 1993, pages 272 to 277
    locator: the zero-suppression rule, the canonical form, and the basic operations on sets of combinations
  - paper: "Shin-ichi Minato, Zero-suppressed BDDs and their applications, International Journal on Software Tools for Technology Transfer 3(2), 2001, pages 156 to 170"
    title: Zero-suppressed BDDs and their applications
    locator: the survey of the operations (offset, onset, change, union, intersection, difference, count) and of the applications
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (zero-suppressed BDDs, the family algebra, and the comparison of B(f) and Z(f))
---

A zero-suppressed binary decision diagram (ZDD) is an ordered [decision diagram](/decision-diagram/) for a family of subsets of a finite set. It uses the merging rule of [ROBDDs](/reduced-ordered-bdd/), but it replaces their elimination rule: a node is removed when its high edge goes to the empty family, not when its two children are equal. With this one change, an element that a path skips is *absent* from the set, while in a BDD a skipped variable is *free*. So a family of a few small sets out of many elements has a small ZDD, even when its BDD must spell out every absent element. ZDDs are canonical for a fixed order of the elements, and they come with a family algebra: union, intersection, difference, join, and the cofactor operations on one element. Minato (1993) introduced them, and Knuth (2011) uses them as a main tool for combinatorial enumeration.

## In plain words

A ZDD is a compact list of sets, for example the sets of items that solve a puzzle. Go through the items in a fixed order. At each node, ask whether the set contains the current item, and go left for no and right for yes. A set is listed if its path ends at the "yes" end. The trick is in what is left out. If a node would only lead to "no" when the item is present, the node is dropped, and a path that skips an item means that the item is not in the set. When most sets contain only a few items, most questions would have this form, so most nodes disappear. Equal sub-lists are stored once, and the result is the same however the family was built.

## The abstract type

The ground set is $\{1, \ldots, n\}$, ordered $1 < 2 < \cdots < n$. A ZDD node $P$ stands for a family $\mathcal{F}(P)$ of subsets. The operations are:

| operation | result |
|---|---|
| GETNODE$(v, L, H)$ | the node of $\mathcal{F}(L) \cup \{ S \cup \{v\} : S \in \mathcal{F}(H) \}$ |
| UNION, INTERSECT, DIFF$(P, Q)$ | $\mathcal{F}(P) \cup \mathcal{F}(Q)$, $\mathcal{F}(P) \cap \mathcal{F}(Q)$, $\mathcal{F}(P) \setminus \mathcal{F}(Q)$ |
| JOIN$(P, Q)$ | $\{ S \cup T : S \in \mathcal{F}(P), T \in \mathcal{F}(Q) \}$ |
| SUBSET0$(P, v)$ | $\{ S \in \mathcal{F}(P) : v \notin S \}$ (Minato's *offset*) |
| SUBSET1$(P, v)$ | $\{ S \setminus \{v\} : v \in S \in \mathcal{F}(P) \}$ (Minato's *onset*) |
| CHANGE$(P, v)$ | $\{ S \mathbin{\triangle} \{v\} : S \in \mathcal{F}(P) \}$, toggle $v$ in every set |
| COUNT$(P)$ | $\lvert \mathcal{F}(P) \rvert$ |
| EQUAL$(P, Q)$ | whether $\mathcal{F}(P) = \mathcal{F}(Q)$, by comparing ids |

A family is the same thing as a [Boolean function](/boolean-function/): $\mathcal{F}$ corresponds to its characteristic function $\chi(x) = 1$ if and only if $\{ i : x_i = 1 \} \in \mathcal{F}$. So a ZDD and a BDD can represent the same object; they differ in size.

## Representation

There are two sinks: $\bot$, the empty family $\emptyset$, and $\top$, the family $\{\emptyset\}$ that holds only the empty set. An inner node is a triple $(v, L, H)$ with $v < \mathrm{var}(L)$ and $v < \mathrm{var}(H)$, where a sink has $\mathrm{var} = n + 1$. Its family is

$$\mathcal{F}(v, L, H) = \mathcal{F}(L) \cup \{ S \cup \{v\} : S \in \mathcal{F}(H) \}.$$

The diagram is **reduced** if it follows two rules.

- **Zero-suppression rule.** No node has $H = \bot$. Such a node would mean $\mathcal{F}(L) \cup \emptyset = \mathcal{F}(L)$, so it is replaced by $L$.
- **Merging rule.** No two nodes have the same triple.

A node with $L = H$ is kept: $(v, L, L)$ is the family $\mathcal{F}(L)$ with $v$ added freely, which differs from $\mathcal{F}(L)$. GETNODE enforces both rules with a unique table, a [hash table](/hash-table/) from triples to ids, as in [hash consing](/hash-consing/). Since all nodes come from GETNODE, the whole store is reduced at all times.

## Operations

Let $\mathrm{split}(P, v)$ be $(L, H)$ if $P = (v, L, H)$, and $(P, \bot)$ if $\mathrm{var}(P) > v$. In the second case no set of $\mathcal{F}(P)$ contains $v$, which is the rule "a skipped element is absent". The binary operations recurse on the smaller top element and cache their results in a [computed table](/computed-table/).

```pseudo id=main
GETNODE(v, L, H)
L1  if H = ⊥ then                              ▷ zero-suppression rule
L2      return L
L3  if U holds (v, L, H) then return U[v, L, H]    ▷ merging rule
L4  u ← a new node (v, L, H); U[v, L, H] ← u
L5  return u

UNION(P, Q)
L6  if P = ⊥ then return Q;  if Q = ⊥ or P = Q then return P
    (return the cached result if there is one)
L7  v ← min(var(P), var(Q)); (P0, P1) ← split(P, v); (Q0, Q1) ← split(Q, v)
L8  return GETNODE(v, UNION(P0, Q0), UNION(P1, Q1))      ▷ and cache it
```

The other operations follow the same pattern.

- INTERSECT returns $\bot$ if an argument is $\bot$, $P$ if $P = Q$, and otherwise GETNODE$(v, \mathrm{INTERSECT}(P_0, Q_0), \mathrm{INTERSECT}(P_1, Q_1))$.
- DIFF returns $\bot$ if $P = \bot$ or $P = Q$, $P$ if $Q = \bot$, and otherwise GETNODE$(v, \mathrm{DIFF}(P_0, Q_0), \mathrm{DIFF}(P_1, Q_1))$.
- JOIN returns $\bot$ if an argument is $\bot$, the other argument if one is $\top$, and otherwise GETNODE$(v, \mathrm{JOIN}(P_0, Q_0), H)$ with $H = \mathrm{JOIN}(P_1, Q_1) \cup \mathrm{JOIN}(P_1, Q_0) \cup \mathrm{JOIN}(P_0, Q_1)$.
- SUBSET0, SUBSET1 and CHANGE walk down to the level of $v$. At a node $(v, L, H)$ they return $L$, $H$, and GETNODE$(v, H, L)$. At a node below $v$ they return $P$, $\bot$, and GETNODE$(v, \bot, P)$. Above $v$ they rebuild the node with GETNODE from the results for the two children.
- COUNT sets $c(\bot) = 0$, $c(\top) = 1$ and $c(v, L, H) = c(L) + c(H)$.

## Example

Let $n = 3$ and $\mathcal{F} = \{\{1, 2\}, \{2, 3\}, \{3\}\}$. The reduced ZDD has four inner nodes:

| node | element | $L$ | $H$ | family |
|---|---|---|---|---|
| $C$ | 3 | $\bot$ | $\top$ | $\{\{3\}\}$ |
| $A$ | 2 | $\bot$ | $\top$ | $\{\{2\}\}$ |
| $B$ | 2 | $C$ | $C$ | $\{\{3\}, \{2, 3\}\}$ |
| $R$ | 1 | $B$ | $A$ | $\{\{3\}, \{2, 3\}, \{1, 2\}\}$ |

With the two sinks it has 6 nodes. The path $R \xrightarrow{1} A \xrightarrow{1} \top$ reads the set $\{1, 2\}$: it skips element 3, so 3 is absent. Node $B$ has equal children and is kept, because it means "2 may or may not be added".

**UNION trace.** Build $\mathcal{F}$ as the union of $P = \{\{1, 2\}\} = (1, \bot, A)$ and $Q = \{\{2, 3\}, \{3\}\} = B$. Line L7 takes $v = \min(1, 2) = 1$, with $\mathrm{split}(P, 1) = (\bot, A)$ and $\mathrm{split}(Q, 1) = (B, \bot)$, since $Q$ does not contain 1. The recursive calls return $\mathrm{UNION}(\bot, B) = B$ and $\mathrm{UNION}(A, \bot) = A$ at line L6. Line L8 calls GETNODE$(1, B, A)$, which returns $R$.

**COUNT.** $c(C) = 1$, $c(A) = 1$, $c(B) = 2$, and $c(R) = 2 + 1 = 3$.

**Size against BDDs.** The table gives the sizes with the sinks, the ZDD size $Z$ and the size $B$ of the reduced OBDD of the characteristic function with the same order. The values were measured by the implementation.

| family | $Z$ | $B$ |
|---|---|---|
| $\{\{1, 2\}, \{2, 3\}, \{3\}\}$ | 6 | 6 |
| the $n$ singletons $\{i\}$ | $n + 2$ | $2n + 1$ |
| all 2-element subsets | $2n$ | $3n - 2$ |
| a family of 4 pairs, $n = 8$ | 10 | 25 |
| the same 4 pairs, $n = 12$ | 10 | 29 |
| all $2^n$ subsets | $n + 1$ | 1 |
| $\{\emptyset\}$ | 1 | $n + 2$ |

Sparse families favour ZDDs; families closed under adding elements favour BDDs.

## Correctness

The main fact is **canonicity**: for a fixed order, each family has exactly one reduced ZDD, so EQUAL is an id comparison. The proof goes by the smallest element. If $(v, L, H)$ is reduced, then $H \ne \bot$, so some set of the family contains $v$, and every other element of every set is larger than $v$. So $v$ is the smallest element used by the family, and $L$ and $H$ are the families SUBSET0 and SUBSET1 at $v$. These are determined by the family, so by induction the children are the same nodes, and the merging rule gives the same node. The sinks are the only nodes for $\emptyset$ and $\{\emptyset\}$.

Each operation is correct by the identity $\mathcal{F}(P) = \mathcal{F}(P_0) \cup \{ S \cup \{v\} : S \in \mathcal{F}(P_1) \}$ for $\mathrm{split}(P, v) = (P_0, P_1)$. For UNION, the sets without $v$ of the result are those of $P_0$ or $Q_0$, and the sets with $v$ come from $P_1$ or $Q_1$.

**Size relation.** For every family, $Z \le n B + 2$ and $B \le n Z + 2$. Each ZDD node is fixed by a pair (an element $k$, a BDD node $w$ with $k \le \mathrm{var}(w)$), and each BDD inner node by a pair (an element $j$, a ZDD node $z$ with $j \le \mathrm{var}(z)$). The family of all subsets ($Z = n + 1$, $B = 1$) and the family $\{\emptyset\}$ ($Z = 1$, $B = n + 2$) show that the factor $n$ is reached in both directions, up to constant terms. The full proofs of these claims are in [the proof file](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| GETNODE | $O(1)$ expected | one hash lookup |
| UNION, INTERSECT, DIFF | $O(\lvert P \rvert \cdot \lvert Q \rvert)$ expected | one call per pair of nodes, with the cache |
| SUBSET0, SUBSET1, CHANGE | $O(\lvert P \rvert)$ expected | one call per node above $v$ |
| JOIN | no bound of the form $O(\lvert P \rvert \cdot \lvert Q \rvert)$ | it calls UNION on intermediate results |
| COUNT | $O(\lvert P \rvert)$ additions | the counts have at most $n + 1$ bits |
| EQUAL | $O(1)$ | canonicity |
| space | $O(\text{nodes})$ | the store, the unique table and the cache |

The recursion depth is at most $n + 1$, because each call goes down at least one element.

## Variants

- **[ROBDDs](/reduced-ordered-bdd/).** The same merging rule with the other elimination rule. Better for functions where skipped variables should be free, such as the constraints of a circuit.
- **Edge attributes.** The [complemented edges](/complemented-edges/) of BDDs do not carry over directly, since the complement of a family depends on the ground set. Minato's packages use an attribute that toggles whether the empty set is in the family.
- **Chain reductions.** Bryant's chain-reduced BDDs and ZDDs (2018) merge chains of nodes of consecutive elements, and so remove most of the factor $n$ between $Z$ and $B$.
- **ZDDs for unate cube sets.** Minato's cube set algebra stores sums of products, with two elements per variable, and supports algebraic division of covers.
- **[MDDs](/multi-valued-decision-diagram/) and other diagrams** apply the same ideas with more than two branches per node.

## When to use it

Use a ZDD for families of sparse sets: the solutions of an [exact cover](/exact-cover/) problem, the paths or matchings of a graph, the edges of a [hypergraph](/hypergraph/), the minimal solutions of a [set cover](/set-cover/) instance, frequent itemsets in data mining, and sums of products in logic synthesis. Knuth's Section 7.1.4 builds ZDDs for families with billions of members and counts them with COUNT. If the sets in the family are dense, or the family is defined by constraints that leave most variables free, a BDD is usually smaller.

## Pitfalls

- **The meaning of a skipped element.** It is absent in a ZDD and free in a BDD. Code that converts between the two, or a COUNT that multiplies by powers of 2 for skipped levels, is wrong for ZDDs.
- **The ground set is part of the meaning of some operations.** The complement of a family, and the BDD of its characteristic function, depend on $n$. Adding an element that no set uses does not change the ZDD, but it changes the BDD.
- **Keeping nodes with equal children.** A ZDD must keep $(v, L, L)$. An implementation that also applies the BDD elimination rule computes a different family.
- **The order.** As for BDDs, the size can change by an exponential factor with the order of the elements.
- **The cache after reordering or garbage collection.** Cached results must be cleared when the nodes that they name are freed.

## Implementations

## History

Minato (1993) introduced zero-suppressed BDDs for sets of combinations in combinatorial problems, with the operations offset, onset, change, union, intersection, difference and count, and he later used them for cube set algebra in logic synthesis. Knuth's Section 7.1.4 (2011) made them a main tool for exact enumeration, presented the family algebra with the join, and compared $B(f)$ and $Z(f)$. Bryant (2018) proposed chain reductions that combine the strengths of BDDs and ZDDs.

## References
