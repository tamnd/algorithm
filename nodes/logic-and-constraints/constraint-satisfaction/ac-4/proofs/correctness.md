---
title: AC-4 computes the arc consistency closure
proves: [correctness, termination]
status: full
---

Fix a binary CSP with input domains $D^0$, a relation $R_{ij}$ for each arc, and $R_{ji}$ the converse of $R_{ij}$. Let $D^\ast \subseteq D^0$ be the arc consistency closure, the largest arc consistent subdomains; the page [arc consistency](/arc-consistency/) proves that it exists and is unique. For an arc $(i, j)$ and a value $a$, let

$$\mathrm{live}(i, j, a) = |\{ b : (a, b) \in R_{ij},\ b \in D_j \text{ or } (j, b) \in L \}|.$$

**Lemma 1 (after the set-up).** When line L7 is first reached:

1. a value is in $D^0_i \setminus D_i$ exactly when $(i, a)$ is in $L$, and it is there once;
2. for each $b \in D^0_j$, the list $S[j, b]$ holds exactly the pairs $(i, a)$ with $a \in D^0_i$ and $(a, b) \in R_{ij}$, over all arcs $(i, j)$;
3. for each arc $(i, j)$ and each $a \in D_i$, $N[i, j, a] = \mathrm{live}(i, j, a) > 0$.

*Proof.* Lines L3 to L5 loop over all $a \in D^0_i$ and $b \in D^0_j$, so after them $N[i, j, a] = |\{b \in D^0_j : (a, b) \in R_{ij}\}|$ and the lists are as in point 2. A value is deleted only at line L6, after the test $a \in D_i$, and is put in $L$ at the same time; nothing is removed from $L$ during the set-up. This gives point 1. By point 1, $D^0_j = D_j \cup \{b : (j, b) \in L\}$, so $N[i, j, a] = \mathrm{live}(i, j, a)$. If this number is 0 for some arc, line L6 for that arc deletes $a$, so each $a$ still in $D_i$ has a positive counter on each arc. $\square$

**Lemma 2 (the loop).** At each test of line L7, points 1 and 3 of Lemma 1 hold with "$(i, a)$ is in $L$ or was removed from $L$" in point 1, and with $\mathrm{live}$ as defined above in point 3.

*Proof.* By induction on the iterations. Let one iteration remove $(j, b)$ at line L8. Then $b \notin D_j$ and $(j, b)$ is no longer in $L$, so for each arc $(i, j)$ and each $a$ with $(a, b) \in R_{ij}$, the number $\mathrm{live}(i, j, a)$ drops by exactly 1. By point 2 of Lemma 1, these $a$ are exactly the entries $(i, a)$ of $S[j, b]$. For each such $a \in D_i$, line L10 lowers $N[i, j, a]$ by 1, so the equality of point 3 stays true. If the counter becomes 0, line L11 deletes $a$ and appends $(i, a)$ to $L$; then $a \notin D_i$, and point 3 says nothing more about it. The deletion of $a$ moves $a$ from $D_i$ to $L$, so $\mathrm{live}(k, i, c)$ does not change for any $k$ and $c$. Counters of values not in $S[j, b]$ do not change, and neither do their live numbers. A value is deleted only when it is in $D_i$, so it enters $L$ at most once. $\square$

**Lemma 3 (no closure value is deleted).** At all times $D^\ast \subseteq D$.

*Proof.* At the start $D = D^0 \supseteq D^\ast$. A value $a$ is deleted at line L6 or line L11 only when its counter on some arc $(i, j)$ is 0. By Lemmas 1 and 2, the counter of a value of $D_i$ is $\mathrm{live}(i, j, a)$, at least the number of supports of $a$ in $D_j$. (At line L6, during the set-up, the counter is the number of supports in $D^0_j \supseteq D_j$.) If $a \in D^\ast_i$, then $a$ has a support in $D^\ast_j$, and $D^\ast_j \subseteq D_j$ by induction, so the counter is at least 1 and $a$ is not deleted. $\square$

**Termination.** Each iteration of line L7 removes one pair from $L$. A pair enters $L$ only when its value is deleted, and each value is deleted at most once (Lemma 2), so there are at most $\sum_i |D^0_i| \le nd$ iterations. Each iteration reads one finite list.

**Theorem.** AC-4 stops with $D = D^\ast$. It returns true if and only if no domain of $D^\ast$ is empty.

*Proof.* When the loop stops, $L$ is empty, so for each arc $(i, j)$ and each $a \in D_i$, the counter equals the number of supports of $a$ in $D_j$ (Lemma 2), and it is positive. So $D$ is arc consistent. $D \subseteq D^0$, so $D \subseteq D^\ast$ because $D^\ast$ is the largest arc consistent subdomain. With Lemma 3, $D = D^\ast$. Line L12 returns true exactly when no domain of $D = D^\ast$ is empty. $\blacksquare$
