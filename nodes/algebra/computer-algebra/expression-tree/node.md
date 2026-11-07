---
tag: 5TDXMG
kind: data-structure
slug: expression-tree
name: Expression tree
aliases:
- syntax tree for expressions
- formula tree
- algebraic expression tree
area: algebra/computer-algebra
level: intro
summary: Tree whose internal nodes are operators and whose leaves are constants or symbols.
implements: [expression]
prereqs: [rooted-tree, tree-traversal, expression]
see_also: [expression-dag, abstract-syntax-tree, binary-tree, canonical-form, shunting-yard-algorithm, reverse-polish-notation, automatic-differentiation, expression-swell]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 2.3.2 (binary tree representation of trees), the representation of algebraic formulas as trees and Algorithm D (differentiation)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 3 (normal forms and algebraic representations), the expression tree level of representation
  - book: isbn:9781568811581
    title: Joel S. Cohen, Computer Algebra and Symbolic Computation, Elementary Algorithms, A K Peters, 2002
    locator: Chapter 3, the recursive structure of mathematical expressions (expression trees, operands, substitution)
  - book: isbn:9780262510875
    title: Harold Abelson and Gerald Jay Sussman, Structure and Interpretation of Computer Programs, second edition, MIT Press, 1996
    locator: Section 2.3.2 (example, symbolic differentiation)
---

An expression tree stores a formula as a rooted tree: each leaf is a constant or a symbol, and each internal node is an operator whose children are its operands, in order. So $(x + 3)(x - y)$ is a node $\times$ with two children, the trees of $x + 3$ and of $x - y$. Evaluation, substitution, differentiation and printing are all one walk over the tree, children before parents, in $O(n)$ node visits for a tree of $n$ nodes. It is the plainest implementation of the [symbolic expression](/expression/) type, and the form that a parser produces. Its weakness is that a repeated subexpression is stored, and processed, once for each occurrence; the [expression DAG](/expression-dag/) removes that.

## In plain words

Write a formula, then draw it as a family tree. The last operation you would carry out sits at the top. Below it hang the two parts it combines, and below each of those, the parts they combine, down to single numbers and letters at the bottom.

To work out the value, start at the bottom: replace each letter by its number, then combine pairs of values on the way up, until one value is left at the top. To put a new formula in place of a letter, swap each leaf with that letter for a copy of the new formula. To take a derivative, apply the rules from calculus at each node, using what was already found for the parts below it.

## The abstract type

The tree implements the [symbolic expression](/expression/) type. Here the constants are rationals, the symbols are names, and the operators are the binary $+$, $-$, $\times$ and the power $u^k$ with a constant integer $k \ge 0$. The operations are the constructors `const`, `sym`, `add`, `sub`, `mul` and `power`; `eval` at an environment $\rho$ that gives each symbol a value; `subs`$(e, x, r)$, which replaces the symbol $x$ by $r$; `diff`$(e, x)$; `equal`, which is syntactic identity; and `size`, `height` and `to_string`. The laws are those of the [expression](/expression/) page, laws (E1) to (E7).

## Representation

A node has three fields: `op`, which is `const`, `sym` or an operator; `val`, the constant or the name at a leaf; and `kids`, the tuple of children, empty at a leaf and of length 2 at an operator. Nodes are immutable. The invariant is:

> **(T)** Every node has a valid `op`. A `const` node holds a rational and a `sym` node a name, and both have no children. An operator node has exactly two children, and the second child of a power is a constant integer $k \ge 0$. Following children from the root never returns to a node on the current path.

The value of a tree is defined by structural recursion: $[\![c]\!]_\rho = c$, $[\![s]\!]_\rho = \rho(s)$, and $[\![\,a \circ b\,]\!]_\rho = [\![a]\!]_\rho \circ [\![b]\!]_\rho$. Because nodes are immutable, two parents may point to the same child without harm; the operations below still treat the structure as a tree, and count a shared child once per occurrence. The size $n$ is the number of nodes counted that way, and the height $h$ is the number of edges on a longest path from the root.

## Operations

The main block evaluates a tree. It walks the tree in postorder with an explicit stack $S$ of pairs (node, done flag) and a stack $V$ of values, so a tree of any height is fine.

```pseudo id=main
EVAL(e, ρ)
L1  S ← a stack holding (e, false); V ← an empty stack of values
L2  while S is not empty do
L3      (u, done) ← POP(S)
L4      if u is a constant c then PUSH(V, c)
L5      else if u is a symbol s then PUSH(V, ρ(s))
L6      else if not done then PUSH(S, (u, true)); PUSH(S, (u.right, false)); PUSH(S, (u.left, false))
L7      else b ← POP(V); a ← POP(V); PUSH(V, a u.op b)
L8  return the only element of V
```

The first time an operator node comes off the stack, line L6 puts it back with the flag set, and above it its two children, the left one on top. When the node comes off the second time, both children have been evaluated, and their values are the top two entries of $V$, the right one on top. Line L7 combines them.

Substitution and differentiation visit the nodes in the same postorder, and store one result per node.

```pseudo id=subs
SUBS(e, x, r)
S1  for each node u of e in postorder do
S2      if u is the symbol x then R[u] ← r
S3      else if u is a leaf then R[u] ← u
S4      else R[u] ← a new node with operator u.op and children R[u.left], R[u.right]
S5  return R[e]
```

```pseudo id=diff
DIFF(e, x)
D1  for each node u of e in postorder do
D2      if u is a constant then D[u] ← 0
D3      else if u is a symbol then D[u] ← 1 if u = x, else 0
D4      else if u = a ± b then D[u] ← D[a] ± D[b]
D5      else if u = a × b then D[u] ← D[a] × b + a × D[b]
D6      else if u = a^k then D[u] ← 0 if k = 0, else k × a^(k−1) × D[a]
D7  return D[e]
```

DIFF builds its result with *smart constructors* that fold constants and apply $0 + u = u$, $0 \cdot u = 0$ and $1 \cdot u = u$, so that $\partial x / \partial x$ is the leaf 1 and not a tree of zeros and ones. These rewrites keep the value. The new nodes of lines D5 and D6 point to the subtrees $a$, $b$, $D[a]$ and $D[b]$ instead of copying them, so DIFF makes $O(1)$ new nodes per node of $e$.

`equal` walks both trees together with a stack of pairs and stops at the first difference. `size`, `height` and `to_string` are postorder walks that combine the results of the children.

## Example

Take $e = (x + 3)(x - y)$ and $\rho = \{x \mapsto 2, y \mapsto 5\}$. The tree has 7 nodes and height 2. Write $A$ for the $\times$ node, $B$ for $x + 3$ and $C$ for $x - y$. The stacks are shown with the top on the right.

| pass | popped | line | $S$ after | $V$ after |
|---|---|---|---|---|
| 1 | $(A, \text{false})$ | L6 | $(A,\text{t})\ (C,\text{f})\ (B,\text{f})$ | |
| 2 | $(B, \text{false})$ | L6 | $(A,\text{t})\ (C,\text{f})\ (B,\text{t})\ (3,\text{f})\ (x,\text{f})$ | |
| 3 | $(x, \text{false})$ | L5 | $(A,\text{t})\ (C,\text{f})\ (B,\text{t})\ (3,\text{f})$ | 2 |
| 4 | $(3, \text{false})$ | L4 | $(A,\text{t})\ (C,\text{f})\ (B,\text{t})$ | 2, 3 |
| 5 | $(B, \text{true})$ | L7 | $(A,\text{t})\ (C,\text{f})$ | 5 |
| 6 | $(C, \text{false})$ | L6 | $(A,\text{t})\ (C,\text{t})\ (y,\text{f})\ (x,\text{f})$ | 5 |
| 7 | $(x, \text{false})$ | L5 | $(A,\text{t})\ (C,\text{t})\ (y,\text{f})$ | 5, 2 |
| 8 | $(y, \text{false})$ | L5 | $(A,\text{t})\ (C,\text{t})$ | 5, 2, 5 |
| 9 | $(C, \text{true})$ | L7 | $(A,\text{t})$ | 5, $-3$ |
| 10 | $(A, \text{true})$ | L7 | | $-15$ |

There are 10 passes: one for each of the 4 leaves and two for each of the 3 operators. DIFF$(e, x)$ gives $(x - y) + (x + 3)$: at $A$, line D5 forms $1 \cdot (x - y) + (x + 3) \cdot 1$, and the smart constructors drop the factors 1. Its value at $\rho$ is $-3 + 5 = 2$. SUBS$(e, x, y + 1)$ gives $((y + 1) + 3)((y + 1) - y)$, which is 4 at $y = 0$. The tests check each of these.

## Correctness

The key fact for EVAL is a stack lemma: if $(u, \text{false})$ is on top of $S$, with $S_0$ below it and $V = W$, then after exactly $\ell(u) + 2 i(u)$ more passes, where $\ell(u)$ and $i(u)$ count the leaves and the operator nodes of the subtree $u$, the stacks are $S = S_0$ and $V = W \cdot [\![u]\!]_\rho$, and nothing in $S_0$ or $W$ was touched in between. It holds for leaves by lines L4 and L5, and for an operator node by line L6, the lemma for the left child, then for the right child, and line L7. Applied to the root with empty $S_0$ and $W$, it shows that EVAL returns $[\![e]\!]_\rho$ after $n + i(e)$ passes. For SUBS and DIFF, postorder means that each node is processed after its children, and induction along that order shows $R[u] = u[x := r]$ and $[\![D[u]]\!]_\rho = \partial [\![u]\!]_\rho / \partial x$ for each node $u$. The full proof is in the proof file below.

## Complexity

The cost is counted in node visits and in arithmetic operations on the constants; the bit size of rational constants can grow, and is not bounded here.

| operation | time | new nodes | notes |
|---|---|---|---|
| const, sym, add, sub, mul, power | $O(1)$ | 1 or 2 | |
| eval | $\Theta(n)$ visits, $n + i(e)$ passes | 0 | one arithmetic operation per operator node, and $O(\log k)$ multiplications for $u^k$ by repeated squaring |
| subs | $\Theta(n)$ | at most $i(e)$ | $r$ is shared, not copied |
| diff | $\Theta(n)$ | $O(n)$ | with sharing; see below |
| equal | $O(\min(n_1, n_2))$ | 0 | $\Omega(n)$ in the worst case, when the trees are equal |
| size, height, to_string | $\Theta(n)$ | 0 | to_string writes $\Theta(n)$ characters, more with long constants |
| space | $n$ nodes and a stack of $O(h)$ entries | | $h \le n - 1$ |

These bounds are proved. A tree that copies instead of sharing pays more. For the product chain $(\cdots((x \cdot x) \cdot x) \cdots) \cdot x$ of $N$ factors, which has $n = 2N - 1$ nodes, the derivative as a fully copied tree has about $N^2$ nodes: $107$, $417$, $1637$ and $6477$ for $N = 10, 20, 40, 80$, measured by the test code, while the shared version has $35$, $75$, $155$ and $315$ distinct nodes. So sharing turns a quadratic cost into a linear one, and an [expression DAG](/expression-dag/) makes that sharing systematic.

## Variants

- **n-ary sum and product nodes.** Systems such as Maple and Mathematica store $a + b + c$ as one node with three children, and keep the children sorted. This flattens associativity and commutativity into the representation, a first step toward a [canonical form](/canonical-form/).
- **Expression DAG.** Equal subtrees are stored once, by [hash consing](/hash-consing/). Equality becomes a pointer test and repeated subexpressions are processed once. See [expression DAG](/expression-dag/).
- **Postfix arrays.** The postorder sequence of the nodes, as in [reverse Polish notation](/reverse-polish-notation/), is a flat encoding of the same tree; EVAL then is a single left-to-right scan with the value stack.
- **Abstract syntax trees.** A compiler's [abstract syntax tree](/abstract-syntax-tree/) is an expression tree with statements and types; it is built from text by a parser such as the [shunting-yard algorithm](/shunting-yard-algorithm/).
- **Forward-mode differentiation.** Evaluating each node and its derivative together, as numbers instead of trees, is [automatic differentiation](/automatic-differentiation/); it avoids the growth of symbolic derivatives.

## When to use it

Use an expression tree for input, output and light manipulation of formulas: parsing, printing, substitution, evaluation at points and symbolic derivatives of small formulas. For polynomial arithmetic, convert to a [dense](/dense-polynomial/) or [sparse](/sparse-polynomial/) polynomial, where addition and multiplication keep a canonical form. For large formulas with much repetition, as produced by differentiation or by code generators, use an [expression DAG](/expression-dag/).

## Pitfalls

- **Recursion depth.** A recursive walk fails on a left-deep chain of $50\,000$ additions in a language with a small call stack. The walks here use explicit stacks, and the tests run them on such a chain.
- **Order on the value stack.** Line L7 pops the right operand first. Swapping the two pops computes $b - a$ instead of $a - b$.
- **Syntactic equality is not equality.** `equal` says that $x + y$ and $y + x$ differ. Equivalence needs a [canonical form](/canonical-form/), and for general expressions it is undecidable; see the [constant problem](/constant-problem/).
- **Sharing mutable nodes.** If nodes can be changed in place, a shared subtree changes in every place it occurs. Keep nodes immutable, or copy on substitution.
- **Power rule edge cases.** The rule $k u^{k-1} u'$ must give $u'$ for $k = 1$ and 0 for $k = 0$; an early version of the code here returned $u \cdot u'$ for $k = 1$, and the random test against an independent polynomial expansion caught it.
- **Growth of derivatives.** Without sharing and simplification, repeated differentiation grows fast; see [expression swell](/expression-swell/).

## Implementations

## History

Programs that differentiate formulas held as trees were among the first nonnumerical programs: Knuth (Section 2.3.2) credits H. G. Kahrimanian and J. Nolan with independent differentiation programs in 1953, and gives the tree algorithm as Algorithm D. McCarthy's LISP (1960) made nested lists, the S-expressions, the standard form of symbolic data, and early computer algebra systems such as MACSYMA, REDUCE and later Maple and Mathematica all store general expressions as trees or DAGs of this kind.

## References
