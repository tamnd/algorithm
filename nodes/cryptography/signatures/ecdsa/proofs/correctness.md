---
title: Honest ECDSA signatures verify, low-s signatures verify, and recovery returns the key
proves: [correctness]
status: full
---

Let $G$ be a point of prime order $n$ on a curve $E$ over $\mathbb{F}_p$, let $d \in [1, n-1]$ and $Q = dG$. Because $G$ has order $n$, $aG = bG$ if and only if $a \equiv b \pmod n$. All the integers below are taken mod $n$ when they multiply a point.

**Lemma 1 (honest signatures verify).** For every message $m$, the output $(r, s)$ of lines L1 to L7 passes lines L8 to L13.

*Proof.* Lines L4 and L6 give $r, s \in [1, n-1]$, so line L8 does not reject. Line L9 computes the same $z$ as line L1. Since $s \ne 0$ and $n$ is prime, $s$ has an inverse $w$ mod $n$. From line L5, $s \equiv k^{-1}(z + r d)$, so $k \equiv w (z + r d) \pmod n$. Line L10 gives $u_1 \equiv z w$ and $u_2 \equiv r w$. Then

$$X = u_1 G + u_2 Q = (z w) G + (r w)(d G) = \big(w (z + r d)\big) G = k G.$$

Since $k \in [1, n-1]$, $kG \ne O$, so line L12 does not reject. By line L3, $x(kG) = x_1$, and by line L4, $x_1 \bmod n = r$. So line L13 returns true. $\square$

**Lemma 2 (the low-s twin).** If $(r, s)$ passes verification for $m$ and $Q$, so does $(r, n - s)$.

*Proof.* $n - s \in [1, n-1]$, so line L8 passes. Its inverse is $-w$, so the new $u_1, u_2$ are $-u_1, -u_2$ and the new point is $-X$. A point and its negation have the same $x$ coordinate, and $-X \ne O$ because $X \ne O$. So line L13 gives the same answer as before. $\square$

Lemma 2 shows that the low-s rule, which outputs $\min(s, n - s)$, keeps honest signatures valid, and that a verifier that asks $s \le (n-1)/2$ accepts exactly one of the two twins. Since $n$ is odd, $s \ne n - s$, so exactly one of them is at most $(n-1)/2$.

**Lemma 3 (public key recovery).** Let $(r, s)$ come from lines L1 to L7 with the point $R = kG$, and let $v$ encode the parity of $y(R)$ and the integer $j$ with $x(R) = r + j n$. Then the point $R'$ with $x(R') = r + jn$ and the parity of $v$ equals $R$, and $r^{-1}(s R' - zG) = Q$.

*Proof.* At most two points of $E$ have a given $x$ coordinate, and they are $P$ and $-P$ with $y$ coordinates $y$ and $p - y$. Since $p$ is odd and $y \ne 0$ (a point with $y = 0$ has order 2, and $n$ is an odd prime), exactly one of them has an odd $y$. So the $x$ coordinate and the parity fix $R$, and $R' = R$. From line L5, $s k \equiv z + r d \pmod n$, so $s R - z G = (s k - z) G = (r d) G = r Q$. Since $r \in [1, n-1]$ it has an inverse mod $n$, and $r^{-1}(s R - z G) = Q$. If the signer replaced $s$ by $n - s$ and flipped the parity in $v$, the same argument applies to the nonce $n - k$, whose point is $-R$. $\blacksquare$
