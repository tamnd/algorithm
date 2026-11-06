---
title: Proof that context-free grammars and pushdown automata define the same languages
proves: [statement]
status: full
---

We use the definitions of the [statement](../): a PDA $P = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$, configurations $(q, w, \gamma)$ with the top of the stack on the left, the move relation $\vdash$, $L(P)$ for acceptance by final state and $N(P)$ for acceptance by empty stack. We prove $1 \Rightarrow 2 \Rightarrow 3 \Rightarrow 2 \Rightarrow 1$.

**Lemma 1 (extra input and extra stack).** If $(q, x, \alpha) \vdash^* (p, \varepsilon, \beta)$, then $(q, xy, \alpha\gamma) \vdash^* (p, y, \beta\gamma)$ for all $y \in \Sigma^*$ and $\gamma \in \Gamma^*$. Conversely, if $(q, xy, X\gamma) \vdash^* (p, y, \gamma)$ and the stack has more than $|\gamma|$ symbols at every configuration of the run except the last, then $(q, x, X) \vdash^* (p, \varepsilon, \varepsilon)$ by the same moves.

*Proof.* A move depends only on the state, the top stack symbol and, if it reads, the next input symbol. In the first claim, every configuration of the run has a nonempty stack before its move, because a configuration with an empty stack has no move. So the top symbol of each configuration lies in the part that comes from $\alpha$, and the same move applies with $\gamma$ below and $y$ after the input; it never reads $y$, because the run reads exactly $x$. In the second claim the moves never pop a symbol of $\gamma$ before the last configuration, and they read exactly $x$, so removing $\gamma$ and $y$ leaves a valid run. $\square$

## From grammars to pushdown automata ($1 \Rightarrow 2$)

Let $G = (V, \Sigma, R, S)$. Define the PDA $P_G$ with one state $q$, stack alphabet $V \cup \Sigma$, start symbol $S$, and the moves

- $(q, \alpha) \in \delta(q, \varepsilon, A)$ for each production $A \to \alpha$ (*expand*);
- $(q, \varepsilon) \in \delta(q, a, a)$ for each $a \in \Sigma$ (*match*).

**Claim.** For all $x, y \in \Sigma^*$ and $\alpha \in (V \cup \Sigma)^*$: $(q, xy, \alpha) \vdash^* (q, y, \varepsilon)$ if and only if $\alpha \Rightarrow^*_{lm} x$.

*Proof of "if".* Induction on the pair (number $k$ of steps of the leftmost derivation, $|\alpha|$), ordered lexicographically. If $\alpha = \varepsilon$ then $x = \varepsilon$ and zero moves suffice. If $\alpha = a\alpha'$ with $a \in \Sigma$, a leftmost derivation from $\alpha$ never rewrites $a$, so $x = a x'$ and $\alpha' \Rightarrow^*_{lm} x'$ in $k$ steps; a match move gives $(q, a x' y, a \alpha') \vdash (q, x'y, \alpha')$, and the induction hypothesis, with the same $k$ and a shorter $\alpha$, finishes. If $\alpha = A\alpha'$ with $A \in V$, then $k \ge 1$, because $x$ has no nonterminal, and the first step rewrites the leftmost nonterminal $A$ by some $A \to \beta$: $\alpha \Rightarrow_{lm} \beta\alpha' \Rightarrow^*_{lm} x$ in $k - 1$ further steps. An expand move gives $(q, xy, A\alpha') \vdash (q, xy, \beta\alpha')$, and the induction hypothesis with $k - 1$ finishes.

*Proof of "only if".* Induction on the number $m$ of moves. If $m = 0$ then $\alpha = \varepsilon$ and $x = \varepsilon$. Otherwise look at the first move. If the top of the stack is a terminal $a$, the move is a match and reads $a$; the run reads exactly $x$, so $x = a x'$, and the remaining $m - 1$ moves give $(q, x'y, \alpha') \vdash^* (q, y, \varepsilon)$ where $\alpha = a\alpha'$. By induction $\alpha' \Rightarrow^*_{lm} x'$, so $\alpha \Rightarrow^*_{lm} a x' = x$. If the top is a nonterminal $A$, the move is an expand by some $A \to \beta$ and reads nothing, and the remaining moves give $(q, xy, \beta\alpha') \vdash^* (q, y, \varepsilon)$. By induction $\beta\alpha' \Rightarrow^*_{lm} x$, and since $A$ is the leftmost symbol of $\alpha = A\alpha'$, $\alpha \Rightarrow_{lm} \beta\alpha' \Rightarrow^*_{lm} x$. $\square$

With $\alpha = S$ and $y = \varepsilon$, the claim says $w \in N(P_G)$ exactly when $S \Rightarrow^* w$, since every derivation of a terminal string can be made leftmost. So $N(P_G) = L(G)$.

## Between the two kinds of acceptance ($2 \Leftrightarrow 3$)

**From empty stack to final state.** Given $P$, add a new start state $p_0$, a new final state $f$, and a new bottom symbol $X_0$. Add the moves $(q_0, Z_0 X_0) \in \delta'(p_0, \varepsilon, X_0)$ and $(f, \varepsilon) \in \delta'(q, \varepsilon, X_0)$ for each $q \in Q$, keep all moves of $P$, and start with $X_0$. Then $F' = \{f\}$. If $(q_0, w, Z_0) \vdash^* (q, \varepsilon, \varepsilon)$ in $P$, Lemma 1 gives $(p_0, w, X_0) \vdash (q_0, w, Z_0 X_0) \vdash^* (q, \varepsilon, X_0) \vdash (f, \varepsilon, \varepsilon)$. Conversely, an accepting run of $P'$ must enter $f$, which happens only by a move on top symbol $X_0$. Before that move, the moves of $P$ never see $X_0$ except at that point, because $P$ has no move on $X_0$, so the run is $(p_0, w, X_0) \vdash (q_0, w, Z_0 X_0) \vdash^* (q, w'', X_0) \vdash (f, w'', \varepsilon)$, and $f$ has no moves, so $w'' = \varepsilon$. By the second part of Lemma 1, $(q_0, w, Z_0) \vdash^* (q, \varepsilon, \varepsilon)$ in $P$. So $L(P') = N(P)$.

**From final state to empty stack.** Given $P$, add a new start state $p_0$, a new bottom symbol $X_0$ and a new state $e$. Add $(q_0, Z_0 X_0) \in \delta'(p_0, \varepsilon, X_0)$, add $(e, \varepsilon) \in \delta'(q, \varepsilon, Y)$ for each $q \in F$ and $Y \in \Gamma \cup \{X_0\}$, and add $(e, \varepsilon) \in \delta'(e, \varepsilon, Y)$ for each $Y \in \Gamma \cup \{X_0\}$. If $P$ accepts $w$ by final state in state $q \in F$ with stack $\gamma$, then $P'$ runs to $(q, \varepsilon, \gamma X_0)$ and empties its stack in state $e$. Conversely, the stack of $P'$ becomes empty only when $X_0$ is popped, which only $e$ and the states of $F$ do, by the new moves. Before the first entry into $e$ or such a pop, the run is a run of $P$ with $X_0$ below; it ends in a state of $F$, and $e$ reads no input, so all of $w$ was read when the run of $P$ reached that state of $F$. So $N(P') = L(P)$.

## From pushdown automata to grammars ($2 \Rightarrow 1$)

Let $P$ accept by empty stack. Define $G_P$ with start symbol $S$ and nonterminals $[pXq]$ for $p, q \in Q$ and $X \in \Gamma$, and the productions

- $S \to [q_0 Z_0 p]$ for each $p \in Q$;
- for each move $(r, Y_1 \cdots Y_k) \in \delta(q, a, X)$ with $a \in \Sigma \cup \{\varepsilon\}$ and $k \ge 0$, and for all states $r_1, \ldots, r_k$, the production $[q X r_k] \to a\, [r Y_1 r_1][r_1 Y_2 r_2] \cdots [r_{k-1} Y_k r_k]$, where for $k = 0$ the production is $[q X r] \to a$.

**Claim.** $[qXp] \Rightarrow^* w$ if and only if $(q, w, X) \vdash^* (p, \varepsilon, \varepsilon)$.

*Proof of "if".* Induction on the number $m \ge 1$ of moves. The first move uses some $(r, Y_1 \cdots Y_k) \in \delta(q, a, X)$ and reads $a$, so $w = a w'$ and $(r, w', Y_1 \cdots Y_k) \vdash^{m-1} (p, \varepsilon, \varepsilon)$. If $k = 0$ then $m = 1$, $r = p$, $w' = \varepsilon$, and $[qXp] \to a$ is a production. If $k \ge 1$, let $r_0 = r$, and for $i = 1, \ldots, k$ let $r_i$ be the state at the first configuration of the remaining run whose stack is $Y_{i+1} \cdots Y_k$, and $w_i$ the input read between the configurations for $i - 1$ and $i$. The stack shrinks by at most one symbol per move, so these configurations exist and come in order, and $r_k = p$, $w' = w_1 \cdots w_k$. Between them the stack is longer than $k - i$, so by the second part of Lemma 1, $(r_{i-1}, w_i, Y_i) \vdash^* (r_i, \varepsilon, \varepsilon)$ in fewer than $m$ moves. By induction $[r_{i-1} Y_i r_i] \Rightarrow^* w_i$, and the production $[qXp] \to a [r_0 Y_1 r_1] \cdots [r_{k-1} Y_k r_k]$ gives $[qXp] \Rightarrow^* a w_1 \cdots w_k = w$.

*Proof of "only if".* Induction on the length of the derivation. Its first step uses a production $[qXp] \to a [r_0 Y_1 r_1] \cdots [r_{k-1} Y_k r_k]$ with $r_k = p$ that comes from a move $(r_0, Y_1 \cdots Y_k) \in \delta(q, a, X)$, and $w = a w_1 \cdots w_k$ with $[r_{i-1} Y_i r_i] \Rightarrow^* w_i$ by shorter derivations. By induction $(r_{i-1}, w_i, Y_i) \vdash^* (r_i, \varepsilon, \varepsilon)$, and by the first part of Lemma 1, $(r_{i-1}, w_i \cdots w_k, Y_i \cdots Y_k) \vdash^* (r_i, w_{i+1} \cdots w_k, Y_{i+1} \cdots Y_k)$. Chaining these after the move $(q, w, X) \vdash (r_0, w_1 \cdots w_k, Y_1 \cdots Y_k)$ gives $(q, w, X) \vdash^* (p, \varepsilon, \varepsilon)$. $\square$

By the claim, $S \Rightarrow^* w$ exactly when $(q_0, w, Z_0) \vdash^* (p, \varepsilon, \varepsilon)$ for some $p$, that is, $L(G_P) = N(P)$.

## Conclusion

$1 \Rightarrow 2$ is the construction of $P_G$, $2 \Rightarrow 3$ and $3 \Rightarrow 2$ are the two conversions between kinds of acceptance, and $2 \Rightarrow 1$ is the construction of $G_P$. All are effective. $\blacksquare$
