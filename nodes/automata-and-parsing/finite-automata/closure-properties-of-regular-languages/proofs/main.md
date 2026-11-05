---
title: Proof of the closure properties of regular languages
proves: [statement]
status: full
---

Fix finite alphabets $\Sigma$ and $\Delta$. Let $L_1 = L(M_1)$ and $L_2 = L(M_2)$ with complete DFAs $M_i = (Q_i, \Sigma, \delta_i, q_i, F_i)$, where $\delta_i : Q_i \times \Sigma \to Q_i$ and there are no $\varepsilon$-moves. We use the lemma $\delta^*(q, xy) = \delta^*(\delta^*(q, x), y)$ of the [DFA](/deterministic-finite-automaton/) page, and we use [Kleene's theorem](/kleene-theorem/): a language is regular if and only if a complete DFA, an NFA, an [epsilon-NFA](/epsilon-nfa/) or a regular expression describes it. For an NFA or an epsilon-NFA we write $p \overset{w}{\leadsto} r$ when some path from $p$ to $r$ has the label $w$, as in the proof of Kleene's theorem.

## Part 1: complement

**Claim.** $\overline{L_1} = \Sigma^* \setminus L_1$ is regular.

*Proof.* Let $M' = (Q_1, \Sigma, \delta_1, q_1, Q_1 \setminus F_1)$. The machines $M_1$ and $M'$ have the same transition function, so they reach the same state $\delta_1^*(q_1, w)$ on each $w \in \Sigma^*$. This state is defined because $\delta_1$ is complete. So $w \in L(M')$ if and only if $\delta_1^*(q_1, w) \notin F_1$, if and only if $w \notin L_1$. $\square$

The proof uses both determinism and completeness. Each string has exactly one run, so "the run does not end in $F_1$" is the same as "no run ends in $F_1$".

## Part 2: the product and the Boolean operations

Let $P = (Q_1 \times Q_2, \Sigma, \delta, (q_1, q_2), F)$ with $\delta((p, r), a) = (\delta_1(p, a), \delta_2(r, a))$, where $F$ is chosen below. This is the [product construction](/product-construction/). It is a complete DFA.

**Lemma 1.** For all $p \in Q_1$, $r \in Q_2$ and $w \in \Sigma^*$, $\delta^*((p, r), w) = (\delta_1^*(p, w), \delta_2^*(r, w))$.

*Proof.* By induction on $|w|$. For $w = \varepsilon$ both sides are $(p, r)$. For $w = va$, by the induction hypothesis and the definition of $\delta$,

$$\delta^*((p, r), va) = \delta(\delta^*((p, r), v), a) = \delta((\delta_1^*(p, v), \delta_2^*(r, v)), a) = (\delta_1^*(p, va), \delta_2^*(r, va)). \quad \square$$

**Claim.** $L_1 \cap L_2$, $L_1 \cup L_2$, $L_1 \setminus L_2$ and $L_1 \triangle L_2$ are regular.

*Proof.* By Lemma 1, $w \in L(P)$ if and only if $(\delta_1^*(q_1, w), \delta_2^*(q_2, w)) \in F$. Take

- $F = F_1 \times F_2$: then $w \in L(P)$ if and only if $w \in L_1$ and $w \in L_2$;
- $F = (F_1 \times Q_2) \cup (Q_1 \times F_2)$: then $w \in L(P)$ if and only if $w \in L_1$ or $w \in L_2$;
- $F = F_1 \times (Q_2 \setminus F_2)$: then $w \in L(P)$ if and only if $w \in L_1$ and $w \notin L_2$;
- $F = (F_1 \times (Q_2 \setminus F_2)) \cup ((Q_1 \setminus F_1) \times F_2)$: then $w \in L(P)$ if and only if exactly one of $w \in L_1$, $w \in L_2$ holds. $\square$

The same argument works for each Boolean function $\beta$ of two arguments, with $F = \{ (p, r) : \beta([p \in F_1], [r \in F_2]) \}$. It also works for $k$ DFAs at once, with $\prod_i |Q_i|$ states. For the union, both DFAs must be complete: if $\delta_1^*(q_1, w)$ were undefined, the product would have no state for $w$ even when $w \in L_2$.

## Part 3: concatenation

**Claim.** $L_1 L_2 = \{ xy : x \in L_1, y \in L_2 \}$ is regular.

*Proof.* Assume $Q_1 \cap Q_2 = \emptyset$. Let $N$ be the epsilon-NFA with the states $Q_1 \cup Q_2$, the start state $q_1$, the accepting states $F_2$, the transitions $\delta_1(p, a) \in \delta_N(p, a)$ for $p \in Q_1$ and $\delta_2(r, a) \in \delta_N(r, a)$ for $r \in Q_2$, and one $\varepsilon$-move $f \to q_2$ for each $f \in F_1$.

Let $w \in L(N)$, with a path from $q_1$ to some $g \in F_2$. The path starts in $Q_1$ and ends in $Q_2$. The only transitions from a state of $Q_1$ to a state of $Q_2$ are the $\varepsilon$-moves $f \to q_2$ with $f \in F_1$, and no transition leads from $Q_2$ to $Q_1$. So the path uses exactly one of these moves. Before it, the path follows $\delta_1$ from $q_1$ to $f$ with some label $x$, so $\delta_1^*(q_1, x) = f \in F_1$ and $x \in L_1$. After it, the path follows $\delta_2$ from $q_2$ to $g$ with some label $y$, so $y \in L_2$. Hence $w = xy \in L_1 L_2$.

Conversely, let $x \in L_1$ and $y \in L_2$. The run of $M_1$ on $x$ is a path of $N$ from $q_1$ to $f = \delta_1^*(q_1, x) \in F_1$. Follow it by the move $f \to q_2$ and by the run of $M_2$ on $y$, which ends in $F_2$. This is a path with the label $xy$, so $xy \in L(N)$. By Kleene's theorem $L(N)$ is regular. $\square$

## Part 4: Kleene star

**Claim.** $L_1^* = \bigcup_{k \ge 0} L_1^k$ is regular.

*Proof.* Let $s \notin Q_1$ be a new state. Let $N$ be the epsilon-NFA with the states $Q_1 \cup \{s\}$, the start state $s$, the accepting states $\{s\}$, the transitions of $M_1$, an $\varepsilon$-move $s \to q_1$, and an $\varepsilon$-move $f \to s$ for each $f \in F_1$.

Let $w \in L(N)$, with a path from $s$ to $s$. Cut the path at each visit to $s$. The path with zero transitions gives $w = \varepsilon \in L_1^0$. Otherwise each piece goes from $s$ to $s$ without visiting $s$ in between. The only move out of $s$ is $s \to q_1$, and the only moves into $s$ are $f \to s$ with $f \in F_1$. So a piece is $s \to q_1$, then a path that follows $\delta_1$ from $q_1$ to some $f \in F_1$ with some label $x_j$, then $f \to s$. Hence $\delta_1^*(q_1, x_j) \in F_1$, each $x_j \in L_1$, and $w = x_1 \cdots x_k \in L_1^k$.

Conversely, $\varepsilon \in L(N)$ by the path with zero transitions. For $x_1, \ldots, x_k \in L_1$ with $k \ge 1$, join the pieces $s \to q_1$, the run of $M_1$ on $x_j$, and the move from its last state, which is in $F_1$, to $s$. This is a path from $s$ to $s$ with the label $x_1 \cdots x_k$. So $L(N) = L_1^*$, and it is regular by Kleene's theorem. $\square$

The new state $s$ is necessary. If we made $q_1$ accepting and added $\varepsilon$-moves $f \to q_1$ instead, a path could return to $q_1$ along a transition of $M_1$ and stop there, in the middle of a word of $L_1$.

## Part 5: reversal

**Claim.** $L_1^R = \{ w^R : w \in L_1 \}$ is regular, where $(a_1 \cdots a_m)^R = a_m \cdots a_1$.

*Proof.* Let $N$ be the epsilon-NFA with the states $Q_1 \cup \{s\}$, where $s$ is new, the start state $s$, the accepting states $\{q_1\}$, an $\varepsilon$-move $s \to f$ for each $f \in F_1$, and a transition $p \in \delta_N(r, a)$ for each transition $\delta_1(p, a) = r$ of $M_1$. So the arrows of $M_1$ are reversed.

A sequence $r_0, r_1, \ldots, r_m$ with $r_t = \delta_1(r_{t-1}, a_t)$ is a path of $M_1$ with the label $a_1 \cdots a_m$ if and only if $r_m, r_{m-1}, \ldots, r_0$ is a path of the reversed transitions with the label $a_m \cdots a_1$. So $w \in L_1$, which means that some path of $M_1$ leads from $q_1$ to some $f \in F_1$ with the label $w$, holds if and only if the path $s \to f$ followed by a reversed path from $f$ to $q_1$ with the label $w^R$ exists, which means $w^R \in L(N)$. So $L(N) = L_1^R$. $\square$

The reversed machine is nondeterministic: a state can have several incoming transitions on one symbol in $M_1$, and $F_1$ can have several states.

## Part 6: homomorphism

A homomorphism is a map $h : \Sigma^* \to \Delta^*$ with $h(xy) = h(x)h(y)$ for all $x, y$. It is fixed by the strings $h(a)$ for $a \in \Sigma$, since $h(a_1 \cdots a_m) = h(a_1) \cdots h(a_m)$ and $h(\varepsilon) = \varepsilon$. For a language $L$, $h(L) = \{ h(w) : w \in L \}$.

**Claim.** If $L \subseteq \Sigma^*$ is regular, then $h(L) \subseteq \Delta^*$ is regular.

*Proof.* By Kleene's theorem $L = L(E)$ for a regular expression $E$ over $\Sigma$. Let $h(E)$ be the expression over $\Delta$ obtained by replacing each occurrence of a symbol $a$ with an expression for the one string $h(a)$: the concatenation of its symbols, or $\varepsilon$ if $h(a) = \varepsilon$. We show $L(h(E)) = h(L(E))$ by structural induction on $E$.

- $E = \emptyset$: $h(\emptyset) = \emptyset$. $E = \varepsilon$: $h(\{\varepsilon\}) = \{\varepsilon\}$. $E = a$: $L(h(a)) = \{h(a)\} = h(\{a\})$.
- $E = E_1 + E_2$: $h(A \cup B) = h(A) \cup h(B)$ for all languages $A, B$, by the definition of the image.
- $E = E_1 E_2$: $h(AB) = \{ h(xy) : x \in A, y \in B \} = \{ h(x)h(y) \} = h(A)h(B)$.
- $E = E_1^*$: $h(A^k) = h(A)^k$ for each $k$, by the previous case and induction on $k$, and so $h(A^*) = \bigcup_k h(A^k) = \bigcup_k h(A)^k = h(A)^*$.

In each case the induction hypothesis gives the expressions for the parts. So $h(L) = L(h(E))$ is regular. $\square$

## Part 7: inverse homomorphism

For $L \subseteq \Delta^*$, let $h^{-1}(L) = \{ w \in \Sigma^* : h(w) \in L \}$.

**Claim.** If $L \subseteq \Delta^*$ is regular, then $h^{-1}(L) \subseteq \Sigma^*$ is regular.

*Proof.* Let $M = (Q, \Delta, \delta, q_0, F)$ be a complete DFA for $L$. Define $M' = (Q, \Sigma, \delta', q_0, F)$ with $\delta'(q, a) = \delta^*(q, h(a))$ for $a \in \Sigma$. It is a complete DFA over $\Sigma$, since $\delta^*$ is defined for each string.

We show $\delta'^*(q, w) = \delta^*(q, h(w))$ by induction on $|w|$. For $w = \varepsilon$ both sides are $q$. For $w = va$, by the induction hypothesis and the lemma $\delta^*(q, xy) = \delta^*(\delta^*(q, x), y)$,

$$\delta'^*(q, va) = \delta'(\delta^*(q, h(v)), a) = \delta^*(\delta^*(q, h(v)), h(a)) = \delta^*(q, h(v)h(a)) = \delta^*(q, h(va)).$$

So $w \in L(M')$ if and only if $\delta^*(q_0, h(w)) \in F$, if and only if $h(w) \in L$. $\square$

## Part 8: right quotient

For languages $L$ and $K$ over $\Sigma$, let $L / K = \{ x : xy \in L \text{ for some } y \in K \}$.

**Claim.** If $L$ is regular, then $L / K$ is regular for each language $K$, regular or not.

*Proof.* Let $M = (Q, \Sigma, \delta, q_0, F)$ be a complete DFA for $L$, and let $F' = \{ q \in Q : \delta^*(q, y) \in F \text{ for some } y \in K \}$. By the lemma $\delta^*(q_0, xy) = \delta^*(\delta^*(q_0, x), y)$, the DFA $(Q, \Sigma, \delta, q_0, F')$ accepts $x$ if and only if some $y \in K$ has $xy \in L$. $\square$

The set $F'$ exists for every $K$, but a program can compute it only when it can decide, for each $q$, whether $K$ meets $\{ y : \delta^*(q, y) \in F \}$. For a regular $K$ this is an emptiness test of a product.

All eight parts together prove the theorem. $\blacksquare$
