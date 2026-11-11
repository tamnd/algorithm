---
title: Honest MQV parties compute the same shared value and key
proves: [correctness]
status: full
---

We use the notation of the page: $G = \langle g \rangle$ has prime order $q$, $h \ge 1$ is an integer with $q \nmid h$, $\hat A$ has $(a, A = g^a)$ and $(x, X = g^x)$, and $\hat B$ has $(b, B = g^b)$ and $(y, Y = g^y)$, with $a, b, x, y \in [1, q - 1]$. The function avf is deterministic.

**Lemma 1 (the implicit signatures).** Let $d = \mathrm{avf}(X)$, $e = \mathrm{avf}(Y)$, $s_A = (x + d a) \bmod q$ and $s_B = (y + e b) \bmod q$. Then $X A^d = g^{s_A}$ and $Y B^e = g^{s_B}$.

*Proof.* $X A^d = g^x g^{a d} = g^{x + d a}$. Since $g$ has order $q$, $g^n = g^{n \bmod q}$ for every integer $n \ge 0$, so $X A^d = g^{s_A}$. The second claim is the same with $(y, e, b)$. $\blacksquare$

**Theorem (agreement).** Suppose the values $X$ and $Y$ arrive unchanged and the static keys in the directories are the true $A$ and $B$. If $\sigma \ne 1$, then $\hat A$'s run of MQV-KEY$(a, x, B, Y)$ and $\hat B$'s run of the mirrored algorithm return the same key $K$. Moreover $\sigma = 1$ happens for both parties or for neither.

*Proof.* Line L2 passes for both parties: $A, B, X, Y$ are powers of $g$ with exponents in $[1, q - 1]$, so they lie in $G$ and differ from 1.

Both parties compute $d = \mathrm{avf}(X)$ and $e = \mathrm{avf}(Y)$ from the same integers, so they get the same $d$ and $e$ at line L3.

$\hat A$ computes at line L5, by Lemma 1,
$$\sigma_A = (Y B^e)^{h s_A} = (g^{s_B})^{h s_A} = g^{h s_A s_B}.$$
$\hat B$ computes, by Lemma 1 again,
$$\sigma_B = (X A^d)^{h s_B} = (g^{s_A})^{h s_B} = g^{h s_A s_B}.$$
So $\sigma_A = \sigma_B$. In particular the test of line L6 gives the same result for both. If it passes, both apply KDF at line L7 to the same tuple $(\sigma, \hat A, \hat B, X, Y)$, with $\hat A$ as the initiator in both runs, and so return the same $K$. $\blacksquare$

**When is $\sigma = 1$?** Since $g$ has prime order $q$, $\sigma = g^{h s_A s_B} = 1$ if and only if $q \mid h s_A s_B$, that is (as $q \nmid h$ and $q$ is prime), if and only if $s_A = 0$ or $s_B = 0$. For a fixed $a$ and $X$, $s_A = 0$ means $x \equiv -d a \pmod q$, which happens for at most one value of $x$; for uniform $x$ this has probability at most $1/(q - 1)$. So line L6 fails only with negligible probability in honest runs, and when it does, both parties fail together.
