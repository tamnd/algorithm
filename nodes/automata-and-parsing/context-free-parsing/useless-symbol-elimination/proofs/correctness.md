---
title: TRIM keeps exactly the productions made of useful symbols, preserves the language and the parse trees, and stops in linear time
proves: [correctness, termination]
status: full
---

We use the notation of the [context-free grammar](/context-free-grammar/) page and the pseudocode TRIM of the page. $G = (V, \Sigma, P, S)$, a nonterminal may have no production, and a symbol is useful if it occurs in some derivation $S \Rightarrow^* \alpha X \beta \Rightarrow^* w$ with $w \in \Sigma^*$.

## Lemma 1: the generating pass

**Invariant.** Call a nonterminal *processed* when line L5 has added it to Gen and line L6 has run for it. Then:

(a) $\mathrm{count}[p]$ is the number of occurrences in the right side of $p$ of nonterminals that are not processed;

(b) every nonterminal on $W$ is the left side of a production whose counter is 0;

(c) every left side of a production with counter 0 is in Gen or on $W$.

Initially no nonterminal is processed, (a) holds by line L1, and line L2 puts on $W$ exactly the left sides of the productions with counter 0, which gives (b) and (c). An iteration that skips $X \in$ Gen changes nothing except removing a copy of $X$, which is in Gen, so (c) still holds. An iteration that processes $X$ decreases, by line L6, the counter of $p$ once for each occurrence of $X$ in $p$, so (a) holds with $X$ processed; every counter that reaches 0 has its left side pushed, which keeps (b) and (c). Since a nonterminal is processed only once (line L4 skips it later), no counter goes below 0.

**Termination.** Each push onto $W$ follows a counter reaching 0 (or line L2), which happens at most once per production, so at most $|P|$ elements are pushed, and the loop runs at most $|P|$ times.

**Soundness.** Every element of Gen is generating. By induction on the order of processing: $X$ was pushed for a production $X \to \alpha$ with counter 0, so by (a) all nonterminals of $\alpha$ were processed before, hence generating; terminals are generating; so $\alpha \Rightarrow^* w$ for some $w \in \Sigma^*$ and $X \Rightarrow \alpha \Rightarrow^* w$.

**Completeness.** Every generating nonterminal is in Gen at the end. Let $A \Rightarrow^* w$, and take a parse tree of $w$ from $A$ of minimum height $h \ge 1$. The root uses $p = A \to \alpha$, and each nonterminal child $B$ has a tree of height less than $h$, so by induction on $h$ it is in Gen at the end, hence processed (every element of Gen is processed in the same iteration). By (a) at the end, $\mathrm{count}[p] = 0$, and by (c) with $W$ empty, $A \in$ Gen. $\square$

## Lemma 2: the reachable pass

Let $P_1$ be the set of line L7, and say $B$ is reachable in $P_1$ if $S \Rightarrow^*_{P_1} \gamma B \delta$.

Every element of Reach is reachable in $P_1$: $S$ is, by the empty derivation, and if $A$ is reachable by $S \Rightarrow^* \gamma A \delta$ and $A \to \alpha_1 B \alpha_2 \in P_1$, then $S \Rightarrow^* \gamma \alpha_1 B \alpha_2 \delta$. Conversely, if $S \Rightarrow^*_{P_1} \gamma B \delta$ in $m$ steps, then by induction on $m$ the occurrence of $B$ was introduced by a step with a production $A \to \alpha_1 B \alpha_2 \in P_1$ applied to an occurrence of $A$ in a sentential form derived in fewer steps; $A \in$ Reach by induction, $A$ was pushed and popped once, and line L10 then added $B$ if it was not already present. Each nonterminal is pushed at most once, so the loop runs at most $|V|$ times. $\square$

## Lemma 3: the output is the set of useful productions

Call a production *useful* if some derivation $S \Rightarrow^* w$ with $w \in \Sigma^*$ uses it. Let $P'$ be the output of line L11.

*Every useful production is in $P'$.* Let $A \to \alpha$ be used in $S \Rightarrow^* \gamma A \delta \Rightarrow \gamma \alpha \delta \Rightarrow^* w$. Every symbol in a sentential form of a derivation of a terminal string derives a substring of $w$, so it is generating; hence every production used in the derivation has all its symbols in Gen by Lemma 1, and is in $P_1$. The derivation of $\gamma A \delta$ therefore uses only $P_1$, so $A$ is reachable in $P_1$, and $A \in$ Reach by Lemma 2. So $A \to \alpha \in P'$.

*Every production of $P'$ is useful.* Let $A \to \alpha \in P'$. By Lemma 2, $S \Rightarrow^*_{P_1} \gamma A \delta$, and by the definition of $P_1$ every symbol of this sentential form and of $\alpha$ is generating. Indeed, each such symbol is a symbol of a right side of a production in $P_1$, all of which are generating by the definition of $P_1$, or it is the start symbol $S$; and $S$ is the left side of the first production of the derivation, or $S = A$ when the derivation is empty, and every left side of $P_1$ is in Gen. Replacing each symbol of $\gamma \alpha \delta$ by a terminal string it derives gives $S \Rightarrow^* \gamma A \delta \Rightarrow \gamma \alpha \delta \Rightarrow^* w$. $\square$

## Theorem

$L(G') = L(G)$, every parse tree of a sentence of $G$ is a parse tree of $G'$ and conversely, and if $L(G) \ne \emptyset$, every symbol of $G'$ is useful in $G'$.

*Proof.* A parse tree of a sentence of $G$ uses only useful productions, which are in $P'$ by Lemma 3; and $P' \subseteq P$, so every tree of $G'$ is a tree of $G$. Equality of trees gives equality of languages. For the last part, every production of $P'$ is used in some derivation of a sentence in $G$; that derivation uses only useful productions, so it is a derivation in $G'$, and every symbol of the production is useful in $G'$. If $L(G) = \emptyset$, no production is useful and $P' = \emptyset$. $\square$

## Running time

Lemma 1 bounds the iterations of lines L3 to L6 by $|P|$, and the decrements of line L6 by the number of nonterminal occurrences, since each nonterminal is processed once and visits its own occurrences. Lines L1, L2 and L7 are single passes over $P$. Lemma 2 bounds the iterations of lines L9 and L10 by $|V|$, and each production of $P_1$ is visited when its left side is popped, once. Line L11 is a pass over $P_1$. With constant-time set and map operations, the total is $O(|G| + |V|)$, which is $O(|G|)$ when every nonterminal occurs in some production. The algorithm terminates on every input.
