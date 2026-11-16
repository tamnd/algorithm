---
tag: RMXE5N
kind: technique
slug: crown-reduction
name: Crown reduction
aliases:
- crown decomposition
area: complexity/parameterized-complexity
level: advanced
summary: "A crown is an independent set C whose neighborhood H has a matching into C. Removing C and H is safe, and it gives a kernel with 3k vertices for vertex cover."
prereqs: [kernelization, parameterized-vertex-cover, konig-theorem, maximum-matching]
see_also: [nemhauser-trotter-theorem, lp-kernelization, buss-kernel, hall-theorem, max-sat, graph-coloring, polynomial-kernel, parameterized-feedback-vertex-set]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Section 2.3, Crown decomposition (Lemma 2.14, the crown lemma; Section 2.3.1 for vertex cover and Section 2.3.2 for maximum satisfiability)
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Chapter 4, Crown decomposition, and Chapter 5, Expansion lemma
  - paper: doi:10.1007/978-3-540-30559-0_22
    title: "Benny Chor, Mike Fellows and David Juedes, Linear kernels in linear time, or how to save k colors in O(n^2) steps, WG 2004, LNCS 3353, 257-269"
    locator: crown reductions, the kernel with 3k vertices for vertex cover and the linear kernel for saving k colors
---

Crown reduction is a [kernelization](/kernelization/) technique for graph problems. A *crown decomposition* of a graph $G$ splits $V(G)$ into three parts $C$, $H$ and $R$: the crown $C$ is a nonempty independent set, the head $H$ is the set of all neighbors of $C$, and the edges between $C$ and $H$ contain a matching that saturates $H$. For [vertex cover](/parameterized-vertex-cover/) with the cover size $k$ as the parameter, some least cover contains all of $H$ and nothing of $C$, so the rule deletes $C \cup H$ and lowers $k$ by $|H|$. A crown can be found in polynomial time whenever the graph has more than $3k$ vertices and no isolated vertex, and this gives a kernel with at most $3k$ vertices.

## In plain words

Picture a group of people who do not know each other, and a second group that contains everyone the first group knows. If each person in the second group can be paired with a different person of the first group, the two groups form a crown.

For the guard problem on a network, the crown gives a sure choice. Each pair in the crown needs one guard, so the crown needs at least as many guards as the second group has people. Putting the guards on the second group uses exactly that many, and it also helps the rest of the network. So you place them, delete both groups, and continue with a smaller network.

A simple search finds a crown in any large network that has no lonely points, unless many disjoint lines exist. Many disjoint lines show at once that the answer is no.

## When it applies

- The problem lives on a graph, or on a bipartite incidence graph such as variables against clauses.
- An independent set $C$ whose neighborhood $H$ is matched into it has a forced treatment: there is an optimal solution that treats $H$ in one fixed way and makes the rest of the instance independent of $C$.
- The parameter bounds a matching: a matching with more than $k$ edges decides the instance at once (a no-instance for vertex cover, a yes-instance for maximum satisfiability).
- A [maximum matching](/maximum-matching/) and a minimum vertex cover of a bipartite graph are cheap to compute. By [König's theorem](/konig-theorem/) the two have the same size, and the proof below needs that.

## The template

The template has three holes. GRAPH(x) builds the graph of the instance with no isolated vertices. BIG(x, k, M) answers the instance when a matching $M$ has more than $k$ edges. TAKE(x, k, C, H) applies the problem rule to a crown and returns a smaller equivalent instance.

```pseudo id=main
CROWN-REDUCE(x, k)
L1  G ← GRAPH(x)                           ▷ no isolated vertex
L2  M ← a maximal matching of G
L3  if |M| > k then return BIG(x, k, M)
L4  I ← V(G) \ V(M)                        ▷ independent, as M is maximal
L5  B ← the bipartite graph of the edges between V(M) and I
L6  M' ← a maximum matching of B
L7  X ← a minimum vertex cover of B         ▷ |X| = |M'| by König
L8  if |M'| > k then return BIG(x, k, M')
L9  H ← X ∩ V(M); C ← I \ X
L10 if C = ∅ then return (x, k)
L11 (x, k) ← TAKE(x, k, C, H)
L12 return CROWN-REDUCE(x, k)
```

For vertex cover, GRAPH deletes the isolated vertices of $G$, BIG returns a fixed no-instance, and TAKE returns $(G - C - H, k - |H|)$.

**Crown lemma.** Let $G$ have no isolated vertex and at least $3k + 1$ vertices. Then lines L2 to L9 run in polynomial time and either find a matching with $k + 1$ edges or find a crown decomposition: $C$ is nonempty and independent, $H = N(C)$, and $M'$ matches $H$ into $C$.

*Proof.* Assume both matchings have at most $k$ edges. Then $|V(M)| \le 2k$, so $|I| \ge 3k + 1 - 2k = k + 1$. The set $I$ is independent, because an edge inside $I$ could be added to the maximal matching $M$. By König's theorem $|X| = |M'| \le k < |I|$, so $C = I \setminus X$ is nonempty and independent.

Take $c \in C$ and an edge $cw$. Since $I$ is independent, $w \in V(M)$, so $cw$ is an edge of $B$. The cover $X$ does not contain $c$, so it contains $w$, and $w \in X \cap V(M) = H$. So $N(C) \subseteq H$.

Each edge of $M'$ has an endpoint in $X$. The edges of $M'$ are disjoint and $|X| = |M'|$, so each edge of $M'$ has exactly one endpoint in $X$, and each vertex of $X$ lies on an edge of $M'$. Let $h \in H$. Its partner $w$ in $M'$ is in $I$, and $w \notin X$ because the edge $hw$ has only one endpoint in $X$. So $w \in C$. This shows that $M'$ matches each vertex of $H$ to a distinct vertex of $C$, and also that $H \subseteq N(C)$. So $H = N(C)$. $\square$

**Safety for vertex cover.** If $(C, H, R)$ is a crown decomposition of $G$, then $G$ has a vertex cover of size at most $k$ if and only if $G - C - H$ has one of size at most $k - |H|$.

*Proof.* Let $S$ be a cover of $G$ with $|S| \le k$. The matching between $H$ and $C$ has $|H|$ disjoint edges, and $S$ contains an endpoint of each, so $|S \cap (C \cup H)| \ge |H|$. The set $S \setminus (C \cup H)$ covers $G - C - H$ and has at most $k - |H|$ vertices. Conversely, let $S'$ cover $G - C - H$ with $|S'| \le k - |H|$. Every edge of $G$ that is not in $G - C - H$ has an endpoint in $H$, because $C$ is independent and $N(C) = H$. So $S' \cup H$ covers $G$ and has at most $k$ vertices. $\square$

**Kernel size.** Each call of TAKE deletes $H$, which is nonempty because $C$ is nonempty and has no isolated vertex. So there are at most $n$ rounds, and each round takes polynomial time, for example $O(m \sqrt{n})$ with [Hopcroft-Karp](/hopcroft-karp/). Line L10 returns only when the crown lemma does not apply, so the output has at most $3k$ vertices. In edges and bits the kernel has size $O(k^2)$.

## Classic examples

### Vertex cover: a kernel with 3k vertices

The graph has 12 vertices and 12 edges. Vertex $a = 0$ has the leaves 2, 3 and 4, vertex $b = 1$ has the leaves 4, 5 and 6, the vertices 7 to 11 form a 5-cycle, and $a$ is joined to 7. A scratch script ran the template with a greedy maximal matching that scans the edges in the order $a2, a3, a4, b4, b5, b6, a7$, then the cycle edges.

- $k = 3$: the maximal matching is $\{a2, b4, 7\text{-}8, 9\text{-}10\}$ with 4 edges, more than $k$, so the answer is NO.
- $k = 4$: the same matching has 4 edges, so $I = \{3, 5, 6, 11\}$. The bipartite graph $B$ has the edges $a3$, $b5$, $b6$, $7\text{-}11$ and $10\text{-}11$. A maximum matching is $\{a3, b5, 7\text{-}11\}$ and the König cover is $X = \{a, b, 11\}$. So $H = \{a, b\}$ and $C = \{3, 5, 6\}$. The rule deletes 5 vertices and gives $k' = 2$. Vertices 2 and 4 are now isolated and GRAPH deletes them. In round 2 the graph is the 5-cycle with $k' = 2$, the procedure finds $C = \emptyset$, and the kernel is the 5-cycle with $k' = 2$.
- $k = 5$: the same two rounds give the 5-cycle with $k' = 3$.

A 5-cycle needs 3 cover vertices, so the kernel for $k = 4$ is a no-instance and the kernel for $k = 5$ is a yes-instance. A brute-force search on the input confirms that its least vertex cover has 5 vertices. The script also checked the crown lemma on 400 random graphs (seed 1) for every $k$ with $n \ge 3k + 1$: each output was a matching with $k + 1$ edges or a valid crown, and after each crown the cover size dropped by exactly $|H|$.

### A crown from the LP

Let $x$ be an optimal half-integral solution of the [LP relaxation](/lp-relaxation/) of vertex cover, and let $V_0$, $V_{1/2}$ and $V_1$ be the vertices with value $0$, $\tfrac12$ and $1$. If $V_0$ is nonempty, then $(V_0, V_1, V_{1/2})$ is a crown decomposition. Every neighbor of a vertex in $V_0$ has value 1. If a vertex of $V_1$ had no neighbor in $V_0$, lowering it to $\tfrac12$ would keep $x$ feasible and lower its value. If a set $Z \subseteq V_1$ had fewer than $|Z|$ neighbors in $V_0$, then setting $Z$ and those neighbors to $\tfrac12$ would also lower the value, so Hall's condition holds and a matching saturates $V_1$. The scratch script checked this on 300 random graphs (seed 7). So the [Nemhauser-Trotter theorem](/nemhauser-trotter-theorem/) contains the crown rule, and its kernel with $2k$ vertices is stronger than the bound of $3k$. The crown method needs only matchings, not an LP solver.

### Maximum satisfiability

The input is a CNF formula and an integer $k$, and the question is whether some assignment satisfies at least $k$ clauses. Build the bipartite graph between variables and clauses, with an edge when a variable occurs in a clause, and look for a crown with $C$ on the variable side. Let $C$ be a set of variables and $H$ the set of clauses that contain them, with a matching that saturates $H$. Set each variable of $C$ so that it satisfies its matched clause. Then every clause of $H$ is true, and the other clauses do not contain variables of $C$. No assignment can do better on $H$ than all $|H|$ clauses, and the other clauses depend only on the other variables, so $(\varphi, k)$ is a yes-instance exactly when the formula without $C$ and $H$ has an assignment that satisfies $k - |H|$ clauses. Here a large matching gives a yes-instance: a matching from clauses to distinct variables lets each matched variable satisfy its clause. Cygan et al. use this in Section 2.3.2 for a kernel with $O(k)$ variables and clauses; see [MAX-SAT](/max-sat/).

### Saving k colors

Chor, Fellows and Juedes asked whether a graph on $n$ vertices can be colored with at most $n - k$ colors. A color class with two or more vertices saves colors, so the question is about how many vertices can share classes. Two vertices can share a class only if they are not adjacent, so the natural graph to work on is the complement, where a matching of non-edges saves one color per edge. Their crown reductions give a kernel with a linear number of vertices, and the title of the paper states the time bound $O(n^2)$. The same paper gives the crown kernel with $3k$ vertices for vertex cover. See [graph coloring](/graph-coloring/) for the classical problem.

## Variations

- **Expansions.** A $q$-expansion of $H$ into $C$ gives each vertex of $H$ its own set of $q$ neighbors in $C$, so a crown is a 1-expansion. The expansion lemma finds a $q$-expansion in a large enough bipartite graph, and it is used for kernels of [feedback vertex set](/parameterized-feedback-vertex-set/) and other deletion problems. Fomin et al. give it in Chapter 5.
- **Weighted and LP versions.** The LP gives a crown whenever its optimum has a vertex of value 0, as shown above, and [LP kernelization](/lp-kernelization/) turns this into a general method.
- **Crowns in incidence graphs.** Any problem with a bipartite structure between choices and demands can use crowns, as maximum satisfiability does.
- **Simpler rules first.** In practice the [Buss kernel](/buss-kernel/) rules run first, because they are linear time, and the crown rule runs on what is left.

## Pitfalls

- **The crown lemma needs no isolated vertex.** An isolated vertex in $I$ is not covered by $X$ and goes into $C$ with no neighbor, so $H$ can be empty and the round makes no progress. Delete isolated vertices first.
- **H must be the whole neighborhood of C.** If a vertex $c \in C$ has a neighbor $w \notin H$, the rule deletes $c$ but keeps $w$. A cover of $G - C - H$ need not contain $w$, so the edge $cw$ can stay uncovered, and the rule is wrong.
- **The matching must saturate H.** Without it, $H$ may be larger than the part of the cover that the crown needs. A star with one center and three leaves, taken with $C$ the center and $H$ the leaves, breaks the rule: it puts 3 vertices in the cover where 1 is enough.
- **The meaning of a large matching depends on the problem.** For vertex cover it gives NO. For maximum satisfiability it gives YES.
- **The unit of size.** The bound $3k$ counts vertices. The kernel can still have $\Theta(k^2)$ edges.
- **3k is not the best bound.** The LP kernel has at most $2k$ vertices. The crown kernel is simpler, not smaller.

## Exercises

1. Show that the graph produced at line L4 has no edge inside $I$, and give an example where $I$ is empty.
2. Prove that if $(C, H, R)$ is a crown decomposition, then $|C| \ge |H|$, and find a graph where $|C| = |H|$.
3. Show that the bound $3k$ in the crown lemma cannot be lowered to $3k - 1$ by this proof: build a graph with $3k$ vertices and no isolated vertex where the procedure finds neither a crown nor a matching with $k + 1$ edges.
4. Use [Hall's theorem](/hall-theorem/) on the incidence graph to prove that a CNF formula in which every set of $j$ clauses contains at least $j$ distinct variables, for every $j$, has an assignment that satisfies all clauses.
5. Show that on $k$ disjoint triangles the template returns the input unchanged, so the bound of $3k$ vertices is reached.

## References
