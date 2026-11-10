---
title: The sparse form of HyperLogLog++ converts to exactly the dense registers, and merges are exact in all modes
proves: [correctness]
status: full
---

Let $h$ map items to 64-bit strings, let $p < p' = 25$, and let $s = p' - p$. For a 64-bit $y$, split it as
$$y = \underbrace{\mathrm{idx}}_{p \text{ bits}}\;\underbrace{\ell}_{s \text{ bits}}\;\underbrace{w'}_{64 - p' \text{ bits}},$$
so that $\mathrm{idx}' = \mathrm{idx}\,\ell$ (the first $p'$ bits) and $w = \ell\,w'$ (the last $64 - p$ bits). For a $k$-bit string $u$, $\rho_k(u)$ is the position of the leftmost 1, counted from 1, with $\rho_k(0) = k + 1$. The dense pair of $y$ is $(\mathrm{idx}, \rho_{64-p}(w))$ and the sparse pair is $(\mathrm{idx}', \rho_{64-p'}(w'))$.

**Lemma 1 (decode).** Let $\mathrm{dec}(\mathrm{idx}', \rho')$ be the pair $(\lfloor \mathrm{idx}'/2^s \rfloor, r)$ with $r = s - \mathrm{bitlen}(\ell) + 1$ if $\ell \ne 0$ and $r = s + \rho'$ if $\ell = 0$, where $\ell = \mathrm{idx}' \bmod 2^s$. Then $\mathrm{dec}$ of the sparse pair of $y$ is the dense pair of $y$.

*Proof.* The first $p$ bits of $\mathrm{idx}'$ are $\mathrm{idx}$, so $\lfloor \mathrm{idx}'/2^s \rfloor = \mathrm{idx}$. If $\ell \ne 0$, the leftmost 1 of $w = \ell\,w'$ lies in $\ell$. In the $s$-bit string $\ell$, a value with bit length $t$ has $s - t$ leading zeros, so its leftmost 1 is at position $s - t + 1$, and this is $\rho_{64-p}(w)$. If $\ell = 0$, the first $s$ bits of $w$ are zeros, so $\rho_{64-p}(w) = s + \rho_{64-p'}(w')$. This also holds when $w' = 0$: then $\rho_{64-p'}(0) = 64 - p' + 1$ and $s + 64 - p' + 1 = 64 - p + 1 = \rho_{64-p}(0)$. $\square$

**Lemma 2 (monotone).** For a fixed $\mathrm{idx}'$, the second part of $\mathrm{dec}(\mathrm{idx}', \rho')$ is a nondecreasing function of $\rho'$.

*Proof.* If $\ell \ne 0$ it does not depend on $\rho'$. If $\ell = 0$ it is $s + \rho'$. $\square$

Write $D(X)$ for the dense registers that lines L1 and L6 build from a set $X$ of distinct items: $D(X)[j] = \max\{\rho_{64-p}(w_x) : x \in X, \mathrm{idx}_x = j\}$, or 0. Write $P(X)$ for the sparse map of line L4: $P(X)[\mathrm{idx}'] = \max\{\rho_{64-p'}(w'_x) : x \in X, \mathrm{idx}'_x = \mathrm{idx}'\}$, for the keys that occur. As on the [HyperLogLog](/hyperloglog/) proof page, both are functions of the set of distinct items, because each update is a maximum with a value that depends only on the item.

**Theorem 3 (the conversion is exact).** Let $C(P)$ be the conversion of line L5: $C(P)[j]$ is the maximum of the second part of $\mathrm{dec}(\mathrm{idx}', P[\mathrm{idx}'])$ over the keys $\mathrm{idx}'$ of $P$ whose first $p$ bits are $j$, or 0. Then $C(P(X)) = D(X)$ for every set $X$.

*Proof.* Fix $j$. The items of $X$ with $\mathrm{idx} = j$ are grouped by their key $\mathrm{idx}'$, and each such key has first $p$ bits $j$. For one key $k$ with items $X_k$, by Lemma 2 and Lemma 1,
$$\mathrm{dec}\big(k, \max_{x \in X_k}\rho'(x)\big)_2 = \max_{x \in X_k}\mathrm{dec}(k, \rho'(x))_2 = \max_{x \in X_k}\rho_{64-p}(w_x),$$
where the first equality holds because a nondecreasing function commutes with a maximum. Taking the maximum over the keys $k$ in bucket $j$ gives $\max\{\rho_{64-p}(w_x) : x \in X, \mathrm{idx}_x = j\} = D(X)[j]$. If no item has $\mathrm{idx} = j$, both sides are 0. $\square$

**Corollary 4 (the switch does not change answers).** Suppose the sketch converts after the set $X_1$ of items and then reads a further set $X_2$ in dense mode. Its registers are $D(X_1 \cup X_2)$, the same as a sketch that was dense from the start.

*Proof.* After the conversion the registers are $C(P(X_1)) = D(X_1)$ by Theorem 3. Line L6 then updates them as the dense sketch would, and $D$ is a register by register maximum over the items, so the result is $D(X_1 \cup X_2)$. $\square$

**Theorem 5 (merges are exact).** Let two sketches use the same $h$ and $p$, built from sets $X$ and $Y$.

1. If both are sparse, the key by key maximum of $P(X)$ and $P(Y)$ is $P(X \cup Y)$.
2. In any other case, let each sketch be converted to dense if it is sparse. The register by register maximum is $D(X \cup Y)$.

*Proof.* Part 1: $P(X \cup Y)[k]$ is a maximum over the items of $X \cup Y$ with key $k$, which is the maximum of the maxima over $X$ and over $Y$ (with an absent key treated as absent from that side). Part 2: by Theorem 3 the converted registers are $D(X)$ and $D(Y)$, and the same argument for the registers gives $D(X \cup Y)$. If the merged sparse map of part 1 exceeds the size limit, converting it gives $D(X \cup Y)$ by Theorem 3. $\square$

**The sparse estimate.** In sparse mode, $|P(X)|$ is the number of keys among $m' = 2^{p'}$ possible keys that some item hits. For independent uniform hash values this is the number of nonzero bits of a [linear counting](/linear-counting/) bitmap of size $m'$, so line L7 is exactly the linear counting estimate $m'\ln(m'/V)$ with $V = m' - |P(X)|$, and the mean and variance of $V$ proved on that page apply.

**What is not proved.** The bias table of line L8, the limit $5m$ for its use, and the thresholds of line L10 are measured by simulation in the paper of Heule, Nunkesser and Hall, and the asymptotic error of the dense estimate is the cited theorem for HyperLogLog with an ideal hash. $\blacksquare$
