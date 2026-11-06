---
title: The canonical LR(k) parser accepts exactly the sentences, returns their parse trees, and reports each error at the first bad token
proves: [correctness]
status: full
---

**Statement.** Let $G$ be a grammar in which every nonterminal derives some terminal string, augmented with $S' \to S$, let $k \ge 0$, and suppose that LRK-TABLES reports no conflict. Then for every input $w = a_1 \cdots a_n$:

1. if LR-PARSE returns a tree, it is a parse tree of $w$ with root $S$;
2. if $w \in L(G)$, LR-PARSE returns a tree;
3. if LR-PARSE reports an error at position $p$ (with $p = n + 1$ for the end of the input), then $a_1 \cdots a_{p-1}$ is a prefix of a sentence, and $a_1 \cdots a_p$ is not when $p \le n$;
4. LR-PARSE stops after $O(n + 1)$ steps.

**Setup.** As on the LL(k) parsing page, the computed $\mathrm{FIRST}_k$ sets are exact, $\mathrm{FIRST}_k(\alpha \beta) = \mathrm{FIRST}_k(\alpha) \oplus_k \mathrm{FIRST}_k(\beta)$, and $L(\alpha) \ne \emptyset$ for every string $\alpha$. For a string $\gamma$ of grammar symbols, let $\mathrm{st}(\gamma)$ be the state reached from $I_0$ by GOTO along $\gamma$, when it exists. Each stack entry is a symbol $X$, a tree with root $X$ and a state. A shift pushes $\mathrm{GOTO}[s, a_i]$ and a reduction pushes $\mathrm{GOTO}[s', A]$, so the state on top is always $\mathrm{st}(\gamma)$, where $\gamma$ is the string of stack symbols. Every kernel item $[A \to \beta_1 X \cdot \beta_2, u]$ of a GOTO state comes from the item $[A \to \beta_1 \cdot X \beta_2, u]$ of the previous state, and every item with the dot at the start, other than $[S' \to \cdot S, \varepsilon]$, is added by closure. The item $[S' \to \cdot S, \varepsilon]$ is only in $I_0$, because $S'$ is on no right side.

**Lemma 1 (validity).** If $[A \to \beta_1 \cdot \beta_2, u] \in \mathrm{st}(\gamma)$, there is a rightmost derivation $S' \Rightarrow_{rm}^* \alpha A y \Rightarrow_{rm} \alpha \beta_1 \beta_2 y$ with $y \in \Sigma^*$, $\alpha \beta_1 = \gamma$ and $\mathrm{FIRST}_k(y) = u$.

*Proof.* By induction on the order in which the construction adds items.

- **The start item.** For $[S' \to \cdot S, \varepsilon] \in I_0$, take the empty derivation with $\alpha = y = \varepsilon$.
- **GOTO.** If $[A \to \beta_1 X \cdot \beta_2, u] \in \mathrm{st}(\gamma X)$ comes from $[A \to \beta_1 \cdot X \beta_2, u] \in \mathrm{st}(\gamma)$, the derivation for the latter has $\alpha \beta_1 = \gamma$, so $\alpha \beta_1 X = \gamma X$.
- **Closure.** Suppose $[B \to \cdot \delta, v]$ is added from $[A \to \beta_1 \cdot B \beta_2, u] \in \mathrm{st}(\gamma)$ with $v \in \mathrm{FIRST}_k(\beta_2) \oplus_k \{u\}$. Take the derivation of the latter. Since $u = \mathrm{FIRST}_k(y)$, $v = \mathrm{FIRST}_k(z y)$ for some $z \in L(\beta_2)$. Rewriting $\beta_2$ to $z$ only touches symbols to the right of $B$, so it is rightmost: $S' \Rightarrow_{rm}^* \alpha A y \Rightarrow_{rm} \alpha \beta_1 B \beta_2 y \Rightarrow_{rm}^* \gamma B z y \Rightarrow_{rm} \gamma \delta z y$, with $\mathrm{FIRST}_k(z y) = v$. $\square$

**Lemma 2 (completeness).** Let $t$ be a parse tree with root $S$, under the extra root $S'$. Let $x$ be an inner node of $t$ with production $A \to \beta_1 \beta_2$, where $\beta_1$ is any prefix of the right side. Let $\alpha$ be the labels of the left siblings of the proper ancestors of $x$ and of $x$ itself, in order, and let $y$ be the part of the yield of $t$ to the right of $x$. Then $\mathrm{st}(\alpha \beta_1)$ exists and contains $[A \to \beta_1 \cdot \beta_2, \mathrm{FIRST}_k(y)]$.

*Proof.* We use induction on the depth of $x$. For the root $S'$, take the start item. Let $x$ be a child of $x'$, with production $B \to \delta A \eta$, where $x$ is the child labeled $A$ after $\delta$. By the induction hypothesis, $[B \to \delta \cdot A \eta, \mathrm{FIRST}_k(y')] \in \mathrm{st}(\alpha' \delta)$, where $\alpha'$ and $y'$ belong to $x'$. Here $\alpha = \alpha' \delta$, and $y$ is the yield of the subtrees of $\eta$ followed by $y'$. So $\mathrm{FIRST}_k(y) \in \mathrm{FIRST}_k(\eta) \oplus_k \{\mathrm{FIRST}_k(y')\}$, and closure puts $[A \to \cdot \beta_1 \beta_2, \mathrm{FIRST}_k(y)]$ into $\mathrm{st}(\alpha)$. GOTO along $\beta_1$ moves the dot, and each GOTO exists because its item has the next symbol after the dot. $\square$

**Lemma 3 (keys).** If $[A \to \beta_1 \cdot \beta_2, u] \in I$, then every $v \in \mathrm{FIRST}_k(\beta_2) \oplus_k \{u\}$ is a key of $\mathrm{ACTION}[I]$.

*Proof.* We use induction on the least height $h$ of a forest of trees for $\beta_2$ whose yield $z$ has $\mathrm{FIRST}_k(z u) = v$. There are three cases.

- **$\beta_2 = \varepsilon$.** Then $v = u$, and line L17 sets the reduction, or accept, at $u$.
- **$\beta_2$ starts with a terminal.** Line L16 sets shift at all of $\mathrm{FIRST}_k(\beta_2) \oplus_k \{u\}$.
- **$\beta_2 = C \beta_2'$ with $C \in V$.** Let the tree of $C$ use $C \to \delta$ with yield $z_1$, and let $z = z_1 z_2$. Closure puts $[C \to \cdot \delta, v']$ into $I$ with $v' = \mathrm{FIRST}_k(z_2 u) \in \mathrm{FIRST}_k(\beta_2') \oplus_k \{u\}$. Then $v = \mathrm{FIRST}_k(z_1 v')$, and the children of the tree of $C$ form a forest for $\delta$ of smaller height. $\square$

**Step 1: acceptance gives a parse tree.** Each reduction by $A \to \beta$ pops the trees of the symbols $\beta$ and pushes a node $A$ with these children. So every tree on the stack is a parse tree of its symbol, and the yields of the stack trees, from bottom to top, spell $a_1 \cdots a_{i-1}$. The accept action comes only from $[S' \to S \cdot, \varepsilon]$. A state with this item is $\mathrm{GOTO}(I, S)$ for a state $I$ that contains $[S' \to \cdot S, \varepsilon]$, so $I = I_0$. The state $I_0$ is only at the bottom of the stack: every other state is a GOTO state, and its kernel items have the dot after a symbol. So at acceptance the stack holds exactly one tree, with root $S$. Line L11 checks $i = n + 1$, so the yield of that tree is $w$. This proves part 1.

**Step 2: sentences are accepted.** Let $w \in L(G)$ and fix a parse tree $t$ of $w$ under the extra root $S'$. Claim: the parser processes the nodes of $t$ below $S'$ in postorder. A leaf is shifted, and an inner node is reduced with its production. At each step the stack holds the roots of the maximal processed subtrees, from left to right. These are the left siblings of the ancestors of the next node in postorder, and the left siblings of that node itself.

Suppose the claim holds and the next node in postorder is $x$, with $i - 1$ tokens shifted. Let $y = a_i \cdots a_n$.

- **$x$ is an inner node.** Say $x$ uses $A \to \beta$. All its children have been processed, so the stack symbols are $\alpha \beta$ in the notation of Lemma 2, and the part of the yield to the right of $x$ is $y$. Lemma 2 gives $[A \to \beta \cdot, \mathrm{FIRST}_k(y)] \in \mathrm{st}(\alpha \beta)$. Since there is no conflict, ACTION at the lookahead $u = \mathrm{FIRST}_k(y)$ is this reduction. The parser pops the $|\beta|$ children and pushes $x$.
- **$x$ is a leaf.** Then $x = a_i$, the child of a node $x'$ with production $A \to \beta_1 a_i \beta_2$, whose children before $a_i$ are processed. Lemma 2 gives $[A \to \beta_1 \cdot a_i \beta_2, \mathrm{FIRST}_k(y')]$ in the top state, where $y'$ is the yield to the right of $x'$. The input $y$ is $a_i$, followed by a yield of $\beta_2$, followed by $y'$. So $\mathrm{FIRST}_k(y) \in \mathrm{FIRST}_k(a_i \beta_2) \oplus_k \{\mathrm{FIRST}_k(y')\}$, and the cell holds shift. GOTO on $a_i$ exists because of the same item.
- **All nodes below $S'$ are processed.** The stack is $S$ over $I_0$, and $i = n + 1$. Lemma 2 for $S'$ with $\beta_1 = S$ gives $[S' \to S \cdot, \varepsilon]$, so the parser accepts.

The tree is finite, so the parser accepts after one step for each node of $t$ and one more. This proves part 2.

**Step 3: every key is a real continuation.** Let the stack symbols be $\gamma$, with $i - 1$ tokens shifted, and let $v$ be a key of $\mathrm{ACTION}[\mathrm{st}(\gamma)]$. Then $a_1 \cdots a_{i-1} z \in L(G)$ for some $z$ with $\mathrm{FIRST}_k(z) = v$.

If the key comes from a complete item, Lemma 1 gives $S' \Rightarrow_{rm}^* \gamma y$ with $\mathrm{FIRST}_k(y) = v$. If it comes from line L16, the item $[A \to \beta_1 \cdot a \beta_2, u]$ and Lemma 1 give $S' \Rightarrow^* \gamma a \beta_2 y'$ with $\mathrm{FIRST}_k(y') = u$. Then $v = \mathrm{FIRST}_k(a z_2 y')$ for some $z_2 \in L(\beta_2)$. In both cases $\gamma$ derives $a_1 \cdots a_{i-1}$ through the stack trees.

**Step 4: the inspected tokens stay consistent.** Let $h$ be the largest position read by a lookahead so far, that is, the largest $\min(i' + k - 1, n)$ over the steps done so far at positions $i'$. Claim: at each test of line L3, $a_i \cdots a_h$ is a prefix of some key of the top state (the empty string when $h < i$).

Let the last step be taken at position $i$ with the lookahead $u$, a key of the state on top then. Then $u$ is $a_i \cdots a_h$, or longer when $h < i + k - 1$.

- **A reduction by $A \to \beta$.** Its item $[A \to \beta \cdot, u]$ traces back through GOTO to $[A \to \cdot \beta, u]$ in the state $s'$ below the popped entries. That item is added by closure from some $[B \to \delta \cdot A \eta, u'] \in s'$ with $u \in \mathrm{FIRST}_k(\eta) \oplus_k \{u'\}$. The new state $\mathrm{GOTO}(s', A)$ contains $[B \to \delta A \cdot \eta, u']$, so $u$ is a key of it by Lemma 3. The position $i$ is unchanged.
- **A shift of $a_i$.** It comes from $[A \to \beta_1 \cdot a_i \beta_2, u_0]$ with $u = \mathrm{FIRST}_k(a_i z)$ for a string $z$ that starts with a yield of $\beta_2$ and continues with $u_0$. The new state contains $[A \to \beta_1 a_i \cdot \beta_2, u_0]$. Its key $\mathrm{FIRST}_k(z)$, which is a key by Lemma 3, has the rest of $u$ as a prefix.

**Step 5: the valid prefix property.** Suppose the parser reports an error at position $p$, with stack symbols $\gamma$ and $i - 1$ tokens shifted. An error arises in one of three ways.

- **No action (line L4).** Here $p = i + d$, and $u$ shares $d$ tokens with a key. By Step 3, $a_1 \cdots a_{p-1}$ starts a sentence. By Step 4, $d \ge h - i + 1$, so $p > h$.
- **Shift without GOTO (line L6), only for $k = 0$.** Here $p = i$ and $h < i$. The top state has a shift item $[A \to \beta_1 \cdot a \beta_2, u]$. By Lemma 1 and Step 3, $a_1 \cdots a_{i-1} a$ starts a sentence, so $a_1 \cdots a_{i-1}$ does too.
- **Accept with input left (line L11).** Here $p = i$ and $h < i$, and $a_1 \cdots a_{i-1} \in L(G)$ by Step 1.

Now let $p \le n$, and suppose that a sentence $s$ starts with $a_1 \cdots a_p$. Every step so far read only positions up to $h < p$ and shifted tokens before $i \le p$. So the parser makes the same moves on $s$ and reaches the same stack. On $s$ it accepts by Step 2, following the tree of $s$. So at this stack, $s$ has the next action that Step 2 describes.

- **No action.** The lookahead on $s$ is a key that agrees with $u$ on $d + 1$ tokens, against the choice of $d$.
- **Shift without GOTO.** The next node of the tree of $s$ is a leaf, and GOTO on $s_i = a_i$ exists, a contradiction.
- **Accept with input left.** The parser on $s$ accepts here while $s$ has the token $s_i$ left, which Step 1 excludes.

This proves part 3.

**Step 6: termination.** Shifts happen at most $n$ times. Between two shifts, the moves depend only on the stack and the lookahead $u$. By Step 3 there is a sentence $s = a_1 \cdots a_{i-1} z$ with $\mathrm{FIRST}_k(z) = u$. It agrees with $w$ on every position read so far, so the parser makes the same moves on $s$, which stop by Step 2. Hence the parser stops on every input. Knuth (1965) shows moreover that for an LR(k) grammar the number of reductions is $O(n + 1)$, which gives part 4. We cite that bound rather than reprove it. $\blacksquare$
