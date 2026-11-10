---
tag: 5KNTQZ
kind: definition
slug: approximation-preserving-reduction
name: Approximation-preserving reduction
aliases:
- AP-reduction
area: approximation/hardness-of-approximation
level: advanced
summary: A reduction between NPO problems that maps instances forward and solutions back so that good approximations of the target give good ones of the source. Strict, L, E, AP and PTAS kinds.
prereqs: [npo-class, polynomial-time-reduction, approximation-ratio]
see_also: [l-reduction, ptas-reduction, gap-preserving-reduction, apx-class, apx-completeness, levin-reduction, transitivity-of-reductions, gadget-reduction]
sources:
  - paper: doi:10.1137/S0097539796304220
    title: Pierluigi Crescenzi, Viggo Kann, Riccardo Silvestri and Luca Trevisan, Structure in approximation classes, SIAM Journal on Computing 28(5), 1999
    locator: The definition of the AP-reduction and its comparison with the other reductions
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 8, Approximation Preserving Reductions (AP-reductions, their composition, and the classes they preserve)
  - paper: doi:10.1016/0022-0000(91)90023-X
    title: Christos H. Papadimitriou and Mihalis Yannakakis, Optimization, approximation, and complexity classes, Journal of Computer and System Sciences 43(3), 1991
    locator: pp. 425 to 440 (the L-reduction)
  - paper: doi:10.1137/S0097539795286612
    title: Sanjeev Khanna, Rajeev Motwani, Madhu Sudan and Umesh Vazirani, On syntactic versus computational views of approximability, SIAM Journal on Computing 28(1), 1998
    locator: Definition 3 (the E-reduction) and Remark 2 (E-reductions preserve FPTAS)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Section 16.2, Reductions that preserve approximation (Definition 16.4 and Theorems 16.5 and 16.6)
---

An **approximation-preserving reduction** from an optimization problem $A$ to an optimization problem $B$ is a pair of polynomial-time maps, one from instances of $A$ to instances of $B$ and one from solutions of $B$ back to solutions of $A$, with a condition that turns good solutions of $B$ into good solutions of $A$. An ordinary [Karp reduction](/polynomial-time-reduction/) keeps yes and no answers but can destroy the quality of approximate solutions, so hardness of approximation needs this stronger kind. This page is the umbrella definition and compares the main kinds; the [L-reduction](/l-reduction/) and the [PTAS-reduction](/ptas-reduction/) have their own pages. The AP-reduction of Crescenzi, Kann, Silvestri and Trevisan (1999), which carries the alias of this page, is defined in full below.

## Definition

**Setting and notation.** $A$ and $B$ are [NPO](/npo-class/) problems. For an instance $x$ and a feasible solution $y$, $m(x, y)$ is the measure and $\mathrm{OPT}(x)$ the optimum. The performance ratio is $R(x, y) = \max(m(x, y)/\mathrm{OPT}(x),\ \mathrm{OPT}(x)/m(x, y)) \ge 1$, as in Ausiello et al. In the convention of this site, a minimization $\rho$-approximation has $\mathrm{ALG} \le \rho\,\mathrm{OPT}$ with $\rho \ge 1$, and a maximization $\alpha$-approximation has $\mathrm{ALG} \ge \alpha\,\mathrm{OPT}$ with $\alpha \le 1$; then $R \le \rho$ and $R \le 1/\alpha$.

**General form.** A reduction from $A$ to $B$ consists of an instance map $f$ and a solution map $g$, both computable in polynomial time, such that for each instance $x$ of $A$, $f(x)$ is an instance of $B$, and for each feasible solution $y$ of $f(x)$, $g(x, y)$ is a feasible solution of $x$. It is *approximation-preserving* for a class $\mathcal{C}$ (such as APX or PTAS) when it comes with a quality condition that implies: if $B \in \mathcal{C}$, then $A \in \mathcal{C}$. Each kind below fixes the quality condition.

**AP-reduction.** $A \le_{AP} B$ if there are maps $f, g$ and a constant $\alpha \ge 1$ such that:

1. for each $x$ and each rational $r > 1$, $f(x, r)$ is an instance of $B$, computable in time polynomial in $|x|$ for each fixed $r$;
2. for each feasible $y$ of $f(x, r)$, $g(x, y, r)$ is a feasible solution of $x$, computable in time polynomial in $|x|$ and $|y|$ for each fixed $r$;
3. for each $x$, $r > 1$ and $y$,
$$R_B(f(x, r), y) \le r \implies R_A(x, g(x, y, r)) \le 1 + \alpha (r - 1).$$

**Other kinds**, from strongest to weakest condition.

- **Strict reduction** (Orponen and Mannila 1987): $f$ and $g$ do not depend on $r$, and $R_A(x, g(x, y)) \le R_B(f(x), y)$ for each $y$.
- **E-reduction** (Khanna, Motwani, Sudan and Vazirani 1998, Definition 3): with $E(x, y) = R(x, y) - 1$, there are a polynomial $p$ and a constant $\beta$ such that $\mathrm{OPT}_B(f(x)) \le p(|x|)\,\mathrm{OPT}_A(x)$ and $E_A(x, g(x, y)) \le \beta\,E_B(f(x), y)$.
- **L-reduction** (Papadimitriou and Yannakakis 1991): constants $\alpha_L, \beta_L > 0$ with $\mathrm{OPT}_B(f(x)) \le \alpha_L\,\mathrm{OPT}_A(x)$ and $|\mathrm{OPT}_A(x) - m_A(x, g(x, y))| \le \beta_L\,|\mathrm{OPT}_B(f(x)) - m_B(f(x), y)|$. See [L-reduction](/l-reduction/).
- **PTAS-reduction** (Crescenzi and Trevisan 1994): a function $c : (1, \infty) \to (1, \infty)$ with $R_B(f(x, r), y) \le c(r) \implies R_A(x, g(x, y, r)) \le r$. See [PTAS-reduction](/ptas-reduction/).
- **Gap-preserving reduction**: no solution map at all, only a map of instances that keeps a gap in the optimum. It transfers hardness, not algorithms. See [gap-preserving reduction](/gap-preserving-reduction/).

**What each kind preserves.** "Yes" means: if $B$ is in the class and $A \le B$, then $A$ is in the class.

| Kind | FPTAS | PTAS | APX |
| --- | --- | --- | --- |
| Strict | yes | yes | yes |
| E-reduction | yes (KMSV, Remark 2) | yes | yes |
| AP-reduction | not in general | yes | yes |
| L-reduction | not in general | yes | yes if $A$ is a minimization problem |
| PTAS-reduction | not in general | yes | not in general |

**Proposition 1 (AP-reductions preserve APX and PTAS).** Let $A \le_{AP} B$ with constant $\alpha$. *APX:* if $\mathcal{B}$ has ratio $r_B$ for $B$, then $x \mapsto g(x, \mathcal{B}(f(x, r_B)), r_B)$ is polynomial and has ratio at most $1 + \alpha(r_B - 1)$. *PTAS:* to get ratio $1 + \varepsilon$ for $A$, call the scheme of $B$ with $r = 1 + \varepsilon/\alpha$ on $f(x, r)$ and map back with $g$; condition 3 gives $R_A \le 1 + \varepsilon$, and the time is polynomial for each fixed $\varepsilon$. $\blacksquare$

**Proposition 2 (AP-reductions compose).** If $A \le_{AP} B$ with $(f_1, g_1, \alpha_1)$ and $B \le_{AP} C$ with $(f_2, g_2, \alpha_2)$, then $A \le_{AP} C$ with constant $\alpha_1 \alpha_2$.

*Proof.* For $r > 1$ let $r' = 1 + \alpha_2(r - 1)$, and set $f(x, r) = f_2(f_1(x, r'), r)$ and $g(x, z, r) = g_1(x, g_2(f_1(x, r'), z, r), r')$. For fixed $r$ the value $r'$ is fixed, so both maps are polynomial. If $R_C(f(x, r), z) \le r$, then $y = g_2(f_1(x, r'), z, r)$ has $R_B \le 1 + \alpha_2(r - 1) = r'$, so $R_A(x, g_1(x, y, r')) \le 1 + \alpha_1(r' - 1) = 1 + \alpha_1 \alpha_2 (r - 1)$. $\blacksquare$

## Examples and non-examples

**A strict reduction: MAX 3SAT to maximum independent set.** For a formula with clauses $C_1, \ldots, C_m$, $f$ builds a graph with one vertex for each literal occurrence, a triangle (or edge) inside each clause, and an edge between each pair of occurrences of $x_i$ and $\lnot x_i$. An independent set $S$ picks at most one literal per clause and never both $x_i$ and $\lnot x_i$; $g$ sets these literals to true and the other variables to false, which satisfies at least $|S|$ clauses. Conversely, from an assignment one picks one true literal in each satisfied clause. So $\alpha(G) = \mathrm{OPT}$ and $m(g(S)) \ge |S|$, which gives $R_A(g(S)) \le R_B(S)$: a strict reduction. Williamson and Shmoys use it in Theorem 16.8. The code on the [gap-preserving reduction](/gap-preserving-reduction/) page checks it by brute force.

**An L-reduction: bounded degree independent set to vertex cover.** In a graph of maximum degree $B$, $f$ is the identity and $g$ takes complements. It is an L-reduction with constants $(B, 1)$; see [L-reduction](/l-reduction/) for the proof and the brute-force check.

**Non-example: the same complement map in general graphs.** From [vertex cover](/vertex-cover/) to [independent set](/maximum-independent-set/) on all graphs, $f$ is the identity and $g(C) = V \setminus C$. This is an exact reduction: optimal solutions map to optimal solutions, since $\alpha(G) = n - \tau(G)$. It does not preserve approximation. In a perfect matching on $n$ vertices, $\tau = n/2$; the cover $C = V$ has ratio 2, but $g(C) = \emptyset$ has no finite ratio. Vertex cover has a 2-approximation, while independent set has no $n^{-(1 - \varepsilon)}$-approximation unless P = NP (see [clique inapproximability](/clique-inapproximability/)).

**Non-example: a Karp reduction with no solution map.** The standard reduction from [3SAT](/3-sat/) to [3-coloring](/three-coloring/) maps satisfiable formulas to 3-colorable graphs, but a coloring with many colors says nothing useful about a formula. It has no solution map that keeps quality, so it is not approximation-preserving. It still gives a [gap problem](/gap-problem/) for chromatic number (3 versus 4), which is the content of the $4/3$ bound in [graph coloring inapproximability](/graph-coloring-inapproximability/).

## Related definitions

- **[L-reduction](/l-reduction/).** The original linear reduction, with a full proof that it preserves PTAS.
- **[PTAS-reduction](/ptas-reduction/).** The weakest common kind; APX-hardness under it already rules out a PTAS.
- **[Gap-preserving reduction](/gap-preserving-reduction/).** Keeps a gap in the optimum and needs no solution map.
- **[APX-completeness](/apx-completeness/).** Completeness for [APX](/apx-class/) under PTAS-reductions or AP-reductions.
- **[Levin reduction](/levin-reduction/).** A Karp reduction with a map of witnesses back; approximation-preserving reductions add a quality condition on top of it.
- **[Transitivity of reductions](/transitivity-of-reductions/).** Each kind above composes; Proposition 2 is the AP case.

## References
