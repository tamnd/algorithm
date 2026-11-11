---
title: Split-ordered lists keep each bucket contiguous and are a linearizable lock-free set
proves: [correctness, linearizability, progress]
status: sketch
---

We use the pseudocode and the model of the page. The contiguity lemma and the facts about the bucket array are proved in full. Linearizability is reduced to that of Michael's list, whose proof is sketched on the Harris list page, so this proof is a sketch as a whole.

Write $\mathrm{low}_i(x) = x \bmod 2^i$ for the low $i$ bits of $x$, and $\mathrm{high}_i(y) = \lfloor y / 2^{W-i} \rfloor$ for the high $i$ bits of a $W$-bit number $y$. Let $\mathrm{rev}_i(z)$ be $z$ written in $i$ bits and reversed.

**Lemma 1 (reversal swaps low and high bits).** For a $W$-bit $x$ and $0 \le i \le W$, $\mathrm{high}_i(\mathrm{rev}(x)) = \mathrm{rev}_i(\mathrm{low}_i(x))$.

*Proof.* Bit $j$ of $x$ (counting from 0 at the low end) is bit $W - 1 - j$ of $\mathrm{rev}(x)$. The bits $j < i$ of $x$ go to the positions $W - 1 - j \ge W - i$, which are the high $i$ positions, in reverse order. ∎

**Lemma 2 (contiguity).** Let $t = 2^i \le 2^{W-1}$ and $b < t$. The regular keys $k$ with $h(k) \bmod t = b$ are exactly the regular keys whose split-order key has $\mathrm{high}_i = \mathrm{rev}_i(b)$. So in any list sorted by split-order key, they form one contiguous run of the regular nodes, and the dummy of $b$, whose key is $\mathrm{sd}(b) = \mathrm{rev}(b)$, comes before all of them. Moreover, no dummy of a bucket $c < t$ with $c \ne b$ lies inside the interval from $\mathrm{sd}(b)$ to the last key of the run.

*Proof.* $h(k) \bmod t = \mathrm{low}_i(h(k)) = \mathrm{low}_i(h(k) \mid 2^{W-1})$, since $i \le W - 1$. By Lemma 1, $\mathrm{high}_i(\mathrm{so}(k)) = \mathrm{rev}_i(\mathrm{low}_i(h(k)))$, and $\mathrm{rev}_i$ is a bijection, so $h(k) \bmod t = b$ if and only if $\mathrm{high}_i(\mathrm{so}(k)) = \mathrm{rev}_i(b)$. The $W$-bit numbers with a fixed value of $\mathrm{high}_i$ form an interval $I_b = [\mathrm{rev}_i(b) \cdot 2^{W-i}, (\mathrm{rev}_i(b) + 1) \cdot 2^{W-i})$, so in sorted order the regular keys of bucket $b$ are contiguous among the nodes with keys in $I_b$. By Lemma 1 again, $\mathrm{high}_i(\mathrm{sd}(b)) = \mathrm{rev}_i(\mathrm{low}_i(b)) = \mathrm{rev}_i(b)$, and since $b < 2^i$ its other bits are 0, so $\mathrm{sd}(b) = \min I_b$; it is even and every regular key is odd, so $\mathrm{sd}(b)$ is strictly below every regular key of the bucket. A dummy of $c < t$, $c \ne b$, has $\mathrm{high}_i = \mathrm{rev}_i(c) \ne \mathrm{rev}_i(b)$, so it is outside $I_b$. Finally, a regular key outside the bucket is outside $I_b$, so no such key lies between two keys of the bucket. ∎

**Corollary 3 (splitting moves nothing).** When the number of buckets goes from $t$ to $2t$, the run of bucket $b$ is the union of the runs of $b$ and $b + t$ for $2t$, the run of $b$ comes first, and the dummy of $b + t$ lies exactly between them.

*Proof.* $I_b$ for $t$ is the union of $I_b$ and $I_{b+t}$ for $2t$: the extra high bit is bit $i$ of $h(k)$, which is 0 for $b$ and 1 for $b + t$ and becomes the $(i+1)$-th high bit after the reversal, so $I_b$ for $2t$ is the lower half. By Lemma 2 for $2t$, $\mathrm{sd}(b + t) = \min I_{b+t}$ for $2t$, the first number of the upper half. The list order is fixed by the keys alone, so nothing moves. ∎

**Lemma 4 (the bucket array).** (a) `T[0]` always points to the dummy of 0, the first node of the list. (b) If `T[b]` is not null, it points to a node with key $\mathrm{sd}(b)$ that is in the list, and it never changes again. (c) Dummy nodes are never marked or unlinked.

*Proof.* (c) LIST_DELETE is called only with odd keys, and a search unlinks only marked nodes. (a) is set at the start and never written. (b) `T[b]` is written only by the CAS at L19, from null, so it is written at most once. The value is either the dummy that this process linked at L18, or the node with key $\mathrm{sd}(b)$ that LIST_INSERT found in the list. In both cases the node was in the list, unmarked, before L19, and by (c) it stays in the list. ∎

**Lemma 5 (the start of a search).** An operation on $k$ that read `size` = $t$ starts its list operation at a node $d$ (the dummy of $b = h(k) \bmod t$) such that every node with key $\mathrm{so}(k)$ that is ever in the list comes after $d$.

*Proof.* `size` is always a power of two and only grows, and $b < t$. By Lemma 4 the start node is the dummy of $b$, in the list. By Lemma 2, $\mathrm{sd}(b) < \mathrm{so}(k)$. The list is sorted (an invariant of Michael's list), so any node with key $\mathrm{so}(k)$ comes after $d$. ∎

**Theorem 1 (linearizability).** Each history is linearizable with respect to the sequential set.

*Proof sketch.* All operations are operations of one Michael list on split-order keys, except that they start at a dummy node instead of the head. By Lemma 5 and since dummy nodes are never removed (Lemma 4(c)), a search from $d$ sees the same nodes with key $\mathrm{so}(k)$ that a search from the head would see, and the predecessor it returns is a node in the list. So the argument for Michael's list applies unchanged: the linearization points are those of the list operations. `so` is injective on regular keys and never equals a dummy key, so the set of regular split-order keys in the list, mapped back, is the abstract set. The `count` and `size` words do not change the set. ∎

**Theorem 2 (progress).** The structure is lock-free. INITIALIZE_BUCKET($b$) calls itself at most $\lfloor \log_2 b \rfloor$ times.

*Proof.* The parent of $b$ has one fewer 1 bit than $b$, so the chain $b$, $\mathrm{parent}(b)$, $\mathrm{parent}(\mathrm{parent}(b))$, and so on reaches 0 after as many steps as $b$ has 1 bits, and no call is made for 0 because `T[0]` is set. So INITIALIZE_BUCKET($b$) makes at most (the number of 1 bits of $b$) $- 1 \le \lfloor \log_2 b \rfloor$ nested calls. Each call does one LIST_INSERT and one CAS. The other steps outside the list operations are a bounded number of reads, one fetch-and-add and one CAS. So an infinite run in which no operation completes would be an infinite run of the list in which no list operation completes, which is impossible since the list is lock-free. ∎
