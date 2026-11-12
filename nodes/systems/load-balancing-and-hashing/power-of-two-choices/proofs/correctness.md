---
title: The d-choice rule places each ball in a least loaded sampled bin, and the supermarket model has the fixed point s_i = lambda^((d^i - 1)/(d - 1))
proves: [correctness]
status: full
---

We use the pseudocode TWO-CHOICE-PLACE of the page, with $n \ge 1$ bins and $d \ge 1$ choices. The procedure RANDOM$(0, n-1)$ returns a uniform index, independent of all other calls. For a load vector $\ell$ and an integer $i$, let $\nu_i(\ell) = |\{j : \ell[j] \ge i\}|$.

## Lemma 1 (the rule)

**Claim.** A call of TWO-CHOICE-PLACE adds 1 to the load of exactly one bin $b^\ast$. The bin $b^\ast$ is one of the $d$ sampled bins, and its load before the call is the least load among the sampled bins. Ties go to the bin sampled first.

*Proof.* Let $b_1, \ldots, b_d$ be the indices drawn at line L1 and at line L3 in rounds $2, \ldots, d$. We show by induction on $r$ the invariant: after round $r$ (line L1 is round 1), $best \in \{b_1, \ldots, b_r\}$, $\ell[best] = \min_{s \le r} \ell[b_s]$, and $best$ is the first of $b_1, \ldots, b_r$ with this load. For $r = 1$, $best = b_1$. In round $r + 1$, line L4 changes $best$ to $b_{r+1}$ if and only if $\ell[b_{r+1}] < \ell[best]$. If it changes, $b_{r+1}$ is the only sample so far with the new least load, so it is the first one. If it does not change, the minimum and the first index with the minimum stay the same. The loads do not change during the loop. After round $d$, line L5 adds 1 to $\ell[best]$ only. $\square$

So after $t$ calls from the zero vector, the loads add up to $t$.

## Lemma 2 (the chance of a high bin)

**Claim.** For each load vector $\ell$ and each integer $i$, the call places its ball in a bin of load at least $i$ with probability exactly $(\nu_i(\ell)/n)^d$.

*Proof.* By Lemma 1, the chosen bin has the least load among the samples. Its load is at least $i$ if and only if every sample has load at least $i$. The $d$ samples are independent and uniform, and each one has load at least $i$ with probability $\nu_i(\ell)/n$. Multiply. $\square$

With one choice the probability is $\nu_i/n$. With $d$ choices it is the $d$-th power. If a fraction $\beta$ of the bins has load at least $i$, then only a fraction about $\beta^d$ of the next balls reach height $i + 1$. The [power of d choices theorem](/power-of-d-choices-theorem/) iterates this step to prove the bound $\ln\ln n/\ln d + O(1)$ on the maximum load.

## Lemma 3 (the supermarket fixed point)

**Model.** There are $n$ servers, each a FIFO queue served at rate 1 with exponential service times. Jobs arrive as a Poisson process of rate $\lambda n$ with $0 < \lambda < 1$. Each job samples $d$ queues and joins the shortest by the rule above. Let $s_i(t)$ be the fraction of queues with at least $i$ jobs, so $s_0 = 1$. Mitzenmacher shows that as $n \to \infty$ the vector $(s_i)$ follows the limit equations

$$ \frac{ds_i}{dt} = \lambda\bigl(s_{i-1}^d - s_i^d\bigr) - \bigl(s_i - s_{i+1}\bigr), \qquad i \ge 1. $$

The first term is the rate per queue of arrivals that join a queue with exactly $i - 1$ jobs: by Lemma 2 an arrival joins a queue with at least $i - 1$ jobs with probability $s_{i-1}^d$ and one with at least $i$ jobs with probability $s_i^d$. The second term is the rate per queue of departures from queues with exactly $i$ jobs.

**Claim.** The only fixed point with $s_0 = 1$ and $s_i \to 0$ is $s_i = \lambda^{(d^i - 1)/(d-1)}$ for $d \ge 2$, and $s_i = \lambda^i$ for $d = 1$.

*Proof.* At a fixed point every right side is 0. Add the equations for $j = i, \ldots, N$. The sums telescope:

$$ 0 = \lambda\bigl(s_{i-1}^d - s_N^d\bigr) - \bigl(s_i - s_{N+1}\bigr). $$

Let $N \to \infty$. Since $s_N \to 0$, we get $s_i = \lambda s_{i-1}^d$ for each $i \ge 1$. With $s_0 = 1$, induction on $i$ gives $s_i = \lambda^{e_i}$ with $e_0 = 0$ and $e_i = 1 + d\,e_{i-1}$, so $e_i = 1 + d + \cdots + d^{i-1}$. This is $(d^i - 1)/(d - 1)$ for $d \ge 2$ and $i$ for $d = 1$. Conversely, $s_i = \lambda s_{i-1}^d$ for all $i$ makes each right side $(s_i - s_{i+1}) - (s_i - s_{i+1}) = 0$. $\square$

## Corollary (expected time in the system)

At the fixed point, the expected number of jobs at a queue is $\sum_{i \ge 1} s_i$, and jobs arrive at each queue at rate $\lambda$. By Little's law the expected time that a job spends in the system is

$$ T_d(\lambda) = \frac1\lambda \sum_{i \ge 1} s_i = \sum_{i \ge 1} \lambda^{(d^i - d)/(d-1)} \quad (d \ge 2), \qquad T_1(\lambda) = \frac{1}{1-\lambda}. $$

For $d \ge 2$ the exponents grow like $d^i$, so the terms fall doubly exponentially once $\lambda^{d^i}$ is small. As $\lambda \to 1$, $T_1$ grows like $1/(1-\lambda)$ but $T_2$ grows only like $\log_2 \frac{1}{1-\lambda}$ up to a constant factor: the terms with $2^i \le 1/(1-\lambda)$ are each at most 1, and the later terms form a sum that is bounded by a constant. $\blacksquare$
