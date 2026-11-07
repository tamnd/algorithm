---
tag: 46Z0DH
kind: data-structure
slug: expression-dag
name: Expression DAG
aliases:
- shared expression graph
- hash-consed expression
- value-numbered expression DAG
area: algebra/computer-algebra
level: core
summary: Expression representation where shared subexpressions are stored once.
implements: [expression]
prereqs: [expression-tree, directed-acyclic-graph, hash-consing, hash-table]
see_also: [term-dag, straight-line-program, e-graph, memoization, topological-sort, canonical-form, expression-swell, automatic-differentiation]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 6.1.1 (directed acyclic graphs for expressions) and Section 6.1.2 (the value-number method for constructing DAGs)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 3 (normal forms and algebraic representations), the representation of expressions with shared subexpressions
  - paper: "Andrei P. Ershov, On programming of arithmetic operations, Communications of the ACM 1(8), 3-6, 1958"
    locator: the use of a hash table to find a previously computed identical operation
  - paper: "Eiichi Goto, Monocopy and associative algorithms in an extended Lisp, Technical Report 74-03, Information Science Laboratory, University of Tokyo, 1974"
    locator: hash consing, the monocopy representation of list structures
---

An expression DAG stores a formula as a directed acyclic graph in which every distinct subexpression is a single node. A node is a constant, a symbol, or an operator with edges to its operand nodes; a subexpression that occurs many times is pointed to many times but stored once. New nodes are made through a [hash table](/hash-table/) keyed by the operator and the child nodes, a technique called [hash consing](/hash-consing/) or value numbering, so building an expression that already exists returns the old node. Then syntactic equality is one comparison of node identifiers, and evaluation, substitution and differentiation cost $O(m)$ for $m$ distinct nodes, while the unfolded [expression tree](/expression-tree/) can have $2^{m}$ nodes.

## In plain words

In a long formula, the same piece often turns up many times. A tree writes the piece out again at each place. A DAG writes it once, gives it a number, and lets every place that uses it refer to that number.

To keep this up, the store keeps an index of every piece it has made, listed by its operator and the numbers of its parts. Before it makes a new piece, it looks it up in the index. If the piece is already there, it hands back the old number. So two pieces are the same formula exactly when they have the same number. Any work on a piece, such as finding its value, is done once and reused at each place.

## The abstract type

The DAG implements the [symbolic expression](/expression/) type with the same operations as the [expression tree](/expression-tree/): the constructors `const`, `sym`, `add`, `sub`, `mul` and `power` (with a constant integer exponent $k \ge 0$); `eval` at an environment $\rho$; `subs`$(e, x, r)$; `diff`$(e, x)$; and `equal`. It adds `dag_size`, the number of distinct nodes reachable from a node, and `tree_size`, the number of nodes of the unfolded tree. Expressions are handles, the integer identifiers of nodes in one store $D$.

## Representation

The store $D$ holds three parallel arrays, `op`, `val` and `kids`, indexed by the node identifier, and a hash table `table` from keys $(\text{op}, \text{val}, \text{kids})$ to identifiers. The invariant is:

> **(H)** The table maps the key of node $i$ to $i$, for each $i$, and has no other entries. So no two nodes have the same key. Every child identifier of node $i$ is less than $i$. Leaves and operators have the arities of the [expression tree](/expression-tree/) page, and the second child of a power is a constant integer $k \ge 0$.

The second clause makes the identifiers a [topological order](/topological-sort/): children come before parents, which is why there can be no cycle. The first clause, together with the second, gives the central fact of the structure:

> two nodes are equal as unfolded trees if and only if they have the same identifier.

The proof is by induction on the larger identifier, and is in the proof file below. Constants are stored as reduced fractions, so $2/4$ and $1/2$ are one node.

## Operations

The main block is the constructor that every other operation uses. It is the whole of hash consing.

```pseudo id=main
MAKE(D, op, val, kids)
L1  key ← (op, val, kids)
L2  if key ∈ D.table then return D.table[key]
L3  i ← the number of nodes of D; append op, val, kids to the arrays of D
L4  D.table[key] ← i
L5  return i
```

Line L2 is the lookup that finds an existing node. Lines L3 and L4 add a node and record it. Since `kids` holds identifiers that already exist, they are less than the new $i$, so (H) is kept.

The walks visit the distinct nodes reachable from the root in increasing identifier order, which puts children before parents, and keep one result per node in a memo table, as in [memoization](/memoization/).

```pseudo id=eval
EVAL(D, e, ρ)
E1  for each node u reachable from e, in increasing identifier order do
E2      if u is a constant c then v[u] ← c
E3      else if u is a symbol s then v[u] ← ρ(s)
E4      else v[u] ← v[u.left] u.op v[u.right]
E5  return v[e]
```

SUBS and DIFF have the same shape. SUBS sets $R[u] \leftarrow r$ for the symbol $x$, $R[u] \leftarrow u$ for other leaves, and $R[u] \leftarrow \text{MAKE}(u.op, R[u.left], R[u.right])$ otherwise. DIFF applies the sum, product and power rules of the [expression tree](/expression-tree/) page through MAKE and the smart constructors that fold $0$ and $1$. Because they build through MAKE, their results are hash-consed too, and they share nodes with the input. `tree_size` uses the same walk with $t[u] = 1 + \sum t[\text{child}]$. `equal`$(a, b)$ returns $a = b$.

## Example

Build $e = (x + y)(x + y) + (x + y)$ in an empty store, and then build $x + y$ a second time.

| call | key | line | result | nodes after |
|---|---|---|---|---|
| sym $x$ | (sym, $x$, ()) | L3 to L5 | 0 | 1 |
| sym $y$ | (sym, $y$, ()) | L3 to L5 | 1 | 2 |
| add(0, 1) | (+, -, (0, 1)) | L3 to L5 | 2 | 3 |
| mul(2, 2) | ($\times$, -, (2, 2)) | L3 to L5 | 3 | 4 |
| add(3, 2) | (+, -, (3, 2)) | L3 to L5 | 4 | 5 |
| sym $x$ | (sym, $x$, ()) | L2 | 0 | 5 |
| sym $y$ | (sym, $y$, ()) | L2 | 1 | 5 |
| add(0, 1) | (+, -, (0, 1)) | L2 | 2 | 5 |

The second $x + y$ makes no node: line L2 finds each key and returns node 2, so `equal` of the two copies is the test $2 = 2$. The DAG of $e$ has 5 nodes, while the tree has 11. EVAL at $x = 1$, $y = 2$ visits nodes 0 to 4 once each and computes $v = 1, 2, 3, 9, 12$, so $e = 12$. DIFF$(e, x)$ is $2(x + y) + 1$ in value, and equals 7 there.

**Repeated squaring.** Start from $u_0 = x + 1$ and set $u_{j+1} = u_j \cdot u_j$. After 40 steps the DAG has 43 nodes, while the tree has $2^{42} - 1$ nodes, and EVAL at $x = -2$ returns 1 after 43 visits. The test file checks both counts.

## Correctness

MAKE keeps (H): a found key returns an existing node; a new key gets a new identifier, larger than its children, and the table gains exactly that entry. From (H), equal identifiers mean equal trees trivially, and equal trees mean equal identifiers by induction: two nodes with equal trees have the same operator and value, their children have equal trees and so, by induction, equal identifiers, so the two nodes have the same key, and the table holds one node per key. The walks are correct because increasing identifier order is a topological order, so each memo entry is ready when a parent reads it, and each node's result depends only on its subtree. The full proof is in the proof file below.

## Complexity

Costs count hash-table operations, node visits and arithmetic operations on the constants; the bit size of the constants is not bounded here. Hash-table costs are expected, under the usual assumption of a good hash function on keys of $O(1)$ size.

| operation | time | new nodes |
|---|---|---|
| const, sym, add, sub, mul, power (MAKE) | $O(1)$ expected | 0 or 1 |
| equal | $O(1)$ | 0 |
| eval | $O(m)$ visits and $O(m)$ arithmetic operations, plus $O(\log k)$ for each power $u^k$ | 0 |
| subs, diff | $O(m)$ visits and MAKE calls | $O(m)$ |
| dag_size, tree_size | $O(m)$; tree_size returns a number that can be $2^{\Theta(m)}$ | 0 |
| space | $\Theta(N)$ for the $N$ nodes of the store, plus the table | |

Here $m$ is the number of distinct nodes reachable from the root, and the reachable set is found by a search in $O(m)$ time; the implementation sorts it, adding $O(m \log m)$, which a postorder walk avoids. These bounds are proved. The gap to the tree is real: for $u_{40}$ above, any tree walk would make $2^{42} - 1$ visits.

The cost model hides one thing: the values computed can be huge. EVAL of $u_{12}$ at $x = 1$ makes 15 visits but returns $2^{4096}$, a number of 4097 binary digits. A DAG of size $m$ can denote a polynomial of degree $2^{m}$, so its expansion, unlike its evaluation, can be exponentially large; see [expression swell](/expression-swell/).

## Variants

- **Sorting the operands of commutative operators.** If `make` sorts the children of $+$ and $\times$ by identifier, then $x + y$ and $y + x$ become one node. Flattening nested sums and products into n-ary nodes before sorting also absorbs associativity. This is a step toward a [canonical form](/canonical-form/), but only for these laws.
- **Straight-line programs.** Listing the nodes in identifier order, each as an assignment $v_i \leftarrow v_j \circ v_k$, gives a [straight-line program](/straight-line-program/), the standard model of algebraic complexity. Algorithms for polynomials given by such programs, such as factorization and identity testing, work on this form directly.
- **Term DAGs and e-graphs.** The same structure, under the name [term DAG](/term-dag/), is the term store of rewriting systems and SMT solvers. An [e-graph](/e-graph/) adds equivalence classes on top of a hash-consed DAG and merges classes as equalities are learned, using [congruence closure](/congruence-closure/).
- **Weak tables.** A long-running system lets nodes that nobody references be reclaimed, by keeping weak references in the table.
- **Reverse-mode differentiation.** Walking the DAG backward, from the root to the leaves, accumulates all partial derivatives in one pass; this is reverse-mode [automatic differentiation](/automatic-differentiation/).

## When to use it

Use a DAG when the same subexpressions recur: derivatives, results of substitution, expressions produced by programs, and large formulas in code generation. It is also the representation behind fast equality tests in theorem provers and compilers. For pure polynomial arithmetic, a [dense](/dense-polynomial/) or [sparse](/sparse-polynomial/) polynomial is usually better, since it keeps a canonical form under addition and multiplication. For small formulas that are only parsed and printed, an [expression tree](/expression-tree/) is simpler.

## Pitfalls

- **Mutation breaks sharing.** Changing a node in place changes every expression that uses it, and its key in the table becomes stale. Nodes must be immutable.
- **Keys must be canonical.** If constants are not reduced, $2/4$ and $1/2$ get two nodes, and equal identifiers no longer capture equal values of constants. The implementation stores constants as reduced fractions.
- **Pointer equality is syntactic.** Two nodes with different identifiers can still be equal as functions, such as $(x + 1)^2$ and $x^2 + 2x + 1$. Hash consing does not decide semantic equality; see the [constant problem](/constant-problem/).
- **Exponential unfoldings.** Printing the tree of a DAG, or expanding it into a polynomial, can take time exponential in the DAG size, as for $u_{40}$. Code that walks the tree instead of the DAG loses the benefit silently.
- **Recursion.** Recursive walks with a memo still recurse to the depth of the DAG. The walks here use the identifier order instead, and the tests run a chain of $30\,000$ nodes.

## Implementations

## History

Ershov (1958) used a hash table to detect repeated arithmetic operations while compiling expressions, which is the value-number method of compilers (Aho, Lam, Sethi and Ullman, Section 6.1.2). Goto (1974) introduced hash consing for Lisp, keeping a single copy of each list structure so that equality is a pointer test. Computer algebra systems adopted shared representations to control the size of intermediate expressions, and algebraic complexity theory took straight-line programs, which are DAGs written as programs, as its basic model.

## References
