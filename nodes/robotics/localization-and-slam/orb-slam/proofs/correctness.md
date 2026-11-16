---
title: The parts of the ORB-SLAM toy are exact where they claim to be, the consistency rule needs three keyframes in a row, and only loop edges move the poses
proves: [correctness]
status: full
---

**Setting.** The toy of `impl/python/orb_slam.py` keeps keyframes with planar poses, map points, the covisibility weights $w(K, J)$, bag of words vectors, an inverted index, the groups of the last consistency check, and loop edges. A keyframe goes through lines L1 to L10 of the pseudocode. These claims are about the toy, not about the full ORB-SLAM system.

**Assumptions.** (A1) Exact arithmetic. (A2) Every bag of words vector has nonnegative entries with sum 1, or is empty. `bow_vector` makes them so.

**Claim 1 (the score).** For vectors $u, v$ as in (A2), $s(u, v) = 1 - \tfrac12 \|u - v\|_1 = \sum_w \min(u_w, v_w)$. So $0 \le s \le 1$, $s = 1$ if and only if $u = v$, and only words in both vectors add to the score.

*Proof.* For $a, b \ge 0$, $|a - b| = a + b - 2\min(a, b)$. Summing over all words gives $\|u - v\|_1 = 1 + 1 - 2\sum_w \min(u_w, v_w)$, which is the identity. Each term $\min(u_w, v_w)$ is nonnegative, and it is zero when one of the two entries is zero, so only shared words count. The sum is at most $\sum_w u_w = 1$, with equality if and only if $\min(u_w, v_w) = u_w$ for every $w$, that is $u \le v$ entrywise, and since both sum to 1, $u = v$. $\square$

**Claim 2 (the inverted index).** `InvertedIndex.query(v)` returns $s(v, u_J)$ for every indexed keyframe $J$ that shares a word with $v$, and returns no other keyframe.

*Proof.* The list of word $w$ holds $(J, u_{J,w})$ for every indexed $J$ with $u_{J,w} > 0$. The query adds $\min(v_w, u_{J,w})$ to the score of $J$ for each word $w$ of $v$ and each entry of its list. This adds exactly the nonzero terms of the sum in Claim 1. A keyframe that shares no word appears in no visited list. $\square$

**Claim 3 (the rigid fit).** For pairs $(p_k, q_k)$ that are not all equal in $p$, `fit_rigid` returns a minimizer of $\sum_k \|R(\theta) p_k + t - q_k\|^2$ over $\theta$ and $t$.

*Proof.* For a fixed $\theta$, the best $t$ is $\bar q - R(\theta)\bar p$, with the means $\bar p, \bar q$. With the centered points $p'_k, q'_k$, the cost becomes $\sum_k \|p'_k\|^2 + \|q'_k\|^2 - 2\, q_k'^\top R(\theta) p'_k$. Here $\sum_k q_k'^\top R(\theta) p'_k = \cos\theta\, S_{xx} + \sin\theta\, S_{xy}$ with $S_{xx} = \sum_k p'_k \cdot q'_k$ and $S_{xy} = \sum_k (p'_{k,x} q'_{k,y} - p'_{k,y} q'_{k,x})$. This is largest at $\theta = \mathrm{atan2}(S_{xy}, S_{xx})$, which is what the code returns. $\square$

`robust_rigid` tries every pair of matches as a sample and keeps the largest inlier set, so it finds the largest set of matches that agrees, within the tolerance, with a pose fitted to some pair of its members. It then refits on that set by Claim 3.

**Claim 4 (consistency).** A candidate $J$ is accepted at keyframe $K_t$ only if there are candidates $J_{t-2}, J_{t-1}, J_t = J$ at the keyframes $K_{t-2}, K_{t-1}, K_t$, processed one after the other with no loop closure between them, such that the groups $G(J_{t-2}) \cap G(J_{t-1})$ and $G(J_{t-1}) \cap G(J_t)$ are not empty, where $G(J) = \{J\} \cup$ the covisible neighbors of $J$.

*Proof.* By induction on $c$, a group with the count $c$ at keyframe $K_t$ has a chain of $c$ groups at $K_{t-c+1}, \dots, K_t$ in which consecutive groups overlap. For $c = 1$ the chain is the group itself. A group gets the count $c + 1 > 1$ only from a group with the count $c$ in the list of the previous keyframe that it overlaps, and the list holds only the groups of the previous keyframe, because it is replaced at each keyframe. A loop closure empties the list. With the threshold 3, the claim follows. $\square$

**Claim 5 (the covisibility weights).** After each call of `add_keyframe`, $p$ is a map point of keyframe $K$ if and only if $K \in$ `seen_by[p]`, and for every pair of keyframes that share a map point, $w(K, J) = w(J, K)$ is the number of map points that they share.

*Proof.* A new keyframe adds itself to `seen_by` of exactly its map points. The fusion moves $K$ from `seen_by` of the old point to `seen_by` of the new point in the same step in which it changes the observation. So the first statement holds. `_connect(K)` counts, for every point of $K$, the other keyframes in its `seen_by`, which is the number of shared points with each of them. It removes the old entries of $K$ in the other keyframes and writes the new counts on both sides, so the weights stay symmetric. The only keyframe whose points change is the new keyframe or the fused keyframe, and `_connect` runs on it right after the change. Other pairs are not affected, because their point sets did not change. $\square$

**Claim 6 (only loop edges move the poses).** Every edge of the essential graph that is not a loop edge has, at the moment it is built, the measurement $Z_{ij} = X_i^{-1} X_j$ of the current poses. So with no loop edges, the current poses have cost 0, the error and the gradient are zero, and a Gauss-Newton step does not move them. With loop edges, the optimization starts from a point at which only the loop edges have an error.

*Proof.* `_essential_edges` sets the measurement of each tree edge and of each strong covisibility edge to `between(poses[i], poses[j])`. The error of such an edge is $\mathrm{Log}(Z_{ij}^{-1} X_i^{-1} X_j) = 0$ at the current poses. The gradient $\sum J^\top e$ is a sum of zero vectors, so the step solves $H \delta = 0$, and $\delta = 0$ because $H$ is positive definite once pose 0 is fixed and the graph is connected. Loop edges carry the measurement of the geometric check and can have an error. The edges are built before the fusion, so the new links across the loop, which join drifted poses, are not edges with zero error that would hold the drift in place. $\square$

**What this does not show.** It does not show that a loop that is accepted is correct; the score, the consistency check and the geometric check reduce wrong loops but do not exclude them, and the tests only measure the result on simulated data. It does not show that Gauss-Newton converges to the global minimum of the essential graph cost. It does not cover anything of the full system that the toy leaves out: ORB features, tracking, local bundle adjustment, monocular scale drift and the Sim(3) fit, keyframe culling, or the final full bundle adjustment of ORB-SLAM2.
