---
title: The first reaction method samples the process of the chemical master equation
proves: [correctness]
status: full
---

Use the setting of the direct method: propensities $a_j(x) \ge 0$, $a_0(x) = \sum_j a_j(x)$, and the Markov jump process $X$ whose forward equation is the chemical master equation. In state $x$ the next reaction of $X$ comes after a time $\tau$ and is reaction $J$, where $(\tau, J)$ has the joint density $a_j(x) e^{-a_0(x) s}$ (Lemma 1 of the proof for the [direct method](/gillespie-algorithm/)). We assume that $X$ does not explode on $[0, T]$.

**Lemma (the minimum of exponential clocks).** Let $E_j$, for the indices $j$ with $a_j > 0$, be independent with $E_j$ exponential of rate $a_j$. Let $S = \min_j E_j$ and let $M$ be the index where the minimum is reached. Then $(S, M)$ has the joint density $a_j e^{-a_0 s}$, with $a_0 = \sum_j a_j$. In particular $S$ is exponential with rate $a_0$, $\Pr(M = j) = a_j / a_0$, and $S$ and $M$ are independent.

*Proof.* Ties have probability 0, because the $E_j$ have densities. For $s \ge 0$, the event $\{M = j, S \in [s, s + ds)\}$ is the event that $E_j \in [s, s + ds)$ and $E_k > s$ for all $k \ne j$ (up to $o(ds)$). By independence its probability is

$$a_j e^{-a_j s}\, ds \prod_{k \ne j} e^{-a_k s} = a_j e^{-a_0 s}\, ds.$$

Summing over $j$ gives the density $a_0 e^{-a_0 s}$ of $S$, and integrating over $s$ gives $\Pr(M = j) = a_j / a_0$. The joint density is the product of the two marginals, so $S$ and $M$ are independent. $\square$

**Theorem.** The first reaction method run from $x_0$ up to $T$ records event times and states with the same joint law as the jumps of $X$ on $[0, T]$. So its last state has the law $P(\cdot, T)$ of the chemical master equation, and it has the same law as the output of the direct method.

*Proof.* Lines L4 to L7 draw one exponential $E_j$ of rate $a_j(x)$ for each $j$ with $a_j(x) > 0$, all independent of each other and of the past, and keep the smallest. Reactions with $a_j(x) = 0$ get no clock and cannot fire, and in $X$ they have probability 0 of firing in state $x$. By the lemma, the pair (time to the event, reaction) has the density $a_j(x) e^{-a_0(x) s}$, which is the next reaction density of $X$. Line L8 stops when no clock was drawn, that is, when $a_0(x) = 0$, and then $X$ stays in $x$. Line L9 stops when the first clock rings after $T$; in $X$, no reaction in $(t, T]$ has probability $e^{-a_0(x)(T - t)}$, which is $\Pr(S > T - t)$. The induction on the number of events is then the same as for the direct method: given the past, each step uses fresh clocks and depends on the past only through the current state, as $X$ does by the strong Markov property. $\square$

**Remark (cost).** A step draws one exponential for each reaction with a positive propensity, so it uses up to $m$ random numbers where the direct method uses 2. The clocks of the reactions that did not fire are thrown away. The [next reaction method](/next-reaction-method/) shows that they can be kept: by the memoryless property, a clock that has not rung yet still has an exponential remaining time.
