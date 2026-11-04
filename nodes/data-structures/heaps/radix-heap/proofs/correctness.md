---
title: The radix heap returns the minimum, and each item moves at most lg U times
proves: [correctness, time.amortized]
status: full
---

Keys are nonnegative integers below $U = 2^w$. For an integer $k \ge last$, let $b(k) = 0$ if $k = last$, and $b(k) = 1 + \lfloor \lg(k \oplus last) \rfloor$ otherwise. So for $b(k) = i \ge 1$, the keys $k$ and $last$ agree on bits $w - 1, \dots, i$ and differ in bit $i - 1$. The invariant is (R1): every key in the heap is at least $last$, and (R2): every item with key $k$ is in $B[b(k)]$.

**Lemma 1 (order of buckets).** Under (R1) and (R2), every key in $B[0]$ equals $last$, and if $1 \le i < j$, every key in $B[i]$ is smaller than every key in $B[j]$. Also, every key in $B[i]$ with $i \ge 1$ is larger than $last$.

*Proof.* $B[0]$ holds only keys with $k \oplus last = 0$. Let $k \in B[i]$ with $i \ge 1$. Then $k \ne last$, and $k$ and $last$ agree above bit $i - 1$ and differ in it. Since $k > last$ by (R1), bit $i - 1$ is 1 in $k$ and 0 in $last$. Now let $k \in B[i]$ and $k' \in B[j]$ with $1 \le i < j$. Both agree with $last$ on bits above $j - 1$. On bit $j - 1$, $k$ agrees with $last$, which has a 0 there, while $k'$ has a 1. So $k < k'$. $\square$

**Lemma 2 (refill).** Let (R1) and (R2) hold, $B[0]$ be empty, $i$ be the smallest index with $B[i]$ not empty, and $d$ be the smallest key in $B[i]$. Then $d$ is the smallest key in the heap. After line L5 sets $last \leftarrow d$, (R1) holds; and for the new $last$, every key of $B[j]$ with $j > i$ still has $b(k) = j$, and every key $k$ of the old $B[i]$ has $b(k) < i$.

*Proof.* By Lemma 1, the keys of $B[i]$ are smaller than those of all higher buckets, and the lower buckets are empty. So $d$ is the minimum, and every key is at least $d$, which is (R1).

Write $\ell$ for the old $last$. Since $d \in B[i]$, the key $d$ agrees with $\ell$ on all bits above $i - 1$, and has a 1 in bit $i - 1$. Let $k \in B[j]$ with $j > i$. Then $k$ agrees with $\ell$, and so with $d$, on all bits above $j - 1$, and differs from $\ell$ in bit $j - 1$. Since $j - 1 > i - 1$, the bit $j - 1$ of $d$ equals that of $\ell$, so $k$ differs from $d$ in bit $j - 1$, and $b(k) = j$ for the new $last$.

Let $k$ be in the old $B[i]$. Then $k$ and $d$ both agree with $\ell$ above bit $i - 1$, and both have a 1 in bit $i - 1$. So $k \oplus d < 2^{i-1}$, and $b(k) \le i - 1$ for the new $last$. $\square$

**Theorem 1 (correctness).** INSERT and EXTRACT-MIN keep (R1) and (R2), and EXTRACT-MIN returns an item with the smallest key.

*Proof.* INSERT checks $\mathrm{key}(x) \ge last$ and puts $x$ in $B[b(\mathrm{key}(x))]$, so both conditions hold. In EXTRACT-MIN, if $B[0]$ is not empty, its items have key $last$, which is the minimum by (R1), and removing one keeps both conditions. Otherwise, by Lemma 2, the new $last$ is the minimum and (R1) holds. Lines L6 and L7 move every item of the old $B[i]$ to its bucket for the new $last$, and by Lemma 2 the items of higher buckets are already in theirs, so (R2) holds. The item with key $d$ has $b(d) = 0$, so $B[0]$ is not empty, and line L8 returns an item of key $d = last$. $\square$

**Theorem 2 (moves).** Each item is moved by line L7 at most $w$ times, so a sequence of $n$ inserts and any number of extract-mins does $O(n \log U)$ moves in total.

*Proof.* By Lemma 2, a move takes an item from $B[i]$ to a bucket with a smaller index, and an item in a higher bucket keeps its index. A change of $last$ is the only event that can change a bucket index, so the index of each item never grows. It starts at most at $w$, the largest index for keys below $2^w$, and it is never below 0. Each move lowers it by at least 1, so there are at most $w = \lg U$ moves per item. $\blacksquare$

The other work of an extract-min is the search of line L4, which takes $O(w)$ time by a scan, or $O(1)$ with a bit mask of nonempty buckets and an instruction for the lowest set bit. So with the mask, the total time of $n$ inserts and $n'$ extract-mins is $O((n + n') + n \log U)$: $O(\log U)$ amortized per insert and $O(1)$ amortized per extract-min.
