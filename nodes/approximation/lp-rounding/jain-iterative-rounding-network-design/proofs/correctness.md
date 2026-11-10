---
title: Each vertex of the cut LP has an edge with value at least 1/2, so iterative rounding costs at most twice the LP
proves: [correctness]
status: full
---

**Setting.** The graph $G = (V, E)$ has costs $c_e \ge 0$. For $S \subseteq V$, $\delta(S)$ is the set of edges with exactly one end in $S$, and for $D \subseteq E$ and a vector $x$, $x(D) = \sum_{e \in D} x_e$ and $d_D(S) = |D \cap \delta(S)|$. Fix a vertex $\rho \in V$. Since $\delta(S) = \delta(V \setminus S)$ and $f(S) = f(V \setminus S)$, it is enough to write the cut rows for the nonempty sets $S \subseteq V \setminus \{\rho\}$; call these the *proper* sets. Two proper sets $A, B$ *cross* if $A \cap B$, $A \setminus B$ and $B \setminus A$ are all nonempty. A family of proper sets is *laminar* if no two of its sets cross. For a proper set $S$, write $\chi_S \in \{0, 1\}^{E'}$ for the incidence vector of $\delta(S) \cap E'$, where $E'$ is the current edge set.

A function $h$ on proper sets is *weakly supermodular* if for each two proper sets $A, B$,

$$h(A) + h(B) \le h(A \cap B) + h(A \cup B) \quad \text{or} \quad h(A) + h(B) \le h(A \setminus B) + h(B \setminus A),$$

where $h(\emptyset) = 0$. All sets named here are proper, since none contains $\rho$.

**Lemma 1 ($f$ is weakly supermodular).** $f(S) = \max \{ r_{uv} : |S \cap \{u, v\}| = 1 \}$, with $\max \emptyset = 0$, is weakly supermodular.

*Proof.* Split $V$ into the four atoms $Q_1 = A \cap B$, $Q_2 = A \setminus B$, $Q_3 = B \setminus A$ and $Q_4 = V \setminus (A \cup B)$. Then $\delta(Q_4) = \delta(A \cup B)$ and $f(Q_4) = f(A \cup B)$, so the two right sides are $f(Q_1) + f(Q_4)$ and $f(Q_2) + f(Q_3)$. A pair is separated by an atom when the atom holds exactly one of its ends, so a pair with ends in two different atoms is separated by both of those atoms. Call $Q_1, Q_4$ the $X$ atoms and $Q_2, Q_3$ the $Y$ atoms.

If $f(A) = 0$, then $f(A) + f(B) = f(B)$. If also $f(B) = 0$, there is nothing to prove. Otherwise a pair that gives $f(B)$ has its ends in two different atoms, so it is separated by at least one atom, and the side that holds this atom is at least $f(B)$, since $f \ge 0$. The case $f(B) = 0$ is the same. Otherwise let $p$ be a pair with $r_p = f(A)$ separated by $A$, so with one end in $Q_1 \cup Q_2$ and one in $Q_3 \cup Q_4$, and let $q$ be a pair with $r_q = f(B)$ separated by $B$, so with one end in $Q_1 \cup Q_3$ and one in $Q_2 \cup Q_4$. It is enough to find two different atoms $Z \ne Z'$ of the same kind ($X$ or $Y$) with $p$ separated by $Z$ and $q$ by $Z'$, or one kind with both atoms separating the same pair of the larger value.

The possible atom pairs of $p$ are $\{1, 3\}$, $\{1, 4\}$, $\{2, 3\}$, $\{2, 4\}$, and those of $q$ are $\{1, 2\}$, $\{1, 4\}$, $\{2, 3\}$, $\{3, 4\}$.

- If $p$ is in $\{1, 4\}$ and $q$ is in $\{2, 3\}$, or $p$ is in $\{2, 3\}$ and $q$ is in $\{1, 4\}$: the pair of larger value is separated by both atoms of one kind, so that side is at least $2 \max(r_p, r_q) \ge r_p + r_q$.
- If $p$ is in $\{1, 4\}$ and $q$ is not in $\{2, 3\}$: $q$ is separated by an $X$ atom $Z'$, and $p$ is separated by the other $X$ atom. The case $q$ in $\{1, 4\}$ and $p$ not in $\{2, 3\}$ is the same with roles swapped, and the cases with $\{2, 3\}$ and the $Y$ atoms are the same with $Y$ for $X$.
- Otherwise $p$ is in $\{1, 3\}$ or $\{2, 4\}$ and $q$ is in $\{1, 2\}$ or $\{3, 4\}$. Each has exactly one $X$ atom and one $Y$ atom. If their $X$ atoms differ, use them. If both have $X$ atom $Q_1$, then $p = \{1, 3\}$ and $q = \{1, 2\}$, with $Y$ atoms $Q_3 \ne Q_2$. If both have $X$ atom $Q_4$, then $p = \{2, 4\}$ and $q = \{3, 4\}$, with $Y$ atoms $Q_2 \ne Q_3$.

In each case one right side is at least $r_p + r_q = f(A) + f(B)$. $\square$

**Lemma 2 (cut functions).** For each $D \subseteq E$ and each $x \ge 0$, and all proper $A, B$,

$$x(\delta(A)) + x(\delta(B)) = x(\delta(A \cap B)) + x(\delta(A \cup B)) + 2 x(E(A \setminus B, B \setminus A)),$$
$$x(\delta(A)) + x(\delta(B)) = x(\delta(A \setminus B)) + x(\delta(B \setminus A)) + 2 x(E(A \cap B, V \setminus (A \cup B))),$$

where $E(P, R)$ is the set of edges with one end in $P$ and one in $R$. In particular $g = f - d_F$ is weakly supermodular for each $F \subseteq E$.

*Proof.* Count each edge by the atoms of its ends. An edge inside one atom is counted 0 times on each side. An edge between $Q_1$ and $Q_2$ is in $\delta(B)$, in $\delta(A \cap B)$ and in $\delta(A \setminus B)$, once on each side of each identity. The same check for the other four kinds of edges shows that the only difference is an edge between $Q_2$ and $Q_3$, counted twice on the left and 0 times on the right of the first identity, and an edge between $Q_1$ and $Q_4$, the same for the second. With $x = \chi_D$, this shows $d_D(A) + d_D(B) \ge d_D(A \cap B) + d_D(A \cup B)$ and $d_D(A) + d_D(B) \ge d_D(A \setminus B) + d_D(B \setminus A)$. Subtract the matching one from the inequality of Lemma 1. $\square$

**Lemma 3 (uncrossing).** Let $0 < x_e < 1$ for each $e \in E'$, and call a proper set $S$ *tight* if $x(\delta(S) \cap E') = g(S)$. If $A$ and $B$ are tight and cross, then either $A \cap B$ and $A \cup B$ are tight and $\chi_A + \chi_B = \chi_{A \cap B} + \chi_{A \cup B}$, or $A \setminus B$ and $B \setminus A$ are tight and $\chi_A + \chi_B = \chi_{A \setminus B} + \chi_{B \setminus A}$.

*Proof.* Suppose the first inequality of weak supermodularity holds for $g$ (Lemma 2). Then, with the first identity of Lemma 2 on $E'$, and with each set feasible,

$$g(A) + g(B) = x(\delta(A)) + x(\delta(B)) \ge x(\delta(A \cap B)) + x(\delta(A \cup B)) \ge g(A \cap B) + g(A \cup B) \ge g(A) + g(B).$$

So all are equalities: $A \cap B$ and $A \cup B$ are tight, and $x(E'(A \setminus B, B \setminus A)) = 0$. Since $x_e > 0$ on $E'$, no edge of $E'$ joins $A \setminus B$ to $B \setminus A$, and the edge count in the proof of Lemma 2 gives $\chi_A + \chi_B = \chi_{A \cap B} + \chi_{A \cup B}$. The other case is the same with the second identity. $\square$

**Lemma 4 (fewer crossings).** Let $\mathcal{L}$ be laminar, $T \in \mathcal{L}$, and let $S$ cross $T$. For each $W \in \{S \cap T, S \cup T, S \setminus T, T \setminus S\}$, every set of $\mathcal{L}$ that crosses $W$ also crosses $S$, and $T$ crosses $S$ but not $W$. So fewer sets of $\mathcal{L}$ cross $W$ than cross $S$.

*Proof.* $T$ does not cross $W$: $S \cap T \subseteq T$, $T \subseteq S \cup T$, $S \setminus T$ is disjoint from $T$, and $T \setminus S \subseteq T$. Let $R \in \mathcal{L}$ cross $W$. Since $R$ and $T$ do not cross, $R \subseteq T$, $T \subseteq R$ or $R \cap T = \emptyset$.

- $W = S \cap T$. If $R \cap T = \emptyset$ then $R \cap W = \emptyset$, and if $T \subseteq R$ then $W \subseteq R$; neither crosses. So $R \subseteq T$. Then $R \cap S \supseteq R \cap W \ne \emptyset$, $R \setminus S = R \setminus W \ne \emptyset$, and $S \setminus R \supseteq W \setminus R \ne \emptyset$.
- $W = S \cup T$. If $R \subseteq T$ then $R \subseteq W$. If $T \subseteq R$: $R \cap S \supseteq T \cap S \ne \emptyset$, $R \setminus S \supseteq R \setminus W \ne \emptyset$, $S \setminus R = W \setminus R \ne \emptyset$. If $R \cap T = \emptyset$: $R \cap S = R \cap W \ne \emptyset$, $R \setminus S \supseteq R \setminus W \ne \emptyset$, $S \setminus R \supseteq S \cap T \ne \emptyset$.
- $W = S \setminus T$. If $R \subseteq T$ then $R \cap W = \emptyset$. If $T \subseteq R$: $R \cap S \supseteq T \cap S \ne \emptyset$, $R \setminus S \supseteq T \setminus S \ne \emptyset$, $S \setminus R = W \setminus R \ne \emptyset$. If $R \cap T = \emptyset$: $R \cap S \supseteq R \cap W \ne \emptyset$, $R \setminus S = R \setminus W \ne \emptyset$, $S \setminus R \supseteq S \cap T \ne \emptyset$.
- $W = T \setminus S$. If $R \cap T = \emptyset$ then $R \cap W = \emptyset$, and if $T \subseteq R$ then $W \subseteq R$. So $R \subseteq T$. Then $R \cap S = R \setminus W \ne \emptyset$, $R \setminus S \supseteq R \cap W \ne \emptyset$, and $S \setminus R \supseteq S \setminus T \ne \emptyset$.

In each case $R$ crosses $S$. $\square$

**Lemma 5 (a laminar basis).** Let $x$ be a vertex of $P = \{ x \in [0, 1]^{E'} : x(\delta(S) \cap E') \ge g(S) \text{ for each proper } S \}$ with $0 < x_e < 1$ for each $e \in E'$. Then there is a laminar family $\mathcal{L}$ of tight sets with $|\mathcal{L}| = |E'|$ whose vectors $\chi_S$ are linearly independent.

*Proof.* No bound $0 \le x_e \le 1$ is tight, so, since $x$ is a vertex, the vectors $\chi_S$ of the tight sets span $\mathbb{R}^{E'}$. Let $\mathcal{L}$ be a maximal laminar family of tight sets, and suppose some tight $S$ has $\chi_S \notin \operatorname{span} \{ \chi_R : R \in \mathcal{L} \}$. Choose such an $S$ that crosses the fewest sets of $\mathcal{L}$. If $S$ crosses no set of $\mathcal{L}$, then $\mathcal{L} \cup \{S\}$ is laminar, against maximality; so $S$ crosses some $T \in \mathcal{L}$. By Lemma 3, $\chi_S = \chi_{W_1} + \chi_{W_2} - \chi_T$ for two tight sets $W_1, W_2$ from Lemma 4's list. One of $\chi_{W_1}, \chi_{W_2}$ is not in the span, and by Lemma 4 it crosses fewer sets of $\mathcal{L}$ than $S$, against the choice of $S$. So the span of $\mathcal{L}$ is $\mathbb{R}^{E'}$, and a basis taken from $\mathcal{L}$ is laminar, tight and of size $|E'|$. $\square$

**Lemma 6 (Jain's theorem).** If $x$ is a vertex of the LP of line L3 and $g(S) > 0$ for some proper $S$, then $x_e \ge 1/2$ for some edge $e$.

*Proof.* If some $x_e = 1$, we are done. Let $E' = \{ e : x_e > 0 \}$. Some $x(\delta(S)) \ge g(S) > 0$, so $E' \ne \emptyset$. The restriction of $x$ to $E'$ is a vertex of the LP on $E'$: if it were the midpoint of two feasible points, padding both with zeros would make $x$ the midpoint of two feasible points of the original LP. So assume, for a contradiction, that $0 < x_e < 1/2$ on $E'$, and take $\mathcal{L}$ from Lemma 5. Each $S \in \mathcal{L}$ has $\chi_S \ne 0$, so $g(S) = x(\delta(S)) > 0$.

Each edge $e = uv \in E'$ hands out tokens: $x_e$ to the smallest set of $\mathcal{L}$ that holds $u$, $x_e$ to the smallest that holds $v$, and $1 - 2x_e$ to the smallest that holds both $u$ and $v$. A token is lost if no such set exists. Each edge hands out at most 1 in total.

*Each set gets at least 1.* Let $S \in \mathcal{L}$ with children $R_1, \ldots, R_t$ (the maximal sets of $\mathcal{L}$ inside $S$), and let $Q = S \setminus \bigcup_i R_i$. Count by where the ends of an edge lie; the second column is the edge's term in $\Delta = x(\delta(S)) - \sum_i x(\delta(R_i))$ and the third its tokens to $S$.

| edge | term in $\Delta$ | tokens to $S$ |
|---|---|---|
| one end in $Q$, the other outside $S$ | $x_e$ | $x_e$ |
| one end in some $R_i$, the other outside $S$ | $0$ | $0$ |
| ends in two different children | $-2x_e$ | $1 - 2x_e$ |
| one end in a child, the other in $Q$ | $-x_e$ | $1 - x_e$ |
| both ends in $Q$ | $0$ | $1$ |
| both ends in one child, or both outside $S$ | $0$ | $0$ |

So the tokens of $S$ total $\Delta + N$, where $N$ is the number of edges whose smallest set holding both ends is $S$. Since all sets are tight, $\Delta = g(S) - \sum_i g(R_i)$ is an integer, so the tokens of $S$ are an integer. Each nonzero entry of the third column is positive, as $0 < x_e < 1/2$. If $S$ got no token, no edge of $E'$ would be in rows 1, 3, 4 or 5, and then $\chi_S = \sum_i \chi_{R_i}$, against independence. So $S$ gets at least 1.

*Some token is lost.* Let $S$ be a maximal set of $\mathcal{L}$, and $e = uv \in \delta(S) \cap E'$, which exists since $\chi_S \ne 0$, with $u \in S$. A set of $\mathcal{L}$ that holds $u$ and $v$ meets $S$, so by laminarity it contains $S$ or lies in $S$; it does not lie in $S$, since $v \notin S$, and it does not strictly contain $S$, by maximality. So no set holds both ends, and the token $1 - 2x_e > 0$ is lost.

So the sets of $\mathcal{L}$ get less than $|E'|$ in total but at least $|\mathcal{L}| = |E'|$, a contradiction. $\square$

**Theorem.** If $E$ meets the requirements, JAIN-ITERATIVE-ROUNDING ends after at most $m$ rounds and returns a feasible $F$ with $c(F) \le 2 \, \text{LP}_1 \le 2 \, \text{OPT}$, where $\text{LP}_1$ is the value of the first LP.

*Proof.* Consider a round with bought set $F$, LP value $\text{LP}$, vertex $x$ and heavy set $H$, so $H \ne \emptyset$ by Lemma 6. Let $x'$ be $x$ restricted to $E \setminus (F \cup H)$. For each proper $S$, since $x_e \le 1$,

$$x'(\delta(S) \setminus (F \cup H)) = x(\delta(S) \setminus F) - x(\delta(S) \cap H) \ge g(S) - |\delta(S) \cap H|,$$

which is the residual requirement after buying $H$. So $x'$ is feasible for the next LP, and its value $\text{LP}'$ satisfies $\text{LP}' \le \text{LP} - \sum_{e \in H} c_e x_e \le \text{LP} - \tfrac{1}{2} c(H)$, since $x_e \ge 1/2$ on $H$ and $c \ge 0$. The first LP is feasible, because $\chi_E$ is feasible, and by induction each later one is. Each round buys at least one new edge, so there are at most $m$ rounds, and the loop of line L2 ends with all residual requirements at most 0, that is, with $F$ feasible by Menger's theorem. Write $\text{LP}_{t+1} = 0$ after the last round $t$, which is valid since the empty point is then feasible. Summing $c(H_s) \le 2 (\text{LP}_s - \text{LP}_{s+1})$ over $s = 1, \ldots, t$ gives $c(F) \le 2 \, \text{LP}_1$. The incidence vector of an optimal feasible set is a point of the first LP, so $\text{LP}_1 \le \text{OPT}$. $\blacksquare$

**Remark.** Only Lemma 1 uses the special form of $f$. The proof of Lemma 6 works for every integer weakly supermodular $f$, so the factor 2 holds for all such requirement functions.
