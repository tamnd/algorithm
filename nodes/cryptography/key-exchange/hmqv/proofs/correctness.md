---
title: Honest HMQV parties compute the same key
proves: [correctness]
status: full
---

We use the notation of the page. $G = \langle g \rangle$ has prime order $q$. $\hat A$ has $(a, A = g^a)$ and $(x, X = g^x)$, $\hat B$ has $(b, B = g^b)$ and $(y, Y = g^y)$, with $a, b, x, y \in [1, q - 1]$. $\bar H$ and $H$ are deterministic functions.

**Lemma 1.** For any integers $u$ and $v \ge 0$, $g^u \cdot (g^v)^{c} = g^{(u + c v) \bmod q}$ for every integer $c \ge 0$.

*Proof.* $g^u (g^v)^c = g^{u + cv}$, and since $g$ has order $q$, $g^n = g^{n \bmod q}$ for every $n \ge 0$. $\blacksquare$

**Theorem.** Suppose $X$ and $Y$ arrive unchanged, $\hat A$ uses the true $B$, $\hat B$ uses the true $A$, $\hat A$ runs HMQV-KEY$(\hat A, \hat B, a, x, B, Y)$ and $\hat B$ runs HMQV-KEY$(\hat B, \hat A, b, y, A, X)$. Then both return the same key $K$.

*Proof.* *Line L2.* $A$, $B$, $X$ and $Y$ are powers of $g$ with exponents in $[1, q - 1]$, so they lie in $G \setminus \{1\}$ and neither party fails.

*Line L3.* $\hat A$ computes $d = \bar H(X, \hat B)$ and $e = \bar H(Y, \hat A)$. $\hat B$, in the role of the first party, computes $d' = \bar H(Y, \hat A)$ for its own value and $e' = \bar H(X, \hat B)$ for the peer's value. So $d' = e$ and $e' = d$: both parties use $d$ with $X$ and $a$, and $e$ with $Y$ and $b$.

*Lines L4 and L5.* Let $s_A = (x + d a) \bmod q$ and $s_B = (y + e b) \bmod q$. $\hat A$ computes
$$\sigma_A = (Y B^e)^{s_A} = (g^{s_B})^{s_A} = g^{s_A s_B}$$
by Lemma 1, and $\hat B$ computes
$$\sigma_B = (X A^d)^{s_B} = (g^{s_A})^{s_B} = g^{s_A s_B}.$$
So $\sigma_A = \sigma_B$.

*Line L6.* Both apply the same function $H$ to the same $\sigma$, so they return the same $K$. $\blacksquare$

**Remark.** The proof uses only that $\bar H$ is a function. The security properties on the page need $\bar H$ and $H$ to behave as random oracles, which this proof does not cover.
