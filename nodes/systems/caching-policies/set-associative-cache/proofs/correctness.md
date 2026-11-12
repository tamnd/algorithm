---
title: A set-associative cache is S separate caches of W blocks, and with one set and LRU it is fully associative LRU
proves: [correctness]
status: full
---

We use the pseudocode of the page. The cache has $S = 2^s$ sets of $W$ ways and blocks of $B = 2^b$ bytes. For a byte address $a$, the block number is $\beta(a) = \lfloor a / B \rfloor$, the set is $\beta(a) \bmod S$ and the tag is $\lfloor \beta(a) / S \rfloor$.

## 1. The address split

**Claim 1.** Line L1 gives offset $= a \bmod B$, index $= \beta(a) \bmod S$ and tag $= \lfloor \beta(a)/S \rfloor$. The map from a block number to the pair (tag, index) is one to one.

*Proof.* The low $b$ bits of $a$ are $a \bmod 2^b$, and shifting right by $b$ gives $\lfloor a / 2^b \rfloor = \beta(a)$. The low $s$ bits of $\beta(a)$ are $\beta(a) \bmod 2^s$, and the bits above them are $\lfloor \beta(a) / 2^s \rfloor$. Since $\beta = \text{tag} \cdot S + \text{index}$ with $0 \le \text{index} < S$, the pair gives $\beta$ back, so two different blocks never have the same tag and index. $\square$

So inside one set, the tag names the block. Two addresses in the same block give the same set and tag, so they hit or miss together.

## 2. The invariant of a set

**Claim 2.** After each access, each set holds at most $W$ tags, all different, and a block $\beta$ is in the cache if and only if its tag is in a way of set $\beta \bmod S$.

*Proof.* At the start every way is empty. An access to set $s$ changes only set $s$. On a hit (lines L3 to L6) no tag changes. On a miss, the tag is in no way of the set, by lines L3 and L4. Line L7 picks one way, and line L8 writes the new tag there and drops the old one. So the tags stay different, and the number of ways bounds their count. By Claim 1, the block with this tag and this index is exactly $\beta$, so the second part holds. $\square$

**Claim 3.** Let $\sigma$ be a sequence of addresses. For each set $s$, the hits and misses of the requests with index $s$ are the same as those of a fully associative cache of $W$ blocks, with the same policy, run on only these requests.

*Proof.* By Claim 2, whether a request hits depends only on the tags in its set. Lines L2 to L10 read and write only the tags and the state of that set. With LRU the state is the time of the last use of each way, and with tree PLRU it is the $W - 1$ bits of the set; both change only on an access to the set. So the run of set $s$ does not depend on the requests to other sets, and it is the run of a $W$-way cache on its own subsequence. (For the random policy this holds when each set has its own random source; with one shared source, the sets are still separate caches, but their random choices are drawn from one stream.) $\square$

## 3. Special cases

**Fully associative LRU.** With $S = 1$ there are no index bits, every block maps to set 0, and the tag is the block number. By Claim 3 the cache is one $W$-way cache on the whole sequence. With LRU, line L5 or L9 stamps the used way with the current time. Line L7 takes an empty way while one is left, and then the way with the least stamp, which is the block whose last use is the oldest. This is the rule of [LRU](/lru/) on $W$ blocks, so the two give the same hits and misses on every sequence.

**Direct mapped.** With $W = 1$ each set has one way, line L7 has one choice, and every policy is the same: block $\beta$ goes to set $\beta \bmod S$ and replaces what was there.

**Tree PLRU with two ways.** With $W = 2$ the tree has one bit, and each use sets it to point at the other way. When both ways are full, the other way is the one used less recently, so PLRU evicts the same way as LRU. With $W \ge 4$ the two differ; the page gives a sequence of seven accesses where they evict different blocks.

## 4. Conflict misses

Take a direct-mapped cache with $S$ sets and the sequence that alternates two blocks $\beta$ and $\beta + S$. Both have index $\beta \bmod S$, so by Claim 3 they share a cache of one block, and each access evicts the other: every access misses. A cache of the same size with two ways keeps both blocks after two cold misses. A fully associative LRU cache of $S$ blocks with $S \ge 2$ does the same. The misses of the direct-mapped cache beyond those of the fully associative cache of the same size are its conflict misses, in the sense of the [three Cs model](/three-cs-model/).

## 5. Cost

Line L1 is a few shifts and masks. Lines L3 and L4 compare the tag with $W$ stored tags: $O(W)$ time in software, one step with $W$ comparators in hardware. LRU victim choice scans $W$ stamps, and tree PLRU walks $\log_2 W$ bits on a use and on a choice. The storage is $S \cdot W$ blocks of data plus, for each way, a tag of $t - s - b$ bits for $t$-bit addresses, a valid bit, and the policy state of the set.
