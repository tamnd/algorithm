---
title: The Sklansky adder computes the sum
proves: [correctness, termination]
status: full
---

Let $a$, $b$, $c_0$, $g_i$, $p_i$ and the carries $c_{i+1} = g_i \vee (p_i \wedge c_i)$ be as on the page of the [Kogge-Stone adder](/kogge-stone-adder/), whose proof shows three facts that we use here.

1. For a block $k..i$ of positions there is a pair $(G_{i:k}, P_{i:k})$ such that the carry out of position $i$ is $G_{i:k} \vee (P_{i:k} \wedge x)$ when the carry into position $k$ is $x$, and $(G_{k:k}, P_{k:k}) = (g_k, p_k)$.
2. For adjacent blocks, $(G_{i:k}, P_{i:k}) = (G_{i:j+1}, P_{i:j+1}) \circ (G_{j:k}, P_{j:k})$ for $k \le j < i$.
3. After line L2 replaces $g_0$ by $g_0 \vee (p_0 \wedge c_0)$, the $G$ part of the block $0..i$ equals $c_{i+1}$, and $a + b + c_0 = \sum_{i<n} (p_i \oplus c_i)2^i + c_n2^n$.

**Lemma.** Let $0 \le lo < hi \le n$, and suppose that before the call PREFIX$(lo, hi)$, $(G[i], P[i]) = (g_i, p_i)$ for every $i \in [lo, hi)$. Then the call terminates, it changes no position outside $[lo, hi)$, and afterwards $(G[i], P[i]) = (G_{i:lo}, P_{i:lo})$ for every $i \in [lo, hi)$. The depth of the recursion below the call is $\lceil \log_2 (hi - lo) \rceil$.

*Proof.* By strong induction on $\ell = hi - lo \ge 1$.

If $\ell = 1$, line L7 returns at once, and $(G[lo], P[lo]) = (g_{lo}, p_{lo}) = (G_{lo:lo}, P_{lo:lo})$. The recursion depth is $0 = \lceil \log_2 1 \rceil$.

If $\ell \ge 2$, line L8 sets $mid = lo + \lceil \ell/2 \rceil$, so $lo < mid < hi$, and both ranges $[lo, mid)$ and $[mid, hi)$ are shorter than $\ell$ and disjoint. By the induction hypothesis the two calls of line L9 terminate, each changes only its own range, and afterwards position $i$ holds $(G_{i:lo}, P_{i:lo})$ for $lo \le i < mid$ and $(G_{i:mid}, P_{i:mid})$ for $mid \le i < hi$. Since the ranges are disjoint, the order in which the two calls run does not matter, so they may run in parallel.

Line L10 reads the pair at $mid - 1$, which is $(G_{mid-1:lo}, P_{mid-1:lo})$ and is not changed by line L10, since $mid - 1 < mid$. For each $i \in [mid, hi)$ it sets the pair at $i$ to

$$(G_{i:mid}, P_{i:mid}) \circ (G_{mid-1:lo}, P_{mid-1:lo}) = (G_{i:lo}, P_{i:lo})$$

by fact 2 with $j = mid - 1$. So every position of $[lo, hi)$ holds the block starting at $lo$, and nothing outside $[lo, hi)$ changed.

The two halves have lengths $\lceil \ell/2 \rceil$ and $\lfloor \ell/2 \rfloor$, and $\lceil \log_2 \lceil \ell/2 \rceil \rceil = \lceil \log_2 \ell \rceil - 1$ for $\ell \ge 2$, so the recursion depth below the call is $1 + (\lceil \log_2 \ell \rceil - 1) = \lceil \log_2 \ell \rceil$. $\square$

**Theorem.** SKLANSKY-ADD terminates and returns the $n + 1$ bits of $a + b + c_0$.

*Proof.* For $n = 0$ the result is the single bit $c_0$. For $n \ge 1$, line L3 sets $(G[i], P[i]) = (g_i, p_i)$ for all $i$, with $g_0$ already updated by line L2, so the lemma applies to PREFIX$(0, n)$: it terminates, with recursion depth $\lceil \log_2 n \rceil$, and leaves $(G_{i:0}, P_{i:0})$ at every position. By fact 3, $G[i] = c_{i+1}$, so line L4 sets the true carries, and line L5 computes $s_i = p_i \oplus c_i$. By fact 3 again, $\sum_{i<n} s_i2^i + c_n2^n = a + b + c_0$. $\blacksquare$
