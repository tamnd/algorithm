---
title: Proof that ambiguity of context-free grammars is undecidable
proves: [statement]
status: full
---

Let $(x, y)$ be an instance of Post's correspondence problem with lists $x = (x_1, \ldots, x_m)$ and $y = (y_1, \ldots, y_m)$ over $\Sigma$, let $I = \{1, \ldots, m\}$ be new symbols, and for a sequence $s = (i_1, \ldots, i_k)$ write $x_s = x_{i_1} \cdots x_{i_k}$, $y_s = y_{i_1} \cdots y_{i_k}$ and $\overleftarrow{s} = i_k \cdots i_1$. Let $G_{x,y}$ have start symbol $S$ and the productions
$$S \to A \mid B, \qquad A \to x_i\, A\, i \mid x_i\, i, \qquad B \to y_i\, B\, i \mid y_i\, i \qquad (i \in I).$$

**Lemma 1.** For every string $w$, there is at most one parse tree of $w$ with root $A$, and at most one with root $B$. The strings derived from $A$ are the strings $x_s \overleftarrow{s}$ with $s$ nonempty, and those derived from $B$ are the strings $y_s \overleftarrow{s}$.

*Proof.* By induction on the number of steps, every sentential form derived from $A$ is $x_{i_1} \cdots x_{i_j} A\, i_j \cdots i_1$, or, after a step $A \to x_i\, i$, a string $x_s \overleftarrow{s}$; and every nonempty $s$ is reached by the obvious derivation. A parse tree with root $A$ is a chain: each node $A$ has the children $x_i$, $A$, $i$, or $x_i$, $i$. The sequence of indices $i$ along the chain, read from the bottom up, is the suffix of the yield in $I^*$. Since the yield $x_s \overleftarrow{s}$ has $\overleftarrow{s}$ as its longest suffix in $I^*$ (the symbol before it, if any, is in $\Sigma$), the yield determines the sequence of indices, and the sequence determines the tree. The same holds for $B$. $\square$

**Lemma 2.** $G_{x,y}$ is ambiguous if and only if the instance has a solution.

*Proof.* Suppose $w$ has two different parse trees $T_1, T_2$ with root $S$. The root of each uses $S \to A$ or $S \to B$. If both used $S \to A$, their subtrees at $A$ would be two different trees of $w$ with root $A$, which Lemma 1 rules out; the same for $B$. So one tree derives $w$ from $A$ and the other from $B$, and by Lemma 1, $w = x_s \overleftarrow{s} = y_t \overleftarrow{t}$ for nonempty $s, t$. Both $\overleftarrow{s}$ and $\overleftarrow{t}$ are the longest suffix of $w$ in $I^*$, so $s = t$, and the parts before the suffix give $x_s = y_s$. So $s$ is a solution.

Conversely, if $s$ is a solution, the string $w = x_s \overleftarrow{s} = y_s \overleftarrow{s}$ has a tree that starts with $S \to A$ and one that starts with $S \to B$, by Lemma 1, and these are different. $\square$

**Theorem.** The set of ambiguous context-free grammars is recursively enumerable and complete for the recursively enumerable sets under many-one reductions. In particular it is undecidable, and the set of unambiguous grammars is not recursively enumerable.

*Proof.* *Membership.* The parse trees of $G$ with root $S$ can be listed effectively, ordered by size. A program that runs through all pairs of different trees in this list and halts when it finds two with the same yield halts exactly when $G$ is ambiguous. So the set is recursively enumerable.

*Hardness.* The map $(x, y) \mapsto G_{x,y}$ is computable, and by Lemma 2 it is a many-one reduction from PCP to ambiguity. PCP is complete for the recursively enumerable sets (Post 1946, and the standard reduction from the halting problem), so ambiguity is complete too. A complete recursively enumerable set is not decidable, and its complement is not recursively enumerable, since a set that is recursively enumerable with a recursively enumerable complement is decidable.

*Restrictions.* $G_{x,y}$ is linear. PCP remains undecidable for lists over $\{a, b\}$. Replacing each index symbol $i$ by the string $d\, c^i$, with new letters $c$ and $d$, keeps Lemma 1 true: the longest suffix of the yield in $\{c, d\}^*$ is the coded index sequence, and the coding $i \mapsto d c^i$ is uniquely decodable because each code word starts with $d$ and contains no other $d$. So the reduction produces linear grammars over $\{a, b, c, d\}$. $\blacksquare$
