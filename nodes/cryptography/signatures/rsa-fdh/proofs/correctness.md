---
title: RSA-FDH signatures verify, and the full-domain hash is statistically close to uniform on Z_N
proves: [correctness]
status: full
---

We use the notation of the page. $N = pq$ with distinct primes, $k$ is the length of $N$ in bytes, $ed \equiv 1 \pmod{\mathrm{lcm}(p-1, q-1)}$, and $H_{\mathrm{FDH}}(M) = \mathrm{OS2IP}(\mathrm{MGF1}(M, k + 16)) \bmod N$.

**Lemma 1.** For every $y$ with $0 \le y < N$, $(y^d)^e \equiv y \pmod N$, and lines L3 compute $y^d \bmod N$.

*Proof.* This is Lemma 1 and Lemma 2 of the [correctness proof of RSA signatures](/rsa-signature/), which use only $ed \equiv 1 \pmod{\mathrm{lcm}(p-1, q-1)}$, Fermat's little theorem and the Chinese remainder theorem. $\square$

**Theorem 1 (correctness).** For every message $M$, VERIFY$((N, e), M, \mathrm{SIGN}(sk, M))$ returns valid.

*Proof.* Line L2 gives $y = H_{\mathrm{FDH}}(M)$ with $0 \le y < N$. By Lemma 1, line L3 gives $s = y^d \bmod N$, so $0 \le s < N < 256^k$ and line L4 outputs a string $S$ of exactly $k$ bytes with $\mathrm{OS2IP}(S) = s$. Line L5 passes, because $|S| = k$ and $s < N$. Line L6 computes $s^e \bmod N = y$ by Lemma 1, and $H_{\mathrm{FDH}}(M) = y$ because the hash is a deterministic function of $M$ and $N$. So line L6 returns valid. $\blacksquare$

**Lemma 2 (the hash is close to uniform).** Let $X$ be uniform on $\{0, \ldots, 2^{8(k+16)} - 1\}$ and $Y = X \bmod N$. Then the statistical distance between $Y$ and the uniform distribution on $\mathbb{Z}_N$ is less than $2^{-128}$.

*Proof.* Write $2^{8(k+16)} = aN + c$ with $0 \le c < N$. Each residue $y < c$ has $a + 1$ preimages in the range of $X$, and each $y \ge c$ has $a$ preimages. So $\Pr[Y = y] = (a + 1)/2^{8(k+16)}$ for $y < c$ and $a/2^{8(k+16)}$ for $y \ge c$. The statistical distance is $\frac{1}{2} \sum_y |\Pr[Y = y] - 1/N|$. Let $M_0 = 2^{8(k+16)}$. For $y < c$ the difference is $(a+1)/M_0 - 1/N = (N - c)/(N M_0)$, and for $y \ge c$ it is $1/N - a/M_0 = c/(N M_0)$. The sum is $c(N - c)/(N M_0) + (N - c)c/(N M_0) = 2c(N-c)/(N M_0)$, so the distance is $c(N - c)/(N M_0) \le N/(4 M_0)$, using $c(N - c) \le N^2/4$. Since $N < 2^{8k}$, this is less than $2^{8k}/2^{8k + 130} = 2^{-130} < 2^{-128}$. $\square$

When MGF1 with SHA-256 is modelled as a random oracle with output of $k + 16$ bytes, Lemma 2 shows that $H_{\mathrm{FDH}}$ is a random oracle into $\mathbb{Z}_N$ up to a statistical distance of $2^{-128}$ per query. This is the hash that the security proof on the page assumes, so a bound for a random oracle into $\mathbb{Z}_N$ carries over with an extra additive term of at most $(q_h + q_s + 1) \cdot 2^{-128}$.
