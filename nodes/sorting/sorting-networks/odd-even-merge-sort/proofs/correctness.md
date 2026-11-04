---
title: Odd-even merge sort sorts each input
proves: [correctness]
status: full
---

The calls of OEM-SORT and ODD-EVEN-MERGE make the same comparators on each input, so they form a comparator network of standard comparators. Each comparator only exchanges two items, so the output is a permutation of the input. By the [zero-one principle](/zero-one-principle/) it is enough to show that the output is sorted for each input of zeros and ones.

For a call ODD-EVEN-MERGE$(A, lo, m, r)$ with $L = m / r \ge 2$, write $x_t = A[lo + t r]$ for $t = 0, \ldots, L - 1$. This is the *subsequence of the call*. Its *first half* is $x_0, \ldots, x_{L/2 - 1}$ and its *second half* is $x_{L/2}, \ldots, x_{L-1}$. Each comparator of the call has both wires in the subsequence, so the call changes no other entry of $A$.

**Lemma 1.** Let $y = 0^{a} 1^{p - a}$ be a sorted 0-1 sequence of even length $p$. Then the items $y_0, y_2, \ldots, y_{p-2}$ at even places hold $\lceil a / 2 \rceil$ zeros and are sorted, and the items $y_1, y_3, \ldots, y_{p-1}$ at odd places hold $\lfloor a / 2 \rfloor$ zeros and are sorted.

*Proof.* A subsequence of a sorted sequence is sorted. The zeros are at places $0, \ldots, a - 1$. Of these, $\lceil a/2 \rceil$ are even and $\lfloor a/2 \rfloor$ are odd. $\square$

**Lemma 2 (merge).** If the first half and the second half of the subsequence of a call ODD-EVEN-MERGE$(A, lo, m, r)$ are sorted 0-1 sequences, then after the call the subsequence is sorted.

*Proof.* By induction on $L = m / r$, which is a power of 2.

If $L = 2$, then $s = 2r = m$, so line L7 fails and line L11 compares $x_0$ and $x_1$. After it, $x_0 \le x_1$.

Let $L \ge 4$ and $p = L / 2$, which is even. Let the first half have $a$ zeros and the second half $b$ zeros. The call of line L8 has the subsequence $x_0, x_2, \ldots, x_{L-2}$ of stride $s$. Its first half is the even places of the first half of $x$, and its second half is the even places of the second half of $x$, because $p$ is even. By Lemma 1 both are sorted. So by the induction hypothesis, after line L8 the even places of $x$ are sorted and hold $E = \lceil a/2 \rceil + \lceil b/2 \rceil$ zeros. In the same way, the call of line L9 has the subsequence $x_1, x_3, \ldots, x_{L-1}$, and after it the odd places of $x$ are sorted and hold $O = \lfloor a/2 \rfloor + \lfloor b/2 \rfloor$ zeros. The two calls have disjoint wires, so the order of lines L8 and L9 does not matter. Now $x_{2t} = 0$ if and only if $t < E$, and $x_{2t+1} = 0$ if and only if $t < O$. Also $E - O \in \{0, 1, 2\}$.

- If $E = O$, the zeros are at the places $0, \ldots, 2E - 1$, so $x$ is sorted.
- If $E = O + 1$, the zeros are at the places $0, \ldots, 2E - 2$, so $x$ is sorted.
- If $E = O + 2$, the zeros are at the places $0, \ldots, 2E - 4$ and at the place $2E - 2$, and the place $2E - 3$ holds a 1. So $x$ is sorted except that $x_{2E - 3} = 1$ and $x_{2E - 2} = 0$. Here $E \ge 2$ and $2E - 2 \le L - 2$, because the even places hold at most $L/2$ zeros.

Line L10 runs over $i = lo + r + 2 r t$ for $t = 0, 1, \ldots$ while $i + r < lo + m$, and compares $A[i] = x_{2t + 1}$ with $A[i + r] = x_{2t + 2}$. So it applies the comparators $[2t + 1 : 2t + 2]$ of the subsequence for $t = 0, \ldots, L/2 - 2$. These pairs are disjoint. In the first two cases each pair is already in order, and nothing changes. In the third case the pair $(2E - 3, 2E - 2)$ is one of them, with $t = E - 2$, and its comparator exchanges the 1 and the 0. Each other pair is in order. After line L10, $x$ is sorted in each case. $\square$

**Theorem.** For each power of 2 $m$ and each $lo$, OEM-SORT$(A, lo, m)$ sorts $A[lo \ldots lo + m - 1]$ for each 0-1 content of this part, and it changes no other entry of $A$. So by the zero-one principle, OEM-SORT$(A, 0, n)$ sorts each array of $n$ items from a totally ordered set.

*Proof.* By induction on $m$. If $m = 1$, line L1 returns. Let $m \ge 2$ and $h = m/2$. By the induction hypothesis, lines L3 and L4 sort $A[lo \ldots lo + h - 1]$ and $A[lo + h \ldots lo + m - 1]$ and change nothing else. The call of line L5 has $r = 1$, so its subsequence is $A[lo \ldots lo + m - 1]$, and its two halves are sorted. By Lemma 2, after line L5 the part is sorted. $\blacksquare$
