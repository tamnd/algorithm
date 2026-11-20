---
tag: BD2KKJ
kind: algorithm
slug: geometric-programming-power-control
name: Power control by geometric programming
aliases:
- GP power control
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: "Writes power control on the SINR model as a geometric program in log powers: exact for min power, max-min SINR and high-SINR rates, and a chain of GPs for the general sum rate."
solves: [max-min-sinr-power-control, weighted-sum-rate-maximization]
model: real-ram
complexity:
  vars: {K: the number of links, T: the number of outer rounds, S: the Newton steps per geometric program}
  time: {worst: O(T S K^4)}
  space: {extra: O(K^2)}
properties: {deterministic: true, global_optimum_for_gp_forms: true, monotone_outer_rounds: true, local_optimum_in_general: true, centralized: true}
history:
  year: 2007
  people: [Mung Chiang, Chee Wei Tan, Daniel P. Palomar, Daniel O'Neill, David Julian]
  note: "Chiang and his coauthors showed that many power control problems are geometric programs at high SINR, and solved the general SINR case by a series of geometric programs built by condensation."
prereqs: [geometric-programming, interior-point-method, foschini-miljanic-power-control]
see_also: [geometric-programming, max-min-sinr-power-control, standard-interference-function, weighted-sum-rate-maximization, barrier-method, weighted-mmse-precoding, energy-efficient-power-allocation, kkt-conditions]
sources:
  - paper: doi:10.1109/TWC.2007.05960
    title: "Mung Chiang, Chee Wei Tan, Daniel P. Palomar, Daniel O'Neill and David Julian, Power control by geometric programming, IEEE Transactions on Wireless Communications 6(7), 2007, pages 2640 to 2651"
    locator: "the power control problems that are geometric programs in the high-SINR regime, and the series of geometric programs by condensation for the general SINR regime"
  - paper: doi:10.1007/s11081-007-9001-7
    title: "Stephen Boyd, Seung-Jean Kim, Lieven Vandenberghe and Arash Hassibi, A tutorial on geometric programming, Optimization and Engineering 8(1), 2007, pages 67 to 127"
    locator: "monomials, posynomials and the standard form; the change of variables that makes a GP convex; the monomial approximation of a posynomial and the heuristic of solving a series of GPs"
  - book: isbn:9780521833783
    title: "Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004"
    locator: "Section 4.5 (geometric programming and its convex form), Section 11.3 (the barrier method and the duality gap m/t on the central path)"
---

Power control by geometric programming is a method that finds the transmit powers of $K$ interfering links by writing the problem as a geometric program (GP) in the variables $y_i = \log p_i$, where it is convex. Minimum power under SINR targets, max-min SINR, and the sum rate in the high-SINR approximation are GPs and are solved to global optimality. The true sum rate is not a GP; the method then solves a chain of GPs, each built by replacing one sum by a single monomial at the current powers, and each round raises the sum rate until it stops at a KKT point, which may be only a local optimum. Next to [Foschini-Miljanic power control](/foschini-miljanic-power-control/), which meets fixed targets by a distributed iteration, and [max-min SINR power control](/max-min-sinr-power-control/), which has its own eigenvalue solution, this is the general tool for objectives on the same SINR model, and it rests on the theory of [geometric programming](/geometric-programming/).

## In plain words

Several radio links share a channel and disturb one another. We want to set their powers well: the least total power that meets each link's need, or the best quality for the worst link, or the most data in total. These tasks look hard because each link's quality is a fraction with the other powers below the line. A change of scale helps: if we work with the logarithm of each power, many of these tasks become bowl-shaped, and a standard solver finds the true best answer. The task of the most total data does not become bowl-shaped. For it, we replace the hard part by a simple guess that is correct at the current powers and never too optimistic, solve that easier task, and repeat. Each round can only improve the total, but the end point can be a good answer that is not the best one.

## The problem

There are $K$ links. The gain from transmitter $j$ to receiver $i$ is $G_{ij} \ge 0$ with $G_{ii} > 0$, receiver $i$ has the noise power $\sigma_i > 0$, and link $i$ has the power limit $\bar p_i$. With the interference plus noise $N_i(p) = \sum_{j \ne i} G_{ij} p_j + \sigma_i$,

$$\mathrm{SINR}_i(p) = \frac{G_{ii}\, p_i}{N_i(p)}.$$

A *monomial* is $c\, x_1^{a_1} \cdots x_n^{a_n}$ with $c > 0$ and real $a_k$; a *posynomial* is a sum of monomials. A GP minimizes a posynomial subject to posynomial $\le 1$ and monomial $= 1$. With $y = \log x$, each monomial is $e^{b + a^T y}$, and $\log$ of a posynomial is the convex function $\log \sum_m e^{b_m + a_m^T y}$. The key fact for power control is that the constraint $\mathrm{SINR}_i(p) \ge \gamma_i$ is the posynomial constraint

$$\frac{\gamma_i}{G_{ii}} \Big( \sum_{j \ne i} G_{ij}\, p_j\, p_i^{-1} + \sigma_i\, p_i^{-1} \Big) \le 1.$$

So these problems are GPs:

1. **Least total power.** Minimize $\sum_i p_i$ subject to $\mathrm{SINR}_i \ge \gamma_i$ and $p_i \le \bar p_i$.
2. **Max-min SINR.** Maximize $t$, that is minimize $t^{-1}$, subject to $t\, N_i(p) / (G_{ii} p_i) \le 1$ and $p_i \le \bar p_i$.
3. **High-SINR sum rate.** When every SINR is large, $\log_2(1 + \mathrm{SINR}_i) \approx \log_2 \mathrm{SINR}_i$, and maximizing $\sum_i \log \mathrm{SINR}_i$ is minimizing $\sum_i \log\big(N_i(p) / (G_{ii} p_i)\big)$, a sum of logs of posynomials, subject to $\mathrm{SINR}_i \ge \gamma_i^{\min}$ and $p_i \le \bar p_i$.

The general problem is the true sum rate:

$$\max_{p} \; \sum_{i=1}^K \log_2\big(1 + \mathrm{SINR}_i(p)\big) \quad \text{s.t.} \quad \mathrm{SINR}_i(p) \ge \gamma_i^{\min},\; 0 < p_i \le \bar p_i. \tag{1}$$

Since $1 + \mathrm{SINR}_i = D_i(p)/N_i(p)$ with $D_i(p) = \sum_j G_{ij} p_j + \sigma_i$ (all $j$, including $i$), (1) is the same as minimizing $\sum_i \log\big(N_i(p) / D_i(p)\big)$: a ratio of posynomials, which is not a GP. In general (1) is NP-hard; see [weighted sum rate maximization](/weighted-sum-rate-maximization/).

## The algorithm

The outer loop handles (1). At the current powers $p$, write the terms of $D_i(p)$ as $u_{i0} = \sigma_i$ and $u_{ij} = G_{ij} p_j$, and put $\alpha_{im} = u_{im} / D_i(p)$, so the weights of each link sum to 1. The weighted arithmetic and geometric mean inequality gives, for all $q > 0$,

$$D_i(q) = \sum_m \alpha_{im}\, \frac{u_{im}(q)}{\alpha_{im}} \;\ge\; \prod_m \Big(\frac{u_{im}(q)}{\alpha_{im}}\Big)^{\alpha_{im}} = \tilde D_i(q),$$

with equality at $q = p$. $\tilde D_i$ is a monomial, so $N_i / \tilde D_i$ is a posynomial. This step is called *condensation*.

```pseudo id=main
GP-POWER-CONTROL(G, σ, p̄, γmin, ε)
L1  p ← a strictly feasible start (Foschini-Miljanic powers for 1.01 γmin)
L2  repeat
L3      for each link i: α_im ← u_im(p) / D_i(p) for the terms u_im of D_i
L4      D̃_i(q) ← Π_m (u_im(q) / α_im)^α_im      ▷ monomial, D̃_i ≤ D_i, equal at p
L5      p_new ← argmin Σ_i log(N_i(q) / D̃_i(q)) s.t. γmin_i N_i(q) / (G_ii q_i) ≤ 1, q_i ≤ p̄_i   ▷ a GP in y = log q
L6      if rate(p_new) - rate(p) ≤ ε then return p_new
L7      p ← p_new
```

Line L5 is solved by the barrier method on the convex form. For $t = 1, \mu, \mu^2, \ldots$, it minimizes $f_0(y) - \frac{1}{t} \sum_k \log(-f_k(y))$ by Newton's method with a backtracking line search, where $f_0$ is the objective and $f_k(y) \le 0$ are the constraints, all logs of posynomials. It stops when $m/t$ is below the gap tolerance, with $m$ constraints. The gradient and the Hessian of $\log \sum_m e^{z_m}$ with $z_m = b_m + a_m^T y$ are $\sum_m w_m a_m$ and $\sum_m w_m a_m a_m^T - (\sum_m w_m a_m)(\sum_m w_m a_m)^T$, with the softmax weights $w_m = e^{z_m} / \sum_l e^{z_l}$. The problems 1, 2 and 3 above use the same solver directly, with no outer loop.

## Example

Take the three links of the [Foschini-Miljanic](/foschini-miljanic-power-control/) example: $G_{ii} = 1$, cross gains $G_{12} = 0.1$, $G_{13} = 0.2$, $G_{21} = 0.2$, $G_{23} = 0.1$, $G_{31} = G_{32} = 0.1$, noise $0.1$ at each receiver, and the limit $\bar p_i = 1$.

- **Least total power** for $\gamma_i = 2$: the GP returns $(0.442105, 0.452632, 0.378947)$, which is $(42, 43, 36)/95$, the Foschini-Miljanic fixed point, to 11 digits.
- **Max-min SINR:** the GP returns $t^* = 2.68487$ (4.29 dB) with $p = (0.9643, 1, 0.7959)$; link 2 is at its limit and all three SINRs equal $t^*$. Bisection on the common target gives the same value.
- **Sum rate** with $\gamma^{\min}_i = 1$: the start is the least power for the targets $1.01$, $p = (0.1416, 0.1427, 0.1297)$, with the sum rate $3.0216$ bits per channel use. The rounds of lines L2 to L7 give $5.3733$, $5.7272$, $5.7302$, $5.7302$ and end at $p = (1, 1, 1)$ with the SINRs $(2.5, 2.5, 3.333)$. Here the high-SINR GP gives the same powers.

**A local optimum.** Two links with strong coupling: $G = \begin{pmatrix} 1 & 0.8 \\ 0.9 & 1 \end{pmatrix}$, noise $0.1$, $\bar p_i = 1$, $\gamma^{\min}_i = 0.1$. From the least-power start, the rounds give $0.2776$, $0.5260$, $0.8948$, $1.3289$, $1.8143$, $2.6493$, $2.8435$ and stop at $p = (0.09, 1)$: link 1 is held at its minimum SINR $0.1$, and the sum rate is $2.8435$. No small feasible change improves it. A grid search finds the global optimum $2.8502$ at $p = (1, 0.1)$, the mirror choice. Both points are KKT points of (1); the outer loop cannot tell them apart.

## Correctness

**Claim.**

1. With $y = \log p$, each problem 1, 2 and 3 is a convex problem, so the barrier method returns a point whose objective is within the gap tolerance of the global optimum.
2. In the outer loop, every iterate is feasible for (1), the sum rate never decreases from one round to the next, and so the sum rates converge. If the GP of line L5 is solved exactly and returns the current $p$, then $p$ is a KKT point of (1).

**Key steps.** The Hessian of $\log \sum_m e^{z_m}$ is the covariance matrix of the vectors $a_m$ under the weights $w_m$, so it is positive semidefinite, and logs of posynomials are convex in $y$. A constraint written as $\log(\text{posynomial}) \le 0$ is then a convex constraint. On the central path of the barrier method, $\lambda_k = 1/(t\,(-f_k))$ are dual feasible multipliers with the duality gap $m/t$. For the outer loop, $\tilde D_i \le D_i$ gives $\log(N_i/\tilde D_i) \ge \log(N_i/D_i)$: the GP objective of line L5 is an upper bound on the objective of (1), equal to it at the current $p$. Minimizing the bound cannot raise it above its value at $p$, so the true objective cannot rise either (this is the majorize-minimize argument). The feasible set of line L5 is that of (1), so feasibility is kept. At $q = p$ the gradients of $\log \tilde D_i$ and $\log D_i$ in $y$ are both $(\alpha_{i1}, \ldots, \alpha_{iK})$, so a fixed point of the loop satisfies the KKT conditions of (1). The full proof is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/), the teaching solver does the following work per Newton step. The objective of line L5 has $K$ posynomials with $K$ terms each, and after condensation each term has an exponent vector with up to $K$ nonzero entries, so the Hessian costs $O(K^4)$; the $2K$ constraints add $O(K^3)$, and the Newton system costs $O(K^3)$ by [Gaussian elimination](/gaussian-elimination/). With $S$ Newton steps per GP and $T$ rounds, the time is $O(T S K^4)$, and the space is $O(K^2)$. Interior-point methods solve a GP in polynomial time, and in practice $S$ is a few tens. On the examples above $T$ is 4 to 7. A solver that keeps the posynomial $N_i$ and the monomial $\tilde D_i$ apart can bring the Hessian cost down to $O(K^3)$.

## Properties

- **Global optimum for GP forms.** Least power, max-min SINR (with any posynomial limits), and the high-SINR sum rate are solved to global optimality, together with dual multipliers that give the sensitivity of the optimum to each target and limit.
- **Monotone outer loop.** The sum rate rises with each round and stays feasible. The loop is a majorize-minimize method, also called successive convex approximation.
- **Local optimum in general.** Problem (1) is NP-hard, and the loop can stop at a KKT point that is not the global optimum, as in the example with strong coupling. The start matters.
- **Exact at high SINR.** When all SINRs are large, $\log(1 + \mathrm{SINR}) - \log \mathrm{SINR} = \log(1 + 1/\mathrm{SINR})$ is small, and a single GP is close to optimal; its answer is also a good start for the outer loop.
- **Centralized.** The solver needs all gains $G_{ij}$, so it runs at a controller that collects them.

## Variants and improvements

- **Other objectives.** Any objective that is a product of posynomials divided by monomials fits, for example weighted products of SINRs (proportional fairness at high SINR) or the least power for given rates, since the rate target $\log_2(1 + \mathrm{SINR}_i) \ge r_i$ is $\mathrm{SINR}_i \ge 2^{r_i} - 1$.
- **Outage limits.** In Rayleigh fading, the probability that the SINR of a link stays above a threshold has a closed product form in the powers. A limit on the outage probability then becomes a constraint that is convex in the log powers, so outage-limited power control is solved by the same kind of solver.
- **Dual decomposition.** At high SINR the GP can be split by links with [dual decomposition](/dual-decomposition/), so that each link updates its own power from messages of its neighbors.
- **Other inner approximations.** The weighted MMSE method of [weighted MMSE precoding](/weighted-mmse-precoding/) and the [fractional programming](/fractional-programming/) transforms also turn (1) into a series of convex problems, with closed-form steps instead of a GP solve. For energy efficiency, the ratio of rate to power, see [energy-efficient power allocation](/energy-efficient-power-allocation/).
- **Global methods.** Branch and bound over the power box, using monotonicity in each power, finds the global optimum of (1) for small $K$, at a cost that grows exponentially in $K$.

## When to use it

Use the GP forms whenever the objective and the limits fit: least power, max-min SINR, and high-SINR rates, for a central controller that knows the gains. They give the global optimum and the dual multipliers. Use the outer loop when the low-SINR links matter and a good local optimum is enough, and start it from the high-SINR GP solution or from several starts. For fixed targets with no central controller, use the [Foschini-Miljanic](/foschini-miljanic-power-control/) iteration instead; for max-min SINR with a total power limit, the eigenvalue solution of [max-min SINR power control](/max-min-sinr-power-control/) is simpler.

## Pitfalls

- **A strictly feasible start.** The barrier method needs a start that meets every constraint with slack. The least powers for targets slightly above $\gamma^{\min}$ give one if they are below the limits; otherwise the problem is infeasible, or a phase I problem must find a start.
- **Zero powers.** The log variables cannot reach $p_i = 0$. If switching a link off is better, as often happens with strong interference, the GP can only push $p_i$ toward its lower bound. Binary on and off choices need a separate search.
- **The high-SINR approximation at low SINR.** At an SINR of 1, $\log_2 \mathrm{SINR} = 0$ while $\log_2(1 + \mathrm{SINR}) = 1$. The approximation rewards a link with a low SINR far less than the true rate does, and its answer can be poor when some SINRs are near or below 1.
- **Local optima.** The outer loop is not a global method. Try several starts when the coupling is strong.
- **Scaling.** Gains often span many orders of magnitude. The log variables help, but very large exponents in the solver can still overflow; the log-sum-exp should subtract the largest term first.

## Implementations

## History

Kandukuri and Boyd (2002) wrote power control with outage limits in Rayleigh fading as a GP, and Julian, Chiang, O'Neill and Boyd (2002) used GPs for rate and fairness goals in cellular and ad hoc networks. Chiang, Tan, Palomar, O'Neill and Julian (2007) collected these into one method: they listed the power control problems that are GPs in the high-SINR regime and treated the general SINR regime by solving a series of GPs built by condensation, a method that had long been used for signomial programs, the extension of GPs that allows negative coefficients. The tutorial of Boyd, Kim, Vandenberghe and Hassibi (2007) gave the modeling rules and the monomial approximation in general form.

## References
