---
title: Parallel map writes f(A[i]) to every B[i] without races, with the stated work and span
proves: [correctness]
status: full
---

**Statement.** Let $f$ be a function whose calls do not write shared memory, and let $A[0 \ldots n-1]$ be an array. PARALLEL-MAP returns the array $B$ with $B[i] = f(A[i])$ for every $i$, and its result does not depend on the schedule. Let call $i$ of $f$ have work $W_i$ and span $S_i$, and let each split node (line L2 to line L5, one spawn and one sync) cost 1 unit of work and 1 unit of span. Then for $n \ge 1$,
$$
W = (n - 1) + \sum_{i} W_i, \qquad \lfloor \lg n \rfloor + \max_i S_i \;\le\; S \;\le\; \lceil \lg n \rceil + \max_i S_i,
$$
with $S = \lceil \lg n \rceil + s$ when every $S_i = s$.

## 1. The call tree

Each call of MAP on a range of $m \ge 2$ items makes two calls, on $\lceil m/2 \rceil$ and $\lfloor m/2 \rfloor$ items, both at least 1 and less than $m$; a call on one item makes none. So the calls form a full binary tree. Its leaves are calls on single items, and by induction on $m$ the leaf ranges of a call on $[lo, hi)$ are exactly $[i, i+1)$ for $lo \le i < hi$, each once: the ranges of the two children split $[lo, hi)$ at $mid$ into two disjoint parts. So the tree has $n$ leaves, one for each index, and $n - 1$ inner nodes.

## 2. The result and the absence of races

The leaf for index $i$ runs line L1, which reads $A[i]$, calls $f$ and writes $B[i]$. No other line writes $B$, and no line reads $B$ before line L8. So the only write to $B[i]$ is by the leaf for $i$, and two different leaves write different cells. The calls of $f$ do not write shared memory by assumption, and $A$ is only read. So no two logically parallel strands access the same location with at least one write: the program has no [determinacy race](/determinacy-race/), and every schedule gives the same final memory. Line L5 waits for the spawned half, and the sync of the root call finishes before line L8, so all leaves have written when $B$ is returned. Thus $B[i] = f(A[i])$ for every $i$. For $n = 0$, line L7 skips the call and the empty array is returned.

## 3. The work

The work is the sum of the costs of all nodes of the call tree: $n - 1$ inner nodes of cost 1 and the $n$ leaves of cost $W_i$. So $W = (n - 1) + \sum_i W_i$.

## 4. The span

The two calls of a split node run in parallel, and the node waits for both, so the span of a call is $1 + \max$ of the spans of its children, and the span of a leaf $i$ is $S_i$. Unrolling this, the span of the root is $\max_i (d_i + S_i)$, where $d_i$ is the depth of leaf $i$, the number of inner nodes on the path from the root.

The depths satisfy $\lfloor \lg n \rfloor \le d_i \le \lceil \lg n \rceil$. For the upper bound, let $D(m)$ be the largest leaf depth for $m$ items: $D(1) = 0$ and $D(m) = 1 + D(\lceil m/2 \rceil)$, since $D$ does not decrease. By the identity $\lceil \lg \lceil m/2 \rceil \rceil = \lceil \lg m \rceil - 1$ (Lemma 1 of the [parallel reduce proof](/parallel-reduce/)), induction gives $D(m) = \lceil \lg m \rceil$. For the lower bound, the smallest leaf depth $d(m)$ satisfies $d(1) = 0$ and $d(m) = 1 + d(\lfloor m/2 \rfloor)$, and $\lfloor \lg \lfloor m/2 \rfloor \rfloor = \lfloor \lg m \rfloor - 1$ for $m \ge 2$, so $d(m) = \lfloor \lg m \rfloor$.

So $S = \max_i (d_i + S_i)$ is at most $\lceil \lg n \rceil + \max_i S_i$, and at least $d_j + S_j \ge \lfloor \lg n \rfloor + \max_i S_i$ for an index $j$ with the largest $S_j$. When every $S_i = s$, the deepest leaf gives $S = \lceil \lg n \rceil + s$. $\blacksquare$
