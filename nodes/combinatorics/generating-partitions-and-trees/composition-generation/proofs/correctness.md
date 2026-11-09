---
title: The lexicographic successor visits each composition of n once, in lexicographic order, in Theta(2^(n-1)) time
proves: [correctness, time.worst]
status: full
---

**Statement.** For each integer $n \ge 0$, COMPOSITIONS$(n)$ visits each composition of $n$ exactly once, in increasing lexicographic order, and stops. For $n \ge 1$ the loop body of line L8 runs $2^{n-1} - n$ times in total, and the running time is $\Theta(2^{n-1})$.

**Setup.** A composition of $n$ is a sequence $c = (c_1, \ldots, c_m)$ of integers $c_i \ge 1$ with sum $n$. For sequences, $c < d$ in lexicographic order when $c$ is a proper prefix of $d$, or when $c_i < d_i$ at the first index $i$ where they differ. Two different compositions of the same $n$ are never prefixes of each other, because the longer one would have a larger sum. So for compositions of $n$ only the second case occurs.

**Lemma 1 (smallest and largest).** For $s \ge 1$, the smallest composition of $s$ is $(1^s)$ and the largest is $(s)$.

*Proof.* Let $e \ne (1^s)$ be a composition of $s$, and let $i$ be the first index with $e_i \ne 1$. Then $e_i \ge 2$, and $e_1 + \cdots + e_i = (i - 1) + e_i \le s$ gives $i \le s - 1$, so $(1^s)$ has the entry $1 < e_i$ at index $i$ and agrees with $e$ before it. So $(1^s) < e$. Every composition of $s$ other than $(s)$ has first part at most $s - 1$, so $(s)$ is the largest. $\square$

**Lemma 2 (successor).** Let $c = (c_1, \ldots, c_m)$ be a composition of $n$ with $m \ge 2$. The smallest composition of $n$ that is larger than $c$ is

$$c^+ = (c_1, \ldots, c_{m-2},\ c_{m-1} + 1,\ 1^{c_m - 1}).$$

*Proof.*

1. $c^+$ is a composition of $n$: its parts are positive and its sum is $c_1 + \cdots + c_{m-1} + 1 + (c_m - 1) = n$. It first differs from $c$ at index $m - 1$, where it is larger, so $c^+ > c$.
2. Let $d > c$ be a composition of $n$ and let $i$ be the first index where they differ, so $d_i > c_i$. If $i = m$, then $d$ agrees with $c$ on the first $m - 1$ parts, so $d_m \le n - (c_1 + \cdots + c_{m-1}) = c_m$, which is a contradiction. So $i \le m - 1$.
3. If $i < m - 1$, then $c^+$ agrees with $c$ at indices up to $i$, so $c^+_i = c_i < d_i$ and $c^+ < d$.
4. If $i = m - 1$ and $d_{m-1} > c_{m-1} + 1$, then $c^+ < d$ at index $m - 1$.
5. If $i = m - 1$ and $d_{m-1} = c_{m-1} + 1$, then $d$ and $c^+$ agree up to index $m - 1$, and both continue with a composition of $c_m - 1$. If $c_m = 1$ both stop, and $d = c^+$. Otherwise $c^+$ continues with $(1^{c_m - 1})$, the smallest such composition by Lemma 1, so $c^+ \le d$.

So $c^+$ is the smallest composition of $n$ larger than $c$. $\square$

**Lemma 3 (one step).** If $a[1 \ldots m]$ holds a composition $c$ with $m \ge 2$, then lines L6 to L8 change it into $c^+$.

*Proof.* Line L6 sets $t = c_m - 1$. Line L7 sets $m$ to $m - 1$ and $a[m - 1]$ to $c_{m-1} + 1$, so $a[1 \ldots m - 1] = (c_1, \ldots, c_{m-2}, c_{m-1} + 1)$. Line L8 appends $t$ ones. The result is $c^+$. $\square$

**Theorem (correctness).** COMPOSITIONS$(n)$ visits each composition of $n$ exactly once, in increasing lexicographic order, and stops.

*Proof.* For $n = 0$, line L1 visits the one composition of $0$, the empty one. For $n \ge 1$, line L2 sets $a = (1^n)$, the smallest composition by Lemma 1. We use the invariant

> **(I)** At line L4, $a[1 \ldots m]$ is a composition of $n$, and the visits so far are, in order, all compositions of $n$ that are smaller than $a$, from the smallest up.

(I) holds at the first visit. If $m = 1$ at line L5, then $a = (n)$, which is the largest composition by Lemma 1, so all compositions have been visited and the algorithm stops. Otherwise Lemma 3 makes $a$ into $a^+$, and by Lemma 2 no composition lies strictly between $a$ and $a^+$, so (I) holds at the next visit. Each step moves to a larger element of a finite set, so the loop stops after $2^{n-1}$ visits, the number of compositions of $n$. $\square$

**Theorem (time).** For $n \ge 1$ the loop body of line L8 runs $2^{n-1} - n$ times in total, and COMPOSITIONS$(n)$ runs in $\Theta(2^{n-1})$ time.

*Proof.* The step from $c$ runs line L8 $c_m - 1$ times, where $c_m$ is the last part of $c$. A step happens from each composition except $(n)$, the only one with last part $n$. For $1 \le j \le n - 1$, the compositions of $n$ with last part $j$ are the compositions of $n - j \ge 1$ with $j$ appended, so there are $2^{n-j-1}$ of them. So the total is

$$T(n) = \sum_{j=1}^{n-1} (j - 1)\, 2^{n-1-j}.$$

We show $T(n) = 2^{n-1} - n$ by induction. $T(1) = 0 = 2^0 - 1$. Splitting off the term $j = n$,

$$T(n + 1) = \sum_{j=1}^{n} (j - 1)\, 2^{n-j} = 2 \sum_{j=1}^{n-1} (j - 1)\, 2^{n-1-j} + (n - 1) = 2T(n) + n - 1 = 2^n - (n + 1).$$

Line L2 takes $O(n)$ time, each of the $2^{n-1}$ passes of the loop takes $O(1)$ time without line L8, and line L8 adds $O(2^{n-1} - n)$. Since $n \le 2^{n-1}$ for $n \ge 1$, the total is $O(2^{n-1})$. It is $\Omega(2^{n-1})$ because there are $2^{n-1}$ visits. $\blacksquare$
