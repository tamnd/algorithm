---
title: Incremental SfM terminates, keeps its filter invariant and recovers exact generic data up to a similarity
proves: [correctness]
status: full
---

We use the notation of the page and exact arithmetic, as in the real RAM model. The true cameras are $(R_i^*, t_i^*)$ with $X_c = R_i^* X + t_i^*$, the true points are $X_j^*$, and the observations are $x_{ij} = \pi(R_i^* X_j^* + t_i^*)$ in normalized coordinates, with $\pi(y) = (y_1 / y_3, y_2 / y_3)$ and $y_3 > 0$. The data are in general position in the following sense.

- (G1) The first pair $(a, b)$ of line L1 has at least 8 common tracks, the two centers differ, and for every 8 of these tracks the conditioned eight-point system has a null space of dimension 1. No point lies on the line through the two centers.
- (G2) For every image $c$ and every 6 points that $c$ sees, the DLT resection system has a null space of dimension 1. This excludes, for example, 6 points on one plane (Hartley and Zisserman, Chapter 7).
- (G3) Each point is seen from at least two distinct centers that do not lie on one line with it, so its linear triangulation system has a null space of dimension 1.

**Claim.** (a) The loop of lines L5 to L9 runs at most $N - 2$ times. (b) After each run of line L9, every kept observation has a reprojection error of at most $\tau$, and every kept point has at least two kept observations. (c) Each bundle adjustment returns a cost no larger than its start cost. (d) On exact data that satisfy (G1) to (G3), every camera and every point in the output equals the truth after one fixed similarity: with $s = 1 / \|t_b^* - R_b^* (R_a^*)^{\mathsf T} t_a^*\|$, the output is $R_i = R_i^* (R_a^*)^{\mathsf T}$, $t_i = s (t_i^* - R_i^* (R_a^*)^{\mathsf T} t_a^*)$ and $X_j = s (R_a^* X_j^* + t_a^*)$.

**Proof of (a).** Each run of the loop either stops at line L5 or line L7, or adds a new image $c$ to the set of registered images. There are $N$ images and two are registered before the loop. $\square$

**Proof of (b).** The filter of line L9 first deletes every observation with an error above $\tau$. It then deletes every point with fewer than two observations, together with its observations. The second deletion changes no error, so every observation left has an error of at most $\tau$, and every point left has at least two observations. $\square$

**Proof of (c).** Levenberg-Marquardt in lines L4 and L9 computes a trial step and accepts it only if the new cost is strictly smaller than the current one. Otherwise it raises the damping and tries again, and it returns the current state when the damping passes its limit. So the cost never rises. $\square$

**Proof of (d).** First we check the similarity. Put $X' = s (R_a^* X + t_a^*)$. Then $X = (R_a^*)^{\mathsf T} (X' / s - t_a^*)$ and
$$s (R_i^* X + t_i^*) = R_i^* (R_a^*)^{\mathsf T} X' + s (t_i^* - R_i^* (R_a^*)^{\mathsf T} t_a^*) = R_i X' + t_i.$$
The camera coordinates are multiplied by $s > 0$, so the projections and the signs of the depths do not change. So the transformed scene explains the same data, camera $a$ has $(I, 0)$, and camera $b$ has $\|t_b\| = 1$. We call it the target, and show that the algorithm returns the target, by induction over the steps.

*Line L2.* In the target, the essential matrix $E = [t_b]_\times R_b$ satisfies $x_{bj}^{\mathsf T} E x_{aj} = 0$ for every common track. By (G1), every sample of 8 tracks gives $E$ up to a nonzero scale, after the conditioning is undone. A true essential matrix has two equal nonzero singular values and one zero, so the projection to the singular values $(1, 1, 0)$ keeps it, up to scale. All Sampson errors are 0, so all common tracks are inliers, and the refit on them gives the same matrix. The four candidates of the decomposition are $(U W V^{\mathsf T}, \pm u_3)$ and $(U W^{\mathsf T} V^{\mathsf T}, \pm u_3)$, and one of them is $(R_b, t_b)$, since $\|t_b\| = 1$. For a point that is not on the baseline, exactly one of the four candidates places it in front of both cameras. Both facts are in the section on the essential matrix of Hartley and Zisserman (Section 9.6). In the target, every point is in front of both cameras, so the true candidate counts every point, and each other candidate counts none. So line L2 returns $(R_b, t_b)$.

*Line L3.* With exact poses, the true point is in the null space of the triangulation system of each track, and by (G3) that null space has dimension 1, so the triangulated point is the target point. Its errors are 0, so it is kept.

*Line L4 and line L9.* The cost of the target is 0. A step is accepted only if the cost becomes strictly smaller than 0, which is impossible, so bundle adjustment returns its start unchanged. Then no error exceeds $\tau$, and the filter deletes nothing, because every kept point has at least two observations.

*Lines L6 and L7.* By the induction hypothesis, all registered cameras and all triangulated points equal the target. Let $c$ be the chosen image. It sees at least 6 triangulated points. By (G2), any 6 of them give the DLT matrix $\lambda [R_c \mid t_c]$ for some $\lambda \ne 0$, after the conditioning is undone. The sign fix makes $\det(\lambda R_c) > 0$, so $\lambda > 0$. The singular values of $\lambda R_c$ are all $\lambda$, so the nearest rotation is $R_c$, and division by the mean singular value gives $t_c$. The pose has zero residuals on the sample, so the Gauss-Newton refinement takes a zero step. All seen points then have error 0, so they are all inliers, the first sample already reaches the full count, and the final refit returns the same pose. So line L7 returns $(R_c, t_c)$ and keeps every observation of $c$ of a triangulated point.

*Line L8.* Each new track is now seen by at least two registered cameras with target poses, and the triangulation is exact as for line L3. All errors are 0, so every view is kept.

So each step keeps the induction hypothesis, and at line L10 the output equals the target. $\blacksquare$
