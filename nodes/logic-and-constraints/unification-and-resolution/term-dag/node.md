---
tag: 9PFAX5
kind: data-structure
slug: term-dag
name: Term DAG
aliases:
- term graph
- shared term DAG
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Term representation with shared subterms, enabling efficient unification.
model: word-ram
complexity:
  vars: {k: the arity of a node, N: the size of a tree term, D: the number of nodes, E: the number of child edges}
  time: {make_node: O(k), intern: O(N), equal: O(1), tree_size: O(D + E)}
  space: {extra: O(D + E)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [term, directed-acyclic-graph, hash-table]
see_also: [hash-consing, expression-dag, paterson-wegman-unification, martelli-montanari-unification, term-graph-rewriting, substitution, unification-problem]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.8, Unification of term graphs (terms as directed acyclic graphs with shared subterms, and the exponential example)
  - paper: "M. S. Paterson and M. N. Wegman, Linear unification, Journal of Computer and System Sciences 16(2), 1978, pages 158 to 167"
    locator: the representation of the input terms as a directed acyclic graph with one node per variable, on which the algorithm runs in linear time
  - paper: doi:10.1145/357162.357169
    title: Alberto Martelli and Ugo Montanari, An efficient unification algorithm, ACM Transactions on Programming Languages and Systems 4(2), 1982, pages 258 to 282
    locator: the shared representation of terms and multiequations used by the efficient algorithm
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (term DAGs and efficient syntactic unification)
---

A **term DAG** stores first-order [terms](/term/) as a directed acyclic graph in which equal subterms are one node. A term with repeated parts, such as $f(g(x, x), g(x, x))$, keeps one node for $g(x, x)$ and one for $x$. With maximal sharing, built by [hash-consing](/hash-consing/), two nodes are equal terms exactly when they are the same node, so equality is a pointer comparison. A term DAG can be exponentially smaller than the tree it stands for. This is why the linear [Paterson-Wegman](/paterson-wegman-unification/) and almost linear [union-find](/martelli-montanari-unification/) unification algorithms work on term DAGs, and why the exponential blow-up of [Robinson's algorithm](/robinson-unification/) disappears with sharing.

## In plain words

A term is a tree of symbols. Often the same branch appears many times. Writing it out each time wastes space, and in unification the copies can double again and again, until the tree is far too large to store.

A term DAG writes each distinct branch once and points to it from every place where it is used. To build it, keep a table of the branches made so far. Before making a new branch, look up its symbol and its parts in the table. If the same branch is already there, reuse it. Then the same branch always has the same address, so checking whether two branches are equal takes one comparison.

## The abstract type

Notation: $D$ is the number of nodes, $E$ the number of child edges, $N$ the size of a tree term and $k$ the arity of a node. A term DAG holds a set of first-order terms over a signature $\Sigma$ and variables $V$. Its operations:

- `make_node(f, (c₁, …, cₖ))`: the node of $f(\mathrm{term}(c_1), \ldots, \mathrm{term}(c_k))$, made if it is new.
- `var(x)`: the node of the variable $x$.
- `intern(t)`: the node of a tree term $t$.
- `symbol(i)`, `children(i)`, `is_var(i)`: read a node.
- `equal(i, j)`: whether two nodes stand for the same term; with maximal sharing this is $i = j$.
- `tree_size(i)`: the number of symbols of the tree that $i$ stands for.
- `unfold(i)`: the tree term of $i$.

A **term graph** in general may share some subterms and not others, and may even have cycles. This page treats the acyclic, maximally shared form, which is the one that unification algorithms build.

## Representation

Node $i$ has a symbol, a variable flag and a tuple of children. Its **key** is $(\mathrm{var}, x)$ for a variable and $(\mathrm{app}, f, (c_1, \ldots, c_k))$ for a function node. A [hash table](/hash-table/) $H$ maps each key to its node. Nodes are numbered in order of creation.

**Invariant.** (H1) $H$ maps the key of each node to that node and has no other entries. (H2) The children of node $i$ have numbers less than $i$. So the numbering is a [topological order](/topological-sort/) of the DAG, from leaves to roots.

Unification algorithms add fields to each node: the parent list for the [Paterson-Wegman algorithm](/paterson-wegman-unification/), a union-find parent for the [Martelli-Montanari algorithm](/martelli-montanari-unification/), or a binding for a variable node.

## Operations

```pseudo id=main
MAKE-NODE(f, c₁, …, cₖ)                  ▷ the node of f(term(c₁), …, term(cₖ))
L1  key ← (f, c₁, …, cₖ)                 ▷ (var, x) for a variable x
L2  if key ∈ H then return H[key]
L3  i ← a new node with symbol f and children c₁, …, cₖ
L4  H[key] ← i
L5  return i

INTERN(t)                                ▷ the node of the tree term t
L6  if t is a variable x then return MAKE-NODE(var, x)
L7  return MAKE-NODE(f, INTERN(t₁), …, INTERN(tₖ))   ▷ t = f(t₁, …, tₖ)
```

TREE-SIZE computes $z(i) = 1 + \sum_l z(c_l)$ for all nodes in increasing order of number, which (H2) allows. UNFOLD rebuilds the tree from the definition of $\mathrm{term}$. The time bounds for MAKE-NODE and INTERN are expected bounds, under the usual assumption on the hash function. The Python implementation runs INTERN in postorder with an explicit stack, so deep terms such as long lists do not overflow the call stack.

## Example

Intern $t = f(g(x, x), g(x, x), x)$.

| call | key | result |
|---|---|---|
| INTERN($x$) | $(\mathrm{var}, x)$ | new node 0 |
| INTERN($x$) | $(\mathrm{var}, x)$ | found node 0 |
| MAKE-NODE($g$, 0, 0) | $(g, 0, 0)$ | new node 1 |
| INTERN($g(x, x)$) again | $(g, 0, 0)$ | found node 1 |
| INTERN($x$) | $(\mathrm{var}, x)$ | found node 0 |
| MAKE-NODE($f$, 1, 1, 0) | $(f, 1, 1, 0)$ | new node 2 |

The DAG has 3 nodes, while the tree has 8 symbols: $z(0) = 1$, $z(1) = 1 + 1 + 1 = 3$, $z(2) = 1 + 3 + 3 + 1 = 8$.

**Exponential compression.** Let $t_0 = x$ and $t_i = g(t_{i-1}, t_{i-1})$. The tree $t_n$ has $2^{n+1} - 1$ symbols, and its DAG has $n + 1$ nodes. This is the shape of the mgu in the [exponential example of unification](/robinson-unification/), where $x_i$ is bound to $t_i$. On the DAG, the binding of $x_i$ is one pointer to the node of $g(x_{i-1}, x_{i-1})$.

## Correctness

(H1) and (H2) hold for the empty DAG, and MAKE-NODE keeps them: it adds a node only when its key is new, and its children already exist, so they have smaller numbers. With the invariant, two nodes stand for the same term exactly when they are the same node. The proof is by induction on the larger number: equal variable terms have the same key, and equal function terms have the same symbol and, by induction on the smaller child numbers, the same children, so the same key. So after interning a set of terms, the nodes match the distinct subterms one to one. The full proof is below.

## Complexity

- **MAKE-NODE.** One hash of a key with $k$ children and one lookup: $O(k)$ expected time.
- **INTERN.** One MAKE-NODE for each symbol occurrence of the tree: $O(N)$ expected time for a tree of $N$ symbols, with each child counted once.
- **Equality.** $O(1)$ by comparing node numbers. On trees, equality costs time linear in the size.
- **TREE-SIZE.** $O(D + E)$ for all nodes at once. The result can be exponential in $D$, so it needs big integers in general.
- **UNFOLD.** Linear in the size of the output tree, which can be exponential in $D$.
- **Space.** $O(D + E)$ for the nodes and the table.

With a balanced search tree in place of the hash table, MAKE-NODE takes $O(k \log D)$ time in the worst case, with no assumption on hashing.

## Variants

- **Partial sharing.** Many systems share only what arises naturally, for example the subterms that a substitution inserts by pointer. Equality is then not a pointer test.
- **Structure sharing and structure copying.** Early Prolog systems represented an instance of a clause by a pointer to the clause and an environment of bindings (structure sharing, Boyer and Moore). The [Warren abstract machine](/warren-abstract-machine/) copies terms to the heap instead, and shares only by pointers to the bindings.
- **Cyclic term graphs.** Allowing cycles gives a finite representation of infinite rational trees. Prolog systems without the [occurs check](/occurs-check/) build such graphs.
- **Garbage collection.** A hash-consing table with weak references lets unused nodes be reclaimed.
- **Term graph rewriting.** [Term graph rewriting](/term-graph-rewriting/) rewrites the DAG in place, so that a duplicated argument is evaluated once.
- **Expression DAGs.** Compilers use the same structure, the [expression DAG](/expression-dag/), to find common subexpressions.

## When to use it

Use a term DAG when terms repeat subterms, when substitutions copy large terms many times, or when equality tests are frequent. It is the input format of linear-time unification and congruence closure, and theorem provers use shared terms to save memory. Plain trees are simpler and faster when terms are small and rarely compared, and when terms are changed in place, which shared nodes do not allow.

## Pitfalls

- **Destructive updates.** A shared node belongs to every term that points to it. Changing it in place changes all those terms. Bindings must live in separate fields or tables.
- **One node per variable.** Unification algorithms on DAGs need each variable to be a single node. Two nodes for the same variable break them.
- **Size counters overflow.** The tree size can be exponential in the number of nodes, so fixed-width counters can overflow.
- **Hash keys of children.** The key must use the child node numbers, not the child terms. Hashing the child terms costs time linear in the tree size and loses the benefit.

## Implementations

## History

Sharing common subexpressions goes back to early compilers, and the technique of looking up each new node in a table before making it is known as hash-consing in Lisp systems. In unification, Huet's thesis (1976) and Paterson and Wegman (1978) used shared term graphs to get almost linear and linear time. Martelli and Montanari (1982) used shared terms in their efficient algorithm. Baader and Nipkow (1998) give the exponential example and the unification of term graphs as a textbook topic.

## References
