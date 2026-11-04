---
title: The one-bitmap Flajolet-Martin estimate is within a constant factor
proves: [complexity]
status: full
---

Take one bitmap, $m = 1$, with $L$ larger than any index that occurs below. Assume ideal hashing: the values $h(x)$ of distinct items are independent and uniform $w$-bit integers, with $w$ large. Then for each item, $\Pr[\rho(h(x)) = r] = 2^{-(r+1)}$, independently over the items. Let $n$ distinct items be seen and let $R$ be the index of the lowest 0 bit.

**Lemma 1.** $\Pr[B[r] = 1] = 1 - (1 - 2^{-(r+1)})^n$.

*Proof.* By Lemma 1 of the correctness proof, $B[r] = 0$ exactly when no item has $\rho = r$. Each of the $n$ independent items avoids $r$ with probability $1 - 2^{-(r+1)}$. $\square$

**Theorem.** For each integer $a \ge 0$,
$$ \Pr[2^R \ge 2^a] \le \frac{n}{2^{a}}, \qquad \Pr[2^R < 2^a] \le \sum_{r=0}^{a-1} \exp\!\left(-\frac{n}{2^{r+1}}\right). $$
In particular, for $c$ a power of two with $n/c$ a power of two, $\Pr[2^R \ge cn] \le 1/c$ and $\Pr[2^R < n/c] \le e^{-c}/(1 - e^{-c})$.

*Proof.* *Upper tail.* If $R \ge a$ with $a \ge 1$, then $B[a-1] = 1$, which by Lemma 1 and Bernoulli's inequality $1 - (1 - p)^n \le np$ has probability at most $n 2^{-a}$. For $a = 0$ the bound $n \ge 1$ is trivial.

*Lower tail.* If $R < a$, then $B[r] = 0$ for some $r < a$. By Lemma 1, $1 - p \le e^{-p}$ and the [union bound](/union-bound/), this has probability at most $\sum_{r < a} e^{-n 2^{-(r+1)}}$.

*The special case.* Take $2^a = cn$ in the upper tail. For the lower tail take $2^a = n/c$. The term $r = a - 1 - l$ is $\exp(-c \, 2^{l})$, and $2^l \ge 1 + l$, so the sum is at most $\sum_{l \ge 0} e^{-c} e^{-cl} = e^{-c}/(1 - e^{-c})$. $\square$

So for $c = 4$ the estimate $2^R$ lies in $[n/4, 4n)$ with probability at least $1 - 1/4 - 0.019 > 0.73$. The constant factor $1/\varphi$ and the averaging over $m$ bitmaps make this a relative error of $O(1/\sqrt{m})$; Flajolet and Martin (1985) proved the exact constants $\varphi = 0.77351$ and $0.78/\sqrt{m}$.

**Cost.** ADD computes one hash, one division by $m$, one count of trailing zeros and one bit write, which is $\Theta(1)$ word operations on the word RAM. ESTIMATE scans at most $L + 1$ bits of each bitmap, $O(mL)$ steps. The space is $mL$ bits. $\blacksquare$
