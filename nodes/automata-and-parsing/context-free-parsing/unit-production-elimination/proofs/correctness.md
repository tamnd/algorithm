---
title: ELIMINATE-UNITS returns a grammar without unit productions in which every nonterminal derives the same terminal strings, and it stops
proves: [correctness, termination]
status: full
---

We use the notation of the [context-free grammar](/context-free-grammar/) page and the pseudocode ELIMINATE-UNITS of the page. $G = (V, \Sigma, P, S)$ is any grammar, with empty productions and cycles of unit productions allowed. A unit production is $B \to C$ with $C \in V$. Write $B \Rightarrow_u C$ for one step with a unit production, and $\Rightarrow_u^*$ for zero or more such steps; $(A, B)$ is a unit pair when $A \Rightarrow_u^* B$. $P'$ is the set built by line L6.

## Lemma 1: the search finds the unit pairs and stops

Fix $A$. Each iteration of lines L4 and L5 pops one element of $W$, and an element is pushed only when it is added to $U$, which happens at most once for each nonterminal. So there are at most $|V|$ iterations, each of which looks at the unit productions of one nonterminal, and the loop stops.

*Every element of $U$ forms a unit pair with $A$.* $A \Rightarrow_u^* A$ by zero steps. If $C$ is added while $B$ is popped, then $B \in U$, so $A \Rightarrow_u^* B$ by induction on the order of insertion, and $B \to C \in P$ gives $A \Rightarrow_u^* C$.

*Every unit pair $(A, C)$ has $C \in U$.* By induction on the number $m$ of steps of $A \Rightarrow_u^m C$. For $m = 0$, $C = A \in U$. For $m > 0$, $A \Rightarrow_u^{m-1} B \Rightarrow_u C$. By induction, $B \in U$; every element of $U$ is pushed on $W$ once and popped once before the loop ends, and when $B$ is popped, line L5 adds $C$ unless it is already in $U$. $\square$

## Lemma 2: no unit productions

Line L6 adds $A \to \alpha$ only for a production $B \to \alpha$ of $P$ that is not a unit production. So no production of $P'$ is a unit production. $\square$

## Lemma 3: derivations in $G'$ are derivations in $G$

If $A \to \alpha \in P'$, it was added for some $B \in U$ with $B \to \alpha \in P$, and by Lemma 1, $A \Rightarrow_u^* B$ in $G$. So $A \Rightarrow^*_G B \Rightarrow_G \alpha$. Replacing each step $\gamma A \delta \Rightarrow_{G'} \gamma \alpha \delta$ of a derivation in $G'$ by the steps $\gamma A \delta \Rightarrow^*_G \gamma B \delta \Rightarrow_G \gamma \alpha \delta$ gives a derivation in $G$ with the same start and end. So $L_{G'}(X) \subseteq L_G(X)$ for every nonterminal $X$. $\square$

## Lemma 4: derivations of terminal strings in $G$ have counterparts in $G'$

**Claim.** If $X \Rightarrow^m_G w$ with $X \in V$ and $w \in \Sigma^*$, then $X \Rightarrow^*_{G'} w$.

*Proof.* By strong induction on $m \ge 1$. Write the derivation as a leftmost one; this does not change $m$. Its first steps rewrite only the leftmost nonterminal, so it starts with some number $k \ge 0$ of unit steps $X = X_0 \Rightarrow_u X_1 \Rightarrow_u \cdots \Rightarrow_u X_k$ followed by a step $X_k \Rightarrow \alpha$ with a production that is not a unit production. Such a step exists: the derivation ends in a terminal string, and a unit step leaves a single nonterminal. So $X \Rightarrow^k_u X_k$, $(X, X_k)$ is a unit pair, and by Lemma 1 and line L6, $X \to \alpha \in P'$.

The rest of the derivation is $\alpha \Rightarrow^{m - k - 1}_G w$. By the splitting lemma of [derivations](/derivation/), write $\alpha = Y_1 \cdots Y_r$ and $w = w_1 \cdots w_r$ with $Y_i \Rightarrow^{m_i}_G w_i$ and $\sum m_i = m - k - 1 < m$. For a terminal $Y_i$, $w_i = Y_i$. For a nonterminal $Y_i$, $m_i \ge 1$ and $m_i < m$, so $Y_i \Rightarrow^*_{G'} w_i$ by the induction hypothesis. Then $X \Rightarrow_{G'} Y_1 \cdots Y_r \Rightarrow^*_{G'} w_1 \cdots w_r = w$. If $r = 0$, then $\alpha = \varepsilon = w$ and the single step is enough. $\square$

## Theorem

For every $X \in V$, $L_{G'}(X) = L_G(X)$; in particular $L(G') = L(G)$. $G'$ has no unit production, and ELIMINATE-UNITS stops after $|V|$ searches, each of at most $|V|$ iterations, and line L6, which writes at most $|U| \le |V|$ copies of each non-unit production.

*Proof.* Lemmas 3 and 4 give the two inclusions, Lemma 2 the absence of unit productions, and Lemma 1 the bound on each search. $\square$

## Remark on the parse trees

The proof of Lemma 4 maps each parse tree of $G$ to a parse tree of $G'$ with the same yield, by collapsing each maximal chain of unit steps into the first node of the chain. Every tree of $G'$ is the image of some tree of $G$, by Lemma 3 applied node by node. So each sentence has at most as many parse trees in $G'$ as in $G$.
