---
tag: DBR5MN
kind: data-structure
slug: binary-decision-diagram
name: Binary decision diagram
aliases:
- BDD
- binary-decision program
- Boolean branching program
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: A rooted DAG of decision nodes that test variables and represent a boolean function.
model: word-ram
complexity:
  vars: {p: the number of nodes of the BDD, l: the number of literal occurrences in the CNF formula, n: the number of variables}
  time: {evaluate: O(p), from_cnf: O(l), is_free: O(p·n), sat_free: O(p)}
  space: {nodes: O(p)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1959
  people: [C. Y. Lee, Sheldon B. Akers, Randal E. Bryant]
  note: Lee described binary-decision programs in 1959, Akers named binary decision diagrams in 1978, and Bryant made the ordered and reduced form the standard tool in 1986.
prereqs: [boolean-function, shannon-expansion, directed-acyclic-graph]
see_also: [ordered-binary-decision-diagram, reduced-ordered-bdd, branching-program, free-binary-decision-diagram, read-once-branching-program, decision-tree, decision-diagram, boolean-equivalence-checking]
sources:
  - paper: doi:10.1002/j.1538-7305.1959.tb01585.x
    title: C. Y. Lee, Representation of switching circuits by binary-decision programs, Bell System Technical Journal 38(4), 1959, pages 985 to 999
    locator: binary-decision programs as a representation of switching functions
  - paper: doi:10.1109/TC.1978.1675141
    title: Sheldon B. Akers, Binary decision diagrams, IEEE Transactions on Computers C-27(6), 1978, pages 509 to 516
    locator: the binary decision diagram of a function and its use to analyse and test digital circuits
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 2, Definitions 1 and 2 (function graphs and the function of a vertex), and the introduction (the earlier unordered diagrams of Lee and Akers)
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 2, Branching programs and decision trees, and Chapter 6, FBDDs and read-once branching programs
---

A binary decision diagram (BDD) is a rooted [directed acyclic graph](/directed-acyclic-graph/) whose inner nodes each test one Boolean variable and have a low edge and a high edge, and whose two sinks are labelled 0 and 1. It represents the [Boolean function](/boolean-function/) that maps an input to the label of the sink that we reach when we follow the tests. With no rule on the order of the tests, a BDD is the same object as a [branching program](/branching-program/) on Boolean inputs: it is small for many functions, but deciding whether it is satisfiable is [NP-complete](/np-complete/). The restricted forms, the [ordered BDD](/ordered-binary-decision-diagram/) and the [reduced ordered BDD](/reduced-ordered-bdd/), give up some of this power and get fast operations and a canonical form in return.

## In plain words

A BDD is a flow chart of yes or no questions. Each box asks about one input: is it on? If yes, follow one arrow. If no, follow the other arrow. In the end you reach a box that says true or a box that says false. Unlike a tree, two arrows can point to the same box, so equal parts of the chart are drawn only once. This makes the chart small. In the general form on this page, any question can come in any place, and a question can even come again later on the same route. That freedom has a cost: the chart can have a route to true that no real input follows, so it is hard to tell whether true can ever be the answer.

## The abstract type

A BDD over the variables $x_1, \ldots, x_n$ stores one or more Boolean functions in $B_n$, one for each root. The operations on this page are:

- EVAL$(u, x)$: the value $f_u(x)$ for an input $x \in \{0,1\}^n$.
- FROM-CNF$(F)$: a BDD for a formula in [conjunctive normal form](/conjunctive-normal-form/).
- IS-FREE$(r)$: does some path from $r$ test a variable twice?
- SAT-FREE$(r)$: is $f_r$ satisfiable, for a root $r$ where IS-FREE is true?

Satisfiability and equality of two general BDDs are also questions of the type, but they have no fast algorithm unless P = NP; see the section on complexity.

## Representation

The terminals 0 and 1 are the nodes with ids 0 and 1. An inner node $u$ is a triple $(\mathrm{var}(u), \mathrm{lo}(u), \mathrm{hi}(u))$, stored in an array. A new node gets the next free id, and its children already exist, so each child has a smaller id than its parent. This keeps the graph acyclic, and the order of the ids is a [topological order](/topological-sort/). Nodes are never changed after they are made, so a root that was returned once stays valid, and many roots can share nodes.

The function of a node is defined from the bottom up:

$$f_0 = 0, \qquad f_1 = 1, \qquad f_u = (\neg x_i \wedge f_{\mathrm{lo}(u)}) \vee (x_i \wedge f_{\mathrm{hi}(u)}) \text{ with } i = \mathrm{var}(u).$$

This is the [Shannon expansion](/shannon-expansion/) drawn as a node. In a general BDD the children may still depend on $x_i$, so $f_{\mathrm{lo}(u)}$ and $f_{\mathrm{hi}(u)}$ need not be the [cofactors](/cofactor/) of $f_u$. The **size** $|B|$ is the number of nodes, terminals included, as in Knuth's $B(f)$.

The pages of this area use these restrictions of the same representation:

| structure | rule on the paths | satisfiability | equivalence | canonical |
|---|---|---|---|---|
| BDD (this page) | none | NP-complete | co-NP-complete | no |
| [free BDD](/free-binary-decision-diagram/) | each variable at most once on each path | $O(p)$ | randomized polynomial time | no |
| [ordered BDD](/ordered-binary-decision-diagram/) | one fixed variable order on all paths | $O(p)$ | polynomial, for the same order | no |
| [reduced ordered BDD](/reduced-ordered-bdd/) | ordered, and no redundant or duplicate node | $O(1)$ | $O(1)$ with a unique table | yes |

## Operations

```pseudo id=main
EVAL(u, x)
L1  while u is not a terminal do
L2      if x[var(u)] = 1 then u ← hi(u) else u ← lo(u)
L3  return the label of u

FROM-CNF(C_1, ..., C_m)              ▷ a BDD for C_1 ∧ ... ∧ C_m
L4  s ← the terminal 1
L5  for j ← m downto 1 do
L6      t ← the terminal 0
L7      for each literal ℓ of C_j, from the last to the first do
L8          if ℓ = x_v then t ← NODE(v, lo = t, hi = s)
L9          else t ← NODE(v, lo = s, hi = t)    ▷ ℓ = ¬x_v
L10     s ← t
L11 return s

IS-FREE(r)
L12 for each node u reachable from r, children before parents do
L13     D[u] ← ∅ if u is a terminal, else D[lo(u)] ∪ D[hi(u)] ∪ {var(u)}
L14     if u is not a terminal and var(u) ∈ D[lo(u)] ∪ D[hi(u)] then return false
L15 return true

SAT-FREE(r)                          ▷ only for a free BDD
L16 return true if the terminal 1 is reachable from r, else false
```

FROM-CNF builds one chain of nodes per clause. In the chain of $C_j$, a literal that is true sends the walk to the start of the chain of $C_{j+1}$, and a literal that is false sends it to the next literal of $C_j$. After the last literal it goes to the terminal 0. This is the reason that a general BDD can have a path to 1 that no input follows: a later clause may test a variable again, with the other value.

The same idea gives the Boolean operations in linear size. For $f_r \wedge f_s$, take a copy of the BDD of $r$ and send each edge into its terminal 1 to $s$ in place of 1. For $f_r \vee f_s$, send each edge into the terminal 0 to $s$. For $\neg f_r$, swap the labels of the two terminals. These constructions break the free and ordered properties, which is why the restricted forms use [APPLY](/bdd-apply/) in place of them.

## Example

Let $F = (x_1 \vee \neg x_2) \wedge (x_2 \vee x_3) \wedge (\neg x_1 \vee \neg x_3)$. FROM-CNF reads the clauses from the last to the first and makes six inner nodes:

| node | var | lo | hi | function |
|---|---|---|---|---|
| $a$ | $x_3$ | 1 | 0 | $\neg x_3$ |
| $b$ | $x_1$ | 1 | $a$ | $\neg x_1 \vee \neg x_3$ |
| $c$ | $x_3$ | 0 | $b$ | $x_3 \wedge (\neg x_1 \vee \neg x_3)$ |
| $d$ | $x_2$ | $c$ | $b$ | $(x_2 \vee x_3) \wedge (\neg x_1 \vee \neg x_3)$ |
| $e$ | $x_2$ | $d$ | 0 | $\neg x_2 \wedge f_d$ |
| $g$ | $x_1$ | $e$ | $d$ | $F$ |

With the two terminals the size is 8. The root is $g$. The input $(x_1, x_2, x_3) = (1, 1, 0)$ follows $g \to d \to b \to a \to 1$, and $(0, 0, 1)$ follows $g \to e \to d \to c \to b \to 1$. These are the only two models of $F$.

The BDD is not free: the path $g \to d \to b$ tests $x_1$ twice, so IS-FREE$(g)$ returns false. The path $g \to e \to d \to b \to 1$, which leaves $g$ by its lo-edge, leaves $e$ by its lo-edge ($x_2 = 0$), leaves $d$ by its hi-edge ($x_2 = 1$) and leaves $b$ by its lo-edge, reaches 1 but asks for $x_2 = 0$ and $x_2 = 1$. No input follows it. Here $F$ is satisfiable anyway, but for $x_1 \wedge \neg x_1$ FROM-CNF gives a BDD where 1 is reachable only by such a path, and the function is 0.

## Correctness

The function of a node is defined from its children, and EVAL keeps $f_u(x)$ unchanged at each step, so it returns $f_u(x)$. FROM-CNF keeps the invariant that after the clauses $C_j, \ldots, C_m$ are done, $f_s = C_j \wedge \cdots \wedge C_m$. Inside a clause, the node for a literal $\ell$ in front of a node for $D \wedge G$ has the function $(\ell \wedge G) \vee (\neg \ell \wedge D \wedge G) = (\ell \vee D) \wedge G$. IS-FREE finds each node that has a node with its own variable below it. SAT-FREE is correct because in a free BDD every path to 1 tests each variable at most once, so it fixes a consistent partial input. The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

Let $p$ be the number of nodes reachable from the root and $\ell$ the number of literal occurrences of the CNF formula.

- EVAL visits each node at most once, since the ids decrease along the walk, so it takes $O(p)$ time. In a free BDD a path has at most $n$ inner nodes, so EVAL takes $O(n)$ time.
- FROM-CNF makes one node per literal occurrence. It takes $O(\ell)$ time, and its result has at most $\ell + 2$ nodes.
- IS-FREE takes $O(p)$ set unions of subsets of $\{1, \ldots, n\}$, so $O(p\,n)$ time with sets of size $n$ and $O(p \lceil n / w \rceil)$ word operations with bit masks of $w$-bit words.
- SAT-FREE is one graph search, $O(p)$ time.

**Hardness.** For general BDDs, satisfiability is NP-complete and equivalence is [co-NP-complete](/co-np-complete/). Satisfiability is in NP, since a model is checked with EVAL in $O(p)$ time. It is NP-hard, since FROM-CNF turns a CNF formula into a BDD for the same function in linear time, and [SAT](/sat/) for CNF formulas is NP-complete. For equivalence, $f_r \neq f_s$ has the witness $x$ with $f_r(x) \neq f_s(x)$, so inequivalence is in NP. And $f_r$ is equivalent to the terminal 0 exactly when $f_r$ is not satisfiable, so equivalence is co-NP-hard.

For free BDDs, equivalence can be decided in randomized polynomial time: Blum, Chandra and Wegman (1980) replace each node by a polynomial over a large field and compare the two polynomials at a random point, as in [polynomial identity testing](/polynomial-identity-testing/). No deterministic polynomial-time algorithm is known. For ordered BDDs with the same order, the [reduction rules](/bdd-reduction-rules/) and [canonicity](/bdd-canonicity/) give a deterministic linear-time test.

## Variants

- **[Free BDD](/free-binary-decision-diagram/)** (FBDD, [read-once branching program](/read-once-branching-program/)): each path tests each variable at most once. Satisfiability is reachability.
- **[Ordered BDD](/ordered-binary-decision-diagram/)**: all paths test the variables in the order of one fixed permutation. Bryant's APPLY works on two ordered BDDs with the same order.
- **[Reduced ordered BDD](/reduced-ordered-bdd/)**: an ordered BDD with no node whose two children are equal and no two nodes with the same triple. For a fixed order it is unique.
- **BDDs with repeated tests**: a variable may be tested up to $k$ times on each path. Wegener (2000, Chapter 7) studies their size.
- **[Decision diagrams](/decision-diagram/)** in general: more than two terminal values, more than two edges per node, or other decomposition rules, as in [zero-suppressed BDDs](/zero-suppressed-bdd/) and [algebraic decision diagrams](/algebraic-decision-diagram/).
- **[Decision tree](/decision-tree/)**: a BDD whose graph is a tree. It shares no nodes, so it can be exponentially larger.

## When to use it

Use the general form as a model of computation. The size of the smallest BDD of a function is the size of its smallest branching program, and lower bounds on this size are lower bounds on space for non-uniform computation: functions with branching programs of polynomial size are exactly the functions in non-uniform logarithmic space. Use the general form also when the only operation is evaluation, for example to run a fixed rule set fast, since it can be smaller than any ordered form.

For symbolic work, where the program builds functions with AND, OR and quantifiers and asks whether two functions are equal, use the [reduced ordered BDD](/reduced-ordered-bdd/). Its operations take polynomial time in the sizes of the inputs, and equality is one comparison.

## Pitfalls

- **Reachability is not satisfiability.** A general BDD can reach the terminal 1 on a path that tests a variable twice with two values. Only for free BDDs does reachability of 1 decide satisfiability.
- **The children are not the cofactors.** If the children of a node on $x_i$ may test $x_i$ again, $f_{\mathrm{lo}(u)}$ need not equal $f_u|_{x_i=0}$. Algorithms that recurse on the cofactors, such as APPLY and RESTRICT, need the ordered form.
- **Not canonical.** One function has many BDDs, even with the same number of nodes, so equal graphs are not a test for equal functions unless the BDD is reduced and ordered.
- **Size conventions differ.** Knuth counts the two terminals in $B(f)$. Some papers count only inner nodes, so their numbers are smaller by 2.

## Implementations

## History

Lee (1959) introduced binary-decision programs as a way to represent switching circuits: a program is a list of instructions that each test one variable and jump to one of two places. Akers (1978) drew such programs as graphs, named them binary decision diagrams, and used them to analyse and test digital circuits. Blum, Chandra and Wegman (1980) showed that equivalence of free BDDs can be decided in randomized polynomial time. Bryant (1986) restricted the diagrams to one variable order and to reduced form, proved that this form is canonical, and gave polynomial algorithms for the Boolean operations. This made BDDs a standard data structure for verification and logic synthesis. Wegener (2000) surveys the theory of branching programs and of each restricted class.

## References
