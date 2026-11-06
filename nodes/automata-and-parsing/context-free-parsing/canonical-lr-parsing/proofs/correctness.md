---
title: The canonical LR(1) parser outputs only rightmost derivations, and with a table free of conflicts it parses every sentence
proves: [correctness]
status: full
---

We use the augmented grammar $G'$ with $S' \to S$ and the end marker $\$$. The item sets are the list $C$ built by lines L1 to L8, and $T$ is the transition function of line L7. For a string $\gamma = X_1 \cdots X_m$ of grammar symbols, write $\mathrm{st}(\gamma)$ for the state reached from state 0 by following $T$ on $X_1, \ldots, X_m$, when all these transitions are defined. FIRST$(\theta)$ denotes the set computed from the FIRST sets of the symbols, as in line L15. For every grammar it contains each terminal that begins a terminal string derived from $\theta$: the fixpoint adds a terminal for each way it can begin such a string. A derivation step is *rightmost* when it rewrites the rightmost nonterminal of the form.

**Lemma 1 (shape of items).** If the item $[A \to \alpha \cdot \beta, a]$ is in $\mathrm{st}(\gamma)$, then $\alpha$ is a suffix of $\gamma$. If moreover $\alpha = \alpha' X$, then $[A \to \alpha' \cdot X \beta, a]$ is in $\mathrm{st}(\gamma')$, where $\gamma = \gamma' X$.

*Proof.* By induction on $|\gamma|$. The items of a CLOSURE are the given items and items with the dot at the left end, which have $\alpha = \varepsilon$. For $\gamma = \varepsilon$ the state is $I_0$, whose only item that is not added by closure is $[S' \to \cdot S, \$]$, so every item has $\alpha = \varepsilon$. For $\gamma = \gamma' X$, the state is GOTO$(\mathrm{st}(\gamma'), X)$ by line L5. By line L17 an item with $\alpha \ne \varepsilon$ in it comes from an item $[A \to \alpha' \cdot X \beta, a]$ of $\mathrm{st}(\gamma')$ with $\alpha = \alpha' X$. By the induction hypothesis $\alpha'$ is a suffix of $\gamma'$, so $\alpha$ is a suffix of $\gamma$. $\square$

**Lemma 2 (validity).** If the item $[A \to \alpha \cdot \beta, a]$ is valid for $\gamma$, then $\mathrm{st}(\gamma)$ is defined and contains the item.

*Proof.* The item is valid through a rightmost derivation $S' \Rightarrow^*_{rm} \delta A x \Rightarrow_{rm} \delta\alpha\beta x$ with $\gamma = \delta\alpha$ and $a$ the first symbol of $x\$$. Let $r$ be the number of steps of $S' \Rightarrow^*_{rm} \delta A x$. We use induction on the pair $(r, |\alpha|)$ in lexicographic order.

*Case $\alpha = \alpha' X$.* The item $[A \to \alpha' \cdot X\beta, a]$ is valid for $\delta\alpha'$ through the same derivation, with the same $r$ and a shorter $\alpha'$. By the induction hypothesis it is in $\mathrm{st}(\delta\alpha')$. So $X$ follows a dot in that state, line L7 defines $T$ on $X$, and line L17 puts $[A \to \alpha \cdot \beta, a]$ into GOTO$(\mathrm{st}(\delta\alpha'), X) = \mathrm{st}(\gamma)$.

*Case $\alpha = \varepsilon$ and $r = 0$.* Then $\delta A x = S'$, so $\gamma = \varepsilon$, $A = S'$, $x = \varepsilon$ and $a = \$$. The only production of $S'$ is $S' \to S$, and $[S' \to \cdot S, \$]$ is in $I_0 = \mathrm{st}(\varepsilon)$ by line L1.

*Case $\alpha = \varepsilon$ and $r \ge 1$.* Here $\gamma = \delta$. Look at the step of the derivation that created this occurrence of $A$: a step $\delta' B y \Rightarrow_{rm} \delta' \eta A \theta y$ by a production $B \to \eta A \theta$, where $y$ is a terminal string because the step is rightmost. After this step, a rightmost derivation rewrites the nonterminals right of $A$ before $A$ itself, and it does not touch the symbols left of $A$ until $A$ is rewritten. So the derivation has the form

$$S' \Rightarrow^*_{rm} \delta' B y \Rightarrow_{rm} \delta'\eta A \theta y \Rightarrow^*_{rm} \delta' \eta A z y = \delta A x,$$

with $\theta \Rightarrow^* z$, $x = zy$ and $\delta = \delta'\eta$. The item $[B \to \eta \cdot A\theta, b]$, with $b$ the first symbol of $y\$$, is valid for $\delta'\eta = \gamma$ through a derivation of $S' \Rightarrow^*_{rm} \delta' B y$ with fewer than $r$ steps. By the induction hypothesis, it is in $\mathrm{st}(\gamma)$. Now $a$ is the first symbol of $zy\$$. If $z \ne \varepsilon$, then $a$ begins a string derived from $\theta$; if $z = \varepsilon$, then $\theta \Rightarrow^* \varepsilon$ and $a = b$. In both cases $a \in$ FIRST$(\theta b)$. So line L15 adds $[A \to \cdot\beta, a]$ for the production $A \to \beta$ to the closure that forms $\mathrm{st}(\gamma)$. $\square$

**Lemma 3 (invariant of the driver).** At each test of line L20, let the stack hold the states $s_0 s_1 \cdots s_m$ and let $u$ be the part of $w$ read so far. Then $s_0 = 0$, there are symbols $X_1, \ldots, X_m$ with $s_j = T[s_{j-1}, X_j]$ for each $j$, so that $s_j = \mathrm{st}(X_1 \cdots X_j)$, and the reductions output so far, applied in reverse order as rewriting steps, derive $u$ from $X_1 \cdots X_m$. In any form of this derivation followed by the rest $v$ of $w$, each step rewrites the rightmost nonterminal.

*Proof.* By induction on the number of steps. At the start, $m = 0$, $u = \varepsilon$, and there are no reductions. A shift on the terminal $a$ pushes $T[s_m, a]$ (line L10 and line L21), so $X_{m+1} = a$ and $u$ grows by $a$; the derivation is unchanged. A reduce by $A \to \beta$ is in the table because some item $[A \to \beta \cdot, a]$ is in $s_m$ (line L11). By Lemma 1, $\beta = X_{m-|\beta|+1} \cdots X_m$, and $s_{m-|\beta|}$ holds $[A \to \cdot \beta, a]$, so $T[s_{m-|\beta|}, A]$ is defined and line L22 pushes it. The new symbols are $X_1 \cdots X_{m-|\beta|} A$, and the new first step rewrites this $A$ to $\beta$. Every symbol right of this $A$, in the form followed by $v$, is a terminal of $v$, so the step is rightmost. The old derivation follows it. $\square$

**Theorem 1 (soundness).** If LR-PARSE$(w)$ returns an output, the output, read backwards, is a rightmost derivation $S \Rightarrow^*_{rm} w$. This holds for every grammar, also when conflicts were resolved in any way.

*Proof.* Accept happens at line L23, so $s_m$ holds $[S' \to S \cdot, \$]$ and the next symbol is $\$$, so $u = w$. By Lemma 1, $X_m = S$ and $s_{m-1}$ holds $[S' \to \cdot S, \$]$. This item is the kernel of $I_0$, it is not added by any closure because $S'$ is on no right side, and it is not the kernel of any GOTO, whose kernels have the dot after a symbol. So $s_{m-1} = 0$, which happens only at the bottom of the stack, because every pushed state is a GOTO and does not hold this item. Hence $m = 1$, and Lemma 3 says that the output, backwards, derives $w$ from $S$ by rightmost steps. $\square$

**Theorem 2 (completeness).** Assume that no entry of ACTION got two actions. If $w \in L(G)$ and $T_w$ is a parse tree of $w$ with root $S$, then LR-PARSE$(w)$ accepts, and the reductions it outputs are the inner nodes of $T_w$ in postorder. In particular $w$ has only one parse tree, so $G$ is unambiguous.

*Proof.* Add a root $S'$ above $T_w$. The *events* of the tree are its terminal leaves and its inner nodes other than $S'$, in postorder. Make a shift event for each terminal leaf and a reduce event for each inner node, and a final accept event. We show by induction that the $t$-th step of the parser is the $t$-th event.

Before an event $e$, call a node *done* if it comes before $e$ in postorder. Let $P$ be the set of nodes that are not done but have a done descendant or are on the path from the root to $e$. These are exactly the proper ancestors of $e$, together with $e$ itself if $e$ is an inner node. For each node $N \in P$ with production $A \to \alpha\beta$, let $\alpha$ be its children that are done, which come before its children that are not done. Let $\gamma$ be the concatenation of these $\alpha$, from the root down. The induction hypothesis is that the stack symbols are $X_1 \cdots X_m = \gamma$ and that the input read is the yield of the done nodes, which is a prefix $u$ of $w$.

The tree gives, for each $N \in P$ with $A \to \alpha \cdot \beta$ as above, a rightmost derivation $S' \Rightarrow^*_{rm} \delta A x \Rightarrow_{rm} \delta\alpha\beta x$. Expand the nodes of the path from the root to $N$, and before each of them expand fully all the subtrees to the right of the path. Then $\delta$ is the concatenation of the done children of the ancestors of $N$, $x$ is the yield of the tree to the right of $N$, and $\delta\alpha$ is a prefix of $\gamma$. So the item $[A \to \alpha \cdot \beta, a]$, with $a$ the first symbol of $x\$$, is valid for $\delta\alpha$.

- If $e$ is a leaf with terminal $a$, its parent $N$ is the lowest node of $P$, and it has $A \to \alpha \cdot a \beta'$ with $\delta\alpha = \gamma$. The next input symbol is $a$, because the done leaves are exactly the leaves before $e$. The item is valid for $\gamma$, so by Lemma 2 it is in $\mathrm{st}(\gamma)$, and line L10 put a shift into ACTION$[\mathrm{st}(\gamma), a]$. With no conflict this is the only action, so the parser shifts $a$, and the hypothesis holds before the next event.
- If $e$ is an inner node with production $A \to \beta$, all its children are done, so $e$ is the lowest node of $P$ with the item $[A \to \beta \cdot, a]$, valid for $\gamma = \delta\beta$. Here $a$ is the first symbol after the yield of $e$, which is the next input symbol. By Lemma 2 and line L11, ACTION$[\mathrm{st}(\gamma), a]$ is reduce $A \to \beta$, and it is the only action. The parser pops the $|\beta|$ symbols of $\beta$ and pushes $A$, which is the stack of the next event, where $e$ is done.
- If all nodes but $S'$ are done, then $\gamma = S$ and the input read is $w$, and $[S' \to S \cdot, \$]$ is valid for $S$. By Lemma 2 and line L12, the action on $\$$ is accept.

So the parser accepts after the events of $T_w$, and outputs its inner nodes in postorder. The parser is deterministic and its run depends only on $w$. Two different parse trees of $w$ would give two different postorders, so they would give two different runs, which is impossible. $\square$

**Lemma 4 (state items are valid).** If $G$ has no useless symbols, every item of $\mathrm{st}(\gamma)$ is valid for $\gamma$.

*Proof.* When every nonterminal derives a terminal string, the computed FIRST$(\theta)$ is exactly the set of terminals that begin a terminal string derived from $\theta$: each terminal that the fixpoint adds begins a sentential form derived from $\theta$, and the rest of that form derives a terminal string. We use induction on the order in which the construction adds items. The item $[S' \to \cdot S, \$]$ is valid for $\varepsilon$. A GOTO item $[A \to \alpha X \cdot \beta, a]$ of $\mathrm{st}(\gamma X)$ comes from $[A \to \alpha \cdot X\beta, a]$ of $\mathrm{st}(\gamma)$, which is valid for $\gamma$; the same derivation makes the new item valid for $\gamma X$. A closure item $[B \to \cdot\eta, b]$ comes from $[A \to \alpha \cdot B \beta, a]$, valid for $\gamma$ through $S' \Rightarrow^*_{rm} \delta A x \Rightarrow_{rm} \delta \alpha B \beta x$, and $b \in$ FIRST$(\beta a)$. Take a terminal string $y$ with $\beta \Rightarrow^* y$ such that $b$ is the first symbol of $yx\$$; it exists by the exactness of FIRST. Then

$$S' \Rightarrow^*_{rm} \delta A x \Rightarrow_{rm} \delta\alpha B \beta x \Rightarrow^*_{rm} \delta\alpha B y x \Rightarrow_{rm} \delta\alpha\eta y x$$

is rightmost, because $\beta$ lies right of $B$. So $[B \to \cdot\eta, b]$ is valid for $\delta\alpha = \gamma$. $\square$

**Theorem 3 (rejection).** Assume that no entry of ACTION got two actions and that $G$ has no useless symbols. If $w \notin L(G)$, LR-PARSE$(w)$ returns error after finitely many steps.

*Proof.* By Theorem 1 the parser never accepts $w$. The theorem of the [complexity proof](complexity.md), which uses only Lemmas 1 to 4 and Theorem 2, shows that on every input the run stops after $O(n)$ steps. A run that stops without accepting ends at line L24. $\blacksquare$

Theorems 1, 2 and 3 together say: with a table free of conflicts, for a grammar without useless symbols, LR-PARSE$(w)$ returns a rightmost derivation of $w$ when $w \in L(G)$ and error otherwise. Theorem 2 alone shows that a grammar with such a table is unambiguous.
