---
title: Kinetic Monte Carlo samples the Markov jump process exactly
proves: [correctness]
status: full
---

We assume exact arithmetic and exact uniform random numbers $u_1$ in $[0, 1)$ and $u_2$ in $(0, 1]$, independent of each other and of all earlier draws. A Markov jump process with rates $k_j(x)$ and targets $y_j(x)$ is the process that, in state $x$, waits a time $\tau$ with $P(\tau > s) = e^{-R(x) s}$, $R(x) = \sum_j k_j(x)$, then jumps to $y_j(x)$ with probability $k_j(x) / R(x)$, independently of $\tau$, and then starts afresh from the new state. This is the standard construction of the process from its jump chain and its holding times; it is equivalent to the infinitesimal description $P(\text{event } j \text{ in } [t, t + dt)) = k_j\, dt + o(dt)$.

**Lemma 1 (the race of exponential clocks).** Let $T_1, \ldots, T_M$ be independent with $P(T_j > s) = e^{-k_j s}$, $k_j > 0$. Let $T = \min_j T_j$ and let $J$ be the index of the minimum. Then $P(T > s, J = j) = (k_j / R) e^{-R s}$ for all $s \ge 0$, with $R = \sum_j k_j$. So $T$ is exponential with rate $R$, $P(J = j) = k_j / R$, and $T$ and $J$ are independent.

*Proof.* The index of the minimum is unique with probability 1, because the laws have densities. Condition on $T_j = r$:

$$P(T > s, J = j) = \int_s^\infty k_j e^{-k_j r} \prod_{i \ne j} P(T_i > r)\, dr = \int_s^\infty k_j e^{-R r}\, dr = \frac{k_j}{R} e^{-R s}.$$

Summing over $j$ gives $P(T > s) = e^{-Rs}$, and $s = 0$ gives $P(J = j) = k_j / R$. The joint law is the product of the two marginal laws, so $T$ and $J$ are independent. $\square$

This is the reason why the two descriptions of the process agree: if every event has its own exponential clock, the first one to ring has the law of the construction above.

**Lemma 2 (one step).** In state $x$ with $R = R(x) > 0$, lines L6, L7 and L10 return $\Delta t$ and $j$ with $P(\Delta t > s, j) = (k_j / R) e^{-R s}$.

*Proof.* Line L7 sets $\Delta t = -\ln(u_2) / R$. For $s \ge 0$, $\Delta t > s$ holds if and only if $u_2 < e^{-Rs}$, which has probability $e^{-Rs}$ because $u_2$ is uniform on $(0, 1]$ and $e^{-Rs} \in (0, 1]$. Line L10 picks the smallest $j$ with $S_j > u_1 R$, where $S_j = k_1 + \cdots + k_j$ and $S_0 = 0$. Because $S_{j-1} < S_j$, this is the $j$ with $S_{j-1} \le u_1 R < S_j$. The variable $u_1 R$ is uniform on $[0, R)$, so this has probability $(S_j - S_{j-1}) / R = k_j / R$. The index depends only on $u_1$ and $\Delta t$ only on $u_2$, so they are independent, and the joint law is the product. $\square$

**Theorem (exact sampling).** Let $t_0 = 0 < t_1 < t_2 < \cdots$ be the times recorded by line L12 and $x_0, x_1, \ldots$ the states. Then the joint law of $(t_n, x_n)_{n \ge 0}$, up to the first $n$ with $t_n \ge t_{\mathrm{end}}$ or $R(x_n) = 0$, is the law of the jump times and states of the Markov jump process started at $x_0$.

*Proof.* By induction on the number $n$ of steps. For $n = 0$ both start at $(0, x_0)$. Assume that the first $n$ pairs have the correct joint law. Given these pairs, step $n + 1$ uses only the state $x_n$ and new random numbers, which are independent of the past. By Lemma 2, it draws the holding time $t_{n+1} - t_n$ and the next state $x_{n+1} = y_j(x_n)$ with the law of the construction, given $x_n$, and independently of the earlier pairs. This is the conditional law of the next jump of the Markov jump process given its past, by the Markov property of the construction. So the first $n + 1$ pairs have the correct joint law. If $R(x_n) = 0$, the state $x_n$ is absorbing and the process stays in it, which is what line L5 returns. If $t_n + \Delta t \ge t_{\mathrm{end}}$, the next jump is after $t_{\mathrm{end}}$, so the process is in $x_n$ on $[t_n, t_{\mathrm{end}}]$, which is what line L8 uses. $\blacksquare$

**The time average.** Lines L8 and L9 add $f(x_n)$ times the length of the part of $[t_n, t_{n+1})$ that lies in $[0, t_{\mathrm{end}}]$. The sum is exactly $\int_0^{t} f(x(s))\, ds$ for the piecewise constant path $x(s)$, and the result is this integral divided by $t$. If the state space is finite and the process is irreducible, the ergodic theorem for Markov jump processes gives $\frac{1}{t}\int_0^t f(x(s))\, ds \to \sum_x \pi(x) f(x)$ almost surely as $t \to \infty$, where $\pi$ is the unique stationary distribution.

For the two-state system of the page this limit can be found directly. The visits to A and B alternate. The times in A are independent with mean $1 / k_{AB}$ and the times in B are independent with mean $1 / k_{BA}$. By the renewal reward theorem, the long-run fraction of time in A is the mean time in A over the mean length of one cycle,

$$\frac{1 / k_{AB}}{1 / k_{AB} + 1 / k_{BA}} = \frac{k_{BA}}{k_{AB} + k_{BA}},$$

which is also $\pi(A)$ from the balance $\pi(A) k_{AB} = \pi(B) k_{BA}$. With $k_{AB} = 1$ and $k_{BA} = 3$ it is $3/4$.

**What is not proved.** The theorem is about the rate model. It says nothing about whether the rates are right, whether the catalog of events is complete, or whether the real system is a Markov jump process. For atomic systems, the Markov property holds only approximately, when the system loses the memory of how it entered a state before it leaves it. This is the separation of time scales that transition state theory assumes.
