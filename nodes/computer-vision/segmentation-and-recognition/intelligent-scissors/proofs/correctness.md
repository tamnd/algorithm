---
title: Correctness of intelligent scissors
proves: [correctness]
status: full
---

This proof covers lines L1 to L13 of the main page. The graph has one node per pixel and a directed link $p \to q$ for each of the 8 neighbors $q$ of $p$. The image has $n = WH$ pixels, so the graph has $n$ nodes and at most $8n$ links. The search finds, for a seed $s$, the least total cost of a path from $s$ to every pixel, and a path that has this cost. Whether that path is the boundary the user wants is a question of the cost function, which the proof does not address.

## The local cost is in [0, 1]

**Lemma 1.** For every link, $0 \le l(p, q) \le 1$.

*Proof.* $f_Z(q) \in \{0, 1\}$ by line L10. By line L11, $f_G(q) = 1 - G(q)/\max G \in [0, 1]$ because $0 \le G(q) \le \max G$, and the scale is $1$ or $1/\sqrt 2$. For line L12, the link vector $L$ is chosen so that $D(p) \cdot L \ge 0$. If $D(p)$ is a unit vector, then $D(p) \cdot L \in [0, 1]$ and its arccosine is in $[0, \pi/2]$. If the gradient at $p$ is zero, the code sets $D(p) = 0$ and the arccosine is $\pi/2$. The second dot product is in $[-1, 1]$, so its arccosine is in $[0, \pi]$. So $f_D \in [0, \frac{2}{3\pi} \cdot \frac{3\pi}{2}] = [0, 1]$. The weights $0.43$, $0.43$ and $0.14$ are nonnegative and sum to $1$, so $l(p, q)$ is a convex combination of numbers in $[0, 1]$ and lies in $[0, 1]$. $\square$

The important part is $l \ge 0$: the search below needs nonnegative link costs.

## The search finds least cost paths

Write $\delta(q)$ for the least cost of a path from $s$ to $q$. Each pixel is reachable from $s$, because the 8-neighbor grid is connected, so $\delta(q)$ is finite.

**Lemma 2 (invariants).** At every point of lines L1 to L9:
1. For each pixel $r$ with a finite $g(r)$, there is a path from $s$ to $r$ of cost $g(r)$ that follows the back pointers, so $g(r) \ge \delta(r)$.
2. For each pixel $r$ that is not expanded, $g(r)$ is the least cost of a path from $s$ to $r$ whose nodes, except $r$, are all expanded.

*Proof.* Line L1 makes both true for $s$, and every other $g$ is infinite. Line L8 sets $g(r) = g(q) + l(q, r)$ and the pointer of $r$ to $q$, which extends the path of $q$ by one link, so part 1 holds. Part 2: when $q$ is expanded at line L4, the paths to a pixel $r$ whose inner nodes are expanded gain those that end with the link $q \to r$; lines L5 to L8 compare their cost $g(q) + l(q, r)$ with the old value and keep the smaller. A path with an inner node that is expanded later is not counted yet. $\square$

**Theorem 1 (Dijkstra).** When line L3 removes $q$ from the active list, $g(q) = \delta(q)$.

*Proof.* Suppose not, and let $q$ be the first pixel removed with $g(q) > \delta(q)$. Take a least cost path from $s$ to $q$, and let $y$ be the first node on it that is not expanded; it exists because $q$ is not expanded yet. All nodes before $y$ are expanded, so by part 2 of Lemma 2 and the choice of $q$, $g(y) \le \delta(y)$. The costs are nonnegative (Lemma 1), so $\delta(y) \le \delta(q)$. So $g(y) \le \delta(y) \le \delta(q) < g(q)$. But $y$ is in the active list with this value, because a finite $g(y)$ was inserted at line L8, and line L3 takes the least $g$, so it would take $y$ before $q$. This is a contradiction. $\square$

The loop ends when the active list is empty. Every pixel is reachable, so every pixel is expanded, and by Theorem 1 and part 1 of Lemma 2, $g(t) = \delta(t)$ for every pixel $t$, and the back pointers from $t$ give a path of that cost. This proves that line L9 returns least cost paths to all pixels at once, so the free point can move to any pixel without a new search. This is the standard proof for [Dijkstra's algorithm](/dijkstra/).

**Removing a worse entry.** The paper removes $r$ from the active list when a lower cost is found, then inserts it again (lines L7 and L8). The code keeps old entries in the heap and skips an entry when it is popped with a value larger than the current $g$. Both forms take the same pixels in the same order of $g$, so the result is the same.

## The bucket queue

**Lemma 3.** If every link cost is an integer in $0, \dots, C$, a circular array of $C + 1$ buckets, indexed by $g \bmod (C + 1)$, gives the same result as the heap.

*Proof.* Let $c$ be the value of the pixel being expanded. Every value in the active list is at least $c$, by Theorem 1 and the order of removal, and at most $c + C$, because each value is $g(q) + l(q, r)$ for an expanded $q$ with $g(q) \le c$. So the values in the list lie in a window of $C + 1$ consecutive integers, and two different values never share a bucket. Scanning the buckets from $c$ upward finds the least value. $\square$

The code rounds the costs to integers for this test. With rounded costs the search is exact for the rounded costs, and the path can differ from the path for the real costs. Mortensen and Barrett use integer costs for this reason.

## What is not proved

The weights $0.43$, $0.43$ and $0.14$ are design choices of the paper, not results. Path cooling and on-the-fly training are heuristics. The theorem says the path is of least cost, not that it is the object boundary: a short path across a weak region can cost less than a long path along a true edge.
