---
title: An SLR(1) parser without conflicts parses exactly the sentences, detects errors at the first bad token, and stops in linear time
proves: [correctness, termination]
status: full
---

We use the notation of the [context-free grammar](/context-free-grammar/) page and the pseudocode BUILD-SLR and SLR-PARSE of the page. Line B1 removes the useless productions; this changes neither $L(G)$ nor the parse trees of sentences, since no parse tree of a sentence uses a useless production. So we assume that $G$ is reduced: every nonterminal is reachable from $S$ and derives a terminal string. $G$ is augmented with $S' \to S$, the end marker is $\$$, and FOLLOW is computed for the augmented grammar. We assume that the table has no conflict. The input is $w = a_1 \cdots a_n$ and $a_{n+1} = \$$.

An item $[A \to \alpha \cdot \beta]$ is *valid* for a string $\gamma$ of grammar symbols if there is a rightmost derivation $S' \Rightarrow^*_{rm} \varphi A z \Rightarrow_{rm} \varphi \alpha \beta z$ with $\gamma = \varphi \alpha$ and $z$ a terminal string. $\gamma$ is a *viable prefix* if some item is valid for it. Write $\delta(\gamma)$ for the state reached from state 0 by the GOTO transitions over the symbols of $\gamma$, if it exists.

## Lemma 1: the states are the sets of valid items

**Claim.** For every $\gamma$, $\delta(\gamma)$ exists if and only if $\gamma$ is viable, and then $\delta(\gamma)$ is the set of items valid for $\gamma$.

*Items in the state are valid.* By induction on the construction. $[S' \to \cdot S]$ is valid for $\varepsilon$ (the derivation with no step, $\varphi = z = \varepsilon$). GOTO keeps validity: if $[A \to \alpha \cdot X \beta]$ is valid for $\gamma$, the same derivation shows that $[A \to \alpha X \cdot \beta]$ is valid for $\gamma X$. CLOSURE keeps validity: if $[A \to \alpha \cdot B \beta]$ is valid for $\gamma$, by $S' \Rightarrow^*_{rm} \varphi A z \Rightarrow \varphi \alpha B \beta z$, then $\beta$ derives a terminal string $y$ because $G$ is reduced, and $\varphi \alpha B \beta z \Rightarrow^*_{rm} \varphi \alpha B y z \Rightarrow \varphi \alpha \eta\, y z$ is a rightmost derivation for every production $B \to \eta$. So $[B \to \cdot \eta]$ is valid for $\gamma = \varphi \alpha$.

*Valid items are in the state.* Let $[A \to \alpha \cdot \beta]$ be valid for $\gamma$, by a derivation of $m$ steps. We show by induction on $m$ that $[A \to \cdot \alpha \beta] \in \delta(\varphi)$, where $\gamma = \varphi \alpha$; then GOTO over the symbols of $\alpha$ gives $[A \to \alpha \cdot \beta] \in \delta(\gamma)$. If $m = 0$, then $A = S'$, $\varphi = \varepsilon$, and $[S' \to \cdot S]$ is in state 0. Otherwise, look at the step of the derivation that created this occurrence of $A$, by a production $B \to \alpha' A \beta'$: $S' \Rightarrow^*_{rm} \varphi' B z' \Rightarrow \varphi' \alpha' A \beta' z'$. After this step the derivation rewrites only symbols to the right of $A$, until $A$ itself is rewritten, because it is rightmost. So $\varphi = \varphi' \alpha'$ and $\beta'$ derives a terminal prefix of $z$. Then $[B \to \alpha' \cdot A \beta']$ is valid for $\varphi$ by a shorter derivation, so by induction it is in $\delta(\varphi)$, and CLOSURE adds $[A \to \cdot \alpha \beta]$.

Finally, a state built by GOTO from a nonempty kernel is nonempty, and every item in it is valid, so $\gamma$ is viable when $\delta(\gamma)$ exists; conversely, if some item is valid for $\gamma$, it lies in $\delta(\gamma)$, which therefore exists. $\square$

## Lemma 2: the stack invariant, and soundness

A *configuration* is a stack of trees with roots $\gamma = X_1 \cdots X_m$, a stack of states, and the position $i$ of the next token. **Invariant:** the states are $\delta(\varepsilon), \delta(X_1), \ldots, \delta(X_1 \cdots X_m)$; the leaves of the trees, left to right, are $a_1 \cdots a_{i-1}$; and each tree is a parse tree with its root.

It holds after line L1. A shift of $a$ pushes $\text{GOTO}[\delta(\gamma), a] = \delta(\gamma a)$ and the leaf $a$. A reduction by $A \to \beta$ is made in a state that contains $[A \to \beta \cdot]$, so by Lemma 1 the item is valid for $\gamma$, which therefore ends with $\beta$, say $\gamma = \alpha \beta$. The same derivation shows that $[A \to \cdot \beta]$ is valid for $\alpha$, so $\delta(\alpha)$, the state uncovered by line L8, has a GOTO on $A$, and line L9 pushes $\delta(\alpha A)$ and a node $A$ over the trees of $\beta$. So the invariant holds, and line L9 never finds GOTO undefined.

**Soundness.** The accept action is only in a state containing $[S' \to S \cdot]$, which by Lemma 1 is valid only for $\gamma = S$, and only on $\$$, that is, at $i = n + 1$. So an accepted result is a single parse tree with root $S$ and leaves $w$. Reading the reductions backwards gives a rightmost derivation of $w$, by Claim 1 of the [shift-reduce parsing](/shift-reduce-parsing/) proof, which holds for every sequence of legal moves.

## Lemma 3: every move toward acceptance is in the table

A configuration is *good* if some sequence of legal shift-reduce moves (shift the next token, or reduce a right side that forms the top of the stack) leads from it to the stack $S$ at position $n + 1$. By Claim 1 of the shift-reduce proof applied to such a continuation, its reductions read backwards give a rightmost derivation $S \Rightarrow^*_{rm} \gamma\, a_i \cdots a_n$.

**Claim.** Let a configuration with the invariant of Lemma 2 be good, and fix an accepting continuation. Its next move is an action in $\text{ACTION}[\delta(\gamma), a_i]$.

*Proof.* *Reduce by $A \to \beta$.* Then $\gamma = \alpha \beta$, and the continuation after the move gives $S \Rightarrow^*_{rm} \alpha A\, a_i \cdots a_n$. With $S' \Rightarrow S$ in front and the step $\alpha A\, a_i \cdots a_n \Rightarrow \alpha \beta\, a_i \cdots a_n$, the item $[A \to \beta \cdot]$ is valid for $\gamma$, so it is in $\delta(\gamma)$ by Lemma 1. The same derivation shows $a_i \in \text{FOLLOW}(A)$ (or $\$ \in \text{FOLLOW}(A)$ when $i = n + 1$). So line B5 put "reduce $A \to \beta$" into the entry.

*Shift $a_i$.* The leaf $a_i$ ends inside the final tree, so some later reduction of the continuation pops it; take the first one, by $A' \to \beta_1 a_i \beta_2$. Until then nothing below $a_i$ is popped, so at that moment the stack is $\gamma\, a_i\, \beta_2$ with $\gamma = \rho \beta_1$, and as in the first case the continuation gives $S' \Rightarrow^*_{rm} \rho A' z \Rightarrow \rho \beta_1 a_i \beta_2 z$ with $z$ terminal. So $[A' \to \beta_1 \cdot a_i \beta_2]$ is valid for $\gamma$, it is in $\delta(\gamma)$, and line B4 put the shift into the entry.

*Accept.* Then $\gamma = S$ and $i = n + 1$; $[S' \to S \cdot]$ is in $\delta(S)$ and line B6 put the accept action on $\$$. $\square$

**Corollary.** Since the table has no conflict, from a good configuration the parser makes the next move of every accepting continuation, and the new configuration is good again. So all accepting continuations from a good configuration are the same sequence, and the parser follows it to acceptance in finitely many moves. In particular the grammar is unambiguous: two parse trees of $w$ would give two different reverse rightmost derivations, that is, two different accepting continuations from the start.

## Theorem 4: the parser accepts exactly $L(G)$

If $w \in L(G)$, the start configuration is good (any rightmost derivation of $w$, read backwards, is an accepting continuation), so by the corollary the parser accepts, with the parse tree of $w$. If $w \notin L(G)$, it never accepts, by soundness. $\square$

## Lemma 5: errors are found at the first bad token

**Claim.** The parser shifts $a_i$ (for $i \le n$) only if $a_1 \cdots a_i$ is a prefix of a sentence, and it accepts only if $a_1 \cdots a_n$ is a sentence. Conversely, if $a_1 \cdots a_i$ is a prefix of a sentence, the parser shifts $a_i$, or accepts when $i = n + 1$ and $w \in L(G)$.

*Proof.* A shift of $a_i$ happens in a state $\delta(\gamma)$ with an item $[B \to \mu \cdot a_i \nu]$, which by Lemma 1 is valid for $\gamma$: $S' \Rightarrow^*_{rm} \rho B z \Rightarrow \rho \mu a_i \nu z$ with $\rho \mu = \gamma$. The trees on the stack show $\gamma \Rightarrow^* a_1 \cdots a_{i-1}$, and $\nu$ derives a terminal string because $G$ is reduced, so $a_1 \cdots a_i$ followed by that string and $z$ is a sentence. For the converse, let $w' \in L(G)$ start with $a_1 \cdots a_i$. Each move depends only on the stack and the token being examined, and until $a_i$ is shifted the parser examines only $a_1, \ldots, a_i$. So the runs on $w$ and $w'$ agree until $a_i$ is shifted, and on $w'$ that happens, by Theorem 4. $\square$

So if $w \notin L(G)$ and the parser stops, it reports the error at the least $i$ such that $a_1 \cdots a_i$ is not a prefix of a sentence, where $i = n + 1$ means that $w$ itself is a proper prefix of a sentence. It remains to show that it stops.

## Lemma 6: no cycle of empty symbols in the automaton

**Claim.** There are no states $p_0, p_1, \ldots, p_k = p_0$, $k \ge 1$, and nullable symbols $Y_1, \ldots, Y_k$ with $\text{GOTO}[p_{j-1}, Y_j] = p_j$.

*Proof.* Suppose there are. Every state is reached by some string, so $p_0 = \delta(\gamma)$ for a viable $\gamma$, and $\delta(\gamma (Y_1 \cdots Y_k)^m) = p_0$ for every $m \ge 0$. By Lemma 1 these strings are viable, so for each $m$ there is a valid item $[B \to \mu \cdot \nu]$ with $S' \Rightarrow^*_{rm} \rho B z \Rightarrow \rho \mu \nu z$, $\rho \mu = \gamma (Y_1 \cdots Y_k)^m$; since $G$ is reduced, $\nu z$ derives a terminal string $x_m$, and the $Y$'s derive $\varepsilon$, so

$$S' \Rightarrow^*_{rm} \gamma\, (Y_1 \cdots Y_k)^m\, x_m \Rightarrow^*_{rm} \gamma\, x_m .$$

Put trees for the symbols of $\gamma$, with some terminal yield $u$, on the stack with the states $\delta$ of its prefixes, and the input $x_m$. Read backwards, the derivation above is an accepting continuation from this configuration, which first builds the $mk$ empty trees $Y_1, \ldots, Y_k, Y_1, \ldots$ one after the other, without shifting. By the corollary of Lemma 3, the parser follows it. But before its first shift, the parser's moves from stack $\gamma$ depend only on the first token $b$ of $x_m \$$. Some $b$ is the first token for infinitely many $m$, and for all of them the parser makes the same sequence of moves before its first shift. That sequence is finite (it is part of an accepting run for one of them) and yet contains a stack of height $|\gamma| + mk$ for infinitely many $m$. This is impossible. $\square$

## Theorem 7: the parser stops after $O(n)$ moves

**Between two shifts there are finitely many reductions.** Suppose that from some configuration the parser reduces forever. No new leaf is shifted, so every tree created from then on, on top of the stack, has the empty yield, and every stack is viable by Lemma 2 and Lemma 1.

*Case 1: some stack of states occurs twice.* The states determine the symbols (each state other than 0 is entered by one symbol), so the two configurations have the same roots $X_1 \cdots X_m$, and the second forest is obtained from the first by at least one reduction, so it has more nodes and the same leaves. Since $X_1 \cdots X_m$ is viable and $G$ is reduced, there is a rightmost derivation $S' \Rightarrow^* X_1 \cdots X_m\, x$ with $x$ terminal; hanging the first forest or the second forest under its tree gives two different parse trees of the same sentence. This contradicts the unambiguity in the corollary of Lemma 3.

*Case 2: no stack of states repeats.* Let $L$ be the lowest stack level that is popped infinitely often, if there is one. Then after some time the levels below $L$ never change, and each time level $L$ is popped, the next push gives a stack of states of height $L$ that consists of the fixed lower part and one state: finitely many stacks, occurring infinitely often, which is Case 1. So every level is eventually never popped. The heights are then unbounded (otherwise some stack would repeat), so there are infinitely many entries that are never popped, above the height $h_0$ at the start; their trees have empty yields. Two of them, at levels $h_0 < j_1 < j_2$, carry the same state, and the entries between them are consecutive, with states linked by GOTO over their nullable root symbols. This is a cycle as in Lemma 6, a contradiction.

So between two shifts the parser makes finitely many reductions, there are at most $n$ shifts, and the parser stops. By Theorem 4 and Lemma 5 it then accepts exactly the sentences, with their parse tree, and reports any other input at the first token that no sentence allows there.

**The number of moves is linear.** Every move creates a node, a leaf for a shift and an inner node for a reduction, and no node is ever destroyed, so the number of moves is at most the number of nodes in the forest on the stack when the parser stops, plus one. Let that forest have the roots $\gamma$ and the leaves $a_1 \cdots a_{i-1}$, with $i \le n + 1$. Since $\gamma$ is viable, as in Case 1 the forest is part of a parse tree $T$ of a sentence, and $G$ is unambiguous. Then in $T$ no node has a proper descendant with the same label and the same span of leaves, since replacing the upper node's subtree by the lower one gives another parse tree of the same sentence. Let $r$ be the longest right side and $N$ the number of states. In the forest:

- the nodes with a nonempty span have at most $2(i - 1)$ different spans, since the spans of a tree are nested or disjoint, and at most $|V| + 1$ nodes have each span, because nodes with the same nonempty span lie on one path and have different labels;
- each maximal subtree with an empty yield has no repeated label on a path, so it has at most $c = 1 + r + \cdots + r^{|V|}$ nodes;
- such a subtree is either a child of a node with a nonempty span, at most $r$ per node, or a root of the forest. The roots with an empty yield come in runs of consecutive stack entries, one run after each root with a nonempty yield and one at the bottom; a run has at most $N$ entries, since two entries with the same state in a run would give a cycle as in Lemma 6.

So the forest has at most $2(i - 1)(|V| + 1)(1 + r c) + i N c$ nodes, which is $O(i)$ for a fixed grammar, and the parser makes $O(n)$ moves. $\square$
