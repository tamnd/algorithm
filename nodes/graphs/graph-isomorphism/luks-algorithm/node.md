---
tag: QX3WY0
kind: algorithm
slug: luks-algorithm
name: Luks's algorithm
aliases:
- Luks bounded-degree isomorphism
area: graphs/graph-isomorphism
level: research
summary: Polynomial-time isomorphism for bounded-degree graphs using group-theoretic composition series.
solves: [bounded-degree-graph-isomorphism, graph-isomorphism-problem]
model: word-ram
complexity:
  vars: {n: the number of points the group acts on, d: a bound such that every composition factor of the group embeds in the symmetric group S_d}
  time: {worst: n^(O(d))}
  space: {extra: n^(O(d))}
properties: {deterministic: true, recursive: true, directed: false}
prereqs: [bounded-degree-graph-isomorphism, graph-automorphism-group, automorphism-orbit]
see_also: [babai-quasipolynomial-algorithm, bounded-degree-graph-isomorphism, cai-furer-immerman-construction, graph-automorphism, gi-completeness, canonical-labeling, nauty]
sources:
  - paper: doi:10.1016/0022-0000(82)90009-5
    title: Eugene M. Luks, Isomorphism of graphs of bounded valence can be tested in polynomial time, Journal of Computer and System Sciences 25(1), 42 to 65 (1982)
    locator: Section 1 (the color automorphism problem and its divide and conquer for groups in Gamma_d), Sections 2 to 4 (the reduction from graphs of bounded valence, first for trivalent graphs)
  - paper: "László Babai, Peter J. Cameron and Péter P. Pálfy, On the orders of primitive groups with restricted nonabelian composition factors, Journal of Algebra 79, 161 to 168 (1982)"
    locator: the main theorem (a primitive group of degree m in Gamma_d has order at most m^(O(d)))
  - book: "Ákos Seress, Permutation Group Algorithms, Cambridge University Press, 2003"
    locator: Chapters 4 and 5 (the Schreier-Sims algorithm, and computing block systems)
  - paper: "László Babai, Graph isomorphism in quasipolynomial time, arXiv:1512.03547 (2015)"
    locator: Sections 2 and 3 (the string isomorphism problem and Luks's framework, which Babai's algorithm extends)
---

Luks's algorithm (1980, journal version 1982) tests isomorphism of graphs of maximum degree $d$ in polynomial time, $n^{O(d)}$. Its heart is a divide and conquer over a permutation group: to find all elements of a group $G$ that map one colored string to another, split the problem along the orbits of $G$, and, for a transitive group, along a system of blocks, running over the few cosets of the subgroup that fixes every block. For groups whose composition factors are small, the number of cosets stays polynomial, and bounded-degree graphs reduce to such groups. It was the first algorithm that used the structure of permutation groups in an essential way for graph isomorphism, and [Babai's quasipolynomial algorithm](/babai-quasipolynomial-algorithm/) is built on the same framework.

## In plain words

Suppose you know all the ways the points could be shuffled, as a group of moves, and you want the moves that turn one row of colored beads into another. Trying every move is too slow. Instead, split the beads into parts that the moves never mix, and solve each part in turn, keeping only the moves that work so far. When the moves do mix all the beads, find a way to group them into boxes that the moves carry around as whole boxes. Then try each way of moving the boxes, which is few when the group is well behaved, and solve the smaller problem inside the boxes. For networks where every point has few links, matching the networks becomes exactly this kind of bead problem.

## The problem

**String isomorphism.** The input is a permutation group $G$ on $\Omega = \{0, \ldots, n-1\}$, given by generators, a $G$-invariant window $\Delta \subseteq \Omega$, and two strings $x, y : \Omega \to$ colors. The output is the set $\mathrm{Iso}^\Delta_G(x, y) = \{ g \in G : x(d) = y(g(d)) \text{ for all } d \in \Delta \}$. This set is empty or a coset $A\tau$ of the group $A = \mathrm{Iso}^\Delta_G(x, x)$, so it has a short description: generators of $A$ and one element $\tau$.

Permutations are applied left to right. Graph isomorphism of two graphs $X$, $Y$ on the same vertex set is the case where $G$ acts on vertex pairs and $x$, $y$ mark the edges. The graphs here are simple and undirected, with optional vertex colors that isomorphisms must keep; edge colors fit in the strings.

**The class $\Gamma_d$.** A group is in $\Gamma_d$ when every composition factor is isomorphic to a subgroup of the symmetric group $S_d$. Products of symmetric groups $S_b$ with $b \le d$ are in $\Gamma_d$, and so are all 2-groups, for $d \ge 2$.

## The algorithm

```pseudo id=main
STRING-ISO(G, Δ, x, y)
L1  if Δ = {d} then return (G, id) if x(d) = y(d), else none
L2  if G is not transitive on Δ then
L3      A ← G; τ ← id
L4      for each orbit O of G on Δ: (A, g) ← STRING-ISO(A, O, x, y ∘ τ), or return none; τ ← g τ
L5      return (A, τ)
L6  B ← a system of maximal blocks of G on Δ; N ← the kernel of the action of G on B
L7  for each t in a transversal of N in G: R_t ← STRING-ISO(N, Δ, x, y ∘ t); if R_t = (A, g) then τ_t ← g t
L8  if every R_t is none then return none
L9  return (⟨A, τ_t τ_1^(-1) for all t⟩, τ_1)
```

Here $(y \circ t)(d) = y(t(d))$. The orbits in L2 come from a breadth-first search over the generators. The maximal blocks in L6 come from Atkinson's method: grow the block of one point while the smallest block containing it and one more point is a proper block. The transversal in L7 comes from a breadth-first search over the action of $G$ on the blocks, which is primitive because the blocks are maximal, and the generators of $N$ are the Schreier generators of that search. The group machinery underneath, the Schreier-Sims algorithm, keeps generating sets small.

**Bounded-degree graphs.** Luks reduces isomorphism of connected graphs of degree at most $d$ to string isomorphism. Fix an edge $e$ of $X$ and try each edge $e'$ of $Y$ as its image. Let $X_r$ be the part of $X$ within distance $r$ of $e$. The isomorphisms that map $X_r$ to $Y_r$ and $e$ to $e'$, restricted to the next layer, form a coset of a group in $\Gamma_d$ (in $\Gamma_2$, so a 2-group, for trivalent graphs), and passing from layer $r$ to layer $r + 1$ is one string isomorphism problem for that group. The implementation on this page applies STRING-ISO directly to colored graphs with small color classes, where $G$ is the product of the symmetric groups on the classes; with classes of size at most $b$ this group is in $\Gamma_b$.

## Example

Three graphs on the vertices $0, \ldots, 5$ with color classes $\{0, 1\}$, $\{2, 3\}$, $\{4, 5\}$: $X$ is two triangles $0, 2, 4$ and $1, 3, 5$; $Y$ is the 6-cycle $0, 2, 4, 1, 3, 5$; $Z$ is the two triangles $0, 2, 5$ and $1, 3, 4$. The group $G$ swaps within classes, with 8 elements, acting on the 15 vertex pairs. It has 6 orbits on pairs: the three pairs inside a class, and three orbits of 4 pairs between two classes. L4 handles them in order.

| orbit of pairs | $\lvert A \rvert$ after it, for $X$ to $Z$ | vertex part of $\tau$ | for $X$ to $Y$ |
|---|---|---|---|
| $\{0, 1\}$ | 8 | identity | 8 |
| $\{0, 2\}, \{0, 3\}, \{1, 2\}, \{1, 3\}$ | 4 | identity | 4 |
| $\{0, 4\}, \{0, 5\}, \{1, 4\}, \{1, 5\}$ | 2 | swap 4 and 5 | 2 |
| $\{2, 3\}$ | 2 | swap 4 and 5 | 2 |
| $\{2, 4\}, \{2, 5\}, \{3, 4\}, \{3, 5\}$ | 2 | swap 4 and 5 | none |
| $\{4, 5\}$ | 2 | swap 4 and 5 | |

So $Z$ is the image of $X$ under the swap of 4 and 5, and $X$ has 2 color-preserving automorphisms: the identity and the map that exchanges the two triangles. $Y$ is not isomorphic to $X$: no element survives the orbit between the classes $\{2, 3\}$ and $\{4, 5\}$. Each 4-pair orbit is handled through the transitive case: the group on it is a 2-group, and the blocks of size 2 halve the problem.

## Correctness

The [full proof](proofs/correctness.md) is an induction.

- **Cosets.** If $\tau$ maps $x$ to $y$ on $\Delta$, then the set of all such elements is $A\tau$, with $A$ the group of elements that keep $x$ on $\Delta$.
- **Chain rule.** The orbits of $G$ are invariant under every subgroup, so the elements that work on $O_1 \cup \cdots \cup O_{i+1}$ are the elements of the current coset that also work on $O_{i+1}$, which is one recursive call with $y$ shifted by $\tau$.
- **Cosets of the kernel.** $G$ is the union of the cosets $Nt$, and the solutions in $Nt$ are the solutions in $N$ for $y \circ t$, shifted by $t$. All nonempty pieces share the group $A = \mathrm{Aut}^\Delta_N(x)$, and their union is a coset of $\langle A, \tau_t\tau_1^{-1} \rangle$.
- **Termination.** Calls in L4 have smaller windows; the call in L7 has the same window but a group $N$ that keeps every one of at least two blocks, so it goes to L2 next.

## Complexity

| case | time | space |
|---|---|---|
| $G$ in $\Gamma_d$ | $n^{O(d)}$ | $n^{O(d)}$ |
| bounded-degree graphs, degree $d$ (Luks) | $n^{O(d)}$ | $n^{O(d)}$ |
| $G$ arbitrary, for example $S_n$ | exponential: L7 enumerates a primitive group, up to $n!$ cosets | as much |
| one Schreier-Sims call | polynomial in $n$ and the number of generators | $O(n^2)$ transversal entries |

The key fact is the bound of Babai, Cameron and Pálfy (1982): a primitive group of degree $m$ in $\Gamma_d$ has at most $m^{O(d)}$ elements. For the 2-groups of the trivalent case it is immediate, since a primitive 2-group has degree 2. So L7 makes $m^{O(d)}$ recursive calls on $m$ blocks of size $|\Delta|/m$, and the recursion $T(k) \le m^{O(d)} \cdot m \cdot T(k/m)$ solves to $k^{O(d)}$. The recursion depth is at most $2\log_2 n$, because blocks at least halve, so the recursion is safe in Python. The implementation favors clarity over speed: it rebuilds a Schreier-Sims structure in every call.

## Properties

- **Exact and deterministic.** It returns all isomorphisms, as a coset, not just one.
- **Group-theoretic.** It needs no combinatorial invariant, so the [CFI graphs](/cai-furer-immerman-construction/), which defeat every fixed level of Weisfeiler-Leman, are solved in polynomial time, since they have bounded degree.
- **Depends on the group, not on the graph.** The running time is governed by the primitive groups met in L6, so the same routine handles graphs, hypergraphs and codes once they are phrased as strings under a group in $\Gamma_d$.
- **Degree is in the exponent.** For degree $d$ growing with $n$ the bound is not polynomial.

## Variants and improvements

- **Canonical forms.** Babai and Luks (1983) turned the method into canonical labeling, and combined it with Zemlyachenko's degree reduction to get the bound $\exp(O(\sqrt{n \log n}))$ for general graphs, the best known until 2015.
- **Better bounds for degree $d$.** Babai, Kantor and Luks (1983) improved the bound to $n^{O(d / \log d)}$, and Grohe, Neuen and Schweitzer (2018) to $n^{\mathrm{polylog}(d)}$; see [bounded-degree graph isomorphism](/bounded-degree-graph-isomorphism/).
- **Babai's algorithm.** [Babai (2015)](/babai-quasipolynomial-algorithm/) keeps Luks's reduction and recursion, and handles the bottleneck, a large primitive group, essentially the symmetric or alternating group acting on subsets, by new combinatorial and group-theoretic tools.
- **Hypergraphs and other structures.** Luks (1999) applied the method to hypergraph isomorphism, in time $2^{O(n)}$ in the number of vertices, and the same framework handles isomorphism of codes and of colored structures with bounded color classes.

## When to use it

It is a theoretical algorithm. Use it to prove polynomial or quasipolynomial bounds, or when the problem comes with a known, well behaved group, such as isomorphism of colored graphs with small color classes or of structures with a given symmetry group. For practical graph isomorphism, [nauty](/nauty/) and related tools are faster on almost all inputs; computer algebra systems solve problems given as groups mostly by backtrack search over the group, such as Leon's partition backtrack.

## Pitfalls

- **Forgetting that the window must be invariant.** The chain rule needs each orbit to be invariant under the current subgroup; using an arbitrary subset of points breaks the coset structure.
- **Left and right cosets.** With left-to-right products, solutions are $A\tau$ with $A$ acting first. Mixing conventions gives wrong $\tau$ when combining results in L4 and L9.
- **Non-maximal blocks.** Any block system with at least two blocks gives correct answers, but only maximal blocks make the action primitive, which is what the bound on the number of cosets needs.
- **Unbounded groups.** Feeding it a large symmetric group, such as all permutations of one big color class, makes L7 enumerate that group; the polynomial bound is only for $\Gamma_d$.

## Implementations

## History

Eugene Luks presented the algorithm at FOCS 1980, with the journal version in 1982, after Babai had used group theory for graphs with bounded color multiplicity. Luks first treated trivalent graphs, where the groups are 2-groups, then all bounded degrees through the class $\Gamma_d$, using the bound on primitive groups that Babai, Cameron and Pálfy proved in 1982. The method changed the field: the best general bound, Babai and Luks's $\exp(O(\sqrt{n \log n}))$ of 1983, used it, and so did Babai's quasipolynomial algorithm of 2015.

## References
