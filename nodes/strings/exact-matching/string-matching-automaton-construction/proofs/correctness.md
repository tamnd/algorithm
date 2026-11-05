---
title: The lagging-state construction computes the transition function
proves: [correctness, termination]
status: full
---

**Claim.** For a pattern $P[0 \ldots m-1]$ over $\{0, \ldots, \sigma-1\}$, COMPUTE-TRANSITION-FUNCTION stops and returns $\delta$ with $\delta[q][c] = \sigma_P(P[0 \ldots q-1]\,c)$ for all $0 \le q \le m$ and all $c$.

Here $\sigma_P(w)$ is the length of the longest prefix of $P$ that is a suffix of $w$. We use the recursion proved on the page of the [string-matching automaton](/string-matching-automaton/): if $r = \sigma_P(w)$, then $\sigma_P(wc) = \sigma_P(P[0 \ldots r-1]\,c)$.

**Termination.** All loops are bounded: $m$ iterations of line L4 with $\sigma$ iterations of line L5 each.

**Row 0.** $\sigma_P(c)$ is 1 if $c = P[0]$ and 0 otherwise, which is what lines L1 and L2 set. For $m = 0$, $\sigma_P$ is always 0 and line L1 sets row 0 to zeros.

**Invariant.** At the start of the iteration for $q$ ($1 \le q \le m$):

> **(I)** rows $0, \ldots, q-1$ are correct, and $X = \sigma_P(P[1 \ldots q-1])$.

For $q = 1$, row 0 is correct and $X = 0 = \sigma_P$ of the empty string.

**Lemma 1.** $X < q$, so row $X$ is correct by (I).

*Proof.* $X \le |P[1 \ldots q-1]| = q - 1$. $\square$

**Lemma 2.** Let $1 \le q \le m$ and let $c$ be a character, with $c \ne P[q]$ if $q < m$. Then $\sigma_P(P[0 \ldots q-1]\,c) = \sigma_P(P[1 \ldots q-1]\,c)$.

*Proof.* Write $w = P[0 \ldots q-1]\,c$ and $w' = P[1 \ldots q-1]\,c$, the string $w$ without its first character. Let $r = \sigma_P(w) \le \min(m, q + 1)$. If $r = q + 1$, then $q < m$ and $P[0 \ldots q] = w$, so $P[q] = c$, which is excluded. So $r \le q = |w'|$, and a suffix of $w$ of length at most $|w'|$ is a suffix of $w'$. Hence $\sigma_P(w) \le \sigma_P(w')$. The other inequality holds because every suffix of $w'$ is a suffix of $w$. $\square$

**Step.** For each $c$ handled by lines L5 and L6 and not overwritten by line L8, Lemma 2, the recursion with $r = X$ and Lemma 1 give

$$\delta[q][c] = \delta[X][c] = \sigma_P(P[0 \ldots X-1]\,c) = \sigma_P(P[1 \ldots q-1]\,c) = \sigma_P(P[0 \ldots q-1]\,c).$$

If $q < m$, line L8 sets $\delta[q][P[q]] = q + 1$, which is correct because $P[0 \ldots q]$ is a suffix of itself and no prefix of $P$ is longer than $q + 1$ characters while ending $P[0 \ldots q]$. Line L9 sets $X$ to $\delta[X][P[q]] = \sigma_P(P[0 \ldots X-1]\,P[q])$, which by the recursion equals $\sigma_P(P[1 \ldots q])$. Row $X$ read here was already correct before the iteration and is not changed by it, since $X < q$. So (I) holds for $q + 1$. At the end, (I) for $q = m + 1$ is the claim. $\blacksquare$
