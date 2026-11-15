---
title: The queue algorithm computes the algebraic closure
proves: [correctness, termination]
status: full
---

Fix a calculus with the finite set $B$ of base relations, the identity base relation $\mathrm{id}$, the converse $r^{\smile}$ and the composition $\diamond$ read from the composition table: for relations $r, s \subseteq B$, $r \diamond s$ is the union of the table entries $a \diamond b$ with $a \in r$ and $b \in s$. Two facts about the table are used.

- **(T1) Converse rule.** $(a \diamond b)^{\smile} = b^{\smile} \diamond a^{\smile}$ for base relations $a, b$, and so for all relations.
- **(T2) Soundness of the table.** If $x \mathrel{a} y$, $y \mathrel{b} z$ and $x \mathrel{c} z$ hold for three objects of the domain, then $c \in a \diamond b$.

Both hold for every table that is built from the domain as the set of the triples that occur (this is weak composition), and so for a strong composition too. Composition distributes over union by its definition, so it is monotone: $r \subseteq r'$ and $s \subseteq s'$ give $r \diamond s \subseteq r' \diamond s'$.

A *network* on the nodes $0, \ldots, n-1$ is a family $R = (R_{ij})$ with $R_{ji} = R_{ij}^{\smile}$ and $R_{ii} = \{\mathrm{id}\}$. For networks $R'$ and $R''$, write $R' \subseteq R''$ and $R' \cup R''$ pair by pair. The *condition* $C(ij, k)$ for distinct $i, j, k$ is $R_{ij} \subseteq R_{ik} \diamond R_{kj}$. By (T1), $C(ij, k)$ and $C(ji, k)$ say the same thing, so we index the conditions by the unordered *target* $\{i, j\}$ and the third node $k$. The two *sides* of $C(ij, k)$ are the pairs $\{i, k\}$ and $\{k, j\}$. $R$ is *algebraically closed* if all conditions hold. Fix the input network $R^0$, and consider only networks $R \subseteq R^0$.

**Lemma 1 (the closure).** The union of two algebraically closed networks is algebraically closed. So there is a largest algebraically closed network $R^\ast \subseteq R^0$. For every solution $v$ of $R^0$, the scenario $S^v$ with $S^v_{ij} = \{$the base relation of $(v_i, v_j)\}$ satisfies $S^v \subseteq R^\ast$.

*Proof.* Let $R'$ and $R''$ be closed. Then $R'_{ij} \subseteq R'_{ik} \diamond R'_{kj} \subseteq (R'_{ik} \cup R''_{ik}) \diamond (R'_{kj} \cup R''_{kj})$ by monotonicity, and the same holds for $R''_{ij}$, so the union satisfies $C(ij, k)$. The network of empty relations is closed, so the union of all closed networks inside $R^0$ (finitely many) is the largest one. For a solution $v$, (T2) applied to $v_i, v_k, v_j$ shows that $S^v$ satisfies every condition, and $S^v \subseteq R^0$ because $v$ satisfies $R^0$. So $S^v \subseteq R^\ast$. $\square$

**Lemma 2 (a revision keeps the closure).** If $R^\ast \subseteq R$ before line L6 or line L10, then $R^\ast \subseteq R$ after line L9 or line L13.

*Proof.* Line L6 sets $T = R_{ik} \cap (R_{ij} \diamond R_{jk})$. Since $R^\ast$ satisfies $C(ik, j)$, $R^\ast_{ik} \subseteq R^\ast_{ij} \diamond R^\ast_{jk} \subseteq R_{ij} \diamond R_{jk}$, so $R^\ast_{ik} \subseteq T$. Line L9 writes $T$ and its converse, so $R^\ast \subseteq R$ still holds. Line L10 is the same with the target $\{k, j\}$ and the third node $i$. $\square$

**Lemma 3 (the queue).** Each time line L3 is reached, every condition that fails in $R$ has a side in $Q$.

*Proof.* At the first test, $Q$ holds all pairs. Consider one iteration, which removes $\{i, j\}$ at line L4. Inside the loop of line L5, $R_{ij}$ never changes, because every write is to a pair $\{i, k\}$ or $\{k, j\}$ with $k \notin \{i, j\}$.

Take a condition $C$ that holds before the iteration, or fails before it with a side in $Q$. We show that at the end of the iteration, $C$ holds or has a side in $Q$.

- A write to a pair puts that pair in $Q$ (lines L9 and L13). If a side of $C$ is written, $C$ has a side in $Q$.
- A write that shrinks the target of $C$ keeps $C$ true if it was true, because the right hand side does not change.
- If neither happens, $C$ reads the same relations as before. Its truth does not change, and the side it had in $Q$ is still in $Q$, unless that side is $\{i, j\}$.

So it is enough to look at the conditions with the side $\{i, j\}$ whose sides were not written. These are $C(ik, j)$ and $C(kj, i)$ for the nodes $k \notin \{i, j\}$. In the pass of the loop for $k$, line L6 makes $R_{ik} \subseteq R_{ij} \diamond R_{jk}$, so $C(ik, j)$ holds after line L9. Line L10 then makes $C(kj, i)$ hold, with the current $R_{ki}$. Later passes, for other values of $k$, do not write $R_{ij}$, $R_{ik}$, $R_{jk}$ or the target $\{k, j\}$ of this $k$. Line L10 of the same pass can write $R_{kj}$, which is a side of $C(ik, j)$, but then $\{k, j\}$ goes into $Q$. So each of these conditions holds or has a side in $Q$ at the end. $\square$

**Termination.** A pair goes into $Q$ only when its label shrinks and stays non-empty. A label has at most $|B|$ base relations, so it shrinks at most $|B| - 1$ times before it would become empty. So at most $\binom{n}{2}(|B| - 1)$ pairs are added after line L2, and at most $\binom{n}{2} |B|$ pairs leave the queue.

**Theorem.** The algorithm stops. It returns INCONSISTENT exactly when $R^\ast$ has an empty label, and then $R^0$ has no solution. Otherwise it returns $R^\ast$.

*Proof.* By Lemma 2 and induction, $R^\ast \subseteq R$ at all times. If line L1, L8 or L12 returns INCONSISTENT, some label of $R$ is empty, so the same label of $R^\ast$ is empty. A solution $v$ would give $S^v \subseteq R^\ast$ with a non-empty label on each pair (Lemma 1), so there is none.

Otherwise the loop ends with $Q = \emptyset$, and by Lemma 3 every condition holds. The conditions with a repeated node hold too: $R_{ij} \subseteq \{\mathrm{id}\} \diamond R_{ij}$ because $\mathrm{id} \diamond a = \{a\}$, and $\{\mathrm{id}\} \subseteq R_{ik} \diamond R_{ki}$ for a non-empty $R_{ik}$ because $\mathrm{id} \in a \diamond a^{\smile}$. Both facts follow from (T2) with two equal objects. So $R$ is closed, $R \subseteq R^\ast$ by Lemma 1, and $R = R^\ast$. If $R^\ast$ had an empty label, so would $R$, and line L1, L8 or L12 would have returned. $\blacksquare$

**Remark.** The theorem does not say that a returned network is consistent. Closure is a necessary condition. It is also sufficient for some calculi and subclasses (the point algebra, ORD-Horn networks, atomic Allen networks), but not for all of Allen's interval algebra.
