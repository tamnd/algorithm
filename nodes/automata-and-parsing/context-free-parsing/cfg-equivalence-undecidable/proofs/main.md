---
title: Proof that equivalence of context-free grammars is undecidable
proves: [statement]
status: full
---

Let $(x, y)$ be an instance of Post's correspondence problem with lists $x = (x_1, \ldots, x_m)$ and $y = (y_1, \ldots, y_m)$ of nonempty strings over $\Sigma$. Let $I = \{1, \ldots, m\}$ be new symbols and $\Delta = \Sigma \cup I$. For a sequence $s = (i_1, \ldots, i_k)$ write $x_s = x_{i_1} \cdots x_{i_k}$ and $\overleftarrow{s} = i_k \cdots i_1$. Let
$$L_x = \{ x_s\, \overleftarrow{s} : s \in I^k,\ k \ge 1 \},$$
and $L_y$ likewise. By Lemma 2 of the [proof for intersections](/cfl-intersection-undecidable/), $L_x \cap L_y \ne \emptyset$ if and only if the instance has a solution. We write $\overline{L} = \Delta^* \setminus L$.

**The grammar for the complement.** Let $G_{\overline{x}}$ have start symbol $C$ and the productions
$$C \to Q \mid D, \qquad D \to x_i\, D\, i \mid Y \mid Z_i\, i \quad (i \in I),$$
where $Q$ generates the regular language $\Delta^* \setminus \Sigma^* I^+$, $Y$ generates $\Sigma^+$, and $Z_i$ generates the regular language $(\Sigma^* \setminus x_i \Sigma^*)\, I^*$, each by a right-linear grammar built from a finite automaton. The construction is computable from $x$.

**Lemma 1.** $L(D) = \{ x_{j_1} \cdots x_{j_r}\, z\, j_r \cdots j_1 : r \ge 0,\ z \in \Sigma^+ \cup \bigcup_{i \in I} (\Sigma^* \setminus x_i \Sigma^*) I^*\, i \}$.

*Proof.* By induction on the number of uses of $D \to x_i D i$: each wraps the current string in $x_i \ldots i$, and the last step uses $D \to Y$ or $D \to Z_i\, i$. $\square$

**Lemma 2.** $L(G_{\overline{x}}) = \overline{L_x}$.

*Proof.* ($\subseteq$) Strings from $Q$ are not in $\Sigma^* I^+ \supseteq L_x$. Let $w \in L(D)$, written as in Lemma 1 with $j = (j_1, \ldots, j_r)$, and suppose $w \in L_x$, say $w = x_s \overleftarrow{s}$. The longest suffix of $w$ in $I^*$ is $\overleftarrow{s}$.

- If $z \in \Sigma^+$, then $w = x_j\, z\, \overleftarrow{j}$, and its longest suffix in $I^*$ is $\overleftarrow{j}$, because $z$ ends with a symbol of $\Sigma$. So $s = j$ and $x_s = x_j z$, which gives $z = \varepsilon$, a contradiction. (If $r = 0$, $w = z$ has no index symbol and is not in $L_x$.)
- If $z = u\, v\, i$ with $u \in \Sigma^* \setminus x_i \Sigma^*$ and $v \in I^*$, then $w = x_j\, u\, v\, i\, \overleftarrow{j}$, and its longest suffix in $I^*$ is $v\, i\, \overleftarrow{j}$. So $\overleftarrow{s} = v\, i\, \overleftarrow{j}$, that is, $s = (j_1, \ldots, j_r, i, \ldots)$ with the reverse of $v$ at the end, and $x_s = x_j\, x_i\, x_{t}$ for the sequence $t$ read from $v$. Comparing with $w = x_s \overleftarrow{s}$ gives $u = x_i\, x_t \in x_i \Sigma^*$, a contradiction.

($\supseteq$) Let $w \notin L_x$. If $w \notin \Sigma^* I^+$, then $w \in L(Q)$. Otherwise $w = u\, \overleftarrow{s}$ with $u \in \Sigma^*$ and $s = (i_1, \ldots, i_k)$, $k \ge 1$, and $u \ne x_s$. Let $r$ be the largest number with $0 \le r \le k$ such that $x_{i_1} \cdots x_{i_r}$ is a prefix of $u$, and write $u = x_{i_1} \cdots x_{i_r}\, u'$.

- If $r = k$, then $u' \ne \varepsilon$ because $u \ne x_s$, and $w = x_{i_1} \cdots x_{i_k}\, u'\, i_k \cdots i_1$ is derived by $k$ uses of $D \to x_i D i$ and then $D \to Y$ with $Y \Rightarrow^* u'$.
- If $r < k$, then $u'$ does not start with $x_{i_{r+1}}$, by the choice of $r$. So $w = x_{i_1} \cdots x_{i_r}\, (u'\, i_k \cdots i_{r+2})\, i_{r+1}\, i_r \cdots i_1$, and the part in parentheses is in $(\Sigma^* \setminus x_{i_{r+1}} \Sigma^*) I^*$, the language of $Z_{i_{r+1}}$. So $w$ is derived by $r$ uses of $D \to x_i D i$ and then $D \to Z_{i_{r+1}}\, i_{r+1}$. $\square$

**Theorem.** Universality, equivalence, inclusion, equality with a regular language and inclusion of a regular language in a context-free one are undecidable, and each is complete for the co-recursively-enumerable sets.

*Proof.* *The reduction.* Given $(x, y)$, compute $G_{\overline{x}}$ and $G_{\overline{y}}$ with disjoint nonterminals and let $G$ have the new start symbol $S$ with $S \to C_x \mid C_y$. By Lemma 2,
$$L(G) = \overline{L_x} \cup \overline{L_y} = \overline{L_x \cap L_y},$$
so $L(G) = \Delta^*$ if and only if $L_x \cap L_y = \emptyset$, if and only if the instance has no solution. This is a many-one reduction from the complement of PCP to universality. The complement of PCP is complete for the co-recursively-enumerable sets, since PCP is complete for the recursively enumerable sets. So universality is hard for that class.

*The other problems.* Let $G_\Delta$ be the grammar $S \to a S \mid \varepsilon$ ($a \in \Delta$) and $E_\Delta$ a regular expression for $\Delta^*$. Then $L(G) = \Delta^*$ if and only if $L(G) = L(G_\Delta)$, if and only if $L(G_\Delta) \subseteq L(G)$, if and only if $L(G) = L(E_\Delta)$, if and only if $L(E_\Delta) \subseteq L(G)$. So universality reduces to each of the problems 2 to 5, and each is hard.

*Membership in the class.* For each problem, a negative answer has a finite witness: a string in one language and not in the other. Membership of a string in a context-free or regular language is decidable, so listing all strings of $\Delta^*$ and testing each finds a witness exactly when the answer is negative. So the complement of each problem is recursively enumerable.

*Fixed alphabet.* PCP remains undecidable for lists over $\Sigma = \{a, b\}$. Replace each index symbol $i$ by the code $d\, c^i$ with new letters $c, d$. Lemma 2 holds with $I^*$ and $I^+$ replaced by the regular sets $\{d c^i : i \in I\}^*$ and its nonempty version, and with "longest suffix in $I^*$" replaced by the longest suffix in $\{c, d\}^*$, which decodes uniquely because every code starts with $d$. One also adds to $Q$ the strings whose suffix in $\{c, d\}^*$ is not a sequence of codes, which is regular. So universality is undecidable over $\{a, b, c, d\}$, and equivalence is undecidable with $G_2$ fixed to the grammar for $\{a, b, c, d\}^*$. $\blacksquare$
