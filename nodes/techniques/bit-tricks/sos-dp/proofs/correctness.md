---
title: SOS DP computes the sum over all submasks for every mask
proves: [correctness]
status: full
---

Let $n \ge 0$, let $(R, +, 0)$ be a commutative monoid, and let $f[0 \ldots 2^n - 1]$ be the input. For a mask $m$ write $m_j$ for bit $j$ of $m$, and $s \subseteq m$ when $s_j \le m_j$ for every $j$.

**Definition.** For $0 \le i \le n$, let
$$ S_i(m) = \{\, s \subseteq m : s_j = m_j \text{ for all } j \text{ with } i \le j \le n - 1 \,\}. $$
A submask in $S_i(m)$ may differ from $m$ only on bits $0$ to $i - 1$. So $S_0(m) = \{m\}$ and $S_n(m) = \{\, s : s \subseteq m \,\}$.

**Lemma 1.** Let $0 \le i < n$.

(a) If $m_i = 0$, then $S_{i+1}(m) = S_i(m)$.

(b) If $m_i = 1$, then $S_{i+1}(m)$ is the disjoint union of $S_i(m)$ and $S_i(m \oplus 2^i)$.

*Proof.* (a) Let $s \in S_{i+1}(m)$. Then $s \subseteq m$ and $m_i = 0$ give $s_i = 0 = m_i$, so $s$ agrees with $m$ on bits $i$ to $n - 1$ and $s \in S_i(m)$. The other inclusion holds because the condition of $S_i$ is stronger than that of $S_{i+1}$.

(b) Let $m' = m \oplus 2^i$, which is $m$ with bit $i$ cleared. Let $s \in S_{i+1}(m)$. If $s_i = 1$, then $s$ agrees with $m$ on bits $i$ to $n - 1$, so $s \in S_i(m)$. If $s_i = 0$, then $s \subseteq m'$ (bit $i$ of both is 0 and the other bits of $m'$ are those of $m$), and $s$ agrees with $m'$ on bits $i$ to $n - 1$, so $s \in S_i(m')$. Conversely, each member of $S_i(m)$ is in $S_{i+1}(m)$; and each $s \in S_i(m')$ satisfies $s \subseteq m' \subseteq m$ and agrees with $m$ on bits $i + 1$ to $n - 1$, so $s \in S_{i+1}(m)$. Every member of $S_i(m)$ has bit $i$ equal to 1, and every member of $S_i(m')$ has it equal to 0, so the union is disjoint. $\square$

**Theorem.** SOS-DP$(f, n)$ returns $F$ with $F[m] = \sum_{s \subseteq m} f[s]$ for every $0 \le m < 2^n$.

*Proof.* We prove this invariant of the loop of line L2.

> **(I)** Before the pass with index $i$, for $0 \le i \le n$: $F[m] = \sum_{s \in S_i(m)} f[s]$ for every mask $m$.

*Initialization.* Line L1 sets $F[m] = f[m]$, and $S_0(m) = \{m\}$, so (I) holds for $i = 0$.

*Maintenance.* Assume (I) before pass $i$, with $i < n$. Let $F_{\text{old}}$ be the array before the pass. In the pass, line L5 writes only to entries $F[m]$ with $m_i = 1$, and only once to each, in the iteration for that $m$. The entry it reads, $F[m \oplus 2^i]$, has bit $i$ of its index equal to 0, so no iteration of this pass writes it, and it equals $F_{\text{old}}[m \oplus 2^i]$ at the time of the read, in any order of the masks.

- If $m_i = 0$, the pass does not change $F[m]$, and by Lemma 1(a) and (I), $F[m] = \sum_{s \in S_i(m)} f[s] = \sum_{s \in S_{i+1}(m)} f[s]$.
- If $m_i = 1$, line L5 sets $F[m] = F_{\text{old}}[m] + F_{\text{old}}[m \oplus 2^i] = \sum_{s \in S_i(m)} f[s] + \sum_{s \in S_i(m \oplus 2^i)} f[s]$ by (I). By Lemma 1(b), the two index sets are disjoint and their union is $S_{i+1}(m)$; since $+$ is associative and commutative, the sum is $\sum_{s \in S_{i+1}(m)} f[s]$.

So (I) holds before pass $i + 1$.

*Termination.* The loop of line L2 runs for $i = 0, \ldots, n - 1$ and stops. Then (I) holds for $i = n$, and $S_n(m)$ is the set of all submasks of $m$. Line L6 returns $F$. $\blacksquare$

**Cost.** Pass $i$ runs line L4 for all $2^n$ masks and line L5 for the $2^{n-1}$ masks with bit $i$ set. So there are $n 2^n$ tests and exactly $n 2^{n-1}$ additions, and the time is $\Theta(n 2^n)$ when each test and addition costs $O(1)$.

**Supersets and the inverse.** The superset version is the same proof with each mask complemented: the map $m \mapsto \lnot m$ (on $n$ bits) turns submasks into supermasks, the test "bit $i$ is 1" into "bit $i$ is 0", and $m \oplus 2^i$ into $m \mathbin{|} 2^i$. For the Möbius transform over a commutative group, pass $i$ with subtraction is the inverse of pass $i$ with addition (it maps $(a, b)$ to $(a, b - a)$ on each pair $(F[m \oplus 2^i], F[m])$, and the pairs of a pass are disjoint), and the passes for distinct bits commute because each acts on one coordinate of the cube $\{0, 1\}^n$; so running all $n$ subtracting passes inverts SOS-DP.
