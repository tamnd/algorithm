---
title: The Chomsky normal form conversion keeps the language and produces Chomsky normal form
proves: [correctness]
status: full
---

Let $G = (V, \Sigma, R, S)$ with $V \cap \Sigma = \emptyset$. Write $G_1, \ldots, G_6$ for the grammars after START (L1), TERM (L2, L3), BIN (L4, L5), DEL (L6 to L8), UNIT (L9, L10) and USELESS (L11). For a grammar $H$ and a symbol $X$ let $L_H(X) = \{ w \in \Sigma^* : X \Rightarrow^*_H w \}$, with $L_H(a) = \{a\}$ for a terminal $a$. We use parse trees throughout: $w \in L_H(X)$ exactly when there is a parse tree of $H$ with root $X$ and yield $w$. All new nonterminals are fresh, so they differ from each other and from every symbol of $G$.

**Invariant 0.** $S_0$ is on no right side of any $G_i$. It is fresh, L1 puts it only on a left side, TERM and BIN rewrite right sides of $G_1$ without adding $S_0$, and DEL and UNIT only build right sides from parts of existing right sides.

**Step 1 (START).** $L_{G_1}(S_0) = L_G(S)$, and $L_{G_1}(A) = L_G(A)$ for $A \in V$.

*Proof.* By Invariant 0, a parse tree of $G_1$ contains $S_0$ at most at the root. A tree with root $A \in V$ is a tree of $G$. A tree with root $S_0$ is $S_0 \to S$ above a tree of $G$ with root $S$. $\square$

**Step 2 (TERM).** $L_{G_2}(A) = L_{G_1}(A)$ for every nonterminal $A$ of $G_1$.

*Proof.* Let $h$ replace each new $T_a$ by $a$. Every production of $G_2$ other than $T_a \to a$ is $A \to \alpha'$ with $A \to h(\alpha')$ in $G_1$. Given a tree of $G_2$ with root $A \ne T_a$, delete every node $T_a$ and attach its leaf $a$ to its parent; the result is a tree of $G_1$ with the same root and yield. Conversely, in a tree of $G_1$, replace at each node that uses a production with $|\alpha| \ge 2$ each terminal child $a$ by a node $T_a$ with the leaf $a$; the result is a tree of $G_2$. $\square$

**Step 3 (BIN).** $L_{G_3}(A) = L_{G_2}(A)$ for every nonterminal $A$ of $G_2$.

*Proof.* The new nonterminals $A_1, \ldots, A_{k-2}$ made for one production $p = A \to X_1 \cdots X_k$ are fresh for $p$, so each $A_i$ has exactly one production, $A_i \to X_{i+1} A_{i+1}$ (or $A_{k-2} \to X_{k-1} X_k$), and appears on exactly one right side, that of $A_{i-1}$ (or of $A$ for $i = 1$). In a tree of $G_3$ with an old root, every node labelled $A_1$ is therefore the right child of a node $A$ that uses $A \to X_1 A_1$, and below it the chain continues to $A_{k-2}$. Contracting each such chain into one node $A$ with children $X_1, \ldots, X_k$ gives a tree of $G_2$ with the same yield. Expanding each node that uses $p$ into the chain turns a tree of $G_2$ into a tree of $G_3$. $\square$

After BIN every right side has length at most 2, and every right side of length 2 consists of two nonterminals, by TERM.

**Step 4 (DEL).** Let $N$ be the set of nullable nonterminals of $G_3$. Then for every nonterminal $A$ of $G_3$ and every $w \ne \varepsilon$, $w \in L_{G_4}(A) \iff w \in L_{G_3}(A)$. Moreover $L_{G_4}(S_0) = L_{G_3}(S_0)$.

*Proof.* ($\Rightarrow$) Every production of $G_4$ other than $S_0 \to \varepsilon$ is $A \to \alpha$ where $\alpha$ comes from a production $A \to \beta$ of $G_3$ by deleting symbols of $N$, which derive $\varepsilon$ in $G_3$. So $A \Rightarrow^*_{G_3} \alpha$, and every derivation of $G_4$ that does not use $S_0 \to \varepsilon$ is simulated in $G_3$. A derivation of $w \ne \varepsilon$ from $A$ does not use $S_0 \to \varepsilon$: if $A \ne S_0$ it never meets $S_0$, by Invariant 0, and if $A = S_0$ the production $S_0 \to \varepsilon$ yields only $\varepsilon$.

($\Leftarrow$) By induction on the height of a tree $T$ of $G_3$ with root $A$ and yield $w \ne \varepsilon$. The root uses $A \to Y_1 \cdots Y_j$ with $1 \le j \le 2$, since $j = 0$ gives the yield $\varepsilon$. Let $w = w_1 \cdots w_j$ be the yields of the children, and let $I = \{ i : w_i \ne \varepsilon \}$, which is nonempty. For $i \notin I$, $Y_i$ derives $\varepsilon$, so it is a nonterminal in $N$. For $i \in I$, $Y_i$ is a terminal with $w_i = Y_i$, or a nonterminal with $w_i \in L_{G_4}(Y_i)$ by induction. The production $A \to (Y_i)_{i \in I}$ is in $G_4$: if $I = \{1, \ldots, j\}$ it is the original nonempty production, kept by L8; if $j = 2$ and $I = \{1\}$ it was added by L7 because $Y_2 \in N$; if $I = \{2\}$, because $Y_1 \in N$. Using it at the root gives a tree of $G_4$ with yield $w$.

Finally, $\varepsilon \in L_{G_4}(S_0)$ exactly when L8 added $S_0 \to \varepsilon$, that is, when $S_0 \in N$, that is, when $\varepsilon \in L_{G_3}(S_0)$: every other production of $G_4$ has a nonempty right side, so no other derivation can yield $\varepsilon$. $\square$

After DEL the productions are $A \to B C$ with $B, C$ nonterminals, $A \to a$, unit productions $A \to B$, and possibly $S_0 \to \varepsilon$. L7 adds only right sides of length 1, and L8 removes every other $\varepsilon$-production.

**Step 5 (UNIT).** For every nonterminal $A$, $L_{G_5}(A) = L_{G_4}(A)$.

*Proof.* ($\subseteq$) A production $A \to \beta$ of $G_5$ comes from some $B \in U(A)$ with $B \to \beta$ in $G_4$, so $A \Rightarrow^*_{G_4} B \Rightarrow_{G_4} \beta$. Replacing each step of a derivation of $G_5$ by these steps gives a derivation of $G_4$.

($\supseteq$) By induction on the number of nodes of a tree $T$ of $G_4$ with root $A$ and yield $w$. Starting at the root, follow the nodes that use unit productions: $A = B_0, B_1, \ldots, B_m$, where $B_{i-1} \to B_i$ is a unit production and the node $B_m$ uses a production $B_m \to \beta$ that is not a unit production. Then $B_m \in U(A)$, so $A \to \beta$ is in $G_5$ by L10. The children of the node $B_m$ are terminals, or roots of subtrees with fewer nodes than $T$ whose yields are, by induction, derivable in $G_5$. Putting $A \to \beta$ at the root above these subtrees gives a tree of $G_5$ with yield $w$. $\square$

$U(A)$ is computed by a graph search over the unit productions, which terminates even when they form cycles. L10 copies only productions that are not unit productions, so $G_5$ has only $A \to BC$, $A \to a$ and $S_0 \to \varepsilon$. Since $S_0$ is on no right side, $S_0 \in U(A)$ only for $A = S_0$, so $S_0 \to \varepsilon$ is not copied to any other nonterminal.

**Step 6 (USELESS).** $L_{G_6}(S_0) = L_{G_5}(S_0)$.

*Proof.* $G_6$ has a subset of the productions of $G_5$, which gives $\subseteq$. Conversely, let $T$ be a tree of $G_5$ with root $S_0$ and yield $w \in \Sigma^*$. Every node $X$ of $T$ is the root of a subtree with a terminal yield, so $X$ is generating, and every production used in $T$ has a generating left side and generating right-side symbols; so it survives the first part of L11. Every node is reached from the root along edges of $T$, which use these surviving productions, so its label is reachable from $S_0$ in the grammar after the first part, and the production survives the second part. So $T$ is a tree of $G_6$. $\square$

**Theorem.** $G_6$ is in Chomsky normal form with start symbol $S_0$, and $L(G_6) = L(G)$.

*Proof.* The language: by Steps 1 to 3, $L_{G_3}(S_0) = L_G(S)$; by Step 4, $L_{G_4}(S_0) = L_{G_3}(S_0)$; by Steps 5 and 6, $L(G_6) = L_{G_5}(S_0) = L_{G_4}(S_0)$. The form: after Step 5 every production is $A \to BC$ with nonterminals $B, C$, $A \to a$, or $S_0 \to \varepsilon$; Step 6 only removes productions; and by Invariant 0, $B, C \ne S_0$. $\blacksquare$
