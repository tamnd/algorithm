---
title: Dynamic perfect hashing keeps its invariants and answers searches correctly
proves: [correctness, termination]
status: full
---

Keys are in $U = \{0, \ldots, p - 1\}$ with $p$ prime. The structure starts with REHASH-ALL$(\emptyset)$. We say that an operation is **effective** when it changes $S$: an insert of a key not in $S$, or a delete of a key in $S$. Only effective operations reach line L2 or L11.

**Invariants.** After each operation:

- **(D1)** $S$ is the disjoint union of $S_0, \ldots, S_{M-1}$, and $S_j = \{x \in S : h(x) = j\}$.
- **(D2)** $T_j$ has $2L_j^2$ slots, $h_j$ maps into them and is one-to-one on $S_j$, and the slots of $T_j$ that are not NIL hold exactly the keys of $S_j$, each $x$ in slot $h_j(x)$.
- **(D3)** $|S_j| \le c_j \le L_j$.
- **(D4)** $\sum_j 2L_j^2 \le 512M$.
- **(D5)** $u \le \lceil M/2 \rceil$.

**Fact (U).** For each $m \ge 1$ and distinct $x, y \in U$, $\Pr[h_{a,b,m}(x) = h_{a,b,m}(y)] \le 1/m$. For $m < p$ this is the universality of the Carter and Wegman family. For $m \ge p$, the reduction mod $m$ does nothing, and $(ax + b) \bmod p \ne (ay + b) \bmod p$ because $a \ne 0$ and $p$ is prime, so the probability is 0.

**Lemma 1 (REBUILD-BUCKET).** If $|S_j| \le L_j$ when REBUILD-BUCKET$(j)$ starts, it ends with probability 1, and afterwards (D2) holds for bucket $j$ and $c_j = |S_j| \le L_j$.

*Proof.* A random $h_j$ into $s = 2L_j^2$ slots has, by (U) and linearity of expectation, an expected number of colliding pairs in $S_j$ of at most $\binom{|S_j|}{2}/s \le \binom{L_j}{2}/(2L_j^2) < 1/4$. By Markov's inequality, a trial fails with probability less than $1/4$, and the trials are independent, so the loop of lines L17 and L18 ends with probability 1. Line L16 leaves $T_j$ with $2L_j^2$ slots, all NIL: a new array is NIL everywhere, and an old one has, by (D2) before the rebuild, no key outside the slots $h_j(y)$ of the old keys $y$, which line L16 clears (the new key of line L4, if any, was never stored). Line L19 then stores each key of $S_j$ in its own slot, since $h_j$ is one-to-one on $S_j$, and sets $c_j = |S_j|$. $\square$

**Lemma 2 (REHASH-ALL).** REHASH-ALL$(S')$ ends with probability 1 and establishes (D1) to (D5) for $S = S'$.

*Proof.* Let $n_0 = |S'|$ and $M = \max(n_0, 1)$. If $n_0 = 0$, then $M = 1$ and the sum of line L22 is $8 \le 64$. If $n_0 \ge 1$, then $M = n_0$, and with $n_j = |S_j|$, $\sum_j n_j^2 = n_0 + 2C$, where $C$ is the number of colliding pairs, so by (U), $E[\sum_j n_j^2] \le n_0 + 2\binom{n_0}{2}/M = 2n_0 - 1$. Since $\max(t, 1)^2 \le t^2 + 1$, $E[\sum_j 8\max(n_j, 1)^2] \le 8(2n_0 - 1 + M) < 24M$, and by Markov's inequality a trial of lines L21 and L22 fails with probability less than $24/64 = 3/8$. So the loop ends with probability 1. Line L21 makes (D1) hold. Line L23 sets $L_j = 2\max(n_j, 1) \ge n_j$, so Lemma 1 applies to each bucket and gives (D2) and (D3). Then $\sum_j 2L_j^2 = \sum_j 8 \max(n_j, 1)^2 \le 64M \le 512M$, which is (D4), and $u = 0$ gives (D5). $\square$

**Lemma 3 (search).** If (D1) and (D2) hold, DPH-SEARCH$(x)$ returns true exactly when $x \in S$.

*Proof.* Let $j = h(x)$. If $x \in S$, then $x \in S_j$ by (D1), and $T_j[h_j(x)] = x$ by (D2), so line L15 returns true. If $x \notin S$, then $x \notin S_j$, and by (D2) each non-NIL slot of $T_j$ holds a key of $S_j$, so $T_j[h_j(x)] \ne x$ and line L15 returns false. $\square$

**Theorem.** Each operation ends with probability 1 and keeps (D1) to (D5). So each search, and the test of lines L1 and L10, is correct.

*Proof.* By induction on the operations. The start is REHASH-ALL, covered by Lemma 2. Assume (D1) to (D5) before an operation. A search changes nothing. By Lemma 3, lines L1 and L10 return exactly for the operations that are not effective, which change nothing.

*Effective insert of $x \notin S$.* If line L3 calls REHASH-ALL, Lemma 2 gives the invariants for $S \cup \{x\}$. Otherwise $u \le \lceil M/2 \rceil$ after line L2, which keeps (D5). Line L4 adds $x$ to $S_{h(x)}$ and nothing else, which keeps (D1), and raises $|S_j|$ and $c_j$ by 1 each, which keeps $|S_j| \le c_j$. Now there are four cases.

1. Line L5 stores $x$. Then $c_j \le L_j$, which is (D3). The slot $h_j(x)$ was NIL, so by (D2) no key of $S_j \setminus \{x\}$ has this slot, $h_j$ is one-to-one on $S_j$, and the stored keys are exactly $S_j$. (D4) is unchanged.
2. $c_j \le L_j$ but the slot was in use. Lines L6 to L8 do nothing, and line L9 rebuilds with $|S_j| \le c_j \le L_j$. Lemma 1 applies.
3. $c_j > L_j$ and $|S_j| \le L_j/2$. Line L9 rebuilds with $|S_j| \le L_j$, and Lemma 1 applies.
4. $c_j > L_j$ and $|S_j| > L_j/2$. Before line L4, $c_j \le L_j$, so now $c_j = L_j + 1$ and $|S_j| \le L_j + 1 \le 2L_j$. Line L7 doubles $L_j$, so $|S_j| \le L_j$ for the new limit. If line L8 calls REHASH-ALL, Lemma 2 applies to $S$, which contains $x$ since line L4. Otherwise $\sum_i 2L_i^2 \le 512M$, which is (D4), and line L9 rebuilds with $|S_j| \le L_j$, so Lemma 1 applies.

In cases 2 to 4, the other buckets and $L_i$ do not change, so their invariants still hold.

*Effective delete of $x \in S$.* If line L12 calls REHASH-ALL, Lemma 2 gives the invariants for $S \setminus \{x\}$. Otherwise (D5) holds as above. By (D1) and (D2), $x \in S_j$ for $j = h(x)$, and $T_j[h_j(x)] = x$. Line L13 sets this slot to NIL and removes $x$ from $S_j$, so the stored keys are again exactly $S_j$, and $h_j$ stays one-to-one on the smaller set: (D1) and (D2) hold. $|S_j|$ goes down and $c_j$ and $L_j$ do not change, so (D3) and (D4) hold. $\square$

**Corollary (the size of $M$).** In each state, $M \le 2|S| + 1$.

*Proof.* Let $n_0$ be the size of $S$ at the last REHASH-ALL. Since then, there were $u \le \lceil M/2 \rceil$ effective updates by (D5), each changing $|S|$ by 1, so $|S| \ge n_0 - \lceil M/2 \rceil$. If $n_0 = 0$, $M = 1 \le 2|S| + 1$. Otherwise $M = n_0$, and $|S| \ge n_0 - \lceil n_0/2 \rceil = \lfloor n_0/2 \rfloor \ge (n_0 - 1)/2$, which gives $M \le 2|S| + 1$. $\square$
