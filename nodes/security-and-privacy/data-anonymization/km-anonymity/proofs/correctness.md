---
title: The counting test decides km-anonymity exactly
proves: [correctness]
status: full
---

Let $D$ be a finite multiset of transactions, each a finite set of items, and let $k \ge 1$ and $m \ge 0$. The support $s(I)$ of an itemset $I$ is the number of transactions $t \in D$, counted with multiplicity, with $I \subseteq t$. $D$ is $k^m$-anonymous if every non-empty itemset $I$ with $|I| \le m$ has $s(I) = 0$ or $s(I) \ge k$.

**Claim 1 (the counts).** After lines L1 to L4, the map $C$ holds exactly the itemsets $I$ with $1 \le |I| \le m$ and $s(I) \ge 1$, and $C[I] = s(I)$ for each of them.

*Proof.* Line L1 starts with an empty map. Line L3 lists each subset of $t$ of size 1 to $m$ exactly once, because the items of $t$ are distinct, and line L4 adds 1 to its count. So after all transactions, $C[I]$ is the number of transactions $t$ for which $I$ is one of the listed subsets, that is, with $I \subseteq t$ and $1 \le |I| \le m$. This number is $s(I)$. An itemset is a key of $C$ exactly when it was listed at least once, that is, when $s(I) \ge 1$. $\square$

**Claim 2 (the test).** KM-ANONYMOUS returns true if and only if $D$ is $k^m$-anonymous.

*Proof.* If $D$ is not $k^m$-anonymous, some $I$ with $1 \le |I| \le m$ has $1 \le s(I) < k$. By Claim 1, $I$ is a key of $C$ with $C[I] = s(I) < k$, so lines L5 and L6 return false when they reach it, or earlier for another such itemset. If $D$ is $k^m$-anonymous, every key $I$ of $C$ has $C[I] = s(I) \ge 1$, so $s(I) \ge k$, line L6 never returns, and line L7 returns true. $\blacksquare$

**Anti-monotone support.** If $I \subseteq J$, every transaction that contains $J$ contains $I$, so $s(I) \ge s(J)$. Hence $k^m$-anonymity implies $k^{m'}$-anonymity for $m' \le m$: the itemsets of size at most $m'$ are among those of size at most $m$.

**Coarser cuts.** Let $g$ map items to items, applied with set semantics: $g(t) = \{g(x) : x \in t\}$. Suppose $D$ is $k^m$-anonymous and $I'$ is an itemset with $1 \le |I'| \le m$ and $s_{g(D)}(I') \ge 1$. Take a transaction $t$ with $I' \subseteq g(t)$, and for each $y \in I'$ pick one $x_y \in t$ with $g(x_y) = y$. The set $J = \{x_y\}$ has $1 \le |J| \le |I'| \le m$ and $s_D(J) \ge 1$, so $s_D(J) \ge k$. Every transaction $u \supseteq J$ has $g(u) \supseteq I'$, so $s_{g(D)}(I') \ge s_D(J) \ge k$. So $g(D)$ is $k^m$-anonymous.

**Cost.** A transaction with $\tau$ items has $\sum_{j=1}^{m} \binom{\tau}{j}$ subsets of size 1 to $m$, each built and hashed in $O(m)$ time. Lines L5 to L7 read each key once. For a fixed $m$ the total is $O(|D|\, \tau^m)$ map operations.
