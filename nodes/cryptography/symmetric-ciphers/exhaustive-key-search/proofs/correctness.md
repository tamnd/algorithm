---
title: Exhaustive key search returns exactly the consistent keys
proves: [correctness]
status: full
---

Let $E : \{0,1\}^k \times \{0,1\}^n \to \{0,1\}^n$ be a cipher and $P = [(x_1, y_1), \ldots, (x_s, y_s)]$ with $s \ge 1$. We identify keys with the integers $0, \ldots, 2^k - 1$. A key $K'$ is *consistent* if $E(K', x_i) = y_i$ for each $i$. Let $C^\ast$ be the set of consistent keys.

**Lemma (loop invariant).** For $0 \le j \le 2^k$, after the iterations of line L1 for the keys $0, \ldots, j - 1$, the list $C$ holds exactly the consistent keys in $\{0, \ldots, j - 1\}$, in increasing order.

*Proof.* By induction on $j$. For $j = 0$, $C$ is empty and the set $\{0, \ldots, -1\}$ is empty, so the claim holds.

Assume the claim for $j$, and consider the iteration for $K' = j$. There are three cases.

1. $E(j, x_1) \ne y_1$. Then $j$ is not consistent. Line L2 goes to the next iteration, and $C$ does not change.
2. $E(j, x_1) = y_1$ and $E(j, x_i) \ne y_i$ for some $i \ge 2$. Then $j$ is not consistent. The test of line L3 is false, and $C$ does not change.
3. $E(j, x_i) = y_i$ for each $i$. Then $j$ is consistent. Both tests pass, and line L4 appends $j$ to $C$.

In each case, $C$ afterwards holds exactly the consistent keys in $\{0, \ldots, j\}$. In case 3, $j$ is larger than each key already in $C$, so the order stays increasing. $\square$

**Theorem.** KEY-SEARCH$(E, P, k)$ stops after $2^k$ iterations and returns $C^\ast$ in increasing order. If $P$ was made with a key $K$, that is $y_i = E_K(x_i)$ for each $i$, then $K$ is in the output.

*Proof.* The loop of line L1 runs over a finite range of $2^k$ keys and each iteration makes at most $s$ calls of $E$, so the algorithm stops. By the lemma with $j = 2^k$, line L5 returns the consistent keys in $\{0, \ldots, 2^k - 1\}$, which is $C^\ast$. The key $K$ is consistent by the definition of $P$, so $K \in C^\ast$. $\square$

**Cost.** Let $C_1 = \{K' : E(K', x_1) = y_1\}$. Each iteration makes one call at line L2. Only the keys of $C_1$ reach line L3, and each of them makes at most $s - 1$ calls there. So the total number of calls of $E$ is at most $2^k + (s - 1)|C_1|$, and at least $2^k$.

**The early stop.** Let FIRST be the variant that returns the first key that passes lines L2 and L3. If $C^\ast = \{K\}$, then the lemma shows that no key below $K$ passes, so FIRST returns $K$ after exactly $K + 1$ iterations. If $K$ is uniform on $\{0, \ldots, 2^k - 1\}$, then the expected number of iterations is

$$\frac{1}{2^k} \sum_{K=0}^{2^k - 1} (K + 1) = \frac{2^k + 1}{2}. \qquad \blacksquare$$
