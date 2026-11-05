---
title: Manacher's algorithm computes the maximal palindrome at every center
proves: [correctness]
status: full
---

Let $s = s[0..n-1]$, $m = 2n + 1$, and $T[0..m-1]$ the implicit string with $T[2k] = \#$ and $T[2k+1] = s[k]$, where $\#$ is not a symbol of $s$. Indices are 0-based. For $0 \le c \le m - 1$ let $\rho(c)$ be the largest $r \ge 0$ with $c - r \ge 0$, $c + r \le m - 1$ and $T[c-r..c+r]$ a palindrome. Write $W(c, q)$ for the window $T[c-q..c+q]$.

**Fact 1 (nesting).** If $W(c, q)$ is a palindrome and $q \ge 1$, then $W(c, q-1)$ is a palindrome. So $W(c, q)$ is a palindrome if and only if $q \le \rho(c)$, and if $q < \rho(c)$, then $c - q - 1 \ge 0$, $c + q + 1 \le m - 1$ and $T[c-q-1] = T[c+q+1]$.

*Proof.* Removing the first and the last symbol of a palindrome leaves a palindrome. The second claim follows, because $W(c, \rho(c))$ is a palindrome and contains $W(c, q)$ for $q \le \rho(c)$, and its symbols at distance $q + 1$ from $c$ are equal. $\square$

**Fact 2 (mirror).** Let $X = T[a..b]$ be a palindrome, and $x \mapsto a + b - x$ its mirror map. If $W(x, q)$ lies inside $[a, b]$, then $W(a + b - x, q)$ is the reversal of $W(x, q)$. So one is a palindrome if and only if the other is.

*Proof.* For $|d| \le q$, $T[x + d] = T[a + b - x - d]$ because $X$ is a palindrome. So the window at $a + b - x$, read from left to right, is the window at $x$ read from right to left. $\square$

**Lemma (mirror lemma).** Let $c < i < r$ with $r = c + \rho(c)$, and $j = 2c - i$. Then $\rho(i) \ge \min(\rho(j), r - i)$. If $\rho(j) < r - i$, then $\rho(i) = \rho(j)$. If $\rho(j) > r - i$, then $\rho(i) = r - i$.

*Proof.* Let $L = c - \rho(c) = 2c - r$, so $X = T[L..r]$ is a palindrome with mirror map $x \mapsto 2c - x$, which sends $i$ to $j$. Since $c < i < r$, we have $L < j < c$. Let $q = \min(\rho(j), r - i)$. Then $W(i, q)$ lies inside $[i - (r - i), r] \subseteq [L, r]$, because $i - (r - i) = 2i - r > 2c - r = L$. The window $W(j, q)$ is a palindrome by Fact 1, so by Fact 2, $W(i, q)$ is a palindrome, and $\rho(i) \ge q$.

*Case $\rho(j) < r - i$.* Suppose $\rho(i) \ge \rho(j) + 1$. The window $W(i, \rho(j) + 1)$ is a palindrome, and it lies inside $[L, r]$ because $\rho(j) + 1 \le r - i$. By Fact 2, $W(j, \rho(j) + 1)$ is a palindrome, which contradicts the definition of $\rho(j)$. So $\rho(i) = \rho(j)$.

*Case $\rho(j) > r - i$.* Let $d = r - i$. If $r = m - 1$, then $i + d + 1 = m$ is outside $T$ and $\rho(i) \le d$. Otherwise $L \ge 1$, because $j - \rho(j) \ge 0$ and $L - 1 = j - d - 1 \ge j - \rho(j)$. By the maximality of $\rho(c)$, $T[L-1] \ne T[r+1]$. Now $L - 1 = j - (d + 1)$, and since $d + 1 \le \rho(j)$, the palindrome $W(j, \rho(j))$ gives $T[L-1] = T[j + d + 1]$. The position $j + d + 1 = 2c - 2i + r + 1$ lies in $[L, r]$, because $i > c$ gives $2c - 2i + 1 \le 0$. Its mirror in $X$ is $2c - (j + d + 1) = i - d - 1$, so $T[j + d + 1] = T[i - d - 1]$. Together, $T[i - d - 1] = T[L - 1] \ne T[r + 1] = T[i + d + 1]$, so $W(i, d+1)$ is not a palindrome, and $\rho(i) = d$ by Fact 1. $\square$

**Invariant.** At the start of the iteration of line L4 with index $i$:

> **(I)** $P[k] = \rho(k)$ for all $k < i$, and $P[k] = 0$ for $k \ge i$. If $i = 0$, then $c = r = 0$. If $i \ge 1$, then $c < i$, $r = c + \rho(c)$, and $r = \max_{k < i} (k + \rho(k))$.

At $i = 0$, lines L2 and L3 make (I) true. Assume (I) at $i$.

*Line L5.* If $i < r$, then $i \ge 1$, so $c < i < r = c + \rho(c)$, and $2c - i < c < i$, so $P[2c - i] = \rho(2c - i)$. Line L5 sets $P[i] = \min(\rho(2c - i), r - i)$, which is at most $\rho(i)$ by the mirror lemma. If $i \ge r$, $P[i]$ stays 0. In both cases $W(i, P[i])$ is a palindrome and $P[i] \le \rho(i)$.

*Lines L6 and L7.* The test of line L6 is "$W(i, P[i] + 1)$ lies in $T$ and its two new ends are equal", and since $W(i, P[i])$ is a palindrome, this is the test "$W(i, P[i] + 1)$ is a palindrome". By Fact 1 it succeeds exactly while $P[i] < \rho(i)$. So the loop ends with $P[i] = \rho(i)$. It ends, because $P[i]$ grows and is bounded by $\rho(i)$.

*Line L8.* If $i + \rho(i) > r$, line L8 sets $c = i$ and $r = i + \rho(i)$; otherwise it keeps them. In both cases $r = \max_{k \le i}(k + \rho(k))$ and $r = c + \rho(c)$ with $c \le i < i + 1$. For $i = 0$, $\rho(0) = 0$ and $c = r = 0$, which is also of this form. So (I) holds at $i + 1$.

At the end of the loop, (I) with $i = m$ gives $P = \rho$, which line L9 returns.

**From $T$ to $s$.** Fix $c$ and let $\rho = \rho(c)$.

*Step 1: the window $W(c, \rho)$ ends on separators.* Suppose $c - \rho$ is odd. Then $c + \rho$ is odd too, so $1 \le c - \rho$ and $c + \rho \le 2n - 1$, and both $c - \rho - 1$ and $c + \rho + 1$ are even positions inside $T$. They hold $\#$, so $W(c, \rho + 1)$ is a palindrome, a contradiction. So $c - \rho = 2a$ and $c + \rho = 2b$ for integers $0 \le a \le b \le n$, with $a + b = c$ and $b - a = \rho$.

*Step 2: windows with separator ends.* For $0 \le a \le b \le n$, the string $T[2a..2b]$ is a palindrome if and only if $s[a..b-1]$ is a palindrome. The mirror of $2a..2b$ sends even positions to even positions, where $T$ is always $\#$, and the odd position $2k + 1$, which holds $s[k]$, to $2a + 2b - 2k - 1 = 2(a + b - 1 - k) + 1$, which holds $s[a + b - 1 - k]$. So $T[2a..2b]$ is a palindrome exactly when $s[k] = s[a + b - 1 - k]$ for $a \le k \le b - 1$, which is the definition of a palindrome for $s[a..b-1]$.

*Step 3.* Each palindrome $s[i..j]$ with $i \le j + 1$ corresponds by Step 2 to the palindrome $T[2i..2j+2]$ with center $c = i + j + 1$ and radius $j - i + 1$. So the palindromes of $s$ with center $c$, that is with $i + j + 1 = c$, are the windows $W(c, q)$ with even ends, and their lengths are the radii $q \equiv c \pmod 2$ with $q \le \rho(c)$, by Fact 1. By Step 1, $\rho(c)$ itself is such a radius. So the longest palindrome of $s$ with center $c$ has length $P[c] = \rho(c)$ and is $s[a..b-1]$ with $a = (c - P[c])/2$ and $b = (c + P[c])/2$. And for $0 \le i \le j \le n - 1$, $s[i..j]$ is a palindrome if and only if $j - i + 1 \le P[i + j + 1]$. $\blacksquare$
