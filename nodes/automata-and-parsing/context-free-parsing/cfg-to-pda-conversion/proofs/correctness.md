---
title: The pushdown automaton built from a grammar accepts exactly the language of the grammar
proves: [correctness]
status: full
---

Let $G = (V, \Sigma, R, S)$ with $V \cap \Sigma = \emptyset$, and let $P$ be the output of lines L1 to L6: one state $q$, stack alphabet $V \cup \Sigma$, start symbol $S$, an expand move $(q, \alpha) \in \delta(q, \varepsilon, A)$ for each production $A \to \alpha$ (line L3) and a match move $(q, \varepsilon) \in \delta(q, a, a)$ for each $a \in \Sigma$ (line L5), and no other move. Configurations are $(q, w, \gamma)$ with the top of the stack on the left.

**Lemma 1 (the moves of $P$).** In a configuration with top symbol $A \in V$, the only moves are expand moves by productions of $A$, and they read no input. In a configuration with top symbol $a \in \Sigma$, the only move is the match move, and it exists exactly when the next input symbol is $a$. A configuration with an empty stack has no move.

*Proof.* Lines L3 and L5 are the only places where moves are added. An expand move has a nonterminal as its top symbol and a match move has a terminal, and $V \cap \Sigma = \emptyset$. $\square$

**Lemma 2 (runs are leftmost derivations).** For all $x, y \in \Sigma^*$ and $\alpha \in (V \cup \Sigma)^*$,
$$(q, xy, \alpha) \vdash^* (q, y, \varepsilon) \iff \alpha \Rightarrow^*_{lm} x.$$
Moreover, the number of expand moves in such a run equals the number of steps of the corresponding derivation, and the run makes exactly $|x|$ match moves.

*Proof of $\Leftarrow$.* Induction on the pair $(k, |\alpha|)$ in lexicographic order, where $k$ is the number of steps of the leftmost derivation. If $\alpha = \varepsilon$, then $x = \varepsilon$ and the empty run works. If $\alpha = a\alpha'$ with $a \in \Sigma$, a derivation from $\alpha$ never changes the first symbol, so $x = a x'$ with $\alpha' \Rightarrow^*_{lm} x'$ in $k$ steps. The match move gives $(q, a x' y, a\alpha') \vdash (q, x'y, \alpha')$, and the hypothesis for $(k, |\alpha'|)$ gives the rest. If $\alpha = A\alpha'$ with $A \in V$, then $k \ge 1$ because $x$ has no nonterminal, and the first step of a leftmost derivation rewrites the leftmost nonterminal, which is $A$: $\alpha \Rightarrow_{lm} \beta\alpha'$ by some $A \to \beta$, and $\beta\alpha' \Rightarrow^*_{lm} x$ in $k - 1$ steps. The expand move gives $(q, xy, A\alpha') \vdash (q, xy, \beta\alpha')$, and the hypothesis for $k - 1$ gives the rest.

*Proof of $\Rightarrow$.* Induction on the number $m$ of moves. If $m = 0$, then $\alpha = \varepsilon$ and $x = \varepsilon$, and the empty derivation works. If $m \ge 1$, the stack is not empty, and Lemma 1 gives two cases. If $\alpha = a\alpha'$ with $a \in \Sigma$, the first move is the match move and reads $a$. The run reads exactly $x$, so $x = a x'$, and the other $m - 1$ moves are a run $(q, x'y, \alpha') \vdash^* (q, y, \varepsilon)$. By induction $\alpha' \Rightarrow^*_{lm} x'$, so $a\alpha' \Rightarrow^*_{lm} a x'$. If $\alpha = A\alpha'$ with $A \in V$, the first move is an expand move by some $A \to \beta$, and the other moves are a run $(q, xy, \beta\alpha') \vdash^* (q, y, \varepsilon)$. By induction $\beta\alpha' \Rightarrow^*_{lm} x$, and since $A$ is the leftmost symbol of $\alpha$, $\alpha \Rightarrow_{lm} \beta\alpha' \Rightarrow^*_{lm} x$.

In both directions each expand move corresponds to one derivation step and each match move to one symbol of $x$, which gives the counts. $\square$

**Theorem 1 (acceptance by empty stack).** $N(P) = L(G)$.

*Proof.* Take $\alpha = S$ and $y = \varepsilon$ in Lemma 2: $(q, w, S) \vdash^* (q, \varepsilon, \varepsilon)$ exactly when $S \Rightarrow^*_{lm} w$. Every derivation of a terminal string from $S$ can be reordered into a leftmost one, because both correspond to the same parse tree, so this holds exactly when $w \in L(G)$. $\square$

**Theorem 2 (acceptance by final state).** Let $P'$ be the output of lines L7 to L10: $P$ with new states $s$ and $f$, a new stack symbol $\bot$, the moves $(q, S\bot) \in \delta(s, \varepsilon, \bot)$ and $(f, \bot) \in \delta(q, \varepsilon, \bot)$, start state $s$, start symbol $\bot$ and $F = \{f\}$. Then $L(P') = L(G)$.

*Proof.* If $w \in L(G)$, Theorem 1 gives a run $(q, w, S) \vdash^* (q, \varepsilon, \varepsilon)$ of $P$. The moves of $P$ do not depend on the symbols below the top, so the same moves give $(q, w, S\bot) \vdash^* (q, \varepsilon, \bot)$ in $P'$, and $(s, w, \bot) \vdash (q, w, S\bot) \vdash^* (q, \varepsilon, \bot) \vdash (f, \varepsilon, \bot)$ accepts.

Conversely, take an accepting run of $P'$ on $w$. The only move from $s$ is the first one, to $(q, w, S\bot)$. The only move into $f$ is the one from $q$ with $\bot$ on top, and $f$ has no moves, so the run ends there and that move happens with all of $w$ read. Between these two moves the state is $q$ and $\bot$ is never on top, because no move of $P$ pops $\bot$ or has $\bot$ as its top, until the stack above $\bot$ is empty. So the middle part is $(q, w, S\bot) \vdash^* (q, \varepsilon, \bot)$, where $\bot$ stays at the bottom, and removing $\bot$ gives a run $(q, w, S) \vdash^* (q, \varepsilon, \varepsilon)$ of $P$. By Theorem 1, $w \in L(G)$. $\blacksquare$
