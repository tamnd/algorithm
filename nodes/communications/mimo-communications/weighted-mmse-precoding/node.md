---
tag: 9QVSR3
kind: algorithm
slug: weighted-mmse-precoding
name: Weighted MMSE precoding
aliases:
- WMMSE algorithm
area: communications/mimo-communications
level: advanced
summary: Maximizes the weighted sum rate of a MIMO broadcast or interference channel by alternating updates of an equivalent MSE problem.
model: real-ram
complexity:
  vars: {T: the number of iterations, M: the number of base station antennas, K: the number of users, B: the number of Newton steps for the multiplier}
  time: {worst: O(T (K M^2 + K^2 M + B M^2 (M + K)))}
  space: {extra: O(M^2 + M K)}
properties: {deterministic: true, linear: true, iterative: true, monotone: true, needs_channel_at_transmitter: true, global_optimum: false}
history:
  year: 2011
  people: [Qingjiang Shi, Meisam Razaviyayn, Zhi-Quan Luo, Chen He, Søren Skovgaard Christensen, Rajiv Agarwal, Elisabeth de Carvalho, John M. Cioffi]
  note: "Christensen, Agarwal, de Carvalho and Cioffi used the link between weighted sum rate and weighted MMSE for the MIMO broadcast channel in 2008, and Shi, Razaviyayn, Luo and He gave the WMMSE algorithm for the interfering broadcast channel in 2011."
prereqs: [weighted-sum-rate-maximization, regularized-zero-forcing-precoding, kkt-conditions, coordinate-descent]
see_also: [zero-forcing-precoding, block-diagonalization, maximum-ratio-transmission, water-filling-power-allocation, dirty-paper-coding, mmse-mimo-detector, geometric-programming-power-control, proportional-fair-scheduling]
sources:
  - paper: doi:10.1109/TSP.2011.2147784
    title: "Qingjiang Shi, Meisam Razaviyayn, Zhi-Quan Luo and Chen He, An iteratively weighted MMSE approach to distributed sum-utility maximization for a MIMO interfering broadcast channel, IEEE Transactions on Signal Processing 59(9), 4331-4340, 2011"
    locator: the equivalence between weighted sum rate maximization and weighted MSE minimization, the WMMSE algorithm, and its convergence to stationary points
  - paper: doi:10.1109/T-WC.2008.070851
    title: "Søren Skovgaard Christensen, Rajiv Agarwal, Elisabeth de Carvalho and John M. Cioffi, Weighted sum-rate maximization using weighted MMSE for MIMO-BC beamforming design, IEEE Transactions on Wireless Communications 7(12), 4792-4799, 2008"
    locator: the relation between the weighted sum rate and the weighted MMSE of the MIMO broadcast channel, and the iterative precoder design
  - paper: doi:10.1109/MSP.2014.2312183
    title: "Emil Björnson, Mats Bengtsson and Björn Ottersten, Optimal multiuser transmit beamforming: a difficult problem with a simple solution structure, IEEE Signal Processing Magazine 31(4), 142-148, 2014"
    locator: the structure of the optimal beams as regularized inverses with one nonnegative parameter per user, and the difficulty of the weighted sum rate problem
---

Weighted MMSE (WMMSE) precoding finds the precoders of a multiuser downlink that maximize a weighted sum rate, $\sum_k a_k \log_2(1 + \mathrm{SINR}_k)$. The rate problem is not convex, but it has the same solutions as a weighted mean square error problem with extra variables, and that problem is easy in each block of variables. WMMSE updates the receive gains, the MSE weights and the precoders in turn, and the rate never decreases. [Regularized zero-forcing precoding](/regularized-zero-forcing-precoding/) is a closed form with one regularization for all users and no target. WMMSE has the same kind of regularized inverse in each step, but it iterates, adapts a weight for each user, and aims at any weighted sum rate. The cost is several iterations, and the result is a stationary point, which is not always the global optimum.

## In plain words

A base station sends to several phones at once, and each phone has a priority. The base station wants the largest total speed, where faster speed for a high priority phone counts more. The direct problem is hard. So the base station pretends each phone has a simple receiver and asks how much error that receiver makes. It then repeats three easy steps: tune each receiver for the current beams, give each phone a weight from its error, and choose the beams that make the weighted errors smallest with the power it has. Each round makes the total speed better or keeps it the same. After some rounds the beams stop changing. The answer is good, but a different start can sometimes give a better one.

## The problem

User $k$ has one antenna and receives $y_k = h_k^H x + w_k$, with $h_k \in \mathbb{C}^M$ known at the base station and $w_k \sim \mathcal{CN}(0, N_0)$. The base station sends $x = \sum_k v_k s_k$ with independent unit-energy symbols $s_k$ and the power constraint $\sum_k \|v_k\|^2 \le P$. With

$$\mathrm{SINR}_k = \frac{|h_k^H v_k|^2}{\sum_{j \ne k} |h_k^H v_j|^2 + N_0},$$

the goal is to maximize $R = \sum_k a_k \log_2(1 + \mathrm{SINR}_k)$ for given weights $a_k > 0$. This is [weighted sum rate maximization](/weighted-sum-rate-maximization/) for the multiple-input single-output (MISO) downlink. The problem is NP-hard in general. The same method works for users with several antennas and for several base stations, with matrices in place of the scalars $u_k$ and $w_k$; the code on this page covers the MISO case.

## The algorithm

User $k$ estimates $s_k$ as $\bar u_k y_k$ with the mean square error $e_k = E|\bar u_k y_k - s_k|^2$. WMMSE minimizes $\sum_k a_k (w_k e_k - \ln w_k)$ over the gains $u_k$, the weights $w_k > 0$ and the precoders, one block at a time.

```pseudo id=main
WMMSE(h₁, ..., h_K, a, P, N0)
L1  V ← a start with Σ‖v_k‖² ≤ P              ▷ for example the beams h_k, scaled to the power P
    repeat
        for each user k:
            T_k ← Σ_j |h_kᴴ v_j|² + N0
L2          u_k ← h_kᴴ v_k / T_k               ▷ the MMSE receive gain
L3          w_k ← 1 / (1 - ū_k h_kᴴ v_k)        ▷ the inverse of the smallest MSE
L4      A ← Σ_k a_k w_k |u_k|² h_k h_kᴴ;  b_k ← a_k w_k u_k h_k
L5      μ ← the smallest μ ≥ 0 with Σ_k ‖(A + μI)⁻¹ b_k‖² ≤ P;  v_k ← (A + μI)⁻¹ b_k
L6      R ← Σ_k a_k log₂(1 + SINR_k)
L7  until R grows by less than a tolerance
    return V
```

Line L2 is the scalar [MMSE receiver](/mmse-mimo-detector/) for the current beams. Line L3 sets the weight to $1/e_k = 1 + \mathrm{SINR}_k$. Lines L4 and L5 solve a convex quadratic problem with one power constraint, whose [KKT conditions](/kkt-conditions/) give a regularized inverse with a Lagrange multiplier $\mu$. The power decreases in $\mu$, so the implementation finds $\mu$ by Newton steps inside a bracket. Each round is one pass of [block coordinate descent](/coordinate-descent/).

## Example

Take three users with orthogonal channels $h_1 = 2 e_1$, $h_2 = e_2$ and $h_3 = 0.5 e_3$, so the gains are $g = (4, 1, 1/4)$. Let the weights be $a = (1, 2, 1.5)$, with $P = 3$ and $N_0 = 1$. There is no interference, so the best powers are the weighted water-filling $p_k = (a_k / \lambda - 1/g_k)^+$ with $\sum_k p_k = 3$. With users 1 and 2 active, $3/\lambda - 1/4 - 1 = 3$ gives $1/\lambda = 17/12$, so $p_1 = 7/6$ and $p_2 = 11/6$. User 3 gets no power, because $a_3 g_3 = 0.375$ is below $\lambda = 12/17$. The best weighted sum rate is $\log_2(17/3) + 2 \log_2(17/6) = 5.508$ bits per channel use.

WMMSE starts with the beams $h_k$ scaled to the power 3.

| iteration | $p_1$ | $p_2$ | $p_3$ | weighted sum rate |
|---|---|---|---|---|
| 0 | 2.286 | 0.571 | 0.143 | 4.722 |
| 1 | 1.924 | 1.042 | 0.034 | 5.198 |
| 2 | 1.669 | 1.323 | 0.008 | 5.376 |
| 3 | 1.500 | 1.498 | 0.002 | 5.450 |
| 10 | 1.186 | 1.814 | 0.000 | 5.505 |
| 35 | 1.167 | 1.833 | 0.000 | 5.508 |

The rate grows in every row and the powers move toward $(7/6, 11/6, 0)$. Equal powers of 1 give only 4.805. With equal weights, water-filling would give $p_1 = 1.875$ and $p_2 = 1.125$; the weight 2 of user 2 moves power toward that user.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Lemma 1 shows that line L2 minimizes the MSE and that the minimum is $1/(1 + \mathrm{SINR}_k)$. Lemma 2 shows that line L3 is the best weight. Together they give $\min_{u, w} G = \sum_k a_k - \ln 2 \cdot R$, so the MSE problem and the rate problem have the same solutions. Lemma 3 shows that lines L4 and L5 give the best precoders for fixed $u$ and $w$. Theorem 1 shows that each iteration keeps the power at most $P$ and never decreases $R$, so the rates converge. Theorem 2 shows that every fixed point satisfies the KKT conditions of the weighted sum rate problem. Theorem 3 shows that with one user WMMSE gives maximum ratio transmission, and Theorem 4 shows that with orthogonal channels the optimum is weighted water-filling, as in the example.

## Complexity

One iteration computes the $K \times K$ matrix of values $h_k^H v_j$ in $O(K^2 M)$ and the matrix $A$ in $O(K M^2)$. Each Newton step of line L5 solves a linear system with $M$ unknowns and $K$ right sides in $O(M^3 + M^2 K)$, and $B$ steps are needed. With $T$ iterations, the time is $O(T (K M^2 + K^2 M + B M^2 (M + K)))$. An eigendecomposition of $A$ once per iteration makes each later evaluation of the power cheaper. The extra space is $O(M^2)$ for $A$ and $O(M K)$ for the precoders. The number of iterations depends on the channel and the start; it is often tens, but there is no small bound.

## Properties

- **Monotone.** The weighted sum rate never decreases from one iteration to the next (theorem).
- **Feasible.** Each iterate meets the power constraint, and the power is exactly $P$ whenever $\mu > 0$ (theorem).
- **Stationary limit.** Every fixed point is a KKT point of the weighted sum rate problem (theorem).
- **Not always global.** The problem is not convex, and WMMSE can stop at a local optimum.
- **Regularized inverse structure.** Each precoder has the form $(A + \mu I)^{-1} h_k$ times a scalar, the same structure as the optimal beams.
- **Exact special cases.** One user gives maximum ratio transmission, and orthogonal channels give weighted water-filling (theorems).
- **Linear.** The output is a linear precoder, so the cost per symbol is $O(M K)$.

## Variants and improvements

- **Users with several antennas.** Replace $u_k$ by a receive matrix and $w_k$ by a weight matrix; the steps stay closed forms, and the method then optimizes the rate of each MIMO link.
- **Interfering broadcast channel.** Shi, Razaviyayn, Luo and He apply the same steps to several base stations, each with its own power constraint, and each base station can compute its own update.
- **Other utilities.** A change of the weight update handles proportional fairness, the harmonic mean rate and other utilities of the rates.
- **Scheduling weights.** In a scheduler, the weights $a_k$ come from queue lengths or from average rates, as in [proportional fair scheduling](/proportional-fair-scheduling/).
- **Several starts.** Run from the maximum ratio transmission beams, from the zero-forcing beams and from random beams, and keep the best result.
- **Linear alternatives.** [Zero-forcing](/zero-forcing-precoding/) and [block diagonalization](/block-diagonalization/) are cheaper and close to WMMSE at high SNR; [dirty paper coding](/dirty-paper-coding/) is the nonlinear scheme that reaches the capacity of the broadcast channel.

## When to use it

Use WMMSE when the base station has good channel knowledge, the users have different priorities, and there is time for a few tens of matrix inversions per channel update. It is a standard reference design for the weighted sum rate of the MIMO downlink and for coordinated base stations. When all weights are equal and the SNR is high, [regularized zero-forcing precoding](/regularized-zero-forcing-precoding/) is close and much cheaper. In massive MIMO with many more antennas than users, the gain over regularized zero forcing is often small.

## Pitfalls

- **Local optima.** On one random two-user channel with the weights 1 and 1.915 and $P = 13.33$, the default start converges to a point that serves both users with the weighted sum rate 9.660. Serving only user 2 by maximum ratio transmission gives 10.418. Try several starts.
- **A zero start.** If $v_k = 0$, then $u_k = 0$ and user $k$ stays off forever. Start with all beams nonzero.
- **Singular $A$.** When $K < M$, $A$ has a null space, and $\mu = 0$ is not defined. Use the smallest positive $\mu$, or the minimum norm solution.
- **The stopping rule.** The rate can grow slowly for many iterations. Stop on a relative change, and also limit the number of iterations.
- **Stale channel.** The steps use $h_k$ exactly; with old channel estimates the computed SINR values are too high.

## Implementations

## History

The link between rate and MSE is old: for a Gaussian channel, the rate is $-\log_2$ of the smallest MSE of the symbol. Christensen, Agarwal, de Carvalho and Cioffi (2008) used this link to design the precoders of the MIMO broadcast channel by an iteration over the receivers, the MSE weights and the precoders. Shi, Razaviyayn, Luo and He (2011) gave the general WMMSE algorithm for the MIMO interfering broadcast channel, showed that the weighted sum rate problem and the weighted MSE problem have the same optimal precoders, and showed that the iteration converges to stationary points of the weighted sum rate. Björnson, Bengtsson and Ottersten (2014) described the structure of the optimal beams as regularized inverses with one parameter per user, and why the weighted sum rate problem is hard.

## References
