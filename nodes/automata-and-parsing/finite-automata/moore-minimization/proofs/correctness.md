---
title: Moore's algorithm outputs the minimal DFA
proves: [correctness, termination]
status: full
---

Let $M = (Q, \Sigma, \delta, q_0, F)$ be a complete DFA, and let $R$ be the set of states reachable from $q_0$. Line L1 computes $R$. For $q \in R$ and $a \in \Sigma$, $\delta(q, a) \in R$, so all the classes in lines L5 and L11 are defined.

**Definitions.** For $i \ge 0$, states $p, q$ are *$i$-equivalent*, $p \sim_i q$, if $\delta^*(p, z) \in F \Leftrightarrow \delta^*(q, z) \in F$ for every $z \in \Sigma^*$ with $|z| \le i$. They are *equivalent*, $p \sim q$, if this holds for every $z$. Each $\sim_i$ and $\sim$ is an equivalence relation, $\sim_{i+1}$ refines $\sim_i$, and $p \sim q$ if and only if $p \sim_i q$ for every $i$.

**Lemma 1 (recursion).** For all $p, q$ and $i \ge 0$: $p \sim_{i+1} q$ if and only if $p \sim_i q$ and $\delta(p, a) \sim_i \delta(q, a)$ for each $a \in \Sigma$.

*Proof.* A word $z$ with $|z| \le i + 1$ is either of length at most $i$, or of the form $a z'$ with $a \in \Sigma$ and $|z'| \le i$; and every word $a z'$ with $|z'| \le i$ has length at most $i + 1$. For the second kind, $\delta^*(p, a z') = \delta^*(\delta(p, a), z')$. So "$p$ and $q$ agree on all $z$ with $|z| \le i + 1$" is the conjunction of "they agree on all $z$ with $|z| \le i$" and "for each $a$, $\delta(p, a)$ and $\delta(q, a)$ agree on all $z'$ with $|z'| \le i$". $\square$

**Lemma 2 (invariant).** Number the passes through lines L5 to L9 as rounds $1, 2, \ldots$, and call the state after lines L2 and L3 round 0. After round $i$, for all $p, q \in R$: $\mathrm{cls}[p] = \mathrm{cls}[q]$ if and only if $p \sim_i q$, and $k$ is the number of classes of $\sim_i$ on $R$.

*Proof.* By induction on $i$. For $i = 0$, $p \sim_0 q$ means that $p$ and $q$ agree on $z = \varepsilon$, that is, $p \in F \Leftrightarrow q \in F$, which is what line L2 records; line L3 counts the classes. For round $i + 1$, line L5 sets $\mathrm{sig}[q] = (\mathrm{cls}[q], \mathrm{cls}[\delta(q, a_1)], \ldots, \mathrm{cls}[\delta(q, a_\sigma)])$ with the classes of round $i$. Line L6 gives two states the same new number if and only if their signatures are equal. By the induction hypothesis, the signatures of $p$ and $q$ are equal if and only if $p \sim_i q$ and $\delta(p, a) \sim_i \delta(q, a)$ for each $a$, which by Lemma 1 holds if and only if $p \sim_{i+1} q$. Line L7 counts the distinct signatures, which is the number of classes of $\sim_{i+1}$, and line L9 stores both. $\square$

**Lemma 3 (termination).** The loop stops after at most $|R|$ rounds. When it stops after round $j$, the partition $\mathrm{cls}$ is the partition of $R$ by $\sim$.

*Proof.* Let $k_i$ be the number of classes of $\sim_i$ on $R$. Since $\sim_{i+1}$ refines $\sim_i$, $k_{i+1} \ge k_i$, and $k_{i+1} = k_i$ holds if and only if the two partitions are equal, because a refinement with the same number of blocks has the same blocks. Line L8 compares $k_{i+1}$ with $k_i$ (Lemma 2). As long as the loop runs, $k$ grows by at least 1 per round; it starts at $k_0 \ge 1$, since $q_0 \in R$, and never exceeds $|R|$. So at most $|R| - 1$ rounds increase $k$, and the round after the last of them stops the loop.

Suppose the loop stops after round $j$, so $\sim_j = \sim_{j-1}$ on $R$. We show $\sim_{i} = \sim_{j-1}$ on $R$ for each $i \ge j - 1$, by induction on $i$. Lemma 1 defines $\sim_{i+1}$ from $\sim_i$ by a rule that does not depend on $i$, and it only looks at states of $R$ when $p, q \in R$. So if $\sim_i = \sim_{i-1}$ on $R$, then $\sim_{i+1} = \sim_i$ on $R$. Hence all $\sim_i$ with $i \ge j - 1$ agree on $R$, and since $p \sim q$ if and only if $p \sim_i q$ for all $i$, the partition after round $j$ is the partition of $R$ by $\sim$. $\square$

**Theorem.** The DFA $M'$ returned by line L11 is a complete DFA with $L(M') = L(M)$, and it has the least number of states among all complete DFAs for $L(M)$.

*Proof.* By Lemma 3, $\mathrm{cls}[p] = \mathrm{cls}[q]$ if and only if $p \sim q$, for $p, q \in R$. The relation $\sim$ is compatible with the transitions: if $p \sim q$, then $\delta(p, a) \sim \delta(q, a)$, because a word $z$ that separated $\delta(p, a)$ from $\delta(q, a)$ would make $az$ separate $p$ from $q$. So $\delta'(\mathrm{cls}[q], a) = \mathrm{cls}[\delta(q, a)]$ does not depend on the choice of $q$ in the class, and $\delta'$ is a complete function on $\{0, \ldots, k - 1\}$. Equivalent states agree on $z = \varepsilon$, so a class lies inside $F$ or inside $Q \setminus F$, and $F'$ contains exactly the classes inside $F$.

By induction on $|w|$, $\delta'^*(\mathrm{cls}[q_0], w) = \mathrm{cls}[\delta^*(q_0, w)]$: the case $w = \varepsilon$ is trivial, and for $w = va$, $\delta'(\mathrm{cls}[\delta^*(q_0, v)], a) = \mathrm{cls}[\delta(\delta^*(q_0, v), a)] = \mathrm{cls}[\delta^*(q_0, va)]$. So $M'$ accepts $w$ if and only if the class of $\delta^*(q_0, w)$ is in $F'$, if and only if $\delta^*(q_0, w) \in F$, if and only if $w \in L(M)$.

Every class contains a reachable state $q = \delta^*(q_0, x)$, and $\mathrm{cls}[q]$ is $\delta'^*(\mathrm{cls}[q_0], x)$, so every state of $M'$ is reachable. Two different classes $\mathrm{cls}[p] \neq \mathrm{cls}[q]$ have $p \not\sim q$, so some $z$ has $\delta^*(p, z) \in F$ and $\delta^*(q, z) \notin F$, or the other way round. By the same induction from $p$ and $q$, $z$ separates the two classes in $M'$. So $M'$ has all its states reachable and no two equivalent states, and by Part 3 of the [uniqueness of the minimal DFA](/minimal-dfa-uniqueness/), it is the minimal DFA for $L(M)$. $\blacksquare$
