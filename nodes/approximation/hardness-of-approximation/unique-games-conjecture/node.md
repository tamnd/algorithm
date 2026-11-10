---
tag: R0SJ0F
kind: concept
slug: unique-games-conjecture
name: Unique Games Conjecture
aliases:
- UGC
- Khot's conjecture
- unique label cover conjecture
area: approximation/hardness-of-approximation
level: research
summary: Khot's conjecture that for unique games, constraint systems in which each label of one endpoint fixes the label of the other, telling value at least 1 - ε from value at most δ is NP-hard.
prereqs: [two-prover-one-round-game, label-cover, np-hard]
see_also: [max-cut-ugc-hardness, raghavendra-theorem, unique-games-subexponential-algorithm, sparsest-cut-ugc-hardness, approximation-resistance, dictatorship-test, vertex-cover-inapproximability, maximum-cut]
sources:
  - paper: "Subhash Khot, On the power of unique 2-prover 1-round games, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC), 2002"
    locator: the statement of the Unique Games Conjecture and its first consequences
  - paper: doi:10.4007/annals.2023.198.1.1
    title: Subhash Khot, Dor Minzer and Muli Safra, Pseudorandom sets in Grassmann graph have near-perfect expansion, Annals of Mathematics 198(1), 1 to 92, 2023 (FOCS 2018)
    locator: the proof of the 2-to-2 games theorem with imperfect completeness, completing the work of Khot, Minzer and Safra (STOC 2017) and Dinur, Khot, Kindler, Minzer and Safra (STOC 2018)
  - paper: doi:10.1137/S0097539705447372
    title: Subhash Khot, Guy Kindler, Elchanan Mossel and Ryan O'Donnell, Optimal inapproximability results for MAX-CUT and other 2-variable CSPs?, SIAM Journal on Computing 37(1), 319 to 357, 2007
    locator: the UG-hardness of max cut and the form of the conjecture for linear equations modulo q
  - paper: "Subhash Khot and Oded Regev, Vertex cover might be hard to approximate to within 2 - epsilon, Journal of Computer and System Sciences 74(3), 335 to 349, 2008"
    locator: UG-hardness of vertex cover within 2 - epsilon
  - paper: "Moses Charikar, Konstantin Makarychev and Yury Makarychev, Near-optimal algorithms for unique games, Proceedings of the 38th ACM Symposium on Theory of Computing (STOC), 2006"
    locator: the SDP algorithm that satisfies a 1 - O(sqrt(epsilon log k)) fraction of the constraints
  - book: isbn:9781107038325
    title: Ryan O'Donnell, Analysis of Boolean Functions, Cambridge University Press, 2014
    locator: Section 7.4 (the Unique Games Conjecture and UG-hardness from dictator tests) and Section 11.7 (UG-hardness of max cut)
---

The Unique Games Conjecture (UGC) of Subhash Khot (2002) states that for every $\varepsilon, \delta > 0$ there is a number of labels $k$ such that, given a unique game on $k$ labels, it is [NP-hard](/np-hard/) to tell whether its value is at least $1 - \varepsilon$ or at most $\delta$. A *unique game* is a [two-prover one-round game](/two-prover-one-round-game/), or a [label cover](/label-cover/) instance, in which each constraint is a bijection between the labels of its two endpoints. The conjecture is open. If it holds, then many simple algorithms are optimal: the [Goemans-Williamson](/maximum-cut/) algorithm for max cut, the factor $2$ for [vertex cover](/vertex-cover-inapproximability/), and the basic [semidefinite program](/semidefinite-programming/) for every constraint satisfaction problem.

## In plain words

Picture a network of locks, where each lock has the same number of positions. Each wire between two locks says: if this lock is in position one, the other must be in position five, and so on, so each position on one side forces exactly one position on the other. If all wires can be satisfied at once, that is easy to find: set one lock and follow the wires. The conjecture says that a small step away from that makes the problem very hard. If someone promises that almost all wires can be satisfied, it is still hard to find a setting that satisfies even a small part of them. Many hardness results for approximation start from this one guess, and they say that well-known simple methods cannot be improved.

## The idea

**Unique games.** An instance $\mathcal{U} = (G, k, \{\pi_e\})$ has a graph $G = (V, E)$ (often bipartite, with a distribution on the edges), a label set $[k]$, and for each edge $e = (u, v)$ a bijection $\pi_e : [k] \to [k]$. A labeling $\ell : V \to [k]$ satisfies $e$ if $\pi_e(\ell(u)) = \ell(v)$. The value $\operatorname{val}(\mathcal{U})$ is the largest fraction of edges that a labeling satisfies. The main special case is Max-2LIN($k$): each constraint has the form $x_u - x_v = c_e \pmod k$.

**The conjecture (Khot 2002).** For every $\varepsilon, \delta > 0$ there is $k = k(\varepsilon, \delta)$ such that it is NP-hard to decide, for a unique game $\mathcal{U}$ with label set $[k]$, whether $\operatorname{val}(\mathcal{U}) \ge 1 - \varepsilon$ or $\operatorname{val}(\mathcal{U}) \le \delta$. "UG-hard" means NP-hard if the UGC holds.

**Why not completeness $1$.** For unique games, deciding whether the value is exactly $1$ takes polynomial time. *Proof.* Treat each connected component separately. Fix a vertex $r$ and try each of the $k$ labels for it. A label at $u$ forces the label $\pi_e(\ell(u))$ at each neighbor $v$ across an edge $e = (u, v)$, and the inverse bijection forces labels in the other direction. Propagate by a graph search. If the search meets an edge whose two forced labels disagree, this choice at $r$ fails. Every labeling of value $1$ on the component agrees with the propagation from its own label at $r$, so value $1$ exists exactly when one of the $k$ tries succeeds. The time is $O(k(|V| + |E|))$. $\square$ So the conjecture must have completeness $1 - \varepsilon$, and this is the main difference from [label cover](/label-cover/), where value $1$ versus $\delta$ is NP-hard by the [PCP theorem](/pcp-theorem/) and [parallel repetition](/parallel-repetition-theorem/).

**How hardness follows.** A [dictatorship test](/dictatorship-test/) with completeness $c$ and soundness $s$ that uses a predicate $P$ becomes, by composing with a unique game and the [long code](/long-code/), a proof that Max-CSP($P$) is UG-hard to approximate within $s/c + \varepsilon$ (O'Donnell, Theorem 7.40). The bijective constraints are what make the composition work with $2$ queries: a dictator at $u$ can be compared with a dictator at $v$ after the coordinates are permuted by $\pi_e$. On this site a maximization ratio means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$.

**Evidence for the conjecture.** The strongest evidence is the *2-to-2 theorem* of Khot, Minzer and Safra (2018), built on joint work with Dinur and Kindler: for 2-to-2 games, in which each label of one endpoint allows exactly two labels of the other, telling value at least $1 - \varepsilon$ from value at most $\delta$ is NP-hard. As a consequence, for unique games it is NP-hard to find a labeling that satisfies an $\varepsilon$ fraction of the constraints, even when a $\tfrac12 - \varepsilon$ fraction can be satisfied. This is the conjecture with completeness about $\tfrac12$ instead of $1 - \varepsilon$. It also gives NP-hardness of vertex cover within $\sqrt{2} - \varepsilon$ without any conjecture.

**Evidence that the conjecture is delicate.** Charikar, Makarychev and Makarychev (2006) give a semidefinite programming algorithm that, on a unique game of value $1 - \varepsilon$ with $k$ labels, satisfies a $1 - O(\sqrt{\varepsilon \log k})$ fraction of the constraints. So the conjecture needs $k$ to grow at least exponentially in $1/\varepsilon$. The [subexponential algorithm](/unique-games-subexponential-algorithm/) of Arora, Barak and Steurer solves the gap problem in time $\exp(k n^{\varepsilon^{c}})$, so a reduction from 3SAT to unique games, if one exists, must produce instances of size at least $n^{1/\varepsilon^{c'}}$ under the exponential time hypothesis.

## Examples

All values below are of Max-2LIN($k$) instances on small graphs, with constraints written as $(u, v, c)$ for $x_u - x_v \equiv c \pmod k$. The values are found by trying all labelings.

| Instance | Constraints | Value | Value 1 by propagation? |
|---|---|---|---|
| triangle, $k = 3$ | $(0,1,0), (1,2,0), (0,2,1)$ | $2/3$ | no |
| 5-cycle, $k = 2$ | $(i, i+1 \bmod 5, 1)$ for $i = 0, \ldots, 4$ | $4/5$ | no |
| 4-cycle, $k = 3$ | $(0,1,1), (1,2,2), (2,3,0), (3,0,0)$ | $1$ | yes, $x = (0, 2, 0, 0)$ |
| $K_4$, $k = 3$ | $(u, v, uv \bmod 3)$ for $u < v$ | $5/6$ | no |

**The triangle.** Going around the cycle, the constraints force $x_0 - x_1 = 0$, $x_1 - x_2 = 0$ and $x_0 - x_2 = 1$. The sum of the first two contradicts the third, so at most $2$ of the $3$ hold, and $x = (0,0,0)$ satisfies two. In general, a cycle of Max-2LIN constraints is satisfiable exactly when the constants add up to $0$ around it, where a constant changes sign when its edge points against the direction of travel.

**Max cut is a unique game.** The 5-cycle with all constants $1$ modulo $2$ asks that adjacent vertices get different bits, which is [max cut](/maximum-cut/) on $C_5$, with value $4/5$. Every max cut instance is a Max-2LIN($2$) instance in this way, which is why the [UG-hardness of max cut](/max-cut-ugc-hardness/) starts from unique games.

**A non-example.** The clause-variable game of a 3CNF formula is a projection game but not a unique game: an assignment to a clause fixes the value of each of its variables, but a value of a variable allows several assignments to the clause. Label cover with value $1$ versus $\delta$ is NP-hard, but such games are not unique.

**The CHSH and odd cycle games.** Both [games](/two-prover-one-round-game/) are unique games with $k = 2$: the answer of one prover and the questions determine the only accepted answer of the other.

## Where it is used

Each result below assumes the UGC and is stated as UG-hardness.

- **Max cut.** Khot, Kindler, Mossel and O'Donnell, with the Majority Is Stablest theorem of Mossel, O'Donnell and Oleszkiewicz, prove that approximating [max cut](/max-cut-ugc-hardness/) within $\alpha_{\mathrm{GW}} + \varepsilon \approx 0.87856 + \varepsilon$ is UG-hard, so the Goemans-Williamson algorithm is optimal.
- **Vertex cover.** Khot and Regev prove that approximating [vertex cover](/vertex-cover-inapproximability/) within $2 - \varepsilon$ is UG-hard.
- **Every CSP.** [Raghavendra's theorem](/raghavendra-theorem/) says that for every Max-CSP the basic SDP relaxation gives the best approximation ratio that any polynomial-time algorithm can reach.
- **Cut problems.** Approximating [sparsest cut and multicut](/sparsest-cut-ugc-hardness/) within any constant factor is UG-hard.
- **Resistance.** Predicates that support a pairwise independent distribution are [approximation resistant](/approximation-resistance/).

## References
