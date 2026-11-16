---
title: Random shortcutting keeps the path free, keeps its end points, and never makes it longer
proves: [correctness]
status: full
---

We use the notation of the page. A path is a polyline $P = (x_0, x_1, \dots, x_n)$ in the plane, and it is free if no segment $x_k x_{k+1}$ meets the open interior of an obstacle rectangle. The input path is free. The claims below are invariants of the loop of lines L1 to L6; they say nothing about how close the result is to a shortest path, because the method is a heuristic. The proof is in exact arithmetic.

## The segment test

**Lemma 1.** `segment_free(p, q)` returns false exactly when the segment from $p$ to $q$ meets the open interior of some rectangle $(x_0, x_1) \times (y_0, y_1)$.

*Proof.* Write the segment as $p + t(q - p)$ for $t \in [0, 1]$. For one axis with $d \ne 0$, the coordinate lies in the open interval of the rectangle exactly for $t$ in the open interval between $t_0$ and $t_1$ of the code. For an axis with $d = 0$, it lies there for all $t$ or for no $t$; the code handles the second case by the flag. Let $\ell$ be the maximum of $0$ and the lower ends, and $u$ the minimum of $1$ and the upper ends. If $\ell < u$, every $t$ strictly between them is in $[0, 1]$ and in every open interval, so the segment meets the interior. Conversely, if some $t^*$ in $[0, 1]$ is in every open interval, then $\ell \le t^* \le u$. Equality on both sides would need $\ell = t^* = 0$ (the open lower ends are below $t^*$) and $u = t^* = 1$, which is impossible. So $\ell < u$. $\square$

## The invariants

Consider one pass of the loop. Line L3 picks arc lengths $s_1 \le s_2$, and line L4 finds the points $a$ on segment $i$ and $b$ on segment $j$ of the current path. If $i = j$ nothing changes. Otherwise $i < j$, and line L6 replaces the path by

$$P' = (x_0, \dots, x_i, a, b, x_{j+1}, \dots, x_n).$$

**Lemma 2.** If $P$ is free, so is $P'$.

*Proof.* The segments $x_k x_{k+1}$ with $k < i$ or $k > j$ are segments of $P$. The segment $x_i a$ is part of the segment $x_i x_{i+1}$ of $P$, and the segment $b x_{j+1}$ is part of $x_j x_{j+1}$, so they meet no interior. The segment $ab$ passed the test of line L5, so by Lemma 1 it meets no interior either. $\square$

**Lemma 3.** $P'$ has the same end points as $P$, and its length is at most the length of $P$.

*Proof.* The point $a$ is on segment $i \ge 0$ and $b$ on segment $j \le n - 1$, so $x_0$ and $x_n$ stay at the ends. The part of $P$ between arc lengths $s_1$ and $s_2$ is a polyline from $a$ to $b$ of length $s_2 - s_1$. By the triangle inequality its length is at least $|a - b|$, the length of the new segment, and the rest of the path does not change. $\square$

**Lemma 4.** $P'$ has at most one more vertex than $P$.

*Proof.* The vertices $x_{i+1}, \dots, x_j$, at least one of them because $j > i$, are removed, and the two vertices $a$ and $b$ are added. $\square$

**Theorem 1.** After any number of iterations and for every sequence of random choices, line L7 returns a free path with the same end points as the input, a length that is at most the input length, and at most $n + 1 + N$ vertices after $N$ iterations.

*Proof.* Induction on the iterations with Lemmas 2, 3 and 4. $\square$

## What is not claimed

The length can stay well above the shortest path length forever. Every new segment joins two points of the current path. If the input goes around a wall by its far end, and no free straight segment joins two points of the path past the near end, then the path stays around the far end, however long it runs. Even in free space, detours near the two end points shrink slowly, because a shortcut must start inside them. The page reports measured lengths, not guarantees.
