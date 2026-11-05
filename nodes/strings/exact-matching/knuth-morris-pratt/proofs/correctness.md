---
title: KMP outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ with $m \ge 1$, KMP-MATCHER$(T, P)$ stops and outputs exactly the shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. (For $m = 0$, line L2 outputs all shifts $0, \ldots, n$, which is the definition.)

**Setup.** For a string $x$, let $\lambda(x)$ be the length of the longest prefix of $P$ that is a suffix of $x$ and has length less than $m$. Let $\pi$ be the [prefix function](/prefix-function/) of $P$. We use two facts proved on that page.

- (F1) The borders of $P[0 \ldots q-1]$, for $q \ge 1$, have the lengths $\pi[q-1], \pi[\pi[q-1]-1], \ldots, 0$, and no other lengths.
- (F2) A border of a border of $x$ is a border of $x$, and a border of $x$ shorter than another border $u$ of $x$ is a border of $u$.

**Lemma 1 (the table).** For $1 \le q < m$, line L16 sets $\mathrm{nxt}[q]$ to the largest $k < q$ such that $P[0 \ldots k-1]$ is a border of $P[0 \ldots q-1]$ and $P[k] \ne P[q]$, or to $-1$ if there is none. Also $\mathrm{nxt}[0] = -1$, which is the same rule for $q = 0$ (no $k < 0$ exists).

*Proof.* By strong induction on $q$. Let $k = \pi[q-1] < q$, the longest proper border length of $P[0 \ldots q-1]$. If $P[k] \ne P[q]$, then $k$ is the largest candidate, and line L16 sets $\mathrm{nxt}[q] = k$. If $P[k] = P[q]$, then $k$ is not a candidate, and by (F1) and (F2) the remaining candidates are exactly the lengths $j < k$ such that $P[0 \ldots j-1]$ is a border of $P[0 \ldots k-1]$ and $P[j] \ne P[q] = P[k]$. By the induction hypothesis for $k < q$, the largest of them is $\mathrm{nxt}[k]$, or $-1$ if there is none. $\square$

**Lemma 2 (one text character).** Let $x$ be a string, $c$ a character, and $q = \lambda(x)$. Run lines L6 to L8 with this $q$ and $T[i] = c$. Then they stop, and afterwards $q = $ the length of the longest prefix of $P$ that is a suffix of $xc$ (this length may be $m$).

*Proof.* Let $B$ be the set of lengths $k$ with $0 \le k \le q$ such that $P[0 \ldots k-1]$ is a suffix of $x$. A prefix $P[0 \ldots j]$ with $j < m$ is a suffix of $xc$ exactly when $P[0 \ldots j-1]$ is a suffix of $x$ and $P[j] = c$. Each such $j$ satisfies $j \le q$ by the definition of $q = \lambda(x)$, so $j \in B$. And for $k \le q$, $P[0 \ldots k-1]$ is a suffix of $x$ exactly when it is a border of $P[0 \ldots q-1]$ or equal to it, by (F2) applied to the suffixes of $x$. So the answer is $1 + \max\{\, j \in B : P[j] = c \,\}$, or $0$ if that set is empty.

The loop of line L6 keeps the invariant: $q = -1$, or $q \in B$ and no $j \in B$ with $j > q$ has $P[j] = c$. It holds at the start. If $q \ge 0$ and $P[q] \ne c$, line L7 sets $q$ to $\mathrm{nxt}[q]$. By Lemma 1, each $j \in B$ with $\mathrm{nxt}[q] < j < q$ has $P[j] = P[q] \ne c$, so the invariant holds for the new value. Each pass decreases $q$ by at least 1 and $q \ge -1$, so the loop stops after at most $q + 1$ passes. At the exit, either $q \ge 0$ and $P[q] = c$, so $q$ is the largest $j \in B$ with $P[j] = c$, or $q = -1$ and no $j \in B$ has $P[j] = c$. Line L8 adds 1, which gives the answer in both cases. $\square$

**Theorem.** The claim holds.

*Proof.* We show by induction on $i$ that at the start of the iteration for $i$ (and at the end, for $i = n$):

> **(I)** $q = \lambda(T[0 \ldots i-1])$, and the output so far is the increasing list of valid shifts $s$ with $s + m - 1 < i$.

*Initialization.* For $i = 0$, the text read is empty, $\lambda$ of the empty string is 0, and nothing is output, so (I) holds after line L4.

*Maintenance.* Assume (I) for $i$. By Lemma 2, after line L8, $q$ is the length $\ell$ of the longest prefix of $P$ that is a suffix of $T[0 \ldots i]$. A valid shift ends at $i$ exactly when $P$ itself is a suffix of $T[0 \ldots i]$, that is when $\ell = m$, and then the shift is $i - m + 1$, larger than all earlier outputs. So lines L9 and L10 output exactly the valid shift that ends at $i$, if any. If $\ell < m$, then $q = \ell = \lambda(T[0 \ldots i])$. If $\ell = m$, the longest prefix of $P$ shorter than $m$ that is a suffix of $T[0 \ldots i]$ is the longest proper border of $P$, by (F2), whose length is $\pi[m-1] = \mathrm{nxt}[m]$, the value set by line L11. In both cases (I) holds for $i + 1$.

*Termination.* The loop of line L5 runs $n$ times, and each inner loop stops by Lemma 2. At the end, (I) for $i = n$ says that the output is the increasing list of all valid shifts. $\blacksquare$

**Cost.** The proof of Lemma 2 shows that each pass of line L7 decreases $q$ by at least 1. The complexity section of the page turns this into the bound of $2n$ comparisons.
