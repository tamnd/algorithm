---
title: The classical conversion gives an equivalent grammar in Greibach normal form
proves: [correctness]
status: full
---

We use the pseudocode of the page and the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol. The input is $G = (V, \Sigma, P, S)$. A production is *in form* if it is $A \to a B_1 \cdots B_k$ with $a \in \Sigma$, $k \ge 0$ and all $B_i$ nonterminals. For a grammar $H$ and a nonterminal $X$ of $H$ write $L_H(X) = \{w \in \Sigma^* : X \Rightarrow_H^* w\}$.

**Theorem.** The algorithm ends and returns a grammar $G'$ with $L(G') = L(G)$ in which every production is in form, except $S_0 \to \varepsilon$ when $\varepsilon \in L(G)$, and then $S_0$ is on no right side.

The proof has three parts: the steps that keep the language, the shape of the productions, and the end of the loops.

## Part 1: the steps keep the language

**Line L2.** Let $G_1$ be the grammar after line L2. The three removals are the standard ones, done in the order $\varepsilon$-productions, unit productions, useless symbols.

- *$\varepsilon$-productions.* Let $\mathcal{N}$ be the set of nullable nonterminals. Replace each production $A \to X_1 \cdots X_k$ by all productions $A \to \alpha$ where $\alpha \ne \varepsilon$ comes from $X_1 \cdots X_k$ by deleting some of the $X_i$ that are in $\mathcal{N}$. Each new production $A \to \alpha$ is simulated by the old production and derivations $X_i \Rightarrow^* \varepsilon$ for the deleted $X_i$, so no new nonempty string is derived. Conversely, take a parse tree of a nonempty $w$ from $A$ in the old grammar. Delete every subtree whose frontier is empty; its root is nullable. A node keeps at least one child, because its frontier is nonempty. The node $A \to X_1 \cdots X_k$ with some children deleted is a new production $A \to \alpha$ with $\alpha \ne \varepsilon$. So $L(A)$ is the same up to $\varepsilon$ for every $A$, and the new grammar has no $\varepsilon$-production.
- *Unit productions.* For each $A$, let $U(A)$ be the set of $B$ with $A \Rightarrow^* B$ by unit productions only. Replace all productions by $A \to \alpha$ for $B \in U(A)$ and $B \to \alpha$ a non-unit production. A new production is simulated by a chain of unit steps and one old production. Conversely, in a parse tree, each maximal chain of nodes joined by unit productions ends at a node with a non-unit production; contract the chain into one node. So the languages do not change, and no unit production remains. No $\varepsilon$-production appears, because only non-unit productions are copied.
- *Useless symbols.* First delete the nonterminals that derive no terminal string, and every production that contains one. Then delete the nonterminals not reachable from $S$. A parse tree of a terminal string uses only symbols that derive terminal strings and that are reachable from its root, so $L(S)$ does not change. If $S$ derives no terminal string, $L(G) \setminus \{\varepsilon\} = \emptyset$ and $G_1$ is empty.

So $L(G_1) = L(G) \setminus \{\varepsilon\}$. In $G_1$ every right side is nonempty, a right side of length 1 is a terminal, and every nonterminal derives some terminal string.

**Line L4.** Replacing a terminal $a$ in a non-first position by $T_a$ and adding $T_a \to a$ keeps every $L(A)$, because $T_a$ derives exactly $a$.

**Substitution (lines L7, L9 and L10).** Let $A \to X \gamma$ be a production with $X$ a nonterminal different from $A$, and let $X \to \delta_1 \mid \cdots \mid \delta_r$ be all productions of $X$. Replacing $A \to X \gamma$ by $A \to \delta_1 \gamma \mid \cdots \mid \delta_r \gamma$ keeps $L(Y)$ for every nonterminal $Y$. Each new production is simulated by two old ones. Conversely, in a tree of the old grammar, a node that uses $A \to X \gamma$ has a first child $X$ that uses some $X \to \delta_t$; merge the two nodes into one node that uses $A \to \delta_t \gamma$. Repeat until no node uses $A \to X \gamma$; each merge removes one node, so this ends. The productions of $X$ do not change, because $X \ne A$. Removing a duplicate production does not change the grammar as a set of productions.

**Immediate left recursion (line L8).** Let the productions of $A$ be $A \to A \alpha_1 \mid \cdots \mid A \alpha_p \mid \beta_1 \mid \cdots \mid \beta_q$, where no $\beta_k$ starts with $A$, and let $B$ be a new nonterminal. The new productions are $A \to \beta_k \mid \beta_k B$ and $B \to \alpha_t \mid \alpha_t B$. In the old grammar, a node $A$ of a parse tree starts a maximal chain of nodes along first children that use the productions $A \to A \alpha_{t_1}$, $A \to A \alpha_{t_2}$, …, $A \to A \alpha_{t_r}$ and ends at a node that uses $A \to \beta_k$; the chain derives $\beta_k \alpha_{t_r} \cdots \alpha_{t_1}$. In the new grammar, $A \Rightarrow \beta_k B \Rightarrow \beta_k \alpha_{t_r} B \Rightarrow \cdots \Rightarrow \beta_k \alpha_{t_r} \cdots \alpha_{t_1}$ (or $A \Rightarrow \beta_k$ when $r = 0$), and every use of $A$ and $B$ in a new tree has this shape. So the two grammars derive the same sentential forms from $A$ by these blocks, and replacing each block by the other one maps trees to trees in both directions. Every $L(Y)$ for an old $Y$ is kept. We need $p \ge 1$ only to create $B$, and $q \ge 1$ holds because $A$ derives a terminal string, which a tree can only do by ending its chain at some $\beta_k$.

**Line L11.** $E$ is computed on the input grammar, so $E$ is true if and only if $\varepsilon \in L(G)$. If $E$ is true, the new $S_0$ has the productions $S_0 \to \varepsilon$ and $S_0 \to \alpha$ for $S \to \alpha$, so $L(S_0) = L(S) \cup \{\varepsilon\} = L(G)$. If $E$ is false, the start symbol stays $S$ and $L(S) = L(G) \setminus \{\varepsilon\} = L(G)$.

So $L(G') = L(G)$ if the algorithm ends.

## Part 2: the shape of the productions

Let the order after line L4 be $A_1, \ldots, A_m$, with the $T_a$ at the end. Call a production *regular* if it is a single terminal, or if it has length at least 2 and every symbol after the first is a nonterminal.

**Claim 1.** After line L4 every production is regular, and every later step keeps this.

After line L2 a right side of length 1 is a terminal, and line L4 makes every non-first symbol a nonterminal. A substitution replaces $A \to X \gamma$, with $|X \gamma| \ge 2$, by $A \to \delta \gamma$ with $\delta$ regular and $\gamma$ a nonempty string of nonterminals; the result has length at least 2, and its symbols after the first are those of $\delta$ after the first and those of $\gamma$, all nonterminals. In line L8, a production $A_i \to A_i \alpha_t$ has length at least 2, so $\alpha_t$ is a nonempty string of nonterminals, and so are $\alpha_t B_i$. The productions $\beta_k$ are regular, and $\beta_k B_i$ is regular because $\beta_k$ is nonempty. $\square$

So a regular production that starts with a terminal is in form. It remains to show that every production starts with a terminal at the end.

**Claim 2.** After iteration $i$ of the loop of line L5, every production of $A_i$ starts with a terminal or with some $A_j$ with $j > i$, and the productions of $A_1, \ldots, A_i$ do not change in later iterations.

By induction on $i$. In iteration $i$, the inner loop goes through $j = 1, \ldots, i - 1$. Before step $j$, by the induction hypothesis for $j' < j$, no production of $A_i$ starts with $A_{j'}$ for $j' < j$: such a production was replaced at step $j'$ by productions that start with the first symbol of a production of $A_{j'}$, which is a terminal or an $A_k$ with $k > j'$; if $k < j$ that production was in turn replaced at step $k$, since the steps go in increasing order. After step $j$ no production starts with $A_j$, by the same argument. So after the inner loop, every production of $A_i$ starts with a terminal or with $A_k$, $k \ge i$. Line L8 removes those with $k = i$: the productions $\beta_k$ and $\beta_k B_i$ start with the first symbol of $\beta_k$, which is a terminal or $A_k$ with $k > i$. Later iterations change only $A_{i'}$ with $i' > i$ and the new $B_{i'}$. $\square$

**Claim 3.** After line L9, every production of every $A_i$ starts with a terminal.

By Claim 2, the productions of $A_m$ start with terminals. Line L9 goes from $i = m - 1$ down to 1. When it handles $A_i$, the productions of all $A_j$ with $j > i$ already start with terminals, and every production of $A_i$ that starts with a nonterminal starts with such an $A_j$, by Claim 2. Substituting $A_j$ gives productions that start with the first symbol of a production of $A_j$, a terminal. $\square$

**Claim 4.** Every production of $B_i$ starts with some $A_k$ or with some $B_j$ with $j < i$.

The productions of $B_i$ are $\alpha_t$ and $\alpha_t B_i$, where $A_i \to A_i \alpha_t$ was a production when line L8 handled $A_i$. By Claim 1, $\alpha_t$ is a nonempty string of nonterminals, and the nonterminals that existed at that time were the $A_k$ and the $B_j$ created at an earlier iteration, so with $j < i$. Lines L9 and L10 do not change which nonterminal starts a production of $B_i$ before line L10 handles $B_i$. $\square$

## Part 3: the loops end and finish the form

The loops of lines L5, L6 and L9 are bounded. Each substitution step is finite, because $X$ has finitely many productions.

For line L10, the implementation keeps the $B_i$ in a queue. It takes the first $B_i$; if a production of $B_i$ starts with a $B_j$ that is still in the queue, it puts $B_i$ back at the end, and otherwise it substitutes the leading nonterminal of each production of $B_i$ and removes $B_i$ from the queue.

**Claim 5.** The queue becomes empty, and then every production of every $B_i$ starts with a terminal.

While the queue is not empty, let $B_i$ be the element with the smallest index. By Claim 4 its productions start with an $A_k$ or with a $B_j$ with $j < i$, and no such $B_j$ is in the queue. So within one pass through the queue, $B_i$ is handled and removed. The queue has at most $m$ elements, so it is empty after at most $m$ passes. When $B_i$ is handled, each production starts with an $A_k$, whose productions start with terminals by Claim 3, or with a $B_j$ that has left the queue, whose productions start with terminals by induction on the order of removal. One substitution therefore makes every production of $B_i$ start with a terminal, and $B_i$ does not change afterwards. $\square$

By Claims 1, 3 and 5 every production of $A_1, \ldots, A_m$ (including the $T_a$) and of every $B_i$ is regular and starts with a terminal, so it is in form. Line L11 adds $S_0 \to \varepsilon$ and copies of the productions of $S$, which are in form; $S_0$ is a fresh name and occurs on no right side. With Part 1, this proves the theorem. $\blacksquare$
