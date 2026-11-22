---
title: SISA deletion gives exactly the checkpoints of training from scratch on the remaining records
proves: [correctness]
status: full
---

**Setting.** A partition assigns each record $u$ a shard $k(u) \in \{1..S\}$ and a slice $r(u) \in \{1..R\}$, fixed when the record enters and never changed. For a dataset $D$ write $D_{kr} = \{u \in D : k(u) = k,\ r(u) = r\}$, listed in a fixed order that depends only on the records (in the code, by id), and $P_{kt}(D) = D_{k1} + \cdots + D_{kt}$ for the concatenation of the first $t$ slices. TRAIN is a deterministic function of a start $\theta$ and an ordered list $X$ (with the step count $E$ fixed), and $\theta_0$ is a fixed start.

**Training from scratch.** For a dataset $D$ define, for each shard $k$,

$$T_{k0}(D) = \theta_0, \qquad T_{kt}(D) = \mathrm{TRAIN}\big(T_{k,t-1}(D),\ P_{kt}(D)\big) \quad (t = 1..R).$$

Lines L2 to L5 of SISA-TRAIN set $C_{kt} = T_{kt}(D)$ for all $k$ and $t$: line L3 sets $C_{k0} = \theta_0$, and the loop of line L4 applies the recursion in the order $t = 1, 2, \ldots, R$, each time from the value just computed. The predictor of line L6 is a function of $C_{1R}, \ldots, C_{SR}$ only.

**Claim.** Let $D^{(0)} = D$ and let $D^{(q)}$ be the dataset after $q$ deletions handled by SISA-DELETE. Then after the $q$-th deletion, $C_{kt} = T_{kt}(D^{(q)})$ for all $k \in \{1..S\}$ and $t \in \{0..R\}$.

*Proof.* By induction on $q$. For $q = 0$ it is the statement about SISA-TRAIN above.

Assume the claim for $q - 1$, and let the $q$-th request delete $u$, with $k^* = k(u)$ and $r^* = r(u)$. Line L7 removes $u$ from $D_{k^* r^*}$, so $D^{(q)} = D^{(q-1)} \setminus \{u\}$. Because the partition and the order inside a slice depend only on each record, the slices of $D^{(q)}$ are those of $D^{(q-1)}$ except that $u$ is gone from slice $(k^*, r^*)$, and the order of the other records there is unchanged.

*Shards $k \ne k^*$.* $P_{kt}(D^{(q)}) = P_{kt}(D^{(q-1)})$ for every $t$, so by the recursion $T_{kt}(D^{(q)}) = T_{kt}(D^{(q-1)})$, which equals $C_{kt}$ by the hypothesis. SISA-DELETE does not change these checkpoints.

*Shard $k^*$, slices $t < r^*$.* $P_{k^* t}$ does not contain slice $r^*$, so it is the same for both datasets, and by induction on $t$ from $T_{k^* 0} = \theta_0$, $T_{k^* t}(D^{(q)}) = T_{k^* t}(D^{(q-1)}) = C_{k^* t}$. SISA-DELETE does not change these checkpoints; in particular $C_{k^*, r^* - 1} = T_{k^*, r^* - 1}(D^{(q)})$.

*Shard $k^*$, slices $t \ge r^*$.* Line L8 sets $\theta = C_{k^*, r^* - 1} = T_{k^*, r^* - 1}(D^{(q)})$. The loop of line L9 runs $t = r^*, \ldots, R$ and keeps the invariant that, before the step for $t$, $\theta = T_{k^*, t-1}(D^{(q)})$. The step computes $\mathrm{TRAIN}(\theta, P_{k^* t}(D^{(q)}))$, because the slices it reads are the current ones, after the removal of $u$; by the recursion this is $T_{k^* t}(D^{(q)})$, which it stores in $C_{k^* t}$ and keeps as the new $\theta$.

So every checkpoint equals $T_{kt}(D^{(q)})$ after the deletion, which completes the induction. $\square$

**Consequence.** The predictor after any sequence of deletions is the predictor that SISA-TRAIN computes from scratch on the remaining records with the same partition. If the partition of each record is a fixed function of that record alone, the partition of $D \setminus R$ computed from scratch is the restriction of the partition of $D$, so the result is exactly $A(D \setminus R)$ for $A$ = SISA-TRAIN, which is the exact unlearning of the problem page.

**The deterministic hypothesis is needed.** The proof uses only that TRAIN returns the same value on the same start and the same ordered list. If TRAIN draws random numbers, give each pair $(k, t)$ an independent seed that does not depend on the data; then each $T_{kt}$ is a function of the data and the seeds, the same argument holds for each fixed value of the seeds, and the outputs are equal in distribution. In floating point, "the same value" means the same operations in the same order, which the code ensures by keeping the records of each slice sorted by id and by summing in that order; the tests check equality bit for bit. $\blacksquare$
