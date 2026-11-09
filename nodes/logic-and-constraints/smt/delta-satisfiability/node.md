---
tag: ZF2DAF
kind: definition
slug: delta-satisfiability
name: Delta-satisfiability
aliases:
- delta-decidability
- delta-complete decision
- δ-satisfiability
- bounded δ-SMT
area: logic-and-constraints/smt
level: research
summary: Decide that a formula is unsatisfiable or that its delta-weakening is satisfiable, with bounded numeric error.
prereqs: [nonlinear-real-arithmetic-satisfiability, computable-real-numbers, computable-function]
see_also: [interval-constraint-propagation, tarski-decidability-theorem, richardson-theorem, ode-initial-value-problem, lipschitz-condition, bounded-model-checking, hybrid-automata, smt-problem]
sources:
  - paper: "Sicun Gao, Jeremy Avigad and Edmund M. Clarke, δ-Complete decision procedures for satisfiability over the reals, Automated Reasoning (IJCAR 2012), Lecture Notes in Computer Science 7364, Springer, 2012, 286 to 300"
    locator: Definition 3.1 (δ-weakening), Definition 3.2 (bounded δ-SMT), Theorem 3.1 (decidability), Theorem 3.2 and Corollaries 3.1 and 3.2 (complexity); page numbers to be checked
  - paper: "Sicun Gao, Jeremy Avigad and Edmund M. Clarke, Delta-decidability over the reals, Proceedings of the 27th IEEE Symposium on Logic in Computer Science (LICS 2012), 305 to 314"
    locator: the δ-decision problem for bounded sentences with arbitrary quantifiers and its complexity in the polynomial hierarchy (page numbers to be checked)
  - paper: "Sicun Gao, Soonho Kong and Edmund M. Clarke, dReal, an SMT solver for nonlinear theories over the reals, Automated Deduction (CADE-24), Lecture Notes in Computer Science 7898, Springer, 2013"
    locator: the solver that implements δ-complete decision with interval constraint propagation
  - paper: "Daniel Richardson, Some undecidable problems involving elementary functions of a real variable, Journal of Symbolic Logic 33(4) (1968), 514 to 520"
    locator: the undecidability of exact problems with sine
  - book: isbn:9783540668176
    title: Klaus Weihrauch, Computable Analysis, An Introduction, Springer, 2000
    locator: the Type 2 model of computation on real numbers and computable real functions
---

Delta-satisfiability is a relaxed version of satisfiability for formulas over the real numbers with functions such as $\sin$, $\exp$ and solutions of differential equations, where exact satisfiability is undecidable. Given a formula $\varphi$ and a small positive rational $\delta$, a *δ-complete* decision procedure answers either "unsatisfiable", which is then exactly true, or "δ-satisfiable", which means that the formula holds after numerical perturbations of size at most $\delta$. Gao, Avigad and Clarke (2012) proved that this question is decidable for bounded formulas over all Type 2 computable functions, and that it is NP-complete for common functions. It is the theory behind numerical SMT solvers such as dReal, and it relaxes exact [nonlinear real arithmetic](/nonlinear-real-arithmetic-satisfiability/).

## Definition

**Functions.** Let $F$ be a finite set of real functions that are *computable* in the Type 2 sense of [computable analysis](/computable-real-numbers/): a machine, given better and better rational approximations of the arguments, outputs rational approximations of the value with any requested accuracy. Addition, multiplication, $\exp$, $\sin$, and solutions of ODE initial value problems with a [Lipschitz](/lipschitz-condition/) right-hand side are all computable. Each computable function on a compact box is continuous, with a computable modulus of continuity.

**Bounded formulas.** A *bounded $\Sigma_1$ sentence* is $\exists^{I_1} x_1 \cdots \exists^{I_n} x_n\, \psi(x)$, where each $I_i$ is a bounded interval with rational ends, $\psi$ is a Boolean combination of atoms $f(x) \bowtie 0$ with $f$ built from $F$, and each function is defined on the closure of the box $I_1 \times \cdots \times I_n$. Such a sentence can be put in the *standard form* (Lemma 2.1 of Gao, Avigad and Clarke 2012)
$$\varphi = \exists^{I} x\, \bigwedge_{i=1}^{m} \bigvee_{j=1}^{k_i} f_{ij}(x) = 0,$$
by turning $f \ne 0$ into $f < 0 \vee f > 0$, and $f \ge 0$ into $f - v = 0$ with a new bounded variable $v \in [0, M]$, where $M$ exceeds the maximum of $f$ on the box ($v \in (0, M]$ for $f > 0$).

**δ-weakening.** For a rational $\delta \ge 0$, the δ-weakening of $\varphi$ is
$$\varphi^{\delta} = \exists^{I} x\, \bigwedge_{i=1}^{m} \bigvee_{j=1}^{k_i} |f_{ij}(x)| \le \delta.$$
Equivalently, $\varphi^{\delta}$ is true if and only if some perturbation of the constants by at most $\delta$, $f_{ij}(x) = c_{ij}$ with $|c_{ij}| \le \delta$, makes $\varphi$ true. Since $c = 0$ is allowed, $\varphi$ implies $\varphi^{\delta}$.

**The bounded δ-SMT problem.** Given $\varphi$ in standard form and $\delta > 0$ rational, return

- **unsat** only if $\varphi$ is false, and
- **δ-sat** only if $\varphi^{\delta}$ is true.

If both hold, either answer is correct. A procedure that always returns a correct answer is *δ-complete*.

**What the answers guarantee.**

- An *unsat* answer is exact: no real point satisfies $\varphi$. A safety check that encodes "a bad state is reachable" as $\varphi$ can therefore prove safety.
- A *δ-sat* answer does not say that $\varphi$ is satisfiable. It says that $\varphi$ is satisfiable or is within $\delta$ of being satisfiable: a small change of the constants would make it true. The witness box returned by a solver need not contain an exact model.
- Neither answer says which case holds when both $\varphi$ is false and $\varphi^{\delta}$ is true. So the answer is not a decision of $\varphi$, and the gap shrinks only as $\delta$ shrinks, at a higher cost.
- The guarantee depends on the syntax of $\varphi$. Rewriting $f = 0$ as $1000 f = 0$ changes the meaning of the δ-weakening.

**Theorem (Gao, Avigad and Clarke 2012).** Let $F$ be a finite set of Type 2 computable functions and $\delta > 0$ rational. Then the bounded δ-SMT problem over $F$ is decidable.

*Proof.* Rescale each variable to $[0, 1]$; each $g_{ij}$, the $f_{ij}$ composed with the rescaling, is still computable, and has a computable modulus of continuity on the compact cube. Choose $\varepsilon = 2^{-e}$ such that $\lVert x - y \rVert < \varepsilon$ implies $|g_{ij}(x) - g_{ij}(y)| < \delta/4$ for all $i, j$, and let $S$ be the finite grid of points with coordinates $k \varepsilon$, $0 \le k \le 2^e$; each point of the cube is within $\varepsilon$ of a grid point. At each $a \in S$, compute an approximation $\tilde g_{ij}(a)$ with $|\tilde g_{ij}(a) - g_{ij}(a)| < \delta/8$, and let $\hat\psi(a)$ be the conjunction over $i$ of the disjunction over $j$ of $|\tilde g_{ij}(a)| < \delta/2$. Return δ-sat if $\hat\psi(a)$ is true for some $a \in S$, and unsat otherwise.

If $\hat\psi(a)$ holds, then $|g_{ij}(a)| < 5\delta/8$ for one $j$ in each clause $i$. If $a$ is in the box, it witnesses $\varphi^{\delta}$; if $a$ is on the boundary of an open interval, continuity gives a nearby point in the box with all these values below $\delta$. So δ-sat is correct. If $\hat\psi(a)$ is false for each $a \in S$, take any $x$ in the box and a grid point $a$ within $\varepsilon$. For some clause $i$, each $j$ has $|\tilde g_{ij}(a)| \ge \delta/2$, so $|g_{ij}(a)| \ge 3\delta/8$ and $|g_{ij}(x)| \ge 3\delta/8 - \delta/4 = \delta/8 > 0$. So clause $i$ fails at $x$, and $\varphi$ is false, so unsat is correct. $\square$

**Complexity (quoted from the same paper).** If the functions in $F$ are in a Type 2 complexity class $C$ with $\mathrm{P} \subseteq C \subseteq \mathrm{PSPACE}$, and the formulas use a uniform bound on the domains, the problem is in $\mathrm{NP}^{C}$: guess a grid point, and evaluate the functions with the oracle. For polynomial-time functions such as $\{+, \times, \exp, \sin\}$ it is NP-complete, and for Lipschitz ODEs it is in PSPACE and PSPACE-complete for some ODEs. The LICS 2012 paper extends decidability to bounded sentences with any quantifiers, and places the version with $k$ quantifier alternations in $(\Sigma_k^{\mathrm{P}})^{C}$.

## Examples and non-examples

Each example was checked with a script that runs the grid procedure from the proof in one variable.

- **A false formula that is δ-sat.** $\exists^{[-1,1]} x\, (x^2 + 1 = 0)$ is false over the reals. Its δ-weakening $|x^2 + 1| \le \delta$ is true for $\delta \ge 1$ (at $x = 0$). With $\delta = 1/2$ the only correct answer is unsat. With $\delta = 4$ both answers are correct, and the grid procedure returns δ-sat.
- **Two distinct points.** $\exists^{[-1,1]} x\, (x = 0 \wedge x = 10^{-6})$ is false, but δ-sat for $\delta = 10^{-3}$, since $x = 0$ is within $\delta$ of both. A δ-sat answer here does not mean a model exists.
- **A transcendental equation.** $\exists^{[3,4]} x\, (\sin x = 0)$ is true ($x = \pi$), so unsat is never a correct answer, and a δ-complete procedure must return δ-sat; the script found the grid point $3.14125$ for $\delta = 10^{-3}$.
- **A robust unsat.** $\exists^{[0,7]} x\, (\sin x = 2)$ is unsat for each $\delta < 1$, since $|\sin x - 2| \ge 1$.
- **SAT inside.** The NP-hardness proof encodes a propositional variable $p$ as a real $x_p \in [-1, 2]$ with the clause $x_p = 0 \vee x_p = 1$, $p$ as $x_p < 0$ and $\neg p$ as $x_p > 1$. For each $\delta < 1/2$ the encoding of a satisfiable CNF is true, and the encoding of an unsatisfiable CNF has a false δ-weakening, so the two cases do not overlap.
- **Non-example: unbounded domains.** The definition needs bounded intervals. Over all of $\mathbb{R}$, the exact problem with $\sin$ is undecidable ([Richardson's theorem](/richardson-theorem/)), and the grid argument fails, because no finite grid covers the domain.
- **Non-example: exact NRA.** For polynomials only, the exact question is decidable by [Tarski's theorem](/tarski-decidability-theorem/); δ-satisfiability is then a cheaper but weaker answer, not a replacement.

## Related definitions

- [Nonlinear real arithmetic](/nonlinear-real-arithmetic-satisfiability/) is the exact problem for polynomials; δ-satisfiability is its numerical relaxation, extended to computable functions.
- [Interval constraint propagation](/interval-constraint-propagation/), a branch and prune search on boxes with [interval arithmetic](/interval-arithmetic/), is the practical δ-complete method. Inside a [DPLL(T)](/dpll-t/) solver it is δ-complete when the pruning operators are well-behaved (Section 4 of the IJCAR paper). dReal implements it.
- [Computable real numbers](/computable-real-numbers/) and [computable functions](/computable-function/) give the model of computation that defines "computable" here.
- In [bounded model checking](/bounded-model-checking/) of [hybrid automata](/hybrid-automata/) with [ODE dynamics](/ode-initial-value-problem/), unsat proves that no bad state is reachable within the bound, and δ-sat says that the system is unsafe under some δ-bounded perturbation, which is a useful warning for robust designs.

## References
