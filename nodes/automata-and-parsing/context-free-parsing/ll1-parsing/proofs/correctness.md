---
title: LL1-PARSE stops in linear time and accepts exactly the sentences of an LL(1) grammar, with their parse trees
proves: [correctness]
status: full
---

**Statement.** Let $G = (V, \Sigma, R, S)$ be a grammar in which every nonterminal derives some terminal string, and let $M$ be the table built from $G$ as on the [LL parse table](/ll-parse-table/) page, with no cell holding two productions. Then for every input $w = a_1 \cdots a_n$:

1. LL1-PARSE stops after at most $c \cdot (n + 1)$ steps, where $c$ depends only on $G$;
2. it accepts if and only if $w \in L(G)$, and then it returns a parse tree of $w$ with root $S$;
3. if it reports an error at $a_i$ (with $a_{n+1} = \$$), then $a_1 \cdots a_{i-1}$ is a prefix of a sentence of $L(G)$, and $a_1 \cdots a_i$ is not when $i \le n$.

**Setup.** Write $\mathrm{FIRST}$, $\mathrm{FOLLOW}$ and $\mathrm{PREDICT}$ for the sets as defined, and $\mathrm{FOLLOW}_M$, $\mathrm{PREDICT}_M$ for the sets that BUILD computes. The LL parse table page proves that the computed nullable set and FIRST sets are exact and that $\mathrm{FOLLOW}_M(A) \supseteq \mathrm{FOLLOW}(A)$ for every $A$. So $\mathrm{PREDICT}_M(p) \supseteq \mathrm{PREDICT}(p)$ for every production $p$, and the cell $M[A, a]$ contains every production $p$ of $A$ with $a \in \mathrm{PREDICT}(p)$. Since no cell has two productions, two different productions of one nonterminal have disjoint PREDICT sets.

The *partial tree* at a moment of the run is the tree below the dummy root built so far: each expanded nonterminal is an inner node, each matched token is a leaf, and each stack entry other than $\$$ is a *slot*, a leaf that will receive the subtree of its symbol. The *start index* of an inner node is the number of tokens matched before it was expanded.

**Step 1: the invariant.** At each test of line L4, after $i - 1$ tokens have been matched, let $\gamma$ be the string of the symbols on the stack above $\$$, read from the top. Then the partial tree has the root $S$, its leaves from left to right are $a_1, \ldots, a_{i-1}$ followed by the slots of $\gamma$ (and $\varepsilon$ marks for empty right sides), every inner node uses a production of $R$, and so $S \Rightarrow_{lm}^* a_1 \cdots a_{i-1} \gamma$.

At the start the tree is the slot $S$ and the claim holds. A match (lines L6 to L8) turns the top slot, a terminal equal to $a_i$, into a matched leaf; the matched prefix grows by $a_i$ and $\gamma$ loses its first symbol. An expansion (lines L10 to L13) by $X \to Y_1 \cdots Y_k$ turns the top slot $X$ into an inner node with the slots $Y_1, \ldots, Y_k$, and replaces the first symbol $X$ of $\gamma$ by $Y_1 \cdots Y_k$. Every slot to the left of the top slot was already a matched leaf, so the step rewrites the leftmost nonterminal of $a_1 \cdots a_{i-1} \gamma$ and is a leftmost step.

**Step 2: acceptance gives a parse tree.** The parser accepts at line L5 only when $\$$ is on top, so $\gamma = \varepsilon$, and $i = n + 1$. By Step 1 the tree has root $S$, uses only productions of $R$, has no slots left, and its leaves spell $a_1 \cdots a_n = w$. So it is a parse tree of $w$, and $w \in L(G)$.

**Step 3: sentences are accepted.** Let $w \in L(G)$ and fix a parse tree $t$ of $w$. Claim: as long as the parser runs, the partial tree is the part of $t$ made of the nodes that have been expanded or matched, together with slots for the children of these nodes that have not, and the next node of $t$ in preorder is the top slot. This holds at the start. Suppose it holds and the top slot is the node $x$ of $t$, with the label $X$, and $i - 1$ tokens matched.

- If $X$ is a terminal, it is the leaf of $t$ after $a_1 \cdots a_{i-1}$ in preorder, so $X = a_i$ and the parser matches it.
- If $X$ is a nonterminal, let $p = X \to \alpha$ be the production of $x$ in $t$, and let $a_i \cdots a_{j-1}$ be the yield of the subtree of $x$; it starts at $a_i$ because every leaf before $x$ in preorder is one of $a_1, \ldots, a_{i-1}$. If $j > i$, then $\alpha \Rightarrow^* a_i \cdots a_{j-1}$ and $a_i \in \mathrm{FIRST}(\alpha)$. If $j = i$, then $\alpha \Rightarrow^* \varepsilon$, and expanding every node of $t$ except the subtree of $x$ gives $S \$ \Rightarrow^* a_1 \cdots a_{i-1} X a_i \cdots a_n \$$, so $a_i \in \mathrm{FOLLOW}(X)$, where $a_{n+1} = \$$. In both cases $a_i \in \mathrm{PREDICT}(p)$, so $M[X, a_i] = p$ and the parser expands $x$ with the children it has in $t$.
- If the top is $\$$, all nodes of $t$ have been processed, all $n$ leaves matched, and the parser accepts.

Each step processes a new node of the finite tree $t$, so the parser accepts $w$ after one step for each node of $t$ and one final step.

**Step 4: an LL(1) grammar is not left-recursive.** Claim: no nonterminal $A$ that is reachable from $S$ has a derivation $A \Rightarrow^+ \beta A \delta$ with $\beta \Rightarrow^* \varepsilon$.

Suppose one does. Following the path from the root to the inner $A$ in the tree of this derivation gives nonterminals $A_0 = A, A_1, \ldots, A_k = A$ with $k \ge 1$ and productions $p_j = A_j \to \beta_j A_{j+1} \delta_j$ with $\beta_j \Rightarrow^* \varepsilon$, indices taken modulo $k$. Each $A_j$ is reachable from $S$. Since $A_j \Rightarrow^* A_{j+1} \delta_j$, we have $\mathrm{FIRST}(A_{j+1}) \subseteq \mathrm{FIRST}(A_j)$, and around the cycle all the sets $\mathrm{FIRST}(A_j)$ are equal to one set $F$. Moreover $F \subseteq \mathrm{FIRST}(\beta_j A_{j+1} \delta_j) \subseteq \mathrm{PREDICT}(p_j)$. Going once around the cycle from $A_j$ gives $A_j \Rightarrow^+ A_j \zeta_j$, where $\zeta_j$ is a string that contains $\delta_j$.

Among all complete trees whose root is one of $A_0, \ldots, A_{k-1}$, choose one of least height; say its root is $A_j$, its root production is $q$, and its yield is $x \in \Sigma^*$. If $q = p_j$, the child $A_{j+1}$ of the root would be the root of a complete tree of smaller height; so $q \ne p_j$.

- If $x \ne \varepsilon$, its first token $a$ is in $\mathrm{FIRST}(A_j) = F \subseteq \mathrm{PREDICT}(p_j)$, and in $\mathrm{FIRST}$ of the right side of $q$, so in $\mathrm{PREDICT}(q)$. Two productions of $A_j$ share $a$, a contradiction.
- If $x = \varepsilon$, the right side of $q$ is nullable and $\mathrm{FOLLOW}(A_j) \subseteq \mathrm{PREDICT}(q)$. Since $A_j$ is reachable, $S \$ \Rightarrow^* u A_j \rho \$$ for some $u, \rho$, and $\rho \$$ derives a terminal string because every symbol is productive, so $\mathrm{FOLLOW}(A_j)$ is not empty. If $\zeta_j$ is not nullable, it derives a nonempty terminal string; let $b$ be its first token. Then $b \in \mathrm{FIRST}(A_j)$, because $A_j \Rightarrow^+ A_j \zeta_j \Rightarrow^* \zeta_j$, and $b \in \mathrm{FOLLOW}(A_j)$, because $S \$ \Rightarrow^* u A_j \zeta_j \rho \$$. So $b \in \mathrm{PREDICT}(p_j) \cap \mathrm{PREDICT}(q)$, a contradiction. If $\zeta_j$ is nullable, then $\delta_j$ is nullable, $A_{j+1} \Rightarrow^* A_j \zeta' \Rightarrow^* \varepsilon$ for a part $\zeta'$ of $\zeta_j$, and $\beta_j$ is nullable; so the right side of $p_j$ is nullable and $\mathrm{PREDICT}(p_j) \supseteq \mathrm{FOLLOW}(A_j)$, which meets $\mathrm{PREDICT}(q)$, a contradiction.

**Step 5: the partial tree is small.** Let $r \ge 2$ be at least the length of every right side, and let $m \le n$ be the number of matched tokens at some moment. Two facts about a path from an inner node $u$ down to an inner node $v$ of the partial tree with the same start index:

- every node to the left of the path inside the subtree of $u$ has been completed without matching a token, so its yield is $\varepsilon$; reading the productions along the path gives $X_u \Rightarrow^+ \beta X_v \delta$ with $\beta \Rightarrow^* \varepsilon$;
- so by Step 4, the labels on such a path are distinct, and the path has at most $|V|$ inner nodes.

Call an inner node *heavy* if its subtree contains a matched token, and *light* otherwise. Consider the tree formed by the heavy nodes and the $m$ matched leaves. A heavy node with one heavy or matched child has all its other children to the left of that child light and complete with yield $\varepsilon$, so it has the same start index as that child. Hence each maximal chain of heavy nodes with one such child has at most $|V|$ nodes. There are at most $m - 1$ heavy nodes with two or more such children, and at most $2m - 1$ chains, one above each matched leaf or branching node. So there are at most $(m - 1) + |V| (2m - 1) \le (2|V| + 1) m$ heavy nodes. A light node has no matched leaf below it, so all inner nodes of a maximal light subtree have its start index, and by the second fact the subtree has height at most $|V|$ and at most $r^{|V|}$ inner nodes. The roots of maximal light subtrees are the root of the tree or children of heavy nodes, so there are at most $r (2|V| + 1) m + 1$ of them. In total the partial tree has at most $c_0 (m + 1)$ inner nodes, with $c_0 = (2|V| + 1)(1 + r^{|V| + 1})$.

**Step 6: termination and the bound.** Each step of the parser is a match, of which there are at most $n$, an expansion, which creates an inner node, or the final step. By Step 5 there are at most $c_0 (n + 1)$ expansions, so the parser stops after at most $c \cdot (n + 1)$ steps with $c = c_0 + 2$. This proves part 1.

**Step 7: rejection.** If $w \notin L(G)$, the parser stops by Step 6 and cannot accept by Step 2, so it reports an error. With Step 3 this proves part 2.

**Step 8: the valid prefix property.** Suppose the parser reports an error at $a_i$. By Step 1, $S \Rightarrow^* a_1 \cdots a_{i-1} \gamma$, and $\gamma$ derives some terminal string $z$ because every symbol is productive; so $a_1 \cdots a_{i-1} z \in L(G)$. Now let $i \le n$ and suppose $a_1 \cdots a_i z' \in L(G)$ for some $z'$. Until it matches $a_i$, the parser looks only at the tokens $a_1, \ldots, a_i$, so it makes the same moves on $w$ and on $a_1 \cdots a_i z'$. On the second input it never reports an error by Step 3, so it matches $a_i$ on both inputs, and it cannot report an error at $a_i$ on $w$. This proves part 3. $\blacksquare$
