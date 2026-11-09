---
title: PC-2 computes the strong path consistency closure
proves: [correctness, termination]
status: full
---

Fix the input domains $D_1, \ldots, D_n$ and the initial relations $R^0_{ij} \subseteq D_i \times D_j$ for $i < j$, with $R_{ji}$ always the converse of $R_{ij}$. A *network* here is a family $R = (R_{ij})_{i < j}$ with $R_{ij} \subseteq R^0_{ij}$; we write $R' \subseteq R$ and $R' \cup R''$ pair by pair. The triple $(i, k, j)$ is *satisfied* in $R$ if every $(a, b) \in R_{ij}$ has some $c \in D_k$ with $(a, c) \in R_{ik}$ and $(c, b) \in R_{kj}$. $R$ is path consistent if every triple is satisfied. The domains $D_k$ do not change before line L8.

**Lemma 1 (the closure).** The union of two path consistent networks is path consistent. So there is a largest path consistent network $R^\ast \subseteq R^0$. Every solution $s$ has $(s_i, s_j) \in R^\ast_{ij}$ for all $i < j$.

*Proof.* Let $(a, b) \in R'_{ij} \cup R''_{ij}$, say in $R'_{ij}$. Then some $c$ has $(a, c) \in R'_{ik} \subseteq R'_{ik} \cup R''_{ik}$ and $(c, b) \in R'_{kj} \subseteq R'_{kj} \cup R''_{kj}$. The network with all relations empty is path consistent, and there are finitely many networks inside $R^0$, so their union $R^\ast$ is the largest. For a solution $s$, the network $R^s_{ij} = \{(s_i, s_j)\}$ is path consistent with the witness $c = s_k$, so $R^s \subseteq R^\ast$. $\square$

**Lemma 2 (REVISE-PATH keeps the closure).** If $R^\ast \subseteq R$ before REVISE-PATH$(i, k, j)$, then $R^\ast \subseteq R$ after it.

*Proof.* Only $R_{ij}$ changes. Let $(a, b) \in R^\ast_{ij}$. Since $R^\ast$ is path consistent, some $c \in D_k$ has $(a, c) \in R^\ast_{ik} \subseteq R_{ik}$ and $(c, b) \in R^\ast_{kj} \subseteq R_{kj}$, so line L10 keeps $(a, b)$. $\square$

**Lemma 3 (the queue).** At each test of line L2, every triple that is not in $Q$ is satisfied in $R$.

*Proof.* Line L1 puts all triples in $Q$. Consider an iteration that removes $(i, k, j)$. After REVISE-PATH, every pair of $R_{ij}$ has a witness in $D_k$, so $(i, k, j)$ is satisfied. If $R_{ij}$ did not change, nothing else changed. If it shrank, look at a triple $t$ that is satisfied before and not in $Q$ after line L7.

- If $t$ does not read $R_{ij}$, it stays satisfied.
- If the target of $t$ is $R_{ij}$, that is $t = (i, k', j)$, then $t$ asks for witnesses of fewer pairs than before, with the same side relations, so it stays satisfied.
- Otherwise $t$ reads $R_{ij}$ as a side relation. The triples whose side relations are $R_{ik'}$ and $R_{k'j'}$ with $\{i, j\} = \{i, k'\}$ or $\{i, j\} = \{k', j'\}$ are, for some $m \notin \{i, j\}$, "the target $\{i, m\}$ through $j$" and "the target $\{j, m\}$ through $i$". These are the triples $(\min(i, m), j, \max(i, m))$ and $(\min(j, m), i, \max(j, m))$, and line L7 puts them in $Q$. So $t$ is not one of them.

So the claim holds at the next test. $\square$

**Termination.** Each iteration either deletes a pair from some $R_{ij}$, which happens at most $\sum_{i < j} |R^0_{ij}| \le n(n-1)d^2/2$ times, or deletes nothing and makes $|Q|$ drop by 1. $|Q|$ never exceeds the number of triples, $n(n-1)(n-2)/2$. So the loop stops.

**Lemma 4 (all or none).** Let $R$ be path consistent, and let $a \in D_i$ occur in some pair $(a, b) \in R_{ij}$. Then for every $k \ne i$ there is a pair $(a, c) \in R_{ik}$.

*Proof.* If $k = j$ this is the pair $(a, b)$. If $k \ne j$, the triple with target $\{i, j\}$ through $k$ is satisfied, so some $c \in D_k$ has $(a, c) \in R_{ik}$. $\square$

**Theorem.** PC-2 stops. Let $R^\ast$ be as in Lemma 1, and let $D^\ast_i$ be the set of values that occur in every $R^\ast_{ij}$, $j \ne i$ (for $n = 1$, $D^\ast_1 = D_1$). If PC-2 returns at line L9, its domains are $D^\ast$, its relations are $R^\ast$ restricted to $D^\ast$, and this network is strongly path consistent and contains every solution. PC-2 returns false exactly when some $R^\ast_{ij}$ or some $D^\ast_i$ is empty, and then the CSP has no solution.

*Proof.* By Lemma 2 and induction, $R^\ast \subseteq R$ at all times. If line L5 returns false, then $R_{ij} = \emptyset$, so $R^\ast_{ij} = \emptyset$, and by Lemma 1 no solution exists. Otherwise the loop ends with $Q = \emptyset$. By Lemma 3, $R$ is path consistent, so $R \subseteq R^\ast$ by Lemma 1, and so $R = R^\ast$.

Line L8 deletes from $D_i$ the values that are missing from some $R^\ast_{ij}$, which leaves $D^\ast_i$. By Lemma 4, a value of $D_i$ that occurs in one relation $R^\ast_{ij}$ occurs in all of them, so the deleted values occur in no relation, and deleting the pairs that use them changes no relation. So the relations stay $R^\ast$, and they stay path consistent. Each $a \in D^\ast_i$ occurs in a pair $(a, b) \in R^\ast_{ij}$ for each $j \ne i$, and $b$ occurs in $R^\ast_{ij}$, so $b \in D^\ast_j$ by Lemma 4 again. So every value has a support on every arc, and the network is arc consistent too, hence strongly path consistent. A solution $s$ has $(s_i, s_j) \in R^\ast_{ij}$ for all $j$, so $s_i \in D^\ast_i$. Line L9 returns false exactly when some $D^\ast_i$ is empty, and then no solution exists. $\blacksquare$

The strongly path consistent network returned is also the largest one inside the input: any strongly path consistent sub-network is path consistent, so its relations lie in $R^\ast$, and each of its values occurs in all its relations (it is arc consistent), so its domains lie in $D^\ast$.
