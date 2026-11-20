---
tag: K8XR5H
kind: algorithm
slug: foschini-miljanic-power-control
name: Foschini-Miljanic power control
aliases:
- distributed power control
area: communications/link-adaptation-and-resource-allocation
level: core
summary: "Each link scales its power by target SINR over measured SINR. If the targets are feasible (spectral radius of the normalized gain matrix below 1), this converges to the least powers that meet them."
model: real-ram
complexity:
  vars: {K: the number of links, T: the number of iterations}
  time: {worst: O(T K^2)}
  space: {extra: O(K)}
properties: {deterministic: true, distributed: true, needs_only_local_measurements: true, converges_iff_feasible: true}
history:
  year: 1993
  people: [Gerard J. Foschini, Zoran Miljanic]
  note: "Foschini and Miljanic gave the law as a differential equation and as a difference equation, and proved exponentially fast convergence whenever a central controller could meet the SINR targets."
prereqs: [perron-frobenius-theorem, fixed-point-iteration]
see_also: [standard-interference-function, max-min-sinr-power-control, geometric-programming-power-control, near-far-problem, jacobi-method, power-iteration, code-division-multiple-access, weighted-sum-rate-maximization]
sources:
  - paper: doi:10.1109/25.260747
    title: "Gerard J. Foschini and Zoran Miljanic, A simple distributed autonomous power control algorithm and its convergence, IEEE Transactions on Vehicular Technology 42(4), 1993, pages 641 to 646"
    locator: "Section III.A (the differential equation form), Section III.B (the difference equation, the step beta in (0, 1] and the proof that beta = 1 is the largest universal choice)"
  - paper: doi:10.1109/49.414651
    title: "Roy D. Yates, A framework for uplink power control in cellular radio systems, IEEE Journal on Selected Areas in Communications 13(7), 1995, pages 1341 to 1347"
    locator: "the standard interference function, with the fixed-assignment iteration of Foschini and Miljanic as the first example, and the synchronous and asynchronous convergence theorems"
  - paper: doi:10.1109/25.120145
    title: "Jens Zander, Performance of optimum transmitter power control in cellular radio systems, IEEE Transactions on Vehicular Technology 41(1), 1992, pages 57 to 62"
    locator: "the normalized link gain matrix and the largest achievable common SINR as the inverse of its spectral radius"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Chapter 4 (power control in the uplink of a CDMA system, and the distributed iteration toward the target SINRs)"
---

Foschini-Miljanic power control is an iterative algorithm that lets $K$ radio links that share a band reach their SINR targets with the least transmit power. Each link measures its own signal to interference plus noise ratio (SINR) and multiplies its power by the target SINR divided by the measured SINR. No link needs the gains of the others, so the method is fully distributed. If the targets can be met at all, which is the case exactly when the spectral radius of the normalized gain matrix is below 1 (see the [Perron-Frobenius theorem](/perron-frobenius-theorem/)), the powers converge geometrically to the unique smallest power vector that meets every target; if not, the powers grow without bound. The iteration is the linear case of the fixed-point theorem on [standard interference functions](/standard-interference-function/). It holds each link at a fixed target, while [max-min SINR power control](/max-min-sinr-power-control/) asks for the largest common target and [power control by geometric programming](/geometric-programming-power-control/) optimizes a rate objective.

## In plain words

Several radios talk at the same time on the same frequency. Each one hears the others as noise. Each link has a quality goal, a ratio of wanted signal to unwanted signal. If one link turns its power up, it reaches its goal, but it also hurts the others, which then turn up too.

The rule is short. Each link looks at the quality it has now. If the quality is half the goal, it doubles its power; if it is twice the goal, it halves its power. It acts as if the others will not change. They do change, but the steps get smaller each round. When all the goals can be met together, the powers settle at the lowest values that meet them. When the goals ask for too much, the powers keep rising, and the system must drop a link or lower a goal.

## The problem

There are $K$ links. Transmitter $j$ uses the power $p_j \ge 0$. The power gain from transmitter $j$ to receiver $i$ is $G_{ij} \ge 0$, with $G_{ii} > 0$ the gain of link $i$, and receiver $i$ has the noise power $\sigma_i > 0$. Powers and noise are in watts (or all in milliwatts), and gains have no unit. Each receiver treats the other signals as noise, so its SINR is

$$\mathrm{SINR}_i(p) = \frac{G_{ii}\, p_i}{\sum_{j \ne i} G_{ij}\, p_j + \sigma_i}.$$

Link $i$ wants $\mathrm{SINR}_i(p) \ge \gamma_i$ for a target $\gamma_i > 0$, for example the SNR that its modulation and code need. Multiply out: the targets hold exactly when $p \ge F p + u$ entrywise, where

$$F_{ij} = \frac{\gamma_i G_{ij}}{G_{ii}} \ (j \ne i), \qquad F_{ii} = 0, \qquad u_i = \frac{\gamma_i \sigma_i}{G_{ii}}.$$

$F$ is the *normalized gain matrix*; it is nonnegative. A power vector with $p \ge Fp + u$ is *feasible*. The problem asks for the feasible vector with the least power, and for a way to reach it in which each link uses only what its own receiver measures.

## The algorithm

Each link keeps its power $p_i(t)$. The step size $\beta$ is in $(0, 1]$; the original law of Foschini and Miljanic has $\beta = 1$ as the best universal choice.

```pseudo id=main
FOSCHINI-MILJANIC(G, γ, σ, p(0), β, T, ε)
L1  for t ← 0 to T - 1 do
L2      for each link i, in parallel, do
L3          I_i ← Σ_{j≠i} G_ij p_j(t) + σ_i        ▷ measured by receiver i
L4          p_i(t+1) ← (1 - β) p_i(t) + β γ_i I_i / G_ii
L5      if max_i |p_i(t+1) - p_i(t)| ≤ ε max_i p_i(t+1) then return p(t+1)
L6  return p(T)
```

Line L4 is the rule "multiply the power by target over measured SINR": when $p_i(t) > 0$, $\gamma_i I_i / G_{ii} = (\gamma_i / \mathrm{SINR}_i)\, p_i(t)$. Written with $I_i$, it also works for a link that starts at zero power. In vector form, one round is

$$p(t+1) = (1 - \beta)\, p(t) + \beta\, \big(F p(t) + u\big).$$

With $\beta = 1$ this is $p(t+1) = F p(t) + u$, the [Jacobi iteration](/jacobi-method/) for the linear system $(I - F) p = u$, computed with no central controller. In a real system the receiver measures $I_i$ or the SINR and sends one number back to its transmitter, and line L5 is replaced by running the loop for as long as the links are active.

## Example

Three links share one channel. The gains, the noise of 0.1 mW at each receiver and the common target $\gamma_i = 2$ (3.01 dB) give

$$G = \begin{pmatrix} 1 & 0.1 & 0.2 \\ 0.2 & 1 & 0.1 \\ 0.1 & 0.1 & 1 \end{pmatrix}, \qquad F = \begin{pmatrix} 0 & 0.2 & 0.4 \\ 0.4 & 0 & 0.2 \\ 0.2 & 0.2 & 0 \end{pmatrix}, \qquad u = \begin{pmatrix} 0.2 \\ 0.2 \\ 0.2 \end{pmatrix}.$$

The spectral radius of $F$ is $\rho(F) = 0.52547$, below 1, so the targets are feasible. Solving $(I - F)p = u$ gives the least powers $p^* = (42, 43, 36)/95 = (0.44211, 0.45263, 0.37895)$ mW. With $\beta = 1$ from $p(0) = 0$:

| $t$ | $p_1(t)$ | $p_2(t)$ | $p_3(t)$ | $\mathrm{SINR}_1$ | $\mathrm{SINR}_2$ | $\mathrm{SINR}_3$ |
|---|---|---|---|---|---|---|
| 1 | 0.2 | 0.2 | 0.2 | 1.2500 | 1.2500 | 1.4286 |
| 2 | 0.32 | 0.32 | 0.28 | 1.7021 | 1.6667 | 1.7073 |
| 3 | 0.376 | 0.384 | 0.328 | 1.8431 | 1.8462 | 1.8636 |
| 4 | 0.408 | 0.416 | 0.352 | 1.9245 | 1.9188 | 1.9298 |
| 5 | 0.424 | 0.4336 | 0.3648 | 1.9601 | 1.9595 | 1.9638 |

The powers rise in every entry, and the SINRs rise toward 2. The error shrinks by about $\rho(F) \approx 0.53$ per round, and the stopping test of line L5 with $\epsilon = 10^{-9}$ stops after 33 rounds, at $p^*$ to 9 digits.

Since $F$ is linear in the common target, $\rho(F) = 0.52547 \cdot \gamma / 2$. So a common target is feasible exactly when $\gamma < 2 / 0.52547 = 3.8061$ (5.81 dB). At $\gamma = 3.5$ the least powers are already $(4.64, 4.89, 3.68)$ mW, and at $\gamma = 4$ no power vector works: the iteration from zero grows past $10^6$ mW within 400 rounds. The largest common target $3.8061$ is the value that [max-min SINR power control](/max-min-sinr-power-control/) finds for this channel without noise.

## Correctness

**Claim.** Let $F \ge 0$, $u > 0$ and $\beta \in (0, 1]$.

1. If $\rho(F) < 1$, then $p^* = (I - F)^{-1} u$ is positive, it meets every target with equality, it is the least feasible vector ($p \ge p^*$ entrywise for every feasible $p$), and $p(t) \to p^*$ from every start $p(0) \ge 0$. The error satisfies $\|p(t) - p^*\| \le c\, r^t$ for each $r > (1 - \beta) + \beta \rho(F)$.
2. If $\rho(F) \ge 1$, then no feasible vector exists, and from $p(0) = 0$ the total power grows without bound.

**Key steps.** For $\rho(F) < 1$, the Neumann series $\sum_k F^k$ converges to $(I - F)^{-1} \ge 0$, so $p^* = u + Fu + F^2 u + \cdots \ge u > 0$. A feasible $p$ satisfies $p \ge u + Fp$; substituting this bound into itself $n$ times gives $p \ge \sum_{k < n} F^k u + F^n p \ge \sum_{k < n} F^k u$, so $p \ge p^*$. The error $e(t) = p(t) - p^*$ obeys $e(t+1) = C e(t)$ with $C = (1 - \beta) I + \beta F$, and every eigenvalue of $C$ has the form $(1 - \beta) + \beta \lambda$ with $|\lambda| \le \rho(F)$, so $\rho(C) \le (1 - \beta) + \beta \rho(F) < 1$. For $\rho(F) \ge 1$, the Perron-Frobenius theorem gives a nonzero $y \ge 0$ with $y^T F = \rho(F) y^T$. A feasible $p$ would give $y^T p \ge \rho(F) y^T p + y^T u > \rho(F)\, y^T p$, which is impossible for $\rho(F) \ge 1$ and $y^T p \ge 0$. The full proof is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/), one round of lines L2 to L4 costs $O(K^2)$ arithmetic operations when one computer simulates all links, because each interference sum has $K - 1$ terms. In a network, each link does $O(1)$ work per round, since its receiver measures $I_i$ as one number, and one number per round goes back over the feedback channel. The space is $O(K)$ besides the gains.

The number of rounds is not fixed. By the claim, the error falls like $\rho(C)^t$ with $\rho(C) = (1 - \beta) + \beta \rho(F)$ when $F$ is irreducible, so about $\ln(1/\epsilon) / \ln(1/\rho(C))$ rounds reduce the error by the factor $\epsilon$. This number grows without bound as the targets approach the edge of the feasible region, where $\rho(F) \to 1$. For $T$ rounds the simulated time is $O(T K^2)$ in the worst case. A central controller that knows $G$ can instead solve $(I - F) p = u$ by [Gaussian elimination](/gaussian-elimination/) in $O(K^3)$ time and test feasibility at the same time.

## Properties

- **Distributed.** Link $i$ uses only $\gamma_i$, $G_{ii}$ and the measured $I_i$ (or, for $p_i > 0$, only its measured SINR). Nobody needs the matrix $G$.
- **Least power.** The limit is the entrywise smallest feasible vector, so no link uses more power than it must, and the interference to everyone is as low as possible.
- **Monotone.** From $p(0) = 0$ the powers increase in every entry at each round; from a feasible start they decrease. This follows from $F \ge 0$.
- **Universal step.** For each $\beta \in (0, 1]$ the iteration converges whenever the targets are feasible, whatever the gains. Foschini and Miljanic showed that $\beta = 1$ is the largest value with this property: for two links and some gains, every $\beta > 1$ diverges although the targets are feasible.
- **Asynchronous.** The fixed point is also reached when links update at different times with old measurements, as long as each link keeps updating; Yates proved this for all [standard interference functions](/standard-interference-function/).

## Variants and improvements

- **Power limits.** Replace line L4 by $p_i \leftarrow \min(\bar p_i, \gamma_i I_i / G_{ii})$. The map is still a standard interference function, so the iteration converges to its unique fixed point. If the targets are not feasible within the limits, some links stay at $\bar p_i$ below their target.
- **Admission and active link protection.** A new link enters at low power and ramps up, while links that already meet their targets scale their targets so that they stay protected (Bambos, Chen and Pottie 2000). A link that cannot reach its target after a time leaves.
- **Up-link and base station choice.** The same rule with the gains of the up-link works there. If each mobile also picks the base station with the least needed power in each round, the map is still a standard interference function (Yates 1995).
- **Fixed steps.** Cellular systems send a one-bit command each slot, "up by 1 dB" or "down by 1 dB", which moves the power toward the target in dB with a fixed step. This is a quantized form of the same loop; it oscillates around the target by one step.
- **Faster solves.** A [Gauss-Seidel](/gauss-seidel-method/) order, where each link uses the newest powers of the others, converges at least as fast for nonnegative $F$. It needs a fixed order of updates.

## When to use it

Use it when each link has a fixed SINR target, for example a voice call with a fixed rate, and the network has no central controller that knows all gains. It is the classic inner loop of power control in CDMA systems, where the [near-far problem](/near-far-problem/) makes power control necessary. When the goal is the best common SINR, use [max-min SINR power control](/max-min-sinr-power-control/); when the rates themselves are to be chosen, use [power control by geometric programming](/geometric-programming-power-control/) or a [weighted sum rate](/weighted-sum-rate-maximization/) method.

## Pitfalls

- **Infeasible targets.** If $\rho(F) \ge 1$, every link raises its power at each round, and the powers only stop at the hardware limits. A system must check feasibility, for example by watching for links that stay at their limit, and remove a link or lower the targets.
- **Near the edge.** As $\rho(F) \to 1$, the least powers grow like $1/(1 - \rho(F))$ and the number of rounds grows like $1/(1 - \rho(F))$. Targets that are feasible on paper can be too costly in practice.
- **Time-varying gains.** The analysis assumes fixed gains. If the gains change faster than the loop converges, the powers track a moving target with a lag, and the least-power property no longer holds at each moment.
- **Step above 1.** An aggressive gain $\beta > 1$ can diverge for feasible targets. Keep $\beta \le 1$.
- **SINR in dB.** The update is multiplicative in linear units: $p \leftarrow p\, \gamma / \mathrm{SINR}$. In dB it is $p_{dB} \leftarrow p_{dB} + \gamma_{dB} - \mathrm{SINR}_{dB}$; adding the difference in linear units is wrong.

## Implementations

## History

Zander (1992) studied the best common SINR without noise and found it from the Perron eigenvalue of the normalized gain matrix, but his iteration did not fix the absolute power level. Foschini and Miljanic (1993) included the receiver noise, fixed the target SINR, and gave a law that each link can run with only local measurements. They stated it first as a differential equation and then as a difference equation with the step $\beta$, and proved exponentially fast convergence whenever a central controller could meet the targets. Yates (1995) showed that the proof needs only three properties of the map from powers to required powers, and so covered power limits, base station choice and asynchronous updates in one theorem.

## References
