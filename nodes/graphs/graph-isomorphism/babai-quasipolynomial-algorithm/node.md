---
tag: E8W04N
kind: algorithm
slug: babai-quasipolynomial-algorithm
name: Babai's quasipolynomial graph isomorphism algorithm
aliases:
- Babai's graph isomorphism algorithm
- quasipolynomial graph isomorphism
area: graphs/graph-isomorphism
level: research
summary: Solves graph isomorphism in quasipolynomial time n^(polylog n), the best known general bound.
solves: [graph-isomorphism-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: exp((log n)^(O(1)))}
  space: {extra: exp((log n)^(O(1)))}
properties: {deterministic: true, recursive: true, directed: false}
prereqs: [luks-algorithm, graph-isomorphism-problem, k-dimensional-weisfeiler-leman]
see_also: [luks-algorithm, gi-completeness, graph-isomorphism-in-np, cai-furer-immerman-construction, canonical-labeling, individualization-refinement, bounded-degree-graph-isomorphism, weisfeiler-leman]
sources:
  - paper: "László Babai, Graph isomorphism in quasipolynomial time, arXiv:1512.03547 (version 1 December 2015; later versions correct the error found in January 2017)"
    locator: Sections 1 to 3 (the main theorem, string isomorphism and Luks's framework), and the sections on local certificates, aggregation of certificates and the split-or-Johnson routine
  - paper: doi:10.1145/2897518.2897542
    title: László Babai, Graph isomorphism in quasipolynomial time [extended abstract], Proceedings of the 48th ACM Symposium on Theory of Computing (STOC 2016), 684 to 697
    locator: the whole extended abstract (the main theorem and an overview of the method)
  - paper: doi:10.1145/3313276.3316356
    title: László Babai, Canonical form for graphs in quasipolynomial time, Proceedings of the 51st ACM Symposium on Theory of Computing (STOC 2019), 1237 to 1246
    locator: the main theorem (canonical forms within the same time bound)
  - paper: doi:10.1016/0022-0000(82)90009-5
    title: Eugene M. Luks, Isomorphism of graphs of bounded valence can be tested in polynomial time, Journal of Computer and System Sciences 25(1), 42 to 65 (1982)
    locator: Section 1 (the group-theoretic divide and conquer that Babai's algorithm extends)
---

Babai's algorithm decides whether two graphs with $n$ vertices are isomorphic in quasipolynomial time, $\exp((\log n)^{c})$ for a constant $c$. László Babai announced it in November 2015, posted it as arXiv:1512.03547 in December 2015, and presented it at STOC 2016. In January 2017 Harald Helfgott found an error in the analysis; within days Babai repaired it, and the quasipolynomial claim stands. The algorithm extends [Luks's](/luks-algorithm/) group-theoretic recursion with new tools for its one hard case, a large symmetric group acting on the pieces. It is the best known bound for general graphs, far below the $\exp(O(\sqrt{n \log n}))$ of Babai and Luks (1983), though it is still not known whether graph isomorphism is in P.

## In plain words

Testing whether two networks are the same up to renaming looks like it needs a search over all renamings, which grows like the factorial. Babai showed that it can be done in time only a little more than any polynomial. The method follows an older plan: describe the possible renamings as a group, and break the problem into smaller ones along the structure of the group. That plan works except when the group can shuffle many pieces in every possible way. For that case Babai found a way to either prove that the shuffles really are symmetries, or to discover hidden structure that breaks the symmetry and cuts the problem down by a large factor.

## The problem

The input is two simple undirected graphs $X$ and $Y$ on $n$ vertices, with optional vertex colors that isomorphisms must keep; directed and edge-colored graphs reduce to this case. The output is an isomorphism or the answer that none exists. Babai solves the more general **string isomorphism** problem: given a permutation group $G$ on a set $\Omega$ of size $n$, by generators, and two strings $x, y : \Omega \to$ colors, find $\mathrm{Iso}_G(x, y) = \{ g \in G : x(d) = y(g(d)) \text{ for all } d \}$, which is empty or a coset of the group $\mathrm{Aut}_G(x)$. Graph isomorphism is the case where $G$ is the symmetric group on the vertices acting on vertex pairs, and $x$, $y$ mark the edges.

**What is proven.** Babai's theorem: string isomorphism, and hence graph isomorphism, can be solved in time $\exp((\log n)^{O(1)})$. The proof relies on the classification of finite simple groups, through results on large primitive groups. In 2019 Babai announced canonical forms of graphs in the same time bound.

## The algorithm

The pseudocode shows the framework that the implementation follows, which is Luks's recursion with the bottleneck detected. Babai's new tools replace the coset loop in the bottleneck case; they are described after it.

```pseudo id=main
STRING-ISO(G, Δ, x, y)
L1  if Δ = {d} then return (G, id) if x(d) = y(d), else none
L2  if G is not transitive on Δ then combine the orbits one by one with the chain rule, as in Luks's algorithm
L3  B ← a system of maximal blocks of G on Δ; φ ← the action of G on B, which is primitive
L4  giant ← whether φ(G) contains the alternating group on B, with |B| above a threshold
L5  N ← the kernel of φ; T ← a transversal of N in G
L6  for each t in T: R_t ← STRING-ISO(N, Δ, x, y ∘ t); if R_t = (A, g) then τ_t ← g t
L7  return none if every R_t is none, else (⟨A, τ_t τ_1^(-1) for all t⟩, τ_1)
```

For graphs, the implementation first runs [color refinement](/weisfeiler-leman/) on both graphs with shared color names, rejects if the color counts differ, renames the second graph so that classes coincide, and takes $G$ as the product of the symmetric groups on the classes.

**Where Luks's recursion is slow.** The loop in L6 runs over $|\varphi(G)|$ cosets. By a theorem of Cameron, sharpened by Maróti, a primitive group of degree $m$ that is not a so-called Cameron group has order at most $m^{O(\log m)}$, so the loop is quasipolynomial unless $\varphi(G)$ is a Cameron group: essentially the alternating or symmetric group $A_k$ or $S_k$ acting on the $t$-subsets of a $k$-set, or a product of such. A Cameron group gives a homomorphism of $G$ onto $A_k$ or $S_k$ with $k$ large, a **giant**. That case is the bottleneck, and the following tools handle it.

- **Local certificates.** For a test set $T$ of a few of the $k$ points, of logarithmic size, Babai computes, by a Luks-type recursion on a smaller problem, whether the restriction of $\mathrm{Aut}_G(x)$ to $T$ is a giant ("full") or not, together with a certificate. If many test sets are full, the certificates generate a subgroup of $\mathrm{Aut}_G(x)$ that maps onto a giant, which reduces the problem. Otherwise the certificates of the non-full test sets give a canonical structure on the $k$ points.
- **Split or Johnson.** Given such structure, a procedure based on $k$-ary coherent configurations, the setting of [Weisfeiler-Leman](/k-dimensional-weisfeiler-leman/) refinement, with individualization of polylogarithmically many points, finds either a canonical coloring in which no class is large, or a canonically embedded Johnson scheme, a large set identified with the $t$-subsets of a smaller set. Either outcome lets the recursion continue on a substantially smaller instance at a quasipolynomial multiplicative cost.
- **The Design Lemma and the Unaffected Stabilizers Theorem** are the main combinatorial and group-theoretic results that make these steps work; the second uses the classification of finite simple groups.

The analysis shows that each reduction costs at most a quasipolynomial factor and shrinks the instance enough that the whole recursion stays quasipolynomial.

## Example

The implementation counts the transitive cases of L4 as "small" or "giant". All values were computed with it.

| pair | color refinement | transitive cases: small, giant | result |
|---|---|---|---|
| $C_6$ and $2K_3$ | not distinguished, both 2-regular | 1, 0 | not isomorphic |
| $K_{3,3}$ and the prism | not distinguished, both 3-regular | 1, 0 | not isomorphic |
| wheel $W_6$ (hub 0 and rim $C_6$) and hub joined to $2K_3$ | hub and rim split, rim not split | 1, 1 | not isomorphic |
| $W_6$ and $W_6$ with the rim renamed | as above | 1, 1 | isomorphic, $\varphi = (0, 1, 3, 5, 2, 4, 6)$, 12 automorphisms |
| path $P_4$ and star $K_{1,3}$ | distinguished by degrees | 0, 0 | not isomorphic |

In the wheel the hub has its own color and $G$ is $S_6$ on the rim. On the 6 spokes, the vertex pairs $\{0, i\}$, $G$ acts as the full $S_6$: a giant, detected in L4. On the 15 rim pairs it acts as $S_6$ on 2-subsets, which is primitive but not a giant on 15 points; it is a Cameron group, the Johnson case, and Babai's algorithm would treat it through the giant homomorphism onto $S_6$. In this model both are handled by the coset loop: the 720 elements of $S_6$ are cheap here, but $S_k$ grows like $k!$, which is exactly the cost Babai's tools avoid.

## Correctness

The [full proof](proofs/correctness.md) covers the implementation, not the quasipolynomial bound.

- **Cosets.** The solutions of a string isomorphism problem form a coset $A\tau$, so a pair of generators and one element describes them.
- **Chain rule and kernel cosets.** Splitting along orbits, and along the cosets of the kernel of the action on blocks, are exact decompositions of the solution set, as in Luks's algorithm.
- **Refinement.** Joint color refinement only removes permutations that cannot be isomorphisms, since an isomorphism keeps refined colors.
- **Termination.** The window shrinks, or stays the same while the group becomes intransitive.

For Babai's tools, correctness rests on the structure theorems of the paper: each reduction either finds automorphisms that genuinely lie in $\mathrm{Aut}_G(x)$, or a structure defined canonically, so that isomorphisms must respect it.

## Complexity

| case | time |
|---|---|
| Babai (2015, repaired 2017) | $\exp((\log n)^{O(1)})$ |
| Babai and Luks (1983), the previous best for general graphs | $\exp(O(\sqrt{n \log n}))$ |
| the implementation on this page, no giant or Cameron group of large degree | Luks's bound for the groups that occur |
| the implementation on this page, worst case | exponential, since the coset loop enumerates giants |

Babai's paper proves the bound with an unspecified constant in the exponent of $\log n$. The quasipolynomial bound is far below the trivial $n!$ but above every polynomial. Isomorphism of groups given by multiplication tables reduces to graph isomorphism and has a simple $n^{O(\log n)}$ algorithm, with no known faster one in general, so a bound for graphs well below $n^{O(\log n)}$ would also improve the bound for groups.

## Properties

- **Deterministic and exact.** No randomness and no heuristics; the answer is always right.
- **General.** It applies to every problem in the class [GI](/gi-completeness/), through polynomial-time reductions.
- **Group-theoretic.** It uses the classification of finite simple groups, as Luks's bounds for bounded degree do in their sharpest form.
- **Theoretical.** No practical implementation is known to compete with [individualization-refinement](/individualization-refinement/) tools such as [nauty](/nauty/), which are exponential in the worst case but fast on almost all inputs.

## Variants and improvements

- **Canonical forms.** Babai (STOC 2019) extended the result to canonical labeling in quasipolynomial time.
- **Groups.** Isomorphism of groups given by multiplication tables remains at $n^{O(\log n)}$ in general and is a barrier for further progress.
- **Bounded degree.** Grohe, Neuen and Schweitzer (2018) adapted Babai's methods to graphs of maximum degree $d$, in time $n^{\mathrm{polylog}(d)}$; see [bounded-degree graph isomorphism](/bounded-degree-graph-isomorphism/).
- **Expositions.** Helfgott wrote a detailed exposition of the algorithm for the Bourbaki seminar (2017), with an English version by Helfgott, Bajpai and Dona; Helfgott found the error in the original analysis while preparing it.

## When to use it

Use it as a theoretical result: to know that graph isomorphism, and every problem that reduces to it, is solvable in quasipolynomial time, and as a source of techniques, such as local certificates and the split-or-Johnson routine, for other problems on groups and combinatorial structures. To decide isomorphism of actual graphs, use [nauty](/nauty/), Traces or [bliss](/bliss/), and use [color refinement](/weisfeiler-leman/) as a fast filter.

## Pitfalls

- **Overstating the result.** It is quasipolynomial, not polynomial; whether graph isomorphism is in P remains open.
- **Stating an explicit exponent.** The published bound is $\exp((\log n)^{O(1)})$; quote a specific exponent only from a source that proves it.
- **Ignoring the 2017 correction.** The first version of the analysis had an error, found by Helfgott; Babai's fix restored the quasipolynomial bound, and citations should refer to the corrected arXiv versions.
- **Taking the model for the algorithm.** The implementation on this page shows where the bottleneck is but solves it by brute force, so it is exponential on graphs whose groups contain large giants.

## Implementations

## History

Graph isomorphism had resisted a subexponential bound until Babai and Luks reached $\exp(O(\sqrt{n \log n}))$ in 1983, building on Luks's bounded-degree algorithm and Zemlyachenko's degree reduction. For more than thirty years that bound was the best known. Babai announced the quasipolynomial algorithm in a series of talks in Chicago in November 2015, posted the paper in December 2015, and presented it at STOC 2016. In January 2017 Helfgott, while checking the proof, found an error in the analysis of one step; Babai first retracted the quasipolynomial claim, then within days announced a fix that restored it. He announced canonical forms in the same time bound at STOC 2019.

## References
