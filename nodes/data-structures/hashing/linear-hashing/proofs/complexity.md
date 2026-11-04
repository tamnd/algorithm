---
title: Expected and amortized cost of linear hashing
proves: [time.search, time.insert, time.delete, space]
status: full
---

We use the names of the page and of the correctness proof: $M = N 2^L$, $B = M + p$, and the invariant (I1) to (I4). Time is counted on the word RAM, with $O(1)$ for one evaluation of $h$, for one comparison of keys, and for one step over a pair of a list. Appending a list to the array of buckets and removing the last one cost $O(1)$ amortized, as in a [dynamic array](/dynamic-array/).

**Assumption (A).** Let $R$ be a multiple of every $2M$ that occurs, for example $R = N 2^w$ for a large $w$. The values $h(k)$ of all keys that occur are independent and uniform on $\{0, \ldots, R - 1\}$, and the sequence of operations is fixed in advance, so it does not depend on these values. Under (A), $h(k) \bmod M$ and $h(k) \bmod 2M$ are uniform for every $M$ that occurs, because $M$ and $2M$ divide $R$.

**Lemma 1 (a fixed bucket).** In a state with (I1), for each key $k$ and each bucket $j$, $\Pr[\mathrm{addr}(k) = j] \le 1/M < 2/B$.

*Proof.* If $p \le j < M$, the event is $h(k) \bmod M = j$, with probability $1/M$. If $j < p$ or $j \ge M$, the event is $h(k) \bmod 2M = j$, with probability $1/(2M)$. Each other $j$ has probability 0 by Lemma 1 of the correctness proof. Finally $B = M + p < 2M$ gives $1/M < 2/B$. $\square$

The state at any time, that is, $n$, $L$, $p$ and the set of stored keys, depends only on the sequence of operations, because the decisions of lines L10 and D4 use only $n$ and $B$. The hash values decide only which list holds which key. This is what lets Lemma 1 apply at each step.

**Search.** Let the query be $k$. Condition on $h(k)$; this fixes the bucket $j = \mathrm{addr}(k)$. Each stored key $k' \ne k$ is in bucket $j$ with probability at most $1/M$, independently of $h(k)$, by (A) and Lemma 1. So the expected number of pairs with a key other than $k$ in the list is at most $n / M < 2n / B \le 2 \alpha_{\max}$ by (I4). The scan of lines L4 to L6 steps over these pairs and over at most one pair with key $k$. So SEARCH takes $O(1 + \alpha_{\max})$ expected time, whether $k$ is present or not.

**The number of splits per insertion.** Before INSERT, (I4) gives $n \le \alpha_{\max} B$. After line L9 there are at most $n + 1$ pairs. Let $s = \lceil 1 / \alpha_{\max} \rceil$. After $s$ splits, $\alpha_{\max} (B + s) \ge \alpha_{\max} B + 1 \ge n + 1$, so the loop of line L10 stops after at most $s$ splits.

**The cost of one split.** A split runs when the table holds some number $n'$ of pairs with $n' \le \alpha_{\max} B_0 + 1$, where $B_0 \le B$ is the size before the insertion and $B$ the current size. It scans the list $p$, an unsplit bucket. By Lemma 1, its expected length is at most $n' / M < 2 n' / B \le 2 \alpha_{\max} + 2 / B \le 2 \alpha_{\max} + 2$. With the $O(1)$ amortized cost of line L11, a split costs $O(1 + \alpha_{\max})$ expected amortized time.

**The cost of one merge.** A merge runs when $n < \alpha_{\min} B$. It moves the pairs of the last list, a split bucket, whose expected length is at most $n / (2M) < n / B < \alpha_{\min}$ by Lemma 1. So a merge costs $O(1 + \alpha_{\min}) = O(1 + \alpha_{\max})$ expected amortized time.

**Insert and delete.** Lines L7 to L9 and D1 to D3 scan one list, with the bound of the search: $O(1 + \alpha_{\max})$ expected time. Start from NEW, with $B = N$. Each split adds one bucket and each merge removes one, and $B \ge N$ at all times, so over any sequence the number of merges is at most the number of splits. The number of splits is at most $s$ times the number of insertions. So a sequence of $m$ operations does at most $2 s m$ splits and merges, with expected total cost $O(s m (1 + \alpha_{\max}))$, and $O(m (1 + \alpha_{\max}))$ for the scans. Since $s \le 1 + 1/\alpha_{\max}$, the expected amortized cost of each operation is

$$O\left((1 + 1/\alpha_{\max})(1 + \alpha_{\max})\right) = O(1 + \alpha_{\max} + 1/\alpha_{\max}),$$

which is $O(1)$ when $\alpha_{\max}$ is a positive constant.

**Worst case.** Without (A), all keys may share one list. Then one scan costs $O(n)$, and one split or merge costs $O(n)$. The loop of line L10 does at most $s$ splits. The loop of line D4 does at most $B - N$ merges, which move at most $n$ pairs in total, so it costs $O(n + B)$.

**Space.** The structure holds $B$ lists and $n$ pairs, so it uses $\Theta(B + n)$ words. If $\alpha_{\min} > 0$, then $B \le \max(N, n / \alpha_{\min} + 1)$ after each operation. This holds after NEW, where $B = N$. A search and a replacement of a value change neither $n$ nor $B$. An insertion without a split makes $n$ larger and keeps $B$. An insertion with splits ends with a split that ran because $n > \alpha_{\max} (B - 1)$ for the final $B$, so $B < n / \alpha_{\max} + 1 \le n / \alpha_{\min} + 1$. A deletion ends the loop of line D4 either with $B = N$ or with $n \ge \alpha_{\min} B$. So the space is $O(N + n / \alpha_{\min})$ words. $\blacksquare$
