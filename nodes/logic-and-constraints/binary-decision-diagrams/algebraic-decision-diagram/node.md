---
tag: 1TQF00
kind: data-structure
slug: algebraic-decision-diagram
name: Algebraic decision diagram
aliases:
- ADD
- multi-terminal BDD
- MTBDD
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: A reduced ordered BDD whose sinks hold values from any set, such as numbers. It represents functions from bit vectors to values canonically and combines them with any pointwise operation.
model: word-ram
complexity:
  vars: {f: the number of nodes of the first argument, g: the number of nodes of the second argument, n: the number of variables}
  time: {mk: O(1) expected, apply: O(f g) expected, evaluate: O(n), from_table: O(2^n) expected}
  space: {nodes: O(f)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1993
  people: [R. Iris Bahar, Erica A. Frohm, Charles M. Gaona, Gary D. Hachtel, Enrico Macii, Abelardo Pardo, Fabio Somenzi]
  note: Bahar and others named algebraic decision diagrams and used them for matrix algebra and shortest paths; Clarke, Fujita and others introduced the same structure as multi-terminal BDDs in the same year.
prereqs: [reduced-ordered-bdd, bdd-apply, bdd-canonicity]
see_also: [reduced-ordered-bdd, bdd-apply, binary-moment-diagram, multi-valued-decision-diagram, markov-decision-process, value-iteration, model-counting, computed-table]
sources:
  - paper: "R. Iris Bahar, Erica A. Frohm, Charles M. Gaona, Gary D. Hachtel, Enrico Macii, Abelardo Pardo, Fabio Somenzi, Algebraic decision diagrams and their applications, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 1993, pages 188 to 191"
    title: Algebraic decision diagrams and their applications
    locator: the definition of ADDs, Apply with arbitrary operators, abstraction, and matrix multiplication and shortest paths
  - paper: "R. Iris Bahar, Erica A. Frohm, Charles M. Gaona, Gary D. Hachtel, Enrico Macii, Abelardo Pardo, Fabio Somenzi, Algebraic decision diagrams and their applications, Formal Methods in System Design 10(2/3), 1997, pages 171 to 206"
    title: Algebraic decision diagrams and their applications (journal version)
    locator: the full treatment of the operations and their costs
  - paper: "Masahiro Fujita, Patrick C. McGeer, Jerry C.-Y. Yang, Multi-terminal binary decision diagrams, an efficient data structure for matrix representation, Formal Methods in System Design 10(2/3), 1997, pages 149 to 169"
    title: Multi-terminal binary decision diagrams, an efficient data structure for matrix representation
    locator: MTBDDs for matrices, and the recursive matrix operations
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: the chapter on integer-valued decision diagrams (MTBDDs, EVBDDs and BMDs)
---

An algebraic decision diagram (ADD) is a [reduced ordered BDD](/reduced-ordered-bdd/) whose sinks are labelled with values from an arbitrary set $D$, usually numbers, in place of 0 and 1. It represents a function $f : \{0, 1\}^n \to D$, also called a pseudo-Boolean function when $D$ is a set of numbers. The same structure is called a multi-terminal BDD (MTBDD). The reduction rules, the canonicity theorem and the [apply](/bdd-apply/) algorithm of BDDs carry over without change, and apply now combines two functions with any pointwise operation, such as $+$, $\times$, $\max$ or $\min$. ADDs are used for matrices indexed by bit vectors, for the value functions of [Markov decision processes](/markov-decision-process/), and for probabilistic model checking. Their weakness is that each distinct value needs its own sink, so functions with many values, such as the binary value of a word, have exponential ADDs. Edge-valued diagrams and [binary moment diagrams](/binary-moment-diagram/) address this.

## In plain words

A BDD answers yes or no after a series of bit questions. An ADD answers with a number. The diagram asks about the bits in a fixed order, and each final box holds a value. As in a BDD, two boxes that do the same work are merged, and a question whose two answers lead to the same place is dropped. So each function has exactly one diagram. To add, multiply or compare two such functions point by point, the program walks both diagrams at once, one bit at a time, and combines the values it finds at the bottom. This works well when the function has few different values that follow a pattern. It works badly when almost every input has its own value.

## The abstract type

The variables are $x_1, \ldots, x_n$ in a fixed order. A node $u$ stands for a function $f_u : \{0, 1\}^n \to D$.

| operation | result |
|---|---|
| CONST$(c)$ | the constant function $c$ |
| MK$(v, l, h)$ | the function equal to $f_l$ where $x_v = 0$ and to $f_h$ where $x_v = 1$ |
| APPLY$(\mathrm{op}, f, g)$ | the function $x \mapsto \mathrm{op}(f(x), g(x))$ |
| SUM-OUT$(f, v)$ | $f\vert_{x_v = 0} + f\vert_{x_v = 1}$, a function that does not depend on $x_v$ |
| THRESHOLD$(f, t)$ | the 0-1 function of the predicate $f(x) \ge t$ |
| EVALUATE$(f, x)$ | $f(x)$ |
| FROM-TABLE$(T)$ | the node of the function with the value table $T$ |
| EQUAL$(f, g)$ | whether $f = g$, by comparing ids |

The decomposition is the arithmetic form of the [Shannon expansion](/shannon-expansion/): for numbers,

$$f = (1 - x_v) \, f|_{x_v = 0} + x_v \, f|_{x_v = 1}.$$

## Representation

A sink is a node $(n + 1, c)$ that stores a value $c \in D$, one per value. An inner node is a triple $(v, l, h)$ with $v$ smaller than the variables of $l$ and $h$. All nodes come from CONST and MK, which keep a unique table, a [hash table](/hash-table/) from keys to ids. MK applies the two rules of ROBDDs: it returns $l$ when $l = h$ (elimination), and the existing node when the triple is stored (merging). APPLY caches its results in a [computed table](/computed-table/) keyed by the operation and the two ids.

A matrix $M$ of size $2^k \times 2^k$ is an ADD over row bits $r_1, \ldots, r_k$ and column bits $c_1, \ldots, c_k$, with $f(r, c) = M[r][c]$. Interleaving the row and column bits ($r_1, c_1, r_2, c_2, \ldots$) keeps block-structured matrices small.

## Operations

Let $\mathrm{cof}(u, v)$ be $(l, h)$ if $u = (v, l, h)$, and $(u, u)$ if $u$ does not test $x_v$ at its root, which means that $f_u$ does not depend on $x_v$.

```pseudo id=main
MK(v, l, h)
L1  if l = h then return l                         ▷ elimination rule
L2  if U holds (v, l, h) then return U[v, l, h]        ▷ merging rule
L3  otherwise make a new node u with U[v, l, h] ← u, and return u

APPLY(op, f, g)
L4  if f and g are sinks then return CONST(op(value(f), value(g)))
L5  if the cache holds (op, f, g) then return it
L6  v ← min(var(f), var(g)); (f0, f1) ← cof(f, v); (g0, g1) ← cof(g, v)
L7  r ← MK(v, APPLY(op, f0, g0), APPLY(op, f1, g1))
L8  cache[op, f, g] ← r; return r
```

- **SUM-OUT$(f, v)$** walks down to $x_v$. At a node of $x_v$ it returns APPLY$(+, l, h)$. At a node below $x_v$, or a sink, $f$ does not depend on $x_v$, and it returns APPLY$(+, f, f)$. Above $x_v$ it rebuilds the node with MK from the results for the two children. Summing out all variables gives $\sum_x f(x)$, and summing out the shared index bits of a product gives a matrix product: $C(r, c) = \sum_k A(r, k) \, B(k, c)$ is APPLY$(\times, A, B)$ followed by SUM-OUT over the bits of $k$.
- **THRESHOLD$(f, t)$** is APPLY with the operation $(a, b) \mapsto [a \ge b]$ and the constant $t$. It turns an ADD into a BDD.
- **FROM-TABLE** builds the diagram bottom-up, one variable per round, as BUILD does for ROBDDs.
- **EVALUATE** follows one path, as for BDDs.

## Example

Let $n = 2$ and $f(x_1, x_2) = x_1 + x_2$, the number of ones. Its ADD has the sinks 0, 1 and 2 and three inner nodes: $A = (x_2, 0, 1)$ for $x_1 = 0$, $B = (x_2, 1, 2)$ for $x_1 = 1$, and the root $R = (x_1, A, B)$. That is 6 nodes.

**APPLY trace.** Multiply $f$ by the 0-1 function $h = x_1$, whose ADD is $(x_1, 0, 1)$. The result should be $x_1 (x_1 + x_2) = x_1 (1 + x_2)$, with the values 0, 0, 1, 2 for $x_1 x_2 = 00, 01, 10, 11$.

- Line L6 at the top takes $v = 1$, with $\mathrm{cof}(R, 1) = (A, B)$ and $\mathrm{cof}(h, 1) = (0, 1)$.
- APPLY$(\times, A, 0)$: line L6 takes $v = 2$, with $\mathrm{cof}(A, 2) = (0, 1)$ and $\mathrm{cof}(0, 2) = (0, 0)$. Line L4 gives $0 \times 0 = 0$ and $1 \times 0 = 0$, and line L1 returns the sink 0.
- APPLY$(\times, B, 1)$: the same steps give the sinks $1 \times 1 = 1$ and $2 \times 1 = 2$, and line L2 finds the stored node $B$.
- Line L7 returns MK$(1, 0, B)$, a new node. The result has 5 nodes: the root, $B$, and the sinks 0, 1, 2.

**SUM-OUT trace.** SUM-OUT$(f, 2) = f|_{x_2=0} + f|_{x_2=1} = 2 x_1 + 1$. The root tests $x_1$, above $x_2$, so it is rebuilt from SUM-OUT$(A, 2) = $ APPLY$(+, 0, 1) = 1$ and SUM-OUT$(B, 2) = $ APPLY$(+, 1, 2) = 3$. The result is $(x_1, 1, 3)$.

**Size.** The implementation measures these sizes, with the sinks:

| function | ADD nodes |
|---|---|
| $\sum_{i=1}^{n} 2^{i-1} x_i$ (the binary value of a word) | $2^{n+1} - 1$ |
| $X \cdot Y$ for words of $w = 1, 2, 3, 4, 5$ bits | 4, 19, 82, 330, 1332 |

The binary value has $2^n$ distinct values, so it needs $2^n$ sinks; the [BMD](/binary-moment-diagram/) of the same word has $2n + 1$ nodes, and the BMD of $X \cdot Y$ has $w^2 + 3w$ nodes.

## Correctness

The proofs are those of ROBDDs, with more than two sinks. **Canonicity**: going up from the sinks, every inner node depends on its variable and not on the variables above it, and two distinct nodes compute distinct functions. A node on level $v$ depends on $x_v$ because its two children are distinct nodes on lower levels, hence distinct functions, and neither depends on $x_v$. Two nodes with the same function must start on the same level, and then their children have the same functions, so they are the same by induction and the merging rule. **APPLY** is correct by the Shannon expansion: $\mathrm{op}(f, g)$ at $x_v = b$ is $\mathrm{op}(f_b, g_b)$, and MK puts the two halves together. **SUM-OUT** is correct because the restriction $f|_{x_v = b}$ commutes with the decomposition at variables above $x_v$. The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| CONST, MK | $O(1)$ expected | one hash lookup |
| APPLY$(\mathrm{op}, f, g)$ | $O(\lvert f \rvert \cdot \lvert g \rvert)$ expected | each pair of nodes is handled once; the result has at most $\lvert f \rvert \cdot \lvert g \rvert$ nodes |
| SUM-OUT$(f, v)$ | at most one APPLY per node of $f$ on level $v$ and below | in practice close to the size of the result |
| EVALUATE | $O(n)$ | one path |
| FROM-TABLE | $O(2^n)$ expected | $2^n - 1$ calls of MK |
| space | $O(\text{nodes})$ | store, unique table and cache |

The size of an ADD is at least the number of distinct values of the function, and at most the size bound of BDDs plus that number of sinks.

## Variants

- **[ROBDDs](/reduced-ordered-bdd/)** are ADDs with $D = \{0, 1\}$.
- **[Multi-valued decision diagrams](/multi-valued-decision-diagram/)** let the variables have more than two values; MDDs with many sinks combine both generalizations.
- **Edge-valued BDDs (EVBDDs)** put additive weights on the edges, so $\sum_i 2^{i-1} x_i$ has linear size; affine ADDs and factored edge-valued BDDs extend this with multiplicative weights.
- **[Binary moment diagrams](/binary-moment-diagram/)** use a different decomposition, by the linear moment in each variable, and make words and products small.
- **Approximate ADDs** merge sinks whose values are close, to keep value functions small in planning.

## When to use it

Use ADDs when a function has few distinct values with structure: costs and probabilities in a [Markov decision process](/markov-decision-process/) solved by [value iteration](/value-iteration/), as in the SPUDD planner of Hoey and others (1999); sparse or block-structured matrices; transition matrices in probabilistic model checking, as in PRISM; and weighted [model counting](/model-counting/). The canonical form makes it cheap to detect that two value functions are equal, which is the stopping test of value iteration.

Do not use them for arithmetic on words, where the number of distinct values is exponential. Use BMDs or edge-valued diagrams there.

## Pitfalls

- **The number of sinks.** Real-valued computations produce many slightly different values. Exact rational numbers or rounding to a tolerance is needed, or the diagram grows without limit; rounding makes the result depend on the order of the operations.
- **The cache key must name the operation.** Two operations on the same pair of ids give different results. If the operation is a fresh closure on each call, the cache never hits.
- **Values must be hashable and comparable for equality.** Floating point values that differ in the last bit are different sinks.
- **The order.** As for BDDs, the size can change by an exponential factor with the variable order; for matrices, interleave row and column bits.

## Implementations

## History

Clarke, Fujita, McGeer, McMillan, Yang and Zhao introduced multi-terminal BDDs in 1993 to represent matrices and to compute spectral transforms. In the same year, Bahar, Frohm, Gaona, Hachtel, Macii, Pardo and Somenzi named algebraic decision diagrams, gave Apply with arbitrary operators and abstraction, and used them for matrix multiplication and shortest paths; the CUDD package of Somenzi supports them. Lai and Sastry (1992) had proposed edge-valued BDDs for the same class of functions. Hoey, St-Aubin, Hu and Boutilier (1999) used ADDs to solve large factored MDPs, and probabilistic model checkers such as PRISM represent transition matrices with MTBDDs.

## References
