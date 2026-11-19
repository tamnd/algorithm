---
title: Simplified Lesk returns the first sense of largest overlap, or the first sense
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The target word $w$ has the senses $s_1, \ldots, s_r$ with $r \ge 1$, in dictionary order. Let $C$ be the context set of line L3: the context words, lowercased, without the stop words and without $w$. Let $S_i$ be the signature of $s_i$ (line L5) and $o_i = |S_i \cap C|$ its overlap (line L6). Let $M = \max(0, o_1, \ldots, o_r) = \max_i o_i$, since each $o_i \ge 0$.

**Claim.** SIMPLIFIED-LESK stops and returns $s_{i^*}$, where $i^* = 1$ if $M = 0$, and otherwise $i^*$ is the smallest index $i$ with $o_i = M$.

*Proof.* For $0 \le t \le r$ let $M_t = \max(0, o_1, \ldots, o_t)$, with $M_0 = 0$. We use this invariant of the loop of line L4.

> **(I)** After the first $t$ iterations, $maxoverlap = M_t$, and $best = s_1$ if $M_t = 0$, while otherwise $best = s_j$ for the smallest $j \le t$ with $o_j = M_t$.

*Initialization.* Before the loop, $t = 0$. Lines L1 and L2 set $best = s_1$ and $maxoverlap = 0 = M_0$, which is (I) for $t = 0$.

*Maintenance.* Assume (I) after $t$ iterations, with $t < r$. The next iteration computes $o_{t+1}$ in lines L5 and L6.

- If $o_{t+1} > M_t$, then $M_{t+1} = o_{t+1} > 0$, and $t + 1$ is the smallest index $j \le t + 1$ with $o_j = M_{t+1}$, because every earlier $o_j$ is at most $M_t < o_{t+1}$. Line L7 is true and line L8 sets $maxoverlap = o_{t+1}$ and $best = s_{t+1}$. So (I) holds after $t + 1$ iterations.
- If $o_{t+1} \le M_t$, then $M_{t+1} = M_t$, and the smallest index with the value $M_{t+1}$ (when $M_{t+1} > 0$) is the same as before, since an index $t + 1$ with $o_{t+1} = M_t$ comes after it. Line L7 is false and nothing changes, so (I) holds after $t + 1$ iterations.

*Termination.* The loop runs over the $r$ senses once, so it stops. With $t = r$, (I) gives $maxoverlap = M_r = M$ and $best = s_{i^*}$, and line L9 returns it. $\square$

**The pair form.** GLOSS-PAIR-LESK takes two words with the senses $a_1, \ldots, a_r$ and $b_1, \ldots, b_u$ and visits the pairs $(a_x, b_y)$ in the order of $x$ and then $y$. It keeps a pair and its overlap, starts with the overlap $-1$, and replaces the pair only when a strictly larger overlap appears. The same argument, with the visiting order in place of the index order and $-1$ in place of $0$, shows that it returns the first pair in that order whose overlap $|S(a_x) \cap S(b_y)|$ is the largest. Since the first overlap is at least $0 > -1$, some pair is always kept. $\blacksquare$
