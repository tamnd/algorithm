---
title: The product construction accepts exactly the strings on which the Boolean operation of the two languages is true
proves: [correctness, termination]
status: full
---

Let $M_1 = (Q_1, \Sigma, \delta_1, s_1, F_1)$ and $M_2 = (Q_2, \Sigma, \delta_2, s_2, F_2)$ be complete DFAs over the same alphabet, with $\delta_i : Q_i \times \Sigma \to Q_i$, and let $\mathrm{op} : \{0, 1\}^2 \to \{0, 1\}$ be a Boolean function. Let $P = (Q, \Sigma, \delta, s, F)$ be the output of PRODUCT$(M_1, M_2, \mathrm{op})$. Write $\delta_i^*$ for the extension to strings: $\delta_i^*(q, \varepsilon) = q$ and $\delta_i^*(q, va) = \delta_i(\delta_i^*(q, v), a)$.

**Lemma 1 (termination and reachability).** The algorithm stops. Its set $Q$ is the set of pairs $(\delta_1^*(s_1, w), \delta_2^*(s_2, w))$ for $w \in \Sigma^*$, and $\delta$ is defined on each pair of $Q$ and each symbol.

*Proof.* A pair enters $W$ only when it enters $Q$, at line L2 or line L7, and never leaves $Q$. So each pair of $Q_1 \times Q_2$ enters $W$ at most once, the loop makes at most $|Q_1| |Q_2|$ passes, and each pass does $|\Sigma|$ steps. Each pair that enters $Q$ is removed from $W$ later, and then line L8 defines its move on each symbol.

Each pair of $Q$ has the stated form: $s = (\delta_1^*(s_1, \varepsilon), \delta_2^*(s_2, \varepsilon))$, and if $(p, q) = (\delta_1^*(s_1, w), \delta_2^*(s_2, w))$, then line L6 adds $(\delta_1(p, a), \delta_2(q, a)) = (\delta_1^*(s_1, wa), \delta_2^*(s_2, wa))$. Conversely, by induction on $|w|$, the pair of $w$ is in $Q$: true for $\varepsilon$, and if the pair of $w$ is in $Q$, it is removed from $W$ at some time, and line L7 puts the pair of $wa$ in $Q$. $\square$

**Lemma 2 (the run of the product).** For each $w \in \Sigma^*$, $\delta^*(s, w) = (\delta_1^*(s_1, w), \delta_2^*(s_2, w))$.

*Proof.* By induction on $|w|$. For $w = \varepsilon$ both sides are $s = (s_1, s_2)$. If the claim holds for $w$, with the pair $(p, q)$, then $\delta^*(s, wa) = \delta((p, q), a) = (\delta_1(p, a), \delta_2(q, a))$ by line L6 and line L8, and this is $(\delta_1^*(s_1, wa), \delta_2^*(s_2, wa))$. $\square$

**Theorem.** $P$ is a complete DFA on its states, and for each $w \in \Sigma^*$,

$$w \in L(P) \iff \mathrm{op}\big(w \in L(M_1),\ w \in L(M_2)\big).$$

In particular, op = and gives $L(M_1) \cap L(M_2)$, op = or gives $L(M_1) \cup L(M_2)$, $\mathrm{op}(x, y) = x \wedge \neg y$ gives $L(M_1) \setminus L(M_2)$, and op = xor gives the symmetric difference.

*Proof.* By Lemma 1, each state of $P$ has a move on each symbol, and the move is one pair of $Q$. By Lemma 2 and line L9, $\delta^*(s, w) \in F$ if and only if $\mathrm{op}(\delta_1^*(s_1, w) \in F_1, \delta_2^*(s_2, w) \in F_2)$, and $\delta_i^*(s_i, w) \in F_i$ if and only if $w \in L(M_i)$. $\blacksquare$

**Why completeness is needed.** If $M_2$ has no move on $(q, a)$, then line L6 has no pair to build, and each string $w$ that drives $M_2$ into this gap is rejected by $P$, whatever the value of op. For op = or, a string in $L(M_1)$ that falls into the gap of $M_2$ must be accepted, so the result is wrong. For op = and it is still correct, because such a string is not in $L(M_2)$. To use any other op, first add a dead state to each input.

**Running time.** By Lemma 1 there are $N \le |Q_1| |Q_2|$ passes, each with $|\Sigma|$ lookups and one dictionary test per symbol, so the time is $O(N |\Sigma|)$ with hashing, and $O(|Q_1| |Q_2| |\Sigma|)$ in the worst case. The table has $N |\Sigma|$ entries.
