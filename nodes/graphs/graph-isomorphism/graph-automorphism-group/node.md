---
tag: JRNSSN
kind: concept
slug: graph-automorphism-group
name: Automorphism group of a graph
aliases:
- Aut(G)
- automorphism group
area: graphs/graph-isomorphism
level: intro
summary: The group of all isomorphisms from a graph onto itself, under composition.
prereqs: [graph-isomorphism-definition, symmetric-group, subgroup]
see_also: [graph-automorphism, automorphism-orbit, asymmetric-graph, almost-all-graphs-asymmetric, nauty, canonical-labeling, burnside-lemma, lagranges-theorem-group-theory]
sources:
  - book: isbn:9780387952208
    title: Chris Godsil and Gordon Royle, Algebraic Graph Theory, Springer, Graduate Texts in Mathematics 207, 2001
    locator: Chapter 1, Graphs (automorphisms, Section 1.2) and Chapter 2, Groups (permutation groups, orbits, the orbit-stabilizer lemma)
  - paper: "Robert Frucht, Herstellung von Graphen mit vorgegebener abstrakter Gruppe, Compositio Mathematica 6, 239 to 250 (1939)"
    locator: the whole paper (every finite group is the automorphism group of a finite graph)
  - paper: doi:10.1016/0020-0190(79)90004-8
    title: Rudolf Mathon, A note on the graph isomorphism counting problem, Information Processing Letters 8(3), 131 to 132 (1979)
    locator: the whole paper (counting isomorphisms and computing the order of the automorphism group are polynomial-time equivalent to deciding isomorphism)
---

The automorphism group $\mathrm{Aut}(G)$ of a graph $G$ is the set of all [isomorphisms](/graph-isomorphism-definition/) from $G$ to itself, with composition of maps as the group operation. It is a [subgroup](/subgroup/) of the [symmetric group](/symmetric-group/) on the vertex set, and it measures how symmetric the graph is: the identity alone for an [asymmetric graph](/asymmetric-graph/), all $n!$ permutations for the complete graph. Isomorphism algorithms such as [nauty](/nauty/) compute it, given by a few generators, as a by-product of [canonical labeling](/canonical-labeling/), and use it to prune their search.

## In plain words

Draw a graph, then rename its vertices. If every edge of the old drawing is still an edge after the renaming, and no new edge appears, the renaming is a symmetry of the graph. A square has eight such symmetries: four turns and four flips.

The symmetries of a graph form a group. Doing one symmetry after another gives a symmetry, doing nothing is a symmetry, and each symmetry can be undone. The group tells you which vertices look exactly alike from inside the graph. It also tells you how many different ways there are to write down the same graph with names: the more symmetric the graph, the fewer distinct namings it has.

## The idea

**Definition.** Let $G = (V, E)$ be a graph with $|V| = n$. A permutation $\sigma$ of $V$ is an automorphism of $G$ when $\{u, v\} \in E \iff \{\sigma(u), \sigma(v)\} \in E$ for all $u, v \in V$. The set

$$\mathrm{Aut}(G) = \{ \sigma \in \mathrm{Sym}(V) : \sigma(E) = E \}$$

is a group under composition. For directed, colored or labeled graphs, $\sigma$ must also keep directions, colors or labels; giving each vertex its own color makes the group trivial, which is how [individualization](/individualization-refinement/) removes symmetry.

**It is a group.** The identity keeps $E$. If $\sigma$ and $\tau$ keep $E$, then $\sigma \tau$ keeps $E$. If $\sigma$ keeps $E$, then $\sigma$ maps $E$ into $E$ and is injective on the finite set of 2-element subsets, so it is a bijection of $E$ onto $E$, and $\sigma^{-1}$ keeps $E$ too.

**Basic facts.**

1. $\mathrm{Aut}(G) = \mathrm{Aut}(\overline G)$, where $\overline G$ is the [complement](/complement-graph/): a permutation keeps the edge set exactly when it keeps the set of non-edges.
2. **Labeled copies.** The number of graphs on the vertex set $V$ that are isomorphic to $G$ is $n! / |\mathrm{Aut}(G)|$. The map $\pi \mapsto \pi(G)$ from $\mathrm{Sym}(V)$ to graphs on $V$ has fibers that are the cosets $\pi \mathrm{Aut}(G)$, and each coset has $|\mathrm{Aut}(G)|$ elements.
3. **Isomorphisms form a coset.** If $\varphi$ is one isomorphism from $G$ to $H$, the set of all isomorphisms from $G$ to $H$ is $\varphi \, \mathrm{Aut}(G)$. So once one isomorphism is known, the automorphism group describes all of them.
4. **Orbit-stabilizer.** For a vertex $v$, the [orbit](/automorphism-orbit/) $\mathrm{Aut}(G) \cdot v$ and the stabilizer $\mathrm{Aut}(G)_v = \{ \sigma : \sigma(v) = v \}$ satisfy $|\mathrm{Aut}(G)| = |\mathrm{Aut}(G) \cdot v| \cdot |\mathrm{Aut}(G)_v|$. Applied along a chain of stabilizers of $v_1, v_2, \ldots$, this gives the order of the group as a product of orbit lengths, which is how programs compute it.
5. **Every group occurs.** For each finite group $\Gamma$ there is a finite graph $G$ with $\mathrm{Aut}(G) \cong \Gamma$ (Frucht 1939).

**Representation.** The group can have up to $n!$ elements, so programs never list it. They store a set of generators. Every subgroup of $\mathrm{Sym}(n)$ has a generating set of at most $n - 1$ elements, and from generators the Schreier-Sims method computes the order and tests membership in polynomial time.

**Complexity.** Computing generators of $\mathrm{Aut}(G)$ is the [graph automorphism problem](/graph-automorphism/). It is polynomial-time equivalent to the [graph isomorphism problem](/graph-isomorphism-problem/), and so is computing $|\mathrm{Aut}(G)|$ (Mathon 1979). Deciding only whether a non-identity automorphism exists reduces to isomorphism, but no reduction in the other direction is known.

## Examples

| graph | $n$ | $\mathrm{Aut}(G)$ | order | labeled copies $n!/\lvert\mathrm{Aut}\rvert$ |
|---|---|---|---|---|
| complete graph $K_n$ | $n$ | $\mathrm{Sym}(n)$ | $n!$ | 1 |
| path $P_n$, $n \ge 2$ | $n$ | identity and reversal | 2 | $n!/2$ |
| cycle $C_n$, $n \ge 3$ | $n$ | dihedral group $D_n$ | $2n$ | $(n-1)!/2$ |
| star $K_{1,3}$ | 4 | $\mathrm{Sym}(3)$ on the leaves | 6 | 4 |
| cube $Q_3$ | 8 | $\mathrm{Sym}(3) \ltimes \mathbb Z_2^3$ | 48 | 840 |
| Petersen graph | 10 | $\mathrm{Sym}(5)$ | 120 | 30240 |
| $4 \times 4$ rook's graph | 16 | $(\mathrm{Sym}(4) \times \mathrm{Sym}(4)) \rtimes \mathbb Z_2$ | 1152 | |
| Shrikhande graph | 16 | | 192 | |

**The 6-cycle.** With vertices $0, \ldots, 5$ and edges $\{i, i+1 \bmod 6\}$, the rotations $i \mapsto i + r$ and the reflections $i \mapsto r - i$ (mod 6) for $r = 0, \ldots, 5$ are the 12 automorphisms. The orbit of vertex 0 is all 6 vertices and its stabilizer is $\{ \mathrm{id}, i \mapsto -i \}$, and $6 \cdot 2 = 12$.

**The Petersen graph.** Its vertices are the 2-element subsets of $\{1, \ldots, 5\}$, adjacent when disjoint. Each permutation of $\{1, \ldots, 5\}$ acts on the subsets and keeps disjointness, which gives 120 automorphisms; there are no others.

**Two graphs with the same parameters, different groups.** The rook's graph and the Shrikhande graph are both strongly regular with parameters $(16, 6, 2, 2)$, but their groups have orders 1152 and 192. Both groups are transitive on the 16 vertices, so the stabilizer of a vertex has order 72 and 12.

**Smallest asymmetric graphs.** Every graph with 2 to 5 vertices has a non-identity automorphism. On 6 vertices, 8 of the 156 isomorphism classes are [asymmetric](/asymmetric-graph/).

## Where it is used

- **Isomorphism and canonical labeling.** [nauty](/nauty/), [bliss](/bliss/) and Traces find automorphisms during the search and use them to skip branches that are images of branches already explored ([individualization-refinement](/individualization-refinement/)).
- **Counting and generation.** The count $n!/|\mathrm{Aut}(G)|$ links labeled and unlabeled enumeration, and [Burnside's lemma](/burnside-lemma/) counts objects up to symmetry. Generators of non-isomorphic graphs use automorphisms to avoid duplicates.
- **Symmetry breaking.** SAT solvers and integer programs add constraints that cut symmetric copies of solutions, using the automorphism group of a graph built from the formula; see [orbital branching](/orbital-branching/) and [symmetry reduction](/symmetry-reduction/).
- **Group-theoretic isomorphism tests.** [Luks's algorithm](/luks-algorithm/) and [Babai's algorithm](/babai-quasipolynomial-algorithm/) work with cosets of automorphism groups throughout.
- **Random graphs.** [Almost all graphs](/almost-all-graphs-asymmetric/) have the trivial group.

## References
