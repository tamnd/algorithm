---
title: Proof that emptiness of the intersection of two context-free languages is undecidable
proves: [statement]
status: full
---

Part 1 of the statement is proved on the page on [closure properties](/cfl-closure-properties/). We prove parts 2 to 4.

Let $(x, y)$ be an instance of Post's correspondence problem with lists $x = (x_1, \ldots, x_m)$ and $y = (y_1, \ldots, y_m)$ over $\Sigma$. Let $I = \{1, \ldots, m\}$ be a set of new symbols, $I \cap \Sigma = \emptyset$, and $\Delta = \Sigma \cup I$. For a sequence $s = (i_1, \ldots, i_k)$ of indices write $x_s = x_{i_1} \cdots x_{i_k}$, $y_s = y_{i_1} \cdots y_{i_k}$ and $\overleftarrow{s} = i_k \cdots i_1 \in I^*$. Define

$$G_x:\ A \to x_i\, A\, i \mid x_i\, i, \qquad G_y:\ B \to y_i\, B\, i \mid y_i\, i \qquad (i \in I),$$

with start symbols $A$ and $B$.

**Lemma 1.** $L(G_x) = \{ x_s\, \overleftarrow{s} : s \in I^k,\ k \ge 1 \}$, and every string of $L(G_x)$ has exactly one parse tree.

*Proof.* Every sentential form derived from $A$ is $x_{i_1} \cdots x_{i_j}\, A\, i_j \cdots i_1$ or a terminal string $x_{i_1} \cdots x_{i_k}\, i_k \cdots i_1$, by induction on the number of steps, since each step replaces the only nonterminal $A$ by $x_i A i$ or $x_i i$. Conversely every sequence $s$ with $k \ge 1$ gives the derivation that uses $A \to x_{i_j} A\, i_j$ for $j < k$ and $A \to x_{i_k} i_k$ last. For uniqueness, a string $w = x_s\, \overleftarrow{s}$ has $\overleftarrow{s}$ as its longest suffix in $I^*$, because $x_s \in \Sigma^*$ and the last symbol of $x_s$, if any, is not in $I$. So $w$ determines $s$, and $s$ determines the sequence of productions, and the grammar is linear, so the derivation is the only one. $\square$

The same holds for $G_y$.

**Lemma 2.** $L(G_x) \cap L(G_y) = \{ x_s\, \overleftarrow{s} : s \text{ is a solution} \}$.

*Proof.* Let $w \in L(G_x) \cap L(G_y)$. By Lemma 1, $w = x_s \overleftarrow{s} = y_t \overleftarrow{t}$ for some nonempty $s$ and $t$. Both $\overleftarrow{s}$ and $\overleftarrow{t}$ are the longest suffix of $w$ in $I^*$, so $s = t$, and then $x_s = y_s$ is the part of $w$ before that suffix. So $s$ is a solution. Conversely, if $s$ is a solution, $x_s \overleftarrow{s} = y_s \overleftarrow{s}$ is in both languages. $\square$

**Lemma 3.** If the instance has a solution, it has infinitely many, and $L(G_x) \cap L(G_y)$ is infinite.

*Proof.* If $s$ is a solution, so is the sequence $s^j$, $s$ repeated $j$ times, for every $j \ge 1$, and the strings $x_{s^j} \overleftarrow{s^j}$ are different because their index suffixes have different lengths. $\square$

**Part 2.** The map $(x, y) \mapsto (G_x, G_y)$ is computable. By Lemmas 2 and 3, the instance has a solution if and only if $L(G_x) \cap L(G_y) \ne \emptyset$. So PCP many-one reduces to intersection nonemptiness. If intersection emptiness were decidable, so would be PCP, which is undecidable (Post 1946). Nonemptiness is recursively enumerable: enumerate the strings of $\Delta^*$ in order of length and accept when one is in both languages, which is decidable for each string by the CYK algorithm. Since PCP is complete for the recursively enumerable sets, so is intersection nonemptiness.

**Part 3.** By Lemmas 2 and 3, $L(G_x) \cap L(G_y)$ is infinite if and only if it is nonempty, if and only if the instance has a solution. So the same reduction shows that infiniteness of the intersection is undecidable.

**Part 4.** $G_x$ and $G_y$ are linear, with at most one nonterminal on each right side, and unambiguous by Lemma 1. A deterministic pushdown automaton $P_x$ accepts $L(G_x)$:

- In state $p$, it reads symbols of $\Sigma$ and pushes each one.
- On reading an index symbol $i$, in state $p$ or $q$, it pops $|x_i|$ symbols one at a time with $\varepsilon$-moves through $|x_i|$ intermediate states that remember $i$ and the position in $x_i$, checking that they are the symbols of $x_i$ from the last to the first. If a check fails or the bottom marker appears too early, it moves to a dead state. After the last check it goes to state $q$.
- In state $q$ it reads no symbol of $\Sigma$: a symbol of $\Sigma$ leads to the dead state. It accepts in $q$ when the bottom marker is on top.

Every configuration has at most one move, so $P_x$ is deterministic. It accepts $w$ exactly when $w = u\, i_k \cdots i_1$ with $u \in \Sigma^*$, $k \ge 1$, and $u$ consumed from its end as $x_{i_k}$, then $x_{i_{k-1}}$, and so on, with nothing left: that is, $u = x_{i_1} \cdots x_{i_k}$. So $L(P_x) = L(G_x)$ by Lemma 1, and the language is deterministic context-free. The same holds for $G_y$. Hence the problems of parts 2 and 3 remain undecidable for linear, unambiguous grammars of deterministic languages. $\blacksquare$
