---
title: The tableau automaton accepts exactly the words of the formula, and its size is 2^O(|φ|)
proves: [correctness, complexity]
status: full
---

We use the pseudocode and the notation of the page. The formula $\varphi$ is already rewritten with $\mathsf{true}$, atomic propositions, $\neg$, $\wedge$, $\mathsf{X}$ and $\mathsf{U}$; this rewriting keeps the set of words that satisfy the formula, so it is enough to prove the claims for the rewritten formula. We write $\mathit{cl}$ for its closure, $AP_\varphi$ for its atomic propositions, and $\sigma^i$ for the suffix $\sigma[i]\sigma[i+1]\ldots$ of a word $\sigma$. A sequence $B_0 B_1 \ldots$ of elementary sets is a *run on $\sigma$* if $B_0 \in Q_0$, $B_i \to B_{i+1}$ for each $i$, and $B_i \cap AP = \sigma[i] \cap AP_\varphi$ for each $i$. It is *accepting* if for each until formula $u = \psi_1\, \mathsf{U}\, \psi_2$ of $\mathit{cl}$, it meets $F_u$ at infinitely many positions.

We use the *expansion law* of until, which follows directly from the semantics: $\sigma^i \models \psi_1\, \mathsf{U}\, \psi_2$ iff $\sigma^i \models \psi_2$, or $\sigma^i \models \psi_1$ and $\sigma^{i+1} \models \psi_1\, \mathsf{U}\, \psi_2$.

**Lemma 1 (every model has an accepting run).** If $\sigma \models \varphi$, then the GBA has an accepting run on $\sigma$.

*Proof.* Let $B_i = \{\psi \in \mathit{cl} : \sigma^i \models \psi\}$.

- *Each $B_i$ is elementary.* $\mathsf{true} \in B_i$, and the rules for $\neg$ and $\wedge$ are the semantics of these connectives. If $\sigma^i \models \psi_2$, then $\sigma^i \models \psi_1\, \mathsf{U}\, \psi_2$, with the witness position $i$. If $\sigma^i \models \psi_1\, \mathsf{U}\, \psi_2$ and $\sigma^i \not\models \psi_2$, then the witness position is some $j > i$, so $\psi_1$ holds at $i$.
- *Labels.* For $p \in AP_\varphi$, $p \in B_i$ iff $\sigma^i \models p$ iff $p \in \sigma[i]$.
- *Initial state.* $\varphi \in B_0$ because $\sigma \models \varphi$.
- *Transitions.* For $\mathsf{X}\psi \in \mathit{cl}$: $\mathsf{X}\psi \in B_i$ iff $\sigma^{i+1} \models \psi$ iff $\psi \in B_{i+1}$, which is the test of line L6. For an until formula, the test of line L7 for the pair $(B_i, B_{i+1})$ is the expansion law at position $i$.
- *Acceptance.* Let $u = \psi_1\, \mathsf{U}\, \psi_2 \in \mathit{cl}$. Suppose that only finitely many $B_i$ are in $F_u$. Then there is $N$ such that for each $i \ge N$, $u \in B_i$ and $\psi_2 \notin B_i$. As $u \in B_N$, $\sigma^N \models u$, so some $j \ge N$ has $\sigma^j \models \psi_2$, that is $\psi_2 \in B_j$. This is a contradiction. $\square$

**Lemma 2 (every accepting run is correct).** Let $B_0 B_1 \ldots$ be an accepting run on $\sigma$. Then for each $\psi \in \mathit{cl}$ and each $i \ge 0$: $\psi \in B_i$ iff $\sigma^i \models \psi$.

*Proof.* By induction on the structure of $\psi$, for all $i$ at once.

- $\psi = \mathsf{true}$: $\mathsf{true}$ is in each elementary set and holds everywhere.
- $\psi = p$: $p \in B_i$ iff $p \in \sigma[i]$, by the label condition, since $p \in AP_\varphi$.
- $\psi = \neg\chi$ or $\psi = \chi_1 \wedge \chi_2$: by the rules of elementary sets and the induction hypothesis.
- $\psi = \mathsf{X}\chi$: by line L6, $\mathsf{X}\chi \in B_i$ iff $\chi \in B_{i+1}$, iff $\sigma^{i+1} \models \chi$ by the induction hypothesis, iff $\sigma^i \models \mathsf{X}\chi$.
- $\psi = u = \psi_1\, \mathsf{U}\, \psi_2$. Line L7 for the pair $(B_l, B_{l+1})$ says: $u \in B_l$ iff $\psi_2 \in B_l$, or $\psi_1 \in B_l$ and $u \in B_{l+1}$. (*)

  *If $\sigma^i \models u$, then $u \in B_i$.* Let $j \ge i$ be the least position with $\sigma^j \models \psi_2$; then $\sigma^l \models \psi_1$ for $i \le l < j$. By the induction hypothesis, $\psi_2 \in B_j$ and $\psi_1 \in B_l$ for $i \le l < j$. By (*), $u \in B_j$. Going down from $l = j - 1$ to $l = i$, (*) gives $u \in B_l$ from $\psi_1 \in B_l$ and $u \in B_{l+1}$. So $u \in B_i$.

  *If $u \in B_i$, then $\sigma^i \models u$.* The run meets $F_u$ infinitely often, so there is a least $j \ge i$ with $B_j \in F_u$, that is $u \notin B_j$ or $\psi_2 \in B_j$. For each $l$ with $i \le l < j$, $B_l \notin F_u$, so $u \in B_l$ and $\psi_2 \notin B_l$; then (*) gives $\psi_1 \in B_l$ and $u \in B_{l+1}$. By induction on $l$ from $i$, $u \in B_l$ for $i \le l \le j$. So $u \in B_j$, and $B_j \in F_u$ forces $\psi_2 \in B_j$. By the induction hypothesis, $\sigma^j \models \psi_2$ and $\sigma^l \models \psi_1$ for $i \le l < j$, so $\sigma^i \models u$. $\square$

**Theorem 1.** The GBA returned at line L10 accepts exactly the words $\sigma$ with $\sigma \models \varphi$.

*Proof.* If $\sigma \models \varphi$, Lemma 1 gives an accepting run. If there is an accepting run $B_0 B_1 \ldots$ on $\sigma$, then $\varphi \in B_0$ by line L3, and Lemma 2 with $i = 0$ gives $\sigma \models \varphi$. $\square$

Lemma 2 also shows that the accepting run on a word is unique: it must be $B_i = \{\psi \in \mathit{cl} : \sigma^i \models \psi\}$.

**Lemma 3 (degeneralization).** Let $G$ be a GBA with acceptance sets $F_0, \ldots, F_{k-1}$, and let $D$ be the automaton that DEGENERALIZE returns. Then $L(D) = L(G)$.

*Proof.* If $k = 0$, every run of $G$ is accepting; DEGENERALIZE uses $k = 1$ and $F_0 = Q$, so every run of $D$ visits $F'$ at every position and is accepting. Now let $k \ge 1$.

*Runs correspond.* The first components of a run $(q_0, c_0)(q_1, c_1)\ldots$ of $D$ form a run $q_0 q_1 \ldots$ of $G$ on the same word, because line L12 copies the transitions, line L13 copies the labels, and line L11 copies the initial states. Conversely, each run $q_0 q_1 \ldots$ of $G$ has exactly one run of $D$ above it: $c_0 = 0$, and $c_{i+1} = (c_i + 1) \bmod k$ if $q_i \in F_{c_i}$, else $c_{i+1} = c_i$. The counter *moves* at position $i$ when $q_i \in F_{c_i}$.

*If the run of $G$ visits each $F_c$ infinitely often, the run of $D$ is accepting.* Suppose the counter moves only finitely often. Then from some position on it stays at one value $c$, and no later $q_i$ is in $F_c$, which is false. So the counter moves infinitely often. Each move goes from $c$ to $c + 1 \bmod k$, so the counter leaves the value $0$ infinitely often. When it leaves $0$ at position $i$, $q_i \in F_0$ and $c_i = 0$, so $(q_i, c_i) \in F' = F_0 \times \{0\}$.

*If the run of $D$ is accepting, the run of $G$ visits each $F_c$ infinitely often.* At each position with $(q_i, c_i) \in F_0 \times \{0\}$ the counter moves. So the counter moves infinitely often, and as it moves in the cyclic order $0, 1, \ldots, k - 1, 0$, it leaves each value $c$ infinitely often. It leaves $c$ only at a position with $q_i \in F_c$. $\square$

With Theorem 1, the Büchi automaton of line L13 accepts exactly the words that satisfy $\varphi$.

**Lemma 4 (size and time).** Let $n = |\varphi|$, let $e$ be the number of base subformulas (of the forms $p$, $\mathsf{X}\psi$ and $\psi_1\,\mathsf{U}\,\psi_2$) of the rewritten formula, and let $k$ be the number of its until subformulas. Then $k \le e \le n$, the GBA has at most $2^e$ states and $4^e$ transitions, the Büchi automaton has at most $\max(k, 1) \cdot 2^e \le n \cdot 2^n$ states (for $n \ge 1$), and the algorithm runs in $O(n \cdot 4^n)$ time.

*Proof.* The rewriting maps each atomic proposition of $\varphi$ to itself, each $\mathsf{X}$ to one $\mathsf{X}$, and each of $\mathsf{U}$, $\mathsf{R}$, $\mathsf{F}$ and $\mathsf{G}$ to one $\mathsf{U}$, and it adds only $\mathsf{true}$, $\neg$ and $\wedge$ otherwise. So each base subformula comes from a different symbol of $\varphi$, and $e \le n$; also $|\mathit{cl}| = O(n)$, since each symbol of $\varphi$ adds a bounded number of subformulas. An elementary set is determined by the base subformulas it contains: the membership of $\mathsf{true}$, of each negation and of each conjunction then follows from the rules, by induction on the formula. So there are at most $2^e$ elementary sets, and at most $(2^e)^2 = 4^e$ pairs, hence transitions. Line L2 tries $2^e$ choices of the base formulas and checks each in $O(|\mathit{cl}|)$ time. Lines L4 to L8 test $4^e$ pairs, each in $O(|\mathit{cl}|) = O(n)$ time. Line L9 takes $O(k \cdot 2^e \cdot n)$ time. DEGENERALIZE makes $\max(k, 1)$ copies of each state and each transition. The total is $O(n \cdot 4^n)$ time. $\square$

**Lemma 5 (the exponential is necessary).** For $m \ge 1$, let $\varphi_m = \bigwedge_{i=1}^{m} \bigl(p_i \leftrightarrow (\neg q\ \mathsf{U}\ (q \wedge p_i))\bigr)$, a formula of size $O(m)$. Every Büchi automaton that accepts exactly the words of $\varphi_m$ has at least $2^m$ states.

*Proof.* For $v \subseteq \{p_1, \ldots, p_m\}$, let $w_v = v\ (v \cup \{q\})\ \emptyset^\omega$. At position 0 of $w_v$, $q$ is false and $q$ holds at position 1, so $\neg q\ \mathsf{U}\ (q \wedge p_i)$ holds iff $p_i \in v$, which is also the value of $p_i$ at position 0. So $w_v \models \varphi_m$. Let $A$ be a Büchi automaton with $L(A) = \mathit{Words}(\varphi_m)$, fix an accepting run $\rho_v = r^v_0 r^v_1 r^v_2 \ldots$ of $A$ on $w_v$ for each $v$, and let $s_v = r^v_1$ be its state after the first letter.

Suppose $s_v = s_{v'}$ for some $v \neq v'$. Then $r^v_0\, r^{v'}_1\, r^{v'}_2 \ldots$ is a run of $A$: it starts in an initial state, reads the first letter $v$ as $\rho_v$ does and arrives at $s_v = s_{v'}$, and then reads $(v' \cup \{q\})\ \emptyset^\omega$ as $\rho_{v'}$ does. It visits the accepting states infinitely often, since $\rho_{v'}$ does. So $A$ accepts $v\ (v' \cup \{q\})\ \emptyset^\omega$. But some $p_i$ is in exactly one of $v$ and $v'$, and on this word the value of $p_i$ at position 0 is "$p_i \in v$", while $\neg q\ \mathsf{U}\ (q \wedge p_i)$ at position 0 has the value "$p_i \in v'$". So the word does not satisfy $\varphi_m$, which is a contradiction. Hence the $2^m$ states $s_v$ are pairwise different. $\square$

The argument works in the same way for automata with labels on transitions. With Lemma 4, the size $2^{\Theta(n)}$ of the translation is optimal up to the constant in the exponent. $\blacksquare$
