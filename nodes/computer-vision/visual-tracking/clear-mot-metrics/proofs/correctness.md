---
title: The CLEAR MOT matching is a valid one-to-one matching with the most pairs, the counts add up, and MOTA is at most 1 but has no lower bound
proves: [correctness]
status: full
---

Notation as on the page. In frame $t$, $G_t$ is the set of objects, $H_t$ the set of hypotheses, $s(o, h) \in [0, 1]$ the similarity, and a pair is valid when $s(o, h) \ge T$ with $0 < T \le 1$. The procedure CLEAR-MOT keeps old matches in line L2, matches the rest in line L3, and counts in lines L4 and L5.

## Claim 1: each frame gets a one-to-one matching of valid pairs

After line L3, the set $C_t$ of matches of frame $t$ uses each object and each hypothesis at most once, and every pair in it is valid.

*Proof.* The matches of line L2 come from $C_{t-1}$, which is one-to-one by induction ($C_0$ is empty), and line L2 keeps only pairs whose two members are present and valid. Line L3 works on the objects and the hypotheses that line L2 did not use, so its pairs share no member with the kept ones. The Hungarian algorithm returns an assignment, which is one-to-one, and the code drops the pairs that are not valid. $\square$

## Claim 2: line L3 finds the most valid pairs, then the largest total similarity

Let the remaining objects be $1, \ldots, r$ and the remaining hypotheses $1, \ldots, c$, with similarities $s_{ij}$. Let $\beta = \min(r, c) + 1$ and give the pair $(i, j)$ the weight $w_{ij} = \beta + s_{ij}$ if it is valid and 0 if not. A maximum weight assignment, with the pairs of weight 0 then removed, is a matching $M$ of valid pairs whose key $(|M|, \sum_{(i,j) \in M} s_{ij})$ is the largest in lexicographic order.

*Proof.* For a matching $M$ of valid pairs, $w(M) = \beta |M| + S(M)$ with $S(M) = \sum s_{ij}$, and $0 \le S(M) \le |M| \le \min(r, c) < \beta$. Each such $M$ extends to an assignment with the same weight by adding pairs of weight 0, and an assignment loses nothing when its pairs of weight 0 are removed. So the maximum weight assignment, after the removal, is a matching $M^*$ of valid pairs that maximizes $w$.

Let $M$ be another matching of valid pairs. If $|M| < |M^*|$, its key is smaller. If $|M| > |M^*|$, then $w(M) \ge \beta |M| \ge \beta |M^*| + \beta > \beta |M^*| + S(M^*) = w(M^*)$, against the choice of $M^*$; so this case does not happen. If $|M| = |M^*|$, then $w(M) \le w(M^*)$ gives $S(M) \le S(M^*)$. In every case the key of $M$ is at most that of $M^*$. The Hungarian algorithm finds a maximum weight assignment; the proof of its optimality is on the [SORT proof](/sort-tracker/) and the [Hungarian algorithm](/hungarian-algorithm/) page. $\square$

The tests compare the key of the matching with the largest key over all matchings of small random matrices.

## Claim 3: the counts add up

For every frame, $c_t + \mathrm{FN}_t = |G_t|$ and $c_t + \mathrm{FP}_t = |H_t|$, and $\mathrm{IDSW}_t \le c_t$.

*Proof.* By Claim 1, $C_t$ is one-to-one, so it uses exactly $c_t$ objects and $c_t$ hypotheses. Line L5 counts the other objects as misses and the other hypotheses as false positives. Line L4 counts at most one switch for each match. $\square$

Summing over the frames gives $\mathrm{TP} + \mathrm{FN} = \mathrm{GT}$ and $\mathrm{TP} + \mathrm{FP} = \sum_t |H_t|$, with $\mathrm{TP} = \sum_t c_t$.

## Claim 4: the range of MOTA and MOTP

If $\mathrm{GT} > 0$, then $\mathrm{MOTA} \le 1$, with equality exactly when $\mathrm{FN} = \mathrm{FP} = \mathrm{IDSW} = 0$. For every real $m$ there is an input with $\mathrm{MOTA} < m$. If there is a match, $T \le \mathrm{MOTP} \le 1$.

*Proof.* The three counts are nonnegative, so the fraction in MOTA is at least 0, and it is 0 exactly when all three are 0. For the lower bound, take one object in one frame and $k$ hypotheses far from it: $\mathrm{FN} = 1$ and $\mathrm{FP} = k$, so $\mathrm{MOTA} = 1 - (k + 1) = -k$, which is below $m$ for $k > -m$. MOTP is a mean of similarities of valid pairs, each in $[T, 1]$ by Claim 1, so the mean is in $[T, 1]$. $\square$

## Claim 5: what an identity switch counts

Let $\lambda_t(o)$ be the hypothesis that $o$ was matched to in its last match before frame $t$, if any. Then $\mathrm{IDSW}_t$ is the number of matches $(o, h) \in C_t$ with $\lambda_t(o)$ defined and different from $h$. In particular, an object that is missed for some frames and then matched again to the same hypothesis adds no switch, and an object that changes its hypothesis $k$ times over the video adds $k$ switches.

*Proof.* The code keeps a table `last` that it sets to $h$ for every match $(o, h)$ after it tests it, and never changes otherwise. So at the start of frame $t$ the table holds $\lambda_t$, and line L4 counts exactly the stated matches. A change of hypothesis is a match with $h \ne \lambda_t(o)$, which happens $k$ times. $\square$

This shows why MOTA treats identity lightly: a hypothesis that takes the wrong object and keeps it for the rest of the video costs one switch, the same as a short swap.
