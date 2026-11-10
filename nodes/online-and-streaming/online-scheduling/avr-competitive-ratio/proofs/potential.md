---
title: AVR uses at most 2^(alpha - 1) alpha^alpha times the energy of any feasible schedule
proves: [statement]
status: full
---

This is the proof of Bansal, Bunde, Chan and Pruhs (Section 5 of their paper), with the details written out. The power is $s^{\alpha}$ with $\alpha > 1$. Jobs are $(r_j, w_j, d_j)$ with density $\delta_j = w_j / (d_j - r_j)$.

## Setup

Fix any feasible schedule $S$. Let $s_{S, j}(t)$ be the rate at which $S$ runs job $j$ at time $t$, and $s_S(t) = \sum_j s_{S, j}(t)$. Its energy is $E(S) = \int s_S(t)^{\alpha} \, dt$. We may assume that $S$ is piecewise constant with finitely many pieces, as the optimal YDS schedule is.

The energy of AVR depends only on its speed $s_{\text{AVR}}(t) = \sum_{j : r_j \le t < d_j} \delta_j$. So for the analysis we let AVR run each job $j$ at rate $\delta_j$ on $[r_j, d_j)$. Then AVR has done $\delta_j (t - r_j)$ units of job $j$ by time $t \in [r_j, d_j]$.

Job $j$ is of **type A** if $\int_{r_j}^{t} s_{S, j} \ge \delta_j (t - r_j)$ for all $t \in [r_j, d_j]$, so $S$ is never behind AVR on $j$. It is of **type B** if $\int_{r_j}^{t} s_{S, j} \le \delta_j (t - r_j)$ for all $t \in [r_j, d_j]$. An input is **bitonic** for $S$ if each job is of type A or of type B.

## Step 1. Reduction to bitonic inputs

Let $g_j(t) = \int_{r_j}^{t} s_{S, j} - \delta_j (t - r_j)$. It is continuous and piecewise linear with finitely many pieces, and $g_j(r_j) = g_j(d_j) = 0$. If $j$ is of neither type, $g_j$ takes both signs, so there is a time $t \in (r_j, d_j)$ with $g_j(t) = 0$ at which the sign of $g_j$ changes. Let $x = \delta_j (t - r_j)$, the work that both have done by $t$. Replace $j$ by the two jobs $j' = (r_j, x, t)$ and $j'' = (t, w_j - x, d_j)$.

- Both new jobs have density $\delta_j$: $x / (t - r_j) = \delta_j$ and $(w_j - x)/(d_j - t) = \delta_j (d_j - t)/(d_j - t) = \delta_j$. So the AVR speed does not change at any time, and the AVR energy is the same.
- Let $S$ run $j'$ where it ran $j$ before $t$, and $j''$ where it ran $j$ after $t$. This is feasible: $S$ did exactly $x$ units of $j$ in $[r_j, t]$ and $w_j - x$ in $[t, d_j]$. The energy is the same.
- The function $g$ of $j'$ is $g_j$ on $[r_j, t]$, and the function $g$ of $j''$ is $g_j$ on $[t, d_j]$, so the number of sign changes drops by one.

Since each $g_j$ has finitely many sign changes, finitely many splits give an input $\sigma'$ that is bitonic for $S$, with $\text{AVR}(\sigma') = \text{AVR}(\sigma)$, and $S$ is a feasible schedule for $\sigma'$ with the same energy. So it is enough to prove $\text{AVR}(\sigma') \le 2^{\alpha - 1} \alpha^{\alpha} E(S)$ for bitonic inputs.

## Step 2. Inputs of type A jobs only

**Lemma A.** If every job is of type A for $S$, then $\text{AVR}(\sigma) \le \alpha^{\alpha} E(S)$.

*Proof.* At the current time $t_0$, let $t_1 < t_2 < \dots < t_m$ be the distinct deadlines after $t_0$ of the jobs released by $t_0$, and let $I_i = [t_i, t_{i+1})$ with length $\tau_i = t_{i+1} - t_i$, for $0 \le i < m$. Let $s_i$ be the AVR speed on $I_i$ if no more jobs arrive; it is the sum of $\delta_j$ over the released jobs with $d_j \ge t_{i+1}$. Since a job open on $I_i$ is open on all earlier intervals, $s_0 \ge s_1 \ge \dots$.

AVR will do $\delta_j \tau_i$ units of each such job $j$ in $I_i$. Let $w_{A, i} = s_i \tau_i$ be the total AVR work planned for $I_i$. For the schedule $S$, assign the remaining work of job $j$ in $S$ to the latest parts of this plan: if $S$ has $\rho_j$ units of $j$ left, then the part of $\rho_j$ in $I_i$ is $\min(\delta_j \tau_i, \max(0, \rho_j - \delta_j (d_j - t_{i+1})))$. Let $w_{S, i}$ be the sum of these parts over the jobs. By type A, $\rho_j \le \delta_j (d_j - t_0)$, the AVR work left on $j$, so all of $\rho_j$ is assigned, and $0 \le w_{S, i} \le w_{A, i}$. When $S$ works on $j$, the part in the smallest index $i$ that holds work of $j$ shrinks. Define

$$\Phi(t_0) = \alpha \sum_{i \ge 0} s_i^{\alpha - 1} \left( w_{A, i} - \alpha \, w_{S, i} \right).$$

We check three properties.

*(a) Boundary values.* Before the first release and after the last deadline there are no intervals, so $\Phi = 0$.

*(b) No increase at events.* A job completes in $S$ or in AVR: $\Phi$ is continuous in the $w$ values, so nothing jumps. The current time reaches $t_1$: then $\tau_0 = 0$, so $w_{A, 0} = 0$, and $w_{S, 0} = 0$ because $\rho_j \le \delta_j (d_j - t_1)$ for each job by type A. The term of $I_0$ is 0, and dropping it does not change $\Phi$. A job arrives with density $y$ and deadline $d$: if $d$ is a new deadline, first split the interval that contains it; the two parts have the same $s_i$, and the terms are linear in the $w$ values, so this does not change $\Phi$. Now $d = t_k$ for some $k$. The arrival adds $y$ to $s_i$ and $y \tau_i$ to both $w_{A, i}$ and $w_{S, i}$ for $i < k$, since $S$ has done none of the new job. With $q = w_{A, i}$, $r = w_{S, i}$ and $\delta = y \tau_i$, and $s_i = q / \tau_i$, the change of the term of $I_i$ is

$$\frac{\alpha}{\tau_i^{\alpha - 1}} \left[ (q + \delta)^{\alpha - 1} (q + \delta - \alpha (r + \delta)) - q^{\alpha - 1} (q - \alpha r) \right],$$

and the bracket is at most 0 by Lemma C below. So $\Phi$ does not increase.

*(c) The running condition.* Between events, AVR runs at speed $s_0$, so $w_{A, 0}$ drops at rate $s_0$ and the other $w_{A, i}$ and all $s_i$ stay fixed. $S$ removes work at total rate $s_S$ from some terms $w_{S, k}$, each with $s_k \le s_0$. Hence

$$\frac{d\Phi}{dt} \le -\alpha s_0^{\alpha - 1} s_0 + \alpha^2 s_0^{\alpha - 1} s_S,$$

and

$$s_0^{\alpha} + \frac{d\Phi}{dt} - \alpha^{\alpha} s_S^{\alpha} \le (1 - \alpha) s_0^{\alpha} + \alpha^2 s_0^{\alpha - 1} s_S - \alpha^{\alpha} s_S^{\alpha}.$$

If $s_S = 0$, the right side is $(1 - \alpha) s_0^{\alpha} \le 0$. Otherwise put $z = s_0 / s_S \ge 0$; the right side is $s_S^{\alpha} u(z)$ with $u(z) = (1 - \alpha) z^{\alpha} + \alpha^2 z^{\alpha - 1} - \alpha^{\alpha}$. Its derivative is $u'(z) = \alpha (\alpha - 1) z^{\alpha - 2} (\alpha - z)$, so $u$ increases on $[0, \alpha]$ and decreases after, and its largest value is $u(\alpha) = (1 - \alpha) \alpha^{\alpha} + \alpha^{\alpha + 1} - \alpha^{\alpha} = 0$. So $s_{\text{AVR}}^{\alpha} + d\Phi/dt \le \alpha^{\alpha} s_S^{\alpha}$.

Integrating (c) over time and using (a) and (b) gives $\text{AVR}(\sigma) \le \alpha^{\alpha} E(S)$. $\square$

## Step 3. Inputs of type B jobs only

**Lemma B.** If every job is of type B for $S$, then $\text{AVR}(\sigma) \le \alpha^{\alpha} E(S)$.

*Proof.* Reverse time: map each job $(r_j, w_j, d_j)$ to $(-d_j, w_j, -r_j)$ and the schedule $S$ to $\bar S(t) = S(-t)$. The density of each job is the same, so the AVR speed of the reversed input is $s_{\text{AVR}}(-t)$ and the AVR energy is the same. $\bar S$ is feasible with the same energy. In the reversed input, by time $-t$ the schedule $\bar S$ has done the work that $S$ does in $[t, d_j]$, which is $w_j - \int_{r_j}^{t} s_{S, j} \ge w_j - \delta_j (t - r_j) = \delta_j (d_j - t)$, the work that AVR does in $[t, d_j]$. So each job is of type A for $\bar S$, and Lemma A applies. $\square$

## Step 4. Combining the two kinds

Let $\sigma$ be bitonic for $S$, with type A jobs $\mathcal A$ and type B jobs $\mathcal B$ (a job of both types goes to $\mathcal A$). Let $s_{\mathcal A}(t)$ and $s_{\mathcal B}(t)$ be the AVR speeds of the two kinds, so $s_{\text{AVR}} = s_{\mathcal A} + s_{\mathcal B}$, and let $S_{\mathcal A}$ and $S_{\mathcal B}$ be $S$ restricted to each kind. Each restriction is feasible for its kind, and each job keeps its type. By the convexity of $x \mapsto x^{\alpha}$, $((a + b)/2)^{\alpha} \le (a^{\alpha} + b^{\alpha})/2$ for $a, b \ge 0$. So

$$\text{AVR}(\sigma) = \int (s_{\mathcal A} + s_{\mathcal B})^{\alpha} \le 2^{\alpha - 1} \left( \int s_{\mathcal A}^{\alpha} + \int s_{\mathcal B}^{\alpha} \right) \le 2^{\alpha - 1} \alpha^{\alpha} \left( E(S_{\mathcal A}) + E(S_{\mathcal B}) \right),$$

by Lemmas A and B. For $x, y \ge 0$ and $\alpha \ge 1$, $x^{\alpha} + y^{\alpha} \le (x + y)^{\alpha}$, so $E(S_{\mathcal A}) + E(S_{\mathcal B}) \le E(S)$. With Step 1, $\text{AVR}(\sigma) \le 2^{\alpha - 1} \alpha^{\alpha} E(S)$ for every input and every feasible $S$. Taking $S$ optimal proves the theorem. $\blacksquare$

## Lemma C

For $q, r, \delta \ge 0$ and $\alpha \ge 1$,

$$f = (q + \delta)^{\alpha - 1} (q - \alpha r - (\alpha - 1) \delta) - q^{\alpha - 1} (q - \alpha r) \le 0.$$

*Proof.* Note that $q + \delta - \alpha(r + \delta) = q - \alpha r - (\alpha - 1)\delta$, so this is the bracket of Step 2. Write

$$f = (q - \alpha r) \left[ (q + \delta)^{\alpha - 1} - q^{\alpha - 1} \right] - (\alpha - 1) \delta (q + \delta)^{\alpha - 1}.$$

The square bracket is at least 0 and $q - \alpha r \le q$, so $f \le q [(q + \delta)^{\alpha - 1} - q^{\alpha - 1}] - (\alpha - 1) \delta (q + \delta)^{\alpha - 1}$. If $q = 0$ this is $-(\alpha - 1) \delta^{\alpha} \le 0$. Otherwise put $\delta = z q$ with $z \ge 0$; the bound is $q^{\alpha} h(z)$ with $h(z) = (1 + z)^{\alpha - 1} - 1 - (\alpha - 1) z (1 + z)^{\alpha - 1}$. Then $h(0) = 0$ and

$$h'(z) = (\alpha - 1)(1 + z)^{\alpha - 2} \left[ 1 - (1 + z) - (\alpha - 1) z \right] = -\alpha (\alpha - 1) z (1 + z)^{\alpha - 2} \le 0,$$

so $h(z) \le 0$ for $z \ge 0$, and $f \le 0$. $\square$
