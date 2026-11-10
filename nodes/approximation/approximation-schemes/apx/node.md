---
tag: 6360RN
kind: definition
slug: apx
name: APX (class of constant-factor approximable problems)
aliases:
- APX class
- APX-hard
- constant-factor approximable problems
area: approximation/approximation-schemes
level: advanced
summary: Optimization problems admitting a constant-factor approximation in polynomial time; problems with a PTAS form a subclass PTAS ⊆ APX.
prereqs: [approximation-ratio, ptas, npo-class]
see_also: [apx-class, apx-completeness, ptas-reduction, l-reduction, approximation-threshold, pcp-theorem, general-tsp-inapproximability, ptas]
sources:
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 3 (the classes APX and PTAS, and the gap technique) and Chapter 8 (APX-completeness)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16 (Techniques in proving the hardness of approximation)
  - title: Sartaj Sahni and Teofilo Gonzalez, P-complete approximation problems, Journal of the ACM 23(3), 1976
    locator: the result that general TSP has no constant ratio unless P = NP
  - title: Christos H. Papadimitriou and Mihalis Yannakakis, Optimization, approximation, and complexity classes, Journal of Computer and System Sciences 43(3), 1991
    locator: the class MAX SNP and the L-reduction
---

APX is the class of NP optimization problems that have a polynomial-time approximation algorithm with a constant ratio. Seen from the side of approximation schemes, it is the next class after [PTAS](/ptas/): each problem with a PTAS is in APX, and under P ≠ NP some problems in APX, such as max 3SAT, [vertex cover](/vertex-cover/) and [bin packing](/bin-packing/), have no PTAS. A problem is APX-hard when every problem in APX reduces to it by a [PTAS reduction](/ptas-reduction/). Then a PTAS for it would give a PTAS for all of APX, and by the [PCP theorem](/pcp-theorem/) this implies P = NP. So APX-hardness is the standard proof that a problem has no approximation scheme. The complexity view of the class, with the complete problems and the closure results, is on the [APX class](/apx-class/) page.

## Definition

Let $\Pi$ be an optimization problem in [NPO](/npo-class/). We use the conventions of [the approximation ratio](/approximation-ratio/) page: $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ with $\rho \ge 1$ for minimization and $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $0 < \alpha \le 1$ for maximization.

**APX.** $\Pi$ is in **APX** when there are a constant $\rho \ge 1$ (minimization) or a constant $\alpha > 0$ (maximization) and a polynomial-time algorithm that returns, for each instance $I$, a feasible solution with $\mathrm{ALG}(I) \le \rho \cdot \mathrm{OPT}(I)$, or $\mathrm{ALG}(I) \ge \alpha \cdot \mathrm{OPT}(I)$. The ratio is absolute: it holds on each instance.

**APX-hard and APX-complete.** $\Pi$ is **APX-hard** when each problem in APX has a PTAS reduction to $\Pi$. It is **APX-complete** when it is APX-hard and in APX. A PTAS reduction from $\Pi_1$ to $\Pi_2$ maps instances and solutions so that a $(1 + \delta)$-approximate solution of $\Pi_2$ maps back to a $(1 + \varepsilon)$-approximate solution of $\Pi_1$, with $\delta$ a function of $\varepsilon$. The [L-reduction](/l-reduction/) of Papadimitriou and Yannakakis is a special case that is easy to check, and the details are on the [APX-completeness](/apx-completeness/) page.

**The chain of classes.** For the classes defined by the form of the guarantee,

$$
\mathrm{FPTAS} \subseteq \mathrm{EPTAS} \subseteq \mathrm{PTAS} \subseteq \mathrm{APX} \subseteq \text{log-APX} \subseteq \text{poly-APX} \subseteq \mathrm{NPO},
$$

where log-APX allows a ratio $O(\log n)$ and poly-APX a ratio $n^{O(1)}$. The step $\mathrm{PTAS} \subseteq \mathrm{APX}$ holds because a PTAS run with the fixed value $\varepsilon = 1$ (minimization) or $\varepsilon = 1/2$ (maximization) is a constant-ratio algorithm. Under P ≠ NP each step except EPTAS ⊆ PTAS is strict, and that step is strict under FPT ≠ W[1]. The [PTAS](/ptas/) page has a table of the separating problems.

**Why APX-hard means no PTAS.** The class PTAS is closed under PTAS reductions: if $\Pi_1$ reduces to $\Pi_2$ and $\Pi_2$ has a PTAS, then $\Pi_1$ has one. Max 3SAT is in APX, and by the PCP theorem there is a constant $\delta > 0$ such that no polynomial-time algorithm has ratio $1 - \delta$ for it unless P = NP. So if an APX-hard problem had a PTAS, max 3SAT would have one, and P = NP.

**Notes.**

- **Absolute ratio.** APX uses the absolute ratio. Bin packing is in APX with the absolute ratio 2, and it has no PTAS, but it has an [asymptotic PTAS](/asymptotic-ptas/). The class of problems with an APTAS is not the same as PTAS.
- **The ratio is a constant.** An algorithm with ratio $H_n$, such as [greedy set cover](/greedy-set-cover/), does not put a problem in APX. It puts it in log-APX.
- **The approximation threshold.** For a problem in APX, the [approximation threshold](/approximation-threshold/) is the infimum of the constants $\rho$ that some polynomial-time algorithm reaches. A problem with a PTAS has threshold 1. The converse is not automatic, because a PTAS needs one algorithm that takes $\varepsilon$ as an input.

## Examples and non-examples

**Problems in APX with no PTAS (if P ≠ NP).** Each row gives a constant-ratio algorithm and a hardness result with its assumption. Vertex cover, max 3SAT, max cut and metric TSP are APX-complete.

| problem | ratio in polynomial time | hardness | assumption |
|---|---|---|---|
| [vertex cover](/vertex-cover/) | 2, [maximal matching](/vertex-cover-2-approximation/) | 1.3606 (Dinur and Safra 2005); $\sqrt 2 - \delta$ (Khot, Minzer and Safra 2018) | P ≠ NP |
| | | $2 - \delta$ (Khot and Regev 2008) | the [unique games conjecture](/unique-games-conjecture/) |
| max 3SAT (exactly 3 literals per clause) | $\alpha = 7/8$, a random assignment | $7/8 + \delta$ (Håstad 2001); see [max 3SAT inapproximability](/max-3sat-inapproximability/) | P ≠ NP |
| max cut | $\alpha \approx 0.878$ (Goemans and Williamson 1995) | $16/17 + \delta$ (Håstad 2001) | P ≠ NP |
| | | $0.878 + \delta$; see [max cut UGC hardness](/max-cut-ugc-hardness/) | the unique games conjecture |
| [metric TSP](/metric-tsp/) | $3/2$, [Christofides](/christofides-algorithm/) | $123/122$ (Karpinski, Lampis and Schmied 2015) | P ≠ NP |
| [k-center](/k-center-problem/) | 2, [Gonzalez](/gonzalez-k-center/) | $2 - \delta$ | P ≠ NP |
| makespan on unrelated machines | 2, [Lenstra, Shmoys and Tardos](/lenstra-shmoys-tardos/) | $3/2 - \delta$ | P ≠ NP |

**Bin packing.** [Bin packing](/bin-packing/) is in APX, with ratio 2 for next fit, and no polynomial-time algorithm has a ratio below $3/2$ unless P = NP, by a direct reduction from [partition](/partition-problem/) (proved on the [PTAS](/ptas/) page). This is a gap argument, not a PCP argument: the gap between 2 and 3 bins is built into the problem.

**Problems in PTAS.** The [knapsack problem](/knapsack-problem/) (it has an [FPTAS](/fptas/)), makespan on identical machines (the [Hochbaum and Shmoys PTAS](/hochbaum-shmoys-makespan-ptas/)), [Euclidean TSP](/euclidean-tsp/) (the [Arora PTAS](/arora-euclidean-tsp-ptas/)) and the [multiple knapsack problem](/multiple-knapsack-problem/) are in APX and also in PTAS.

**Non-example: general TSP (the separation APX ⊊ NPO).** For the [traveling salesman problem](/traveling-salesman-problem/) with arbitrary non-negative costs, no polynomial-time algorithm has a constant ratio $\rho$ unless P = NP (Sahni and Gonzalez 1976).

*Proof.* Let $G = (V, E)$ be an instance of the [Hamiltonian cycle](/hamiltonian-cycle/) problem with $n = |V| \ge 3$. Build the complete graph on $V$ with cost 1 on the edges of $E$ and cost $\rho n + 1$ on the other pairs. If $G$ has a Hamiltonian cycle, that cycle is a tour of cost $n$, so $\mathrm{OPT} = n$ and a $\rho$-approximation returns a tour of cost at most $\rho n$. If $G$ has no Hamiltonian cycle, each tour uses a pair outside $E$, so each tour costs at least $(\rho n + 1) + (n - 1) > \rho n$. So the tour that the algorithm returns costs at most $\rho n$ exactly when $G$ is Hamiltonian. The new costs have $O(\log(\rho n))$ bits, so the reduction runs in polynomial time, and the algorithm would decide an NP-complete problem. $\square$

The same proof works for any ratio $\rho(n)$ that is computable in polynomial time and has $\log \rho(n)$ polynomial in $n$, for example $\rho(n) = 2^n$. So general TSP is not even in poly-APX. See [general TSP inapproximability](/general-tsp-inapproximability/).

**Non-example: set cover.** [Set cover](/set-cover/) is in log-APX: [greedy set cover](/greedy-set-cover/) has ratio $H_n \le \ln n + 1$. For each $\delta > 0$, no polynomial-time algorithm has ratio $(1 - \delta) \ln n$ unless P = NP (Dinur and Steurer 2014), so set cover is not in APX. See [set cover inapproximability](/set-cover-inapproximability/).

**Non-example: clique.** Maximum [clique](/clique-problem/) is in poly-APX: the trivial algorithm that returns one vertex has $\alpha = 1/n$. For each $\delta > 0$, no polynomial-time algorithm has $\alpha = n^{-(1 - \delta)}$ unless P = NP (Håstad 1999, Zuckerman 2007). So clique is not in APX, nor in log-APX. See [clique inapproximability](/clique-inapproximability/).

## Related definitions

- **The APX class page.** The [APX class](/apx-class/) page treats APX from the side of complexity: its closure under reductions and its relation to the syntactic class MAX SNP of Papadimitriou and Yannakakis.
- **APX-completeness.** The complete problems and the reductions between them are on the [APX-completeness](/apx-completeness/) page. The main reductions are the [PTAS reduction](/ptas-reduction/) and the [L-reduction](/l-reduction/).
- **NPO.** [NPO](/npo-class/) is the class of all optimization problems whose feasibility and value can be checked in polynomial time. APX is the subclass with a constant ratio.
- **PTAS.** A [PTAS](/ptas/) gives each ratio $1 + \varepsilon$. Under P ≠ NP, $\mathrm{PTAS} \subsetneq \mathrm{APX}$.
- **Approximation threshold.** The [approximation threshold](/approximation-threshold/) of a problem is the best constant ratio for it, and hardness results bound it from below.

## References
