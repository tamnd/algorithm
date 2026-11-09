---
title: Benders decomposition stops with the right answer
proves: [correctness]
status: full
---

**Statement.** Let $X \subseteq \mathbb{Z}^p$ be finite, and let all data be rational. Then BENDERS stops after at most $|V(D)| + |V(R)| + 1$ iterations, where $V(D)$ is the set of vertices of $D = \{u \ge 0 : B^\top u \le d\}$ and $V(R)$ the set of vertices of $R = \{\rho \ge 0 : B^\top \rho \le 0,\ 1^\top \rho \le 1\}$. It returns INFEASIBLE if the problem has no feasible solution, UNBOUNDED if its value is $-\infty$, and otherwise an optimal solution.

**Setup.** For $x \in X$ let $r(x) = h - G x$ and $\Phi(x) = \min\{d^\top y : B y \ge r(x),\ y \ge 0\}$, with $\Phi(x) = +\infty$ when this linear program is infeasible and $\Phi(x) = -\infty$ when it is unbounded. The problem is $\mathrm{OPT} = \min_{x \in X} (c^\top x + \Phi(x))$. A point $x \in X$ is *good* if $\Phi(x) < +\infty$. We use [Farkas' lemma](/farkas-lemma/) in this form: the system $B y \ge r$, $y \ge 0$ has no solution if and only if some $\rho \ge 0$ has $B^\top \rho \le 0$ and $\rho^\top r > 0$. We also use [weak and strong duality](/lp-duality/) for the pair $\mathrm{SP}$, $\mathrm{DSP}$ of the page.

**Lemma 1 (feasibility cuts are valid).** If $\rho \ge 0$ and $B^\top \rho \le 0$, then $\rho^\top r(x) \le 0$ for every good $x$.

*Proof.* Take $y \ge 0$ with $B y \ge r(x)$. Since $\rho \ge 0$, $\rho^\top r(x) \le \rho^\top B y = (B^\top \rho)^\top y$. Since $B^\top \rho \le 0$ and $y \ge 0$, this is at most $0$. $\square$

**Lemma 2 (the test of line L6).** The value $w$ of line L6 is positive if and only if $\hat{x}$ is not good.

*Proof.* If $w > 0$, the optimal $\rho$ has $\rho \ge 0$, $B^\top \rho \le 0$ and $\rho^\top r(\hat{x}) = w > 0$, so $\hat{x}$ is not good by Lemma 1. If $\hat{x}$ is not good, Farkas' lemma gives $\rho \ge 0$ with $B^\top \rho \le 0$ and $\rho^\top r(\hat{x}) > 0$. Then $\rho \ne 0$, and $\rho / (1^\top \rho)$ is feasible for the LP of line L6 with a positive value, so $w > 0$. $\square$

**Lemma 3 (optimality cuts are valid).** If $u \in D$, then $u^\top r(x) \le \Phi(x)$ for every good $x$.

*Proof.* For each $y \ge 0$ with $B y \ge r(x)$: $u^\top r(x) \le u^\top B y = (B^\top u)^\top y \le d^\top y$, because $u \ge 0$, $B^\top u \le d$ and $y \ge 0$. Take the infimum over $y$. $\square$

**Lemma 4 (the master is a relaxation).** In each iteration, every good $x$ meets all feasibility cuts in $F$, and for each such $x$ and each $y$ feasible for $\mathrm{SP}(x)$, the point $(x, \eta) = (x, d^\top y)$ is feasible for the master. So, if a good $x$ exists, the master is feasible and its optimal value is at most $\mathrm{OPT}$.

*Proof.* The cuts of $F$ come from line L6, so they satisfy the hypothesis of Lemma 1. The cuts of $O$ are optimal solutions of $\mathrm{DSP}$, so they lie in $D$, and Lemma 3 gives $u^\top r(x) \le \Phi(x) \le d^\top y$. While $O$ is empty, $\eta$ is free and the bound is trivial. $\square$

**The returns are correct.**

1. *Line L4.* The master is infeasible. By Lemma 4 no $x \in X$ is good, so the problem has no feasible solution.
2. *Line L9.* We reach line L8 only when $w = 0$, so $\hat{x}$ is good by Lemma 2. A feasible linear program whose dual is infeasible is unbounded, by the duality theorem. So $\Phi(\hat{x}) = -\infty$ and $\mathrm{OPT} = -\infty$.
3. *Line L10.* Here $\hat{x}$ is good and $\mathrm{DSP}(\hat{x})$ has an optimal solution, so by strong duality $\mathrm{SP}(\hat{x})$ has an optimal $y^*$ with $d^\top y^* = s$. The test $\hat{\eta} \ge s$ cannot hold while $\hat{\eta} = -\infty$, so $O$ is not empty, and the master value is $c^\top \hat{x} + \hat{\eta}$. By Lemma 4,
$$c^\top \hat{x} + d^\top y^* = c^\top \hat{x} + s \le c^\top \hat{x} + \hat{\eta} \le \mathrm{OPT} \le c^\top \hat{x} + d^\top y^*,$$
where the last step holds because $(\hat{x}, y^*)$ is feasible. So all terms are equal, and $(\hat{x}, y^*)$ is optimal.

Since the three returns are the only exits and each one is correct, the answer INFEASIBLE comes exactly when the problem is infeasible, and so on for the other two, once we show that the method stops.

**Termination.** Consider an iteration that does not return.

1. *It ends at line L7.* The simplex method returns a basic optimal solution, so $\rho \in V(R)$. The point $\hat{x}$ is a master solution, so $\rho'^\top r(\hat{x}) \le 0$ for each $\rho' \in F$. But $\rho^\top r(\hat{x}) = w > 0$. So $\rho \notin F$, and $|F|$ grows by one.
2. *It ends at line L11.* The cut $u$ is a basic optimal solution of $\mathrm{DSP}(\hat{x})$, so $u \in V(D)$. The test of line L10 failed, so $\hat{\eta} < s = u^\top r(\hat{x})$. If $u$ were in $O$, the master would force $\hat{\eta} \ge u^\top r(\hat{x})$. So $u \notin O$, and $|O|$ grows by one.

So the quantity $|F| + |O|$ increases by exactly one in each iteration that does not return, and it never exceeds $|V(R)| + |V(D)|$. The polyhedra $R$ and $D$ are defined by finitely many rational inequalities, so they have finitely many vertices. Hence there are at most $|V(R)| + |V(D)|$ iterations that do not return, and the next iteration returns. $\blacksquare$
