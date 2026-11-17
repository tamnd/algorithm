---
title: The next reaction method samples the process of the chemical master equation
proves: [correctness]
status: full
---

Use the setting of the [first reaction method](/first-reaction-method/): propensities $a_j(x) \ge 0$, $a_0 = \sum_j a_j$, and the Markov jump process $X$ of the chemical master equation, assumed not to explode on $[0, T]$. In state $x$, the next reaction of $X$ comes after a time $\tau$ and is reaction $J$, with the joint density $a_j(x) e^{-a_0(x) s}$.

**The residuals.** At any moment of the run, give each reaction $k$ a *residual* $r_k \ge 0$, in the units of a unit-rate clock:

- if $a_k > 0$, then $r_k = a_k (\tau_k - t)$, where $\tau_k$ is the time stored in the queue and $t$ is the current time;
- if $a_k = 0$, then $r_k$ is the stored clock of line L11, and $\tau_k = \infty$.

So $\tau_k = t + r_k / a_k$ when $a_k > 0$. Line L2 sets $r_k$ to a fresh unit exponential for each $k$.

**Lemma 1 (the update keeps the residuals).** Let reaction $\mu$ fire at time $t'$, after the previous event at time $t$, and let $s = t' - t$. Then after lines L8 to L12, for each $k \ne \mu$, the new residual of $k$ is $r_k - a_k s$, where $r_k$ and $a_k$ are the residual and the propensity just after the previous event. The residual of $\mu$ is a fresh unit exponential.

*Proof.* Between the two events the state does not change, so $a_k$ is constant on $[t, t')$. For $k$ with $a_k > 0$, the residual at time $t'$ is $a_k(\tau_k - t') = a_k(\tau_k - t) - a_k s = r_k - a_k s$. Line L11 computes exactly this number when $k \in G[\mu]$ and the propensity changes, and stores it in the new time $t' + r / a_k^{\text{new}}$, or in the stored clock if $a_k^{\text{new}} = 0$. If $k \notin G[\mu]$, or the propensity does not change, the stored $\tau_k$ is kept, and $a_k(\tau_k - t')$ is the same number. For $k$ with $a_k = 0$, nothing is consumed ($a_k s = 0$), and the stored clock is kept or moved into a time, unchanged. For $k = \mu$, line L10 draws a fresh unit exponential. Reactions outside $G[\mu]$ keep their propensity by the definition of the dependency graph, so no reaction that needs a new propensity is missed. $\square$

**Lemma 2 (the residuals are fresh).** Just after each event (and at the start), given the whole history of the run so far (the event times, the fired reactions and the states), the residuals $r_1, \ldots, r_m$ are independent unit exponentials.

*Proof.* By induction on the number of events. At the start it holds by line L2. Assume it holds just after an event at time $t$ in state $x$. The next event is at $t + S$ with $S = \min_{k : a_k > 0} r_k / a_k$, and it is the reaction $M$ that reaches the minimum. Condition on $S = s$ and $M = \mu$. For $k \ne \mu$ with $a_k > 0$, this conditions $r_k$ only through the event $r_k > a_k s$, and the $r_k$ are independent, so the $r_k$ stay independent. By the memoryless property of the exponential law, $r_k - a_k s$ given $r_k > a_k s$ is again a unit exponential. For $k$ with $a_k = 0$, $r_k$ does not enter $S$ or $M$, so it is unchanged and still a unit exponential, independent of the rest. The residual of $\mu$ is a fresh draw. By Lemma 1 these are the new residuals, so the claim holds after the new event. $\square$

**Theorem.** The next reaction method run from $x_0$ up to $T$ records event times and states with the same joint law as the jumps of $X$ on $[0, T]$. So its last state has the law $P(\cdot, T)$, and it has the same law as the outputs of the direct method and the first reaction method.

*Proof.* Just after an event in state $x$, by Lemma 2 the numbers $r_k / a_k$ for $a_k > 0$ are, given the history, independent exponentials with rates $a_k$. The queue returns their minimum and its index (lines L5 and L7). By the lemma on the minimum of exponential clocks (in the proof for the first reaction method), the pair (time to the event, reaction) has the density $a_j(x) e^{-a_0(x) s}$, the next reaction density of $X$, and it depends on the history only through $x$. Line L6 stops when the smallest time is infinite ($a_0(x) = 0$, so $X$ stays in $x$) or after $T$ (no reaction of $X$ in $(t, T]$, which has the same probability $e^{-a_0(x)(T - t)}$). The induction over the events is then the same as for the direct method. $\square$

**Remark (one random number per event).** Line L2 draws $m$ unit exponentials, and each event draws one more, at line L10. So a run with $N$ events uses $m + N$ random numbers. The direct method uses $2N$ (plus one for the last, discarded waiting time), and the first reaction method uses up to $mN$.

**Remark (the source of the reuse rule).** Gibson and Bruck (2000) reuse the clocks of the reactions that did not fire by rescaling the remaining time, $\tau_k \leftarrow t + (a_k^{\text{old}} / a_k^{\text{new}})(\tau_k - t)$, which is line L11. The handling of a propensity that drops to 0 and later becomes positive here keeps the residual $r_k$ of the unit clock. This is the view of the random time change representation of the process, in which each reaction has its own unit-rate Poisson process, run at the speed $a_k(X(t))$.
