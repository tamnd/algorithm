---
title: The direct method samples the process of the chemical master equation
proves: [correctness]
status: full
---

Fix a network with stoichiometric vectors $\nu_1, \ldots, \nu_m$ and propensities $a_j(x) \ge 0$, and write $a_0(x) = \sum_j a_j(x)$. The chemical master equation is the forward equation of the Markov jump process $X(t)$ with these jump rates: in a state $x$, the process waits an exponential time with rate $a_0(x)$, and then it jumps to $x + \nu_j$ with probability $a_j(x) / a_0(x)$. We assume that this process does not explode on $[0, T]$, that is, it makes finitely many jumps in $[0, T]$ with probability 1. This holds, for example, when the reachable states are finite, or when $a_0$ is bounded on them.

**Lemma 1 (the next reaction density).** Let the process be in state $x$ at time $t$, with $a_0(x) > 0$. Let $\tau$ be the time to the next reaction and $J$ the index of that reaction. Then $(\tau, J)$ has the joint density

$$p(s, j \mid x) = a_j(x)\, e^{-a_0(x) s}, \qquad s \ge 0, \; j = 1, \ldots, m.$$

*Proof.* In the jump process, reaction $j$ fires in $[t + s, t + s + ds)$ with probability $a_j(x)\, ds + o(ds)$, given that the state is still $x$. Let $P_0(s)$ be the probability that no reaction fires in $[t, t + s)$. Then $P_0(s + ds) = P_0(s)\,(1 - a_0(x)\, ds + o(ds))$, so $P_0' = -a_0 P_0$ with $P_0(0) = 1$, and $P_0(s) = e^{-a_0(x) s}$. The probability that the first reaction is $j$ and fires in $[t + s, t + s + ds)$ is $P_0(s)\, a_j(x)\, ds$. $\square$

**Lemma 2 (one step of the direct method).** In state $x$ with $a_0 = a_0(x) > 0$, lines L5 to L8 return a pair $(\tau, \mu)$ with the density $p(s, j \mid x)$ of Lemma 1.

*Proof.* Line L5 draws $\tau$ with density $a_0 e^{-a_0 s}$. Line L7 draws $u$ uniform on $[0, a_0)$, independent of $\tau$. Line L8 returns the first index $\mu$ with $a_1 + \cdots + a_\mu > u$. Indices with $a_j = 0$ add nothing to the sum, so they are never returned. For an index $j$ with $a_j > 0$, the event $\mu = j$ is the event $a_1 + \cdots + a_{j-1} \le u < a_1 + \cdots + a_j$, which has probability $a_j / a_0$. So $(\tau, \mu)$ has the density $a_0 e^{-a_0 s} \cdot a_j / a_0 = a_j e^{-a_0 s}$. $\square$

**Theorem.** Run the direct method from $x_0$ up to $T$. Let $t_1 < t_2 < \cdots$ be the event times and $x_1, x_2, \ldots$ the states that it records. Then the sequence $(t_k, x_k)$ has the same joint law as the jump times and the states after the jumps of $X$ on $[0, T]$. In particular, the last recorded state has the law $P(\cdot, T)$, the solution of the chemical master equation at time $T$.

*Proof.* By induction on $k$. Assume that $(t_1, x_1, \ldots, t_k, x_k)$ has the law of the first $k$ jumps of $X$ (for $k = 0$ there is nothing to prove). By the strong Markov property of $X$ at its $k$-th jump time, the next waiting time and the next reaction of $X$, given the past, have the density $p(s, j \mid x_k)$ of Lemma 1, and they depend on the past only through $x_k$. The direct method draws fresh random numbers in each step, so its next pair, given its past, has the density of Lemma 2, which is the same. So the first $k + 1$ jumps have the same law.

If $a_0(x_k) = 0$, then $X$ stays in $x_k$ for ever, and line L4 stops the run in $x_k$: both agree.

Stopping at $T$: line L6 discards a waiting time with $t_k + \tau > T$ and stops. In $X$, the event that no reaction fires in $(t_k, T]$ has probability $e^{-a_0(x_k)(T - t_k)} = \Pr(\tau > T - t_k)$, so the two agree on the event that there is no further event before $T$, and the state at $T$ is $x_k$ in both. Since $X$ does not explode on $[0, T]$, the run stops after finitely many events with probability 1. $\square$

**Remark (number of events).** The number of events in $[0, T]$ is the number of jumps of $X$ in $[0, T]$. For pure death $X \to 0$ with rate $c$ per molecule from $x_0$, each molecule dies by time $T$ with probability $1 - e^{-cT}$, so the mean number of events is $x_0 (1 - e^{-cT})$. For immigration-death at stationarity, births and deaths each fire at the mean rate $b$, so the mean number of events in $[0, T]$ is $2 b T$.
