---
title: The Hillis-Steele scan is correct, with exactly n⌈lg n⌉ − 2^⌈lg n⌉ + 1 combines in ⌈lg n⌉ rounds
proves: [correctness]
status: full
---

**Statement.** Let $\oplus$ be an [associative operator](/associative-operator/) on a set $S$, and let $A[0 \ldots n-1]$ be an array over $S$ with $n \ge 1$. Let $K = \lceil \lg n \rceil$. Then HILLIS-STEELE-SCAN returns the array $x$ with $x[i] = A[0] \oplus A[1] \oplus \cdots \oplus A[i]$ for each $i$. It runs exactly $K$ rounds and applies $\oplus$ exactly $nK - 2^K + 1$ times. This is $\Theta(n \log n)$, so the scan is not work-efficient.

**Notation.** For $0 \le j \le i < n$, write $A[j..i]$ for $A[j] \oplus A[j+1] \oplus \cdots \oplus A[i]$. By the [associative operator](/associative-operator/) page, this value does not depend on the bracketing, and $A[j..m] \oplus A[m+1..i] = A[j..i]$ for $j \le m < i$.

## 1. The invariant

**Claim.** When the loop test on line L3 is reached for the $(k+1)$-th time, $d = 2^k$ and, for each $i$, $x[i] = A[\max(0, i - d + 1)..i]$.

*Proof by induction on $k$.* For $k = 0$, line L1 has copied $A$ and line L2 has set $d = 1$, so $x[i] = A[i] = A[i..i]$.

Assume the claim for $k$, with $d = 2^k < n$, and run one round. Line L5 computes each $y[i]$ from the old array $x$ only, because the round writes into $y$ and line L6 replaces $x$ only after all of $y$ is written. Fix $i$.

1. If $i \ge d$, then $i - d + 1 \ge 1$, so the hypothesis gives $x[i] = A[i-d+1..i]$, and it gives $x[i-d] = A[\max(0, i - 2d + 1)..i-d]$. The two ranges are adjacent and in order, so $y[i] = x[i-d] \oplus x[i] = A[\max(0, i - 2d + 1)..i]$.
2. If $i < d$, then $i - d + 1 \le 0$, so $x[i] = A[0..i]$. Also $i - 2d + 1 \le 0$, so $A[\max(0, i - 2d + 1)..i] = A[0..i] = y[i]$.

After line L7, $d = 2^{k+1}$, and in both cases $x[i] = A[\max(0, i - d + 1)..i]$. $\square$

## 2. The result

The loop stops at the first $k$ with $2^k \ge n$, which is $k = K$, since $2^{K-1} < n \le 2^K$ (for $n = 1$, $K = 0$ and no round runs). Then $i - 2^K + 1 \le (n - 1) - n + 1 = 0$ for each $i < n$, so the claim gives $x[i] = A[0..i]$, which line L8 returns. The order of the operands on line L5, with $x[i - d]$ on the left, is what makes the ranges join in order. So the operator need not be commutative.

## 3. The work

Round $k$, for $k = 0, \ldots, K - 1$, applies $\oplus$ once for each $i$ with $d \le i < n$, which is $n - 2^k$ times. So the work is
$$
W(n) = \sum_{k=0}^{K-1} (n - 2^k) = nK - (2^K - 1) = n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1.
$$
Since $n \le 2^K < 2n$, we have $nK - 2n + 1 < W(n) \le nK - n + 1$. For $n \ge 16$, $K \ge 4$, so $W(n) > nK - 2n \ge nK/2$. With $K \ge \lg n$, this gives $W(n) = \Theta(n \log n)$. For $n = 2^K$, $W(n) = n(\lg n - 1) + 1$.

A sequential scan applies $\oplus$ exactly $n - 1$ times, and no algorithm that must produce all $n$ prefixes of a general operator, such as string concatenation, can use fewer, because each output except $x[0]$ needs at least one application of its own. So the ratio of the work to the optimal work is $\Theta(\log n)$, and the scan is not [work-efficient](/work-efficiency/).

## 4. The span

Each round applies $\oplus$ at most once on each path of the dependence graph, because every $y[i]$ is computed from values of the round before. So the longest chain of dependent applications has at most $K$ applications. It has exactly $K$: the value $x[n-1]$ is updated in each round, since $n - 1 \ge 2^k$ for every $k < K$, and each update uses the result of the round before. No scan can do better: the output $x[n-1]$ depends on all $n$ inputs, and a value made by $s$ levels of a binary operator depends on at most $2^s$ inputs, so $s \ge \lceil \lg n \rceil$.

## 5. The PRAM cost

On a PRAM with $n$ processors, processor $i$ does the work of position $i$ in each round. In the first substep, processor $i$ reads $x[i]$; in the second, processor $i \ge d$ reads $x[i - d]$; then it writes $y[i]$. In each substep the addresses are distinct, so no two processors read or write the same cell at the same time, and the algorithm runs on an EREW PRAM in $O(K) = O(\log n)$ steps. Its processor-time product is $\Theta(n \log n)$.

So the Hillis-Steele scan computes the inclusive scan in exactly $\lceil \lg n \rceil$ rounds with exactly $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ applications of $\oplus$. $\blacksquare$
