---
title: The safe tier rule returns the exact top k, and the approximate rule returns true scores
proves: [correctness]
status: full
---

The rank order $\prec$ is score descending, then docid ascending, and $\mathrm{top}_k(S)$ is the first $\min(k, |S|)$ pairs of a set $S$ in this order. The query has $m$ distinct terms, $M$ is the set of matching documents, and $s(x)$ is the score of $x$. The weights are at least 0, the thresholds satisfy $\tau_1 > \cdots > \tau_r > 0$, and weights, thresholds and scores are exact numbers.

**Lemma 1 (tiers).** Each posting is in exactly one tier. A posting with weight $w$ is in a tier $i \le j$ if and only if $w \ge \tau_j$, for each $j \le r$.

*Proof.* The build puts $w$ in the least tier $i$ with $w \ge \tau_i$, or in tier $r + 1$ if there is none. Since the thresholds decrease, $w \ge \tau_j$ holds if and only if that least $i$ is at most $j$. $\square$

**Lemma 2 (the map).** After tier $j$ has been read, $F$ has an entry for $x$ if and only if some query term has a posting of $x$ in tiers $1, \ldots, j$, and then $F[x] = s(x)$.

*Proof.* Lines L3 and L4 add an entry for each new docid met in the tiers read so far, and line L5 computes it by random access to every query term, so the entry is the sum of all the query weights of $x$. $\square$

**Lemma 3 (unseen documents).** After tier $j \le r$, every $y \in M$ with no entry in $F$ has $s(y) < m \tau_j$.

*Proof.* By Lemma 2, no query term has a posting of $y$ in tiers $1, \ldots, j$, so by Lemma 1 each query weight of $y$ is less than $\tau_j$. The document $y$ has at most $m$ such weights and at least one, since it matches, so the sum is less than $m \tau_j$. $\square$

**Theorem 1 (safe rule).** TIERED-SEARCH$(q, k, \mathit{safe})$ returns $\mathrm{top}_k(\{(x, s(x)) : x \in M\})$ in the order $\prec$.

*Proof.* If the loop reads all $r + 1$ tiers, then $F$ holds every posting of the query terms, so by Lemma 2 it maps each $x \in M$ to $s(x)$, and line L8 returns the top $k$. Otherwise line L7 breaks after a tier $j \le r$, with $|F| \ge k$ and the $k$-th best score $s_k$ in $F$ at least $m \tau_j$. Let $E$ be the set of documents in $F$ with their scores, and take $y \in M$ with no entry. By Lemma 3, $s(y) < m \tau_j \le s_k$, so each of the $k$ best documents of $E$ has a score strictly greater than $s(y)$ and ranks before $y$. So no such $y$ is in $\mathrm{top}_k(M)$, and $\mathrm{top}_k(M) = \mathrm{top}_k(E)$, which line L8 returns. $\blacksquare$

**Proposition 2 (approximate rule).** TIERED-SEARCH$(q, k, \mathit{approx})$ returns $\min(k, |M|)$ documents of $M$, each with its true score, in the order $\prec$. It reads no more tiers than the safe rule.

*Proof.* Each entry of $F$ is a document of $M$ with its true score by Lemma 2, and line L8 sorts by $\prec$. If line L6 breaks, $|F| \ge k$ and $k$ entries are returned. If it never breaks, all tiers are read and $F$ holds all of $M$, so $\min(k, |M|)$ entries are returned. The approximate rule breaks after the first tier at which $|F| \ge k$, and the safe rule cannot break before that tier, since it also needs $|F| \ge k$. $\square$

The approximate rule does not return $\mathrm{top}_k(M)$ in general. In the toy example of the page, with $\tau = (1.5, 1.0)$, q1 and $k = 2$, it returns d1 and d7, while the true second document is d2.

**Remark (strictness).** Line L7 may use $s_k \ge m \tau_j$ because Lemma 3 is strict: the weights in later tiers are strictly less than $\tau_j$. If the build put the weights equal to $\tau_j$ into tier $j + 1$, the bound would be $s(y) \le m \tau_j$, and the test would need $s_k > m \tau_j$, or a tie with a smaller docid could be lost.

**Remark (tighter bounds).** A smaller bound in place of $m \tau_j$ is also safe if every unseen document is strictly below it. An example is the sum over the query terms of $\min(\tau_j, U_t)$, where $U_t$ is the largest weight of term $t$, provided that the build and the test use the same numbers.
