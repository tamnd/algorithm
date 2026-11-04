---
title: Counter overflow in a counting Bloom filter
proves: [complexity]
status: full
---

**Setting.** Let $n$ distinct keys be stored once each. Assume ideal hashing: the $kn$ values $h_i(x)$ are independent and uniform on $\{0, \ldots, m-1\}$. Let $N_j$ be the number of the $kn$ values equal to $j$. By invariant (C) of the correctness proof, counter $j$ can be stuck only if $N_j$ reached $c_{\max}$ at some time, and with inserts only $N_j$ never falls, so it suffices to bound $N_j$ at the end. With deletes, the bound below applies to each set of $n$ keys that is present at some time.

**Lemma.** For each $j$ and each integer $i \ge 1$, $\Pr[N_j \ge i] \le \binom{kn}{i} m^{-i}$.

*Proof.* If $N_j \ge i$, then some set of $i$ of the $kn$ hash values is all equal to $j$. A fixed set of $i$ values is all equal to $j$ with probability $m^{-i}$ by independence. There are $\binom{kn}{i}$ sets, and the [union bound](/union-bound/) gives the claim. $\square$

**Theorem.** If $k \le (m/n) \ln 2$, then for each integer $i \ge 1$,
$$ \Pr[\max_j N_j \ge i] \le m \left(\frac{e \ln 2}{i}\right)^i. $$

*Proof.* By the bound $\binom{a}{i} \le (ea/i)^i$,
$$ \binom{kn}{i} m^{-i} \le \left(\frac{e k n}{i m}\right)^i \le \left(\frac{e \ln 2}{i}\right)^i, $$
using $kn/m \le \ln 2$. The union bound over the $m$ positions multiplies by $m$. $\blacksquare$

**Numbers.** For $i = 16$ the factor is $(e \ln 2/16)^{16} \approx 1.37 \cdot 10^{-15}$, and for $i = 15$, the value at which a 4-bit counter sticks, it is about $3.1 \cdot 10^{-14}$. The exact law of $N_j$ is binomial with $kn$ trials and success probability $1/m$, close to a [Poisson](/poisson-distribution/) law with mean $kn/m \le \ln 2$, so the true tail is smaller still: the Poisson tail at mean $0.7$ for 16 or more is about $8 \cdot 10^{-17}$.

**Time.** Each of INSERT, DELETE and QUERY makes at most $k$ hash evaluations and $k$ counter accesses, and does constant work for each, so it takes $\Theta(k)$ time in the worst case on the word RAM with $c \le w$. The array uses $mc$ bits.
