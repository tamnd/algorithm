---
title: Delta mush is a linear smoothing with orthonormal frames, gives the rest mesh in the bind pose, and commutes with a common rigid motion
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact, every vertex has at least one neighbor, and the weights of each vertex sum to 1.
Write the positions of a mesh as the rows of an $n \times 3$ matrix $X$, the adjacency matrix as $A$, and the diagonal matrix of the degrees as $D$.

## The smoothing

**Lemma 1.** One step of line L8 is $X \mapsto P X$ with $P = I - \lambda L$ and $L = I - D^{-1} A$, so SMOOTH is $X \mapsto P^K X$.
Each row of $P$, and so each row of $P^K$, sums to 1.

*Proof.*
Row $i$ of $D^{-1} A X$ is the mean of the neighbors of $i$, so row $i$ of $X + \lambda (D^{-1} A X - X)$ is the update of line L8; all rows use the old $X$, as in the code.
The rows of $D^{-1} A$ sum to 1, so the rows of $L$ sum to 0 and those of $P$ sum to 1.
If the rows of $P$ and $Q$ sum to 1, then $P Q \mathbf 1 = P \mathbf 1 = \mathbf 1$, so by induction the rows of $P^K$ sum to 1. $\square$

**Lemma 2.** For an affine map $G(x) = R x + c$, applied to each vertex, $\mathrm{SMOOTH}(G X) = G\, \mathrm{SMOOTH}(X)$.

*Proof.*
Let $p_{ik}$ be the entries of $P^K$.
Vertex $i$ of the smoothed $G X$ is $\sum_k p_{ik} (R x_k + c) = R \sum_k p_{ik} x_k + c \sum_k p_{ik} = R\, \tilde x_i + c$, by Lemma 1. $\square$

## The frames

**Lemma 3.** If the normal sum $s_i$ at vertex $i$ is not zero and the edge $e$ to the first neighbor is not parallel to it, line L9 returns a right-handed orthonormal frame $(t, b, n)$.

*Proof.*
$n = s_i / \lvert s_i \rvert$ is a unit vector.
$e - (e \cdot n) n$ is not zero, because $e$ is not parallel to $n$, and its dot product with $n$ is $e \cdot n - (e \cdot n) = 0$; so $t$ is a unit vector orthogonal to $n$.
$b = n \times t$ is orthogonal to $n$ and $t$, and $\lvert b \rvert = \lvert n \rvert \lvert t \rvert \sin 90° = 1$.
Finally $t \times b = t \times (n \times t) = n (t \cdot t) - t (t \cdot n) = n$, so the frame is right-handed. $\square$

So the matrix $F_i = [t\; b\; n]$ is a rotation, and $F_i^{\mathsf T} F_i = F_i F_i^{\mathsf T} = I$.

**Lemma 4.** For a rigid motion $G(x) = R x + c$ with $R$ a rotation, the frame of vertex $i$ of $G X$ is $R F_i$, where $F_i$ is the frame of $X$.

*Proof.*
Each difference of two vertices turns to $R$ times the old difference, and $R a \times R b = R (a \times b)$ for a rotation.
So each face cross product, and their sum $s_i$, turns to $R$ times the old one, and since $\lvert R s_i \rvert = \lvert s_i \rvert$, the normal turns to $R n$.
The edge turns to $R e$, and $R e - (R e \cdot R n) R n = R (e - (e \cdot n) n)$, so the tangent turns to $R t$.
Then $R n \times R t = R (n \times t) = R b$. $\square$

## Bind pose and rigid motions

**Lemma 5.** If the skinned mesh of line L3 is the rest mesh, $U = V$, the output is $V$.
In particular this holds in the bind pose, where every $C_j = I$ and $u_i = \sum_j w_{ij} v_i = v_i$.

*Proof.*
$\tilde U = \tilde V$, so $G_i = F_i$ for every $i$, and line L6 gives $\tilde v_i + F_i F_i^{\mathsf T} (v_i - \tilde v_i) = v_i$ by Lemma 3. $\square$

**Lemma 6.** If every $C_j$ is the same rigid motion $G(x) = R x + c$, the output is $G v_i$ for every vertex.

*Proof.*
Line L3 gives $u_i = \sum_j w_{ij} G v_i = G v_i$, because the weights sum to 1.
By Lemma 2, $\tilde u_i = R \tilde v_i + c$, and by Lemma 4, $G_i = R F_i$.
So line L6 gives $R \tilde v_i + c + R F_i F_i^{\mathsf T} (v_i - \tilde v_i) = R v_i + c$. $\square$

## What is not proved

The lemmas say nothing about how close the output is to a good deformation in a general pose.
The smoothing of a bent or twisted mesh does not shrink it in the same way as the rest mesh, so the deltas restore the rest shape only in part; the tables of the page are measurements.
