---
title: CARP routes each URL to the highest score, and its load factor multipliers give each member exactly its load factor
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $K \ge 1$ members. Member $k$ has the member hash $M_k$, the load factor $P_k > 0$ with $\sum_k P_k = 1$, and the multiplier $X_k$. The members are numbered so that $P_1 \le P_2 \le \cdots \le P_K$, which is the order in which the draft computes the multipliers. Write $P_0 = 0$ and $X_0 = 0$.

**Lemma 1 (the route is the highest score).** CARP-ROUTE returns a member $k$ whose score $s_k = c_k \cdot X_k$ is the largest, where $c_k$ is the combined hash of the URL and member $k$. Among equal largest scores, it returns the first one in the member list.

*Proof.* Lines L1 to L3 compute the URL hash $u$. The loop of line L5 keeps this invariant: after members $1, \ldots, j$, $best$ is the first member among them with the largest score, and $bestScore$ is that score. Before the loop $bestScore = -1$, which is below every score, because $c_k \ge 0$ and $X_k > 0$. In the step for member $j + 1$, lines L6 to L8 compute $c_{j+1}$ from $u$ and $M_{j+1}$, line L9 computes $s_{j+1}$, and line L10 replaces $best$ only if $s_{j+1}$ is strictly larger. So the invariant holds after the step, and line L11 returns the claimed member. $\square$

The result depends only on the URL, the member names and the load factors, so all clients and all proxies that read the same membership table route a URL to the same member.

**Lemma 2 (the multipliers are well defined, positive and nondecreasing).** The recurrence

$$X_1 = (K P_1)^{1/K}, \qquad X_k = \left( \frac{(K - k + 1)(P_k - P_{k-1})}{X_1 X_2 \cdots X_{k-1}} + X_{k-1}^{\,K-k+1} \right)^{1/(K-k+1)} \quad (2 \le k \le K)$$

gives $0 < X_1 \le X_2 \le \cdots \le X_K$.

*Proof.* $X_1 > 0$ because $P_1 > 0$. Assume that $X_1, \ldots, X_{k-1}$ are positive. The fraction is at least 0, because $P_k \ge P_{k-1}$, so the bracket is at least $X_{k-1}^{K-k+1} > 0$. Its positive root $X_k$ is then at least $X_{k-1}$. $\square$

**Lemma 3 (the product is 1).** $X_1 X_2 \cdots X_K = 1$.

*Proof.* Let $\Pi_k = X_1 \cdots X_k$ and $\Pi_0 = 1$, and let $G_k = X_k^{K-k} \Pi_k$ for $1 \le k \le K$, and $G_0 = 0$. Multiply the recurrence, raised to the power $K - k + 1$, by $\Pi_{k-1}$:

$$X_k^{K-k+1} \Pi_{k-1} - X_{k-1}^{K-k+1} \Pi_{k-1} = (K - k + 1)(P_k - P_{k-1}).$$

The first term is $X_k^{K-k} \Pi_k = G_k$. For $k \ge 2$ the second term is $X_{k-1}^{K-k+1} \Pi_{k-1} = G_{k-1}$, and for $k = 1$ it is $X_0^K \Pi_0 = 0 = G_0$, which also covers the formula for $X_1$. So $G_k - G_{k-1} = (K - k + 1)(P_k - P_{k-1})$ for $1 \le k \le K$. Sum over $k$:

$$G_K = \sum_{k=1}^{K} (K - k + 1)(P_k - P_{k-1}) = \sum_{k=1}^{K} (K - k + 1) P_k - \sum_{k=1}^{K-1} (K - k) P_k = \sum_{k=1}^{K} P_k = 1.$$

And $G_K = X_K^0 \Pi_K = \Pi_K$. $\square$

**Theorem (exact shares).** Assume that, for a random URL, the combined hashes $c_1, \ldots, c_K$ are independent and uniform on $(0, 1)$. Then the URL goes to member $k$ with probability exactly $P_k$.

*Proof.* Let $S = \max_i X_i c_i$ be the largest score. Ties have probability 0, because the scores have continuous laws. For $t > 0$,

$$\Pr[S \le t] = \prod_{i=1}^{K} \Pr\left[c_i \le \frac{t}{X_i}\right] = \prod_{i=1}^{K} \min\left(1, \frac{t}{X_i}\right).$$

Take $t$ in the interval $I_j = (X_{j-1}, X_j]$ for some $j$ with $1 \le j \le K$. By Lemma 2, $t > X_i$ for $i < j$ and $t \le X_i$ for $i \ge j$, so

$$\Pr[S \le t] = \frac{t^{K-j+1}}{\prod_{i \ge j} X_i} = t^{K-j+1}\, \Pi_{j-1},$$

where the second form uses Lemma 3. On $I_j$ a member $i < j$ cannot have the score $t$, because its score is at most $X_i < t$. For a member $i \ge j$, the event "member $i$ wins with score in $[t, t + dt]$" has probability $\frac{dt}{X_i} \prod_{l \ne i} \min(1, t / X_l) = dt \cdot t^{K-j}\, \Pi_{j-1}$, and this does not depend on $i$. So, given that $S$ falls in $I_j$, each of the $K - j + 1$ members $j, \ldots, K$ wins with the same probability. The probability that $S$ falls in $I_j$ is

$$q_j = \Pr[S \le X_j] - \Pr[S \le X_{j-1}] = \left(X_j^{K-j+1} - X_{j-1}^{K-j+1}\right) \Pi_{j-1} = G_j - G_{j-1} = (K - j + 1)(P_j - P_{j-1}),$$

with the notation of Lemma 3. The intervals $I_1, \ldots, I_K$ cover $(0, X_K]$, which holds $S$. (If some $X_{j-1} = X_j$, the interval $I_j$ is empty and $q_j = 0$, in agreement with $P_j = P_{j-1}$.) Member $k$ can win only when $S$ falls in $I_j$ with $j \le k$, so

$$\Pr[\text{member } k \text{ wins}] = \sum_{j=1}^{k} \frac{q_j}{K - j + 1} = \sum_{j=1}^{k} (P_j - P_{j-1}) = P_k. \qquad \square$$

**Corollary 1 (equal load factors).** If every $P_k = 1/K$, then every $X_k = 1$, and CARP is [rendezvous hashing](/rendezvous-hashing/) with the score $c_k$.

*Proof.* $X_1 = (K / K)^{1/K} = 1$. If $X_1 = \cdots = X_{k-1} = 1$, the fraction in the recurrence is 0, so $X_k = X_{k-1} = 1$. $\square$

**Corollary 2 (removal with equal load factors).** With equal load factors before and after, the removal of a member $r$ moves only the URLs of $r$, and each goes to the member with its second highest score. This is Section 3.5 of the draft, which routes around a failed member to the second highest score.

*Proof.* By Corollary 1 all multipliers are 1 before and after the removal, so the scores of the other members do not change. A URL whose highest scoring member is not $r$ keeps it, because a subset that contains the largest element has the same largest element. A URL of $r$ goes to the largest of the remaining scores, which is its second highest. $\square$

**Remark (removal with unequal load factors).** The load factors of the remaining members must again sum to 1, so they change, and with them all the multipliers. A URL can then move between two members that both stay. The page gives a run where 1,540 of 40,000 URLs do so. The theorem still holds for the new factors: the shares are right, but the [monotonicity property](/monotonicity-property/) of plain rendezvous hashing is lost.

**What the theorem does not cover.** The real combined hashes are 32-bit integers from a fixed function, not independent uniform numbers. The theorem gives the share in the limit of an ideal hash. The draft's hash mixes poorly, so the real shares can be far from $P_k$ for some sets of names; the page shows an example.
