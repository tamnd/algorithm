---
tag: 216ZVB
kind: theorem
slug: simulated-annealing-convergence
name: Convergence of simulated annealing
aliases:
- Hajek's theorem
- Hajek's cooling theorem
- logarithmic cooling theorem
area: optimization/metaheuristics
level: advanced
summary: Simulated annealing is at a global minimum with probability tending to 1 if and only if the sum of exp(-d*/T_k) diverges, d* being the deepest trap. For T_k = c/log(k+1) this means c ≥ d*.
prereqs: [simulated-annealing, metropolis-criterion, markov-chain, stationary-distribution]
see_also: [cooling-schedule, ergodic-theorem, total-variation-distance, mixing-time, detailed-balance, local-optimum, global-optimization]
sources:
  - paper: doi:10.1287/moor.13.2.311
    title: Bruce Hajek, Cooling schedules for optimal annealing, Mathematics of Operations Research 13(2), 1988
    locator: pages 311 to 329 (the definitions of reachability, weak reversibility and depth, and Theorem 1)
  - paper: doi:10.1109/TPAMI.1984.4767596
    title: Stuart Geman and Donald Geman, Stochastic relaxation, Gibbs distributions, and the Bayesian restoration of images, IEEE Transactions on Pattern Analysis and Machine Intelligence 6(6), 1984
    locator: pages 721 to 741 (the annealing theorem with a logarithmic schedule and a constant that grows with the size of the problem)
  - paper: doi:10.2307/1427186
    title: Debasis Mitra, Fabio Romeo and Alberto Sangiovanni-Vincentelli, Convergence and finite-time behavior of simulated annealing, Advances in Applied Probability 18(3), 1986
    locator: pages 747 to 771 (weak and strong ergodicity of the inhomogeneous chain under a logarithmic schedule)
  - book: doi:10.1007/978-1-4757-3124-8
    title: Pierre Brémaud, Markov Chains, Gibbs Fields, Monte Carlo Simulation, and Queues, Springer, 1999
    locator: Chapter 6 (Dobrushin's ergodic coefficient and the ergodicity of inhomogeneous chains) and Chapter 7 (simulated annealing)
---

Hajek's theorem gives the exact condition under which [simulated annealing](/simulated-annealing/) on a finite set finds a global minimum in the limit: the probability that the current state is a global minimum tends to 1 if and only if $\sum_k e^{-d^*/T_k} = \infty$, where $d^*$ is the depth of the deepest local minimum that is not global. For the schedule $T_k = c/\ln(k+1)$ this holds if and only if $c \ge d^*$. The theorem is a statement about the distribution of the walk in the limit. It does not bound the number of steps, and the schedules that people use in practice fall much faster than it allows.

## Statement

**Setting.** $S$ is a finite set, $V : S \to \mathbb{R}$ is the energy to minimize, and $S^* = \arg\min V$. Each state $i$ has a set of neighbors $N(i) \subseteq S \setminus \{i\}$ and a proposal distribution $R(i, \cdot)$ with $R(i, j) > 0$ if and only if $j \in N(i)$. Given a schedule $T_1 \ge T_2 \ge \dots > 0$ with $T_k \to 0$, the chain $(X_k)$ moves from $i$ to $j \in N(i)$ with probability $R(i, j) \exp(-\max(V(j) - V(i), 0)/T_k)$ at step $k$, and stays at $i$ otherwise. This is the [Metropolis criterion](/metropolis-criterion/).

**Definitions.** A state $j$ is *reachable at height $E$* from $i$ if there is a path $i = i_0, i_1, \dots, i_p = j$ with $i_{q+1} \in N(i_q)$ and $V(i_q) \le E$ for all $q$. The structure is *irreducible* if each state is reachable from each other state at some height, and *weakly reversible* if for all $E$, $i$ is reachable from $j$ at height $E$ exactly when $j$ is reachable from $i$ at height $E$. A symmetric neighborhood, $j \in N(i) \iff i \in N(j)$, is weakly reversible. A state $i$ is a *local minimum* if no state $j$ with $V(j) < V(i)$ is reachable from $i$ at height $V(i)$. The *depth* $d(i)$ of a local minimum $i \notin S^*$ is the smallest $E > 0$ such that some $j$ with $V(j) < V(i)$ is reachable from $i$ at height $V(i) + E$. Let $d^*$ be the largest depth of a local minimum not in $S^*$, and $d^* = 0$ if there is none.

**Theorem (Hajek 1988).** Assume irreducibility and weak reversibility. Then

$$\lim_{k \to \infty} \Pr[X_k \in S^*] = 1 \quad \iff \quad \sum_{k=1}^{\infty} e^{-d^*/T_k} = \infty.$$

**Corollary.** For $T_k = c/\ln(k+1)$ with $c > 0$, the walk converges to $S^*$ in probability if and only if $c \ge d^*$.

The proof below proves the corollary from the theorem, the necessity of the condition when the deepest trap is a single state, and the sufficiency of the stronger condition $\sum_k e^{-D\Delta/T_k} = \infty$ for a symmetric proposal, where $D$ and $\Delta$ are defined there. The sharp constant $d^*$ in both directions is proved in Hajek's paper.

## In plain words

A trap is a valley that is not the deepest one. Its depth is how far the walk must climb to get out of it toward lower ground. At a given temperature, the walk climbs out of a trap only rarely, and the deeper the trap, the rarer it is.

If the temperature falls too fast, there is a real chance that the walk sits in a deep trap and never climbs out, so the method can fail forever. If it falls slowly enough, the walk always gets another chance, and in the end it settles in the deepest valley. Hajek found the exact border between the two cases. Only the deepest trap matters, and the border is a temperature that falls like one over the logarithm of the step number. That is extremely slow.

## Proof

**The corollary.** With $T_k = c/\ln(k+1)$, $e^{-d^*/T_k} = (k+1)^{-d^*/c}$. The series $\sum_k (k+1)^{-p}$ diverges if and only if $p \le 1$, that is, $c \ge d^*$. If $d^* = 0$, every term is 1 and the series diverges for each $c$.

**Necessity when the trap is one state.** Let $i \notin S^*$ be a local minimum with $d(i) = d^*$, and assume that every neighbor $j$ of $i$ has $V(j) \ge V(i) + d^*$. Assume $\sum_k e^{-d^*/T_k} < \infty$. At step $k$, the chain leaves $i$ with probability $\sum_{j \in N(i)} R(i, j) e^{-(V(j) - V(i))/T_k} \le e^{-d^*/T_k} =: p_k$. Each $p_k$ is in $(0, 1)$, and a product $\prod_k (1 - p_k)$ with $0 \le p_k < 1$ and $\sum_k p_k < \infty$ is positive, so $b = \prod_{k \ge 1} (1 - p_k) > 0$. By irreducibility there is a path $x_0 = i_0, i_1, \dots, i_\ell = i$ from the start to $i$. At step $q$ the chain moves from $i_{q-1}$ to $i_q$ with probability at least $R(i_{q-1}, i_q) e^{-|V(i_q) - V(i_{q-1})|/T_q} > 0$, so $a = \Pr[X_\ell = i] > 0$. By the Markov property, $\Pr[X_k = i \text{ for all } k \ge \ell] \ge a \prod_{k > \ell} (1 - p_k) \ge a b > 0$. So $\Pr[X_k \in S^*] \le 1 - ab$ for all $k \ge \ell$, and the limit is not 1.

**Sufficiency with a weaker constant.** Assume that $R$ is symmetric, the neighborhood graph is connected and $V$ is not constant. Let $r = \min\{R(i, j) : R(i, j) > 0\}$, $\Delta = \max\{|V(j) - V(i)| : j \in N(i)\}$, and pick an edge $\{z, w\}$ with $V(w) > V(z)$. Let $D$ be the largest graph distance from a state to $z$. We prove: if $\sum_k e^{-D\Delta/T_k} = \infty$, then $\Pr[X_k \in S^*] \to 1$.

*Step 1, a contraction.* For a stochastic matrix $Q$ let $\delta(Q) = \frac12 \max_{i, i'} \sum_l |Q(i, l) - Q(i', l)|$. For a signed vector $\sigma$ with $\sum_l \sigma(l) = 0$, write $\sigma = \sigma^+ - \sigma^-$ with both parts of mass $s = \|\sigma\|_1/2$. Then $\sigma Q = s^{-1} \sum_{i, i'} \sigma^+(i) \sigma^-(i') (Q(i, \cdot) - Q(i', \cdot))$, so $\|\sigma Q\|_1 \le s^{-1} \cdot s^2 \cdot 2\delta(Q) = \delta(Q) \|\sigma\|_1$. Also $\|\sigma Q\|_1 \le \|\sigma\|_1$ for every $\sigma$. Since $\frac12 \sum_l |a_l - b_l| = 1 - \sum_l \min(a_l, b_l)$ for two probability vectors, $\delta(Q) \le 1 - \min_i Q(i, z)$.

*Step 2, a lower bound for $D$ steps.* At every step, $P_{T}(z, z) \ge R(z, w)(1 - e^{-(V(w) - V(z))/T}) \ge \rho := r(1 - e^{-(V(w) - V(z))/T_1})$, because $T \le T_1$. A move along an edge has probability at least $r e^{-\Delta/T}$. From each $i$, follow a shortest path to $z$ and then stay at $z$, for $D$ steps in total. With $Q_k = P_{T_{k+1}} \cdots P_{T_{k+D}}$ and the schedule nonincreasing, $Q_k(i, z) \ge \rho^D e^{-D\Delta/T_{k+D}}$, since $\rho \le r$. So $\delta(Q_k) \le 1 - \rho^D e^{-D\Delta/T_{k+D}}$.

*Step 3, weak ergodicity.* For two start distributions at time $m$ and $n = m + qD$, Step 1 applied block by block and $1 - x \le e^{-x}$ give $\|\mu P_{m+1} \cdots P_n - \nu P_{m+1} \cdots P_n\|_1 \le 2 \exp(-\rho^D \sum_{t=1}^{q} e^{-D\Delta/T_{m+tD}})$. The terms $e^{-D\Delta/T_k}$ do not increase in $k$, so $\sum_t e^{-D\Delta/T_{m+tD}} \ge \frac1D \sum_{k > m+D} e^{-D\Delta/T_k} = \infty$. Hence the bound tends to 0 as $q \to \infty$, for each $m$. Steps that do not fill a block only contract further.

*Step 4, the moving equilibrium.* Let $\pi_k$ be the Boltzmann distribution at $T_k$, which is stationary for $P_{T_k}$ (detailed balance, see the [Metropolis criterion](/metropolis-criterion/)). With $\beta = 1/T$ and $a = V - \min V$, $\frac{d}{d\beta} \ln \pi(i) = \mathbb{E}_\pi[a] - a(i)$, and $\frac{d}{d\beta}\mathbb{E}_\pi[a] = -\mathrm{Var}_\pi(a) \le 0$. So $\ln \pi(i)$ has a derivative that does not increase, and $\pi(i)$ rises and then falls at most once as $\beta$ grows. The sequence $\pi_k(i)$ is therefore a monotone sequence followed by another, so $\sum_k |\pi_{k+1}(i) - \pi_k(i)| \le 2$, and $\sum_k \|\pi_{k+1} - \pi_k\|_1 \le 2|S|$.

*Step 5, the limit.* With $\mu_n$ the distribution of $X_n$ and $m < n$, the identity $\pi_{j-1} P_{T_j} - \pi_j = (\pi_{j-1} - \pi_j) P_{T_j}$ telescopes to $\pi_m P_{T_{m+1}} \cdots P_{T_n} - \pi_n = \sum_{j=m+1}^{n} (\pi_{j-1} - \pi_j) P_{T_j} \cdots P_{T_n}$. So
$$\|\mu_n - \pi_n\|_1 \le \|(\mu_m - \pi_m) P_{T_{m+1}} \cdots P_{T_n}\|_1 + \sum_{j > m} \|\pi_{j-1} - \pi_j\|_1.$$
Given $\varepsilon > 0$, Step 4 gives $m$ with the sum below $\varepsilon$, and Step 3 gives $n_0$ with the first term below $\varepsilon$ for $n \ge n_0$. So $\|\mu_n - \pi_n\|_1 \to 0$. Since $T_n \to 0$, $\pi_n$ tends to the uniform distribution on $S^*$ (the concentration claim on the [simulated annealing](/simulated-annealing/) page). Hence $\Pr[X_n \in S^*] = \mu_n(S^*) \to 1$. $\square$

For $T_k = c/\ln(k+1)$ this argument needs $c \ge D\Delta$. Step 2 pays the largest step $\Delta$ on each of $D$ edges. Hajek's proof works instead with the cups of the landscape, the sets of states reachable from a state below a given height, and bounds the probability of leaving each cup in terms of its depth. This gives the sharp condition with $d^*$ in both directions, for cups of any size.

## Consequences

- **The schedule $T_k = c/\ln(k+1)$ with $c \ge d^*$ is enough, and nothing faster of this form is.** For the 8-state cycle of the [simulated annealing](/simulated-annealing/) page, with $V = (3, 1, 4, 2, 5, 0, 3, 6)$ and the two cycle neighbors, the local minima are state 1 with depth 4 and state 3 with depth 2, so $d^* = 4$. The crude constant of the proof is $D\Delta = 4 \cdot 5 = 20$.
- **Exact probabilities on this cycle.** Multiplying the transition matrices from the start state 0 gives the probability of the global minimum, state 5:

| $c$ | $k = 10$ | $k = 100$ | $k = 1000$ | $k = 10^4$ | $k = 10^5$ |
|---|---|---|---|---|---|
| 1 | 0.037 | 0.037 | 0.037 | 0.037 | 0.037 |
| 2 | 0.117 | 0.136 | 0.139 | 0.139 | 0.140 |
| 4 | 0.195 | 0.419 | 0.593 | 0.720 | 0.812 |
| 8 | 0.195 | 0.401 | 0.552 | 0.668 | 0.755 |

  With $c = 1$ and $c = 2$ the probability stops below 1, and the walk stays in the trap at state 1 (its probability is 0.951 for $c = 1$ and still rising, 0.833, for $c = 2$ at $k = 10^5$). With $c = 4$ the probability tends to 1, but it is only 0.81 after $10^5$ steps. A larger $c$ is also safe but slower.
- **The set of global minima, not one of them.** The theorem gives $\Pr[X_k \in S^*] \to 1$. It does not say that $X_k$ settles at one state, and it is about the current state, not the best state seen.
- **The best state seen.** Since $\Pr[X_k \in S^*] \to 1$, the probability that the walk has visited $S^*$ by step $k$ also tends to 1. A random search or a restarted local search has the same property, so this alone does not favor annealing.
- **Exponential time.** Reaching temperature $T$ takes $e^{c/T} - 1$ steps. The theorem gives no polynomial bound, and none holds in general for NP-hard problems.

## Tightness

The constant $d^*$ cannot be lowered: by the necessity part, if $c < d^*$ then $\sum_k (k+1)^{-d^*/c} < \infty$, and the walk stays in a trap of depth $d^*$ forever with positive probability. On the cycle above this is the row $c = 2$. Only the deepest trap matters, not a shallower one: with $c = 2$ the probability of state 3 (depth 2) falls from 0.096 at $k = 100$ to 0.028 at $k = 10^5$, since $\sum_k (k+1)^{-1} = \infty$, while the probability of state 1 (depth 4) keeps growing.

The sufficiency constant $D\Delta$ of the proof is not tight: it is 20 on the cycle, while $d^* = 4$ suffices. The older results of Geman and Geman (1984) and of Mitra, Romeo and Sangiovanni-Vincentelli (1986) had constants of this crude kind, which grow with the size of the problem.

## History

Kirkpatrick, Gelatt and Vecchi proposed simulated annealing in 1983 without a proof of convergence. Geman and Geman proved in 1984, for Gibbs samplers on images, that a schedule $c/\log k$ with a large enough constant converges to the global minima. Mitra, Romeo and Sangiovanni-Vincentelli gave a proof by the ergodicity of inhomogeneous chains in 1986. Hajek found the exact constant $d^*$, with the necessary and sufficient condition, in 1988.

## References
