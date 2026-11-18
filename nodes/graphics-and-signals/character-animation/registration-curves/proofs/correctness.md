---
title: The slope limited time warp is a minimum cost monotone path, and the blended times never decrease
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact.
$D$ is an $n$ by $m$ matrix of frame distances, $D_{ij} \ge 0$.
A step is one of $(1, 1)$, $(1, 0)$ and $(0, 1)$.
An admissible path starts at $(0, 0)$, ends at $(n - 1, m - 1)$, and has no run of more than $L$ equal steps of kind $(1, 0)$, and none of more than $L$ steps of kind $(0, 1)$.
Its cost is the sum of $D_{ij}$ over its cells, the first one included.

## The state graph

A state is $(i, j, s, r)$: the cell, the kind of the last step ($s = 0$ for the diagonal, 1 for $(1, 0)$, 2 for $(0, 1)$), and the length $r$ of the current run of non-diagonal steps of that kind ($r = 0$ after a diagonal step).
The start state is $(0, 0, 0, 0)$.
From $(i, j, s, r)$, a step of kind $k$ goes to $(i + \delta_i, j + \delta_j, k, r')$ with $r' = 0$ if $k = 0$, $r' = r + 1$ if $k = s \ne 0$, and $r' = 1$ otherwise; line L4 forbids it if $r' > L$, and the step must stay in the matrix.
The cost of entering a state is $D$ at its cell (line L5).

**Lemma 1.** Admissible paths correspond one to one to walks in the state graph from the start state to a state with cell $(n - 1, m - 1)$, and the cost of the path is $D_{00}$ plus the costs of the entered states.

*Proof.*
Given a path, the states are fixed by its steps: $s$ is the last step and $r$ counts the run, by the rule above.
The run limit of the path is exactly the test $r' \le L$.
Conversely, the cells of a walk form a path whose runs are the counts $r$, so it is admissible. $\square$

**Lemma 2.** The state graph has no cycle, and the loops of lines L2 and L3 process every state after all its predecessors.

*Proof.*
Every step increases $i + j$ by 1 or 2, so there is no cycle.
A predecessor of a state at $(i, j)$ is at $(i - 1, j - 1)$, $(i - 1, j)$ or $(i, j - 1)$.
The loops visit the cells with $i$ in the outer loop and $j$ in the inner loop, so all three come earlier. $\square$

**Theorem 1.** Line L6 returns the smallest cost of an admissible path, line L7 returns such a path, and the code raises an error exactly when no admissible path exists.

*Proof.*
By Lemma 2, when the loop reaches a state, every relaxation into it is done, and best holds the minimum over its predecessors of their best value plus $D$ at its cell.
By induction along the order of Lemma 2, best of each reached state is the smallest cost of a walk from the start to it, and its stored predecessor gives such a walk.
States that no walk reaches never enter best.
Line L6 takes the minimum over the end states, and Lemma 1 turns walks into admissible paths with the same cost.
If no end state is reached, there is no admissible path, and the code raises an error. $\blacksquare$

**Theorem 2.** The path is monotone in both indices, and every window of $L + 1$ consecutive steps contains a step that moves $i$ and a step that moves $j$.
So the time warp never goes back in time, and it cannot hold one motion still while the other plays for more than $L$ frames.

*Proof.*
Every step has $\delta_i, \delta_j \ge 0$.
A window of $L + 1$ steps with no step moving $j$ would be $L + 1$ steps of kind $(1, 0)$ in a row, which the run limit forbids; the same holds for $i$. $\blacksquare$

Note that an admissible path exists only if the shapes allow it: for example $n = 1$ and $m > L + 1$ admit no path.

## The alignment and the blend

The alignment of each pair $(i, j)$ is the best 2D rigid transform of frame $B_j$ onto frame $A_i$; its closed form and its optimality are proved on the motion graph page (Theorem 1 of its proof file).
Line L8 adds a multiple of $2\pi$ to each angle so that it differs from the previous angle by at most $\pi$; this changes no transform.

**Theorem 3.** For a fixed weight $w \in [0, 1]$, the blended times $\tau_l = w\, i_l + (1 - w)\, j_l$ along the path never decrease, start at 0 and end at $w(n - 1) + (1 - w)(m - 1)$.
If $0 < w < 1$, they strictly increase.

*Proof.*
From one path pair to the next, $i$ and $j$ do not decrease and at least one increases, so $\tau_{l+1} - \tau_l = w\,\delta_i + (1 - w)\,\delta_j \ge 0$, and it is positive when both weights are positive.
The ends are the corners of the path. $\blacksquare$

**Theorem 4.** If $B_j = T^{-1}(A_j)$ for one rigid transform $T$ about the vertical axis and $n = m$, then every alignment is $T$ (up to $2\pi$ in the angle), the diagonal path has cost 0, and the blend at any $w$ equals $A$ along the diagonal.

*Proof.*
The aligned distance of $A_i$ and $B_i$ is 0, which is the smallest possible value, so the diagonal path has cost 0 and is a minimum cost path.
For each pair the transform $T$ makes the residual zero, so it minimizes the alignment energy; it is the one the closed form returns when the points do not all lie on the vertical line through their mean.
The blend is $w A_i + (1 - w) T(B_i) = A_i$. $\blacksquare$

The test checks that the path is the diagonal in this case; with other paths of cost 0 the code could return another one, which a strictly positive distance off the diagonal rules out.
