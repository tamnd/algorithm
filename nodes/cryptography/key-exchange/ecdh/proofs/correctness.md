---
title: Honest ECDH parties pass validation and get the same x-coordinate
proves: [correctness]
status: full
---

We use the notation of the page. $E(\mathbb{F}_p)$ is a finite commutative group under point addition, with identity $O$ and order $hn$, where $n$ is prime and $\gcd(h, n) = 1$. $G$ has order $n$. For an integer $k$ and a point $P$, $kP$ is the $k$-fold sum, with $0P = O$ and $(-k)P = -(kP)$.

**Lemma 1 (scalar multiplication).** For all integers $a$, $b$ and every point $P$, $a(bP) = (ab)P$. Also $kP = O$ for every multiple $k$ of the order of $P$, and if $P$ has prime order $n$ then $kP = O$ exactly when $n \mid k$.

*Proof.* The map $k \mapsto kP$ is a group homomorphism from $\mathbb{Z}$ to $E(\mathbb{F}_p)$, because the group is commutative; this gives $a(bP) = (ab)P$ by induction on $|a|$. Its kernel is the set of multiples of the order of $P$. $\blacksquare$

**Lemma 2 (honest points pass VALIDATE).** If $1 \le d \le n - 1$ and $Q = dG$ is computed in line L2, then lines L4 to L7 do not fail.

*Proof.* Since $n$ is prime and $n \nmid d$, Lemma 1 gives $Q \ne O$, so line L4 passes. The group law outputs coordinates reduced modulo $p$, so line L5 passes. The sum of two points of $E$ lies on $E$, so $Q$ satisfies the curve equation and line L6 passes. Finally $nQ = (nd)G = d(nG) = dO = O$ by Lemma 1, so line L7 passes. $\blacksquare$

**Theorem (agreement).** Let Alice and Bob run lines L1 to L3 and get $(d_A, Q_A)$ and $(d_B, Q_B)$. Then ECC-CDH$(d_A, Q_B)$ and ECC-CDH$(d_B, Q_A)$ both pass line L9 and return the same string.

*Proof.* By Lemma 2, both received points pass validation. Line L8 of Alice's call computes

$$(h d_A) Q_B = (h d_A)(d_B G) = (h d_A d_B) G,$$

and Bob's call computes $(h d_B)(d_A G) = (h d_A d_B) G$ by Lemma 1. These are the same point $P$. Since $n$ is prime, $n \nmid d_A$, $n \nmid d_B$ and $n \nmid h$, we have $n \nmid h d_A d_B$, so $P \ne O$ by Lemma 1 and line L9 passes. Line L10 encodes the $x$-coordinate of the same point with the same fixed length, so the outputs are equal. $\blacksquare$

**Theorem (validated points give a point of order n).** If $Q$ passes lines L4 to L7 and $1 \le d \le n - 1$, then $P = (hd)Q$ has order $n$.

*Proof.* Lines L4 and L6 give $Q \in E(\mathbb{F}_p) \setminus \{O\}$, and line L7 gives $nQ = O$, so the order of $Q$ divides $n$ and is not 1; it is $n$. Since $n \nmid hd$, Lemma 1 gives $P \ne O$, and $nP = (hd)(nQ) = O$, so $P$ has order $n$. $\blacksquare$

**Remark (partial validation when $h = 1$).** If $h = 1$ then $\#E(\mathbb{F}_p) = n$ is prime, so every $Q \ne O$ on $E$ has order $n$ by Lagrange's theorem, and line L7 holds automatically after lines L4 to L6. This is why partial validation suffices for P-256 and P-384. $\blacksquare$
