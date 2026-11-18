---
title: The motion matching scan and the k-d tree return the brute force nearest frame
proves: [correctness]
status: full
---

We use the notation of the page.
The database has $f$ frames with raw feature vectors $v_i \in \mathbb{R}^d$, and a list $P$ of playable frames in increasing order.
Line L1 maps a raw vector $v$ to $x = \sigma \odot (v - \mu)$, where $\mu_k$ is the mean of dimension $k$ and $\sigma_k = w_{g(k)} / s_k$ is the weight of the feature group of $k$ over the standard deviation of $k$.
The cost of frame $i$ for the query $q$ is $c_i = \sum_{k=1}^{d} (x_{ik} - q_k)^2$.
The brute force answer is the smallest index $i \in P$ with the smallest $c_i$.

## The normalization

**Lemma 1.** The cost is the weighted squared distance $c_i = \sum_k (w_{g(k)} / s_k)^2 (v_{ik} - v_k^{q})^2$ of the raw vectors, where $v^q$ is the raw query.
In particular the mean $\mu$ drops out, and scaling dimension $k$ of all the data and the query by a factor $a \ne 0$ does not change any cost.

*Proof.*
$x_{ik} - q_k = \sigma_k (v_{ik} - \mu_k) - \sigma_k (v^q_k - \mu_k) = \sigma_k (v_{ik} - v^q_k)$.
A scaling by $a$ multiplies $s_k$ and $v_{ik} - v^q_k$ by $|a|$ and $a$, so $\sigma_k (v_{ik} - v^q_k)$ changes only its sign. $\square$

## The scan with early exit

**Lemma 2.** In the loop of line L3, the partial sum $s$ never decreases.
This also holds in floating point arithmetic with rounding to nearest.

*Proof.*
Each step adds $t^2 \ge 0$.
In floating point, $\operatorname{fl}(s + t^2) \ge s$, because $s + t^2 \ge s$ and rounding to nearest is monotone and leaves $s$ unchanged. $\square$

**Theorem 1.** Line L6 returns the brute force answer.

*Proof.*
The invariant of the loop of line L2 is: after the frames $P_1, \dots, P_m$, $\text{best} = \min_{l \le m} c_{P_l}$ and $\text{best\_i}$ is the first $P_l$ with that cost.
It holds before the loop with $\text{best} = \infty$.
Take the next frame $i$.
If the loop of line L3 ends early at line L4, then a partial sum is greater than best, so by Lemma 2 $c_i > \text{best}$, and frame $i$ changes nothing; the code does not change best, because $s > \text{best}$ fails the test of line L5.
Otherwise $s = c_i$, computed in the same order as the brute force cost.
Line L5 replaces best only if $c_i < \text{best}$, so a later frame with an equal cost does not replace an earlier one.
So the invariant holds after frame $i$.
At the end, $m = |P|$, and since $P$ is increasing the first frame with the smallest cost is the smallest index with that cost. $\blacksquare$

## The k-d tree

The tree stores the normalized playable frames.
An inner node splits on a dimension $k$ at a value $t$: the points with $x_k < t$ go left, the others go right.
The search visits the child on the side of $q$ first, and visits the other child only if $(q_k - t)^2 \le \text{best}$.

**Lemma 3.** If $(q_k - t)^2 > \text{best}$, no point of the far child has a cost at most best.

*Proof.*
Every point $x$ of the far child is on the other side of $t$ from $q_k$ in dimension $k$, or on the plane, so $|x_k - q_k| \ge |q_k - t|$.
So its cost is at least $(x_k - q_k)^2 \ge (q_k - t)^2 > \text{best}$. $\square$

**Theorem 2.** The k-d tree search returns the brute force answer.

*Proof.*
The search keeps the same pair (best, best_i) as the scan, but it updates it on a cost that is smaller, or equal with a smaller index.
By Lemma 3, a subtree that the search skips holds no point with a cost at most best at the time of the skip, and best only decreases later, so the skipped points cannot be the answer or tie with it.
Every other point is compared.
So the search ends with the smallest cost and, among equal costs, the smallest index. $\blacksquare$

The test compares the scan and the tree with the brute force search on 251 queries, including a duplicated feature row that makes a tie.
