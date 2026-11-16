---
tag: PC152B
kind: technique
slug: kernelization
name: Kernelization
aliases:
- preprocessing with guarantees
- data reduction
area: complexity/parameterized-complexity
level: core
summary: "Shrink an instance (x, k) with safe polynomial-time reduction rules, then prove that a reduced yes-instance has size at most g(k). The result is a kernel."
prereqs: [kernel, fixed-parameter-tractable]
see_also: [buss-kernel, polynomial-kernel, crown-reduction, nemhauser-trotter-theorem, lp-kernelization, sunflower-lemma, kernel-lower-bounds, bounded-search-tree]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 2, Kernelization (Section 2.2.1 for the O(k^2) kernel of vertex cover, Section 2.3.1 for the 3k crown kernel, and the sunflower kernel for d-hitting set)
  - book: isbn:9780198566076
    title: Rolf Niedermeier, Invitation to Fixed-Parameter Algorithms, Oxford University Press, 2006
    locator: Chapter 7, Data reduction and problem kernels
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: Chapter 4, Kernelization, and Chapter 5, More on Kernelization
  - paper: doi:10.1137/0222038
    title: "Jonathan F. Buss and Judy Goldsmith, Nondeterminism within P, SIAM Journal on Computing 22(3), 560-572 (1993)"
    locator: the high-degree rule for vertex cover
  - paper: doi:10.1006/jagm.2001.1186
    title: "Jianer Chen, Iyad A. Kanj and Weijia Jia, Vertex cover: further observations and further improvements, Journal of Algorithms 41(2), 280-301 (2001)"
    locator: the kernel with at most 2k vertices from the Nemhauser-Trotter theorem
---

Kernelization is the technique of building a [kernel](/kernel/): a polynomial-time algorithm that turns an instance $(x, k)$ of a [parameterized problem](/parameterized-problem/) into an equivalent instance whose size is bounded by a function $g(k)$ of the parameter. The algorithm applies *reduction rules*. Each rule is safe, which means that it does not change the answer, and each one makes the instance smaller or the parameter lower. When no rule applies, the instance is *reduced*, and a separate counting argument shows that a reduced yes-instance has size at most $g(k)$. A reduced instance that is larger must be a no-instance. The [Buss kernel](/buss-kernel/) for vertex cover is the first example, and the [crown](/crown-reduction/) and [LP](/lp-kernelization/) kernels refine it.

## In plain words

Before you solve a hard puzzle, you can often make it smaller. Some parts of it have only one sensible choice, so you make that choice and remove the part. Other parts can never matter, so you delete them. Each step must keep the answer the same.

When no step applies any more, you look at what is left. If the answer is yes, the rest must be small, because a small solution cannot handle a large puzzle with no easy parts. So a large rest means that the answer is no. A small rest can be solved by any method, even by trying every choice, and the time for that depends only on how small the solution must be.

## When it applies

- The problem has a parameter $k$ that bounds the size of a solution, or a structure that a solution must use, such as a cover, a hitting set or a deletion set.
- Some local patterns in the input force a choice (a vertex of high degree must be in every small vertex cover) or are irrelevant (an isolated vertex never needs to be in a cover).
- A reduced yes-instance has bounded size: you can count its parts against the $k$ elements of a solution.
- You want a preprocessing step that runs in polynomial time before an exponential algorithm, such as a [bounded search tree](/bounded-search-tree/).

## The template

The template has four holes. RULES is a list of reduction rules. Each rule $R$ maps $(x, k)$ to $(x', k')$, runs in polynomial time, and is *safe*: $(x, k) \in L$ if and only if $(x', k') \in L$. MEASURE is a nonnegative integer, such as $|x| + k$, that each rule lowers and that is polynomial in $|x| + k$ at the start. BOUND is a computable function, and the *size lemma* says that each reduced yes-instance has size at most $\mathrm{BOUND}(k)$. NO is a fixed no-instance of constant size.

```pseudo id=main
KERNELIZE(x, k)
L1  while some rule R in RULES applies to (x, k) do
L2      (x, k) ← R(x, k)                  ▷ safe, and MEASURE drops
L3      if k < 0 then return NO
L4  if |x| > BOUND(k) then return NO      ▷ by the size lemma
L5  return (x, k)
```

**Lemma.** If each rule is safe and polynomial, MEASURE drops at each application, and the size lemma holds, then KERNELIZE is a kernelization of size $\max(\mathrm{BOUND}(k), |\mathrm{NO}|)$.

*Proof.* The loop runs at most MEASURE times, which is polynomial, and each pass takes polynomial time, so KERNELIZE runs in polynomial time. Each rule is safe, so the instance after the loop is equivalent to the input. A negative parameter means that no solution of size $k$ exists, so line L3 is correct. At line L4 the instance is reduced. If it is a yes-instance, the size lemma gives $|x| \le \mathrm{BOUND}(k)$; so a larger reduced instance is a no-instance, and returning NO is correct. Every output has size at most $\max(\mathrm{BOUND}(k), |\mathrm{NO}|)$, and the parameter never grows. $\square$

The size lemma is the part that needs ideas. The rules make the reduced instance regular enough to count, and the count gives BOUND.

## Classic examples

The examples go from simple to hard.

### Vertex cover: the Buss kernel

The parameter $k$ is the size of the cover. Rule 1: delete an isolated vertex. Rule 2: if a vertex $v$ has degree more than $k$, delete $v$ and lower $k$ by one; every cover of size at most $k$ contains $v$, because otherwise it contains all of its more than $k$ neighbors. Size lemma: in a reduced yes-instance each vertex has degree at most $k$, so the $k$ cover vertices cover at most $k^2$ edges, and the graph has at most $k$ cover vertices and $k^2$ other vertices. The bound is $k^2$ edges and $k^2 + k$ vertices. For a star with 50 leaves plus 3 disjoint edges and $k = 4$, rule 2 removes the center, rule 1 removes the 50 leaves, and the kernel is the 3 edges with $k = 3$. The [Buss kernel](/buss-kernel/) page has the algorithm, a proof and code.

### d-Hitting set: sunflowers

The input is a family of sets of size $d$ and the parameter $k$. A sunflower with $k + 1$ petals is a set of $k + 1$ members whose pairwise intersections all equal one core $Y$. A hitting set of size at most $k$ must hit $Y$, because it cannot hit the $k + 1$ disjoint petals outside $Y$ with $k$ elements. So the rule replaces the sunflower by the single set $Y$, and if $Y$ is empty the answer is no. The [sunflower lemma](/sunflower-lemma/) says that more than $d!\,k^d$ sets of size $d$ contain such a sunflower, so a reduced family has at most $d!\,k^d$ sets. This is a polynomial kernel for each fixed $d$; see [parameterized hitting set](/parameterized-hitting-set/).

### Vertex cover: crowns

A crown is an independent set $C$ and its neighborhood $H$ such that the edges between them contain a matching that saturates $H$. Some least cover contains $H$ and no vertex of $C$, so the rule deletes $C \cup H$ and lowers $k$ by $|H|$. A crown can be found from a maximal matching and a maximum matching in a bipartite graph, both in polynomial time. A graph with no isolated vertex and more than $3k$ vertices has a crown or a matching of size $k + 1$, and in the second case it has no cover of size $k$. This gives a kernel with at most $3k$ vertices; see [crown reduction](/crown-reduction/).

### Vertex cover: linear programming

Solve the [LP relaxation](/lp-relaxation/) of vertex cover. By the [Nemhauser-Trotter theorem](/nemhauser-trotter-theorem/) there is an optimal solution with values in $\{0, \tfrac{1}{2}, 1\}$, and some least cover contains all vertices of value 1 and none of value 0. Fixing those leaves the vertices of value $\tfrac{1}{2}$, and a yes-instance has at most $2k$ of them, because the LP value is at most the size of a cover. Chen, Kanj and Jia used this for a kernel with at most $2k$ vertices; see [LP kernelization](/lp-kernelization/). In units of bits this is $O(k^2)$. Dell and van Melkebeek proved that no kernel has $O(k^{2 - \varepsilon})$ bits for a constant $\varepsilon > 0$ unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$, so the bit size is close to the best possible.

## Variations

- **Kernels of polynomial size.** A [polynomial kernel](/polynomial-kernel/) has $g(k) = k^{O(1)}$. It is the usual goal, because every decidable FPT problem has a kernel of some size.
- **Compressions.** A [polynomial compression](/polynomial-compression/) may output an instance of another problem. [Kernel lower bounds](/kernel-lower-bounds/), for example by [cross-composition](/cross-composition/), rule out polynomial compressions and so also polynomial kernels.
- **Transfers between problems.** A [polynomial parameter transformation](/polynomial-parameter-transformation/) moves polynomial kernels and their lower bounds from one problem to another.
- **Approximate answers.** A [lossy kernel](/lossy-kernelization/) keeps an approximation ratio instead of the exact answer and can be smaller.
- **Kernel then search.** Running a [bounded search tree](/bounded-search-tree/) on the kernel turns time $O(c^k (n + m))$ into $O(n + m + c^k k^{O(1)})$, because the search runs on an instance of size $k^{O(1)}$.

## Pitfalls

- **An unsafe rule.** For vertex cover, a vertex $v$ of degree 1 with neighbor $u$ allows the rule "take $u$". The rule "take $v$" is wrong: in a star with three leaves, it uses three vertices where one is enough.
- **The size lemma for no-instances.** The size lemma bounds only reduced yes-instances. Line L4 must return NO for larger instances; returning the large instance breaks the size bound.
- **A parameter that grows.** The output parameter must be at most $g(k)$. A rule that raises $k$ needs its own bound.
- **No polynomial bound on the loop.** Each rule must lower a measure that is polynomial at the start. Rules that undo each other can loop forever.
- **The unit of size.** A kernel with $2k$ vertices has $O(k^2)$ edges. State whether $g$ counts vertices, edges or bits.
- **Rules in the wrong order.** In the Buss kernel, the edge count at line L4 is valid only after the degree rule no longer applies.

## Exercises

1. Prove that the degree-1 rule for vertex cover is safe: if $v$ has degree 1 and neighbor $u$, then $(G, k)$ is a yes-instance exactly when $(G - u - v, k - 1)$ is one.
2. Give a kernel for vertex cover in graphs of maximum degree 3 with $O(k)$ vertices, using only the degree rules and a count.
3. Show that a family of sets of size 2 with more than $2k^2$ members has a sunflower with $k + 1$ petals. Use this to give a kernel with $O(k^2)$ edges for vertex cover.
4. The Buss kernel bound is $k^2 + k$ vertices. Find, for each $k$, a reduced yes-instance that reaches it.
5. Point line cover asks if $n$ points in the plane lie on $k$ lines. Give a rule for a line with more than $k$ points and prove a kernel with at most $k^2$ points.

## References
