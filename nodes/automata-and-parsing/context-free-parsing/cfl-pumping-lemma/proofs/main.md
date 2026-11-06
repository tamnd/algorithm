---
title: Proof of the pumping lemma for context-free languages
proves: [statement]
status: full
---

Let $L$ be a context-free language. By the [Chomsky normal form](/chomsky-normal-form/) theorem there is a grammar $G = (V, \Sigma, R, S)$ with $L(G) = L \setminus \{\varepsilon\}$ whose productions all have the form $A \to B C$ with $B, C \in V$ or $A \to a$ with $a \in \Sigma$. Let $k = |V|$ and $p = 2^k$. In a parse tree of $G$, every inner node is labelled by a nonterminal and has two inner children ($A \to B C$) or one leaf child ($A \to a$); the leaves are terminals. The *height* of a tree is the number of edges of its longest root-to-leaf path.

**Lemma 1.** A parse tree of $G$ of height $h$ has a yield of length at most $2^{h-1}$.

*Proof.* By induction on $h$. A tree of height 1 is a root $A$ with one leaf $a$, of yield length $1 = 2^0$. A tree of height $h \ge 2$ has a root that uses $A \to B C$, with two subtrees of height at most $h - 1$, whose yields have length at most $2^{h-2}$ each by induction. The yield of the tree is their concatenation, of length at most $2 \cdot 2^{h-2} = 2^{h-1}$. $\square$

**Lemma 2.** Every nonterminal $A$ with $A \Rightarrow^* w$ derives only nonempty strings $w$.

*Proof.* No production has an empty right side, and every derivation step replaces a nonterminal by one or two symbols, so the length of a sentential form never decreases and starts at 1. $\square$

**Lemma 3 (cut and paste).** Let $T$ be a parse tree with root label $X$ and yield $s$, let $N_1$ be a node of $T$ and $N_2$ a proper descendant of $N_1$, both labelled $A$, and write $s = u v x y z$ where $v x y$ is the yield of $N_1$ and $x$ is the yield of $N_2$. Then $X \Rightarrow^* u v^i x y^i z$ for every $i \ge 0$.

*Proof.* Let $T_1$ and $T_2$ be the subtrees at $N_1$ and $N_2$. Both have root label $A$, so either can stand at any node labelled $A$ and the result is still a parse tree: the production used at the parent of that node does not change. Replacing $T_1$ in $T$ by $T_2$ gives a tree with yield $u x z$, which is the case $i = 0$. For $i \ge 1$, let $T^{(1)} = T_1$, and let $T^{(j+1)}$ be $T_1$ with its subtree $T_2$ replaced by $T^{(j)}$; then $T^{(j)}$ has root $A$ and yield $v^j x y^j$, by induction on $j$, since $T_1$ has yield $v x y$ with $x$ the yield of the replaced subtree. Replacing $T_1$ in $T$ by $T^{(i)}$ gives a tree with yield $u v^i x y^i z$. $\square$

**Theorem.** Every $s \in L$ with $|s| \ge p$ can be written as $s = u v x y z$ with $|v y| \ge 1$, $|v x y| \le p$, and $u v^i x y^i z \in L$ for every $i \ge 0$.

*Proof.* If $L(G)$ is empty there is nothing to prove, so let $k \ge 1$. Since $|s| \ge p \ge 1$, $s \ne \varepsilon$, so $s \in L(G)$ and $s$ has a parse tree $T$ with root $S$. Let $h$ be its height. By Lemma 1, $2^k \le |s| \le 2^{h-1}$, so $h \ge k + 1$.

Fix a longest root-to-leaf path $P$ of $T$. It has $h$ edges and $h + 1$ nodes; the last one is a leaf and the other $h$ are inner nodes labelled by nonterminals. Look at the lowest $k + 1$ inner nodes of $P$. There are only $k$ nonterminals, so two of them have the same label $A$. Let $N_1$ be the upper one and $N_2$ the lower one. Let $v x y$ be the yield of $N_1$ and $x$ the yield of $N_2$, which is a factor of the yield of $N_1$ because $N_2$ is a descendant of $N_1$, and write $s = u v x y z$ accordingly.

*Condition $|v x y| \le p$.* The part of $P$ from $N_1$ to the leaf has at most $k + 1$ edges, because $N_1$ is one of the lowest $k + 1$ inner nodes of $P$. It is a longest path in the subtree at $N_1$: a longer path from $N_1$ down, together with the part of $P$ above $N_1$, would be a root-to-leaf path longer than $P$. So the subtree at $N_1$ has height at most $k + 1$, and by Lemma 1 its yield has length $|v x y| \le 2^k = p$.

*Condition $|v y| \ge 1$.* $N_1$ is an inner node with a proper descendant that is inner, so it uses a production $A \to B C$. Its children $M_B$ and $M_C$ have yields $s_B$ and $s_C$ with $v x y = s_B s_C$, and both are nonempty by Lemma 2. $N_2$ lies in one of the two subtrees. If it lies below $M_B$, then $x$ is a factor of $s_B$, so $y$ ends with all of $s_C$, and $|y| \ge |s_C| \ge 1$. If it lies below $M_C$, then $x$ is a factor of $s_C$, so $v$ starts with all of $s_B$, and $|v| \ge 1$.

*Condition $u v^i x y^i z \in L$.* By Lemma 3 with $X = S$, $S \Rightarrow^* u v^i x y^i z$ for every $i \ge 0$, so $u v^i x y^i z \in L(G) \subseteq L$. $\blacksquare$
