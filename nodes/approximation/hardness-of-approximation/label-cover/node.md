---
tag: N3TWC8
kind: problem
slug: label-cover
name: Label Cover
aliases:
- Gap Label Cover
- Max Label Cover
- projection game
- label cover with projection constraints
area: approximation/hardness-of-approximation
level: advanced
summary: Label the vertices of a bipartite graph so that each edge's projection constraint holds. For each s > 0, telling value 1 from value at most s is NP-hard, so it starts many gap reductions.
prereqs: [gap-problem, pcp-theorem, two-prover-one-round-game, max-3sat-inapproximability]
see_also: [parallel-repetition-theorem, unique-games-conjecture, hastad-3bit-pcp, long-code, set-cover-inapproximability, nearest-codeword-inapproximability, gap-eth, gap-preserving-reduction]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 22, Sections 22.1 and 22.2 (two-prover games, parallel repetition and Håstad's 3-bit PCP)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 29 (hardness of approximation, label cover and set cover)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 16 (techniques in proving the hardness of approximation, label cover)
  - paper: doi:10.1006/jcss.1997.1472
    title: S. Arora, L. Babai, J. Stern and Z. Sweedyk, The hardness of approximate optima in lattices, codes, and systems of linear equations, Journal of Computer and System Sciences 54(2), 1997
    locator: the definition of label cover and its minimization form
  - paper: doi:10.1137/S0097539795280895
    title: Ran Raz, A parallel repetition theorem, SIAM Journal on Computing 27(3), 1998
    locator: the main theorem
  - paper: doi:10.1145/278298.278306
    title: S. Arora, C. Lund, R. Motwani, M. Sudan and M. Szegedy, Proof verification and the hardness of approximation problems, Journal of the ACM 45(3), 1998
    locator: the PCP theorem and the gap for Max-3SAT
  - paper: doi:10.1145/2591796.2591884
    title: Irit Dinur and David Steurer, Analytical approach to parallel repetition, STOC 2014
    locator: the bound for repeated projection games
  - paper: doi:10.1145/1754399.1754402
    title: Dana Moshkovitz and Ran Raz, Two-query PCP with subconstant error, Journal of the ACM 57(5), 2010
    locator: label cover with sub-constant soundness and near-linear size
---

Label cover is a constraint problem on a bipartite graph. Each vertex gets a label from a finite set, and each edge says which label on its right end the label on its left end requires. The value of an instance is the largest fraction of edges that a labeling can satisfy. By the [PCP theorem](/pcp-theorem/) and the [parallel repetition theorem](/parallel-repetition-theorem/), for each constant $s > 0$ it is NP-hard to tell instances of value 1 from instances of value at most $s$. This strong gap, with the *projection property* of the constraints, makes label cover the usual starting point for reductions that prove optimal hardness results, for example for [set cover](/set-cover-inapproximability/) and for [Max-3SAT](/max-3sat-inapproximability/). The same object is a [two-prover one-round game](/two-prover-one-round-game/) with projection constraints.

## In plain words

You have two kinds of boxes, left and right, and lines between some left and right boxes. You write one word in each box. Each line has a rule: for each word in its left box, the rule names the one word that must be in its right box. You want a choice of words that obeys as many rules as possible.

For some instances all rules can be obeyed. For others, every choice breaks almost all of them. The hard fact is that no fast method can always tell these two cases apart, even when "almost all" means 99 percent or more. Many hardness proofs start here: they turn the words into a code and the rules into simple tests on the code.

## Definition

**Instance.** A label cover instance $\mathcal{L} = (U, W, E, \Sigma_U, \Sigma_W, \{\pi_e\})$ has:

- a bipartite graph with left vertices $U$, right vertices $W$ and edges $E \subseteq U \times W$, possibly with repeated edges;
- a left alphabet $\Sigma_U$ and a right alphabet $\Sigma_W$, with $|\Sigma_U| \ge |\Sigma_W|$;
- for each edge $e = (u, w)$ a map $\pi_e : \Sigma_U \to \Sigma_W$, the *projection* of $e$.

**Labeling and value.** A labeling is a pair of maps $\ell_U : U \to \Sigma_U$ and $\ell_W : W \to \Sigma_W$. It satisfies the edge $e = (u, w)$ when $\pi_e(\ell_U(u)) = \ell_W(w)$. The value is

$$\mathrm{val}(\mathcal{L}) = \max_{\ell_U, \ell_W} \frac{|\{e \in E : \pi_e(\ell_U(u)) = \ell_W(w)\}|}{|E|}.$$

Max label cover asks for $\mathrm{val}(\mathcal{L})$, a maximization problem. A ratio $\alpha \le 1$ means a labeling that satisfies at least $\alpha \cdot \mathrm{val}(\mathcal{L}) \cdot |E|$ edges.

**Gap version.** For $0 < s < 1$, $\mathrm{GapLC}_{1, s}$ is the promise problem: given $\mathcal{L}$ with $\mathrm{val}(\mathcal{L}) = 1$ or $\mathrm{val}(\mathcal{L}) \le s$, decide which. The number $s$ is the *soundness*, and $|\Sigma_U|$ is the *alphabet size*.

**The projection property.** Each constraint is a function from left labels to right labels. So for each left label exactly one right label satisfies the edge. This is what the reductions use: a left label "decodes" to a unique right label, and a proof that many edges are satisfied can be turned into an explicit labeling.

**Size.** The instance size is about $|E| \cdot |\Sigma_U|$, the size of the tables of all $\pi_e$.

## Variants

- **Min-rep, or the minimization form.** Each vertex gets a *set* of labels, each edge must contain a pair $(a, b)$ with $\pi_e(a) = b$, and the goal is to minimize the total number of labels. This is the form of Arora, Babai, Stern and Sweedyk (1997); it starts the reductions for [nearest codeword](/nearest-codeword-inapproximability/) and lattice problems.
- **Unique games.** The maps $\pi_e$ are bijections. Then deciding $\mathrm{val} = 1$ is easy, by fixing one label and propagating it, and the [unique games conjecture](/unique-games-conjecture/) states that telling $1 - \varepsilon$ from $\varepsilon$ is hard.
- **$d$-to-1 games.** Each right label has exactly $d$ preimages under each $\pi_e$. Khot's 2-to-1 conjecture is about $d = 2$.
- **Smooth and multi-layered label cover.** Versions with extra structure used for hypergraph coloring and hypergraph vertex cover (Khot 2002; Dinur, Guruswami, Khot and Regev 2003).
- **General 2-CSP.** The constraint on an edge is any relation $R_e \subseteq \Sigma_U \times \Sigma_W$, not a function. This is the general two-prover game.

## Examples

**The clause-variable game.** Let $\varphi$ be a 3-CNF formula with clauses $C_1, \ldots, C_m$ on the variables $x_1, \ldots, x_n$, each clause with three literals on distinct variables. The left vertices are the clauses, the right vertices are the variables, and each clause has an edge to each of its three variables, so $|E| = 3m$. A left label is one of the 7 assignments to the clause's variables that satisfy it, a right label is a bit, and $\pi_e$ maps a clause assignment to the bit of that variable. Then

$$\mathrm{val} = 1 - \frac{1 - \mathrm{sat}(\varphi)}{3},$$

where $\mathrm{sat}(\varphi)$ is the largest fraction of clauses that one assignment satisfies.

*Proof.* The right labels form an assignment $x$. If $x$ satisfies $C_j$, the restriction of $x$ to $C_j$ is a left label that satisfies all 3 edges of $C_j$. If $x$ does not satisfy $C_j$, every left label of $C_j$ is a satisfying assignment, so it differs from $x$ in at least one variable, and at most 2 edges of $C_j$ hold. Two are reached: flip one variable of $C_j$ in $x$, which makes one literal true. So the best labeling with right labels $x$ satisfies $3 \cdot \mathrm{sat}_x + 2 (m - \mathrm{sat}_x)$ edges, where $\mathrm{sat}_x$ counts the clauses $x$ satisfies. Maximize over $x$ and divide by $3m$. $\blacksquare$

The formula with all 8 clauses on $x_1, x_2, x_3$ has $\mathrm{sat} = \frac78$, so its game has 8 left vertices, 3 right vertices, 24 edges and value $\frac{23}{24}$. The formula $(x_1 \lor x_2 \lor x_3) \land (\lnot x_1 \lor x_2 \lor \lnot x_3) \land (\lnot x_2 \lor x_3 \lor x_4)$ is satisfiable, so its game has value 1.

**Parallel repetition.** The $k$-fold repetition $\mathcal{L}^{\otimes k}$ has left vertices $U^k$, right vertices $W^k$, edges $E^k$, alphabets $\Sigma_U^k$ and $\Sigma_W^k$, and the projection that acts in each coordinate. A labeling of $\mathcal{L}$ used in each coordinate gives $\mathrm{val}(\mathcal{L}^{\otimes k}) \ge \mathrm{val}(\mathcal{L})^k$, and in particular value 1 stays 1. Each labeling of $\mathcal{L}^{\otimes k}$ restricted to the first coordinate, for fixed other coordinates, gives $\mathrm{val}(\mathcal{L}^{\otimes k}) \le \mathrm{val}(\mathcal{L})$. The value does not always equal $\mathrm{val}^k$, because the provers can correlate their answers across coordinates; the content of the theorem is that it still falls at an exponential rate.

## Known algorithms

| algorithm | guarantee | time |
|---|---|---|
| Exact, all right labelings | the value | $O(|\Sigma_W|^{|W|} \cdot |E| \cdot |\Sigma_U|)$ |
| Majority labeling | satisfies at least $|E| / |\Sigma_W|$ edges | $O(|E|)$ |
| Unique games, propagation | decides $\mathrm{val} = 1$ | $O(|E| \cdot |\Sigma_U|)$ |
| Unique games, SDP (Charikar, Makarychev and Makarychev 2006) | value $1 - O(\sqrt{\varepsilon \log |\Sigma|})$ on value $1 - \varepsilon$ | polynomial |

*Exact search.* Once the right labels are fixed, the left vertices do not interact, so each takes the label that satisfies most of its edges.

*Majority labeling.* Give every left vertex any label. Each edge at $w$ then names one right label for $w$; give $w$ the label named most often. At least a $1/|\Sigma_W|$ fraction of the edges at $w$ name it. Summing over $w$ gives at least $|E|/|\Sigma_W|$ satisfied edges. So $\mathrm{val} \ge 1/|\Sigma_W|$ always, and a gap $\mathrm{GapLC}_{1, s}$ can be hard only if $|\Sigma_W| \ge 1/s$.

## Bounds

- **NP-hardness of the exact problem.** By the clause-variable game, deciding $\mathrm{val} = 1$ is as hard as 3-SAT.
- **Constant gap.** The [PCP theorem](/pcp-theorem/) (Arora, Lund, Motwani, Sudan and Szegedy 1998) gives $\varepsilon > 0$ such that, for 3-CNF formulas with distinct variables in each clause, telling $\mathrm{sat} = 1$ from $\mathrm{sat} \le 1 - \varepsilon$ is NP-hard. By the identity above, $\mathrm{GapLC}_{1, 1 - \varepsilon/3}$ with $|\Sigma_U| = 7$ and $|\Sigma_W| = 2$ is NP-hard. This step is proved in full above.
- **Any constant soundness (cited).** Raz (1998) proved: if $\mathrm{val}(\mathcal{L}) \le 1 - \delta$, then $\mathrm{val}(\mathcal{L}^{\otimes k}) \le (1 - \delta^{c})^{\Omega(k / \log |\Sigma_U|)}$ for a universal constant $c$. For the clause-variable game, $k = O(\log(1/s))$ repetitions give soundness $s$, with alphabet sizes $7^k$ and $2^k$, both $\mathrm{poly}(1/s)$, and instance size $(3m)^k \cdot 7^k$, polynomial for constant $k$. So for each constant $s > 0$, $\mathrm{GapLC}_{1, s}$ is NP-hard with alphabet size $\mathrm{poly}(1/s)$. Dinur and Steurer (2014) give, for projection games, the explicit bound $\mathrm{val}(\mathcal{L}^{\otimes k}) \le \left(\frac{2\sqrt{v}}{1 + v}\right)^{k/2}$ with $v = \mathrm{val}(\mathcal{L})$.
- **Sub-constant soundness.** With $k = \Theta(\log \log n)$ repetitions the soundness is $1/\mathrm{polylog}(n)$ and the size is $n^{O(\log \log n)}$, which is why some hardness results assume NP $\not\subseteq$ DTIME$(n^{O(\log \log n)})$. Moshkovitz and Raz (2010) gave sub-constant soundness with size $n^{1 + o(1)}$ by a different construction. The *sliding scale conjecture* asks for soundness $1/\mathrm{poly}(n)$ with polynomial alphabet; it is open.
- **Under Gap-ETH.** The clause-variable map has linear size, so [Gap-ETH](/gap-eth/) for 3-SAT gives a constant-gap label cover that has no $2^{o(n)}$ algorithm.

## Reductions

- **From 3-SAT.** The clause-variable game above. Each variable appearing in a bounded number of clauses gives a biregular graph, which some later steps need.
- **To set cover.** Each edge becomes a block of elements, each pair (vertex, label) becomes a set, and a partition system on each block makes the cost of a cover track the number of satisfied edges; see [set cover inapproximability](/set-cover-inapproximability/).
- **To Max-3LIN and Max-3SAT.** Each label is encoded by its [long code](/long-code/), and the verifier tests one edge with three bits; see [Håstad's 3-bit PCP](/hastad-3bit-pcp/). The projection property is used in the decoding step.
- **To nearest codeword and lattice problems.** The minimization form starts the reductions of Arora, Babai, Stern and Sweedyk; see [nearest codeword inapproximability](/nearest-codeword-inapproximability/).
- **To unique games.** Unique games are the special case with bijective projections, and the conjecture says that they keep a gap, with imperfect completeness.

## Applications

- The tight hardness of [set cover](/set-cover-inapproximability/) and [max coverage](/max-coverage-inapproximability/), $\ln n$ and $1 - 1/e$.
- The optimal inapproximability of [Max-3SAT](/max-3sat-inapproximability/) and Max-3LIN, $\frac78$ and $\frac12$.
- Hardness for [clique](/clique-inapproximability/) and chromatic number through PCPs with many queries, and for [nearest codeword](/nearest-codeword-inapproximability/), closest vector and directed Steiner problems through the minimization form.
- [Parameterized inapproximability](/parameterized-inapproximability/): under Gap-ETH, label cover instances with $k$ left vertices and large alphabets have no $f(k) \cdot n^{o(k)}$ algorithm that approximates well.

## References
