---
title: Median of medians returns the k-th smallest item and stops
proves: [correctness, termination]
status: full
---

For a list $S$ of $n$ items and $1 \le k \le n$, write $\operatorname{sel}(S, k)$ for the $k$-th entry of a sorted order of $S$. All sorted orders of $S$ have the same entries, so this value is well defined.

**Claim.** For each list $S$ of $n \ge 1$ items and each $k$ with $1 \le k \le n$, SELECT$(S, k)$ stops and returns $\operatorname{sel}(S, k)$.

**Lemma (split).** Let $x$ be an item, and let $L$, $E$ and $G$ be the items of $S$ that are less than, equal to and greater than $x$. Then

$$ \operatorname{sel}(S, k) = \begin{cases} \operatorname{sel}(L, k) & \text{if } k \le |L|, \\ x & \text{if } |L| < k \le |L| + |E|, \\ \operatorname{sel}(G, k - |L| - |E|) & \text{if } k > |L| + |E|. \end{cases} $$

*Proof.* The order is total, so each item of $S$ is in exactly one of the three lists. Sort $L$ and $G$, and write $E$ as $|E|$ copies of $x$. The list "sorted $L$, then $E$, then sorted $G$" is sorted: each item of $L$ is less than $x$, and each item of $G$ is greater than $x$. It holds the items of $S$, so it is a sorted order of $S$. Its entries $1$ to $|L|$ are the sorted $L$, its entries $|L| + 1$ to $|L| + |E|$ are equal to $x$, and its entry $|L| + |E| + j$ is the entry $j$ of the sorted $G$. $\square$

**Proof of the claim.** By strong induction on $n$. The hypothesis $H(m)$ says that SELECT$(S', k')$ stops and returns $\operatorname{sel}(S', k')$ for each list $S'$ of $m$ items and each $1 \le k' \le m$.

1. *Base, $n \le 5$.* Line L1 sorts $S$ by insertion sort, which stops and is correct, and returns its entry of rank $k$, which is $\operatorname{sel}(S, k)$ by definition.
2. *Step, $n \ge 6$.* Assume $H(m)$ for each $m < n$.
   - Line L2 makes $g = \lceil n/5 \rceil$ groups. Each group is not empty, and $g \le (n + 4)/5 < n$ because $n \ge 2$.
   - Line L3 makes the list $M$ of $g$ group medians. Each is an item of $S$.
   - Line L4 calls SELECT$(M, \lceil g/2 \rceil)$. Here $1 \le \lceil g/2 \rceil \le g$ and $g < n$, so by $H(g)$ the call stops and returns $x = \operatorname{sel}(M, \lceil g/2 \rceil)$, which is an item of $M$ and so of $S$.
   - Line L5 makes $L$, $E$ and $G$ as in the lemma. Since $x$ is an item of $S$, $|E| \ge 1$, so $|L| \le n - 1$ and $|G| \le n - 1$.
   - If $k \le |L|$, line L6 calls SELECT$(L, k)$ with $1 \le k \le |L| < n$. By $H(|L|)$ it returns $\operatorname{sel}(L, k)$, which is $\operatorname{sel}(S, k)$ by the lemma.
   - If $|L| < k \le |L| + |E|$, line L7 returns $x$, which is $\operatorname{sel}(S, k)$ by the lemma.
   - Otherwise $|L| + |E| < k \le n$, so $k' = k - |L| - |E|$ satisfies $1 \le k' \le n - |L| - |E| = |G| < n$. Line L8 calls SELECT$(G, k')$, which by $H(|G|)$ returns $\operatorname{sel}(G, k')$, which is $\operatorname{sel}(S, k)$ by the lemma.

   In each case the call stops, because each recursive call stops, and returns $\operatorname{sel}(S, k)$.

So $H(n)$ holds for each $n \ge 1$. The proof uses no property of $x$ except that it is an item of $S$. The choice of $x$ as the median of the medians matters only for the running time, which the Complexity section of the page proves. $\blacksquare$
