---
title: The Coffman-Graham schedule is optimal on two machines
proves: [correctness]
status: full
---

We use the notation of the page with $m = 2$. The graph $G$ is transitively reduced (line L1), so no arc $u \to w$ exists if $u$ also reaches $w$ by a path of two or more arcs. We write $u \prec w$ if $G$ has a path from $u$ to $w$ with at least one arc. The labels are $\alpha$, the schedule is $\sigma$, and $C$ is its makespan. A slot is *full* if it holds two jobs. For a job $u$, $N(u)$ is the set of labels of its immediate successors, compared as a decreasing sequence in lexicographic order.

**Fact 0 (the order on label sets).** For two different finite sets $X, Y$ of integers, $X$ is lexicographically larger than $Y$ if and only if the largest element of the symmetric difference $X \triangle Y$ is in $X$.

*Proof.* Let $c = \max (X \triangle Y)$. The two decreasing sequences agree on all elements above $c$. At the next position, the sequence of the set that holds $c$ has $c$, and the other one has a smaller element or ends. $\square$

**Lemma 1 (labels decrease along paths).** If $u \prec w$ then $\alpha(u) > \alpha(w)$.

*Proof.* Line L3 makes a job ready only when all of its immediate successors have labels, and labels are given in increasing order. So $\alpha(u) > \alpha(w)$ for each arc, and the claim follows along a path. $\square$

**Lemma 2 (larger label, larger sequence).** If $\alpha(u) > \alpha(y)$ then $N(u) \ge N(y)$ in lexicographic order.

*Proof.* Let $k = \alpha(y)$. If $u$ was in $R$ at step $k$, then line L5 chose $y$ over $u$, so $N(y) \le N(u)$; the sets did not change later, because all their labels were already given. Else some immediate successor $w$ of $u$ had no label at step $k$, so $\alpha(w) > k$. All labels in $N(y)$ are below $k$. By Fact 0, $N(u) > N(y)$. $\square$

**Lemma 3 (list scheduling).** Take a slot $k$ and a job $j$ with $\sigma(j) > k$. If slot $k$ has an idle machine, or holds a job with a smaller label than $\alpha(j)$, then $j$ has an immediate predecessor $u$ with $\sigma(u) \ge k$.

*Proof.* Otherwise all predecessors of $j$ are in slots below $k$, so $j$ is in the set $A$ of line L10 at slot $k$. Line L10 then fills the idle machine with $j$, or takes $j$ before the job of smaller label. $\square$

**The blocks.** Let $x_0$ be the job of smaller label in slot $C$, and $k_0 = C$. Given $k_i \ge 1$ and a job $x_i$ in slot $k_i$, write $a_i = \alpha(x_i)$, and let $k_{i+1}$ be the largest $t < k_i$ such that slot $t$ is not full or holds a job of label below $a_i$; let $k_{i+1} = 0$ if there is no such $t$. If $k_{i+1} \ge 1$, let $x_{i+1}$ be the job of larger label in slot $k_{i+1}$. The process stops at the first $r$ with $k_{r+1} = 0$. Let

$$S_i = \{ j : k_{i+1} < \sigma(j) \le k_i,\ \alpha(j) \ge a_i \}.$$

Each slot strictly between $k_{i+1}$ and $k_i$ is full with two jobs of label at least $a_i$. Slot $k_i$ holds $x_i$, and at most one other job. So $|S_i|$ is $2(k_i - k_{i+1})$ or $2(k_i - k_{i+1}) - 1$, and $\lceil |S_i|/2 \rceil = k_i - k_{i+1}$.

**Lemma 4.** For each $i \le r$: (a) every job in a slot after $k_i$ has label below $a_i$, and (b) if $i < r$, then $x_{i+1} \prec j$ for every $j \in S_i$, and every job of $S_i$ that has no predecessor in $S_i$ is an immediate successor of $x_{i+1}$.

*Proof.* We prove (a) for $i$, then (b) for $i$, then (a) for $i + 1$. Part (a) holds for $i = 0$ because no slot comes after $C$.

Assume (a) for $i$, and $i < r$. Write $a = a_i$, $k = k_{i+1} \ge 1$, $y = x_{i+1}$ and $D = S_i$. By (a), $D$ is the set of all jobs in slots after $k$ with label at least $a$.

We show by induction on $\sigma(j)$ that $y \prec j$ for each job $j$ with $\sigma(j) > k$ that is in $D$, or, if slot $k$ is not full, for every job $j$ with $\sigma(j) > k$. Slot $k$ is not full, or it holds a job $x \ne y$ of label below $a$, and then $\alpha(x) < a \le \alpha(j)$ for $j \in D$. In both cases Lemma 3 gives an immediate predecessor $u$ of $j$ with $\sigma(u) \ge k$.

- If $\sigma(u) = k$, then $u = y$, or slot $k$ is full and $u = x$. In the second case $j \in D$, and Lemma 1 would give $\alpha(j) < \alpha(x) < a$, which is false. So $u = y$, and $y \to j$ is an arc.
- If $\sigma(u) > k$, then $\alpha(u) > \alpha(j)$ by Lemma 1, so $u$ is in $D$ when $j$ is, and $u$ is in an earlier slot than $j$. By induction $y \prec u$, so $y \prec j$.

A job $j \in D$ with no predecessor in $D$ is in the first case, because in the second case $u \in D$ (this holds also when slot $k$ is not full, since $\sigma(u) > k$ and $\alpha(u) > \alpha(j) \ge a$). So $j$ is an immediate successor of $y$. This proves (b) for $i$.

For (a) at $i + 1$: a job after slot $k$ is in $D$, or it is in a slot of $(k, k_i]$ with label below $a$, or it is after slot $k_i$ and has label below $a$ by (a) for $i$. Since $x_i \in D$, (b) and Lemma 1 give $\alpha(y) > a$, and also $\alpha(y) > \alpha(j)$ for $j \in D$. So every job after slot $k = k_{i+1}$ has label below $\alpha(y) = a_{i+1}$. $\square$

**Lemma 5 (the chain).** For each $i < r$, every job of $S_{i+1}$ precedes every job of $S_i$: $u \prec w$ for all $u \in S_{i+1}$ and $w \in S_i$.

*Proof.* Use the names $a, k, y, D$ from the proof of Lemma 4, and let $B = S_{i+1}$ and $k' = k_{i+2}$. Let $T$ be the set of jobs of $D$ with no predecessor in $D$. Each job of $D$ is in $T$ or has a predecessor in $T$, because $D$ is finite and $\prec$ has no cycle. So it is enough to show that each $u \in B$ is an immediate predecessor of every $\tau \in T$.

*Step 1: the successors of $y$.* By Lemma 4(b), each $\tau \in T$ is an immediate successor of $y$. Conversely, let $w$ be an immediate successor of $y$ with $\alpha(w) \ge a$. Then $\sigma(w) > k$, so $w \in D$. If $w$ had a predecessor $d \in D$, then $y \prec d \prec w$ by Lemma 4(b), and the arc $y \to w$ would be implied by a longer path, which the transitive reduction excludes. So $w \in T$. Hence the labels in $N(y)$ that are at least $a$ are exactly the labels of $T$.

*Step 2: induction over the slots of $B$, from slot $k$ down to slot $k' + 1$.* We show $u \prec \tau$ for all $u \in B$ and $\tau \in T$. The job $y \in B$ is in slot $k$, and $y \to \tau$ for all $\tau \in T$ by Step 1. Now take $u \in B$ with $u \ne y$, and assume the claim for all jobs of $B$ in later slots than $u$. Then $\alpha(u) \ge \alpha(y)$, and $\alpha(u) \ne \alpha(y)$, so $\alpha(u) > \alpha(y)$.

If $u \prec v$ for some $v \in B$ in a later slot, then $v \prec \tau$ for every $\tau \in T$ by the induction, so $u \prec \tau$.

Else $u$ precedes no job of $B$ in a later slot, and we show that $u \to \tau$ is an arc for every $\tau \in T$. Let $w$ be an immediate successor of $u$ with $\alpha(w) \ge a$. Then $\sigma(w) > \sigma(u) > k'$. If $\sigma(w) \le k$, then $w$ is in slot $k$ or in a full slot strictly between $k'$ and $k$ whose jobs have labels at least $\alpha(y)$. In slot $k$, $w$ is not $y$ (as $u$ precedes no job of $B$ later), and not the job of label below $a$. In a slot between, $w \in B$, which is also excluded. So $\sigma(w) > k$, and $w \in D$. Thus every label in $N(u)$ that is at least $a$ belongs to a job of $D$.

By Lemma 2, $N(u) \ge N(y)$. Suppose that some $\tau \in T$ is not an immediate successor of $u$. Then $N(u) \ne N(y)$, and by Fact 0 the largest element $c$ of $N(u) \triangle N(y)$ is in $N(u)$. If $c \ge a$, then $c = \alpha(w)$ for an immediate successor $w \in D$ of $u$, and $w \notin T$ because all labels of $T$ are in $N(y)$. So some $\tau' \in T$ has $\tau' \prec w$, and $\alpha(\tau') > c$ by Lemma 1. Every label above $c$ is in both sets or in neither, and $\alpha(\tau') \in N(y)$, so $\alpha(\tau') \in N(u)$: the arc $u \to \tau'$ exists. Then $u \to \tau' \prec w$ is a longer path, and the arc $u \to w$ contradicts the transitive reduction. So $c < a$. Then $N(u)$ and $N(y)$ agree on all labels at least $a$, and these are the labels of $T$, so $\tau \in N(u)$, a contradiction. Hence $u \to \tau$ for every $\tau \in T$.

In both cases $u \prec \tau$ for every $\tau \in T$, which completes the induction. $\square$

**Theorem.** For $m = 2$, $C = \mathrm{OPT}$.

*Proof.* Take any feasible schedule $\pi$ on two machines. By Lemma 5, every job of $S_{i+1}$ runs in $\pi$ in an earlier slot than every job of $S_i$. So the sets $S_r, \ldots, S_0$ use pairwise disjoint ranges of slots, in this order. Each slot holds at most two jobs, so $S_i$ uses at least $\lceil |S_i|/2 \rceil$ slots. The makespan of $\pi$ is then at least

$$\sum_{i=0}^{r} \lceil |S_i|/2 \rceil = \sum_{i=0}^{r} (k_i - k_{i+1}) = k_0 - k_{r+1} = C.$$

So $C \le \mathrm{OPT}$, and $C \ge \mathrm{OPT}$ because $\sigma$ is feasible. $\blacksquare$

**Remark.** The transitive reduction is used twice, in Step 1 and in the last part of Step 2. The tie-breaking rule in line L5 is not used: Lemma 2 holds for every choice among equal sequences.
