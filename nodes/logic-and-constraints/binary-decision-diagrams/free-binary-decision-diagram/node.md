---
tag: DQZTGE
kind: data-structure
slug: free-binary-decision-diagram
name: Free binary decision diagram
aliases:
- FBDD
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: A BDD in which each path tests each variable at most once, but different paths may use different orders. It allows linear-time counting and a randomized equivalence test.
model: word-ram
complexity:
  vars: {s: the number of nodes of the diagram, n: the number of variables, t: the number of random trials}
  time: {mk: O(1) expected, evaluate: O(n), is_free: O(s n), count: O(s), arith: O(s), probably_equal: O(t s)}
  space: {nodes: O(s)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1980
  people: [Manuel Blum, Ashok K. Chandra, Mark N. Wegman]
  note: Blum, Chandra and Wegman gave the randomized equivalence test for free Boolean graphs; Gergov and Meinel (1994) and Sieling and Wegener (1995) made FBDDs with a fixed graph order a practical data structure.
prereqs: [read-once-branching-program, reduced-ordered-bdd, binary-decision-diagram]
see_also: [read-once-branching-program, ordered-binary-decision-diagram, hidden-weighted-bit-lower-bound, polynomial-identity-testing, schwartz-zippel-lemma, bdd-satisfy-count, model-counting, hash-consing]
sources:
  - paper: "Manuel Blum, Ashok K. Chandra, Mark N. Wegman, Equivalence of free Boolean graphs can be decided probabilistically in polynomial time, Information Processing Letters 10(2), 1980, pages 80 to 82"
    title: Equivalence of free Boolean graphs can be decided probabilistically in polynomial time
    locator: the arithmetization of a free graph and the randomized equivalence test
  - paper: "Jordan Gergov, Christoph Meinel, Efficient Boolean manipulation with OBDD's can be extended to FBDD's, IEEE Transactions on Computers 43(10), 1994, pages 1197 to 1209"
    title: Efficient Boolean manipulation with OBDD's can be extended to FBDD's
    locator: types (graph orders), canonicity for a fixed type, and the synthesis algorithms
  - paper: "Detlef Sieling, Ingo Wegener, Graph driven BDDs, a new data structure for Boolean functions, Theoretical Computer Science 141, 1995, pages 283 to 310"
    title: Graph driven BDDs, a new data structure for Boolean functions
    locator: graph-driven BDDs, their reduction, and the hidden weighted bit function
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 6, Free BDDs (FBDDs) and read-once BPs
---

A free binary decision diagram (FBDD) is a [binary decision diagram](/binary-decision-diagram/) in which no path from the root tests a variable twice. Unlike an [ordered BDD](/ordered-binary-decision-diagram/), it does not fix one order of the variables: each path can choose its own order. As a model of computation it is the [read-once branching program](/read-once-branching-program/), and the two names denote the same graphs. FBDDs keep two useful properties of OBDDs: every path to the 1-sink is followed by some input, so satisfiability and model counting take linear time, and equivalence has a fast randomized test. They lose one: the reduced FBDD of a function is not unique, so equality is no longer a pointer comparison. The gain is size. The [hidden weighted bit function](/hidden-weighted-bit-lower-bound/) has FBDDs with at most $n(n+1)$ inner nodes but needs exponential OBDDs for every order.

## In plain words

Think of a quiz where each question looks at one bit of the input, and the next question depends on the answers so far. In an ordered diagram the questions always come in the same list order. In a free diagram, each route may ask the bits in its own order, but no route asks the same bit twice. Equal sub-quizzes are stored once. Because no route asks a bit twice, every route to "yes" really happens for some input, and each question splits the inputs in two equal halves. That makes counting the "yes" inputs easy. To check whether two free diagrams agree, the program replaces the bits by random numbers, computes one number for each diagram, and compares them. Different diagrams of the same function always give the same number.

## The abstract type

A store holds nodes over the variables $x_1, \ldots, x_n$. A node $u$ represents a function $f_u : \{0, 1\}^n \to \{0, 1\}$. The operations are:

| operation | result | precondition |
|---|---|---|
| MK$(v, l, h)$ | the node of $(\neg x_v \wedge f_l) \vee (x_v \wedge f_h)$ | for a free result, $x_v$ is not tested below $l$ or $h$ |
| EVALUATE$(u, x)$ | $f_u(x)$ | none |
| IS-FREE$(u)$ | whether no path from $u$ tests a variable twice | none |
| COUNT$(u)$ | $\lvert \{x : f_u(x) = 1\} \rvert$ | $u$ is free |
| ARITH$(u, r, p)$ | the multilinear extension of $f_u$ at $r \in \mathbb{F}_p^n$ | $u$ is free |
| PROBABLY-EQUAL$(u, w)$ | whether $f_u = f_w$, with one-sided error | $u$ and $w$ are free |
| NOT$(u)$ | $\neg f_u$, by exchanging the two sinks | none |

The **multilinear extension** of $f$ is the unique polynomial $\hat f(y) = \sum_{a \in \{0,1\}^n} f(a) \prod_{i} (a_i y_i + (1 - a_i)(1 - y_i))$, which has degree at most 1 in each variable and equals $f$ on $\{0, 1\}^n$.

There is no APPLY with a polynomial bound: the AND of two FBDDs whose paths use conflicting orders can need exponential size (see [read-once branching program](/read-once-branching-program/)).

## Representation

Node 0 is the 0-sink and node 1 is the 1-sink. An inner node is a triple $(\mathrm{var}, \mathrm{lo}, \mathrm{hi})$, and nodes are created only by MK through a unique table, a [hash table](/hash-table/) from triples to ids, as in [hash consing](/hash-consing/). MK applies the two reduction rules of [ROBDDs](/reduced-ordered-bdd/): it returns $l$ when $l = h$, and it returns the existing node when the triple is already stored. So the store has no redundant node and no two equal nodes. Children always have smaller ids than their parents, so the ids give a topological order.

The free property is a property of the graph below a root, not of a single node. MK does not check it; IS-FREE does.

## Operations

The procedure TOPO$(u)$ lists the inner nodes that $u$ reaches, each after its children, by an iterative depth-first search. The code uses 0-based variables.

```pseudo id=main
EVALUATE(u, x)
L1  while u is an inner node do
L2      if x[var(u)] = 1 then u ← hi(u) else u ← lo(u)
L3  return u                                   ▷ the sink 0 or 1

IS-FREE(root)                                  ▷ below[0] = below[1] = ∅
L4  for u in TOPO(root) do
L5      if var(u) ∈ below[lo(u)] ∪ below[hi(u)] then return false
L6      below[u] ← below[lo(u)] ∪ below[hi(u)] ∪ {var(u)}
    return true

COUNT(root)                                    ▷ c[0] = 0, c[1] = 2^n
L7  for u in TOPO(root) do
L8      c[u] ← (c[lo(u)] + c[hi(u)]) / 2
    return c[root]

ARITH(root, r, p)                              ▷ val[0] = 0, val[1] = 1
L9  for u in TOPO(root) do
L10     val[u] ← ((1 − r[var(u)]) · val[lo(u)] + r[var(u)] · val[hi(u)]) mod p
    return val[root]

PROBABLY-EQUAL(f, g)                           ▷ p = 2^61 − 1, t trials
    repeat t times
        r ← a uniform random point of F_p^n
L11     if ARITH(f, r, p) ≠ ARITH(g, r, p) then return false
L12 return true
```

The implementation also builds the FBDD of the hidden weighted bit function with at most $n(n+1)$ inner nodes. Its node $(a, b, \gamma)$ holds the unread interval $x_a, \ldots, x_b$, tests $x_b$ when $\gamma = 1$ and $x_a$ when $\gamma = 0$; the proof is on the [HWB page](/hidden-weighted-bit-lower-bound/).

## Example

The construction for $n = 4$ gives this reduced FBDD of $\mathrm{HWB}_4$ (the bit $x_{|x|}$, and 0 for $x = 0$), with 6 inner nodes and 2 sinks:

| node | tests | lo | hi |
|---|---|---|---|
| $a$ | $x_1$ | 0 | 1 |
| $b$ | $x_2$ | 0 | 1 |
| $c$ | $x_3$ | 0 | 1 |
| $d$ | $x_1$ | $b$ | $c$ |
| $e$ | $x_3$ | $a$ | $b$ |
| root | $x_4$ | $e$ | $d$ |

The path through $d$ tests $x_1$ before $x_3$, and the path through $e$ tests $x_3$ before $x_1$, so no single order fits; the node $b$ is shared by both. The best OBDD of $\mathrm{HWB}_4$ has 9 nodes, against 8 here.

- **EVALUATE** on $x = (0, 1, 0, 1)$: the weight is 2, so the answer is $x_2 = 1$. The walk goes root $\to d$ (since $x_4 = 1$) $\to b$ (since $x_1 = 0$) $\to 1$ (since $x_2 = 1$).
- **IS-FREE**: below$[a] = \{1\}$, below$[b] = \{2\}$, below$[c] = \{3\}$, below$[d] = \{1, 2, 3\}$, below$[e] = \{1, 2, 3\}$, and the root tests $x_4 \notin$ below$[d] \cup$ below$[e]$. So it returns true.
- **COUNT** with $2^4 = 16$: $c[a] = c[b] = c[c] = (0 + 16)/2 = 8$, $c[d] = (8 + 8)/2 = 8$, $c[e] = 8$, and $c[\text{root}] = 8$. Check by weight: weight 1 needs $x_1 = 1$ (1 input), weight 2 needs $x_2 = 1$ (3 inputs), weight 3 needs $x_3 = 1$ (3 inputs), and weight 4 gives $x_4 = 1$ (1 input), so there are 8 models.
- **ARITH** at $r = (2, 3, 5, 7)$: val$[a] = 2$, val$[b] = 3$, val$[c] = 5$, val$[d] = (1 - 2) \cdot 3 + 2 \cdot 5 = 7$, val$[e] = (1 - 5) \cdot 2 + 5 \cdot 3 = 7$, and val$[\text{root}] = (1 - 7) \cdot 7 + 7 \cdot 7 = 7$. Any other FBDD of $\mathrm{HWB}_4$, for example the best OBDD, gives 7 at this point too.

## Correctness

EVALUATE follows the computation path. IS-FREE computes, for each node, the set of variables tested on some path below it, and a node whose variable is in the set of a child is the start of a repeated test. COUNT and ARITH rest on one fact about free diagrams: no node below a child of $u$ tests $\mathrm{var}(u)$. So the number of inputs that reach the 1-sink from a child does not depend on the bit $x_{\mathrm{var}(u)}$, which gives the halving in line L8, and the polynomial of a child does not contain the variable $y_{\mathrm{var}(u)}$, which makes the polynomial of every node multilinear. Two multilinear polynomials that agree on $\{0, 1\}^n$ are equal, so ARITH computes the multilinear extension, the same for every FBDD of the function. If the functions differ, the difference of the extensions is a nonzero polynomial of degree at most $n$, and by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) a random point is a root with probability at most $n/p$. The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| MK | $O(1)$ expected | one hash lookup |
| EVALUATE | $O(n)$ | a free path has at most $n$ inner nodes |
| IS-FREE | $O(s n)$ | one set union of size at most $n$ per node; $O(s)$ word operations when $n$ fits in a word |
| COUNT | $O(s)$ additions | the numbers have at most $n + 1$ bits |
| ARITH | $O(s)$ operations in $\mathbb{F}_p$ | |
| PROBABLY-EQUAL | $O(t s)$ operations in $\mathbb{F}_p$ | error at most $(n/p)^t$, only when the functions differ |
| NOT | $O(s)$ | copy with the sinks exchanged |
| space | $O(s)$ | nodes, the unique table and the per-call arrays |

Here $s$ is the number of nodes that the root reaches. For PROBABLY-EQUAL it is the sum for the two roots.

## Variants

- **[OBDDs](/ordered-binary-decision-diagram/).** The special case with one order for all paths. Reduced OBDDs are canonical, so equality is $O(1)$, and APPLY is polynomial.
- **Graph-driven BDDs (FBDDs of a fixed type).** Fix a *graph order*: a read-once diagram with one sink in which every path tests every variable once. An FBDD *respects* it if every input tests its variables in the order that the graph order gives for that input. For a fixed graph order the reduced FBDD is canonical, and APPLY, quantification and equality run in polynomial time, as for OBDDs (Gergov and Meinel 1994, Sieling and Wegener 1995). For example, the unreduced HWB construction, with its two sinks merged, is a graph order, and the reduced HWB diagram respects it.
- **Semantic read-once diagrams.** Only the paths that some input follows must be read-once. Counting and the reachability test for satisfiability fail for them.
- **Read-$k$ BDDs** allow $k$ tests of a variable on a path, and **nondeterministic** or **parity** FBDDs allow nodes that combine two children by OR or XOR.

## When to use it

Use FBDDs when a function has no small OBDD for any order, but has a small diagram whose order can depend on the data, as for the hidden weighted bit function. They are also a target of knowledge compilation, where a formula is compiled once and then many counting or satisfiability queries are answered in linear time; see [model counting](/model-counting/). If the functions must be combined often, use a fixed graph order, or stay with OBDDs.

## Pitfalls

- **No canonical form.** Two reduced FBDDs of one function can differ, so equal ids do not follow from equal functions. Use PROBABLY-EQUAL, or a fixed graph order.
- **Freeness is global.** MK cannot check it locally; a node can be free in one diagram and part of a repeated test in another. Run IS-FREE before COUNT or ARITH, which give wrong answers on diagrams that are not free.
- **The prime must be large.** The error bound is $n/p$ per trial. With a small prime, many distinct functions get equal fingerprints.
- **Large counts.** COUNT works with numbers up to $2^n$, which need big integers for $n$ above the word size.

## Implementations

## History

Blum, Chandra and Wegman (1980) introduced free Boolean graphs and showed that their equivalence can be decided by a randomized polynomial algorithm, by evaluating the arithmetized graphs at random points. In complexity theory, read-once branching programs became a main model for lower bounds in the 1980s, with exponential bounds by Žák (1984) and Wegener (1988). After the success of OBDDs, Gergov and Meinel (1994) and Sieling and Wegener (1995) showed that FBDDs with a fixed graph order (a type) are canonical and support efficient operations, which made them a practical data structure. Sieling and Wegener used the hidden weighted bit function to show the gain over OBDDs.

## References
