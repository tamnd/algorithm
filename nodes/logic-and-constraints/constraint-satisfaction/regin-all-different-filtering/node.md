---
tag: A7F2AJ
kind: algorithm
slug: regin-all-different-filtering
name: Régin's all-different filtering
aliases:
- Régin's algorithm
- matching-based alldifferent propagation
- GAC for alldifferent
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Filters the domains of an all-different constraint to generalized arc consistency with one maximum matching of the value graph and one strongly connected components pass, in O(n^(3/2) d) time.
model: word-ram
complexity:
  vars: {n: the number of variables of the constraint, d: the largest domain size}
  time: {worst: O(n^(3/2) d)}
  space: {extra: O(n d)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1994
  people: [Jean-Charles Régin]
  note: Régin gave the filter at AAAI-94. He stated the time as O(p^2 d^2) for p variables. With the Hopcroft-Karp matching the bound is O(p^(1/2) E) for E edges of the value graph, as in later surveys.
prereqs: [all-different-constraint, bipartite-matching, berge-lemma, strongly-connected-components]
see_also: [global-constraint, hopcroft-karp, hall-theorem, alternating-path, tarjan-scc, arc-consistency, bounds-consistency, maintaining-arc-consistency]
sources:
  - paper: "Jean-Charles Régin, A filtering algorithm for constraints of difference in CSPs, Proceedings of the 12th National Conference on Artificial Intelligence (AAAI-94), 1994, pages 362 to 367"
    locator: the value graph, the property of edges that belong to some maximum matching (taken from Berge), the filtering algorithm and its complexity
  - paper: doi:10.1137/0202019
    title: John E. Hopcroft and Richard M. Karp, An n^(5/2) algorithm for maximum matchings in bipartite graphs, SIAM Journal on Computing 2(4), 1973
    locator: pages 225 to 231 (the phase bound and the O(sqrt(V) E) time)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 1972
    locator: pages 146 to 160 (strongly connected components in linear time)
  - paper: "Willem-Jan van Hoeve, The alldifferent constraint, a survey, 2001, arXiv:cs/0105015"
    locator: the section on generalized arc consistency (Régin's filter, the O(m sqrt(n)) bound, and the comparison with the binary decomposition and bounds consistency)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 6, Global constraints, by Willem-Jan van Hoeve and Irit Katriel (the alldifferent constraint and its filters)
---

Régin's all-different filtering is the algorithm that makes an [all-different constraint](/all-different-constraint/) generalized arc consistent: it removes from each domain exactly the values that belong to no solution of the constraint. It finds one maximum [matching](/bipartite-matching/) in the bipartite graph of variables and values, orients the edges by the matching, and keeps an edge only if it is in the matching, in a [strongly connected component](/strongly-connected-components/), or on a path from an unmatched value. The proof rests on [Berge's lemma](/berge-lemma/) on alternating paths and cycles. With the [Hopcroft-Karp](/hopcroft-karp/) matching it runs in $O(n^{3/2} d)$ time for $n$ variables with domains of size at most $d$.

## In plain words

Each variable must get its own value, and no two variables may share a value. Draw the variables on the left, the values on the right, and a line from each variable to each of its possible values. A full solution picks one line for each variable, with no value used twice. This is a matching.

The filter finds one such matching. Then it asks, for each line not in it: can I swap some lines so that this line is used and every variable still has its own value? A swap works along a closed loop of alternating lines, or along a chain that starts at a value nobody uses. A graph search finds all loops and chains at the same time. Each line with no loop and no chain cannot occur in any solution, so the filter deletes that value.

## The problem

The input is a constraint all-different$(x_1, \ldots, x_n)$ with finite domains $D(x_1), \ldots, D(x_n)$. Its solutions are the tuples $(a_1, \ldots, a_n)$ with $a_i \in D(x_i)$ and $a_i \ne a_j$ for $i \ne j$. A value $a \in D(x_i)$ has a *support* if some solution has $a_i = a$. The constraint is *generalized arc consistent* (GAC) if each value of each domain has a support. The output is the largest GAC subdomains: the domains with every unsupported value removed, or "failure" if the constraint has no solution.

The *value graph* $G$ is the bipartite graph with the variables on one side, the values $\bigcup_i D(x_i)$ on the other side, and an edge $\{x_i, a\}$ for each $a \in D(x_i)$. Let $E = \sum_i |D(x_i)| \le n d$ be its number of edges. A solution is exactly a matching of $G$ that covers every variable. Notation: $n$ is the number of variables of the constraint and $d$ the largest domain size, as on the other pages of this area.

## The algorithm

```pseudo id=main
REGIN-FILTER(x_1, ..., x_n, D)
L1  build the value graph G: an edge {x, a} for each variable x and each a ∈ D(x)
L2  M ← a maximum matching of G                      ▷ Hopcroft-Karp
L3  if |M| < n then return failure                    ▷ no solution
L4  orient G: each edge of M from x to a, each other edge from a to x
L5  R ← the vertices reachable from a free value     ▷ a value that M does not cover
L6  compute the strongly connected components of the oriented graph
L7  for each edge {x, a} of G do
L8      if {x, a} ∉ M and a ∉ R and x, a are in different components then
L9          remove a from D(x)
L10 return D
```

Line L3 uses [Hall's theorem](/hall-theorem/) in its matching form: a matching that covers all variables exists exactly when the constraint has a solution, and then every maximum matching covers all variables. After line L4, the only edge that leaves a variable $x$ is its matched edge $x \to M(x)$, and the edges that leave a value are its unmatched edges. So a directed path alternates between unmatched and matched edges. Line L5 is one breadth-first search from all free values at once. Line L6 is [Tarjan's algorithm](/tarjan-scc/) or any linear-time method. Line L8 keeps an unmatched edge $a \to x$ in two cases: it lies on a directed cycle (same component), or it lies on a directed path from a free value (then $a$ itself is reachable).

## Example

Let $D(x_1) = D(x_2) = \{1, 2\}$, $D(x_3) = \{1, 2, 3, 4\}$, $D(x_4) = \{2, 3, 4\}$ and $D(x_5) = \{3, 5, 6\}$. The value graph has 14 edges.

| step | result |
|---|---|
| L2 | $M = \{x_1\text{-}1, x_2\text{-}2, x_3\text{-}3, x_4\text{-}4, x_5\text{-}5\}$, size 5, so line L3 passes |
| L4 | matched edges $x_i \to i$; unmatched edges $2 \to x_1$, $1 \to x_2$, $1 \to x_3$, $2 \to x_3$, $4 \to x_3$, $2 \to x_4$, $3 \to x_4$, $3 \to x_5$, $6 \to x_5$ |
| L5 | the free value is 6; $R = \{6, x_5, 5\}$ |
| L6 | components $\{x_1, x_2, 1, 2\}$, $\{x_3, x_4, 3, 4\}$, $\{x_5\}$, $\{5\}$, $\{6\}$ |
| L8 | remove 1 and 2 from $D(x_3)$, 2 from $D(x_4)$, 3 from $D(x_5)$ |

The cycle $x_3 \to 3 \to x_4 \to 4 \to x_3$ keeps the edges $x_3$-4 and $x_4$-3. The path $6 \to x_5 \to 5$ keeps $x_5$-6. The result is $D(x_3) = D(x_4) = \{3, 4\}$ and $D(x_5) = \{5, 6\}$, and $D(x_1), D(x_2)$ do not change. In words: $x_1$ and $x_2$ use up the values 1 and 2 (a Hall set), then $x_3$ and $x_4$ use up 3 and 4. The four removed values are exactly the values in no solution.

The binary decomposition into ten constraints $x_i \ne x_j$ removes nothing here, because no domain is a single value. The smallest example of the gap is $D(x_1) = D(x_2) = D(x_3) = \{1, 2\}$: each $x_i \ne x_j$ is arc consistent, since each value has a different partner, but the constraint has no solution, and line L3 reports failure.

## Correctness

The key fact is a lemma from matching theory. Let $M$ be a maximum matching. An edge $e \notin M$ is in some maximum matching if and only if $e$ lies on an alternating cycle of even length, or on an alternating path of even length that starts at a vertex that $M$ does not cover. The proof takes the symmetric difference of $M$ with a maximum matching that holds $e$, as in the proof of [Berge's lemma](/berge-lemma/). In the oriented graph, these cycles are the directed cycles and these paths are the directed paths from a free value. So line L8 removes an edge exactly when no maximum matching holds it, that is, exactly when its value has no support.

**Theorem.** REGIN-FILTER returns failure if and only if the constraint has no solution. Otherwise it returns the largest GAC subdomains: a value stays in $D(x)$ if and only if some solution gives it to $x$. The full proof is below.

**Strictly stronger than the binary decomposition.** Write $C_{\ne}$ for the set of binary constraints $x_i \ne x_j$, $i < j$. If the all-different constraint is GAC, then each $x_i \ne x_j$ is arc consistent: a support of $a \in D(x_i)$ in the constraint gives a value of $x_j$ different from $a$. The converse is false, by the three-variable example above. A second example shows that GAC can remove values even when it does not fail: with $D(x_1) = D(x_2) = \{1, 2\}$ and $D(x_3) = \{1, 2, 3\}$, arc consistency on $C_{\ne}$ removes nothing, and REGIN-FILTER removes 1 and 2 from $D(x_3)$. Arc consistency on $C_{\ne}$ removes a value $a$ from $D(x_j)$ only when some $D(x_i) = \{a\}$, so it never sees a set of $k$ variables that share $k$ values.

## Complexity

- **Matching (line L2).** Hopcroft and Karp proved that their algorithm uses $O(\sqrt{s})$ phases, where $s \le n$ is the size of a maximum matching, and each phase takes $O(V + E)$ time. Only values that occur in some domain are vertices, so $V \le n + E$. The matching takes $O(\sqrt{n}\, E)$ time.
- **Lines L1, L4 to L9.** Building and orienting the graph, one breadth-first search and one strongly connected components pass take $O(n + E)$ time.
- **Total.** $O(\sqrt{n}\, E) \subseteq O(n^{3/2} d)$ in the worst case, in the word-RAM, since $E \le n d$. The space is $O(n + E) = O(n d)$.

Régin's paper states the bound $O(p^2 d^2)$ for $p$ variables. In a search, the filter runs many times with small changes. The previous matching stays valid except at the edges that were removed, and each lost matched edge costs one augmenting-path search of $O(E)$ time to repair. Then lines L4 to L9 cost $O(n + E)$.

## Properties

- **Exact.** It reaches GAC, the strongest pruning that looks at this one constraint alone.
- **Idempotent.** A second call removes nothing, because each value that stays has a support.
- **Order independent.** The result does not depend on which maximum matching line L2 finds, because the set of supported values does not.
- **Deterministic and not recursive.** The implementation uses explicit stacks for the matching and the component search.

## Variants and improvements

- **Incremental use in search.** Keep the matching and the graph between calls, as described above. This is how solvers run it inside [maintaining arc consistency](/maintaining-arc-consistency/).
- **Bounds consistency.** Puget (1998) prunes only the bounds of interval domains in $O(n \log n)$ time, and López-Ortiz, Quimper, Tromp and van Beek (2003) do it in linear time after the bounds are sorted. This is weaker than GAC but faster. See [bounds consistency](/bounds-consistency/).
- **Global cardinality.** Régin (1996) extended the method to the global cardinality constraint, where each value may be used between a lower and an upper number of times, with a flow in place of the matching.

## When to use it

Use it for an all-different constraint whose domains are small sets with holes, for example in puzzles such as [Sudoku](/sudoku/), in scheduling with distinct time slots, and in [graph coloring](/graph-coloring/) models with cliques. When domains are long intervals and only the bounds matter, bounds consistency costs less. When the constraint is loose (many more values than variables), the filter rarely removes anything, and the binary decomposition, which a solver can propagate cheaply, often does as well.

## Pitfalls

- **Testing only the matched edges.** Line L8 must not remove an edge of $M$. Every matched edge is in a maximum matching, by definition.
- **Forgetting the free values.** A filter that keeps only the edges inside strongly connected components removes too much when there are more values than variables. In the example, it would remove 6 from $D(x_5)$, but $x_5 = 6$ is in a solution. Line L5 is needed.
- **Wrong orientation.** If the matched edges point from value to variable and the reachability starts at the free values, the search follows the wrong edges. Keep one orientation for both line L4 and line L5: matched edges from variable to value, others from value to variable, and search forward from the free values.
- **Treating the binary decomposition as equivalent.** Arc consistency on $x_i \ne x_j$ for all pairs is strictly weaker, as the example shows.

## Implementations

## History

Régin published the filter in 1994 and used it in the RESYN system for subgraph isomorphism. He stated the cost as $O(p^2 d^2)$ time and $O(p d)$ space. The matching theory it uses is older: the characterization of the edges that belong to some maximum matching comes from Berge's work on alternating paths, and the matching algorithm from Hopcroft and Karp (1973). Van Hoeve's survey (2001) gives the $O(\sqrt{n} E)$ form of the bound and compares the filter with the weaker propagators.

## References
