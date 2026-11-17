---
title: Each step of static optimization dFBA is an exact FBA solve followed by an Euler step
proves: [correctness]
status: full
---

Fix a network with matrix $S$, bounds $lb, ub$, a biomass index $b$, and a medium with species $k = 1, \ldots, K$. The matrix $E$ gives the change of species $k$ per unit flux of reaction $j$ and per unit biomass. Each uptake reaction $j$ of species $k$ has the parameters $v^{\max}_j > 0$ and $K_j \ge 0$. The state at step $i$ is $(t_i, X_i, z_i)$ with biomass $X_i \ge 0$ and concentrations $z_i \in \mathbb{R}^K$.

The code does the following at step $i$ (lines L3 to L7). For each uptake reaction $j$ of species $k$, with $s = \max(z_{i,k}, 0)$, it sets the upper bound

$$\bar u_j = \min\left( \frac{v^{\max}_j s}{K_j + s}, \; \frac{s}{X_i \Delta t} \right)$$

(the second term only when $X_i > 0$, and $\bar u_j = 0$ when $K_j + s = 0$). It solves the FBA problem $\max \{v_b : S v = 0, \; lb \le v \le \bar{ub}\}$, where $\bar{ub}$ is $ub$ with these entries replaced. If the LP is not optimal, it stops. Otherwise, with the optimal $v^{(i)}$ and $\mu_i = v^{(i)}_b$, the Euler update is

$$X_{i+1} = X_i + \Delta t \, \mu_i X_i, \qquad z_{i+1} = z_i + \Delta t \, (E v^{(i)}) X_i .$$

The exponential update replaces the factor $\Delta t$ by $(e^{\mu_i \Delta t} - 1)/\mu_i$ (or $\Delta t$ if $\mu_i = 0$) in the $z$ update, multiplies $X$ by $e^{\mu_i \Delta t}$, and cuts each $z_{i+1,k}$ at 0.

**Lemma 1 (each LP is solved exactly).** At each step the code stops if and only if the FBA problem with the bounds $lb, \bar{ub}$ is infeasible or unbounded, and otherwise $v^{(i)}$ is an optimal solution and $\mu_i$ is the optimal growth rate.

*Proof.* The bound $\bar u_j$ is a float, and Fraction(float) is the exact rational value of that float, so the LP has rational data. solve_lp then returns the exact status and an exact optimum (Lemma 1 of the proof on the flux variability analysis page). The conversion of $v^{(i)}$ to float for the update rounds each flux once, which is the only rounding in the step apart from the float arithmetic of the update itself. $\square$

**Lemma 2 (the update is the Euler step of the ODE).** Let $v(t)$ be the flux vector that the method uses on $[t_i, t_{i+1})$. The Euler update is one explicit Euler step of

$$\frac{dX}{dt} = v_b X, \qquad \frac{dz}{dt} = (E v) X$$

with step $\Delta t$ from $(X_i, z_i)$. The exponential update is the exact solution of this ODE on $[t_i, t_{i+1}]$ when $v$ is held at $v^{(i)}$ over the step, up to the cut at 0.

*Proof.* The first part is the definition of the explicit Euler method: the right side is evaluated at the start of the step. For the second, with $v = v^{(i)}$ constant, $X(t) = X_i e^{\mu_i (t - t_i)}$ solves the first equation, and then $z_k(t) = z_{i,k} + (E v^{(i)})_k X_i \int_0^{t - t_i} e^{\mu_i \tau} \, d\tau = z_{i,k} + (E v^{(i)})_k X_i (e^{\mu_i (t - t_i)} - 1)/\mu_i$ for $\mu_i \ne 0$, and $z_{i,k} + (E v^{(i)})_k X_i (t - t_i)$ for $\mu_i = 0$. At $t = t_{i+1}$ these are the formulas of the code. $\square$

**Lemma 3 (the medium does not become negative).** Assume that species $k$ is used only by its uptake reaction $j$, that is, $E_{k j} = -1$ and $E_{k j'} v_{j'} \ge 0$ for every $j' \ne j$ and every feasible $v$ (as in the overflow network of the page). If $z_{i,k} \ge 0$ and $X_i > 0$, then the Euler update gives $z_{i+1,k} \ge 0$. If $X_i = 0$, then $X_{i+1} = 0$ and $z_{i+1} = z_i$.

*Proof.* With $X_i > 0$, $v^{(i)}_j \le \bar u_j \le z_{i,k} / (X_i \Delta t)$. So $z_{i+1,k} \ge z_{i,k} - \Delta t \, v^{(i)}_j X_i \ge z_{i,k} - z_{i,k} = 0$, since the other terms of $(E v^{(i)})_k$ are not negative. With $X_i = 0$ both updates add 0. $\square$

**Lemma 4 (biomass stays non-negative).** If $X_0 \ge 0$, then $X_i \ge 0$ for all $i$ for the exponential update. For the Euler update, $X_i \ge 0$ holds whenever $1 + \Delta t \, \mu_i \ge 0$ at every step, in particular whenever every $\mu_i \ge 0$ (for example when $lb_b \ge 0$).

*Proof.* $X_{i+1} = X_i e^{\mu_i \Delta t}$ in the first case, and $X_{i+1} = X_i (1 + \Delta t \, \mu_i)$ in the second. $\square$

**Lemma 5 (a constant yield conserves mass).** Let the substrate be species $k$ with uptake reaction $j$, and assume that every LP of the run has $\mu_i = Y v^{(i)}_j$ and $(E v^{(i)})_k = -v^{(i)}_j$ for a constant $Y > 0$. Then the Euler update keeps $X_i + Y z_{i,k}$ constant, exactly in real arithmetic.

*Proof.* $X_{i+1} + Y z_{i+1,k} = X_i + \Delta t \, Y v^{(i)}_j X_i + Y z_{i,k} - Y \Delta t \, v^{(i)}_j X_i = X_i + Y z_{i,k}$. $\square$

In the overflow network of the page, a large oxygen bound gives $\mu = \frac{2}{15} u$ for every uptake $u$, so Lemma 5 holds with $Y = \frac{2}{15}$. The test checks it to $10^{-9}$, which is the effect of float rounding only.

**Theorem.** Run dfba for $N$ steps. Every record $(t_i, X_i, z_i, v^{(i)})$ with $v^{(i)}$ not None holds an exact FBA optimum $v^{(i)}$ for the bounds of step $i$ (rounded to float), and $(X_{i+1}, z_{i+1})$ is the Euler step (or the exponential step) of the ODE of Lemma 2 with $v = v^{(i)}$ on $[t_i, t_{i+1})$. The run stops early exactly when some LP is infeasible or unbounded. Under the hypotheses of Lemmas 3 and 4, the biomass and the substrate concentrations stay non-negative.

*Proof.* Induction over the steps with Lemmas 1 to 4. $\square$

**Remark (convergence).** If the map $z \mapsto v(z)$ from the medium to the chosen FBA optimum is Lipschitz near the solution, the ODE of Lemma 2 has a unique solution, and the explicit Euler method converges to it with a global error of order $\Delta t$; this is the standard convergence theorem of the Euler method. The optimal value of an LP is a continuous, piecewise linear function of the bounds, so $\mu$ is Lipschitz whenever the uptake bounds are Lipschitz in $z$ (the Monod term is, for $K_j > 0$). The other fluxes need not be: when the LP optimum is not unique, the solver may jump between optimal vertices. In the overflow network the optimum is unique and piecewise linear in $u$, so the theorem applies away from depletion, where the cap $s/(X \Delta t)$ is not active. The test measures the error ratio for halved steps, which is close to 2.
