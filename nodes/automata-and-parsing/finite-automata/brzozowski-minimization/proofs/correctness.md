---
title: Brzozowski's algorithm outputs the minimal DFA
proves: [correctness, termination]
status: full
---

Let $N = (Q, \Sigma, \delta, I, F)$ be an NFA with a set $I$ of start states and no $\varepsilon$-moves. For a set $S \subseteq Q$ and a string $w$, let $\hat\delta(S, w)$ be the set of states reachable from $S$ by a path labelled $w$: $\hat\delta(S, \varepsilon) = S$ and $\hat\delta(S, wa) = \bigcup_{q \in \hat\delta(S, w)} \delta(q, a)$. $N$ accepts $w$ when $\hat\delta(I, w) \cap F \neq \emptyset$.

## Part 1: the subset construction

**Lemma 1.** DETERMINIZE (lines L6 to L13) stops, and returns a complete DFA $\det(N)$ that accepts $L(N)$, whose states are exactly the sets $\hat\delta(I, w)$ for $w \in \Sigma^*$, with the state reached on $w$ equal to $\hat\delta(I, w)$.

*Proof.* Each subset gets a number at most once (line L10), and there are at most $2^{|Q|}$ subsets, so the loop of line L7 runs at most $2^{|Q|}$ times and stops. Line L9 sets $\delta'(S, a) = \hat\delta(S, a)$, and every numbered subset is processed, so $\delta'$ is total. By induction on $|w|$, the state reached on $w$ is $\hat\delta(I, w)$: for $w = \varepsilon$ it is $S_0 = I$, and if it is $\hat\delta(I, w)$ for $w$, then on $wa$ it is $\hat\delta(\hat\delta(I, w), a) = \hat\delta(I, wa)$. Every numbered subset was found from $S_0$ by a sequence of moves, so it is $\hat\delta(I, w)$ for some $w$, and each such set is numbered because the search follows every move of every numbered subset. Line L12 makes the state of $w$ accepting if and only if $\hat\delta(I, w) \cap F \neq \emptyset$, that is, if and only if $w \in L(N)$. $\square$

## Part 2: reversal

**Lemma 2.** $\mathrm{rev}(N) = (Q, \Sigma, \delta^R, F, I)$, with $\delta^R(q, a) = \{ p : q \in \delta(p, a) \}$, accepts $L(N)^R$. More precisely, $p \in \hat\delta^R(S, w)$ if and only if $\hat\delta(\{p\}, w^R) \cap S \neq \emptyset$.

*Proof.* A path $q_0 \xrightarrow{a_1} q_1 \cdots \xrightarrow{a_m} q_m$ in $N$ is the same as a path $q_m \xrightarrow{a_m} \cdots \xrightarrow{a_1} q_0$ in $\mathrm{rev}(N)$, by the definition of $\delta^R$. So $\mathrm{rev}(N)$ has a path labelled $w$ from some state of $S$ to $p$ if and only if $N$ has a path labelled $w^R$ from $p$ to some state of $S$. With $S = F$ and $p \in I$ this says that $\mathrm{rev}(N)$ accepts $w$ if and only if $N$ accepts $w^R$. $\square$

## Part 3: determinizing the reverse of a reachable DFA

**Theorem.** Let $D = (P, \Sigma, \eta, p_0, G)$ be a deterministic automaton, where $\eta$ may be partial, in which every state is reachable from $p_0$. Then $\det(\mathrm{rev}(D))$ is the minimal complete DFA for $L(D)^R$.

*Proof.* Write $\eta^*(p, x)$ for the state reached from $p$ on $x$, when it is defined. By Lemma 1, the state of $\det(\mathrm{rev}(D))$ reached on $w$ is $S_w = \hat\eta^R(G, w)$, and by Lemma 2,

$$S_w = \{ p \in P : \eta^*(p, w^R) \text{ is defined and lies in } G \}.$$

By Lemma 1 and Lemma 2, $\det(\mathrm{rev}(D))$ accepts $L(D)^R$, and all its states are reachable.

Let $S_u \neq S_v$ be two of its states, and take $p$ in one of them and not in the other, say $p \in S_u \setminus S_v$. Since $p$ is reachable in $D$, there is $x$ with $\eta^*(p_0, x) = p$. Since $D$ is deterministic, $\eta^*(p_0, x y)$ is defined if and only if $\eta^*(p, y)$ is, and then they are equal. Now

$$p_0 \in S_{u x^R} \iff \eta^*(p_0, (u x^R)^R) \in G \iff \eta^*(p_0, x u^R) \in G \iff \eta^*(p, u^R) \in G \iff p \in S_u,$$

and the same holds for $v$. The state $S_{u x^R}$ is the state reached from $S_u$ on $x^R$, and it is accepting if and only if it contains $p_0$, because the accepting states of $\mathrm{rev}(D)$ form the set $\{p_0\}$. So $x^R$ is accepted from $S_u$ and rejected from $S_v$, and the two states are not equivalent.

So $\det(\mathrm{rev}(D))$ is a complete DFA for $L(D)^R$ whose states are all reachable and pairwise inequivalent. By Part 3 of the uniqueness theorem for minimal DFAs, it is the minimal complete DFA for $L(D)^R$. $\square$

## Part 4: the algorithm

Lines L1 and L2 compute $D_1 = \det(\mathrm{rev}(N))$. By Lemmas 1 and 2, $D_1$ is a complete DFA for $L(N)^R$ with all states reachable. Line L3 computes $\mathrm{rev}(D_1)$, an NFA with the single start set $F_1$ (the accepting states of $D_1$) and the single accepting state, the start state of $D_1$. Line L4 computes $\det(\mathrm{rev}(D_1))$. By the theorem of Part 3 with $D = D_1$, this is the minimal complete DFA for $L(D_1)^R = (L(N)^R)^R = L(N)$. Both calls of DETERMINIZE stop by Lemma 1, and lines L1 and L3 are single passes over the transitions, so the algorithm stops and line L5 returns the minimal complete DFA for $L(N)$. $\blacksquare$
