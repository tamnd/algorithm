---
tag: WXRBXA
kind: definition
slug: ptas-reduction
name: PTAS-reduction
aliases:
- PTAS reduction
area: approximation/hardness-of-approximation
level: advanced
summary: A reduction between NPO problems whose maps may depend on the target ratio r, with a function c such that ratio c(r) in the target gives ratio r in the source. It preserves PTAS.
prereqs: [approximation-preserving-reduction]
see_also: [l-reduction, apx-completeness, apx-class, ptas, npo-class, max-sat, vertex-cover, maximum-independent-set]
sources:
  - paper: doi:10.1007/s002249910001
    title: Pierluigi Crescenzi and Luca Trevisan, On approximation scheme preserving reducibility and its applications, Theory of Computing Systems 33(1), 2000 (conference version FSTTCS 1994)
    locator: The definition of the PTAS-reduction and the result that the closure of APX-PB under it is APX
  - paper: doi:10.1137/S0097539796304220
    title: Pierluigi Crescenzi, Viggo Kann, Riccardo Silvestri and Luca Trevisan, Structure in approximation classes, SIAM Journal on Computing 28(5), 1999
    locator: The definitions of the PTAS-reduction and the AP-reduction and the comparison with the L-reduction
  - paper: doi:10.1137/S0097539795286612
    title: Sanjeev Khanna, Rajeev Motwani, Madhu Sudan and Umesh Vazirani, On syntactic versus computational views of approximability, SIAM Journal on Computing 28(1), 1998
    locator: Remark 5 (with the PTAS-reductions of Crescenzi and Trevisan, the closure of MAX SNP is APX)
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 8, Approximation Preserving Reductions
---

A **PTAS-reduction** from an optimization problem $A$ to an optimization problem $B$ is a reduction whose instance map and solution map may both depend on the target ratio $r$, together with a function $c$ such that any solution of the new instance with ratio $c(r)$ maps back to a solution of the old instance with ratio $r$. Crescenzi and Trevisan (1994) defined it, and Crescenzi, Kann, Silvestri and Trevisan (1999) use it next to the AP-reduction. It is weaker than the [L-reduction](/l-reduction/), which is a special case with a fixed map and a linear $c$, but it still carries a PTAS from $B$ back to $A$. That makes it the standard reduction for [APX-completeness](/apx-completeness/).

## Definition

**Notation.** $A$ and $B$ are [NPO](/npo-class/) problems. For an instance $x$ and a feasible solution $y$, $m(x, y)$ is the measure and $R(x, y) = \max(m(x, y)/\mathrm{OPT}(x),\ \mathrm{OPT}(x)/m(x, y)) \ge 1$ is the performance ratio of Ausiello et al. On this site a minimization $\rho$-approximation has $\mathrm{ALG} \le \rho\,\mathrm{OPT}$ with $\rho \ge 1$, and a maximization $\alpha$-approximation has $\mathrm{ALG} \ge \alpha\,\mathrm{OPT}$ with $\alpha \le 1$; so $R \le r$ means $\rho \le r$ or $\alpha \ge 1/r$.

**PTAS-reduction.** $A \le_{PTAS} B$ if there are maps $f$, $g$ and a function $c : (1, \infty) \cap \mathbb{Q} \to (1, \infty) \cap \mathbb{Q}$ such that:

1. for each instance $x$ of $A$ and each rational $r > 1$, $f(x, r)$ is an instance of $B$, and for each fixed $r$ it is computable in time polynomial in $|x|$;
2. for each feasible solution $y$ of $f(x, r)$, $g(x, y, r)$ is a feasible solution of $x$, and for each fixed $r$ it is computable in time polynomial in $|x|$ and $|y|$;
3. for each $x$, $r > 1$ and feasible $y$ of $f(x, r)$,
$$R_B(f(x, r), y) \le c(r) \implies R_A(x, g(x, y, r)) \le r.$$

**Theorem 1 (it preserves PTAS).** If $A \le_{PTAS} B$ and $B$ has a PTAS, then $A$ has a PTAS.

*Proof.* Fix $r > 1$. Compute $x' = f(x, r)$, run the scheme of $B$ with ratio $c(r)$ on $x'$ to get $y$, and output $g(x, y, r)$. Each step is polynomial for the fixed $r$, because $c(r)$ is a fixed number. Since $R_B(x', y) \le c(r)$, condition 3 gives $R_A \le r$. $\blacksquare$

**Theorem 2 (composition).** If $A \le_{PTAS} B$ with $(f_1, g_1, c_1)$ and $B \le_{PTAS} C$ with $(f_2, g_2, c_2)$, then $A \le_{PTAS} C$ with

$$f(x, r) = f_2(f_1(x, r),\ c_1(r)), \qquad g(x, z, r) = g_1(x,\ g_2(f_1(x, r), z, c_1(r)),\ r), \qquad c(r) = c_2(c_1(r)).$$

*Proof.* For fixed $r$ the number $c_1(r)$ is fixed, so $f$ and $g$ are polynomial. If $R_C(f(x, r), z) \le c_2(c_1(r))$, the second reduction, used with ratio $c_1(r)$, gives a solution of $f_1(x, r)$ with $R_B \le c_1(r)$, and the first reduction then gives $R_A \le r$. $\blacksquare$

**How it differs from the L-reduction.**

| | L-reduction | PTAS-reduction |
| --- | --- | --- |
| Maps | $f(x)$, $g(x, y)$, one pair for all ratios | $f(x, r)$, $g(x, y, r)$, polynomial for each fixed $r$ |
| Condition | (L1) $\mathrm{OPT}_B \le a\,\mathrm{OPT}_A$ and (L2) error transfer with factor $b$ | only "ratio $c(r)$ in $B$ gives ratio $r$ in $A$" |
| Control of the optimum | (L1) is required | none |
| Preserves PTAS | yes | yes |
| Preserves APX | for minimization $A$ | not in general |
| Relation | each L-reduction is a PTAS-reduction with $c(r) = 1 + (1 - 1/r)/(ab)$ | strictly more general as a definition |

The proof that an L-reduction is a PTAS-reduction is Theorem 3 on the [L-reduction](/l-reduction/) page. Some lists give "L-reduction" as a name of this page; the L-reduction is the special case in the table, not a synonym.

**Why APX is not preserved.** If $(f, g, c)$ is a PTAS-reduction, so is $(f, g, c')$ for any $c' \le c$, because condition 3 only gets weaker in its hypothesis. So one may assume $c(r) < 1.01$ for all $r$. An algorithm for $B$ with ratio 2 then never meets the hypothesis, and the reduction gives no ratio at all for $A$. The [AP-reduction](/approximation-preserving-reduction/) fixes this by asking for $c$ of the form $c(r) = 1 + (r - 1)/\alpha$.

## Examples and non-examples

**Example: weighted MAX SAT to unweighted MAX SAT, by rounding that depends on $r$.** Problem $A$ is MAX SAT with clauses $C_1, \ldots, C_m$, none of them empty, and positive integer weights $w_j$ written in binary. Problem $B$ is MAX SAT where a clause may appear several times and each copy counts 1. Let $W = \max_j w_j$; one literal of the heaviest clause can be made true, so $\mathrm{OPT}_A \ge W$.

Given $r > 1$, let $\eta = 1 - 1/\sqrt{r}$ and $u = \eta W / m$. The map $f(x, r)$ takes $k_j = \lfloor w_j / u \rfloor$ copies of $C_j$; each $k_j \le m/\eta$, so the new instance has at most $m^2/\eta$ clauses, a polynomial for fixed $r$. The map $g$ keeps the assignment. For an assignment $\tau$ let $S(\tau)$ be its weight in $A$ and $S'(\tau)$ its count in $B$. Since $u k_j \le w_j < u(k_j + 1)$,

$$u\,S'(\tau) \le S(\tau) \le u\,S'(\tau) + m u = u\,S'(\tau) + \eta W.$$

So $u\,\mathrm{OPT}_B \ge \mathrm{OPT}_A - \eta W \ge (1 - \eta)\,\mathrm{OPT}_A$. Let $c(r) = \sqrt{r}$. If $S'(\tau) \ge \mathrm{OPT}_B / \sqrt{r}$, then

$$S(\tau) \ge u\,S'(\tau) \ge \frac{u\,\mathrm{OPT}_B}{\sqrt{r}} \ge \frac{(1 - \eta)\,\mathrm{OPT}_A}{\sqrt{r}} = \frac{\mathrm{OPT}_A}{r},$$

so $R_A \le r$. This is a PTAS-reduction. The instance map depends on $r$ in an essential way: writing $w_j$ in unary for all $r$ at once would take exponential size. It shows that a problem with large weights can reduce to a polynomially bounded one, which is the idea behind the result of Crescenzi and Trevisan that APX is the closure of APX-PB under PTAS-reductions.

**Example: each L-reduction.** MAX 3SAT to maximum independent set with $a = b = 1$, and bounded degree independent set to bounded degree vertex cover with $a = B$, $b = 1$, are PTAS-reductions with $c(r) = 1 + (1 - 1/r)$ and $c(r) = 1 + (1 - 1/r)/B$. See [L-reduction](/l-reduction/).

**Example: the reductions to MAX 3SAT for APX-completeness.** In the proof that MAX 3SAT is [APX-complete](/apx-completeness/), the number of formulas that $f$ builds grows with $1/(r - 1)$. A single map for all $r$ is not available, so the proof needs a PTAS-reduction.

**Non-example: the complement map from independent set to vertex cover.** Take $f(G, r) = G$ and $g(C) = V \setminus C$ on all graphs. In the complete graph $K_n$, $\tau = n - 1$, and the cover $C = V$ has $R_B = n/(n - 1)$. For each fixed $c(r) > 1$, a large $n$ gives $n/(n - 1) \le c(r)$, but $g(C) = \emptyset$ is not a solution with a finite ratio. So no function $c$ works, and this is not a PTAS-reduction. On graphs of bounded degree it is an L-reduction (see [L-reduction](/l-reduction/)), because (L1) excludes $K_n$ with large $n$.

**Non-example: a Karp reduction alone.** A [polynomial-time reduction](/polynomial-time-reduction/) between the decision versions has no solution map $g$. It shows NP-hardness of exact optimization, not of approximation.

## Related definitions

- **[Approximation-preserving reduction](/approximation-preserving-reduction/).** The umbrella page: strict, E-, L-, AP- and PTAS-reductions and what each one preserves.
- **[L-reduction](/l-reduction/).** The special case with fixed maps and two constants; Theorem 3 there converts it into a PTAS-reduction.
- **AP-reduction.** A PTAS-reduction with $c(r) = 1 + (r - 1)/\alpha$; it also preserves APX.
- **[APX-hard](/apx-completeness/).** Defined by PTAS-reductions from each problem of [APX](/apx-class/); a PTAS for an APX-hard problem gives P = NP.
- **[PTAS](/ptas/).** The class that this reduction preserves.

## References
