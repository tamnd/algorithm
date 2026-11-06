---
title: The LL(k) tables are conflict-free exactly for LL(k) grammars, and LLK-PARSE accepts exactly the sentences in linear time with exact error positions
proves: [correctness]
status: full
---

**Statement.** Let $G = (V, \Sigma, R, S)$ be a grammar in which every nonterminal derives some terminal string, and let $k \ge 1$. Then:

1. LLK-TABLES reports a conflict if and only if $G$ is not LL(k);
2. if it reports none, then for every input $w = a_1 \cdots a_n$, LLK-PARSE stops after at most $c \cdot (n + 1)$ steps, where $c$ depends only on $G$ and $k$;
3. it accepts if and only if $w \in L(G)$, and then it returns a parse tree of $w$ with root $S$;
4. if it reports an error at position $p$ (with $p = n + 1$ meaning the end of the input), then $a_1 \cdots a_{p-1}$ is a prefix of a sentence, and $a_1 \cdots a_p$ is not when $p \le n$.

**Setup.** For $\alpha \in (V \cup \Sigma)^*$ write $L(\alpha)$ for the set of terminal strings that $\alpha$ derives; by the hypothesis, $L(\alpha) \neq \emptyset$ for every $\alpha$. The sets computed at line L12 are the least fixed point of $F_A = \bigcup_{A \to Y_1 \cdots Y_m} F_{Y_1} \oplus_k \cdots \oplus_k F_{Y_m}$, with $F_a = \{a\}$ for a terminal. They equal $\mathrm{FIRST}_k(A)$. Each element of the fixed point is $\mathrm{FIRST}_k$ of a derived string, by induction on the iteration. Conversely, by induction on the height of a parse tree with root $A$ and yield $x$, $\mathrm{FIRST}_k(x)$ enters the fixed point, since $\mathrm{FIRST}_k(x_1 \cdots x_m)$ depends only on the $\mathrm{FIRST}_k(x_j)$. The operation $\oplus_k$ is associative, and $\mathrm{FIRST}_k(\alpha \beta) = \mathrm{FIRST}_k(\alpha) \oplus_k \mathrm{FIRST}_k(\beta)$. So the set $U$ of line L15 is $\mathrm{FIRST}_k(Y_1 \cdots Y_m) \oplus_k L$, and the set $L_j$ of line L17 is $\mathrm{FIRST}_k(Y_{j+1} \cdots Y_m) \oplus_k L$. Every $U$ is nonempty because every symbol is productive.

**Step 1: every table comes from a left-sentential form.** Claim: for every table $T(A, L)$ that LLK-TABLES creates, there is a leftmost derivation $S \Rightarrow_{lm}^* u A \alpha$ with $u \in \Sigma^*$ and $\mathrm{FIRST}_k(\alpha) = L$. For $T(S, \{\varepsilon\})$ take $u = \alpha = \varepsilon$. If $T(Y_j, L_j)$ is created while $T(A, L)$ is filled, with the production $A \to Y_1 \cdots Y_m$ and a form $u A \alpha$ for $T(A, L)$, then
$$u A \alpha \Rightarrow_{lm} u Y_1 \cdots Y_m \alpha \Rightarrow_{lm}^* u z_1 \cdots z_{j-1} Y_j Y_{j+1} \cdots Y_m \alpha,$$
where each $Y_i$ with $i < j$ is derived to some $z_i \in L(Y_i)$, leftmost. The context is $\alpha' = Y_{j+1} \cdots Y_m \alpha$, and $\mathrm{FIRST}_k(\alpha') = \mathrm{FIRST}_k(Y_{j+1} \cdots Y_m) \oplus_k L = L_j$.

**Step 2: the stack invariant.** Read the stack from the top as $(X_1, t_1), \ldots, (X_q, t_q)$. Claim: at each test of line L2, whenever $X_j \in V$, its table is $t_j = T(X_j, \mathrm{FIRST}_k(X_{j+1} \cdots X_q))$. Moreover, if $i - 1$ tokens have been matched, the tree built so far is the tree of a leftmost derivation $S \Rightarrow_{lm}^* a_1 \cdots a_{i-1} X_1 \cdots X_q$, with one slot for each stack entry.

At the start the stack is $(S, T(S, \{\varepsilon\}))$. A match removes the top terminal; the matched prefix grows by it, and the other entries keep their tables and the symbols below them. Now take an expansion of $(X_1, T(X_1, L))$ with $L = \mathrm{FIRST}_k(X_2 \cdots X_q)$, by $X_1 \to Y_1 \cdots Y_m$. It pushes $Y_j$ with the table $T(Y_j, L_j)$, where
$$L_j = \mathrm{FIRST}_k(Y_{j+1} \cdots Y_m) \oplus_k \mathrm{FIRST}_k(X_2 \cdots X_q) = \mathrm{FIRST}_k(Y_{j+1} \cdots Y_m X_2 \cdots X_q).$$
That is the claim for the new stack. The step rewrites the leftmost nonterminal of $a_1 \cdots a_{i-1} X_1 \cdots X_q$, so it is a leftmost step.

A consequence: when $X_1 \in V$ is on top with the table $T(X_1, L)$, the keys of the table are the union over the productions $X_1 \to \beta$ of $\mathrm{FIRST}_k(\beta) \oplus_k L$, which is $\mathrm{FIRST}_k(X_1 \cdots X_q)$.

**Step 3: acceptance gives a parse tree.** The parser accepts only when the stack is empty and $i = n + 1$. By Step 2 the tree is then the tree of a derivation $S \Rightarrow_{lm}^* a_1 \cdots a_n$, so it is a parse tree of $w$, and $w \in L(G)$.

**Step 4: sentences are accepted.** Assume no conflict, let $w \in L(G)$, and fix a parse tree $t$ of $w$. As in the LL(1) case, the claim is that the parser expands the nodes of $t$ in preorder with their productions in $t$. Suppose that so far it has done so, and that the top slot is the node $x$ of $t$, with $i - 1$ tokens matched. The stack then holds the slots of $t$ that come after the matched leaves, in preorder of the remaining frontier. If $x$ is a terminal leaf, it is $a_i$ and the parser matches it. If $x$ is labeled $X_1 \in V$ and uses $X_1 \to \beta$ in $t$, the subtrees of the stack slots spell $a_i \cdots a_n$. So $a_i \cdots a_n \in L(\beta X_2 \cdots X_q)$, and $u = \mathrm{FIRST}_k(a_i \cdots a_n)$, the lookahead of line L7, lies in $\mathrm{FIRST}_k(\beta) \oplus_k L$ with $L = \mathrm{FIRST}_k(X_2 \cdots X_q)$ by Step 2. Line L18 then put $X_1 \to \beta$ into $T(X_1, L)[u]$. Since there is no conflict, it is the only production there, and the parser expands $x$ as $t$ does. When all nodes of $t$ are processed, the stack is empty, $i = n + 1$, and the parser accepts.

**Step 5: conflicts are exactly the violations of LL(k).** Suppose LLK-TABLES reports a conflict in $T(A, L)$, between productions $A \to \beta$ and $A \to \gamma$ that share a lookahead $u$. Take the form $u_0 A \alpha$ of Step 1, with $\mathrm{FIRST}_k(\alpha) = L$. Then $u \in \mathrm{FIRST}_k(\beta \alpha) \cap \mathrm{FIRST}_k(\gamma \alpha)$, so there are $x \in L(\beta \alpha)$ and $y \in L(\gamma \alpha)$ with $\mathrm{FIRST}_k(x) = \mathrm{FIRST}_k(y) = u$, and $G$ is not LL(k).

Conversely, suppose there is no conflict but $G$ is not LL(k). Take two leftmost derivations $S \Rightarrow_{lm}^* u_0 A \alpha \Rightarrow_{lm} u_0 \beta \alpha \Rightarrow_{lm}^* u_0 x$ and $S \Rightarrow_{lm}^* u_0 A \alpha \Rightarrow_{lm} u_0 \gamma \alpha \Rightarrow_{lm}^* u_0 y$ with $\beta \ne \gamma$ and $\mathrm{FIRST}_k(x) = \mathrm{FIRST}_k(y) = u$. Run the parser on $u_0 x \in L(G)$. By Step 4 it follows the tree of the first derivation in preorder, so at some point it has matched $u_0$ and has $A$ on top, with the stack $A \alpha$ and the table $T(A, \mathrm{FIRST}_k(\alpha))$ by Step 2. Both $\mathrm{FIRST}_k(\beta \alpha)$ and $\mathrm{FIRST}_k(\gamma \alpha)$ contain $u$, so line L16 saw a conflict in this table, a contradiction. This proves part 1.

**Step 6: no left recursion.** Assume no conflict, so that $G$ is LL(k) by Step 5. Claim: no nonterminal $A$ that is reachable from $S$ has a derivation $A \Rightarrow^+ \beta A \delta$ with $\beta \Rightarrow^* \varepsilon$.

Suppose one does. Along the path to the inner $A$ we get nonterminals $A_0 = A, A_1, \ldots, A_r = A$, with $r \ge 1$, and productions $p_j = A_j \to \beta_j A_{j+1} \delta_j$ with $\beta_j \Rightarrow^* \varepsilon$, indices modulo $r$. Each $A_j$ is reachable from $S$, because $A$ is and $A \Rightarrow^* \cdots A_j \cdots$. Among all complete trees whose root is one of the $A_j$, choose one of least height, with root $A_j$, root production $q$ and yield $x$. Then $q \ne p_j$, since otherwise its child $A_{j+1}$ would root a lower complete tree.

Going once around the cycle from $A_j$ with $p_j$ first, and deriving each $\beta$ to $\varepsilon$ before the next step, gives $A_j \Rightarrow_{lm}^+ A_j \zeta$ for a string $\zeta$. Pick $z \in L(\zeta)$, nonempty if possible. Since $A_j$ is reachable and every symbol is productive, some leftmost derivation reaches $u_0 A_j \alpha$ with $u_0 \in \Sigma^*$; let $y \in L(\alpha)$. For any $m \ge 0$, $S \Rightarrow_{lm}^* u_0 A_j \zeta^m \alpha$, and from this form:

- applying $q$ first gives $u_0 x z^m y$;
- applying $p_j$ first gives $u_0 A_j \zeta^{m+1} \alpha \Rightarrow^* u_0 x z^{m+1} y$.

If $z \neq \varepsilon$, take $m = k$; then both strings after $u_0$ start with $x z^k$, which has length at least $k$. If $z = \varepsilon$, both strings are $u_0 x y$. Either way the first $k$ tokens after $u_0$ agree while the productions $q$ and $p_j$ differ, against the LL(k) condition.

**Step 7: the tree is small, and the parser stops.** Steps 5 and 6 of the proof for [LL(1) parsing](/ll1-parsing/) use only the absence of the left recursion of Step 6, and they apply word for word. When $m$ tokens have been matched, every downward path between inner nodes with the same start index has distinct labels, because all labels in the tree are reachable from $S$. So the partial tree has at most $c_0 (m + 1)$ inner nodes, with $c_0 = (2|V| + 1)(1 + r_0^{|V| + 1})$ and $r_0 \ge 2$ at least the length of every right side. Each step is a match (at most $n$), an expansion (one new inner node) or the last step, so there are at most $c \cdot (n + 1)$ steps with $c = c_0 + 2$. This is part 2. If $w \notin L(G)$, the parser stops and cannot accept by Step 3, so it reports an error. With Step 4 this is part 3.

**Step 8: the inspected tokens stay consistent.** Let $h$ be the end of the furthest lookahead used so far: the largest $\min(i' + k - 1, n)$ over the expansions done so far at positions $i'$, or $0$ if there were none. Claim: at each test of line L2, with stack $\gamma = X_1 \cdots X_q$ and $i - 1$ tokens matched, $h \le i + k - 1$, and $a_i \cdots a_h$ is a prefix of some element of $\mathrm{FIRST}_k(\gamma)$ (the empty string when $h < i$).

The bound on $h$ holds because the positions $i'$ never exceed $i$. After an expansion at $i$ with the lookahead $u = a_i \cdots a_{\min(i+k-1, n)}$, we have $h = \min(i + k - 1, n)$. The new stack $\beta X_2 \cdots X_q$ was chosen with $u \in \mathrm{FIRST}_k(\beta) \oplus_k \mathrm{FIRST}_k(X_2 \cdots X_q)$, which is $\mathrm{FIRST}_k$ of the new stack. After a match of $X_1 = a_i$, let $a_i \cdots a_h$ be a prefix of $v = \mathrm{FIRST}_k(a_i z)$ with $z \in L(X_2 \cdots X_q)$. Then $a_{i+1} \cdots a_h$ is a prefix of $\mathrm{FIRST}_{k-1}(z)$, which is a prefix of $\mathrm{FIRST}_k(z) \in \mathrm{FIRST}_k(X_2 \cdots X_q)$. Since every $\gamma$ is productive, $\mathrm{FIRST}_k(\gamma)$ is never empty, which covers $h < i$.

**Step 9: the valid prefix property.** Suppose the parser reports an error at position $p$, in configuration $(i, \gamma)$. Every element $v \in \mathrm{FIRST}_k(\gamma)$ is $\mathrm{FIRST}_k(z)$ for some $z \in L(\gamma)$, and $a_1 \cdots a_{i-1} z \in L(G)$ by Step 2. We now check the three places where an error can be reported.

- **Line L5.** Here $p = i$ and $\gamma$ starts with the terminal $X_1$. The prefix $a_1 \cdots a_{i-1}$ extends to a sentence.
- **Line L8.** Here $p = i + d$, where $u$ and some key $v \in \mathrm{FIRST}_k(\gamma)$ share $d$ tokens. The prefix $a_1 \cdots a_{p-1}$ is $a_1 \cdots a_{i-1}$ followed by the first $d$ tokens of $v$, so it starts a sentence. By Step 8, $a_i \cdots a_h$ is a prefix of a key, so $d \ge h - i + 1$ and $p > h$.
- **Line L11.** Here $\gamma = \varepsilon$ and $p = i$; then $a_1 \cdots a_{i-1} \in L(G)$. If the last decision ended at $h \ge i$, Step 8 with $\gamma = \varepsilon$ gives $a_i \cdots a_h = \varepsilon$, so $h < i = p$.

In all three cases $p > h$, because at line L5 we have $h \le i - 1$: if $h \ge i$, then $a_i$ is the first token of an element of $\mathrm{FIRST}_k(X_1 \cdots)$, which starts with $X_1$, so $X_1 = a_i$ and there is no error.

Now let $p \le n$ and suppose some sentence $s$ starts with $a_1 \cdots a_p$. Every expansion so far looked at tokens with positions at most $h < p$, and every match at positions below $i \le p$. The parser therefore makes the same moves on $s$ as on $w$ and reaches the same configuration $(i, \gamma)$. On $s$ it accepts by Step 4, and the rest of its run derives the rest of $s$ from $\gamma$, so $\mathrm{FIRST}_k(s_i s_{i+1} \cdots) \in \mathrm{FIRST}_k(\gamma)$. We look at the three lines again.

- **Line L5.** On $s$ the parser matches $X_1 = s_i = a_i$, a contradiction.
- **Line L8.** On $s$ the lookahead is a key of $t$ that agrees with $u$ on its first $d + 1$ tokens, because $s$ and $w$ agree up to position $p = i + d$. This contradicts the maximality of $d$.
- **Line L11.** The stack is empty while $s$ has the token $s_p = a_p$ left, so the parser would not accept $s$.

This proves part 4. $\blacksquare$
