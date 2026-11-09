---
title: The genetic algorithm keeps the best string it saw, elitism keeps the best fitness of the population, and with elitism it reaches an optimum with probability 1
proves: [correctness]
status: full
---

We use the pseudocode of the page. The search space is $\{0,1\}^n$, $f : \{0,1\}^n \to \mathbb{R}$, $f^* = \max f$, and $P_t$ is the population after generation $t$, with $P_0$ from line L1.

**Claim 1 (size and form).** Each $P_t$ has exactly $N$ strings in $\{0,1\}^n$.

*Proof.* Line L1 makes $N$ strings of length $n$. In a generation, line L4 puts $e < N$ strings into $Q$. Each pass of lines L6 to L9 adds at least one string while $|Q| < N$ and adds the second only if $|Q| < N$, so the loop of line L5 stops with $|Q| = N$. One-point crossover and bit flips map strings of length $n$ to strings of length $n$. $\square$

**Claim 2 (the returned string).** After generation $t$, $best$ is a string of $P_0 \cup \dots \cup P_t$ and $f(best) = \max\{f(x) : x \in P_0 \cup \dots \cup P_t\}$.

*Proof.* By induction on $t$. Line L2 gives the claim for $t = 0$. Assume it for $t - 1$. Line L11 replaces $best$ by a best string of $P_t$ exactly when that string is better than $best$. So $f(best)$ becomes $\max(f(best), \max_{x \in P_t} f(x))$, which is the maximum over $P_0 \cup \dots \cup P_t$, and $best$ stays a string of one of these populations. $\square$

**Claim 3 (elitism).** If $e \ge 1$, then $\max_{x \in P_t} f(x) \ge \max_{x \in P_{t-1}} f(x)$ for each $t \ge 1$.

*Proof.* Line L4 puts the $e$ strings of $P_{t-1}$ with the largest $f$ into $Q$. As $e \ge 1$, one of them has the largest $f$ in $P_{t-1}$. Lines L5 to L9 only add strings to $Q$, and line L10 sets $P_t = Q$. So $P_t$ holds a string with fitness $\max_{x \in P_{t-1}} f(x)$. $\square$

**Claim 4 (every string can appear).** Let $0 < p_m < 1$ and $\delta = \min(p_m, 1 - p_m)^n$. For each child that line L8 makes and each fixed $y \in \{0,1\}^n$, the probability that the child equals $y$ is at least $\delta$, given anything that happened before line L8.

*Proof.* Let $z$ be the string before mutation. The bits flip independently, so the child equals $y$ with probability $p_m^{h}(1 - p_m)^{n - h}$, where $h$ is the [Hamming distance](/hamming-distance/) of $z$ and $y$. Each factor is at least $\min(p_m, 1 - p_m)$, so the product is at least $\delta$, whatever $z$ is. $\square$

**Claim 5 (convergence with elitism).** Let $e \ge 1$ and $0 < p_m < 1$, and let $A_t$ be the event that no string of $P_0, \dots, P_t$ is optimal. Then $\Pr[A_t] \le (1 - \delta)^t$. Hence $f(best) = f^*$ after finitely many generations with probability 1, and from then on, $P_t$ always holds an optimal string.

*Proof.* Each generation makes at least one child at line L8, because $e < N$. Fix an optimal string $x^*$. By Claim 4, given the history up to the start of generation $t$, the first child of that generation equals $x^*$ with probability at least $\delta$. So $\Pr[A_t \mid A_{t-1}] \le 1 - \delta$, and $\Pr[A_t] \le (1 - \delta)^t$ by induction. The events $A_t$ decrease, so $\Pr[\bigcap_t A_t] = \lim_t \Pr[A_t] = 0$. Thus some $P_t$ holds an optimal string with probability 1. By Claim 2, $f(best) = f^*$ from that generation on, and by Claim 3, every later population holds a string with fitness $f^*$. $\square$

Claim 5 needs elitism for its last part. Without elitism, Rudolph (1994) showed that the populations form an irreducible Markov chain on a finite set when $0 < p_m < 1$, so the chain visits every population, including populations with no optimal string, infinitely often. The best string seen still reaches $f^*$ with probability 1 by Claims 2 and 4. $\blacksquare$
