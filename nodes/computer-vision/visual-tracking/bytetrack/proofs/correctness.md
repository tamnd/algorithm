---
title: Why each BYTE round is a largest weight matching, why the rounds match nothing twice, why low boxes start no track, and why BYTE only adds matches
proves: [correctness]
status: full
---

Notation as on the page. In one frame, a round works on a set $R$ of tracks, a set $C$ of detections and a bound $\beta \in (0, 1)$. Write $\mathrm{IoU}(i, j)$ for the IoU between the predicted box of track $i$ and the box of detection $j$, and $w_{ij} = \mathrm{IoU}(i, j) - \beta$. A matching is a set of pairs in $R \times C$ in which no track and no detection appears twice. It is *valid* if every pair has $w_{ij} \ge 0$. Its weight is $W(M) = \sum_{(i, j) \in M} w_{ij}$. The claims are about the algorithm in one frame.

## Claim 1: the computation of one round

Let $\sigma$ be a full assignment of least total cost for the cost $-\max(0, w_{ij})$ on $R \times C$, and let $M = \{(i, j) \in \sigma : w_{ij} \ge 0\}$. Then $M$ is a valid matching of largest weight.

*Proof.* $M$ is a subset of an assignment, so it is a matching, and it is valid by its definition. Let $w^+_{ij} = \max(0, w_{ij})$. For any valid matching $M'$, extend it to a full assignment $\tau$ by adding pairs between the rows and columns it does not use; the added pairs have $w^+ \ge 0$, so $\sum_\tau w^+ \ge \sum_{M'} w^+ = W(M')$, since $w^+ = w$ on valid pairs. By the optimality of $\sigma$ (Claim 1 of the [SORT proof](/sort-tracker/) on the Hungarian algorithm), $\sum_\sigma w^+ \ge \sum_\tau w^+ \ge W(M')$. The pairs of $\sigma$ with $w_{ij} < 0$ have $w^+ = 0$, so $\sum_\sigma w^+ = \sum_M w = W(M)$. Hence $W(M) \ge W(M')$. $\square$

The tests compare the result with a search over all valid matchings of up to 4 tracks and 4 detections, for $\beta = 0.2$ and $\beta = 0.5$.

## Claim 2: the cost limit of the released code gives the same matching

Use the cost $c_{ij} = 1 - \mathrm{IoU}(i, j)$ and the limit $\ell = 1 - \beta$, and extend the $|R| \times |C|$ matrix to a square matrix of size $|R| + |C|$ with $|C|$ new rows and $|R|$ new columns. The entries of the new rows in real columns and of real rows in new columns are $\ell / 2$, and the block where new rows meet new columns is 0. A full assignment of this matrix that matches $k$ real pairs $M$ costs

$$\sum_{(i, j) \in M} c_{ij} + \frac{\ell}{2}(|R| - k) + \frac{\ell}{2}(|C| - k) = \frac{\ell}{2}(|R| + |C|) - \sum_{(i, j) \in M} (\ell - c_{ij}),$$

and $\ell - c_{ij} = \mathrm{IoU}(i, j) - \beta = w_{ij}$. So a least cost assignment of the extended matrix gives a matching of largest $\sum_M w_{ij}$. If such a matching has a pair with $w_{ij} < 0$, removing the pair raises the weight, so an optimal matching has only pairs with $w_{ij} \ge 0$, and pairs with $w_{ij} = 0$ do not change the weight. The real pairs of the optimum are therefore a valid matching of largest weight, as in Claim 1.

*Proof of the cost formula.* Every real row is matched either to a real column or to a new column, at cost $c_{ij}$ or $\ell / 2$. The $|R| - k$ real rows not in $M$ pay $\ell / 2$ each. Every real column not in $M$ is taken by a new row, at cost $\ell / 2$, which gives $(|C| - k)\, \ell / 2$. The other new rows and new columns meet in the zero block. $\square$

A solver with a cost limit, as the released code calls through the Jonker-Volgenant solver, can be built by this extension. The two methods can differ only in the choice between matchings of the same weight.

## Claim 3: no track and no detection is matched twice

*Proof.* Each round returns a matching by Claim 1. The rows of the rounds are disjoint: line L3 uses the confirmed tracks, line L4 only the confirmed tracks that line L3 left unmatched, and line L6 only the unconfirmed tracks. The detections of line L3 and line L6 are high, and line L6 uses only the high detections that line L3 left. The detections of line L4 are low, a set disjoint from the high ones by the split of line L1. $\square$

## Claim 4: a low box never starts a track

A detection with score $s \le \tau$ never starts a track. If a frame has no detection with score above $\tau$, no track is created in it.

*Proof.* New tracks are created only in line L7, which iterates over detections left in $D_{\text{high}}$, all with $s > \tau$. A low detection is in $D_{\text{low}}$ or dropped in line L1, and line L5 drops the low detections that line L4 did not match. If $D_{\text{high}}$ is empty, line L7 does nothing. $\square$

With the start threshold $\tau + 0.1$ of the released code, a high box with score in $(\tau, \tau + 0.1)$ also starts no track; it can only extend one.

## Claim 5: BYTE only adds matches

Fix the tracks before line L3 and the detections of the frame. Let $B$ be the same procedure without line L4. Then the pairs of line L3 are the same in BYTE and in $B$, and the set of tracks matched in the frame by BYTE contains the set matched by $B$.

*Proof.* Line L3 depends only on the predicted tracks and on $D_{\text{high}}$, which are the same in both, so (with the same tie rule of the solver) it returns the same pairs. In $B$, line L6 uses the same unconfirmed tracks and the same high detections left by line L3, so it returns the same pairs as in BYTE, since line L4 uses neither unconfirmed tracks nor high detections. BYTE adds the pairs of line L4, which involve tracks that are unmatched in $B$. $\square$

The claim is about one frame. Over many frames the states of the two trackers differ, so the claim does not compare whole runs. The occlusion sequence of the page shows a case where BYTE reports the hidden person in 10 more frames.
