---
title: The bitmap allocator returns the first fit and frees exactly the block
proves: [correctness, termination]
status: full
---

**Setting.** Units are numbered $0$ to $h - 1$, and words hold $w$ bits. Unit $x$ is bit $x \bmod w$ of word $\lfloor x / w \rfloor$. The units $h$ to $w \lceil h/w \rceil - 1$ are *padding*. Let $\mathcal{B}$ be the set of allocated blocks, each an interval $[a, a + n)$ of units. A unit is *free* when it is in no block of $\mathcal{B}$ and is not padding.

**Invariant (I).** (1) USED$[x] = 1$ exactly when $x$ is padding or lies in a block of $\mathcal{B}$; (2) START$[x] = 1$ exactly when $x$ is the first unit of a block of $\mathcal{B}$; (3) the blocks of $\mathcal{B}$ are pairwise disjoint.

At the start, $\mathcal{B}$ is empty, USED holds 1 only on the padding, and START is all 0, so (I) holds.

**Lemma 1 (RUN-OF-ONES).** For a $w$-bit word $f$ and $1 \le n \le w$, bit $j$ of RUN-OF-ONES$(f, n)$ is 1 exactly when $j + n \le w$ and bits $j$ to $j + n - 1$ of $f$ are all 1.

*Proof.* Let $k$ be the sum of the shifts done so far. We show that bit $j$ of $r$ is the AND of the bits $j$ to $j + k$ of $f$, where bits at positions $w$ and above count as 0. At the start $k = 0$ and $r = f$. A step with shift $t$ sets bit $j$ of $r$ to the AND of the windows $[j, j + k]$ and $[j + t, j + t + k]$. The shifts are $1, 2, 4, \ldots$, capped at the remaining amount, so before a step with shift $t$ we have $k = 1 + 2 + \cdots + t/2 = t - 1$ for the doubling steps, and $k \ge t - 1$ for the capped last step. So $t \le k + 1$, the two windows touch or overlap, and their union is $[j, j + t + k]$. The new sum of shifts is $k + t$, so the claim holds after the step. The loop ends when the sum of shifts is $n - 1$, so bit $j$ is the AND of bits $j$ to $j + n - 1$. The shift fills the top with 0, so this AND is 0 when $j + n - 1 \ge w$. The loop runs $\lceil \lg n \rceil$ times, because the shifts double until their sum reaches $n - 1$. $\square$

**Lemma 2 (the meaning of run).** Assume (I). At the start of pass $i$ of the loop of line L2, the variable run is the number of free units in a row that end at unit $w i - 1$, that is, the largest $\rho$ such that the units $w i - \rho$ to $w i - 1$ are free, if the scan has not returned before.

*Proof.* At $i = 0$, run $= 0$, and there is no unit before 0. Assume the claim at the start of pass $i$. By (I.1), the 1 bits of $f = $ NOT USED$[i]$ are the free units of word $i$. If $f$ is all ones, the whole word is free, and the free run that ends at $w(i + 1) - 1$ is the old run plus $w$ units. Otherwise, LZ(NOT $f$) is the number of 1 bits of $f$ at the top of the word before its highest 0 bit, so it is the number of free units in a row that end at $w(i + 1) - 1$, and that run stops inside word $i$. Line L7 sets run to exactly these values. $\square$

**Lemma 3 (first fit).** Assume (I). BITMAP-MALLOC$(n)$ returns the least $a$ such that the units $a$ to $a + n - 1$ are all free, and FAIL if no such $a$ exists.

*Proof.* Call such an $a$ a *fit*, and let $e(a) = \lfloor (a + n - 1)/w \rfloor$ be the word of its last unit. If $a \le a'$ then $e(a) \le e(a')$. Padding units are not free, so a fit never covers them. Note that NOT $f$ is USED$[i]$, so TZ(NOT $f$) is the number of free units at the bottom of word $i$.

*Step 1: every returned value is a fit $a$ with $e(a) \le i$, where $i$ is the pass.* If line L4 returns $a = w i - \text{run}$, then by Lemma 2 the units from $a$ to $w i - 1$ are free, and the units from $w i$ to $w i + n - \text{run} - 1$, if $n > \text{run}$, are free at the bottom of word $i$, because TZ(NOT $f$) $\ge n - \text{run}$. So $a$ is a fit, and its last unit is in word $i$ or before. If line L6 returns $a = w i + $ TZ$(r)$, then by Lemma 1 the units $a$ to $a + n - 1$ are free and lie in word $i$, so $a$ is a fit with $e(a) = i$.

*Step 2: the scan returns the least fit.* If no fit exists, no line returns by Step 1, and line L8 returns FAIL. Otherwise let $a^*$ be the least fit and $i^* = e(a^*)$. No pass $i < i^*$ returns: it would return a fit $a$ with $e(a) \le i < i^*$, so $a < a^*$, which contradicts the choice of $a^*$. So the scan reaches pass $i^*$, and Lemma 2 applies there. There are two cases.

- $a^* < w i^*$: the fit starts in an earlier word. The units from $a^*$ to $w i^* - 1$ are free, so run $\ge w i^* - a^* > 0$ by Lemma 2. The units from $w i^*$ to $a^* + n - 1$ are free, so TZ(NOT $f$) $\ge a^* + n - w i^*$. So run $+$ TZ(NOT $f$) $\ge n$, and line L4 returns $w i^* - \text{run} \le a^*$. By Step 1 this is a fit, so it equals $a^*$.
- $a^* \ge w i^*$: the fit lies inside word $i^*$, so $n \le w$. If line L4 returned, it would return a fit below $w i^* \le a^*$, which is not possible. By Lemma 1, bit $a^* - w i^*$ of $r$ is 1, so line L6 returns $w i^* + $ TZ$(r) \le a^*$. By Step 1 this is a fit, so it equals $a^*$. $\square$

**Lemma 4 (malloc keeps (I)).** If BITMAP-MALLOC returns $a$, then after MARK$(a, n)$, (I) holds with $[a, a + n)$ added to $\mathcal{B}$.

*Proof.* By Lemma 3 the units of $[a, a + n)$ are free, so the new block is disjoint from the others and from the padding, which gives (I.3). MARK sets exactly their USED bits and the START bit of $a$, which gives (I.1) and (I.2). $\square$

**Lemma 5 (free).** Assume (I) and let $p$ be the first unit of a block $[p, p + n) \in \mathcal{B}$. Then BITMAP-FREE$(p)$ clears exactly the USED bits of $[p, p + n)$ and the START bit of $p$, so (I) holds with the block removed.

*Proof.* Line L9 clears START$[p]$ and looks for the least $q > p$ with START$[q] = 1$ or USED$[q] = 0$, capped at $h$. For $p < x < p + n$, unit $x$ is in the block, so USED$[x] = 1$ by (I.1), and START$[x] = 0$ by (I.2) and (I.3): no block starts inside another. So $q \ge p + n$. The unit $p + n$, if $p + n < h$, is either free, so USED is 0, or in another block, which by (I.3) must start at $p + n$, so START is 1. So $q = p + n$, or $q$ is capped at $h = p + n$. Line L10 clears the USED bits from $p$ to $p + n - 1$ and nothing else. $\square$

**Theorem.** For any sequence of calls in which `free` is called only on the first unit of an allocated block: (I) holds after each call; each BITMAP-MALLOC$(n)$ returns the lowest address of $n$ free units in a row, or FAIL when there is none; each call ends after $O(\lceil h/w \rceil \lg w + n/w)$ word operations for malloc and $O(n/w + 1)$ for free; and when every block is freed, all USED bits are 0 except the padding.

*Proof.* (I) holds at the start and is kept by Lemmas 4 and 5, so by induction it holds before each call, and Lemma 3 gives the first fit. The loop of line L2 has $\lceil h/w \rceil$ passes, each with $O(1)$ word operations plus at most $\lceil \lg w \rceil$ steps of RUN-OF-ONES by Lemma 1; MARK and line L10 touch $O(n/w + 1)$ words, and the scan of line L9 stops after $O(n/w + 1)$ words because $q = p + n$ by Lemma 5. When $\mathcal{B}$ is empty, (I.1) leaves only the padding bits set. $\blacksquare$
