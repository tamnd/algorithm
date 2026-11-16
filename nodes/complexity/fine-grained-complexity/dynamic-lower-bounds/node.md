---
tag: YW1X2M
kind: concept
slug: dynamic-lower-bounds
name: Dynamic lower bounds
aliases:
- dynamic data structure lower bounds
area: complexity/fine-grained-complexity
level: advanced
summary: "Lower bounds on the update and query time of dynamic algorithms. Proved ones are only polylogarithmic; polynomial ones are conditional, mostly on OMv and SETH."
prereqs: [conditional-lower-bound, dynamic-graph, amortized-update-time]
see_also: [omv-conjecture, online-matrix-vector-multiplication, cell-probe-lower-bound, update-query-tradeoff, dynamic-reachability, decremental-sssp, 3sum-hardness, strong-exponential-time-hypothesis]
sources:
  - paper: arxiv:1511.06773
    title: "Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, STOC 2015, 21-30"
    locator: Section 1.1 and Figure 1, Tables 4 to 6, Lemmas 3.1 and 3.2, Section 4, Section 5.1 (Definition 5.1, Lemma 5.2, Corollary 5.3) and Appendix A of the arXiv version, which the page relies on
  - paper: doi:10.1145/1806689.1806772
    title: "Mihai Pătraşcu, Towards polynomial lower bounds for dynamic problems, STOC 2010"
    locator: the multiphase problem and its reduction from 3SUM, as restated in Section 5.1 of Henzinger et al.
  - paper: doi:10.1109/FOCS.2014.53
    title: "Amir Abboud and Virginia Vassilevska Williams, Popular conjectures imply strong lower bounds for dynamic problems, FOCS 2014"
    locator: the bounds from 3SUM, triangle, combinatorial BMM and SETH, as listed in Tables 5 and 6 and Appendix A of Henzinger et al.
  - paper: doi:10.1137/1.9781611974331.ch89
    title: "Tsvi Kopelowitz, Seth Pettie and Ely Porat, Higher lower bounds from the 3SUM conjecture, SODA 2016"
    locator: the bound for d-failure connectivity, as listed in Table 5 of Henzinger et al.
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Pătraşcu and Erik D. Demaine, Logarithmic lower bounds in the cell-probe model, SIAM Journal on Computing 35(4), 2006, 932-963 (conference version in STOC 2004)"
    locator: the Omega(log n) bounds for dynamic connectivity and partial sums; the page relies on the journal version
  - paper: doi:10.1145/2213977.2213987
    title: "Kasper Green Larsen, The cell probe complexity of dynamic range counting, STOC 2012, 85-94"
    locator: the lower bound for dynamic weighted orthogonal range counting, about log^2 n per query
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the introduction (the 3SUM and APSP hypotheses and three hinted OMv variants are refuted; plain OMv and SETH are not affected; the affected dynamic bounds are at the end of the trade-off curves with the fastest queries); not yet refereed
---

A dynamic lower bound says that no algorithm for a dynamic problem can have both a small update time and a small query time. A dynamic algorithm keeps an object, such as a graph or an array, under changes. It has three costs: preprocessing time, update time and query time. Each may be a worst-case bound for each operation or an amortized bound over a sequence. A lower bound rules out some combination of the three.

There are two kinds. Unconditional bounds are proved in the [cell probe model](/cell-probe-model/), and the best of them are only polylogarithmic per operation. Conditional bounds are polynomial, such as $m^{1/2-\varepsilon}$ per update or $m^{1-\varepsilon}$ per query, and they follow from hypotheses of [fine-grained complexity](/fine-grained-reduction/) by reductions. Since Henzinger, Krinninger, Nanongkai and Saranurak (STOC 2015), most conditional bounds come from the [OMv conjecture](/omv-conjecture/), and the rest from [SETH](/strong-exponential-time-hypothesis/). Many of them are tight: a known algorithm matches them.

## In plain words

Some programs must keep an answer up to date while their data changes, for example "can I still get from A to B in this road map" while roads close and open. Each change costs some work, and each question costs some work.

A lower bound says you cannot make both costs small at once. If changes are cheap, questions must be expensive, and the other way round.

For a few simple problems, this has been proved, but only for small costs. For the large costs that matter in practice, the proofs depend on a bet that some basic problem is hard. If the bet is right, the bound is right. Most of these bets lead back to one problem: answering many grid times list questions one at a time.

## The idea

### Unconditional bounds

In the cell probe model, a data structure is charged only for the memory cells it reads or writes. Bounds in this model hold for every algorithm on the word RAM, with no hypothesis. Pătraşcu and Demaine proved $\Omega(\log n)$ per operation for [dynamic connectivity](/dynamic-connectivity-lower-bound/) and for [partial sums](/dynamic-partial-sums-lower-bound/). Larsen (STOC 2012) proved about $\log^2 n$ per query for dynamic weighted range counting in the plane. No polynomial cell probe bound is known for any natural dynamic problem. See [cell probe lower bounds](/cell-probe-lower-bound/).

So for problems like dynamic reachability, where the best algorithms take polynomial time per operation, all known polynomial lower bounds are conditional.

### How a conditional bound is proved

Take a problem $P$ that is believed to be hard, with a total time bound $T$. Build a dynamic instance from an instance of $P$ by preprocessing, then solve $P$ with $U$ updates and $Q$ queries. If the dynamic algorithm has preprocessing time $p$, update time $u$ and query time $q$, then $P$ takes $p + U u + Q q$ time. If this is $O(T^{1-\varepsilon})$, the hypothesis for $P$ fails. So $u$ and $q$ cannot both be small.

- If the instance of $P$ is solved with a few long sequences of operations, the bound holds for amortized time, but only for fully dynamic algorithms, which can undo changes.
- If each part of $P$ needs only a short sequence on a fresh copy, the bound holds for the worst-case time of partially dynamic algorithms too. Henzinger et al. state their bounds for amortized time of fully dynamic algorithms and for worst-case time of partially dynamic algorithms.

### Hypothesis (OMv)

For every constant $\varepsilon > 0$, no algorithm solves [online matrix-vector multiplication](/online-matrix-vector-multiplication/) on an $n \times n$ Boolean matrix and $n$ vectors in time $O(n^{3-\varepsilon})$ with error probability at most $1/3$. The model is the word RAM with words of $O(\log n)$ bits. The entries are bits. Randomized algorithms with error at most $1/3$ are excluded too. Henzinger et al. show that it also excludes any polynomial preprocessing time.

### Hypothesis (3SUM, APSP, triangle and combinatorial BMM, as used by Abboud and Vassilevska Williams)

Henzinger et al. (Appendix A) restate these from Abboud and Vassilevska Williams (FOCS 2014). All are in the word RAM with words of $O(\log n)$ bits, and all bound the expected time, so they exclude randomized algorithms with expected running time too.

In each item, $\varepsilon > 0$ is any constant.

- **3SUM.** No algorithm decides in expected time $O(n^{2-\varepsilon})$ whether a set of $n$ integers in $\{-n^3, \ldots, n^3\}$ has three distinct elements with $a + b = c$. See [3SUM conjecture](/3sum-conjecture/).
- **APSP.** For some constant $c$, no algorithm computes all-pairs shortest paths on $n$ nodes with weights in $\{1, \ldots, n^c\}$ in expected time $O(n^{3-\varepsilon})$. See [APSP conjecture](/apsp-conjecture/).
- **Triangle.** For some constant $\delta > 0$, no algorithm detects a triangle in a graph with $m$ edges in expected time $O(m^{1+\delta-\varepsilon})$.
- **Combinatorial BMM.** No combinatorial algorithm multiplies two $n \times n$ Boolean matrices in expected time $O(n^{3-\varepsilon})$. "Combinatorial" has no formal definition. See [combinatorial BMM conjecture](/combinatorial-bmm-conjecture/).

### Hypothesis (SETH)

For every $\varepsilon > 0$ there is a $k$ such that no algorithm decides satisfiability of $k$-CNF formulas on $n$ variables in time $O^{*}(2^{(1-\varepsilon) n})$, where $O^{*}$ hides polynomial factors. The usual form excludes randomized algorithms with bounded error too. See [SETH](/strong-exponential-time-hypothesis/).

### The history in four steps

1. **Pătraşcu (STOC 2010)** defined the multiphase problem. In the matrix form of Henzinger et al. (Definition 5.1): phase 1 preprocesses an $n_1 \times n_2$ Boolean matrix $M$ in time $O(n_1 n_2 \tau)$, phase 2 receives a vector $v$ and may spend $O(n_2 \tau)$, and phase 3 receives an index $i$ and must answer $(M v)_i$ in time $O(\tau)$. Pătraşcu showed, conditional on 3SUM, that no algorithm has $\tau = \tilde{o}(\sqrt{n_2})$ when $n_1 = n_2^{2.5}$, and reduced the multiphase problem to many dynamic problems. These bounds are for worst-case time.
2. **Abboud and Vassilevska Williams (FOCS 2014)** proved bounds for many dynamic graph problems from 3SUM, APSP, triangle, combinatorial BMM and SETH. Their SETH bounds already hold with any polynomial preprocessing time.
3. **Kopelowitz, Pettie and Porat (SODA 2016)** proved stronger bounds from 3SUM, for example for $d$-failure connectivity.
4. **Henzinger et al. (STOC 2015)** showed that the OMv conjecture gives, for most bounds of these three papers except the SETH ones, the same or a stronger bound on the amortized time, with any polynomial preprocessing time. Their Figure 1 marks all the earlier bounds from 3SUM as subsumed. They state that OMv and SETH together give all the dynamic bounds known at the time with polynomial preprocessing.

### Status in 2026

Preprints of October 2026 (not yet refereed) give truly subquadratic 3SUM and truly subcubic APSP. Alman and Vassilevska Williams (arXiv:2610.06783) also refute three hinted forms of OMv used by van den Brand, Nanongkai and Saranurak (FOCS 2019), and state that plain OMv, SETH and Orthogonal Vectors are not affected.

- Bounds based only on 3SUM or APSP lose their base. Most of them are subsumed by OMv bounds, which still stand.
- Bounds based on the hinted OMv forms lose their base. The authors write that these are at the end of the update and query trade-off curves with the fastest queries.
- Bounds based on OMv or SETH are unchanged.

### Pitfalls

- State the kind of time. An amortized bound for fully dynamic algorithms says nothing about a partially dynamic algorithm, and the other way round.
- State the preprocessing. Some 3SUM bounds allow only $m^{4/3}$ preprocessing, while OMv bounds allow any polynomial.
- State the range of $m$. Many bounds hold only for $m$ in some range in terms of $n$, for example $m = O(n^2)$.
- A bound from combinatorial BMM holds only for combinatorial algorithms. For $s$-$t$ reachability, Sankowski's algebraic algorithm breaks the combinatorial bound.
- A conditional bound is only as strong as its hypothesis. Check its status, as the 2026 preprints show.

## Examples

**From OuMv to $s$-$t$ shortest paths.** This is Lemma 3.2 of Henzinger et al. Take an $n_1 \times n_2$ Boolean matrix $M$ with $n_1 = n_2 = \sqrt{m}$. Build an undirected graph with nodes $l_1, \ldots, l_{n_1}$, $r_1, \ldots, r_{n_2}$, $s$ and $t$, an edge $l_i r_j$ for each $M_{ij} = 1$, and all edges $t l_i$ and $r_j s$. It has at most $n_1 n_2 + n_1 + n_2 = O(m)$ edges. When a pair $(u, v)$ arrives, delete $t l_i$ for each $u_i = 0$ and $r_j s$ for each $v_j = 0$. Then $u^{T} M v = 1$ exactly when $d(s, t) = 3$, and otherwise $d(s, t) \ge 5$ or there is no path.

With

$$M = \begin{pmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 0 & 1 \\ 1 & 1 & 0 & 0 \end{pmatrix},$$

the graph has $7 + 4 + 4 = 15$ edges. Three rounds:

| $u$ | $v$ | deletions | $d(s, t)$ | $u^{T} M v$ |
|---|---|---|---|---|
| $(0, 1, 0, 0)$ | $(0, 0, 0, 1)$ | 6 | no path | 0 |
| $(0, 0, 1, 0)$ | $(0, 0, 1, 1)$ | 5 | 3, by $t, l_3, r_4, s$ | 1 |
| $(1, 0, 0, 1)$ | $(0, 1, 0, 0)$ | 5 | 3, by $t, l_4, r_2, s$ | 1 |

A fully dynamic algorithm inserts the deleted edges again after each query. So each round costs $O(\sqrt{m})$ updates and one query. If the update time is $m^{1/2-\varepsilon}$ and the query time is $m^{1-\varepsilon}$, then $n_3$ rounds take $O(n_3 m^{1-\varepsilon})$ time, which is $\tilde{o}(n_1 n_2 n_3)$ because $n_1 n_2 = m$. This contradicts the OMv conjecture (Theorem 2.7 of Henzinger et al.). So, conditional on OMv, no fully dynamic algorithm for $s$-$t$ shortest paths has polynomial preprocessing, amortized update time $m^{1/2-\varepsilon}$ and query time $m^{1-\varepsilon}$, for $m = O(n^2)$. The same graph gives the bound for $s$-$t$ reachability and subgraph connectivity (Lemma 3.1, with nodes turned off). The bound is tight: recompute from scratch at each query, or do nothing at each update, which gives $O(1)$ update and $O(m)$ query.

**The same idea with 3 against 5.** Since the distance is 3 or at least 5, an algorithm that only tells 3 from 5 suffices. So the bound holds for $(\alpha, \beta)$-approximate $s$-$t$ distances with $3\alpha + \beta < 5$ (Table 5 of Henzinger et al.).

**A trade-off.** For subgraph connectivity, where nodes are turned on and off and a query asks whether two nodes are connected through nodes that are on, Henzinger et al. show, conditional on OMv, that no algorithm has polynomial preprocessing, amortized update time $m^{\delta-\varepsilon}$ and query time $m^{1-\delta-\varepsilon}$, for any $\delta \in (0, 1)$. Abboud and Vassilevska Williams had shown, conditional on 3SUM, that no algorithm has $m^{4/3}$ preprocessing, update time $m^{\delta-\varepsilon}$ and query time $m^{2/3-\delta-\varepsilon}$, for $\delta \in [1/6, 1/3]$. The OMv bound is stronger and is tight at $\delta = 2/3$, where an algorithm of Chan, Pătraşcu and Roditty has $\tilde{O}(m^{2/3})$ amortized update and $\tilde{O}(m^{1/3})$ query time. See [update and query trade-offs](/update-query-tradeoff/).

**Decremental single-source shortest paths.** The [Even-Shiloach tree](/even-shiloach-tree/) keeps exact distances from a source under edge deletions in $O(m n)$ total time with $O(1)$ query time. Conditional on OMv, no exact algorithm has polynomial preprocessing, total update time $m n^{1-\varepsilon}$ and query time $\tilde{O}(1)$ (Section 4 of Henzinger et al.). Roditty and Zwick had proved the same for combinatorial algorithms, from combinatorial BMM. See [decremental SSSP](/decremental-sssp/).

**Multiphase from OMv.** Henzinger et al. (Lemma 5.2) solve OMv with a multiphase algorithm: run phase 1 once, phase 2 once per vector, and phase 3 once per row of each vector. This takes $O((n_1 n_2 + n_2 n_3 + n_1 n_3)\tau)$ time. With $n_3 = \min\{n_1, n_2\}$, conditional on OMv, no algorithm has $\tau = \tilde{o}(\min\{n_1, n_2\})$ (Corollary 5.3). This is stronger than Pătraşcu's $\sqrt{n_2}$ from 3SUM.

## Where it is used

- **Dynamic graph algorithms.** Lower bounds tell which known algorithms cannot be improved: for [dynamic reachability](/dynamic-reachability/), subgraph connectivity, $s$-$t$ shortest paths, [decremental SSSP](/decremental-sssp/), approximate diameter and densest subgraph, among others. See [dynamic graph](/dynamic-graph/) and [fully dynamic graph](/fully-dynamic-graph/).
- **Data structures.** Bounds for Pagh's problem, Erickson's problem, Langerman's problem and $d$-failure connectivity come from the same hypotheses (Table 6 of Henzinger et al.).
- **Amortized against worst case.** Some bounds hold only for one kind of time; see [amortized update time](/amortized-update-time/) and [worst-case update time](/worst-case-update-time/).
- **Algorithm design.** A bound shows which approach to avoid. Henzinger et al. use the OMv conjecture to show limits of some approaches to dynamic minimum Steiner tree and minimum cut.
- **Testing hypotheses.** The 2026 preprints show that a dynamic bound can fall when its hypothesis falls. Bounds from several hypotheses at once, like OMv and 3SUM for the same problem, are more robust.

## References
