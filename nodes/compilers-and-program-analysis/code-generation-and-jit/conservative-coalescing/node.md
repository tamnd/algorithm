---
tag: VQDV7X
kind: technique
slug: conservative-coalescing
name: Conservative coalescing
aliases:
- Briggs test
- George test
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Coalesces two nodes only when a degree test proves that the merged graph stays as colorable as before.
prereqs: [register-coalescing-problem, interference-graph]
see_also: [iterated-register-coalescing, briggs-optimistic-coloring, chaitin-register-allocation, degeneracy, k-coloring, out-of-ssa-translation, ssa-based-register-allocation, graph-coloring]
sources:
  - paper: doi:10.1145/177492.177575
    title: Preston Briggs, Keith D. Cooper and Linda Torczon, Improvements to graph coloring register allocation, ACM Transactions on Programming Languages and Systems 16(3), 1994, 428-455
    locator: conservative coalescing with the test on the number of neighbors of significant degree
  - paper: doi:10.1145/229542.229546
    title: Lal George and Andrew W. Appel, Iterated register coalescing, ACM Transactions on Programming Languages and Systems 18(3), 1996, 300-324
    locator: the George test, its use for precolored nodes, and the proofs that both tests are safe
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 11 (Register Allocation), the section on coalescing and the Briggs and George criteria
  - paper: doi:10.1109/CGO.2007.26
    title: Florent Bouchez, Alain Darte and Fabrice Rastello, On the complexity of register coalescing, International Symposium on Code Generation and Optimization (CGO), 2007, 102-114
    locator: the NP-completeness of conservative coalescing and the analysis of the incremental question that the two tests answer in part
---

Conservative coalescing merges the two names of a copy `x = y` in the [interference graph](/interference-graph/) only when a cheap local test proves that the merge cannot make the graph harder to color. The two tests in use are the *Briggs test*, from Briggs, Cooper and Torczon (1994), and the *George test*, from George and Appel (1996). Both look only at the degrees of the neighbors of $x$ and $y$. Both guarantee that if the graph was $k$-colorable it stays $k$-colorable, and that if [Chaitin's simplify phase](/chaitin-register-allocation/) could color it, it still can. They are sufficient conditions: a safe merge can fail both tests. The problem they help with, [register coalescing](/register-coalescing-problem/), is NP-complete.

## In plain words

When one value is a copy of another, putting both in the same register removes the copy. But the joined value now clashes with everything that either value clashed with, and that can force some value out to memory. A safe rule looks at the neighbors of the joined value. A neighbor with few clashes is never a problem, because it can always find a free register at the end. So the first rule says: join only if few neighbors have many clashes. The second rule says: join the copy into the original only if each neighbor of the copy is already a neighbor of the original or has few clashes. Either rule makes sure that the join never forces a value out to memory.

## When it applies

- The allocator works on an interference graph with $k$ colors and uses simplification, as in [Chaitin's allocator](/chaitin-register-allocation/), [optimistic coloring](/briggs-optimistic-coloring/) or [iterated register coalescing](/iterated-register-coalescing/).
- There is a copy `x = y` whose names do not interfere. A copy by itself never makes its two names interfere; they interfere only if one of them is defined, by an instruction other than this copy, while the other is live.
- The test is applied to the current graph, with the current degrees. A degree is *high* if it is at least $k$ and *low* otherwise.

## The template

Let $u$ and $v$ be the vertices of $x$ and $y$, not adjacent, and let $G'$ be the graph after the merge, where the new vertex $w$ has the neighbors $N(u) \cup N(v)$. A common neighbor of $u$ and $v$ loses one edge in $G'$; every other vertex keeps its degree.

```
BRIGGS-OK(G, u, v, k)
  H <- the vertices t in N(u) + N(v) with degree(t) - [t in N(u) and t in N(v)] >= k
  return |H| < k

GEORGE-OK(G, u, v, k)          // merge v into u
  return every t in N(v) is in N(u) or has degree(t) < k
```

An allocator merges $u$ and $v$ if BRIGGS-OK passes, or if GEORGE-OK passes in one of the two directions. Each test runs in $O(\deg u + \deg v)$ time with adjacency sets.

**Why the Briggs test is safe.** The neighbors of $w$ with low degree in $G'$ can be simplified away. Then $w$ has fewer than $k$ neighbors left, all of high degree, so $w$ can be simplified too. What remains is $G$ without $u$, $v$ and some low vertices, a subgraph of $G$. So a $k$-coloring of $G$ gives one of what remains, and the simplify rule extends it back to $G'$. For the $k$-core: in a nonempty $k$-core of $G'$ that contains $w$, the vertex $w$ would need $k$ neighbors of degree at least $k$, which the test excludes.

**Why the George test is safe.** The neighbors of $v$ that are not neighbors of $u$ have low degree, and they keep the same degree in $G'$. Simplify them away. Then $w$ has exactly the neighbors of $u$, so what remains is $G$ without $v$ and those vertices, with $w$ in the place of $u$. Again it is a subgraph of $G$.

The full proofs, for both $k$-colorability and the empty $k$-core, are Lemmas 1 and 2 of the proof file of [iterated register coalescing](/iterated-register-coalescing/).

## Classic examples

**A merge that only George allows.** In the summing loop of the iterated coalescing page, with $k = 2$, the interference graph is the cycle $i, s, j, t$ plus a vertex $n$ with no edge, and there is a copy `i = n`. Merging $n$ into $i$ gives a vertex with the neighbors $s$ and $t$, both of degree 2, so the Briggs test fails. The George test, merging $n$ into $i$, passes at once: $n$ has no neighbor.

**A merge that only Briggs allows.** Take $k = 3$. Let $u$ have the neighbor $a$, and $v$ the neighbor $b$, where $a$ and $b$ each have two more neighbors of their own, so both have degree 3. The merged vertex has the neighbors $a$ and $b$, two of high degree, fewer than 3, so the Briggs test passes. The George test fails in both directions: $b$ is not a neighbor of $u$ and has degree 3, and $a$ is not a neighbor of $v$ and has degree 3.

**A merge that both refuse, rightly.** In the path $a, x, y, b$ with $k = 2$, merging $a$ and $b$ makes a triangle. After the merge, $x$ and $y$ have degree 2, so the Briggs test fails. The George test fails both ways: $x$ is not a neighbor of $b$ and $y$ is not a neighbor of $a$, and both have degree 2. Aggressive coalescing would merge them and force a spill.

**A merge that both refuse, wrongly.** In the cycle $0, 1, 2, 3, 4, 5$ with $k = 2$, merge $0$ and $2$. The merged vertex has the neighbors $1, 3, 5$, and $3$ and $5$ have degree 2 after the merge, so the Briggs test fails. The George test fails both ways, because of $3$ and of $5$. But the merged graph has the edges $w$-$1$, $w$-$3$, $w$-$5$, $3$-$4$ and $4$-$5$, and it is bipartite with the sides $\{w, 4\}$ and $\{1, 3, 5\}$, so it is still 2-colorable.

## Variations

- **Before coloring.** Briggs, Cooper and Torczon (1994) applied the Briggs test in the build and coalesce loop before simplification.
- **Interleaved with simplify.** George and Appel (1996) test copies between simplify steps. A failed copy is tried again when a degree drops to $k - 1$, because simplification lowers degrees and turns more tests into passes ([iterated register coalescing](/iterated-register-coalescing/)).
- **Precolored vertices.** A machine register that is fixed by a calling convention interferes with a very large set of names. The George test, with $u$ the precolored vertex, needs only the neighbors of the other vertex and a membership check in $N(u)$, so allocators use it in that case.
- **Either test.** Since both tests are safe, an allocator can accept a merge if either one passes.
- **Exact incremental test.** One can ask exactly whether a merge keeps the $k$-core empty, by running simplification on the merged graph. This costs time linear in the graph for each copy, instead of the degrees of two vertices.

## Pitfalls

- **Degrees after the merge.** The Briggs test counts degrees in the merged graph. A common neighbor of $u$ and $v$ loses one edge, and using its old degree makes the test refuse merges it could allow.
- **A copy is not an interference.** If the build phase adds an edge between the two names of every copy, no copy can ever be coalesced. At the copy `x = y`, the source $y$ is left out of the edges of $x$.
- **Safe is not optimal.** The tests are sufficient conditions, and the order of the copies changes which merges pass. Finding the best conservative coalescing is NP-complete.
- **Aggressive is not safe.** Merging every pair of non-interfering copy ends can turn a 2-colorable graph into a triangle.
- **The guarantee is about this graph.** If the graph already has a nonempty $k$-core, the tests keep it $k$-colorable when it was, but the allocator may still spill for other reasons.

## Exercises

1. Show that the Briggs test with the degrees of $G$ instead of $G'$ is still safe, but refuses more merges.

   *Answer.* For a neighbor $t$ of $w$, $\deg_{G'}(t) = \deg_G(t) - 1$ if $t$ is a common neighbor and $\deg_G(t)$ otherwise. So $\deg_{G'}(t) \le \deg_G(t)$, and every vertex counted as high with the degrees of $G'$ is also high with the degrees of $G$. If the test passes with the degrees of $G$, it passes with those of $G'$, and the merge is safe. A common neighbor of degree exactly $k$ in $G$ is high in $G$ and low in $G'$, so the version with $G$ can refuse a merge that the right version allows.

2. In the George test, why can the degrees of $G$ be used, not those of $G'$?

   *Answer.* The test looks only at neighbors $t$ of $v$ that are not neighbors of $u$. Such a $t$ loses its neighbor $v$ and gains $w$, and it was not adjacent to $u$, so its degree in $G'$ is the same as in $G$.

3. Let $u$ have no neighbor of high degree, and let $v$ be any vertex not adjacent to $u$. Which test passes for merging $u$ into $v$?

   *Answer.* The George test, merging $u$ into $v$: every neighbor of $u$ has low degree. The Briggs test may fail if $v$ has $k$ or more neighbors of high degree.

4. In the cycle $0, 1, 2, 3, 4, 5$ with $k = 2$, is there a merge of two non-adjacent vertices that the Briggs test allows?

   *Answer.* No. Two non-adjacent vertices are at distance 2 or 3. At distance 2, as for $0$ and $2$, the merged vertex has three neighbors, and the two that are not common keep degree 2. At distance 3, as for $0$ and $3$, the merged vertex has four neighbors, each of degree 2 after the merge. In both cases at least 2 neighbors have degree at least 2. So the Briggs test refuses every merge in this cycle, although the merge of $0$ and $2$ keeps it 2-colorable.

## References
