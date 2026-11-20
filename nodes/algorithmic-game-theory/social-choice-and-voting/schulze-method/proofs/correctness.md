---
title: Correctness and properties of the Schulze method
proves: [correctness]
status: full
---

Let $A = \{0, \ldots, m - 1\}$, let $P$ be a profile of $n$ full rankings, and let $g(x, y) = n_P(x, y) - n_P(y, x)$ be the margins. The weighted majority graph has a link $x \to y$ of strength $g(x, y)$ when $g(x, y) > 0$. All link strengths are positive. The strength of a walk is the smallest strength of its links, and $p(x, y)$ is the largest strength of a path from $x$ to $y$, or 0 if there is none. Write $x \succ_S y$ when $p(x, y) > p(y, x)$.

**Claim 1 (walks).** If there is a walk from $x$ to $y \ne x$ of strength $s$, then $p(x, y) \ge s$. So $p(x, z) \ge \min(p(x, y), p(y, z))$ for distinct $x, y, z$.

*Proof.* If the walk visits a candidate twice, remove the part between the two visits. The result is a shorter walk from $x$ to $y$ whose links are a subset of the old links, so its strength is at least $s$. Repeat until no candidate repeats; the result is a path. For the second part, if $p(x, y) = 0$ or $p(y, z) = 0$, the bound holds because $p(x, z) \ge 0$. Otherwise join a strongest path from $x$ to $y$ and one from $y$ to $z$ into a walk of strength $\min(p(x, y), p(y, z))$.

**Claim 2 (invariant).** For $k = 0, \ldots, m$, let $p_k(i, j)$ be the largest strength of a path from $i$ to $j$ whose inner candidates are all less than $k$, or 0 if there is none. After $k$ rounds of the loop of lines L3 to L5, $p[i][j] = p_k(i, j)$ for all $i \ne j$. In particular, at the end $p[i][j] = p(i, j)$.

*Proof.* For $k = 0$, a path without inner candidates is a single link, and line L2 sets $p[i][j]$ to its strength, or to 0. Assume the claim after $k$ rounds, and take round $k$ (the candidate $k$ is the inner candidate that becomes allowed). Lines L4 and L5 never change an entry in row $k$ or in column $k$, so during the round $p[i][k] = p_k(i, k)$ and $p[k][j] = p_k(k, j)$. A path from $i$ to $j$ with inner candidates less than $k + 1$ either does not pass through $k$, and then its strength is at most $p_k(i, j)$, or it is a path from $i$ to $k$ followed by a path from $k$ to $j$, both with inner candidates less than $k$, and then its strength is at most $\min(p_k(i, k), p_k(k, j))$. Conversely, joining a path from $i$ to $k$ and a path from $k$ to $j$ gives a walk from $i$ to $j$; by the argument of Claim 1, it contains a path from $i$ to $j$ with at least the same strength, and its inner candidates are still less than $k + 1$. So $p_{k+1}(i, j) = \max(p_k(i, j), \min(p_k(i, k), p_k(k, j)))$, which is what line L5 computes. When $p[i][k] = 0$ the minimum is 0 and no update is needed, so line L4 may skip row $i$.

**Claim 3 (transitivity).** If $a \succ_S b$ and $b \succ_S c$ for distinct $a, b, c$, then $a \succ_S c$.

*Proof.* Suppose $p(c, a) \ge p(a, c)$. By Claim 1, $p(a, c) \ge \min(p(a, b), p(b, c))$.

If $p(a, b) \le p(b, c)$, then $p(c, a) \ge p(a, c) \ge p(a, b)$, and Claim 1 gives $p(b, a) \ge \min(p(b, c), p(c, a)) \ge p(a, b)$. This contradicts $a \succ_S b$.

If $p(b, c) < p(a, b)$, then $p(c, a) \ge p(a, c) \ge p(b, c)$, and Claim 1 gives $p(c, b) \ge \min(p(c, a), p(a, b)) \ge p(b, c)$. This contradicts $b \succ_S c$.

So $p(a, c) > p(c, a)$.

**Claim 4 (correctness).** The set $W$ of line L6 is the set of Schulze winners, and it is not empty. The ranking of the code lists every candidate once, and no candidate in it is beaten by a candidate below it.

*Proof.* By Claim 2, line L6 tests $p(a, b) \ge p(b, a)$ for all $b \ne a$, which is the definition. The relation $\succ_S$ is asymmetric and, by Claim 3, transitive, so it has no cycle. In a finite set with an acyclic relation, some element is beaten by no other; so $W \ne \emptyset$. The same holds for the restriction of $\succ_S$ to any nonempty set of candidates, so the ranking loop always finds a candidate to take. When it takes $r_i$, every later $r_j$ is still left, so $r_j$ does not beat $r_i$.

**Claim 5 (Smith consistency).** Let $S$ be the Smith set, the smallest nonempty set of candidates each of whom has a positive margin over every candidate outside it. Then $x \succ_S y$ for every $x \in S$ and $y \notin S$. So $W \subseteq S$, and a Condorcet winner is the only winner.

*Proof.* For $x \in S$ and $y \notin S$, $g(x, y) > 0$, so there is no link from $y$ to $x$. A path from outside $S$ to a member of $S$ has a first link that enters $S$, and no such link exists. So $p(y, x) = 0 < g(x, y) \le p(x, y)$. A Condorcet winner $c$ has $S = \{c\}$.

**Claim 6 (Pareto).** If $n \ge 1$ and every voter ranks $a$ above $b$, then $a \succ_S b$, so $b \notin W$.

*Proof.* No margin exceeds $n$, so no strength does. The link $a \to b$ has strength $n$, so $p(a, b) = n$. If $p(b, a) = n$, a path $b = u_0 \to u_1 \to \cdots \to u_k = a$ has $g(u_{i-1}, u_i) = n$ for every link, so every voter ranks $u_{i-1}$ above $u_i$, and by transitivity of each ballot every voter ranks $b$ above $a$. This contradicts $n \ge 1$. So $p(b, a) < n = p(a, b)$.

**Claim 7 (anonymity and neutrality).** Reordering the voters does not change $W$. For a permutation $\pi$ of $A$, the winner set of $\pi P$ is $\pi W$.

*Proof.* The algorithm reads $P$ only through $g$, which does not depend on the order of the voters. In $\pi P$, $g'(\pi x, \pi y) = g(x, y)$, so the graph of $\pi P$ is the image of the graph of $P$, $p'(\pi x, \pi y) = p(x, y)$, and line L6 selects $\pi W$. The resolute rule of line L7 is not neutral: for the ballots $(0, 1)$ and $(1, 0)$, $W = \{0, 1\}$ for the profile and for its image under the swap of 0 and 1, and line L7 returns 0 in both cases.

**Claim 8 (monotonicity).** Let $w \in W(P)$, and let $Q$ be $P$ with $w$ moved up one place on one ballot, passing the candidate $x$. Then $w \in W(Q)$.

*Proof.* Only the pair $\{w, x\}$ changes: $g_Q(w, x) = g(w, x) + 2$ and $g_Q(x, w) = g(x, w) - 2$. Write $p_Q$ for the strengths in $Q$. A path that starts at $w$ never enters $w$ again, so it does not use the link $x \to w$. A strongest path from $w$ to any $b$ in $P$ is a path in $Q$ too, with the same or a stronger link $w \to x$, so $p_Q(w, b) \ge p(w, b)$. A path that ends at $w$ never leaves $w$ before, so it does not use the link $w \to x$. A strongest path from any $b$ to $w$ in $Q$ is a path in $P$ too, since a link $x \to w$ in $Q$ has $g(x, w) = g_Q(x, w) + 2 > 0$, and each of its links is at least as strong in $P$; so $p(b, w) \ge p_Q(b, w)$. Then $p_Q(w, b) \ge p(w, b) \ge p(b, w) \ge p_Q(b, w)$ for every $b \ne w$.

**Claim 9 (winning votes).** With full rankings, the link strengths $n_P(x, y)$ for $g(x, y) > 0$ give the same relation $\succ_S$.

*Proof.* $n_P(x, y) = (n + g(x, y))/2$, an increasing function $f$ of the margin, and $f$ commutes with $\min$ and $\max$. So every path strength, and every $p(x, y)$ that is not 0, is mapped by $f$, and $f$ is larger than 0 on positive margins. Comparisons between two values of $p$ are therefore the same under both strengths.

**Claim 10 (time).** SCHULZE runs in $O(n m^2 + m^3)$ time and $O(m^2)$ extra space.

*Proof.* Line L1 visits the $m(m - 1)/2$ pairs of each ballot once, in $O(n m^2)$ time. Line L2 and line L6 take $O(m^2)$ time. Lines L3 to L5 do $O(1)$ work for each of at most $m^3$ triples. The matrices $g$ and $p$ have $m^2$ entries. $\blacksquare$
