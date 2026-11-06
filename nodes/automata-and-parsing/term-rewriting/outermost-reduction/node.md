---
tag: 1DTK3Q
kind: algorithm
slug: outermost-reduction
name: Outermost (leftmost-outermost) reduction
aliases:
- leftmost-outermost reduction
- normal-order reduction
area: automata-and-parsing/term-rewriting
level: core
summary: Always contracts the leftmost outermost redex; normalizing for left-normal orthogonal systems and for the lambda calculus.
solves: [normal-form-computation]
model: word-ram
complexity:
  vars: {n: the size of the input term, k: the number of rewrite steps, N: the largest size of a term in the reduction written as a tree, m: the largest size of a rule side, r: the number of rules}
  time: {worst: O((k + 1) N r m)}
  space: {extra: O(N)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1977
  people: [Michael J. O'Donnell]
  note: O'Donnell proved that leftmost-outermost reduction is normalizing for left-normal orthogonal systems, and parallel-outermost reduction for all orthogonal systems.
prereqs: [rewrite-step, reduction-strategy, normal-form, term-matching]
see_also: [innermost-reduction, normal-form-computation, orthogonal-rewrite-system, standardization-theorem, beta-reduction, graph-reduction, combinatory-logic, weak-normalization]
sources:
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 9, Strategies (outermost strategies, left-normal systems and needed reduction); Chapter 4, Orthogonality
  - paper: doi:10.1007/3-540-08531-9
    title: Michael J. O'Donnell, Computing in Systems Described by Equations, Lecture Notes in Computer Science 58, Springer, 1977
    locator: Chapter V, Termination (pp. 40 to 53, outermost strategies for regular systems)
  - paper: "Gérard Huet and Jean-Jacques Lévy, Computations in orthogonal rewriting systems, I and II, in J.-L. Lassez and G. Plotkin (editors), Computational Logic, Essays in Honor of Alan Robinson, MIT Press, 1991"
    locator: pp. 395 to 443 (needed redexes and strongly sequential systems)
  - book: isbn:9780444875082
    title: Henk P. Barendregt, The Lambda Calculus, Its Syntax and Semantics, revised edition, North-Holland, 1984
    locator: Chapter 13, Reduction strategies (the normalization theorem for leftmost reduction)
---

**Outermost reduction** computes a [normal form](/normal-form/) of a term by always contracting an outermost redex, one that does not lie inside another redex. The leftmost-outermost variant, also called normal-order reduction, takes the leftmost of them. It rewrites a function call before its arguments, so an argument that the rule throws away is never evaluated. This makes it **normalizing** where innermost reduction is not: in the lambda calculus and in left-normal [orthogonal](/orthogonal-rewrite-system/) systems, it reaches the normal form of every term that has one. The price is that an argument copied by a rule may be evaluated many times, which lazy evaluation repairs with sharing.

## In plain words

To evaluate an expression, look at it from the top. If a rule applies to the whole expression, apply it now, without simplifying the parts first. If not, go into the parts from left to right and do the same there. After every step, start again from the top.

This is how lazy languages think: a function gets its inputs unevaluated, and an input is computed only when a rule needs to look inside it. An input that is never needed is never computed, so a computation that would run forever in that input does no harm. The cost is that if a rule makes several copies of an input before it is computed, each copy may be computed separately.

## The problem

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, subterm $t|_p$ and replacement $t[s]_p$, substitutions $\sigma$ applied as $t\sigma$, rules $l \to r$ with $l \notin V$ and $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$, and $\to_R^*$ the reflexive transitive closure of the rewrite relation of a [term rewriting system](/term-rewriting-system/) $R$.

The input is a finite list of rules $R$, a term $t$ and optionally a step bound $B$. The output is a normal form $v$ with $t \to_R^* v$, as in the [normal form computation](/normal-form-computation/) problem, or a report that $B$ steps did not reach one.

A position $p$ of $t$ is a **redex** if $t|_p = l\tau$ for some rule $l \to r$; it is **outermost** if no proper prefix of $p$ is a redex. Distinct outermost redexes are side by side, and the **leftmost-outermost** [strategy](/reduction-strategy/) contracts the leftmost of them, with the first rule of the list that matches there.

## The algorithm

The leftmost-outermost redex is the first redex in preorder, the order "node, then its children from left to right". So each step is one preorder search, with an explicit stack, followed by a replacement along the path to the redex.

```pseudo id=main
OUTERMOST(t, R, B)                         ▷ B is a step bound, or ∞
L1  steps ← 0
L2  loop
L3      search the positions of t in preorder for the first p and the first rule l → r with t|p = lτ
L4      if there is none then return (t, steps)           ▷ t is a normal form
L5      if steps = B then return ⊥                       ▷ bound reached
L6      t ← t[rτ]p                                       ▷ rebuild the path from p up to the root
L7      steps ← steps + 1
```

Line L3 pops a position, tries the rules there by [term matching](/term-matching/), and if none matches pushes the children with the leftmost on top. The search stops at the first redex, so a step near the root costs little even in a huge term. The search keeps the path to each position as a linked list, so that going one level down costs $O(1)$, and line L6 copies only the nodes on the path; the rest of the term is shared.

## Example

The rules, numbered 0 to 3, describe the infinite list $0, 1, 2, \ldots$ of numerals $s^i(0)$:

$$\mathit{from}(x) \to \mathit{cons}(x, \mathit{from}(s(x))), \quad \mathit{hd}(\mathit{cons}(x, y)) \to x, \quad \mathit{tl}(\mathit{cons}(x, y)) \to y, \quad \mathit{loop} \to \mathit{loop}.$$

Take $t = \mathit{hd}(\mathit{tl}(\mathit{from}(0)))$, the second element of the list.

| step | position | rule | term after the step |
|---|---|---|---|
| 1 | $1\,1$ | 0 | $\mathit{hd}(\mathit{tl}(\mathit{cons}(0, \mathit{from}(s(0)))))$ |
| 2 | $1$ | 2 | $\mathit{hd}(\mathit{from}(s(0)))$ |
| 3 | $1$ | 0 | $\mathit{hd}(\mathit{cons}(s(0), \mathit{from}(s(s(0)))))$ |
| 4 | $\varepsilon$ | 1 | $s(0)$ |

In step 1 neither $\mathit{hd}(\ldots)$ nor $\mathit{tl}(\mathit{from}(0))$ matches a rule, so the first redex in preorder is $\mathit{from}(0)$. In step 2 the root still does not match, and $\mathit{tl}(\mathit{cons}(\ldots))$ at position $1$ is the first redex, above the redex $\mathit{from}(s(0))$. In step 4 the redex $\mathit{from}(s(s(0)))$ is thrown away without being touched. [Innermost reduction](/innermost-reduction/) on the same term never stops: after step 1 the innermost redex is $\mathit{from}(s(0))$, then $\mathit{from}(s(s(0)))$, and so on. Likewise $\mathit{hd}(\mathit{cons}(a, \mathit{loop}))$ reaches $a$ in one outermost step, while innermost reduction contracts $\mathit{loop}$ forever.

## Correctness

Two facts show that the algorithm makes exactly the leftmost-outermost steps.

1. **The search visits the positions in preorder.** It pops a position, then the whole subtree of its first child, then that of its second child, and so on, by induction on the size of the subtree.
2. **The first redex in preorder is the leftmost-outermost redex.** Its proper prefixes come earlier in preorder and are not redexes, so it is outermost. Any other outermost redex is not its prefix and comes later in preorder, so it is to the right.

Replacing along the path gives $t[r\tau]_p$, and when the search finds no redex, every position was checked, so $t$ is a normal form. The full argument is in [the correctness proof](proofs/correctness.md).

Whether the sequence of leftmost-outermost steps ends is a property of the system, not of the algorithm:

- **Left-normal orthogonal systems.** A system is orthogonal if it is left-linear and has no [critical pairs](/critical-pair/), and left-normal if in every left side all function symbols come before all variables in preorder. For such systems, leftmost-outermost reduction is normalizing: if $t$ has a normal form, the algorithm reaches it (O'Donnell 1977). The reason is that the leftmost-outermost redex is **needed**: every reduction of $t$ to normal form contracts some copy of it.
- **The lambda calculus.** [Combinatory logic](/combinatory-logic/) is a left-normal orthogonal system, and for [beta-reduction](/beta-reduction/) the corresponding result is the normalization theorem, a consequence of the [standardization theorem](/standardization-theorem/).

The test file checks normalization on 1500 random left-normal orthogonal constructor systems: whenever the brute-force set of reachable terms is finite and contains a normal form, the algorithm returns that normal form.

## Complexity

Let $N$ be the largest size of a term in the reduction, counted as a tree. One search visits at most $N$ positions, tries at most $r$ rules at each, and matching a left-linear left side costs $O(m)$. Building $r\tau$ costs $O(m)$ because the values of $\tau$ are shared, and rebuilding the path costs $O(N)$ in the worst case. So $k$ steps and the final search take $O((k + 1)\, N\, r\, m)$ time on the [word RAM](/word-ram/), and the space is $O(N)$.

The bound is pessimistic when redexes are near the root, as with lazy data such as $\mathit{from}$: each search stops early. It is tight for deep redexes: computing $\mathit{add}(s^m(0), y)$ with $\mathit{add}(s(x), y) \to s(\mathit{add}(x, y))$ moves the redex one level down per step, so step $i$ walks a path of length $i$, and the total is $\Theta(m^2)$, against $\Theta(m)$ for innermost reduction. A machine that keeps its place, as in [graph reduction](/graph-reduction/) or an abstract machine for lazy languages, avoids restarting from the root.

**Duplication.** With $d(x) \to p(x, x)$, an unevaluated argument is copied, and in outermost reduction it is then evaluated once per copy. The number of steps can grow exponentially compared with innermost reduction. Sharing the copies as one node of a graph, so that evaluating one evaluates all, is the idea of lazy evaluation; see [graph reduction](/graph-reduction/).

## Properties

- **Normalizing on suitable systems.** See Correctness. On the lambda calculus this is why normal order is the reference strategy.
- **Not normalizing in general.** The orthogonal system $f(x, b) \to c$, $a \to a$, $d \to b$ is not left-normal, because $x$ comes before $b$. The term $f(a, d)$ has the normal form $c$, via $d \to b$, but the leftmost-outermost redex is $a$, and the algorithm contracts it forever. Parallel-outermost reduction, which contracts all outermost redexes at once, is normalizing for all orthogonal systems (O'Donnell 1977).
- **Non-orthogonal systems.** For overlapping rules, outermost reduction can miss normal forms and can return different normal forms depending on the order of the rules.

## Variants and improvements

- **Parallel-outermost.** Contract all outermost redexes in one round. Normalizing for every orthogonal system, at the cost of contracting redexes that may not be needed.
- **Needed reduction.** Huet and Lévy showed that in every orthogonal system each term that is not a normal form has a needed redex, and that contracting needed redexes is normalizing. Finding one is undecidable in general; strongly sequential systems are the class where a needed redex can be found by looking only at the left sides, and left-normal systems are a special case.
- **Lazy evaluation.** Outermost reduction on [term graphs](/term-graph-rewriting/) shares the copies of an argument, so each argument is evaluated at most once. Functional languages such as Haskell implement this by [graph reduction](/graph-reduction/).
- **Weak head normal form.** Evaluation stops when the root is a constructor or a $\lambda$, and the arguments stay unevaluated until a consumer needs them. This is what lazy languages compute.
- **Innermost reduction.** [Innermost reduction](/innermost-reduction/) evaluates the arguments first; it is cheaper per step and copies only normal forms, but it is not normalizing.

## When to use it

Use leftmost-outermost reduction when the system is not terminating but some terms have normal forms, in particular for lazy data structures, conditionals written as rules such as $\mathit{if}(\mathit{true}, x, y) \to x$, and the lambda calculus or combinatory logic. Check that the system is orthogonal and left-normal; otherwise use parallel-outermost reduction or a step bound. For a terminating system, [innermost reduction](/innermost-reduction/) is usually faster, because it never evaluates a copied argument twice and does not restart from the root.

## Pitfalls

- **Assuming normalization for every orthogonal system.** The leftmost choice is normalizing only with left-normality; see the example $f(a, d)$ above.
- **Restarting from the root naively with copied positions.** Building each position as a fresh tuple costs time proportional to the depth at each node, which makes a search on a deep term quadratic. Keep the path as a linked list, as the implementation does.
- **Exponential work from duplication.** Without sharing, a rule that copies an argument makes outermost reduction evaluate it once per copy. The terms built by the implementation share the copies in memory, but a preorder search still walks each copy, so $N$ counts the tree, not the graph.
- **Recursion on deep terms.** Terms such as $s^{n}(0)$ have depth $n$. Search, match, substitute and compare with explicit stacks; the implementation handles terms of depth $20000$.
- **Rule order.** On overlapping rules the first matching rule decides the result. Orthogonal systems avoid this, since at most one rule matches at a position.

## Implementations

## History

The normalization theorem for the lambda calculus, that leftmost reduction finds the normal form whenever there is one, goes back to Curry and Feys in 1958. For first-order term rewriting, O'Donnell's 1977 monograph proved that parallel-outermost reduction is normalizing for orthogonal (regular) systems and leftmost-outermost reduction for left-normal ones. Huet and Lévy, in a report of 1979 published in 1991, introduced needed redexes and strongly sequential systems, which explain these results and give a normalizing strategy for a larger class.

## References
