---
title: Why the Deep SORT gate has probability 0.95, why the cascade gives priority and matches nothing twice, why it is not a global optimum, and why uncertain tracks have a wider gate
proves: [correctness]
status: full
---

Notation as on the page. In one frame there are tracks $i$ with predicted measurement $y_i \in \mathbb{R}^4$, innovation covariance $S_i$ (positive definite), gallery $G_i$ and count $a_i$ of frames since the last update after line L1, and detections $j$ with measurement $z_j$ and embedding $e_j$. A pair is admissible if $d_1(i, j) \le t_1$ and $d_2(i, j) \le t_2$. The claims are about the algorithm in one frame. The quality of the embeddings is not part of any claim.

## Claim 1: the probability of the gate

Let $\nu = z - y$ be Gaussian with mean 0 and covariance $S$ in $\mathbb{R}^4$. Then $d_1 = \nu^{\mathsf T} S^{-1} \nu$ has the chi-square distribution with 4 degrees of freedom, and

$$\Pr(d_1 \le t) = 1 - e^{-t/2}\left(1 + \frac{t}{2}\right).$$

*Proof.* Let $S = M M^{\mathsf T}$ with $M$ the Cholesky factor, and $w = M^{-1} \nu$. Then $w$ has covariance $M^{-1} S M^{-\mathsf T} = I$, so $w_1, \ldots, w_4$ are independent standard normal numbers, and $d_1 = w^{\mathsf T} w = w_1^2 + w_2^2 + w_3^2 + w_4^2$. That is the chi-square distribution with 4 degrees of freedom, whose density is $f(x) = \tfrac{x}{4} e^{-x/2}$ for $x \ge 0$. The function $g(x) = -e^{-x/2}(1 + x/2)$ has derivative $\tfrac12 e^{-x/2}(1 + x/2) - \tfrac12 e^{-x/2} = \tfrac{x}{4} e^{-x/2}$, so $\int_0^t f = g(t) - g(0) = 1 - e^{-t/2}(1 + t/2)$. $\square$

For $t = 9.4877$, $e^{-4.74385} = 0.0087051$ and $1 + 4.74385 = 5.74385$, so the product is $0.0500$ and the probability is $0.9500$. The claim needs the Gaussian model. The tests draw 4000 measurements from the projected distribution of a filter and find a fraction within 0.015 of 0.95.

## Claim 2: each stage gives a matching, and the frame matches nothing twice

Each call of the minimum cost matching on rows $R$ and columns $C$ returns a set of pairs in $R \times C$ in which no row and no column appears twice, and all pairs are admissible for that stage. Over the whole frame, no track and no detection is matched twice.

*Proof.* The routine solves a full assignment of the matrix on $R \times C$, in which a pair that is not admissible has a cost one above the largest admissible cost. By Claim 1 of the [SORT proof](/sort-tracker/) on the Hungarian algorithm, the result is an assignment of least cost of that matrix, so it is a set of pairs with distinct rows and distinct columns. The routine then drops the pairs that are not admissible, and a subset of an assignment is an assignment.

The rows of the levels are the sets $T_n = \{i \text{ confirmed} : a_i = n\}$, which are disjoint for different $n$. The rows of the IoU stage are the tentative tracks, which are in no $T_n$, and the confirmed tracks that the cascade left unmatched. So no track takes part in two stages in which it is matched. The columns of each stage are the set $U$ of free detections, and every detection matched in a stage is removed from $U$ before the next stage. So no detection is matched twice. $\square$

## Claim 3: priority of fresh tracks

The tracks of level $n$ choose among all detections that the levels $1, \ldots, n - 1$ did not take, and the tracks of the levels above $n$ see only the detections that level $n$ left free. In particular, if $T_n = \{i\}$ has one track and some free detection is admissible for $i$, then $i$ gets its cheapest admissible free detection, whatever the tracks of higher levels would prefer.

*Proof.* The first sentence is the order of the loop of line L2 and the update of $U$ in line L4. For a single row, a full assignment picks one column. Every admissible column has a cost below the cost of every column that is not admissible, so the least cost column is the cheapest admissible one, and it is kept. $\square$

## Claim 4: the cascade is not a global optimum

There is a frame where the cascade keeps fewer admissible pairs than one assignment over all confirmed tracks.

*Example.* Track 1 has $a_1 = 1$ and track 2 has $a_2 = 2$. There are detections $a$ and $b$ with costs $c(1, a) = 0.10$, $c(1, b) = 0.12$, $c(2, a) = 0.05$, all admissible, and $(2, b)$ not admissible. Level 1 is $\{1\}$, and by Claim 3 track 1 takes $a$. Level 2 is $\{2\}$, and the only free detection $b$ is not admissible, so track 2 stays unmatched. Since $a_2 = 2$, track 2 is not a candidate of the IoU stage. One pair is kept. A single assignment over both tracks can use $\{(1, b), (2, a)\}$, which has two admissible pairs and total cost $0.17$, while any assignment that uses $(1, a)$ must give track 2 the detection $b$, which is not admissible. So the single assignment keeps two pairs. $\square$

The tests check this example with the implementation.

## Claim 5: a larger covariance gives a wider gate

Let $S$ and $S'$ be positive definite with $S' - S$ positive semidefinite. Then for every $\nu$, $\nu^{\mathsf T} S'^{-1} \nu \le \nu^{\mathsf T} S^{-1} \nu$. So every measurement inside the gate of $S$ is also inside the gate of $S'$.

*Proof.* Let $S^{1/2}$ be the symmetric positive definite square root of $S$, and $B = S^{-1/2} S' S^{-1/2}$. Then $B - I = S^{-1/2} (S' - S) S^{-1/2}$ is positive semidefinite, so every eigenvalue of the symmetric matrix $B$ is at least 1. The eigenvalues of $B^{-1} = S^{1/2} S'^{-1} S^{1/2}$ are their inverses, at most 1, so $I - B^{-1}$ is positive semidefinite. With $\mu = S^{-1/2} \nu$,

$$\nu^{\mathsf T} S^{-1} \nu - \nu^{\mathsf T} S'^{-1} \nu = \mu^{\mathsf T} \mu - \mu^{\mathsf T} S^{1/2} S'^{-1} S^{1/2} \mu = \mu^{\mathsf T} (I - B^{-1}) \mu \ge 0. \qquad \square$$

Each prediction without an update adds $Q$ and spreads the position by the velocity variance, so the innovation covariance of a track usually grows while it is missing. In the example of the page, the first entry of $S$ grows from 13.3 after one prediction to 195 after ten, and the squared Mahalanobis distance of a fixed offset drops from 15.0 to 1.0. Claim 5 then says that a missing track accepts every detection that a fresh track at the same place would accept, and more. Without the cascade, such a track would win detections because its $d_1$ is small; the cascade of Claim 3 prevents that.

## Claim 6: the filter

The prediction and the update are the Kalman recursion for the linear model of the page, and the implementation uses the Joseph form for the update. By Claim 6 of the [SORT proof](/sort-tracker/), the covariance stays symmetric and positive definite, since the motion noise and the measurement noise are positive definite for every height $h > 0$. This is what makes $S_i^{-1}$ and $d_1$ well defined.
