---
title: The MOSA archive is the front of all points evaluated, and both acceptance rules have the Boltzmann distribution of the weighted sum as their fixed-temperature equilibrium
proves: [correctness]
status: full
---

All objectives are minimized, $p$ is the number of objectives, $w \ge 0$ is the weight vector, $h(x) = \sum_m w_m f_m(x)$, and line numbers refer to the `pseudo id=main` block of the multi-objective simulated annealing page. We write $\Delta_m = f_m(y) - f_m(x)$ for a move from $x$ to $y$, $a \preceq b$ when $a$ weakly dominates $b$, and $a^+ = \max(0, a)$.

The two rules are $\pi_S = \min(1, e^{-\sum_m w_m \Delta_m / T}) = e^{-(\sum_m w_m \Delta_m)^+ / T}$ and $\pi_P = \prod_m \min(1, e^{-w_m \Delta_m / T}) = e^{-\sum_m (w_m \Delta_m)^+ / T}$.

## The archive

**Theorem 1.** After each step, the images of the archive are exactly the non-dominated images of the start point and all neighbours evaluated, one member per image.

*Proof.* By induction. The archive starts as the start point. Let it be the non-dominated images of the set $S$ evaluated before $y$. If a member $a$ has $a \preceq f(y)$, line L4 changes nothing: every image that $f(y)$ dominates is dominated by $a$, and $f(y)$ is dominated by or equal to $a$, so the non-dominated images of $S \cup \{f(y)\}$ are those of $S$. Otherwise no point of $S$ dominates $f(y)$, since a dominator $s$ would give a non-dominated $u \preceq s$ in the archive that dominates $f(y)$. So $f(y)$ is non-dominated in $S \cup \{f(y)\}$, and the others are the members that $f(y)$ does not dominate. Line L4 removes the rest and adds $f(y)$. $\square$

The archive does not depend on the acceptance rule; the rule only decides where the search goes next.

## The acceptance rules

**Lemma 2.** For $T > 0$:

1. $\pi_P \le \pi_S$.
2. If $f(y) \preceq f(x)$, then $\pi_P = \pi_S = 1$.
3. If $f(x)$ dominates $f(y)$ and $w > 0$, then $\pi_P \le \pi_S < 1$, and both fall as $T$ falls.

*Proof.* (1) $\sum_m (w_m \Delta_m)^+ \ge (\sum_m w_m \Delta_m)^+$, because each $(a_m)^+ \ge a_m$ and each $(a_m)^+ \ge 0$. (2) All $\Delta_m \le 0$ and $w \ge 0$, so both exponents are $0$. (3) All $\Delta_m \ge 0$, one is positive, and $w > 0$, so $\sum_m w_m \Delta_m > 0$ and $\pi_S < 1$. A positive exponent $-s/T$ with $s > 0$ decreases as $T$ decreases. $\square$

**Theorem 3.** Both rules satisfy $\pi(x \to y)\, e^{-h(x)/T} = \pi(y \to x)\, e^{-h(y)/T}$. So if the neighbour proposal is symmetric and the neighbour graph is connected, the chain of current solutions at a fixed temperature $T$ has the stationary distribution $e^{-h(x)/T} / Z$.

*Proof.* For any real $a$, $a^+ - (-a)^+ = a$. For the sum rule take $a = \sum_m w_m \Delta_m = h(y) - h(x)$: $\pi_S(x \to y) / \pi_S(y \to x) = e^{-(a^+ - (-a)^+)/T} = e^{-(h(y) - h(x))/T}$. For the product rule apply the identity to each $a_m = w_m \Delta_m$ and sum: $\sum_m (a_m^+ - (-a_m)^+) = \sum_m a_m = h(y) - h(x)$. This is detailed balance; with a symmetric proposal $q(x, y) = q(y, x)$, the transition kernel $q \pi$ is reversible for $e^{-h/T}$, which is then stationary. $\square$

So at a fixed temperature both rules sample the same distribution, which puts more weight on the minimizers of the weighted sum $h$ as $T$ falls. The sum rule is exactly the [Metropolis criterion](/metropolis-criterion/) for $h$, so the current solution of MOSA with the sum rule is a plain simulated annealing chain on $h$, and the [convergence theorem of simulated annealing](/simulated-annealing-convergence/) applies to $h$ under its hypotheses: a finite space, a connected and weakly reversible neighbourhood, and a schedule $T_k = c/\log(k+1)$ with $c$ at least the depth of the deepest non-global local minimum of $h$. Then the probability that the current solution minimizes $h$ tends to $1$. The product rule is not the Metropolis rule, so that theorem does not apply to it as stated.

**Lemma 4.** If $w > 0$, every minimizer of $h$ is Pareto-optimal.

*Proof.* If $f(z)$ dominated $f(x)$, then $w_m f_m(z) \le w_m f_m(x)$ for all $m$, with strict inequality for one $m$ because $w_m > 0$. So $h(z) < h(x)$, and $x$ is not a minimizer. $\square$

The converse fails: a Pareto-optimal point that is not supported minimizes $h$ for no $w$, as on the [weighted sum method](/weighted-sum-method/) page. So the limit theorem for a fixed $w$ reaches only supported points. The archive can still hold unsupported points, because it keeps every non-dominated point the chain evaluates.
