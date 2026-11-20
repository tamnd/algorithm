---
title: Analog Monte Carlo gives unbiased estimates of the transport solution
proves: [correctness]
status: full
---

We assume exact arithmetic and exact independent uniform random numbers. The phase space is $P = \{(x, \mu) : 0 \le x \le L,\ -1 \le \mu \le 1\}$, the medium is uniform with $\Sigma_t > 0$, $0 \le \Sigma_s \le \Sigma_t$ and $c = \Sigma_s / \Sigma_t$, and scattering is isotropic. The case $L = \infty$ is the infinite medium with no faces.

**The random path.** One history of ANALOG-HISTORY is a sequence of collision points $(x_1, \mu_1), (x_2, \mu_2), \ldots$, where $\mu_j$ is the direction before the collision, ended by absorption or leakage. Given the state $(x_{j}, \mu')$ after collision $j$ (or at the source, $j = 0$), the next collision is at $x_{j+1} = x_j + \mu' S$, where $S$ has the density $\Sigma_t e^{-\Sigma_t s}$ by [free-flight sampling](/free-flight-sampling/), if this point is inside the slab; otherwise the particle leaks. After a collision, line L8 ends the history with probability $1 - c$, and line L9 draws a new $\mu'$ with density $1/2$ on $[-1, 1]$. Write $K$ for the transition kernel from one collision to the next one in the slab:

$$K(x, x') = c \int_{-1}^{1} \frac{1}{2}\, \Sigma_t e^{-\Sigma_t (x' - x)/\mu'}\, \frac{\mathbf{1}[(x' - x)/\mu' > 0]}{|\mu'|}\, d\mu' = \frac{c\, \Sigma_t}{2} E_1(\Sigma_t |x' - x|),$$

the density of the next collision at $x'$ given a collision at $x$. Here $E_1(z) = \int_1^\infty e^{-zt}/t\, dt$, and the factor $1/|\mu'|$ turns a path length into a distance in $x$. The density $F_1$ of the first collision is the density of the source flight in the same way.

**Lemma 1 (termination).** If $c < 1$, or if $L < \infty$, the history ends with probability 1, and the number of collisions $k$ has finite moments of every order.

*Proof.* If $c < 1$, each collision ends the history with probability $1 - c$, independently of the past, so $P(k > n) \le c^n$. If $L < \infty$ and $c = 1$, a particle at any point $x$ of the slab that scatters into $\mu' \in [1/2, 1]$ leaves through $x = L$ on the next flight with probability at least $e^{-2 \Sigma_t L}$, because the path to the face is at most $2L$. The direction has probability $1/4$, so each collision is the last one with probability at least $q = e^{-2 \Sigma_t L}/4 > 0$, and $P(k > n) \le (1 - q)^n$. In both cases the tail is geometric, so all moments are finite. $\square$

**Lemma 2 (the collision density).** Let $F_k$ be the density of the $k$-th collision point (zero if the history ended before), so $F_{k+1}(x') = \int F_k(x) K(x, x')\, dx$. The expected number of collisions in a set $B$ is $\int_B F(x)\, dx$ with $F = \sum_{k \ge 1} F_k$, and $F$ solves the integral equation

$$F(x') = F_1(x') + \int_0^L F(x) K(x, x')\, dx.$$

*Proof.* The number of collisions in $B$ is $\sum_{k \ge 1} \mathbf{1}[\text{collision } k \text{ exists and lies in } B]$. Its expectation is $\sum_k \int_B F_k$ by monotone convergence, and the sum is finite by Lemma 1. Summing the recursion over $k$ gives the equation. $\square$

The integral equation of Lemma 2 is the integral form of the [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/) for the collision density $F = \Sigma_t \phi$ in slab geometry, and the sum $F = \sum_k F_k$ is its [Neumann series](/neumann-series/). Lemma 1 shows that the series converges in the sense of total mass: $\int F = E[k] < \infty$. So the expected collision density of the analog game is the solution of the transport equation, which is the link between the game and the equation.

**Theorem (unbiased counts).** For each event $e \in \{\text{TRANSMITTED}, \text{REFLECTED}, \text{ABSORBED}\}$, the estimate $p_e = \text{count}[e]/N$ of line L12 has $E[p_e] = P(e)$ and variance $P(e)(1 - P(e))/N$, the mean of $k$ is an unbiased estimate of $E[k]$, and $p_T + p_R + p_A = 1$ exactly.

*Proof.* Line L10 runs $N$ independent histories with fresh random numbers, so the indicators $\mathbf{1}[e_n = e]$ are independent Bernoulli variables with mean $P(e)$. Their mean has expectation $P(e)$ and variance $P(e)(1 - P(e))/N$. The same argument holds for $k$, which has a finite variance by Lemma 1. By Lemma 1 every history ends in exactly one of the three events, so the counts add up to $N$. $\blacksquare$

**The infinite medium.** With $L = \infty$, no history leaks, and each collision is the last one with probability $1 - c$ independently. So $P(k = n) = c^{n-1}(1 - c)$ for $n \ge 1$, $E[k] = 1/(1 - c)$ and $\mathrm{Var}[k] = c/(1 - c)^2$. With a uniform source of $Q$ particles per unit volume and time, the collision rate density is $Q E[k] = Q/(1 - c)$, and $\phi = F/\Sigma_t = Q / (\Sigma_t (1 - c)) = Q/\Sigma_a$, which is the check value of the page.

**The pure absorber.** With $c = 0$ the history is one flight, and the beam is transmitted if and only if $S > L$, which has probability $e^{-\Sigma_t L}$ by free-flight sampling. With scattering, the uncollided transmission is the same event and has the same probability.

**The error bar.** The standard error of line L12 uses the sample variance. By the [central limit theorem](/central-limit-theorem/), $(p_e - P(e))/s_e$ tends in law to the standard normal law as $N \to \infty$, so $p_e \pm 2 s_e$ covers $P(e)$ with a probability that tends to about 0.95. This is a statement about the limit $N \to \infty$; for a small $N$ or a rare event it can be far off.
