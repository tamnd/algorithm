---
title: Arpa's trick returns the leftmost minimum of each range
proves: [correctness, termination]
status: full
---

Write $\mathrm{root}(t)$ for the root of the tree of $t$ in the forest $p$. Positions are compared as integers. We prove an invariant of the sweep and derive the answers from it.

**Invariant (A).** After line L7 of step $i$, let the stack be $s_1 < s_2 < \cdots < s_k = i$, and put $s_0 = -1$. Then:

1. $a[s_1] \le a[s_2] \le \cdots \le a[s_k]$;
2. for $0 \le t \le i$, $\mathrm{root}(t) = s_j$ for the least $j$ with $s_j \ge t$, and positions $t > i$ are their own roots;
3. for each $j$ and each $t$ with $s_{j-1} < t \le s_j$, every $u \in [t, s_j)$ has $a[u] > a[s_j]$.

So part 3 says that $s_j$ is the unique leftmost minimum of $a[t..s_j]$: every earlier position of the interval has a strictly larger value.

We also use that every parent pointer goes to a larger position, $p[t] \ge t$, with equality only at roots. Line L6 sets $p[j] \leftarrow i$ with $j < i$, and path compression sets $p[x] \leftarrow r$ with $r$ the root reached from $x$, which is larger than $x$ when $x$ is not a root. So FIND climbs strictly increasing positions and stops after at most $n$ steps. This is the **termination** of each FIND; the sweep has $n$ steps, each position is pushed once and popped at most once, and there are $q$ finds, so the algorithm terminates.

**Path compression keeps the roots.** A FIND sets $p[x]$ to $\mathrm{root}(x)$ for nodes on the path to that root, so each node keeps its root. So the statements of (A), which speak only of roots, the stack and the array, are not changed by the finds of lines L8 and L9. We can ignore compression below.

**Base.** Before step 0 the stack is empty and every position is a root. In step 0 nothing is popped and 0 is pushed. Then $k = 1$, $s_1 = 0$, part 1 is empty, part 2 holds since $\mathrm{root}(0) = 0$, and part 3 holds for $t = 0$, because the range $[0, 0)$ is empty.

**Step.** Assume (A) after step $i - 1$, with the stack $s_1 < \cdots < s_k = i - 1$. In step $i$, the loop of lines L5 and L6 pops $s_k, s_{k-1}, \ldots, s_{h+1}$, the positions with $a[s_j] > a[i]$, and stops at $s_h$ with $a[s_h] \le a[i]$, or $h = 0$ when the stack runs out. By part 1, the popped positions are exactly the top ones with values larger than $a[i]$, because the values on the stack do not fall from bottom to top. Each popped $s_j$, which is a root, gets the parent $i$, which is a root. Line L7 pushes $i$. The new stack is $s_1 < \cdots < s_h < i$.

*Part 1.* $a[s_h] \le a[i]$ by the stop condition, and the lower part is unchanged.

*Part 2.* For $t \le s_h$, the root of $t$ is the old one, $s_j$ with $j \le h$, which is still on the stack and is the least stack position $\ge t$. For $s_h < t \le i - 1$, the old root was some popped $s_j$ with $j > h$, which now has the parent $i$, a root; so $\mathrm{root}(t) = i$, the least stack position $\ge t$. For $t = i$, $\mathrm{root}(i) = i$. Positions after $i$ are untouched.

*Part 3.* For the intervals $(s_{j-1}, s_j]$ with $j \le h$, nothing changed. For the new last interval $(s_h, i]$, take $t$ in it. If $t = i$ the claim is trivial. Otherwise $t$ lies in an old interval $(s_{j-1}, s_j]$ with $h < j \le k$. By part 3 for the old state, every $u \in [t, s_j]$ has $a[u] \ge a[s_j] > a[i]$, because $s_j$ was popped. For $u$ in a later old interval $(s_{l-1}, s_l]$ with $j < l \le k$, the same argument applied to $t' = s_{l-1} + 1$ gives $a[u] \ge a[s_l] > a[i]$. So every $u \in [t, i)$ has $a[u] > a[i]$, which is part 3 for the new interval.

So (A) holds after step $i$.

**The answers.** At line L9 of step $i$, take a query $(L, i)$. By part 2, $\mathrm{FIND}(L) = s_j$, the least stack position $\ge L$, so $s_{j-1} < L \le s_j$. By part 3 with $t = L$, every $u \in [L, s_j)$ has $a[u] > a[s_j]$. For $u \in (s_j, i]$, $u$ lies in some interval $(s_{l-1}, s_l]$ with $l > j$, and by part 3 and part 1, $a[u] \ge a[s_l] \ge a[s_j]$. So $a[s_j]$ is the minimum of $a[L..i]$, and no position before $s_j$ in the range reaches it. So $s_j$ is the leftmost minimum, which is the required answer. $\blacksquare$
