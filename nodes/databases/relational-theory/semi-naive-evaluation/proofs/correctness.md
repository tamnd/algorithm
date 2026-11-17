---
title: Semi-naive evaluation computes the least model and fires each true rule instance once
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $P$ is a Datalog program, $D$ a finite set of EDB facts, and $M^*$ the least model of $P$ on $D$, which is the least fixed point of $T_P$. A *rule instance* is a rule together with a map $\theta$ from its variables to constants; it is *true* in a set of facts $I$ when $\theta(B) \in I$ for each body atom $B$. IDB facts do not occur in $D$.

Name the sets of the run. $\Delta_0$ and $M_0 = D \cup \Delta_0$ are the sets of lines L1 and L2. For round $t = 1, 2, \ldots$ of the loop of line L3, $\Delta_{t-1} \ne \emptyset$, the old facts are $M_{t-1} \setminus \Delta_{t-1}$ (line L4), $N_t$ is the set built at lines L5 to L7, $\Delta_t = N_t \setminus M_{t-1}$ (line L8) and $M_t = M_{t-1} \cup \Delta_t$ (line L9).

**Claim.** The loop stops after some round $T$ with $\Delta_T = \emptyset$, and then (a) $M_T = M^*$, and (b) each rule instance that is true in $M^*$ is fired exactly once: in line L1 if its body has no IDB atom, and otherwise in exactly one round and for exactly one position $j$ at line L7.

**Lemma 1 (soundness).** $M_t \subseteq M^*$ for each $t$.

*Proof.* $D \subseteq M^*$. Each fact of $\Delta_0$ is the head of an instance whose body facts are in $D$, and each fact of $N_t$ is the head of an instance whose body facts are in $M_{t-1}$, since the old facts and $\Delta_{t-1}$ are subsets of $M_{t-1}$. $M^*$ is closed under the rules. By induction on $t$, $M_t \subseteq M^*$. $\square$

**Termination.** $\Delta_t$ is disjoint from $M_{t-1}$, so while $\Delta_t \ne \emptyset$, $|M_t| > |M_{t-1}|$. By Lemma 1, $|M_t| \le |M^*|$, which is finite, because there are finitely many constants and no function symbols. So some $\Delta_T$ is empty, and the loop stops after round $T$ with $M_T = M_{T-1}$.

**Stages.** The sets $\Delta_0, \Delta_1, \ldots$ are pairwise disjoint, since each $\Delta_t$ is disjoint from $M_{t-1} \supseteq \Delta_0 \cup \cdots \cup \Delta_{t-1}$. Each IDB fact $f$ of $M_T$ is in exactly one of them; call that index $t$ its *stage* $\sigma(f)$. Then for each $t$: the facts of $M_t$ are $D$ and the IDB facts of stage at most $t$; $\Delta_t$ holds the IDB facts of stage exactly $t$; and the old facts of round $t + 1$, $M_t \setminus \Delta_t$, are $D$ and the IDB facts of stage less than $t$.

**Lemma 2 (each true instance is fired).** Let a rule instance be true in $M_T$. If its body has no IDB atom, line L1 fires it. Otherwise let $s$ be the largest stage of its IDB body facts, and let $j$ be the first IDB position of the body whose fact has stage $s$. Then round $s + 1$ fires it for position $j$.

*Proof.* If the body has no IDB atom, its facts are in $D$, and line L1 evaluates the rule on $D$. Otherwise $s \le T - 1$, because $\Delta_T$ is empty, so round $s + 1$ runs. In that round, line L7 for position $j$ reads the IDB atoms before $j$ in the old facts, which hold all facts of stage less than $s$; this holds for them, because $j$ is the first position with stage $s$. It reads atom $j$ in $\Delta_s$, which holds its fact. It reads the other atoms in $M_s$, which holds $D$ and all facts of stage at most $s$. So all body facts are found, and the instance is fired. $\square$

**Proof of (a).** By Lemma 2 the head of each instance that is true in $M_T$ is in $\Delta_0$ or in some $N_{s+1}$, so it is in $M_T$: a fact of $N_{s+1}$ is in $\Delta_{s+1}$ or already in $M_s$. So $M_T$ contains $D$ and is closed under $T_P$, and therefore $M^* \subseteq M_T$. With Lemma 1, $M_T = M^*$. $\square$

**Proof of (b).** By (a), the instances true in $M^*$ are those true in $M_T$, and Lemma 2 fires each of them at least once. Line L1 fires only instances with no IDB atom, and line L7 only instances with an IDB atom at position $j$, so the two kinds are fired in different places. Suppose round $t$ fires an instance for position $j'$. Then the fact of atom $j'$ is in $\Delta_{t-1}$, so it has stage $t - 1$. The IDB facts before $j'$ are old facts, so their stage is less than $t - 1$, and the IDB facts after $j'$ are in $M_{t-1}$, so their stage is at most $t - 1$. So $t - 1$ is the largest stage $s$ of the body, and $j'$ is the first position with stage $s$. So $t = s + 1$ and $j' = j$ are fixed by the instance, and line L7 fires it once, in one search, which finds each map $\theta$ once. $\square$

The claim follows from the termination argument and from (a) and (b). $\blacksquare$
