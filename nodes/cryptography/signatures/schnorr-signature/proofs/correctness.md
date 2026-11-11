---
title: Honest Schnorr signatures verify, in both forms and in BIP 340
proves: [correctness]
status: full
---

Let $G$ be a cyclic group of prime order $q$ with generator $g$, so that $g^a = g^b$ if and only if $a \equiv b \pmod q$. Let $x \in [1, q-1]$ and $y = g^x$.

**Lemma 1 (the $(R, s)$ form).** For every message $m$ and every nonce $k \in [1, q-1]$, the output $(R, s)$ of lines L1 to L5 passes lines L6 to L8.

*Proof.* Line L2 gives $R = g^k \in G$, and line L4 gives $s \in [0, q-1]$, so line L6 does not reject. Line L7 recomputes $e = H(R \| m) \bmod q$, the same value as line L3, because $H$ is a function and its inputs are equal. By line L4 there is an integer $j$ with $s = k + e x - j q$. Then $g^s = g^k \cdot (g^x)^e \cdot (g^q)^{-j} = R \cdot y^e$, because $g^q = 1$. So line L8 returns true. $\square$

**Lemma 2 (the $(e, s)$ form).** Let $(R, s)$ be an honest signature and $e = H(R \| m) \bmod q$. The verifier of the $(e, s)$ form computes $R' = g^s y^{-e}$ and accepts if $e = H(R' \| m) \bmod q$. It accepts $(e, s)$.

*Proof.* By Lemma 1, $g^s = R y^e$, so $R' = g^s y^{-e} = R$. Then $H(R' \| m) \bmod q = H(R \| m) \bmod q = e$. $\square$

**Lemma 3 (the forms are equivalent).** For a fixed $y$ and $m$, the map $(R, s) \mapsto (H(R \| m) \bmod q, s)$ sends the valid $(R, s)$ signatures onto the valid $(e, s)$ signatures, and $(e, s) \mapsto (g^s y^{-e}, s)$ is its inverse on them.

*Proof.* If $(R, s)$ is valid then $(e, s)$ with $e = H(R \| m) \bmod q$ is valid by the argument of Lemma 2, which used only the equation $g^s = R y^e$. If $(e, s)$ is valid, set $R = g^s y^{-e}$. Then $e = H(R \| m) \bmod q$ by the check, and $g^s = R y^e$, so $(R, s)$ is valid and maps back to $(e, s)$. Starting from a valid $(R, s)$, the map and then the inverse give $g^s y^{-e} = R$. $\square$

**Lemma 4 (BIP 340).** Let $d' \in [1, n-1]$ be a secret key of secp256k1, of prime order $n$, with $P' = d' G$. Let the signer follow lines L1 to L8 of the code, and let the verifier follow lines L9 to L13. If $k_0 \ne 0$, the verifier accepts.

*Proof.* The point $P'$ and its negation $-P' = (n - d') G$ have the same $x$ coordinate and $y$ coordinates $y$ and $p - y$. Since $p$ is odd, exactly one of them is even, unless $y = 0$, which does not happen because the curve has no point of order 2 ($n$ is odd). Line L2 sets $d = d'$ or $d = n - d'$ so that $P = d G$ has an even $y$. Line L9 of the verifier lifts $x(P)$ to the point with this $x$ and an even $y$, which is $P$, because the curve equation has at most two points with a given $x$.

In the same way line L6 sets $k = k_0$ or $k = n - k_0$ so that $R = k G$ has an even $y$. The signature is $r = x(R)$ and $s = (k + e d) \bmod n$ with $e$ computed from $x(R)$, $x(P)$ and $m$. The verifier hashes the same 96 bytes, so it gets the same $e$. Now $r < p$ and $s < n$, so line L10 does not reject. Line L12 computes $sG - eP = (k + e d) G - e d G = k G = R$, using that $G$ has order $n$. This point is not the point at infinity because $k \ne 0 \bmod n$, it has even $y$, and its $x$ coordinate is $r$. So line L13 does not reject, and the verifier accepts. $\blacksquare$

**Uniqueness of $s$.** In the $(R, s)$ form, for fixed $y$, $m$ and $R$, the value $e$ is fixed, and the equation $g^s = R y^e$ fixes $s$ mod $q$. Since the verifier asks $s \in [0, q-1]$, at most one $s$ is valid for each $R$. This is the algebraic fact behind the strong unforgeability claim of the page.
