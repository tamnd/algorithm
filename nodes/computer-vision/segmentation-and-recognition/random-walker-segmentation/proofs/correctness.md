---
title: Correctness of random walker segmentation
proves: [correctness]
status: full
---

This proof covers lines L1 to L8 of the main page. The graph has the node set $V$ with $n = |V|$, undirected edges with weights $w_{ij} > 0$, and the degrees $d_i = \sum_j w_{ij}$. Line L1 gives $w_{ij} = e^{-\beta d_{ij}} > 0$ for every grid edge, so this holds. The Laplacian of line L2 is $L = D - W$: $L_{ii} = d_i$, $L_{ij} = -w_{ij}$ for an edge and $0$ otherwise. The seeded nodes $M$ are not empty, and each seed $j \in M$ has a label $\ell(j) \in \{1, \dots, K\}$. The free nodes are $U = V \setminus M$. Order the nodes with $M$ first, so that
$$L = \begin{pmatrix} L_M & B \\ B^T & L_U \end{pmatrix}.$$
For a label $s$, the boundary vector $m^s$ on $M$ has $m^s_j = 1$ if $\ell(j) = s$ and $0$ otherwise. The hypothesis is: **each connected component of the graph holds at least one seed**. A grid graph is connected, so one seed is enough there.

## Lemma 1 (the system has one solution)

$L_U$ is symmetric positive definite.

*Proof.* For $y \in \mathbb R^U$, extend it by $0$ on $M$ to a vector $\bar y$. Then
$$y^T L_U y = \bar y^T L \bar y = \sum_{\{i, j\} \in E} w_{ij} (\bar y_i - \bar y_j)^2 \ge 0.$$
The identity $\bar y^T L \bar y = \sum_{\{i,j\}} w_{ij} (\bar y_i - \bar y_j)^2$ follows from $L = D - W$ by expanding the square. If the sum is $0$, then $\bar y$ is constant on each connected component of the graph, because every weight is positive. Each component holds a seed, where $\bar y = 0$, so $\bar y = 0$ and $y = 0$. $\square$

So the system $L_U x_U = -B^T m^s$ of line L5 has exactly one solution $x^s_U$. Write $x^s$ for the full vector with $x^s_M = m^s$.

## Lemma 2 (mean value property)

For each free node $i$, $x^s_i = \frac{1}{d_i} \sum_j w_{ij} x^s_j$.

*Proof.* Row $i$ of $L_U x_U + B^T m^s = 0$ reads $d_i x^s_i - \sum_j w_{ij} x^s_j = 0$, where the sum runs over all neighbors, free or seeded. $\square$

A vector with this property on $U$ is called *harmonic* on $U$.

## Lemma 3 (minimum of the Dirichlet energy)

Among all $x$ with $x_M = m^s$, the vector $x^s$ is the only minimizer of $D[x] = \frac12 x^T L x = \frac12 \sum_{\{i,j\}} w_{ij} (x_i - x_j)^2$.

*Proof.* With $x_M = m^s$ fixed,
$$D[x] = \tfrac12 (m^s)^T L_M m^s + x_U^T B^T m^s + \tfrac12 x_U^T L_U x_U.$$
This is a quadratic function of $x_U$ with the Hessian $L_U$, which is positive definite by Lemma 1. So it is strictly convex, and its only minimizer is the zero of the gradient $L_U x_U + B^T m^s$, which is $x^s_U$. $\square$

## Lemma 4 (maximum principle)

Let $x$ be harmonic on $U$. Then $\min_M x \le x_i \le \max_M x$ for each $i$. In particular $0 \le x^s_i \le 1$.

*Proof.* Let $c = \max_V x$, and suppose $c > \max_M x$. The set $S = \{i : x_i = c\}$ is not empty and lies in $U$. Take $i \in S$. By Lemma 2, $x_i$ is a weighted mean of its neighbors with positive weights, and no neighbor is above $c$, so every neighbor equals $c$ and is in $S$. So $S$ is closed under taking neighbors, and $S$ is a whole connected component of the graph. That component holds a seed, which is in $M$, a contradiction. The bound from below is the same argument for $-x$. $\square$

## Lemma 5 (the random walk)

Take the walk that moves from node $i$ to a neighbor $j$ with probability $w_{ij} / d_i$ and stops at the first seed it reaches. For a free start node $i$, let $h_i$ be the probability that the walk stops at a seed of label $s$, and let $h_j = m^s_j$ on $M$. Then $h = x^s$.

*Proof.* First, the walk stops with probability 1. From each free node there is a path to a seed with at most $n$ steps, by the hypothesis. Each step of that path has probability at least $p = \min_{i,j} w_{ij} / d_i > 0$. So in each block of $n$ steps the walk stops with probability at least $p^n$, and the probability that it never stops is at most $\lim_k (1 - p^n)^k = 0$.

Next, condition on the first step. From a free node $i$ the walk goes to $j$ with probability $w_{ij} / d_i$ and then behaves as a walk from $j$, so $h_i = \sum_j (w_{ij} / d_i) h_j$. This is the property of Lemma 2, with the same values on $M$. The difference $h - x^s$ is harmonic on $U$ and $0$ on $M$, so it is $0$ by Lemma 4. $\square$

## Theorem 1 (the sum rule of line L6)

$\sum_{s=1}^K x^s = \mathbf 1$. So the vector $x^K = \mathbf 1 - \sum_{s < K} x^s$ of line L6 equals the solution of the system for label $K$.

*Proof.* The rows of $L$ sum to $0$, so $L \mathbf 1 = 0$, and its rows in $U$ give $L_U \mathbf 1_U + B^T \mathbf 1_M = 0$. Each seed has exactly one label, so $\sum_s m^s = \mathbf 1_M$. The systems are linear with the same matrix, so $\sum_s x^s_U$ solves $L_U y = -B^T \mathbf 1_M$. By Lemma 1 that solution is unique, and it is $\mathbf 1_U$. So $\sum_s x^s = \mathbf 1$, and $x^K = \mathbf 1 - \sum_{s<K} x^s$. $\square$

## Theorem 2 (the output)

Lines L1 to L8 return, for each pixel $i$ and each label $s$, the probability $x^s_i$ of Lemma 5 that a walker from $i$ first reaches a seed of label $s$, and the label of largest probability.

*Proof.* Lines L1 to L4 build $L$, the partition and the vectors $m^s$. Line L5 solves the systems for $s < K$, which have one solution each by Lemma 1. Line L6 gives $x^K$ by Theorem 1. Line L7 takes the argmax. The values are the walk probabilities by Lemma 5 and lie in $[0, 1]$ by Lemma 4. $\square$

## Proposition 1 (connected segments, two labels)

Let $K = 2$, and give node $i$ the label $s$ only if $x^s_i > x^f_i$ for the other label $f$. Then each node with label $s$ is joined to a seed of label $s$ by a path of nodes with label $s$.

*Proof.* With $K = 2$, $x^f = \mathbf 1 - x^s$, so node $i$ has label $s$ exactly when $x^s_i > 1/2$. Let $P$ be a connected component of the set $\{i : x^s_i > 1/2\}$, and suppose that $P$ has no seed. Seeds of the other label have $x^s = 0$, so $P \subseteq U$. Let $c = \max_P x^s$ and $S = \{i \in P : x^s_i = c\}$. Take $i \in S$. Each neighbor $j$ of $i$ either is in $P$, with $x^s_j \le c$, or has $x^s_j \le 1/2 < c$. By Lemma 2, $x^s_i$ is a weighted mean of its neighbors with positive weights, so every neighbor has $x^s_j = c > 1/2$, is in $P$, and is in $S$. So $S$ is a whole connected component of the graph, and it holds a seed. That seed is in $P$, a contradiction. $\square$

This is Proposition 1 of Grady (2006) in the case $K = 2$.

## Remark: more than two labels

For $K \ge 3$ the statement is false. Take seven nodes: node 0 joins nodes 1 and 2 with weight 1; node 1 joins a seed of label 0 with weight 1 and a seed of label 1 with weight 1.2; node 2 joins another seed of label 0 with weight 1 and a seed of label 2 with weight 1.2. By symmetry $x^0_0 = x^0_1 = x^0_2 = p$, and the equation at node 1 gives $p (1 + 1.2 + 1) = p + 1$, so $p = 1/2.2 \approx 0.4545$. Then $x^1_0 = x^2_0 = (1 - p)/2 \approx 0.2727$, so node 0 has label 0. At node 1, $x^1_1 = (0.2727 + 1.2)/3.2 \approx 0.4602 > p$, so node 1 has label 1, and node 2 has label 2 in the same way. Node 0 has label 0, but none of its neighbors does. The test file checks this graph, and a $2 \times 5$ image with the same pattern.

The proof in the paper shows, for each other label $f$ separately, that some neighbor of the component has $x^s > x^f$. For $K = 2$ that is enough. For $K \ge 3$ the neighbor can differ from one $f$ to the next, and it can have a third label, as in the example.

## What is not proved

Nothing here says that the segments match the objects the user has in mind. That depends on the weights, on $\beta$ and on the seeds. Lemma 1 needs exact arithmetic. In floating point a large $\beta$ gives weights near $0$, and then $L_U$ is close to singular. The test file uses moderate values of $\beta$ for this reason.
