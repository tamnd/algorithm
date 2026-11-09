---
tag: XZKWT3
kind: algorithm
slug: huet-unification
name: Huet's almost-linear unification
aliases:
- Huet unification
- union-find unification
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: First-order unification on a term DAG. Union-find merges the classes of nodes that must be equal, and one cycle test at the end does the occurs check. It runs in O(N α(N)) time.
solves: [unification-problem]
model: word-ram
complexity:
  vars: {N: the number of nodes of the term DAG of the two input terms}
  time: {worst: O(N α(N))}
  space: {extra: O(N)}
properties: {deterministic: true}
history:
  year: 1976
  people: [Gérard Huet]
  note: Huet gave the union-find unification algorithm in his thesis at the Université Paris VII, first for infinite rational trees and then with a final acyclicity test for finite terms.
prereqs: [unification-problem, term-dag, disjoint-set-forest, occurs-check]
see_also: [robinson-unification, paterson-wegman-unification, martelli-montanari-unification, most-general-unifier, union-find-amortized-bound, huet-pre-unification, cycle-detection-in-graph]
sources:
  - paper: "Gérard Huet, Résolution d'équations dans des langages d'ordre 1, 2, ..., ω, Thèse d'État, Université Paris VII (1976)"
    locator: the chapter on first-order unification (union-find on term graphs, rational trees, and the final test for finite terms)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press (1998)
    locator: Chapter 4 (unification of terms), the section on efficient unification algorithms
  - paper: "Franz Baader and Wayne Snyder, Unification theory, in Handbook of Automated Reasoning, volume I, Elsevier and MIT Press (2001)"
    locator: the section on syntactic unification and its almost-linear and linear algorithms
---

Huet's almost-linear unification solves the first-order [unification problem](/unification-problem/) in $O(N\,\alpha(N))$ time, where $N$ is the size of the [term DAG](/term-dag/) of the input and $\alpha$ is the inverse Ackermann function. It keeps a [union-find](/disjoint-set-forest/) structure on the nodes of the DAG. Each class holds nodes that every unifier must make equal. When two classes with function nodes merge, their arguments must be equal, so they are merged too. The [occurs check](/occurs-check/) is not done at each step: a single cycle test on the classes at the end replaces it. Gérard Huet gave the algorithm in his thesis in 1976. This is a different algorithm from [Huet's pre-unification](/huet-pre-unification/) (1975), which is a search for higher-order terms.

## In plain words

Put both terms in one drawing where equal parts are shared. Every point of the drawing starts in its own group. The two roots must be equal, so put their groups together. When a group gets two points that both start with a function symbol, the symbols must be the same, and their children must also be equal, so put the groups of the children together too. A variable just joins whatever group it is put in. When nothing is left to join, look at the groups as a map: a group points to the groups of its children. If you can walk in a circle on this map, some variable would have to contain itself, so there is no answer. If not, read the answer off the groups.

## The problem

The input is two first-order terms $s$ and $t$, given as nodes of one term DAG with $N$ nodes. A node is a variable or a function node with a symbol $f$ of arity $k$ and $k$ children. The output is a [most general unifier](/most-general-unifier/) of $s$ and $t$, or *fail* if there is none.

## The algorithm

Each class of the union-find structure has a *schema*: a function node of the class if it has one, and otherwise a variable of the class.

```pseudo id=main
HUET-UNIFY(s, t)                       ▷ s and t are nodes of one term DAG
L1  make each node a class of its own, with itself as the schema
L2  S ← a stack with the pair (s, t)
L3  while S is not empty do
L4      (u, v) ← pop(S)
L5      u ← FIND(u), v ← FIND(v)
L6      if u = v then continue
L7      a ← schema(u), b ← schema(v)
L8      if a and b are both function nodes then
L9          if a and b have different symbols or arities then return fail
L10         UNION(u, v), with the schema a
L11         push (a_i, b_i) on S, for each argument place i
L12     else UNION(u, v), with a function node as the schema if a or b is one
L13 G ← the graph with an edge from each class to the class of each child of its schema
L14 search G for a cycle
L15 if G has a cycle then return fail                ▷ this is the occurs check
L16 return σ, where σ(x) is the term read from the schema of the class of x
```

In line L16 the term of a class is read from its schema: a function node gives its symbol with the terms of the classes of its children, and a variable gives itself. If the schema of the class of $x$ is $x$, then $\sigma$ does not change $x$. The graph $G$ has no cycle, so the reading stops. The result is best kept as a DAG, with one node for each class, because as a tree it can have size exponential in $N$.

## Example

Unify $s = f(X, g(Y))$ with $t = f(g(Z), X)$.

| step | pair taken | action | classes after the step |
|---|---|---|---|
| 1 | $(s, t)$ | both start with $f$: merge, push $(X, g(Z))$ and $(g(Y), X)$ | $\{s, t\}$ |
| 2 | $(g(Y), X)$ | $X$ is a variable: merge, schema $g(Y)$ | $\{X, g(Y)\}$ |
| 3 | $(X, g(Z))$ | schemas $g(Y)$ and $g(Z)$: merge, push $(Y, Z)$ | $\{X, g(Y), g(Z)\}$ |
| 4 | $(Y, Z)$ | two variables: merge, schema $Z$ | $\{Y, Z\}$ |

The classes are $\{s, t\}$, $\{X, g(Y), g(Z)\}$ and $\{Y, Z\}$. The graph has the edges $\{s, t\} \to \{X, \ldots\}$ (twice) and $\{X, \ldots\} \to \{Y, Z\}$, and no cycle. Reading the classes gives $\sigma = \{X \mapsto g(Z), Y \mapsto Z\}$, and $\sigma(s) = \sigma(t) = f(g(Z), g(Z))$.

For $X \doteq f(X)$, line L12 puts $X$ and $f(X)$ in one class with the schema $f(X)$. The child of the schema is $X$, which is in the same class, so $G$ has a loop and line L15 fails.

## Correctness

Write $\equiv$ for the final partition into classes. The full proof is in the [correctness proof](proofs/correctness.md). It has three parts.

1. **Each unifier respects the classes.** Each pair that is pushed must be equal under every unifier $\theta$: this holds for $(s, t)$, and if $\theta(a) = \theta(b)$ for two function nodes with the same symbol, then $\theta(a_i) = \theta(b_i)$. So $\theta$ is constant on each class. A clash in line L9 means two different symbols must be equal, and a cycle in $G$ means that the term of a class is a proper subterm of itself. In both cases there is no unifier.
2. **The classes are closed downward.** At the end, two function nodes in one class have the same symbol, and their children are pairwise in the same classes. This holds because each merge of two function schemas pushes their children, and the loop runs until the stack is empty.
3. **The result is a most general unifier.** By part 2, $\sigma$ maps each node of a class to the term of that class, so $\sigma(s) = \sigma(t)$. For each unifier $\theta$, induction over the acyclic graph $G$ gives $\theta(\sigma(x)) = \theta(x)$ for each variable $x$, so $\theta = \theta \circ \sigma$.

## Complexity

The algorithm makes at most $N - 1$ unions. A pair is pushed in line L11 only when the class of $b$ loses its function schema, which happens at most once for each function node. So the number of pushes, and of FIND calls, is at most the total arity of the DAG plus one, which is $O(N)$. With union by rank and path compression, the $O(N)$ operations take $O(N\,\alpha(N))$ time ([Tarjan's bound](/union-find-amortized-bound/)). The cycle test in lines L13 to L15 is one [depth-first search](/depth-first-search/) on a graph with at most $N$ nodes and $O(N)$ edges, so it takes $O(N)$ time. The space is $O(N)$. Since $\alpha(N) \le 4$ for any input that fits in a computer, the time is almost linear.

## Properties

- **Almost linear.** $O(N\,\alpha(N))$ time and $O(N)$ space.
- **One occurs check at the end.** The test is a single search for a cycle, not a test at each binding.
- **Works on shared terms.** The input and the output are DAGs. The mgu as a DAG has at most $N$ nodes.
- **Not online.** A failure of the occurs check is found only at the end, after all merges.

## Variants and improvements

- **Rational trees.** Without lines L13 to L15, the algorithm unifies over rational trees, the infinite trees with finitely many different subtrees. Huet developed it first for this setting. Prolog systems that omit the occurs check work in a similar setting.
- **Linear time.** [Paterson and Wegman](/paterson-wegman-unification/) (1978) gave a linear-time algorithm. It processes the classes in an order that makes union-find unnecessary, and detects cycles on the way.
- **Martelli and Montanari.** The [Martelli-Montanari algorithm](/martelli-montanari-unification/) (1982) works on multi-equations and selects the variable to eliminate with counters. It is also almost linear and finds cycles early.
- **Incremental use.** Unification in Prolog and in type inference often works with union-find on variables in a similar way, but binds variables one at a time and undoes the bindings on backtracking.

## When to use it

Use it when terms are large or shared, and when an almost-linear bound matters, for example in type inference for languages with polymorphic types or in theorem provers that unify big terms. The algorithm is simple and has small constant factors, so it is often faster in practice than the linear Paterson-Wegman algorithm. For small terms, [Robinson's algorithm](/robinson-unification/) with a careful occurs check is often fine.

## Pitfalls

- **Losing the function schema.** When a variable class meets a function class, the merged class must keep the function node as its schema (line L12). Otherwise the arguments of a later function node are never compared.
- **Skipping the cycle test.** Without it, $X \doteq f(X)$ succeeds. The result is a rational tree, not a finite term.
- **Reading the result as a tree.** The mgu of $h(X_1, \ldots, X_n) \doteq h(f(X_0, X_0), \ldots, f(X_{n-1}, X_{n-1}))$ has a term of size $2^{n+1} - 1$ for $X_n$. Keep it as a DAG.
- **Only one union strategy.** Path compression alone, or union by rank alone, gives a worse bound. Use both to get $O(N\,\alpha(N))$.

## Implementations

## History

Huet described the algorithm in his Thèse d'État at the Université Paris VII in 1976, "Résolution d'équations dans des langages d'ordre 1, 2, ..., ω". He first solved equations over infinite rational trees with union-find, and then added the acyclicity test for finite terms. The same thesis treats higher-order unification, which is the subject of his [pre-unification procedure](/huet-pre-unification/). Paterson and Wegman published a linear algorithm in 1978, and Martelli and Montanari published their algorithm in 1982.

## References
