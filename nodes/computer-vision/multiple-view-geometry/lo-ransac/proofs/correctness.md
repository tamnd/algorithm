---
title: LO-RANSAC keeps the model with most inliers it evaluates, never trails RANSAC on the same samples, and runs the local step about ln k times
proves: [correctness]
status: full
---

We use the notation of the page. $I(\theta) = \{x \in D : r(\theta, x) \le \varepsilon\}$, a round is one pass of lines L3 to L13, and "evaluated" means that $I(\cdot)$ of the model was compared with the best so far, either in line L7 or in a "try" of the local step. The minimal solver, the least squares solver and the residual are correct subroutines, and the model of computation is the real RAM.

**Claim.** (a) LOCAL-OPT$(\theta, I(\theta))$ returns a pair $(\theta_L, I(\theta_L))$ with $|I(\theta_L)| \ge |I(\theta)|$. (b) At each test of line L2, $n_s$ is the largest $|I(\theta)|$ over the models of the samples drawn so far, $I^* = I(\theta^*)$, and $|I^*| \ge n_s$. (c) The loop ends after at most $k_{\max}$ rounds. (d) Run RANSAC and LO-RANSAC on the same sequence of minimal samples. After each round, $|I^*|$ of LO-RANSAC is at least $|I^*|$ of RANSAC, and the value of $k$ of LO-RANSAC is at most that of RANSAC. (e) If the consensus sizes of the minimal-sample models of $k$ rounds are independent and identically distributed, the expected number of runs of the local step is at most the harmonic number $H_k = \sum_{j=1}^k 1/j \le 1 + \ln k$.

**Lemma 1.** Part (a) holds.

*Proof.* Line L16 sets best to $(\theta, I(\theta))$. Every later change of best, in line L17, in a try of line L23 and in the last try of line L26, replaces best by a pair $(\theta', I(\theta'))$ only if $|I(\theta')|$ is larger. So the size of the inlier set of best never decreases, and the returned pair is a model with its own inlier set. $\square$

**Lemma 2.** Part (b) holds.

*Proof.* At the start, $n_s = 0$, $I^* = \emptyset$ and no model is drawn. In a round with a model $\theta$, line L8 compares $|I(\theta)|$ with $n_s$ and line L9 raises $n_s$ if it is larger, so $n_s$ stays the largest size among the sample models. When $n_s$ is raised to $|I(\theta)|$, line L10 runs the local step on $\theta$, and by Lemma 1 its result has at least $|I(\theta)| = n_s$ inliers. Lines L11 and L12 then make $|I^*| \ge n_s$, and they store a model together with its own inlier set. When $n_s$ is not raised, neither $n_s$ nor $I^*$ changes. $\square$

**Lemma 3.** Part (c) holds.

*Proof.* $k$ starts at $k_{\max}$ and line L13 sets it only to values at most $k_{\max}$. Each round increases $t$ by 1, so after $k_{\max}$ rounds the test of line L2 fails. $\square$

**Proof of (d).** After a round, the best set of RANSAC has the largest consensus size of the sample models so far, which is $n_s$ of LO-RANSAC on the same samples. By Lemma 2, $|I^*| \ge n_s$ for LO-RANSAC. Both algorithms set $k = \min(k_{\max}, \lceil \log(1 - p) / \log(1 - w^s) \rceil)$ with $w = |I^*|/n$, and this value does not increase in $w$, as shown for RANSAC. A value of $k$ is only set when the best set grows, and $|I^*|$ of LO-RANSAC is at least that of RANSAC at all times, so its current $k$ is at most that of RANSAC. Hence on the same samples LO-RANSAC stops no later than RANSAC, and since its best set is never smaller, any run in which RANSAC finds a set of a given size is also a run in which LO-RANSAC does. $\square$

**Proof of (e).** The local step runs in round $j$ exactly when the size $X_j$ of the sample model is larger than all earlier sizes, a strict record. Let $U_1, \ldots, U_k$ be independent and uniform on $(0, 1)$, independent of the $X_j$, and order the pairs $(X_j, U_j)$ lexicographically. Every strict record of the sequence $X_j$ is a record of the pairs, because $X_j > X_i$ for all $i < j$ implies $(X_j, U_j) > (X_i, U_i)$. The pairs are independent and identically distributed, and ties between them have probability 0, so all $j!$ orders of the first $j$ pairs are equally likely, and the probability that the $j$-th pair is the largest of the first $j$ is $1/j$. By linearity of expectation, the expected number of records of the pairs is $H_k$, and the expected number of strict records of the $X_j$ is at most $H_k$. Finally $H_k \le 1 + \int_1^k dx/x = 1 + \ln k$. $\square$

**Remark (assumptions of (e)).** The sizes are independent and identically distributed when the samples are, and when the number of rounds is fixed in advance. With the adaptive stopping rule, the number of rounds depends on the sizes; the bound then holds for each fixed horizon $k$, and the count of local steps up to round $k$ is at most $H_k$ in expectation. That the local step brings the number of samples close to the formula of the iteration bound is a benchmark result of Chum, Matas and Kittler (2003), not part of this proof.
