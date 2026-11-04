---
tag: EXDCQH
kind: concept
slug: polynomial-time-equivalence
name: Polynomial-time equivalence of problems
aliases:
- polynomially equivalent problems
- interreducibility
area: techniques/reductions-and-transforms
level: core
summary: Two problems are equivalent when each reduces to the other in polynomial time, so they have the same complexity.
prereqs: [reduction, polynomial-time-reduction, p, np]
see_also: [np-complete, transitivity-of-reductions, independent-set, vertex-cover, clique, search-to-decision-reduction, fine-grained-equivalence-class, ladner-theorem]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 8.1, Polynomial-time reductions (independent set and vertex cover reduce to each other; transitivity)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 34.3, NP-completeness and reducibility; Section 34.5, NP-complete problems (the clique and vertex cover problems, with the reduction through the complement graph)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum, 1972, 85-103"
    locator: the polynomial-time complete problems and their reductions, including clique, node cover and set packing
  - paper: doi:10.1145/321864.321877
    title: "Richard E. Ladner, On the structure of polynomial time reducibility, Journal of the ACM 22(1) (1975), 155-171"
    locator: the theorem that, if P is not NP, then NP has problems that are neither in P nor NP-complete
---

Two problems $A$ and $B$ are polynomial-time equivalent when $A$ reduces to $B$ and $B$ reduces to $A$ by [polynomial-time reductions](/polynomial-time-reduction/). The relation is an equivalence relation, and equivalent problems are either both in [P](/p/) or both outside it. All [NP-complete](/np-complete/) problems form one class of this relation, and so do the decision, search and optimization forms of problems such as [vertex cover](/vertex-cover/).

## In plain words

Two problems are equivalent when each one can be rewritten as the other with a fast translation. Then a fast method for either one gives a fast method for both, and a proof that one of them has no fast method covers the other as well. In this sense they are the same problem in two costumes.

Equivalence is a coarse measure. It ignores how fast the translation is, as long as it is fast in the broad sense. Two equivalent problems can still differ a lot in practice, for example one taking about twice the time of the other, or the square of it.

Many familiar problems fall in one big group: finding a large set of vertices with no edges between them, a small set that touches every edge, or a large set where every pair is joined. A single trick links each of these to the others.

## The idea

### Definition

Write $A \le_m^p B$ when $A$ many-one reduces to $B$ in polynomial time: there is a function $f$, computable in polynomial time, with $x \in A \iff f(x) \in B$ for every $x$ (see [reduction](/reduction/)). Then

$$A \equiv_p B \quad\Longleftrightarrow\quad A \le_m^p B \ \text{ and } \ B \le_m^p A.$$

For search and optimization problems, which have answers other than yes and no, the same definition is used with Turing reductions $\le_T^p$, and the relation is written $\equiv_T^p$.

**Theorem 1.** $\equiv_p$ is an equivalence relation on decision problems. So is $\equiv_T^p$.

*Proof.* Reflexive: the identity map $f(x) = x$ is computable in linear time and gives $x \in A \iff f(x) \in A$, so $A \le_m^p A$. Symmetric: the definition is symmetric in $A$ and $B$. Transitive: let $A \equiv_p B$ and $B \equiv_p C$. Then $A \le_m^p B \le_m^p C$ and $C \le_m^p B \le_m^p A$. The composition of two polynomial-time reductions is a polynomial-time reduction (Lemma 2 of [reduction](/reduction/), stated as a theorem on [transitivity of reductions](/transitivity-of-reductions/)), so $A \le_m^p C$ and $C \le_m^p A$. The same three steps work for $\le_T^p$: a machine that copies its input to the oracle and returns the answer gives reflexivity, and Lemma 2 covers Turing reductions as well. $\square$

### What equivalent problems share

**Theorem 2.** If $A \equiv_p B$, then $A \in$ P if and only if $B \in$ P, and $A \in$ [NP](/np/) if and only if $B \in$ NP.

*Proof.* If $B \in$ P, then $A \le_m^p B$ gives $A \in$ P by Lemma 1 of [reduction](/reduction/). By symmetry, $A \in$ P gives $B \in$ P. For NP, the same page shows that a problem that many-one reduces to a problem in NP is in NP; apply it in both directions. $\square$

**Theorem 3.** Any two NP-complete problems are polynomial-time equivalent.

*Proof.* Let $A$ and $B$ be NP-complete. Then $A \in$ NP and $B$ is [NP-hard](/np-hard/), so $A \le_m^p B$. In the same way $B \le_m^p A$. $\square$

So the NP-complete problems form one equivalence class. By Theorem 2, this class lies inside P if P $=$ NP and is disjoint from P if P $\ne$ NP. Ladner (1975) proved that, if P $\ne$ NP, then NP also has problems that are neither in P nor NP-complete ([Ladner's theorem](/ladner-theorem/), [NP-intermediate](/np-intermediate/)). Such a problem is not equivalent to SAT.

**Theorem 4.** Inside P there are exactly three classes of $\equiv_p$: $\{\emptyset\}$, $\{\Sigma^*\}$, and all other problems of P.

*Proof.* Let $A \in$ P, and let $B$ have a yes-instance $b_1$ and a no-instance $b_0$. The map $f(x) = b_1$ if $x \in A$, and $f(x) = b_0$ otherwise, is computable in polynomial time, since $A \in$ P, and gives $x \in A \iff f(x) \in B$. So $A \le_m^p B$. If $A$ and $B$ are both in P and both have yes- and no-instances, this gives $A \equiv_p B$. A problem $A$ reduces to $\emptyset$ only if no $x$ has $f(x) \in \emptyset$, that is, only if $A = \emptyset$. In the same way only $\Sigma^*$ reduces to $\Sigma^*$. $\square$

Theorem 4 shows the limit of the concept: polynomial-time equivalence cannot tell apart two nontrivial decision problems in P, such as "is this list sorted?" and "is this graph connected?". Finer relations, with reductions that keep the exponent of the running time, are the subject of [fine-grained equivalence classes](/fine-grained-equivalence-class/).

### Decision, search and optimization

Let $\tau(G)$ be the size of a minimum [vertex cover](/vertex-cover/) of a graph $G$ with $n$ vertices. Consider three problems: the decision problem "is $\tau(G) \le k$?", the optimization problem "compute $\tau(G)$", and the search problem "find a vertex cover of size $\tau(G)$". They are polynomial-time Turing equivalent.

*Decision from optimization.* One call to compute $\tau(G)$, then compare with $k$.

*Optimization from decision.* Ask "is $\tau(G) \le k$?" for $k = 0, 1, \ldots, n$ and stop at the first yes: at most $n + 1$ calls. Binary search on $k$ uses $\lceil \lg(n + 1) \rceil$ calls.

*Search from decision.* For a vertex $v$, let $G - v$ be $G$ without $v$ and its edges. First: some minimum cover of $G$ contains $v$ if and only if $\tau(G - v) = \tau(G) - 1$. If $C$ is a minimum cover with $v \in C$, then $C \setminus \{v\}$ covers $G - v$, so $\tau(G - v) \le \tau(G) - 1$. Any cover $D$ of $G - v$ gives the cover $D \cup \{v\}$ of $G$, so $\tau(G) \le \tau(G - v) + 1$. Together, $\tau(G - v) \ge \tau(G) - 1$ always, and equality holds when a minimum cover contains $v$. Conversely, if $\tau(G - v) = \tau(G) - 1$, a minimum cover $D$ of $G - v$ gives the cover $D \cup \{v\}$ of size $\tau(G)$, a minimum cover that contains $v$.

The algorithm keeps a current graph $H$ (first $G$), a set $C$ (first empty) and $k = \tau(H)$. It takes the vertices $v$ of $G$ one by one. If $\tau(H - v) = k - 1$, it adds $v$ to $C$, sets $H \leftarrow H - v$ and $k \leftarrow k - 1$. Invariant: $\tau(H) = k$, and $C$ together with any minimum cover of $H$ is a minimum cover of $G$. At the end $k = 0$. Suppose not: then a minimum cover of the final $H$ contains some vertex $v$. When $v$ was tested, the current graph was $H' = H + T$ for the set $T$ of vertices taken later, with $\tau(H) = \tau(H') - |T|$, and $v$ was not taken, so no minimum cover of $H'$ contained $v$. But a minimum cover $D$ of $H$ with $v \in D$ gives the cover $D \cup T$ of $H'$ of size $\tau(H')$, a minimum cover with $v$. This is a contradiction. So $H$ has no edges, and $C$ is a minimum cover of $G$. The algorithm uses one computation of $\tau(G)$ and then $n$ calls of the decision problem with bound $k - 1$. See [search-to-decision reduction](/search-to-decision-reduction/) and [self-reducibility](/self-reducibility/).

## Examples

### Independent set and vertex cover

Let $G = (V, E)$ with $n = |V|$. A set $S \subseteq V$ is an [independent set](/independent-set/) when no edge has both endpoints in $S$, and a vertex cover when every edge has at least one endpoint in $S$.

**Lemma.** $S$ is independent if and only if $V \setminus S$ is a vertex cover.

*Proof.* $S$ is independent if and only if every edge has at most one endpoint in $S$, that is, at least one endpoint in $V \setminus S$, that is, $V \setminus S$ is a vertex cover. $\square$

So $G$ has an independent set of size at least $k$ if and only if it has a vertex cover of size at most $n - k$. The map $(G, k) \mapsto (G, n - k)$ reduces independent set to vertex cover, and the same map reduces vertex cover to independent set (Kleinberg and Tardos, Section 8.1). Both maps take linear time. So $\mathrm{IS} \equiv_p \mathrm{VC}$, with no need to know that either problem is NP-complete.

### Clique and independent set

A set $S$ is a [clique](/clique/) of $G$ if and only if it is independent in the [complement graph](/complement-graph/) $\bar{G}$, which has an edge exactly where $G$ has none. The map $(G, k) \mapsto (\bar{G}, k)$ reduces clique to independent set and, since $\bar{\bar{G}} = G$, also independent set to clique. It takes $O(n^2)$ time. Together with the lemma, $(G, k) \mapsto (\bar{G}, n - k)$ reduces clique to vertex cover, which is the reduction in CLRS Section 34.5.

### A worked case

Take $V = \{1, \ldots, 6\}$ and the seven edges $12, 13, 23, 34, 45, 46, 56$: two triangles joined by the edge $34$.

| Quantity | Value | One optimal set |
|---|---|---|
| largest independent set | 2 | $\{1, 4\}$ |
| smallest vertex cover | 4 | $\{2, 3, 5, 6\}$ |
| largest clique of $\bar{G}$ (8 edges) | 2 | $\{1, 4\}$ |

The independent set $\{1, 4\}$ and the cover $\{2, 3, 5, 6\}$ are complements, and $4 = 6 - 2$. The graph has $8$ independent sets of size $2$ and $8$ vertex covers of size $4$, and the map $S \mapsto V \setminus S$ is a bijection between them. For every $k$ from $0$ to $6$, "independent set of size $k$" and "vertex cover of size $6 - k$" have the same answer: yes for $k \le 2$, no for $k \ge 3$. The search algorithm above, with the vertices in the order $1, \ldots, 6$, takes $1$, $2$, $4$, $5$ and returns the cover $\{1, 2, 4, 5\}$ after $1 + 6 = 7$ calls.

### A pair that is not known to be equivalent

[2-SAT](/2-sat/) reduces to [3-SAT](/3-sat/): repeat a literal to fill each clause. The other direction holds if and only if P $=$ NP. If $3\text{-SAT} \le_m^p 2\text{-SAT}$, then 3-SAT is in P by Theorem 2, since 2-SAT is in P, and so P $=$ NP. If P $=$ NP, then 3-SAT is in P, and Theorem 4 gives $3\text{-SAT} \le_m^p 2\text{-SAT}$.

## Where it is used

- **NP-completeness proofs.** One reduction from a known NP-complete problem to a new problem in NP puts the new problem in the class of Theorem 3. Karp's list ([Karp's 21 NP-complete problems](/karps-21-np-complete-problems/)) was built this way. See [NP-hardness reductions](/np-hardness-reductions/).
- **Choosing a problem to reduce from.** Since independent set, vertex cover and clique are equivalent by short maps, a hardness proof can start from whichever of them has the closest structure.
- **Search versus decision.** The [optimization-to-decision reduction](/optimization-to-decision-reduction/) and the [search-to-decision reduction](/search-to-decision-reduction/) justify the study of decision problems only.
- **Fine-grained complexity.** Equivalence with exponents kept: for example the [APSP and negative triangle equivalence](/apsp-negative-triangle-equivalence/) and the [equivalence of matrix multiplication and inversion](/matrix-multiplication-inversion-equivalence/).
- **The structure of NP.** [Ladner's theorem](/ladner-theorem/) shows that, if P $\ne$ NP, NP has classes of $\equiv_p$ other than the classes inside P and the class of the NP-complete problems.

## References
