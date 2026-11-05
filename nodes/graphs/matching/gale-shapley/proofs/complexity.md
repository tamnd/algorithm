---
title: Gale-Shapley runs in O(n + m) time
proves: [time.worst]
status: full
---

Let $n = |P| + |R|$ and let $m$ be the total length of all preference lists. Agents are indices, and each array access, comparison and stack operation costs $O(1)$ on the [word RAM](/word-ram/).

**Preprocessing, line L1.** For each entry $r$ at position $i$ on the list of $p$, append the pair $(p, i)$ to a bucket of $r$: $O(n + m)$. Then for each receiver $r$, write $\text{mark}[q] \leftarrow$ the position of $q$ on the list of $r$ for each $q$ on that list, read $\text{mark}[p]$ for each pair $(p, i)$ in the bucket of $r$ and store it at entry $i$ of the list of $p$ (or $-1$ if $p$ is not on the list of $r$), and reset the marks. Each list entry is touched a constant number of times, so this costs $O(n + m)$ and gives $\text{rank}_r(p)$ at the moment of the proposal in $O(1)$.

**The main loop.** By the termination argument of the correctness proof, there are at most $|P| + m$ passes, and each pass costs $O(1)$: a pop, one test on $\text{next}[p]$, one list access, one rank comparison and at most one push. Line L12 costs $O(n)$. The total time is $O(n + m)$.

**Complete lists.** Let $|P| = |R| = k$ with complete lists, so $m = 2k^2$ and the bound is $O(k^2)$. The number of proposals is at most $k^2 - k + 1$. Suppose $p$ proposes to the last receiver $r$ on its list. Then $p$ has been rejected by the other $k - 1$ receivers, and each of them holds someone from then on, by Claim 2 of the correctness proof. If $r$ had received a proposal before, all $k$ receivers would hold proposers, so all $k$ proposers would be held, while $p$ is free; so this is the first proposal to $r$. After it all $k$ receivers hold a proposer, so $F$ becomes empty and the run ends. Hence at most one proposer makes $k$ proposals, and the others make at most $k - 1$ each: in total at most $(k - 1)^2 + k = k^2 - k + 1$.

**Space.** The lists, the rank entries, the buckets, the arrays $\text{next}$, $\text{holder}$ and $\text{mark}$, and a stack of at most $|P|$ entries take $\Theta(n + m)$ space. $\blacksquare$
