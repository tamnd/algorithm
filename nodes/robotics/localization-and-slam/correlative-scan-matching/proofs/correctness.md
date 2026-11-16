---
title: The branch and bound of correlative scan matching returns a pose of the largest score in the window
proves: [correctness]
status: full
---

**Setting.** $L$ is a table of real (in the code, integer) scores on $\mathbb{Z}^2$, with $L(c) = 0$ outside a finite grid. For a block side $D \ge 1$, $L_D(c) = \max_{0 \le a, b < D} L(c + (a, b))$. The window is a finite set of angles $\Theta$ and the shifts $T = \{-w, \dots, w\}^2$. For each $\theta \in \Theta$, the scan gives cells $c_1(\theta), \dots, c_n(\theta) \in \mathbb{Z}^2$, and the score of a pose is $s(\theta, t) = \sum_i L(c_i(\theta) + t)$. The blocks are $B_b = (\{b_x, \dots, b_x + D - 1\} \times \{b_y, \dots, b_y + D - 1\}) \cap T$ for the corners $b = (b_x, b_y)$ with $b_x, b_y \in \{-w, -w + D, -w + 2D, \dots\}$, $b_x, b_y \le w$. The coarse score of a block is $U(\theta, b) = \sum_i L_D(c_i(\theta) + b)$.

**Assumptions.**

- (A1) The arithmetic on scores is exact. (The code uses integers.)
- (A2) The heap returns an entry with the largest $U$ among the entries it holds.

**Claim.** The algorithm ends, and it returns a pose $(\theta^*, t^*) \in \Theta \times T$ with $s(\theta^*, t^*) = \max_{\theta \in \Theta, t \in T} s(\theta, t)$.

*Proof.*

*Step 1: the blocks partition the window.* For one axis, the corners $-w, -w + D, \dots$ up to $w$ split $\{-w, \dots, w\}$ into the disjoint runs $\{b, \dots, \min(b + D - 1, w)\}$, and every shift lies in the run of the largest corner not above it. The product of the runs of the two axes gives that each $t \in T$ lies in exactly one block. Lines L3 to L5 push one entry for each pair of an angle and a block, so each pose $(\theta, t)$ of the window belongs to exactly one heap entry.

*Step 2: the coarse score bounds the block.* Let $t \in B_b$, so $t = b + (a, a')$ with $0 \le a, a' < D$. For each point, $L(c_i(\theta) + t) = L((c_i(\theta) + b) + (a, a')) \le L_D(c_i(\theta) + b)$ by the definition of $L_D$. Summing over $i$ gives $s(\theta, t) \le U(\theta, b)$.

*Step 3: termination.* Each pass through line L8 removes one entry, and nothing is pushed after line L5. The heap has $|\Theta|$ times the number of blocks entries, so the loop runs at most that many times. Each pass scores at most $D^2$ poses. Hence the algorithm ends.

*Step 4: the invariant.* After each pass through lines L8 to L11, $\mathit{best}$ is the largest score of the poses in the entries popped so far, and $\mathit{pose}$ is a pose that reaches it. This holds after zero passes with $\mathit{best} = -\infty$ and the empty set of poses. A pass that does not stop at line L9 scores every pose of its block in line L11 and keeps the largest score, so the invariant holds after it.

*Step 5: the result.* There are two ways to leave the loop.

- The heap is empty. Then every entry was popped and scored in full, so by Step 1 and Step 4, $\mathit{best}$ is the largest score over the whole window.
- Line L9 stops at an entry with $U \le \mathit{best}$. By (A2), every entry left in the heap has a coarse score at most this $U$. By Step 2, every pose in such an entry has a score at most its coarse score, so at most $\mathit{best}$. The popped entry itself also has all its poses at most $U \le \mathit{best}$. Every other pose was in an entry popped earlier and is at most $\mathit{best}$ by Step 4. So no pose of the window has a score above $\mathit{best}$.

In both cases $\mathit{best}$ is the maximum over the window. It is at least the score of any pose, and the scores are finite, so at least one pass scored a pose and $\mathit{pose}$ is set, with $s(\mathit{pose}) = \mathit{best}$. $\blacksquare$

**What this does not show.** The claim is about the discrete window and the given table. It says nothing about how close the best pose of the window is to the true pose; that depends on the resolution, the kernel and the scene.
