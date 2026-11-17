---
title: Correctness of Boykov-Jolly interactive graph cuts
proves: [correctness]
status: full
---

This proof covers lines L1 to L13 of the main page. The image has the pixel set $P$ with $n = |P|$, a neighbor system $\mathcal N$ of unordered pairs, the object seeds $O$ and the background seeds $G$, with $O \cap G = \emptyset$. A labeling $A$ gives each pixel the label 1 (object) or 0 (background). The energy is
$$E(A) = \lambda \sum_{p} R_p(A_p) + \sum_{\{p, q\} \in \mathcal N} B_{pq}\, [A_p \ne A_q],$$
and $A$ is *feasible* if $A_p = 1$ for $p \in O$ and $A_p = 0$ for $p \in G$. The hypotheses are $\lambda \ge 0$, $R_p(\cdot) \ge 0$ and $B_{pq} \ge 0$. Line L1 gives $R_p = -\ln \Pr \ge 0$, and line L2 gives $B_{pq} > 0$. If some $R_p$ is negative, add the same constant to $R_p(0)$ and $R_p(1)$; this changes $E$ by a constant and does not change the minimizers. Nothing here says that the minimum energy labeling is the object the user wants. That depends on the model and the seeds.

## The network

The network has the nodes $P \cup \{S, T\}$. Each pair $\{p, q\} \in \mathcal N$ gives two arcs $p \to q$ and $q \to p$ with capacity $B_{pq}$. Each pixel has the arcs $S \to p$ and $p \to T$ with the capacities of lines L5 to L7:

| pixel | $c(S, p)$ | $c(p, T)$ |
|---|---|---|
| $p \in O$ | $K$ | $0$ |
| $p \in G$ | $0$ | $K$ |
| other | $\lambda R_p(0)$ | $\lambda R_p(1)$ |

with $K = 1 + \max_p \sum_{q : \{p, q\} \in \mathcal N} B_{pq}$ (line L3). An S-T cut is a set $X$ of nodes with $S \in X$ and $T \notin X$. Its cost $c(X)$ is the sum of the capacities of the arcs that leave $X$. Write $A^X$ for the labeling with $A^X_p = 1$ if and only if $p \in X$.

**Lemma 1 (cost of a cut).** For every cut $X$,
$$c(X) = \sum_{p \notin O \cup G} \lambda R_p(A^X_p) + \sum_{p \in O} K\,[A^X_p = 0] + \sum_{p \in G} K\,[A^X_p = 1] + \sum_{\{p, q\} \in \mathcal N} B_{pq}\, [A^X_p \ne A^X_q].$$

*Proof.* Count the arcs that leave $X$. For a pixel $p \in X$, the arc $p \to T$ leaves $X$ and the arc $S \to p$ does not. For $p \notin X$, the arc $S \to p$ leaves $X$ and $p \to T$ does not. So each pixel adds exactly one of its two terminal capacities. For a free pixel this is $\lambda R_p(1)$ if $A^X_p = 1$ and $\lambda R_p(0)$ if $A^X_p = 0$. For $p \in O$ it is $0$ if $p \in X$ and $K$ if not; for $p \in G$ it is $K$ if $p \in X$ and $0$ if not. For a pair $\{p, q\}$, one of the two arcs leaves $X$ exactly when one end is in $X$ and the other is not, and then it adds $B_{pq}$. $\square$

**Lemma 2 (a minimum cut is feasible).** If $X$ is a minimum cut, then $A^X$ is feasible.

*Proof.* Suppose $p \in O$ and $p \notin X$. Let $X' = X \cup \{p\}$. By Lemma 1 the term $K$ of $p$ goes away, the terminal term of $p$ becomes $0$, and only the pairs that contain $p$ change. They add at most $\sum_q B_{pq} \le K - 1$. So $c(X') \le c(X) - K + K - 1 < c(X)$, and $X$ is not minimum. The case $p \in G$, $p \in X$ is the same with $X' = X \setminus \{p\}$. $\square$

**Theorem 1 (Boykov and Jolly 2001, Theorem 1).** Let $X$ be a minimum cut. Then $A^X$ minimizes $E$ over the feasible labelings, and
$$c(X) = E(A^X) - \lambda \sum_{p \in O} R_p(1) - \lambda \sum_{p \in G} R_p(0).$$

*Proof.* For a feasible labeling $A$, take $X = \{S\} \cup \{p : A_p = 1\}$. The $K$ terms of Lemma 1 are zero, so $c(X) = E(A) - C_0$ with the constant $C_0 = \lambda \sum_{p \in O} R_p(1) + \lambda \sum_{p \in G} R_p(0)$, the region terms of the seeds that the network does not hold. This map from feasible labelings to cuts is one to one. By Lemma 2 a minimum cut is one of these cuts, so it is a minimum of $E(A) - C_0$ over the feasible $A$. $\square$

## The max flow

**Lemma 3 (lines L8 and L9 find a minimum cut).** Line L8 stops with a maximum flow $f$. The set $X$ of nodes reachable from $S$ in the residual graph of $f$ is a minimum cut, and its cost is the value of $f$.

*Proof.* The code augments along a shortest path in the residual graph (Edmonds-Karp). The Edmonds-Karp analysis bounds the number of augmentations by $O(|V||E|)$ for any start flow and any real capacities, because it uses only the residual graph: the BFS distance from $S$ to each node never decreases, and each augmentation saturates an arc that then cannot be on a shortest path again until the distance of one of its ends grows. When no augmenting path is left, $T \notin X$. Every arc that leaves $X$ is saturated, and every arc that enters $X$ carries no flow, otherwise its tail would be reachable. So the value of $f$ equals $c(X)$. Every flow is at most the cost of every cut, so $f$ is maximum and $X$ is minimum. This is the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). $\square$

Lemmas 2 and 3 and Theorem 1 give the correctness of lines L1 to L10: the labeling of line L9 satisfies the seeds and has the least energy among the labelings that satisfy them.

## Adding a seed

Lines L11 to L13 make a free pixel $p$ an object seed after a flow $f$ was found. The histograms do not change. Let $c_p = \lambda (R_p(1) + R_p(0)) \ge 0$. Line L12 sets the capacities of $p$ to $c'(S, p) = K + c_p$ and $c'(p, T) = c_p$. The background case is the mirror image, with $c'(S, p) = c_p$ and $c'(p, T) = K + c_p$.

**Lemma 4 (the old flow stays feasible).** The new capacities are at least the old ones, so $f$ is a feasible flow in the new network.

*Proof.* $c'(S, p) - \lambda R_p(0) = K + \lambda R_p(1) \ge 0$ and $c'(p, T) - \lambda R_p(1) = \lambda R_p(0) \ge 0$. All other capacities are the same. A flow that satisfies the capacity bounds and the conservation law still does both when bounds grow. In the residual graph, the residual capacity of each changed arc grows by the same amount as its capacity, which is what line L12 adds. $\square$

**Lemma 5 (the shift does not change the minimum cut).** Let $N_1$ be the network of lines L4 to L7 for the seeds $O \cup \{p\}$ and $G$, and let $N_2$ be the network after line L12. For every cut $X$, $c_{N_2}(X) = c_{N_1}(X) + c_p$.

*Proof.* In $N_1$ the terminal capacities of $p$ are $K$ and $0$; in $N_2$ they are $K + c_p$ and $c_p$. By the proof of Lemma 1, every cut contains exactly one of the two terminal arcs of $p$, so every cut cost grows by $c_p$. Nothing else differs. $\square$

By Lemma 4, line L13 continues Edmonds-Karp from a feasible flow, and Lemma 3 holds for any start flow. So it stops with a maximum flow of $N_2$ and a minimum cut $X$ of $N_2$. By Lemma 5, $X$ is also a minimum cut of $N_1$, so by Theorem 1 the new labels are a minimum of $E$ under the new seeds. The code keeps the sum of the shifts $c_p$ in `offset`, and the flow minus the offset is the minimum cut of $N_1$. The test file checks it against a new computation from zero flow.

## What is not proved

The histograms of line L1 and the boundary term of line L2 are modeling choices of Boykov and Jolly; they call the boundary term ad hoc. The add-one smoothing of the histograms is a choice of this code. If the histograms are computed again after a new seed, every terminal capacity can change, some can decrease, and Lemma 4 no longer holds; the code does not do this. The [GrabCut](/grabcut/) page covers a method that refits the color models.
