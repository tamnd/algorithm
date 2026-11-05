---
title: The subset construction builds a complete DFA with the language of the NFA
proves: [correctness, termination]
status: full
---

Let $N = (Q, \Sigma, \delta, q_0, F)$ be the input, with $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to \mathcal{P}(Q)$. For $S \subseteq Q$, let $E(S)$ be the set of states $r$ such that there is a path $p_0, p_1, \ldots, p_k$ with $k \ge 0$, $p_0 \in S$, $p_k = r$ and $p_i \in \delta(p_{i-1}, \varepsilon)$ for $1 \le i \le k$. For $S \subseteq Q$ and $a \in \Sigma$, let $\mathrm{step}(S, a) = \bigcup_{q \in S} \delta(q, a)$.

A *run* of $N$ on $w = a_1 \cdots a_\ell$ is a sequence of states joined by moves, which starts in $q_0$, whose labels in order are $a_1, \ldots, a_\ell$ with any number of $\varepsilon$ labels between them, before them and after them. Let $R(w)$ be the set of the last states of the runs on $w$. By definition, $w \in L(N)$ if and only if $R(w) \cap F \ne \emptyset$.

**Lemma 1 (CLOSE).** CLOSE$(S)$ stops and returns $E(S)$.

*Proof.* A state enters $C$ at most once, and it is pushed on $K$ only when it enters $C$, so line L13 runs at most $|Q|$ times and the loop stops. We show two inclusions for the returned $C$.

$C \subseteq E(S)$: at line L11, $C = S \subseteq E(S)$, because a path with $k = 0$ is allowed. Line L14 adds $r$ only when $r \in \delta(q, \varepsilon)$ for some $q \in C$. If $q \in E(S)$ by a path ending in $q$, then that path followed by $r$ shows $r \in E(S)$. So $C \subseteq E(S)$ holds after each step.

$E(S) \subseteq C$: each state of $C$ is pushed once and popped once before the loop ends, and when $q$ is popped, line L14 adds each element of $\delta(q, \varepsilon)$ to $C$. So the final $C$ contains $S$ and is closed under $\varepsilon$-moves: $q \in C$ and $r \in \delta(q, \varepsilon)$ give $r \in C$. By induction on $k$, the last state of each path $p_0, \ldots, p_k$ with $p_0 \in S$ lies in $C$. $\square$

**Lemma 2.** $R(\varepsilon) = E(\{q_0\})$, and $R(wa) = E(\mathrm{step}(R(w), a))$ for each $w \in \Sigma^*$ and $a \in \Sigma$.

*Proof.* A run on $\varepsilon$ is a path of $\varepsilon$-moves from $q_0$, so $R(\varepsilon) = E(\{q_0\})$. A run on $wa$ has exactly one move labelled $a$, the last move with a symbol label. Cut the run there. The part before the move is a run on $w$, ending in a state $q \in R(w)$. The move goes to a state $p \in \delta(q, a)$, so $p \in \mathrm{step}(R(w), a)$. The part after the move is a path of $\varepsilon$-moves from $p$, so the last state is in $E(\mathrm{step}(R(w), a))$. Conversely, each $q \in R(w)$ with a run on $w$, each $p \in \delta(q, a)$ and each path of $\varepsilon$-moves from $p$ join into a run on $wa$. $\square$

**Lemma 3 (termination and completeness).** The loop of line L3 stops. At the end, $\delta'(S, a)$ is defined for each $S \in Q'$ and each $a \in \Sigma$, and $\delta'(S, a) \in Q'$.

*Proof.* A set enters $W$ only at line L2 or line L7, and only when it is not yet in $Q'$, after which it is in $Q'$. Sets are never removed from $Q'$. So each set enters $W$ at most once, and since $Q' \subseteq \mathcal{P}(Q)$, the loop runs at most $2^{|Q|}$ times. Each run of the loop removes one set, so the loop stops, and each set of $Q'$ is removed once. When $S$ is removed, lines L5 to L8 define $\delta'(S, a)$ for each $a \in \Sigma$, and line L7 puts the value into $Q'$ before line L8 uses it. $\square$

**Theorem.** The DFA $D = (Q', \Sigma, \delta', S_0, F')$ returned at line L10 is complete, each of its states is reachable from $S_0$, and $L(D) = L(N)$.

*Proof.* Completeness is Lemma 3. Each set is put into $Q'$ at line L2, as $S_0$, or at line L7 as $\delta'(S, a)$ of a set $S$ already in $Q'$; by induction on the order of insertion, each set of $Q'$ is reachable from $S_0$.

We prove $\delta'^*(S_0, w) = R(w)$ by induction on $|w|$. For $w = \varepsilon$, $\delta'^*(S_0, \varepsilon) = S_0 = $ CLOSE$(\{q_0\}) = E(\{q_0\}) = R(\varepsilon)$ by Lemma 1 and Lemma 2. For $wa$, let $S = \delta'^*(S_0, w)$, which equals $R(w)$ by the induction hypothesis. By line L6 and Lemma 1, $\delta'(S, a) = E(\mathrm{step}(S, a))$, which is $R(wa)$ by Lemma 2. So $\delta'^*(S_0, wa) = \delta'(S, a) = R(wa)$.

By line L9, $D$ accepts $w$ if and only if $\delta'^*(S_0, w) \cap F \ne \emptyset$, that is, $R(w) \cap F \ne \emptyset$, that is, $w \in L(N)$. $\blacksquare$
