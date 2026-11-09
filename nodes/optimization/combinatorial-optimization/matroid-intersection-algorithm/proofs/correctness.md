---
title: Augmenting along a shortest exchange path keeps a common independent set, and the absence of a path gives a set U with |I| = r1(U) + r2(E - U)
proves: [correctness, optimality, termination, certificate]
status: full
---

Let $M_1 = (E, \mathcal{I}_1)$ and $M_2 = (E, \mathcal{I}_2)$ be matroids on the same finite ground set $E$, with rank functions $r_1$ and $r_2$. For $I \in \mathcal{I}_1 \cap \mathcal{I}_2$ the *exchange graph* $D(I)$ has vertex set $E$ and, for $y \in I$ and $x \in E \setminus I$,

- an arc $(y, x)$ if $I - y + x \in \mathcal{I}_1$,
- an arc $(x, y)$ if $I - y + x \in \mathcal{I}_2$.

Let $X_1 = \{x \in E \setminus I : I + x \in \mathcal{I}_1\}$ and $X_2 = \{x \in E \setminus I : I + x \in \mathcal{I}_2\}$. We write $I - y + x$ for $(I \setminus \{y\}) \cup \{x\}$.

We use two standard facts about a matroid $M = (E, \mathcal{I})$. (F1) If $I \in \mathcal{I}$ and $I + x \notin \mathcal{I}$, then $I + x$ contains a unique circuit $C(I, x)$, it contains $x$, and $I - y + x \in \mathcal{I}$ holds exactly for $y \in C(I, x)$. (F2) For $S \subseteq E$, all maximal independent subsets of $S$ have size $r(S)$, so if $J \subseteq S$ is independent and $|J| < r(S)$, then $J + x \in \mathcal{I}$ for some $x \in S \setminus J$. Let $\mathrm{span}(I) = I \cup \{x : I + x \notin \mathcal{I}\}$ for independent $I$. (F3) If $J$ is independent and $J \subseteq \mathrm{span}(I)$, then $\mathrm{span}(J) \subseteq \mathrm{span}(I)$. Indeed, $I$ is a maximal independent subset of $\mathrm{span}(I)$, so $r(I \cup J) = |I|$ by (F2). If $x \in \mathrm{span}(J)$, then $r(J + x) = r(J)$, and submodularity of the rank function gives $r(I \cup J + x) \le r(I \cup J) + r(J + x) - r(J) = |I|$. So $I + x$ is not independent unless $x \in I$, that is, $x \in \mathrm{span}(I)$.

**Lemma 1 (exchange with a triangular pattern).** Let $I \in \mathcal{I}$, let $y_1, \ldots, y_m \in I$ and $x_1, \ldots, x_m \in E \setminus I$ be distinct, and suppose

1. $I - y_i + x_i \in \mathcal{I}$ for all $i$, and
2. $I - y_i + x_j \notin \mathcal{I}$ for all $i < j$.

Then $J = I - \{y_1, \ldots, y_m\} + \{x_1, \ldots, x_m\} \in \mathcal{I}$.

*Proof.* By induction on $m$. For $m \le 1$ the claim is condition 1. Let $m \ge 2$ and $I' = I - y_1 + x_1$, which is independent by condition 1. Fix $j \ge 2$. By condition 2 with $i = 1$, $I - y_1 + x_j \notin \mathcal{I}$, so $I + x_j \notin \mathcal{I}$ and, by (F1), $y_1 \notin C(I, x_j)$. So $C(I, x_j) \subseteq I - y_1 + x_j \subseteq I' + x_j$. Since $I'$ is independent, $C(I, x_j)$ is the unique circuit of $I' + x_j$, that is, $C(I', x_j) = C(I, x_j)$. By (F1), for every $i \ge 2$ we get $I' - y_i + x_j \in \mathcal{I}$ if and only if $y_i \in C(I, x_j)$, if and only if $I - y_i + x_j \in \mathcal{I}$. So the pairs $(y_2, x_2), \ldots, (y_m, x_m)$ satisfy conditions 1 and 2 for $I'$, and the induction hypothesis gives $I' - \{y_2, \ldots, y_m\} + \{x_2, \ldots, x_m\} = J \in \mathcal{I}$. $\square$

**Lemma 2 (augmentation).** Let $I \in \mathcal{I}_1 \cap \mathcal{I}_2$ and let $P = (x_0, y_1, x_1, y_2, \ldots, y_m, x_m)$ be a shortest path in $D(I)$ from $X_1$ to $X_2$, with $m \ge 0$. Then $J = I \,\triangle\, V(P) = I - \{y_1, \ldots, y_m\} + \{x_0, \ldots, x_m\}$ is in $\mathcal{I}_1 \cap \mathcal{I}_2$, and $|J| = |I| + 1$.

*Proof.* The arcs alternate as stated: an arc leaving an element of $E \setminus I$ enters $I$, and an arc leaving $I$ enters $E \setminus I$. Since $x_0 \in X_1 \subseteq E \setminus I$, the vertices $x_j$ are outside $I$ and the $y_i$ are in $I$, so $|J| = |I| + 1$. Because $P$ is shortest, it has no shortcut:

- (a) $x_j \notin X_1$ for $j \ge 1$, and $x_j \notin X_2$ for $j < m$;
- (b) there is no arc $(y_i, x_j)$ with $j > i$;
- (c) there is no arc $(x_j, y_i)$ with $i > j + 1$.

Each would give a shorter path from $X_1$ to $X_2$.

*$J \in \mathcal{I}_1$.* The arcs $(y_i, x_i)$ of $P$ give $I - y_i + x_i \in \mathcal{I}_1$, and (b) gives $I - y_i + x_j \notin \mathcal{I}_1$ for $i < j$. By Lemma 1 in $M_1$, $J' = I - \{y_1, \ldots, y_m\} + \{x_1, \ldots, x_m\} \in \mathcal{I}_1$. By (a), every $x_j$ with $j \ge 1$ lies in $\mathrm{span}_1(I)$, so $J' \subseteq \mathrm{span}_1(I)$ and, by (F3), $\mathrm{span}_1(J') \subseteq \mathrm{span}_1(I)$. Since $x_0 \in X_1$, $x_0 \notin \mathrm{span}_1(I)$, so $x_0 \notin \mathrm{span}_1(J')$ and $J = J' + x_0 \in \mathcal{I}_1$.

*$J \in \mathcal{I}_2$.* The arcs $(x_{i-1}, y_i)$ of $P$ give $I - y_i + x_{i-1} \in \mathcal{I}_2$. List the pairs in the order $(y_m, x_{m-1}), (y_{m-1}, x_{m-2}), \ldots, (y_1, x_0)$. For a pair $(y_i, x_{i-1})$ listed before a pair $(y_k, x_{k-1})$ we have $k < i$, so $k - 1 < i - 1$, and (c) gives $I - y_i + x_{k-1} \notin \mathcal{I}_2$. By Lemma 1 in $M_2$, $J'' = I - \{y_1, \ldots, y_m\} + \{x_0, \ldots, x_{m-1}\} \in \mathcal{I}_2$. By (a), $x_0, \ldots, x_{m-1} \in \mathrm{span}_2(I)$, so $\mathrm{span}_2(J'') \subseteq \mathrm{span}_2(I)$, while $x_m \in X_2$ is not in $\mathrm{span}_2(I)$. So $J = J'' + x_m \in \mathcal{I}_2$. $\square$

**Lemma 3 (certificate).** Let $I \in \mathcal{I}_1 \cap \mathcal{I}_2$ and suppose $D(I)$ has no path from $X_1$ to $X_2$. Let $U$ be the set of elements of $E$ from which $D(I)$ has a path to $X_2$ (so $X_2 \subseteq U$). Then $r_1(U) = |I \cap U|$ and $r_2(E \setminus U) = |I \setminus U|$, so $|I| = r_1(U) + r_2(E \setminus U)$.

*Proof.* There is no path from $X_1$ to $X_2$, so $X_1 \cap U = \emptyset$.

Suppose $r_1(U) > |I \cap U|$. By (F2) there is $x \in U \setminus I$ with $(I \cap U) + x \in \mathcal{I}_1$. As $x \in U$, $x \notin X_1$, so $I + x \notin \mathcal{I}_1$. The circuit $C = C_1(I, x)$ is not contained in the independent set $(I \cap U) + x$, so it contains some $y \in I \setminus U$. By (F1), $I - y + x \in \mathcal{I}_1$, which is an arc $(y, x)$. Then $y$ reaches $X_2$ through $x$, so $y \in U$, a contradiction.

Suppose $r_2(E \setminus U) > |I \setminus U|$. By (F2) there is $x \in (E \setminus U) \setminus I$ with $(I \setminus U) + x \in \mathcal{I}_2$. As $x \notin U \supseteq X_2$, $I + x \notin \mathcal{I}_2$. The circuit $C_2(I, x)$ is not contained in $(I \setminus U) + x$, so it contains some $y \in I \cap U$. By (F1), $I - y + x \in \mathcal{I}_2$, which is an arc $(x, y)$. Then $x$ reaches $X_2$ through $y$, so $x \in U$, a contradiction.

Both ranks are at least the sizes on the right, since $I \cap U$ and $I \setminus U$ are independent. So equality holds, and $|I| = |I \cap U| + |I \setminus U| = r_1(U) + r_2(E \setminus U)$. $\square$

**Lemma 4 (weak duality).** For every $J \in \mathcal{I}_1 \cap \mathcal{I}_2$ and every $U \subseteq E$, $|J| \le r_1(U) + r_2(E \setminus U)$.

*Proof.* $J \cap U$ is independent in $M_1$ and $J \setminus U$ is independent in $M_2$, so $|J| = |J \cap U| + |J \setminus U| \le r_1(U) + r_2(E \setminus U)$. $\square$

**Theorem.** The algorithm terminates after at most $r + 1$ rounds, where $r$ is the size of a largest common independent set. It returns a common independent set $I$ of size $r$ and a set $U$ with $|I| = r_1(U) + r_2(E \setminus U)$.

*Proof.* Line L1 starts with $I = \emptyset$, which is common independent. Line L5 finds a shortest path by breadth-first search from all of $X_1$ at once, and by Lemma 2 line L9 replaces $I$ by a common independent set one element larger. The size cannot exceed $r$, so after at most $r$ augmentations there is no path, and lines L7 and L8 return. At that point Lemma 3 gives $|I| = r_1(U) + r_2(E \setminus U)$, and Lemma 4 shows that no common independent set is larger than this number. So $|I| = r$, and $U$ proves it. $\blacksquare$

**Remark.** The same proof gives the [matroid intersection theorem](/matroid-intersection-theorem/), $\max |I| = \min_U \left( r_1(U) + r_2(E \setminus U) \right)$, since Lemma 4 is the inequality and the algorithm attains it.
