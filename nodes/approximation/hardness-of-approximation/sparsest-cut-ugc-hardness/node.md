---
tag: TMW3A6
kind: theorem
slug: sparsest-cut-ugc-hardness
name: Sparsest cut UGC hardness
aliases:
- Khot-Vishnoi sparsest cut hardness
- UGC hardness of sparsest cut
- CKKRS theorem
area: approximation/hardness-of-approximation
level: research
summary: If the Unique Games Conjecture holds, then non-uniform sparsest cut and multicut have no constant-factor approximation in polynomial time unless P = NP.
prereqs: [unique-games-conjecture, sparsest-cut-problem, multicut-problem, fourier-analysis-of-boolean-functions]
see_also: [max-cut-ugc-hardness, integrality-gap, semidefinite-programming, metric-tree-embedding, unique-games-subexponential-algorithm, long-code, raghavendra-theorem]
sources:
  - paper: doi:10.1007/s00037-006-0210-9
    title: Shuchi Chawla, Robert Krauthgamer, Ravi Kumar, Yuval Rabani and D. Sivakumar, On the hardness of approximating multicut and sparsest-cut, Computational Complexity 15(2), 94 to 114, 2006 (CCC 2005)
    locator: Theorem 1.2 (the quantitative reduction from unique games), Corollaries 1.3 and 1.4, and the reduction through bicriteria multicut on hypercubes
  - paper: doi:10.1145/2629614
    title: Subhash Khot and Nisheeth K. Vishnoi, The Unique Games Conjecture, integrality gap for cut problems and embeddability of negative-type metrics into l1, Journal of the ACM 62(1), Article 8, 2015 (FOCS 2005)
    locator: the UG-hardness of non-uniform sparsest cut and balanced separator, and the integrality gap for the SDP with triangle inequalities
  - paper: "Sanjeev Arora, Satish Rao and Umesh Vazirani, Expander flows, geometric embeddings and graph partitioning, Journal of the ACM 56(2), Article 5, 2009 (STOC 2004)"
    locator: the O(sqrt(log n)) approximation for uniform sparsest cut
  - paper: "Sanjeev Arora, James R. Lee and Assaf Naor, Euclidean distortion and the sparsest cut, Journal of the American Mathematical Society 21(1), 1 to 21, 2008 (STOC 2005)"
    locator: the O(sqrt(log k) log log k) approximation for non-uniform sparsest cut with k demand pairs
---

Two groups proved in 2005, independently, that if the [Unique Games Conjecture](/unique-games-conjecture/) holds, then the non-uniform [sparsest cut problem](/sparsest-cut-problem/) has no constant-factor approximation algorithm unless P = NP: Chawla, Krauthgamer, Kumar, Rabani and Sivakumar (CKKRS), and Khot and Vishnoi (KV). CKKRS prove the same for [multicut](/multicut-problem/), and give a quantitative form that turns stronger versions of the conjecture into hardness factors that grow with $n$. Khot and Vishnoi also turned their reduction into an [integrality gap](/integrality-gap/) for the standard semidefinite relaxation, which disproved the Goemans-Linial conjecture on embedding negative type metrics into $\ell_1$. The best algorithms reach $O(\sqrt{\log k}\,\log\log k)$ for $k$ demand pairs, so the true threshold lies somewhere between a constant and that.

## Statement

On this page sparsest cut and multicut are minimization problems, and an $\alpha$-approximation finds a solution with $\mathrm{ALG} \le \alpha \cdot \mathrm{OPT}$, $\alpha \ge 1$.

An instance of *non-uniform sparsest cut* has a graph $G = (V, E)$ with capacities $c : E \to \mathbb{R}_{\ge 0}$ and demand pairs $(s_1, t_1), \ldots, (s_k, t_k)$ with demands $D_i > 0$. The sparsity of a set $S \subseteq V$ is

$$\Psi(S) = \frac{\sum_{e \in \delta(S)} c(e)}{\sum_{i : |S \cap \{s_i, t_i\}| = 1} D_i},$$

and the task is to find a set $S$ of least sparsity. In the *uniform* version every pair of vertices is a demand pair with demand $1$. An instance of *multicut* has the same data, and the task is to remove edges of least total capacity so that every $s_i$ is separated from its $t_i$.

**Theorem (CKKRS 2006, Theorem 1.2).** There are constants $c_1, c_2 > 0$ with the following property. Suppose that for functions $\eta(n)$ and $\delta(n)$ it is NP-hard to tell unique games on $n$ vertices with at most $O(\log n)$ labels and value at least $1 - \eta(n)$ from those with value at most $\delta(n)$. Then it is NP-hard to approximate multicut, non-uniform sparsest cut and Min-2CNF$\equiv$ Deletion within

$$L(n) = c_1 \min\Big\{ \frac{1}{\eta(n^{c_2})},\ \log \frac{1}{\delta(n^{c_2})} \Big\}.$$

For sparsest cut the hardness is for finding a sparse cut. It is a Cook reduction, so it applies to the search version, not to the version that only estimates the value.

**Corollary (CKKRS 2006, Corollary 1.3; KV 2005).** If the Unique Games Conjecture holds, then for every constant $C \ge 1$ it is NP-hard to approximate non-uniform sparsest cut, or multicut, within $C$.

The corollary follows from the theorem with constant $\eta$ and $\delta$: as $\eta, \delta \to 0$ the bound $L$ grows above every constant. CKKRS also show (Corollary 1.4) that a stronger form of the conjecture, with $\eta$ and $\delta$ shrinking with $n$, gives hardness $\Omega(\sqrt{\log\log n})$.

## In plain words

In this problem a network has links with costs and a list of pairs of points that want to talk. The goal is to split the network into two parts so that the cost of the links that are cut is small compared with the number of pairs that are split apart. This theorem says that, if a well-known guess about unique games is true, then no fast method can always get within any fixed factor of the best split. The proof builds a cube for each point of the puzzle and asks to separate opposite corners of every cube. The cheapest way to do that cuts each cube in half along one direction, and that direction tells the label of the point. A cheap answer in the built network must look like such direction cuts, so it gives a good answer to the puzzle.

## Proof

A sketch is in [proofs/sketch.md](proofs/sketch.md). It proves in full the hypercube fact that drives completeness: in the cube $\{0,1\}^m$ with each antipodal pair as a demand, every cut has at least as many cut edges as separated pairs, and a cut along one coordinate has exactly as many. The rest of the reduction, which uses a junta theorem for soundness and a reduction from bicriteria multicut to sparsest cut, is described in outline and cited from CKKRS.

The reduction, in short. For each vertex $v$ of a unique game with $m$ labels, take a copy of the cube $\{0,1\}^m$. For each constraint $(u, v, \pi)$, join $(u, x)$ to $(v, \pi(x))$, where $\pi$ permutes the coordinates. The demand pairs are the antipodal pairs $(v, x)$ and $(v, \bar x)$ of each cube.

- *Completeness.* A labeling $\ell$ that satisfies a $1 - \eta$ fraction of the constraints gives the cut that splits each cube along coordinate $\ell(v)$. It separates every antipodal pair and cuts a $1/m$ fraction of the cube edges, plus the edges of the violated constraints.
- *Soundness.* A cheap cut that separates most antipodal pairs must, on most cubes, have small total influence. A junta theorem then says it depends mostly on few coordinates, and those coordinates, matched across the edges of the game, give a labeling that satisfies a fraction of the constraints that is exponentially small in the cost ratio. This is the source of the term $\log(1/\delta)$ in $L(n)$.

## Consequences

- **No constant factor.** Under the UGC, the gap between the $O(1)$ hardness for constant parameters and the $O(\sqrt{\log k}\,\log\log k)$ algorithm of Arora, Lee and Naor is the open region for non-uniform sparsest cut.
- **Multicut.** The same holds for multicut, where the best known ratio is $O(\log k)$ by region growing.
- **Integrality gap.** Khot and Vishnoi turn the construction into an instance where the SDP relaxation of non-uniform sparsest cut with triangle inequalities has integrality gap $(\log\log n)^{1/6 - \varepsilon}$. A negative type metric, which is what that SDP produces, therefore cannot always embed into $\ell_1$ with constant distortion, which disproved the conjecture of Goemans and Linial.
- **Balanced separator.** Khot and Vishnoi prove UG-hardness within any constant factor for balanced separator as well.

## Tightness

**Uniform demands.** For uniform sparsest cut, Arora, Rao and Vazirani give an $O(\sqrt{\log n})$-approximation, and the theorem does not apply, because the reduction needs the antipodal demand pairs. No constant-factor UG-hardness is known for the uniform version.

**The factor.** For constant parameters the reduction gives only constant hardness. Corollary 1.4 of CKKRS gives $\Omega(\sqrt{\log\log n})$ from a stronger conjecture, which is still far below the upper bound $O(\sqrt{\log n}\,\log\log n)$.

**The cube is the right gadget.** In the cube $\{0,1\}^m$ with antipodal demands, every cut has sparsity at least $1$, and coordinate cuts have sparsity exactly $1$. Trying all cuts of the cubes with $m = 2, 3, 4$ gives a minimum sparsity of exactly $1$, reached by the coordinate cut. So on one cube the coordinate cuts are optimal and the completeness case loses nothing. The soundness proof needs more: cuts of nearly optimal cost are close to functions of few coordinates.

## History

Arora, Rao and Vazirani improved the uniform case to $O(\sqrt{\log n})$ in 2004, and Arora, Lee and Naor gave $O(\sqrt{\log k}\,\log\log k)$ for the non-uniform case in 2005. In 2005 CKKRS (CCC) and Khot and Vishnoi (FOCS) proved UG-hardness within every constant independently, with CKKRS getting a slightly stronger quantitative bound. Khot and Vishnoi's integrality gap answered the Goemans-Linial question.

## References
