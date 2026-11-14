---
title: A dictionary lookup returns exactly the faults that the tests cannot tell apart from the true one
proves: [correctness]
status: full
---

We use the notation of the page. The circuit $C$ has $O$ outputs, the tests are $t_0, \ldots, t_{T-1}$, and $G[j]$ is the good output vector on $t_j$. For a fault $f$, $Z_j(f)$ is the output vector of $C$ with $f$ on $t_j$, $R_j(f) = Z_j(f) \oplus G[j]$ is its error word, $R(f) = (R_0(f), \ldots, R_{T-1}(f))$, and $P(f) = \{ j : R_j(f) \ne 0 \}$. Simulation is deterministic, so $R(f)$ and $P(f)$ depend only on $f$.

**Lemma 1 (invariant).** After any sequence of calls to `add_fault`, with $D$ the set of faults added, every $f \in D$ is in exactly one list of `FULL`, the one under the key $R(f)$, and in exactly one list of `PF`, the one under the key $P(f)$, and no list holds a fault outside $D$.

*Proof.* By induction on the number of calls. Before any call both maps are empty and $D$ is empty. Consider a call with a fault $f$. If $f \in D$ already, the call returns at once and nothing changes. Otherwise lines L2 and L3 compute $R_j = Z_j(f) \oplus G[j] = R_j(f)$ for every $j$, line L4 computes $P = \{ j : R_j \ne 0 \} = P(f)$, and lines L5 and L6 append $f$ to the lists under $R(f)$ and under $P(f)$. No other list changes, and $f$ was in no list before, since by the induction hypothesis the lists hold only faults of $D$. So after the call every fault of $D \cup \{f\}$ is in exactly one list of each map, under its own key. $\blacksquare$

**Theorem 1 (full lookup).** Let a chip give the output vectors $z_0, \ldots, z_{T-1}$, and let $r = (z_0 \oplus G[0], \ldots, z_{T-1} \oplus G[T-1])$ as in line L7. Then line L8 returns exactly $\{ g \in D : Z_j(g) = z_j \text{ for all } j \}$. In particular, if the chip behaves like the circuit with a fault $f \in D$, the answer is $\{ g \in D : Z_j(g) = Z_j(f) \text{ for all } j \}$, and it contains $f$.

*Proof.* By Lemma 1, the list under the key $r$ is $\{ g \in D : R(g) = r \}$, which is empty when the key is absent. For each $j$, $R_j(g) = r_j$ means $Z_j(g) \oplus G[j] = z_j \oplus G[j]$, and adding $G[j]$ to both sides gives $Z_j(g) = z_j$. So $R(g) = r$ exactly when $Z_j(g) = z_j$ for every $j$. If the chip behaves like $C$ with $f$, then $z_j = Z_j(f)$, and $g = f$ satisfies the condition. $\blacksquare$

**Theorem 2 (pass-fail lookup).** Line L9 returns exactly $\{ g \in D : P(g) = \{ j : r_j \ne 0 \} \}$, and this set contains the answer of line L8.

*Proof.* The first part follows from Lemma 1 as in Theorem 1. If $R(g) = r$, then $R_j(g) \ne 0$ exactly when $r_j \ne 0$, so $P(g) = \{ j : r_j \ne 0 \}$. So every fault returned by line L8 is also returned by line L9. $\blacksquare$

**Corollary 1 (classes).** Call two faults of $D$ full-equivalent when $R(f) = R(g)$, and pass-fail-equivalent when $P(f) = P(g)$. Full-equivalent faults are pass-fail-equivalent, since $P$ is a function of $R$. So each full class lies inside one pass-fail class, and the number of pass-fail classes is at most the number of full classes. Since $P(f)$ is a subset of $\{0, \ldots, T-1\}$, there are at most $2^T$ pass-fail classes, and since $R(f)$ is a string of $T \cdot O$ bits, there are at most $2^{T \cdot O}$ full classes. $\blacksquare$

**Theorem 3 (sizes).** Stored as a matrix with one row per fault, the full dictionary needs $|D| \cdot T \cdot O$ bits and the pass-fail dictionary needs $|D| \cdot T$ bits. No coding of $R$ alone can use fewer than $\lceil \log_2 K \rceil$ bits per fault for $K$ full classes in the worst case.

*Proof.* A row of the full dictionary is $R(f)$, that is $T$ error words of $O$ bits each, and a row of the pass-fail dictionary is the indicator of $P(f)$, that is $T$ bits. For the lower bound, a code that gives the same string to two faults with different $R$ cannot return different answers for them, so it needs $K$ distinct strings, and fewer than $\lceil \log_2 K \rceil$ bits give fewer than $K$ strings. $\blacksquare$

Theorem 1 says nothing about chips whose defect is not a fault of $D$. For such a chip the lookup may return the empty list, or a list of faults that happen to have the same response.
