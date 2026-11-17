---
title: What tau-leaping guarantees
proves: [correctness]
status: full
---

Tau-leaping is an approximation, so "correct" here means four precise claims: the leap is exact when the propensities do not change during the leap; the step of lines L5 to L8 meets the leap condition by construction; the method never returns a negative count; and when every reaction is critical, it is the exact direct method. The bias of a leap chain in a linear network is computed at the end. The setting is that of the [direct method](/gillespie-algorithm/): propensities $a_j(x)$, change vectors $\nu_j$, and the Markov jump process $X$ of the chemical master equation.

**Claim 1 (exact for constant propensities).** Suppose that the propensities stay at $a_j(x)$ on $[t, t + \tau)$ whatever reactions fire. Then the numbers $K_j$ of firings of the reactions in that interval are independent, with $K_j$ Poisson of mean $a_j(x) \tau$.

*Proof.* With constant rates, the firings of reaction $j$ form a Poisson process of rate $a_j(x)$, and the processes of different reactions are independent (a jump process with constant rates $a_1, \ldots, a_m$ splits into independent Poisson processes, one per reaction). The count of a Poisson process of rate $a$ in an interval of length $\tau$ is Poisson of mean $a \tau$. $\square$

This holds exactly when every reaction has order 0 (sources only). Then a leap of any length gives the exact law. In general the propensities change with $x$, and a leap uses their values at the start of the step. That is the approximation.

**Claim 2 (the leap condition).** Let $\tau'$ be the value of line L5, and let $I$ be the set of reactant species. For each $i \in I$, write $\hat\mu_i = \sum_{j \text{ noncritical}} \nu_{ij} a_j(x)$ and $\hat\sigma_i^2 = \sum_{j \text{ noncritical}} \nu_{ij}^2 a_j(x)$. Then for every leap of length $\tau \le \tau'$ in which no critical reaction fires,

$$|\mathbb{E}[\Delta x_i]| \le \max(\varepsilon x_i / g_i, 1), \qquad \operatorname{Var}[\Delta x_i] \le \max(\varepsilon x_i / g_i, 1)^2,$$

where $\Delta x_i = \sum_j \nu_{ij} K_j$ is the change of species $i$ in the leap.

*Proof.* In such a leap, the $K_j$ of the noncritical reactions are independent Poisson variables of mean $a_j \tau$, so $\mathbb{E}[\Delta x_i] = \hat\mu_i \tau$ and $\operatorname{Var}[\Delta x_i] = \hat\sigma_i^2 \tau$. Write $b_i = \max(\varepsilon x_i / g_i, 1)$. Line L5 takes $\tau' \le b_i / |\hat\mu_i|$ and $\tau' \le b_i^2 / \hat\sigma_i^2$ for each $i$ (a term with a zero denominator puts no bound). So $|\hat\mu_i| \tau \le b_i$ and $\hat\sigma_i^2 \tau \le b_i^2$. $\square$

Cao, Gillespie and Petzold (2006) choose $g_i$ from the highest order reaction in which species $i$ is a reactant so that a relative change of at most $\varepsilon / g_i$ in $x_i$ changes each propensity by a relative amount of at most about $\varepsilon$. For example, for $2X_i \to \ldots$ with propensity $c\, x_i (x_i - 1) / 2$, a change $\delta$ in $x_i$ changes the propensity by the factor $1 + \delta (2 x_i - 1 + \delta) / (x_i (x_i - 1))$, whose first order part in $\delta / x_i$ is $(2 + 1/(x_i - 1))\, \delta / x_i$, the value of $g_i$ for this case. The bound "at least 1" on $b_i$ lets a species with a small count change by about one molecule.

**Claim 3 (no negative counts).** Every state that the method records has all counts $\ge 0$.

*Proof.* A leap is accepted at line L11 only if $x + \sum_j K_j \nu_j \ge 0$ in every entry; otherwise it is drawn again with a smaller step. The steps of the direct method in line L6 fire one reaction with a positive propensity, and a mass action propensity is positive only if the reactants are present, so these steps keep the counts $\ge 0$. The repeat terminates with probability 1: as $\tau' \to 0$, the probability that every noncritical $K_j$ is 0 tends to 1, and a leap in which only one critical reaction fires once (or nothing fires) never makes a count negative. $\square$

**Claim 4 (all critical gives the direct method).** If every reaction with $a_j(x) > 0$ is critical in the state $x$, the step from $x$ has the law of one step of the direct method.

*Proof.* With no noncritical reaction, $\hat\mu_i = \hat\sigma_i^2 = 0$, so $\tau' = \infty$ and line L6 does not switch. Line L7 draws $\tau''$ exponential with rate $a_0^c = a_0(x)$. Line L8 gives $\tau = \min(\tau'', T - t)$, and line L9 sets every $K_j = 0$. If $\tau = \tau''$, line L10 picks one reaction with probability $a_j / a_0$ and fires it once. This is the next reaction density $a_j e^{-a_0 s}$ of Lemma 2 of the proof for the direct method, and when $t + \tau'' > T$ no reaction fires in $(t, T]$, as in the direct method. $\square$

In the code the draws are in the same order as in `ssa_direct` of the helper, so the test checks that the two give the same trajectory, not only the same law.

**The bias of a fixed-step leap in two linear networks.** For pure death $X \to 0$ at rate 1 per molecule, a leap of length $\tau$ maps $x$ to $x - K$ with $K$ Poisson of mean $x \tau$ (ignore the rare rejected leaps). By the laws of total expectation and variance, $m_{k+1} = (1 - \tau) m_k$ and $V_{k+1} = (1 - \tau)^2 V_k + \tau m_k$. So after $T / \tau$ steps the mean is $x_0 (1 - \tau)^{T/\tau}$, against the exact $x_0 e^{-T}$. For immigration-death with rates $b$ and 1, $m_{k+1} = m_k + \tau (b - m_k)$ and $V_{k+1} = (1 - \tau)^2 V_k + \tau (b + m_k)$. The fixed point is $m = b$ and $V = 2 b \tau / (1 - (1 - \tau)^2) = 2b / (2 - \tau)$, against the exact stationary variance $b$. So the leap chain has the right stationary mean, and a stationary variance that is too large by the factor $2 / (2 - \tau)$, for $0 < \tau < 2$.
