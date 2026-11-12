---
title: GDSF keeps its keys above L, contains LRU, and has no constant competitive ratio
proves: [correctness]
status: full
---

We use the pseudocode of the page. The cache has capacity $k$. The key of a cached file is $\mathrm{Pr}(f)$, and the order of files is by key, with ties broken by the time the key was set (the older key first). The new file at a miss is newer than each cached file.

## 1. The heap code chooses the right victims

The rule in the report is: take the files of the cache, with the new file $f$ among them, in increasing order, and stop as soon as the files taken so far free enough space for $f$. If $f$ is among the files taken, cache nothing and evict nothing; otherwise evict the files taken.

Lines L6 to L10 pop the cached files in increasing order. Before they take a cached file $g$, line L8 compares $g$ with $f$; if $f$ comes first, then $f$ is the next file in the order of the report, and since space is still missing, the report would take $f$. So line L9 refuses $f$ in exactly the cases where the report does. If all cached files are taken and space is still missing (this happens only if $s(f) > k$), the next file in the order is $f$, and line L7 gives the same answer. The popped entries are pushed back unchanged, so a refusal leaves the heap as it was, up to the order of equal entries, which the time stamps fix.

## 2. Keys stay at least $L$, and $L$ never falls

**Claim.** After each request, each cached key is at least $L$, and $L$ is at least its value before the request.

*Proof.* By induction on the requests. At the start the cache is empty and $L = 0$.

- *Hit.* Line L3 sets $\mathrm{Pr}(f) = L + \mathrm{Fr}(f)\,c(f)/s(f) \ge L$, and $L$ does not change.
- *Miss, $f$ refused.* Nothing changes.
- *Miss, no eviction.* Line L5 gives $f$ the key $L + c(f)/s(f) \ge L$.
- *Miss with evictions.* Let $g_1, \ldots, g_r$ be the files taken, in order. Line L12 sets $L' = \mathrm{Pr}(g_r)$. By the induction hypothesis $\mathrm{Pr}(g_r) \ge L$, so $L' \ge L$. Each file that stays was not taken, so it comes after $g_r$ in the order, and its key is at least $L'$. The new file was not taken either, so it also comes after $g_r$, and its key is at least $L'$. $\square$

So $L$ works as a clock: a file that is not requested keeps its key while $L$ rises past it, and then it is among the first to go.

## 3. LRU is a special case

Let all sizes and costs be $1$ and keep $\mathrm{Fr} = 1$. Each key is $L_t + 1$, where $L_t$ is the value of $L$ when the key was set at time $t$. Since $L$ never falls, a key set later is at least as large as a key set earlier, and ties go to the older key. So the order of the cached files is the order of their last requests. The new file gets $L + 1$, which is at least each cached key, so it is never first in the order and is always cached. The file taken is the least recently used one. This is [LRU](/lru/).

## 4. No constant competitive ratio

Take $k = 2$, unit sizes and costs, an integer $N \ge 1$, and the sequence $a^N (b\,c)^N$.

The first request for $a$ misses, and the next $N - 1$ hit, so $\mathrm{Pr}(a) = N$ and $L = 0$. The request for $b$ misses and fits. From then on, as long as $a$ stays, the cache holds $a$ and one file $x \in \{b, c\}$, and the request is for the other file, so it misses. Number these misses $j = 1, 2, \ldots$, with $j = 1$ the miss on $b$, and let $x_j$ be the file loaded at miss $j$ and $L_j$ the value of $L$ after it.

At miss $j \ge 2$ the new file gets the key $L_{j-1} + 1$, computed before the eviction. If the victim is $x_{j-1}$, then $L_j = \mathrm{Pr}(x_{j-1}) = L_{j-2} + 1$, with $L_0 = L_1 = 0$. So, as long as $a$ stays, $\mathrm{Pr}(x_j) = \lceil j/2 \rceil$. The new key is never below the key of $x_{j-1}$, so the new file is never refused. The victim is the smaller of $a$ and $x_{j-1}$ in the order, and $a$ is older, so $a$ is evicted at the first miss $j$ with $\mathrm{Pr}(x_{j-1}) \ge N$, that is, at $j = 2N$. That is the last request of the sequence, and all $2N$ requests of the loop miss.

So GDSF has $2N + 1$ misses. An offline policy evicts $a$ at the first request for $c$ and has $3$ misses. Since $N$ is arbitrary, no constants $\alpha, \beta$ give $\mathrm{GDSF} \le \alpha \cdot \mathrm{OPT} + \beta$ on all sequences. GreedyDual-Size, which keeps no count, is $k$-competitive (see [GreedyDual](/greedy-dual/)); the count is what loses the bound. $\square$
