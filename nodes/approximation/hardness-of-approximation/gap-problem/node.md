---
tag: XZDSGQ
kind: definition
slug: gap-problem
name: Gap problem
aliases:
- gap version of a problem
- promise gap problem
area: approximation/hardness-of-approximation
level: advanced
summary: The promise problem gap-Π[c, s] asks whether the optimum is at least c or below s, with no answer required in between. If it is NP-hard, no ratio better than s/c is possible unless P = NP.
prereqs: [npo-class, np-hard]
see_also: [gap-preserving-reduction, gap-amplification, approximation-threshold, pcp-theorem, probabilistically-checkable-proof, max-3sat-inapproximability, label-cover, decision-problem]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 11, PCP Theorem and Hardness of Approximation, Sections 11.2 and 11.3 (gap problems and the equivalence of the two views of the PCP theorem)
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems, PWS Publishing, 1997
    locator: Chapter 10, Sanjeev Arora and Carsten Lund, Hardness of Approximations (gap problems and gap-preserving reductions)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 16, Section 16.3, Reductions from probabilistically checkable proofs (Theorem 16.18 and the gap form of MAX E3SAT)
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 2001
    locator: The NP-hardness of the gap versions of MAX E3SAT and MAX E3LIN2
---

A **gap problem** is the promise version of an optimization problem in which the input is guaranteed to have either a large optimum or a small one, and the task is to tell which. For thresholds $c$ and $s$ it is written gap-$\Pi[c, s]$; instances with an optimum between the two thresholds may get any answer. Gap problems are the link between [probabilistically checkable proofs](/probabilistically-checkable-proof/) and hardness of approximation: if gap-$\Pi[c, s]$ is NP-hard, then no polynomial-time algorithm can approximate $\Pi$ better than the ratio $s/c$ unless P = NP.

## Definition

**Promise problems.** A promise problem is a pair $(\mathrm{YES}, \mathrm{NO})$ of disjoint sets of strings. An algorithm *solves* it if it accepts each string of YES and rejects each string of NO; on other strings its output does not matter. A promise problem is NP-hard if there is a polynomial-time map $h$ from [3SAT](/3-sat/) with $\varphi$ satisfiable $\Rightarrow h(\varphi) \in \mathrm{YES}$ and $\varphi$ unsatisfiable $\Rightarrow h(\varphi) \in \mathrm{NO}$.

**Gap problem, maximization.** Let $\Pi$ be a maximization problem in [NPO](/npo-class/), and let $c, s$ be functions of the instance with $c(x) \ge s(x)$ (often constants times a size parameter). With $c = s$ the promise is empty and the gap problem is the decision problem. Then gap-$\Pi[c, s]$ is the promise problem with

$$\mathrm{YES} = \{x : \mathrm{OPT}(x) \ge c(x)\}, \qquad \mathrm{NO} = \{x : \mathrm{OPT}(x) < s(x)\}.$$

$c$ is the *completeness* and $s$ the *soundness*. For constraint satisfaction problems the thresholds are usually fractions of the number of constraints: gap-MAX 3SAT$[1, s]$ means "all clauses satisfiable" versus "fewer than a fraction $s$ of the clauses satisfiable".

**Gap problem, minimization.** For a minimization problem with $c(x) \le s(x)$, gap-$\Pi[c, s]$ has $\mathrm{YES} = \{x : \mathrm{OPT}(x) \le c(x)\}$ and $\mathrm{NO} = \{x : \mathrm{OPT}(x) > s(x)\}$.

**Ratios.** On this site a minimization $\rho$-approximation has $\mathrm{ALG} \le \rho\,\mathrm{OPT}$ with $\rho \ge 1$, and a maximization $\alpha$-approximation has $\mathrm{ALG} \ge \alpha\,\mathrm{OPT}$ with $\alpha \le 1$. The ratio of the gap is $s/c$: below 1 for maximization, above 1 for minimization.

**Proposition (gap hardness gives ratio hardness).** If gap-$\Pi[c, s]$ is NP-hard and $c, s$ are computable in polynomial time, then, unless P = NP, $\Pi$ has no polynomial-time $\alpha$-approximation with $\alpha > s/c$ (maximization), and no $\rho$-approximation with $\rho < s/c$ (minimization).

*Proof.* Maximization: let $\mathcal{A}$ be an $\alpha$-approximation with $\alpha > s/c$. Accept $x$ when $\mathcal{A}(x) \ge s(x)$. On YES, $\mathcal{A}(x) \ge \alpha\,\mathrm{OPT} \ge \alpha c > s$. On NO, $\mathcal{A}(x) \le \mathrm{OPT} < s$. Minimization: let $\mathcal{A}$ be a $\rho$-approximation with $\rho < s/c$, and accept when $\mathcal{A}(x) \le s(x)$. On YES, $\mathcal{A}(x) \le \rho c < s$. On NO, $\mathcal{A}(x) \ge \mathrm{OPT} > s$. In both cases the test solves the gap problem in polynomial time, and composing with the map $h$ decides 3SAT. $\blacksquare$

The converse direction also has content: the [PCP theorem](/pcp-theorem/) is equivalent to the statement that gap-MAX 3SAT$[1, 1 - \varepsilon_0]$ is NP-hard for some constant $\varepsilon_0 > 0$ (Arora and Barak, Section 11.3). The direction from the PCP theorem to the gap is proved on [MAX 3SAT inapproximability](/max-3sat-inapproximability/).

## Examples and non-examples

**From an NP-hard decision problem with integer values.** If the decision question "$\mathrm{OPT} \le k$?" is NP-hard and the measure is an integer, then gap-$\Pi[k, k]$ in the minimization form (YES: $\mathrm{OPT} \le k$, NO: $\mathrm{OPT} > k$, so $\mathrm{OPT} \ge k + 1$) is NP-hard. The integer values give a better bound than the proposition: a $\rho$-approximation with $\rho < (k+1)/k$ returns a value below $k + 1$, so at most $k$, on YES instances, and at least $k + 1$ on NO instances. The bound $(k+1)/k$ is useful only when $k$ is a constant. For the [chromatic number](/chromatic-number/), the NP-hardness of [3-coloring](/three-coloring/) gives the gap "at most 3 colors" versus "at least 4 colors", so no algorithm has $\rho < 4/3$ unless P = NP (see [graph coloring inapproximability](/graph-coloring-inapproximability/)).

**A gap of unbounded ratio.** For general TSP, the map from [Hamiltonian cycle](/hamiltonian-cycle/) with weights 1 and $rn$ gives gap-TSP$[n, rn]$: YES instances have a tour of cost $n$, NO instances have none of cost at most $rn$. The ratio $r$ is arbitrary (see [general TSP inapproximability](/general-tsp-inapproximability/)).

**From the PCP theorem.** gap-MAX 3SAT$[1, 1 - \varepsilon_0]$ is NP-hard for a constant $\varepsilon_0 > 0$. Håstad (2001) shows that gap-MAX E3SAT$[1, 7/8 + \varepsilon]$ is NP-hard for each $\varepsilon > 0$, where E3 means exactly three literals per clause; see [Håstad's 3-bit PCP](/hastad-3bit-pcp/).

**From label cover.** gap-[label cover](/label-cover/)$[1, \delta]$ is NP-hard for each constant $\delta > 0$ with a large enough alphabet; it is the usual starting point for set cover and other problems.

**Non-example: perfect completeness for 2SAT.** gap-[MAX 2SAT](/max-2-sat/)$[1, s]$ is in P for each $s < 1$: deciding if all clauses can be satisfied is [2SAT](/two-sat-algorithm/), which is solvable in linear time. Hardness for MAX 2SAT needs completeness below 1.

**Non-example: perfect completeness for MAX CUT.** gap-[MAX CUT](/maximum-cut/)$[1, s]$, read as "all edges cut" versus "fewer than a fraction $s$ cut", is in P: all edges are cut exactly when the graph is bipartite, which breadth-first search decides.

**Non-example: perfect completeness for linear equations.** gap-MAX E3LIN2$[1, s]$ asks if a system of equations $x_i + x_j + x_k = b \pmod 2$ is fully satisfiable. [Gaussian elimination](/gaussian-elimination/) decides this (see [XOR-SAT](/xor-sat/)), so the problem is in P. Håstad's theorem is for gap-MAX E3LIN2$[1 - \varepsilon, 1/2 + \varepsilon]$, with imperfect completeness, and that version is NP-hard.
## Related definitions

- **[Gap-preserving reduction](/gap-preserving-reduction/).** A map from gap-$\Pi[c, s]$ to gap-$\Pi'[c', s']$ that sends YES to YES and NO to NO; it carries hardness from one problem to another.
- **[Gap amplification](/gap-amplification/).** Ways to make the ratio $s/c$ smaller (for max): graph products, parallel repetition, and the steps of Dinur's proof.
- **[Approximation threshold](/approximation-threshold/).** The best ratio possible unless P = NP; gap problems give its lower bounds.
- **[Probabilistically checkable proofs](/probabilistically-checkable-proof/).** A PCP verifier with completeness $c$ and soundness $s$ gives an NP-hard gap problem for the maximum acceptance probability.
- **[Decision problem](/decision-problem/).** The case $c = s$ for maximization with $\ge$ versus $<$; a gap problem is a decision problem with a promise.

## References
