---
title: Rabin-Karp outputs exactly the occurrences of the pattern
proves: [correctness, termination]
status: full
---

**Claim.** For every text $T[0 \ldots n-1]$, every pattern $P[0 \ldots m-1]$ and every value of the base $r$ drawn at line L3, RABIN-KARP stops and outputs, in increasing order, exactly the shifts $s$ with $0 \le s \le n - m$ and $T[s \ldots s+m-1] = P$ (all $s$ from $0$ to $n$ when $m = 0$).

**Notation.** All hash values are in $\{0, \ldots, p-1\}$. For a string $x$ of length $\ell$, $h(x) = \sum_{i=0}^{\ell-1} c(x_i)\, r^{\ell-1-i} \bmod p$, and $t_s = h(T[s \ldots s+m-1])$ for $0 \le s \le n - m$.

**Lemma 1 (Horner's rule).** After line L6, $hp = h(P)$ and $ht = t_0$.

*Proof.* Let $v_i$ be the value of $hp$ after $i$ passes, with $v_0 = 0$. By induction on $i$, $v_i = \sum_{j=0}^{i-1} c(P[j])\, r^{i-1-j} \bmod p$: the case $i = 0$ is the empty sum, and $v_{i+1} = v_i r + c(P[i]) = \sum_{j=0}^{i-1} c(P[j])\, r^{i-j} + c(P[i]) = \sum_{j=0}^{i} c(P[j])\, r^{i-j}$ modulo $p$. For $i = m$ this is $h(P)$. The same argument with $T[0 \ldots m-1]$ gives $ht = t_0$. $\square$

**Lemma 2 (the window update).** For $0 \le s < n - m$, $\big((t_s - c(T[s])\, R)\, r + c(T[s+m])\big) \bmod p = t_{s+1}$, where $R = r^{m-1} \bmod p$.

*Proof.* Work in the ring of integers modulo $p$. By definition $t_s = \sum_{j=0}^{m-1} c(T[s+j])\, r^{m-1-j}$, and the term with $j = 0$ is $c(T[s])\, r^{m-1} = c(T[s])\, R$. So

$$(t_s - c(T[s])\, R)\, r + c(T[s+m]) = \sum_{j=1}^{m-1} c(T[s+j])\, r^{m-j} + c(T[s+m]).$$

Put $j = k + 1$. The sum becomes $\sum_{k=0}^{m-2} c(T[s+1+k])\, r^{m-1-k}$, and the last term is the term $k = m - 1$ of $\sum_{k=0}^{m-1} c(T[s+1+k])\, r^{m-1-k} = t_{s+1}$. The reduction modulo $p$ returns the representative in $\{0, \ldots, p-1\}$, which is $t_{s+1}$. $\square$

**Lemma 3 (loop invariant).** If $1 \le m \le n$, then at line L8 in the pass with shift $s$, $ht = t_s$ and $hp = h(P)$.

*Proof.* By induction on $s$. For $s = 0$, this is Lemma 1. Line L4 sets $R = r^{m-1} \bmod p$, and no line changes $hp$ or $R$ after line L6. If the claim holds for $s < n - m$, then line L10 is true and line L11 sets $ht$ to the value of Lemma 2, which is $t_{s+1}$. $\square$

**Lemma 4 (the test at one shift).** If $1 \le m \le n$ and $0 \le s \le n - m$, the pass for $s$ outputs $s$ if and only if $T[s \ldots s+m-1] = P$.

*Proof.* If $T[s \ldots s+m-1] = P$, then the two strings are the same, so $t_s = h(P)$, and by Lemma 3 the test of line L8 is true. Line L9 compares the window with $P$ character by character, finds them equal, and outputs $s$. If $T[s \ldots s+m-1] \ne P$, then either the test of line L8 is false, or it is true and line L9 finds a position where the window and $P$ differ. In both cases nothing is output for $s$. The pass for $s$ outputs no other shift. $\square$

**Termination.** Each loop runs over a finite range of integers: line L6 runs $m$ times, line L7 runs $n - m + 1$ times, and the comparison of line L9 looks at most at $m$ positions. So the algorithm stops.

**Theorem.** The claim holds.

*Proof.* If $m = 0$, line L1 outputs $0, 1, \ldots, n$, and the empty pattern occurs at exactly these shifts. If $m > n$, no shift $s$ satisfies $0 \le s \le n - m$, and line L2 stops with no output. Otherwise, line L7 visits each $s$ from $0$ to $n - m$ once, in increasing order, and by Lemma 4 it outputs $s$ exactly when $P$ occurs at $s$. The proof does not use any property of $r$ or of $p$, so the output is correct for every base. $\blacksquare$

**Remark (where randomness enters).** The choice of $r$ affects only how often line L9 runs on a window that is not an occurrence. For a fixed $T$ and $P$ and a shift $s$ that is not an occurrence, the window and $P$ are distinct strings of the same length $m$, and by the polynomial hash collision bound $\Pr_r[t_s = h(P)] \le (m-1)/p$ when $p$ is prime and $r$ is uniform on $\{0, \ldots, p-1\}$. This gives the expected time on the main page.
