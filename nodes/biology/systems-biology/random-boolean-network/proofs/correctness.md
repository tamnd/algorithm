---
title: The attractor scan finds every attractor and basin, and two exact means of the random ensemble
proves: [correctness]
status: full
---

**Setup.** Let $F$ be a map of a finite set $Q$ of $M$ states to itself, here $Q = \{0, 1\}^N$ and $M = 2^N$. A state $x$ is *cyclic* if $F^k(x) = x$ for some $k \ge 1$. The cycles of $F$ are the attractors, and the basin of an attractor $C$ is the set of states $x$ with $F^t(x) \in C$ for some $t \ge 0$.

**Lemma 1.** Every state reaches exactly one cycle, so the basins partition $Q$.

*Proof.* The sequence $x, F(x), F^2(x), \ldots$ takes values in a finite set, so $F^a(x) = F^b(x)$ for some $a < b$, and $F^a(x)$ is cyclic. Once the sequence is on a cycle it stays on that cycle, because $F$ maps a cycle to itself. Two different cycles are disjoint, since each state has one successor. So the cycle that the sequence enters is unique. $\square$

**Theorem 1 (the scan).** ATTRACTORS returns every cycle of $F$ once, and the label of each state is the cycle that it reaches. It makes $O(M)$ calls of $F$.

*Proof.* We show by induction over the scan the invariant: every labeled state carries the cycle that it reaches, and every cycle that contains a labeled state has been reported once. It holds at the start, when no state is labeled. Take the scan of $s$ (lines L3 to L6), with $s$ unlabeled. Line L4 follows $s, F(s), \ldots$ and stops at the first state $t$ that is labeled or already on the path; it stops because the states on the path are distinct and $Q$ is finite.

If $t$ is labeled, with cycle $a$, then by the invariant $t$ reaches $a$, so every state on the path, which reaches $t$, reaches $a$, and line L6 labels it $a$. No state on the path is on a new cycle: a cyclic state on the path would make the walk return to it before reaching $t$, which line L4 would have caught as a repeat. So no cycle is missed.

If $t$ is not labeled, it is on the path, so the walk from $t$ returns to $t$, and the part of the path from $t$ onward is a cycle $C$. No state of $C$ was labeled before, so by the invariant $C$ had not been reported, and line L5 reports it now. The states of the path before $t$ reach $C$, and line L6 labels all of them $C$.

Each state is appended to a path once, since it is labeled at the end of that scan and later scans stop at labeled states. So the total length of all paths is $M$, and there are $O(M)$ calls of $F$. After the scan of all $s$ every state is labeled; every cycle contains a labeled state and so has been reported once. $\square$

**Lemma 2 (the second method of the test).** Let $X_0 = Q$ and $X_{t+1} = F(X_t)$. The sequence is decreasing, it becomes constant, and its limit is the set of cyclic states.

*Proof.* $X_1 \subseteq X_0$, and $X_{t+1} \subseteq X_t$ implies $X_{t+2} = F(X_{t+1}) \subseteq F(X_t) = X_{t+1}$. A decreasing sequence of finite sets becomes constant, say $X$, with $F(X) = X$. Then $F$ is onto $X$, so it is a permutation of the finite set $X$, and every state of $X$ is cyclic. Conversely, a cyclic state $x$ with $F^k(x) = x$ is $F^{tk}(x) \in X_{tk}$ for all $t$, so it is in $X$. $\square$

**Theorem 2 (fixed points).** For the random ensemble with any $N$, $K$ and bias $p$, the expected number of fixed points is 1.

*Proof.* For a fixed state $x$, $f_i(x)$ is one entry of the table of gene $i$, a bit that is 1 with probability $p$, independent of the input list. So $P(F(x)_i = x_i) = p^{x_i} (1 - p)^{1 - x_i}$. The tables of different genes are independent, so $P(F(x) = x) = \prod_{i} p^{x_i} (1 - p)^{1 - x_i}$. Summing over all $x \in \{0, 1\}^N$ gives $\prod_i (p + (1 - p)) = 1$, and by linearity of expectation this sum is the expected number of fixed points. $\square$

**Theorem 3 (spread).** Draw a network from the ensemble, a state $x$ and a gene $g$, independently and uniformly. The expected number of genes $i$ with $F(x)_i \neq F(x \oplus e_g)_i$ is $2 p (1 - p) K$.

*Proof.* Fix $i$. If $g$ is not in the input list of $i$, the two arguments of $f_i$ are equal and so are the values. If $g$ is in the list, which has probability $K / N$ for a uniform list of $K$ distinct genes, the two arguments differ in one coordinate, so they are two different entries of the table of $i$. These are independent bits with bias $p$, given the list, $x$ and $g$, and they differ with probability $2 p (1 - p)$. So $P(\text{gene } i \text{ changes}) = \frac{K}{N} \cdot 2 p (1 - p)$, and summing over the $N$ genes gives $2 p (1 - p) K$. $\square$

**Theorem 4 (fully random networks).** For $K = N$ and $p = 1/2$, $F$ is uniform among all $M^M$ maps of $Q$ to itself.

*Proof.* For $K = N$, the input list of gene $i$ is a permutation of all genes, so the entries of its table are in one to one correspondence with the states, and $F(x)_i$ is a separate bit of the table for each $x$. All $N \cdot M$ bits are independent and uniform, so the $M$ values $F(x)$ are independent and uniform on $Q$. $\square$

The exact law of the number of cycles of a uniform random map, which the test uses, is checked there against an enumeration of all $27$ maps on 3 points.
