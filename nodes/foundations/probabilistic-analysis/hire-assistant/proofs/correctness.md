---
title: Hire-assistant hires exactly the candidates who beat all earlier ones
proves: [correctness]
status: full
---

We use the pseudocode of the page, with candidates $C[1 \ldots n]$ and a dummy candidate $C[0]$ that is worse than each real candidate. A position $j \ge 1$ is a *record* if $C[j]$ is better than each of $C[0], C[1], \ldots, C[j-1]$. Since $C[0]$ is worse than all, position 1 is always a record.

**Claim.** HIRE-ASSISTANT hires exactly the records, in increasing order of position, and at the end $C[best]$ is a best candidate of $C[1 \ldots n]$ when $n \ge 1$.

*Proof.* We use this invariant of the loop of line L2.

> **(I)** Before the iteration for $i$, with $1 \le i \le n + 1$: (a) $0 \le best \le i - 1$, and $C[best]$ is at least as good as each of $C[0 \ldots i-1]$; (b) the hires so far are exactly the records $j \le i - 1$, in increasing order.

*Initialization.* Before the first iteration, $i = 1$ and line L1 sets $best = 0$. Part (a) holds because $C[0 \ldots 0]$ is the dummy alone. Part (b) holds because no hire was made and no record $j \le 0$ exists.

*Maintenance.* Assume (I) for $i \le n$. By (a), $C[best]$ is a maximum of $C[0 \ldots i-1]$. So $C[i]$ is better than $C[best]$ if and only if $C[i]$ is better than each of $C[0 \ldots i-1]$, that is, if and only if $i$ is a record. Line L3 does not change $best$ or the hires.

- If $i$ is a record, line L4 is true. Line L5 sets $best = i$, and $C[i]$ is better than each of $C[0 \ldots i-1]$, so (a) holds for $i + 1$. Line L6 hires $i$, which is larger than each earlier hire, so (b) holds for $i + 1$.
- If $i$ is not a record, line L4 is false and nothing changes. $C[i]$ is not better than $C[best]$, so in a total order $C[best]$ is at least as good as $C[i]$, and (a) holds for $i + 1$. No record was missed, so (b) holds for $i + 1$.

*Termination.* The loop stops with $i = n + 1$. By (b), the hires are exactly the records $j \le n$, in order. By (a), $C[best]$ is at least as good as each of $C[0 \ldots n]$. If $n \ge 1$, position 1 is a record, so a real candidate was hired and $best \ge 1$; hence $C[best]$ is a best candidate of $C[1 \ldots n]$, and $best$ is the last hire. $\square$

**Cost.** The loop runs $n$ times and each iteration does one comparison in line L4 and $O(1)$ other work, so the time is $\Theta(n)$. The number of hires $m$ is the number of records.

**Expected number of hires.** Let the order of $C[1 \ldots n]$ be a uniform random permutation of distinct candidates, and let $X_i$ be the indicator that $i$ is a record. The relative order of $C[1 \ldots i]$ is uniform on the $i!$ orders, so each of these $i$ positions holds the best of them with probability $1/i$, and $\Pr[X_i = 1] = 1/i$. By linearity of expectation, $\mathbb{E}[m] = \sum_{i=1}^n \mathbb{E}[X_i] = H_n$. For RANDOMIZED-HIRE-ASSISTANT, the shuffle makes the order uniform for each fixed input of distinct candidates, so the same computation gives $\mathbb{E}[m] = H_n$ for each input. $\square$
