---
title: Simulated annealing returns the best solution it saw, and at a fixed temperature it samples the Boltzmann distribution
proves: [correctness]
status: full
---

We use the pseudocode of the page. $S$ is a finite set, $f : S \to \mathbb{R}$, and $R(i, \cdot)$ is a probability distribution on $N(i)$ with $i \notin N(i)$. We write $x_k$ for the value of $x$ after the iteration for $k$, and $x_0$ for the start.

**Claim 1 (the returned solution).** After the iteration for $k$, $f(best) = \min\{f(x_0), \dots, f(x_k)\}$ and $best \in \{x_0, \dots, x_k\}$.

*Proof.* By induction on $k$. Line L1 gives $best = x_0$, which is the claim for $k = 0$. Assume it for $k - 1$. If line L5 rejects, $x_k = x_{k-1}$, so the minimum does not change and neither does $best$. If line L5 accepts, $x_k = y$, and line L7 sets $best = x_k$ exactly when $f(x_k) < f(best) = \min\{f(x_0), \dots, f(x_{k-1})\}$. In both branches, $f(best)$ becomes $\min(\min\{f(x_0), \dots, f(x_{k-1})\}, f(x_k))$, and $best$ is one of the visited solutions. $\square$

**Claim 2 (the Markov chain).** Given $x_{k-1} = i$, the probability that $x_k = j$ is
$$P_{T_k}(i, j) = R(i, j) \min\left(1, e^{-(f(j) - f(i))/T_k}\right) \quad (j \ne i), \qquad P_{T_k}(i, i) = 1 - \sum_{j \ne i} P_{T_k}(i, j).$$
It depends only on $i$, $j$ and $k$, so $(x_k)$ is a Markov chain, and it is time-homogeneous when $T_k$ is constant.

*Proof.* Line L3 draws $y = j$ with probability $R(i, j)$, using fresh random numbers. Given $y = j$, line L5 accepts with probability 1 if $\Delta = f(j) - f(i) \le 0$. If $\Delta > 0$, it accepts when a fresh uniform $u \in [0, 1)$ satisfies $u < e^{-\Delta/T_k}$, which has probability $e^{-\Delta/T_k} \in (0, 1)$. In both cases the probability is $\min(1, e^{-\Delta/T_k})$. The two draws are independent of the past given $x_{k-1}$, so the product rule gives $P_{T_k}(i, j)$. The solution stays at $i$ exactly when the move is rejected, which gives the diagonal entry. $\square$

**Claim 3 (Boltzmann equilibrium).** Fix $T > 0$ and assume $R(i, j) = R(j, i)$ for all $i, j$. Let $\pi_T(i) = e^{-f(i)/T}/Z_T$ with $Z_T = \sum_{j \in S} e^{-f(j)/T}$. Then $\pi_T(i) P_T(i, j) = \pi_T(j) P_T(j, i)$ for all $i, j$, and $\pi_T P_T = \pi_T$.

*Proof.* For $i = j$ there is nothing to prove. For $i \ne j$, let $a = f(i)$ and $b = f(j)$ and assume $a \le b$ by symmetry of the statement. Then
$$Z_T \pi_T(i) P_T(i, j) = e^{-a/T} R(i, j) e^{-(b - a)/T} = R(i, j) e^{-b/T}, \qquad Z_T \pi_T(j) P_T(j, i) = e^{-b/T} R(j, i) \cdot 1 = R(j, i) e^{-b/T}.$$
These are equal because $R$ is symmetric. Summing the detailed balance equation over $i$ gives $\sum_i \pi_T(i) P_T(i, j) = \pi_T(j) \sum_i P_T(j, i) = \pi_T(j)$, since each row of $P_T$ sums to 1. $\square$

**Claim 4 (convergence at a fixed temperature).** Under the assumptions of Claim 3, assume also that the graph with the edges $\{i, j\}$, $R(i, j) > 0$, is connected and that $f$ is not constant. Then for each start, the distribution of $x_k$ converges to $\pi_T$ as $k \to \infty$.

*Proof.* Irreducibility: if $R(i, j) > 0$ then $P_T(i, j) \ge R(i, j) e^{-|f(j) - f(i)|/T} > 0$, so each edge of the connected graph can be used in both directions. Aperiodicity: since $f$ is not constant and the graph is connected, some edge $\{i, j\}$ has $f(j) > f(i)$. Then $P_T(i, i) \ge R(i, j)(1 - e^{-(f(j) - f(i))/T}) > 0$, so state $i$ has period 1, and in an irreducible chain all states have the same period. A finite irreducible aperiodic chain converges to its unique stationary distribution from each start (the [ergodic theorem](/ergodic-theorem/) for finite chains), and by Claim 3 that distribution is $\pi_T$. $\square$

**Claim 5 (concentration).** Let $S^* = \{i : f(i) = f^*\}$. As $T \to 0^+$, $\pi_T(i) \to 1/|S^*|$ for $i \in S^*$ and $\pi_T(i) \to 0$ otherwise.

*Proof.* Multiply the numerator and the denominator by $e^{f^*/T}$: $\pi_T(i) = e^{-(f(i) - f^*)/T} / \sum_j e^{-(f(j) - f^*)/T}$. Each term $e^{-(f(j) - f^*)/T}$ equals 1 when $j \in S^*$ and tends to 0 when $f(j) > f^*$. The sum has finitely many terms, so it tends to $|S^*|$, and the claim follows. $\square$

**Claim 6 (zero temperature).** If $T_k = 0$ is read as "accept only $\Delta \le 0$", then $f(x_k) \le f(x_{k-1})$.

*Proof.* Line L5 accepts only when $\Delta \le 0$, and a rejection keeps $x$. $\square$

Claims 1 to 6 do not say that a finite run finds a global minimum. That needs a schedule that falls slowly enough, and the exact condition is the theorem of Hajek on the page [convergence of simulated annealing](/simulated-annealing-convergence/).
