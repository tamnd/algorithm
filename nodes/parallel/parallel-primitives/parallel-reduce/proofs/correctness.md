---
title: The tree reduce is correct, with exactly n − 1 combines and span ⌈lg n⌉
proves: [correctness]
status: full
---

**Statement.** Let $\oplus$ be an [associative operator](/associative-operator/) on a set $S$, and let $A[0 \ldots n-1]$ be an array over $S$ with $n \ge 1$. Then REDUCE$(A, 0, n)$ returns $A[0] \oplus A[1] \oplus \cdots \oplus A[n-1]$. It applies $\oplus$ exactly $n - 1$ times, and the longest chain of applications in which each one uses the result of the one before has exactly $\lceil \lg n \rceil$ applications. With unit cost for each call and each sync as well, the work is $\Theta(n)$ and the span is $\Theta(\log n)$.

**Setup.** Write $m = hi - lo$ for the length of a call. Line L2 sets $mid = lo + \lceil m/2 \rceil$, so the first call of line L3 gets $\lceil m/2 \rceil$ items and the call of line L4 gets $\lfloor m/2 \rfloor$ items. For $m \ge 2$ both numbers are at least 1 and at most $m - 1$. Write $L(x_1, \ldots, x_k)$ for the left fold $(\cdots((x_1 \oplus x_2) \oplus x_3) \cdots) \oplus x_k$. The lemma on the [associative operator](/associative-operator/) page says that $L(x_1, \ldots, x_j) \oplus L(x_{j+1}, \ldots, x_k) = L(x_1, \ldots, x_k)$ for $1 \le j < k$.

**Lemma 1 (ceilings).** For each integer $m \ge 2$, $\lceil \lg \lceil m/2 \rceil \rceil = \lceil \lg m \rceil - 1$.

*Proof.* Let $k = \lceil \lg m \rceil$. Then $k \ge 1$ and $2^{k-1} < m \le 2^k$. From $m \le 2^k$ we get $m/2 \le 2^{k-1}$, and since $2^{k-1}$ is an integer, $\lceil m/2 \rceil \le 2^{k-1}$. From $m > 2^{k-1}$ we get $\lceil m/2 \rceil \ge m/2 > 2^{k-2}$. So $2^{k-2} < \lceil m/2 \rceil \le 2^{k-1}$, which means $\lceil \lg \lceil m/2 \rceil \rceil = k - 1$. $\square$

## 1. The result

We show by strong induction on $m \ge 1$ that REDUCE$(A, lo, hi)$ returns $L(A[lo], \ldots, A[hi-1])$.

1. If $m = 1$, line L1 returns $A[lo] = L(A[lo])$.
2. If $m \ge 2$, both recursive calls have between 1 and $m - 1$ items. By the induction hypothesis, line L3 sets $x = L(A[lo], \ldots, A[mid-1])$ and line L4 sets $y = L(A[mid], \ldots, A[hi-1])$.
3. The two calls read the array and write nothing, so they do not interfere, and line L5 makes both values available.
4. Line L6 returns $x \oplus y$ with $x$ on the left. By the lemma with $j = mid - lo$, this is $L(A[lo], \ldots, A[hi-1])$.

For $n = 0$, line L7 returns the identity, which is the value of the empty product by definition.

## 2. The number of combines

Let $W(m)$ be the number of applications of $\oplus$ in a call of length $m$. Line L1 gives $W(1) = 0$. For $m \ge 2$, line L6 does one application, so $W(m) = W(\lceil m/2 \rceil) + W(\lfloor m/2 \rfloor) + 1$. By strong induction, $W(m) = m - 1$: the base case holds, and for $m \ge 2$ the hypothesis gives $W(m) = (\lceil m/2 \rceil - 1) + (\lfloor m/2 \rfloor - 1) + 1 = m - 1$.

## 3. The span in combines

Let $S(m)$ be the largest number of applications of $\oplus$ on one chain of dependences in a call of length $m$. The two calls run in parallel, and line L6 depends on both results, so $S(1) = 0$ and $S(m) = \max(S(\lceil m/2 \rceil), S(\lfloor m/2 \rfloor)) + 1$ for $m \ge 2$. We show $S(m) = \lceil \lg m \rceil$ by strong induction. The base case is $S(1) = 0 = \lceil \lg 1 \rceil$. For $m \ge 2$, the hypothesis gives $S(\lceil m/2 \rceil) = \lceil \lg \lceil m/2 \rceil \rceil$ and $S(\lfloor m/2 \rfloor) = \lceil \lg \lfloor m/2 \rfloor \rceil$. The function $\lceil \lg \cdot \rceil$ does not decrease, and $\lfloor m/2 \rfloor \le \lceil m/2 \rceil$, so the maximum is the first term. By Lemma 1 it equals $\lceil \lg m \rceil - 1$, so $S(m) = \lceil \lg m \rceil$.

## 4. The cost of the fork-join control

Each call of length $m \ge 2$ makes two calls, and a call of length 1 makes none. So the calls form a full binary tree with $n$ leaves, which has $n - 1$ inner nodes and $2n - 1$ nodes in total. With a unit cost for each call, each spawn and each sync, the work is at most a constant times $2n - 1$ plus the $n - 1$ combines, so it is $\Theta(n)$. The longest chain of calls has length $S(n) + 1$, because each level of the call tree adds one combine on the way up, by part 3. Each level adds a constant to the span, so the span is $\Theta(\lceil \lg n \rceil + 1) = \Theta(\log n)$ for $n \ge 2$.

So REDUCE is correct, with exactly $n - 1$ combines, a combine span of exactly $\lceil \lg n \rceil$, work $\Theta(n)$ and span $\Theta(\log n)$. $\blacksquare$
