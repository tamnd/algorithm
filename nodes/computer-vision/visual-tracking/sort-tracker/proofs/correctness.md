---
title: Why the SORT assignment is optimal, why separated objects keep their identities, and why the Joseph form keeps the covariance positive definite
proves: [correctness]
status: full
---

Notation as on the page. In one frame there are $n$ tracks and $m$ detections, and $c_{ij} = \mathrm{IoU}(\hat b_i, d_j) \in [0, 1]$ is the IoU between the predicted box of track $i$ and detection $j$. An assignment is a set of pairs $(i, j)$ in which no track and no detection appears twice. It is *full* if it has $\min(n, m)$ pairs. Line L3 asks for a full assignment of largest total $\sum c_{ij}$, which is the same as a full assignment of smallest total for the cost $-c_{ij}$. The claims are about the algorithm, not about real video.

## Claim 1: the assignment of line L3 is optimal

Let $r \le c$ (else transpose the matrix) and let $a_{ij} = -c_{ij}$ be the $r \times c$ cost matrix. The solver of the implementation is the Hungarian method with potentials $u_1, \ldots, u_r$ and $v_1, \ldots, v_c$. When it stops, it has a full assignment $\sigma$ (every row $i$ has a column $\sigma(i)$) and potentials with

1. $u_i + v_j \le a_{ij}$ for all $i, j$,
2. $u_i + v_{\sigma(i)} = a_{i \sigma(i)}$ for every row $i$,
3. $v_j \le 0$ for every column $j$, and $v_j = 0$ for every column not in $\sigma$.

Then $\sigma$ has the smallest total cost of all full assignments.

*Proof of the three facts.* Facts 1 and 2 are the invariants of the Hungarian method: each change of potentials by $\delta$ adds $\delta$ to $u$ on the rows of the search tree and subtracts $\delta$ from $v$ on its columns, so the reduced costs $a_{ij} - u_i - v_j$ inside the tree do not change and outside it they drop by at most their smallest value, which keeps them nonnegative. An augmenting path only uses pairs with reduced cost 0. For fact 3, $v_j$ only decreases, and only for columns in the search tree. A column joins the tree only when it is matched, because the search stops at the first free column that it reaches, before the next change of potentials. A matched column stays matched. So a column that is free at the end was never in a tree and has $v_j = 0$.

*Proof of optimality.* Let $\tau$ be any full assignment, so each row $i$ has a column $\tau(i)$ and the columns are distinct. By fact 1, $\sum_i a_{i \tau(i)} \ge \sum_i u_i + \sum_i v_{\tau(i)}$. Since every $v_j \le 0$, adding the other columns can only lower the sum, so $\sum_i v_{\tau(i)} \ge \sum_{j=1}^{c} v_j$. By fact 3 the right side equals $\sum_i v_{\sigma(i)}$. By fact 2, $\sum_i u_i + \sum_i v_{\sigma(i)} = \sum_i a_{i \sigma(i)}$. So $\sum_i a_{i \tau(i)} \ge \sum_i a_{i \sigma(i)}$. $\square$

The tests compare the solver with a search over all full assignments on 200 random matrices of size up to $5 \times 5$.

## Claim 2: the kept pairs

After line L4, the kept pairs form an assignment in which every pair has $c_{ij} \ge \mathrm{IoU}_{\min}$. Every track and every detection is either in one kept pair or in none.

*Proof.* The kept pairs are a subset of $\sigma$, and a subset of an assignment is an assignment. The filter keeps a pair only if $c_{ij} \ge \mathrm{IoU}_{\min}$. $\square$

## Claim 3: filtering after the assignment is not the same as gating first

The kept set of line L4 need not be an assignment of largest total among assignments that use only pairs with $c_{ij} \ge \mathrm{IoU}_{\min}$, and it can have fewer pairs.

*Example.* Take two tracks $A, B$, two detections $a, b$, $\mathrm{IoU}_{\min} = 0.3$, and $c_{Aa} = 0.9$, $c_{Ab} = 0.5$, $c_{Ba} = 0.5$, $c_{Bb} = 0.25$. The two full assignments have totals $0.9 + 0.25 = 1.15$ and $0.5 + 0.5 = 1.0$, so line L3 takes $\{(A, a), (B, b)\}$, and line L4 drops $(B, b)$. One pair is kept, with total 0.9. If the pair $(B, b)$ is forbidden before the assignment, the best assignment is $\{(A, b), (B, a)\}$, with two pairs and total 1.0. $\square$

The released code of the paper filters after the assignment, and so does the implementation of this page. The difference is a design choice, not an error, but the two rules give different tracks.

## Claim 4: separated objects keep their identities

Suppose that in one frame, tracks $1, \ldots, q$ and detections $1, \ldots, q$ satisfy $c_{kk} \ge \mathrm{IoU}_{\min} > 0$ for $k \le q$, and every other entry of the IoU matrix is 0 (this includes the rows of other tracks and the columns of other detections). Then every assignment of largest total contains the pairs $(k, k)$ for all $k \le q$, and line L4 keeps them.

*Proof.* Since $q \le \min(n, m)$, the pairs $(1, 1), \ldots, (q, q)$ extend to a full assignment by adding any pairs between the other rows and columns, and its total is $\sum_{k \le q} c_{kk}$, because all the added pairs have IoU 0. So the optimum is at least $\sum_{k \le q} c_{kk}$. In any assignment, the only pairs with a nonzero entry are pairs $(k, k)$, so its total is the sum of $c_{kk}$ over the pairs $(k, k)$ it contains. If it misses some $(k, k)$, its total is at most $\sum_{k \le q} c_{kk} - c_{kk} < \sum_{k \le q} c_{kk}$, because $c_{kk} > 0$. So every optimal assignment contains all of them. Each has $c_{kk} \ge \mathrm{IoU}_{\min}$, so line L4 keeps each one. $\square$

*Corollary.* If the hypothesis holds in every frame, with track $k$ created from the first detection of object $k$, then by induction over the frames track $k$ is updated only with detections of object $k$, and no identity switch occurs. The hypothesis is about the predicted boxes, so it is a condition on the input and on the filter, not a fact that SORT ensures. When two objects overlap, the IoU matrix has nonzero entries off the diagonal, and the claim says nothing.

## Claim 5: the counters

With the code of the page, a track that is not matched in $k$ frames in a row has a count of frames since its last update equal to $k$ after line L7 of the $k$-th of these frames, if it is still there. It is deleted in the first frame where $k > \texttt{max\_age}$. With $\texttt{max\_age} = 1$ it survives one missed frame and is deleted in the second.

*Proof.* Line L1 adds 1 to the count of every track, and line L5 sets it to 0 for each matched track. A track not matched in $k$ frames in a row therefore has count $k$ after line L5 of the $k$-th frame. Line L7 deletes it when the count exceeds $\texttt{max\_age}$, which first happens at $k = \texttt{max\_age} + 1$. $\square$

## Claim 6: the Kalman steps

For the linear model $x_{t+1} = F x_t + w_t$, $z_t = H x_t + e_t$, with Gaussian noise of covariances $Q$ and $R$, independent of each other and of the start, the prediction $\hat x \leftarrow F \hat x$, $P \leftarrow F P F^{\mathsf T} + Q$ and the update with gain $K = P H^{\mathsf T} (H P H^{\mathsf T} + R)^{-1}$ give the mean and covariance of the state given all measurements so far. This is the Kalman filter; the proof is on the page [Kalman filter](/kalman-filter/). Two facts about the implementation remain.

(a) If $P$ is positive definite and $Q$ is positive definite, then $F P F^{\mathsf T} + Q$ is positive definite. Indeed $y^{\mathsf T} F P F^{\mathsf T} y \ge 0$ and $y^{\mathsf T} Q y > 0$ for $y \ne 0$. Here $Q = \mathrm{diag}(1, 1, 1, 1, 0.01, 0.01, 10^{-4})$ is positive definite.

(b) The Joseph form $P' = (I - K H) P (I - K H)^{\mathsf T} + K R K^{\mathsf T}$ is symmetric for every $K$, and positive definite if $P$ and $R$ are. Symmetry holds because both terms have the form $M A M^{\mathsf T}$ with $A$ symmetric. For $y \ne 0$, if $K^{\mathsf T} y \ne 0$ then $y^{\mathsf T} K R K^{\mathsf T} y > 0$. If $K^{\mathsf T} y = 0$, then $(I - K H)^{\mathsf T} y = y - H^{\mathsf T} K^{\mathsf T} y = y$, so the first term gives $y^{\mathsf T} P y > 0$. In both cases $y^{\mathsf T} P' y > 0$, since both terms are positive semidefinite. $\square$

For the optimal gain the Joseph form equals the short form $(I - K H) P$, but in floating point it keeps symmetry and positive definiteness, which the short form can lose. The model of a box as a constant velocity point with constant aspect ratio is a heuristic, so the "mean given the measurements" of Claim 6 is exact only for data that follow the model.
