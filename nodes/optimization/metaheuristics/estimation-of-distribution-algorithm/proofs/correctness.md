---
title: UMDA keeps a valid model, absorbs at 0 and 1 without margins, drifts as a martingale under a flat score, and samples every string with margins
proves: [correctness]
status: full
---

We use the pseudocode of the page. Write $p^{(t)}$ for the model after generation $t$, with $p^{(0)} = (1/2, \dots, 1/2)$, and $a_j$ for the number of kept samples with bit $j$ equal to 1 in a generation.

**Claim 1 (valid model).** After every generation, $p_j = \min(1 - 1/n, \max(1/n, a_j/\mu))$ with margins, and $p_j = a_j/\mu$ without, for an integer $0 \le a_j \le \mu$. In particular $p_j \in [1/n, 1 - 1/n]$ or $p_j \in [0, 1]$.

*Proof.* Line L5 sets $p_j = a_j/\mu$, and $a_j$ counts some of the $\mu$ kept samples, so $0 \le a_j \le \mu$. Line L6 clamps it to $[1/n, 1 - 1/n]$, which is not empty for $n \ge 2$. $\square$

**Claim 2 (absorption without margins).** Without line L6, if $p_j^{(t)} = 0$ then $p_j^{(s)} = 0$ for every $s > t$, and the same for 1.

*Proof.* If $p_j = 0$, every sample of the next generation has $x_j = 0$, so $a_j = 0$ and line L5 gives $p_j = 0$ again. If $p_j = 1$, every sample has $x_j = 1$ and $a_j = \mu$. Induction on $s$ finishes the proof. $\square$

**Claim 3 (genetic drift).** Assume no margins and a constant score, with ties broken by the order of the samples, so that line L4 keeps the first $\mu$ samples. Then for each $j$:

1. $E[p_j^{(t+1)} \mid p^{(t)}] = p_j^{(t)}$, so $p_j^{(t)}$ is a martingale;
2. with probability 1 there is a $t$ with $p_j^{(t)} \in \{0, 1\}$;
3. $P(p_j \text{ is fixed at } 1) = p_j^{(0)}$.

*Proof.* The kept samples are the first $\mu$, and which samples are kept does not depend on their bits. So $a_j$ is a sum of $\mu$ independent Bernoulli variables with mean $p_j^{(t)}$, that is, $a_j \sim \mathrm{Bin}(\mu, p_j^{(t)})$, and $E[a_j/\mu] = p_j^{(t)}$. This is part 1.

For part 2, after the first generation $p_j$ takes values in the finite set $\{0, 1/\mu, \dots, 1\}$, and it is a Markov chain on that set. From any value $q \in (0, 1)$, the next value is 0 with probability $(1 - q)^\mu \ge \mu^{-\mu}$, since $q \le 1 - 1/\mu$. So from every state, the chain is absorbed within one step with probability at least $\delta = \mu^{-\mu} > 0$, and the probability that it is not absorbed within $t$ steps is at most $(1 - \delta)^{t-1}$, which goes to 0.

For part 3, let $\tau$ be the time of absorption, which is finite with probability 1 by part 2. The martingale is bounded by 0 and 1, so by the optional stopping theorem $E[p_j^{(\tau)}] = p_j^{(0)}$. Since $p_j^{(\tau)} \in \{0, 1\}$, $E[p_j^{(\tau)}] = P(p_j^{(\tau)} = 1)$, and by Claim 2 the value stays there. $\square$

So with a flat score, half of the positions end at 0 and half at 1 on average, and a position that the score does not push strongly enough can be fixed at the wrong value. The tests check that all 400 positions of a run with a constant score are fixed and that the fraction at 1 is close to $1/2$.

**Claim 4 (with margins, every string has a chance).** With line L6, every sample equals any given string $z \in \{0, 1\}^n$ with probability at least $n^{-n}$. So after $t$ samples in total, the probability that no sample was $z$ is at most $(1 - n^{-n})^t$.

*Proof.* The bits of a sample are independent, and bit $j$ equals $z_j$ with probability $p_j$ or $1 - p_j$, both at least $1/n$ by Claim 1. So the probability of $z$ is at least $(1/n)^n$. Given everything before it, each sample is $z$ with probability at least $n^{-n}$, so the probability that none of $t$ samples is $z$ is at most $(1 - n^{-n})^t$. $\square$

This is the same kind of guarantee as for random search: it holds for every score, and it says nothing useful about the time.

**Claim 5 (invariance).** Let $g$ be strictly increasing. With the same random numbers and the same rule for ties, the runs on $S$ and on $g \circ S$ give the same models and the same best string.

*Proof.* By induction on the generation. If the models are the same, line L3 gives the same samples. Since $g(S(x)) > g(S(y))$ if and only if $S(x) > S(y)$, and equal scores stay equal, line L4 keeps the same samples and finds the same best one. Lines L5 and L6 use only the kept samples, so the new models are the same. $\square$
