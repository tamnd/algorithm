---
title: Why the cost matrix encodes Reid's formula, why Murty's method lists the assignments in order, why global pruning keeps the best children, and why the batch problem is NP-hard
proves: [correctness]
status: full
---

Notation as on the page. A hypothesis $h$ has $n$ tracks and the log weight $w_h$. The frame has $m$ measurements. The matrix $C$ of $h$ has $m$ rows and $n + 2m$ columns: the tracks, then one new-target column $NT_j$ and one false-alarm column $FT_j$ for each measurement $j$.

## Claim 1: the children of a hypothesis and the cost of an assignment

A child of $h$ gives each measurement exactly one role: a track of $h$ whose gate holds it, a new target, or a false alarm, with no track given two measurements. The children of $h$ correspond one to one with the assignments of finite cost of $C$ (each row to a distinct column), and for the child of the assignment $a$,

$$
w_h + n \ln(1 - p_D) - \operatorname{cost}(a) = w_h + N_{DT} \ln p_D + (n - N_{DT}) \ln(1 - p_D) + N_{FT} \ln \beta_{FT} + N_{NT} \ln \beta_{NT} + \sum_{(i,j)} \ln \mathcal N(z_j; \hat z_i, S_i),
$$

which is the log of Reid's formula.

*Proof.* Given a child, send row $j$ to the column of the track of $z_j$, or to $NT_j$, or to $FT_j$. Two rows never share a track column because a track takes at most one measurement, and they never share an $NT$ or $FT$ column because column $NT_j$ and column $FT_j$ are finite only in row $j$. A track column is used only if the pair is gated, so the cost is finite. Conversely, an assignment of finite cost uses only finite entries, which are exactly the allowed roles, and distinct columns mean that no track gets two measurements. The two maps are inverse to each other.

The cost of $a$ is $\sum_{(i,j)} [-\ln p_D - \ln \mathcal N_{ij} + \ln(1 - p_D)] - N_{NT} \ln \beta_{NT} - N_{FT} \ln \beta_{FT}$, with $N_{DT}$ terms in the sum. So $n \ln(1 - p_D) - \operatorname{cost}(a) = N_{DT} \ln p_D + (n - N_{DT}) \ln(1 - p_D) + \sum \ln \mathcal N_{ij} + N_{NT} \ln \beta_{NT} + N_{FT} \ln \beta_{FT}$. $\square$

In Reid's derivation, the posterior of a child is this factor times the posterior of its parent, divided by a normalizing constant that depends only on the measurements of the frame. So the constant is the same for every child of every hypothesis, and comparing log weights compares posterior probabilities. Line L5 removes the constant by normalizing.

## Claim 2: Murty's method lists the assignments in order of cost

A node of the search is a subproblem: the assignments that use every pair of a set $F$ (forced) and no pair of a set $B$ (forbidden). Let $a$ be the best assignment of the subproblem $(F, B)$ and $r_1 < \ldots < r_k$ the rows not forced by $F$. For $t = 1, \ldots, k$ let part $t$ be the subproblem $(F \cup \{(r_s, a(r_s)) : s < t\},\ B \cup \{(r_t, a(r_t))\})$. Then the assignments of $(F, B)$ other than $a$ are split by the parts: each lies in exactly one part, and each assignment of a part lies in $(F, B)$.

*Proof.* A part only adds constraints, so its assignments lie in $(F, B)$, and $a$ lies in no part because it uses the forbidden pair $(r_t, a(r_t))$ of part $t$. Let $b \ne a$ be an assignment of $(F, B)$. On the forced rows, $b$ and $a$ agree, so they differ on some free row. Let $t$ be the first $t$ with $b(r_t) \ne a(r_t)$. Then $b$ uses the forced pairs of part $t$ and avoids its new forbidden pair, so $b$ is in part $t$. For $s < t$, $b$ uses $(r_s, a(r_s))$, which part $s$ forbids. For $s > t$, part $s$ forces $(r_t, a(r_t))$, which $b$ does not use. So $b$ is in no other part. $\square$

By induction on the number of reported assignments, the subproblems in the priority queue split the set of assignments not yet reported, with no overlap. Each subproblem is stored with its best cost, so the cheapest entry of the queue holds an assignment of least cost among all those not yet reported. So the reported costs are nondecreasing, no assignment is reported twice, and none is skipped. A subproblem with no finite assignment is not pushed, which removes nothing. The constraints are applied by setting entries to $\infty$: a forbidden pair gets $\infty$, and a forced pair $(r, c)$ gets $\infty$ in the rest of row $r$ and of column $c$. The Hungarian algorithm then returns a best assignment of the subproblem or reports that none exists.

## Claim 3: keeping the best children of each parent, then the best overall, is exact

Let every hypothesis produce its $M$ best children by Claim 2, and keep the $M$ best of all of them. Then the kept log weights are the $M$ largest log weights over all children of all hypotheses.

*Proof.* Within one parent, the log weight of a child is $w_h + n_h \ln(1 - p_D)$ minus its cost, so the order by weight is the order by cost. Let $c$ be a child of $h$ among the $M$ best overall. Fewer than $M$ children of all hypotheses have a strictly larger weight, so fewer than $M$ children of $h$ do. So the weight of $c$ is among the $M$ largest weights of the children of $h$, which Murty's method returns (with ties, a child of the same weight is returned instead). So the union of the lists holds $M$ children with the $M$ largest weights overall, and the final cut keeps them. $\square$

With $M = 1$, the single kept child of a single hypothesis is the best assignment of $C$, which is [GNN](/global-nearest-neighbor-association/) with the costs of $C$.

## Claim 4: the best partition of three frames into tracks is NP-hard

Consider the batch problem: given the measurements of 3 frames, a cost for every possible track (a choice of at most one measurement per frame) and a cost for every measurement left out, partition the measurements into tracks and left-out measurements at least total cost. This problem is NP-hard.

*Proof.* Reduce from [three-dimensional matching](/three-dimensional-matching/), which Karp (1972) proved NP-complete. An instance has three sets $X$, $Y$, $Z$ of size $q$ and a set $T \subseteq X \times Y \times Z$, and asks whether $q$ triples of $T$ cover every element exactly once. Make frame 1 hold one measurement per element of $X$, frame 2 one per element of $Y$, and frame 3 one per element of $Z$. A track with one measurement in each frame, $(x, y, z)$, costs 0 if $(x, y, z) \in T$ and 1 otherwise. Every other track, which misses a frame, costs $q + 1$, and so does a left-out measurement.

Any $q$ disjoint full triples cover all measurements at cost at most $q$, so an optimal partition costs at most $q$ and uses no short track and no left-out measurement. So it is a split of the measurements into $q$ full triples, and its cost is the number of triples not in $T$. The optimum is 0 if and only if the instance has a perfect matching. The construction takes polynomial time. $\square$

MHT with pruning does not solve this problem exactly. Its hypothesis of highest weight is the best among the hypotheses it kept. If no hypothesis is ever dropped, MHT is exact for its model, at a cost exponential in the number of frames.
