---
title: GREEDY-ASSEMBLE merges by largest overlap, returns superstrings, and reconstructs a genome whose repeats are shorter than the read overlaps
proves: [correctness, termination]
status: full
---

**Notation.** Strings are over a finite alphabet and indexed from 0. For strings $a \ne b$, $\mathrm{ov}(a, b)$ is the length of the longest proper suffix of $a$ that is also a proper prefix of $b$. A set of strings is *substring-free* if no string in it occurs inside another one. After line L1 the reduced reads $s_0, \ldots, s_{m-1}$ are distinct and substring-free. A *contig* is a chain $h_0 \to h_1 \to \cdots \to h_r$ of accepted pairs; its *head* is $h_0$, its *tail* is $h_r$, and its *string* is $s_{h_0}$ followed, for $q = 1, \ldots, r$, by $s_{h_q}$ without its first $w(h_{q-1}, h_q)$ letters, where $w(i, j) = \mathrm{ov}(s_i, s_j)$.

**Lemma 1 (removed reads are covered).** Each nonempty input read occurs inside some reduced read.

*Proof.* A repeated read is covered by its kept copy. A read $x$ removed as contained occurs in a strictly longer read $y$. If $y$ is removed too, repeat with $y$. Lengths grow strictly, so the process stops at a kept read, and occurrence is transitive. $\square$

**Lemma 2 (contig strings).** The string of a contig starts with $s_{h_0}$, ends with $s_{h_r}$, and contains every $s_{h_q}$.

*Proof.* By induction on $r$. For $r = 0$ the string is $s_{h_0}$. The step appends $s_{h_{r+1}}$ without its prefix of length $w(h_r, h_{r+1})$, and that prefix is a suffix of $s_{h_r}$, hence of the current string. So the new string ends with $s_{h_{r+1}}$ and keeps all earlier reads. $\square$

**Lemma 3 (one merge).** Let $C$ be a substring-free set of at least two strings. Let $(a, b)$ be a pair of distinct strings of $C$ with the largest overlap $k = \mathrm{ov}(a, b)$, and let $c = a \cdot b[k..]$. Then for every $t \in C \setminus \{a, b\}$:

1. $t$ does not occur in $c$, and $c$ does not occur in $t$;
2. $\mathrm{ov}(c, t) = \mathrm{ov}(b, t)$ and $\mathrm{ov}(t, c) = \mathrm{ov}(t, a)$.

*Proof.* The string $c$ starts with $a$ and ends with $b$, since $b[..k)$ is a suffix of $a$.

(1) If $c$ occurs in $t$, then $a$ occurs in $t$, which is excluded. Suppose $t$ occurs in $c$ at position $p$. If $p + |t| \le |a|$, then $t$ occurs in $a$. If $p \ge |a| - k$, then $t$ lies inside the last $|b|$ letters of $c$, which spell $b$, so $t$ occurs in $b$. Otherwise $p < |a| - k$ and $p + |t| > |a|$. If $p = 0$, then $a$ is a prefix of $t$. If $p > 0$, the suffix of $a$ that starts at $p$ has length $|a| - p < |t|$, is proper, and is a prefix of $t$, so $\mathrm{ov}(a, t) \ge |a| - p > k$, which contradicts the choice of $(a, b)$. Every case is impossible.

(2) Let $\ell$ be the length of a proper suffix of $t$ that is a proper prefix of $c$. If $\ell \ge |a|$, then $a$ is a prefix of this suffix, so $a$ occurs in $t$, which is excluded. So $\ell < |a|$, the prefix of $c$ of length $\ell$ is a proper prefix of $a$, and $\ell < \min(|t|, |a|)$. Conversely, each overlap of $t$ with $a$ is a proper prefix of $c$. So $\mathrm{ov}(t, c) = \mathrm{ov}(t, a)$. In the same way, a suffix of $c$ of length at least $|b|$ that is a prefix of $t$ puts $b$ inside $t$; so the overlaps of $c$ with $t$ are the suffixes of $b$ that are proper prefixes of $t$, and $\mathrm{ov}(c, t) = \mathrm{ov}(b, t)$. $\square$

**Invariant of the scan.** Before each step of line L3, let $C$ be the set of contig strings. Then:

- (I1) the accepted pairs form vertex-disjoint chains that cover all $m$ reads, $\mathit{next}[i]$ is unset exactly for the tails, $\mathit{prev}[j]$ is unset exactly for the heads, and the arrays $\mathit{head}$ and $\mathit{tail}$ give the head of the contig of each tail and the tail of the contig of each head;
- (I2) $C$ is substring-free, and for two distinct contigs $X, Y$, $\mathrm{ov}(X, Y) = w(\mathrm{tail}(X), \mathrm{head}(Y))$;
- (I3) a pair $(i, j)$ is *live* if $i$ is a tail, $j$ is a head and they lie in different contigs. Every pair before the current position of the scan is not live.

*Initially* each read is a contig alone, so (I1) and (I2) hold with $C$ the reduced reads, and (I3) holds because no pair has been passed.

*Live pairs and contig pairs.* By (I1), the map that sends a live pair $(i, j)$ to the contig with tail $i$ and the contig with head $j$ is a bijection onto the ordered pairs of distinct contigs. By (I2), the weight $w(i, j)$ is the overlap of these two contigs.

*A step.* Liveness is never regained: $\mathit{next}$ and $\mathit{prev}$ are never cleared, and two reads in one contig stay in one contig. So by (I3) the first live pair at or after the current position is the first live pair of the whole sorted list. Line L4 skips exactly the pairs that are not live, since for a tail $i$ and a head $j$ the test $\mathit{head}[i] = j$ says that they lie in the same contig. So the pair $(i, j)$ that reaches line L5 is a pair of contigs $(X, Y)$ with the largest overlap, with ties broken by the smaller $i$ and then the smaller $j$. If its weight is below $\tau$, then every remaining pair has a weight below $\tau$, and the loop stops. Otherwise lines L6 and L7 join the two chains, set $\mathit{next}[i]$ and $\mathit{prev}[j]$, and record the new head and tail, so (I1) holds. The new contig string is $X \cdot Y[w(i, j)..]$ with $w(i, j) = \mathrm{ov}(X, Y)$, which is the merge of Lemma 3 with $a = X$ and $b = Y$. Lemma 3 gives (I2) for the new set, since the new contig has head $\mathrm{head}(X)$ and tail $\mathrm{tail}(Y)$. The accepted pair is no longer live, so (I3) holds.

So the scan performs exactly the string form of the algorithm: at each round it merges two current strings with the largest overlap, while that overlap is at least $\tau$.

**Termination.** Each pass of line L3 moves to the next pair of a finite list of $m(m - 1)$ pairs, and each accepted pair lowers the number of contigs by exactly one, so the loop ends. Line L8 walks each chain once.

**Superstring.** By Lemmas 1 and 2, every input read occurs in some output contig.

**One contig when $\tau = 0$.** Suppose two contigs $X \ne Y$ remain at the end, and let $t = \mathrm{tail}(X)$ and $h = \mathrm{head}(Y)$. The pair $(t, h)$ is live at the end, so by the remark on liveness it was live when the scan passed it, and its weight is at least $0 = \tau$. Then it was accepted, and $t$ is not a tail, a contradiction. The loop can also stop at $m - 1$ merges, and then one contig is left.

**Theorem (reconstruction).** Let $x$ be a string of length $G$, and let $R$ be the length of its longest repeat: the largest $\ell$ such that some string of length $\ell$ occurs at two different positions of $x$ ($R = 0$ if there is none). Let the reads be substrings $x[p..e)$ of $x$, each given as a string. Call a read *maximal* if its interval $[p, e)$ is not strictly inside the interval of another read. Let the distinct maximal intervals be $[p_1, e_1), \ldots, [p_k, e_k)$ with $p_1 < \cdots < p_k$. Assume $p_1 = 0$, $e_k = G$, and $e_i - p_{i+1} > R$ for $1 \le i < k$. Then GREEDY-ASSEMBLE with any $\tau \le R + 1$ returns the one contig $x$.

*Proof.* No maximal interval contains another, so $e_1 < \cdots < e_k$ too. Each maximal read has length greater than $R$: for $k = 1$ it is $x$ itself, which has length $G > R$; for $k \ge 2$ it overlaps a neighbour by more than $R$ letters. A string longer than $R$ occurs at exactly one position of $x$.

*Line L1.* A read that is not maximal lies inside a maximal one, as an interval and so as a string, and is removed. A maximal read $u$ that occurs as a string in a read $v$ occurs in $x$ inside the interval of $v$; it occurs in $x$ only at its own interval, so its interval lies inside the interval of $v$, and maximality makes the two intervals equal. So line L1 keeps exactly one copy of each maximal read.

*Invariant.* The current strings are $x[a_1..b_1), \ldots, x[a_t..b_t)$ with $a_1 = 0 < a_2 < \cdots < a_t$, $b_1 < \cdots < b_t = G$, $b_j - a_{j+1} > R$ for $j < t$, and each of length greater than $R$. This holds after line L1 with the maximal intervals.

*A round.* Let $t \ge 2$. The true overlap $b_1 - a_2 > R$ is a proper overlap of the first two strings, so the largest overlap $k^*$ of a pair $(u, v)$ of current strings satisfies $k^* > R \ge \tau - 1$, and the loop does not stop. The common part has length $k^* > R$, so it occurs at one position of $x$; it ends at $b_u$ as a suffix of $u$ and starts at $a_v$ as a prefix of $v$, so $a_v = b_u - k^*$. Since the overlap is proper, $a_u < a_v$ and $b_u < b_v$. If some current string $z$ had $a_u < a_z < a_v$, then $b_u < b_z$, and the suffix of $u$ from $a_z$ would be a proper prefix of $z$ of length $b_u - a_z > b_u - a_v = k^*$, which contradicts the choice of $k^*$. So $u$ and $v$ are the $j$-th and $(j+1)$-th strings for some $j$, the merge uses the overlap $k^* = b_j - a_{j+1}$, and it yields $x[a_j..b_{j+1})$. The new list satisfies the invariant: the starts and ends stay sorted, the overlaps with the neighbours are unchanged, and the new string is longer than $R$.

Each round lowers $t$ by one and the loop does not stop while $t \ge 2$, so it ends with $t = 1$, and the one string is $x[0..G) = x$. $\blacksquare$
