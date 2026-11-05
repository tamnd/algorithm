---
title: Correctness of the DeRemer and Pennello lookahead computation
proves: [correctness]
status: full
---

We prove that the algorithm on the [LALR lookahead computation](/lalr-lookahead-computation/) page returns, for every completed item $A \to \omega \cdot$ of every LR(0) state $q$ with $A \ne S'$, exactly the set of lookaheads that the item has in the canonical LR(1) states whose core is $q$.

**Notation and assumptions.** $G = (V, \Sigma, P, S)$ is augmented with $S' \to S$ as production 0, and $S'$ occurs on no right side. $G$ is reduced: every nonterminal is reachable from $S$ and derives some terminal string. LR(0) states are identified with their kernels; $\overline{p}$ is the closure of $p$, and $\mathrm{GOTO}(p, \beta)$ is defined symbol by symbol. For a string $\gamma$ and a set $M$ of terminals, $\mathrm{FIRST}(\gamma M)$ is $\mathrm{FIRST}(\gamma)$, together with $M$ when $\gamma \Rightarrow^* \varepsilon$. $T(q)$ is the set of terminals $t$ with $\mathrm{GOTO}(q, t)$ defined. Items $A \to \cdot \omega$ with $A \ne S'$ are never kernel items, and $\mathrm{GOTO}$ never leads to state 0, whose only kernel item has the dot at position 0.

## Part 1: merged lookaheads as a least solution

For a state $p$ and an item $i \in \overline{p}$, let $M(p, i)$ be the set of $b$ such that $[i, b]$ belongs to some canonical LR(1) state whose core is $\overline{p}$.

**Lemma 1.** $M$ is the least family of sets, indexed by pairs $(p, i)$ with $i \in \overline{p}$, that satisfies

- (a) $\$ \in M(0, S' \to \cdot S)$;
- (b) $M(\mathrm{GOTO}(p, Y), B \to \beta Y \cdot \gamma) \supseteq M(p, B \to \beta \cdot Y \gamma)$;
- (c) $M(p, C \to \cdot \eta) \supseteq \mathrm{FIRST}(\gamma\, M(p, B \to \beta \cdot C \gamma))$ for every item $B \to \beta \cdot C \gamma \in \overline{p}$ and every production $C \to \eta$.

*Proof.* Because $G$ is reduced, every $\mathrm{FIRST}(\gamma b)$ is nonempty, so the LR(1) closure adds a dotted production exactly when the LR(0) closure does, and the core of $\mathrm{GOTO}_1(J, Y)$ is $\overline{\mathrm{GOTO}(\mathrm{core}(J), Y)}$. Hence $M$ satisfies (a), since the start state contains $[S' \to \cdot S,\ \$]$; (b), since $\mathrm{GOTO}_1(J, Y)$ contains $[B \to \beta Y \cdot \gamma,\ b]$ whenever $J$ contains $[B \to \beta \cdot Y \gamma,\ b]$; and (c), since every LR(1) state is closed. Conversely let $M_0$ be the least solution. Every LR(1) state is built from the start item by GOTO and closure steps, and by induction on the number of steps each of its items $[i, b]$, in a state with core $\overline{p}$, has $b \in M_0(p, i)$: the start item by (a), a kernel item made by GOTO by (b), and an item added by closure by (c). So $M \subseteq M_0$, and $M_0 \subseteq M$ because $M$ is a solution. $\square$

In the least solution each set is exactly the union of what the rules put into it. Items with the dot at position 0 and $A \ne S'$ get lookaheads only from (c), and items with the dot later only from (b). Unrolling (b) along the symbols before the dot gives, for $B \ne S'$,
$$M(q, B \to \beta \cdot \gamma) = \bigcup \{ M(p, B \to \cdot \beta \gamma) : \mathrm{GOTO}(p, \beta) = q,\ B \to \cdot \beta \gamma \in \overline{p} \}, \tag{1}$$
while $M(0, S' \to \cdot S) = M(\mathrm{GOTO}(0, S), S' \to S \cdot) = \{\$\}$. For a nonterminal transition $(p, A)$ define
$$\mathrm{Fol}(p, A) = \bigcup \{ \mathrm{FIRST}(\gamma\, M(p, B \to \beta \cdot A \gamma)) : B \to \beta \cdot A \gamma \in \overline{p} \}.$$
By (c), $M(p, A \to \cdot \omega) = \mathrm{Fol}(p, A)$ for every production $A \to \omega$ with $A \ne S'$. An item $A \to \cdot \omega$ lies in $\overline{p}$ exactly when $(p, A)$ is a nonterminal transition: it is added by closure from an item with the dot before $A$, and such an item makes $\mathrm{GOTO}(p, A)$ defined. So (1) gives
$$M(q, A \to \omega \cdot) = \bigcup \{ \mathrm{Fol}(p, A) : (q, A \to \omega) \text{ lookback } (p, A) \}. \tag{2}$$

## Part 2: the first terminals of a state

For a state $q$, let $R(q)$ be the union of $T(q')$ over all states $q'$ reachable from $q$ by moves on nullable nonterminals, $q$ itself included.

**Lemma 2.** $R(q) = \bigcup \{ \mathrm{FIRST}(\lambda) : K \to \kappa \cdot \lambda \text{ is a kernel item of } q \}$.

*Proof of $\supseteq$.* We show the stronger claim: for every state $q'$ and every item $E \to \zeta \cdot \eta \in \overline{q'}$, $\mathrm{FIRST}(\eta) \subseteq R(q')$. Take $t \in \mathrm{FIRST}(\eta)$ and a derivation $\eta \Rightarrow^* t z$ with the fewest steps; induct on that number. Let $\eta = Y_1 \eta'$. If $Y_1 = t$, then $t \in T(q') \subseteq R(q')$. Otherwise $Y_1$ is a nonterminal, and either $t$ comes from $Y_1$, so that $Y_1 \to \eta_1$ with $\eta_1 \Rightarrow^* t z_1$ in fewer steps, and $Y_1 \to \cdot \eta_1 \in \overline{q'}$ gives $t \in R(q')$ by induction; or $Y_1 \Rightarrow^+ \varepsilon$ and $\eta' \Rightarrow^* t z$ in fewer steps, and then the item $E \to \zeta Y_1 \cdot \eta'$ lies in $\overline{q''}$ for $q'' = \mathrm{GOTO}(q', Y_1)$, a move on a nullable nonterminal, so $t \in R(q'') \subseteq R(q')$ by induction.

*Proof of $\subseteq$.* Let $U(q)$ be the right side of the lemma. First, $T(q) \subseteq U(q)$: an item $E \to \zeta \cdot t \eta \in \overline{q}$ is a kernel item, so $t \in U(q)$, or it was added by closure from a kernel item $K \to \kappa \cdot D \lambda$ through productions that each begin with the next nonterminal of the chain, so $D \lambda \Rightarrow^* t \eta \mu \lambda$ and $t \in \mathrm{FIRST}(D \lambda) \subseteq U(q)$. Second, if $C$ is nullable and $q_1 = \mathrm{GOTO}(q, C)$, then $U(q_1) \subseteq U(q)$: a kernel item of $q_1$ is $B \to \beta C \cdot \gamma$ for some $B \to \beta \cdot C \gamma \in \overline{q}$. If that item is a kernel item of $q$, then $\mathrm{FIRST}(\gamma) \subseteq \mathrm{FIRST}(C \gamma)$ because $C$ is nullable. If it was added by closure from a kernel item $K \to \kappa \cdot D \lambda$, then $D \lambda \Rightarrow^* B \mu \lambda \Rightarrow C \gamma \mu \lambda \Rightarrow^* \gamma \mu \lambda$, so $\mathrm{FIRST}(\gamma) \subseteq \mathrm{FIRST}(\gamma \mu \lambda) \subseteq \mathrm{FIRST}(D \lambda)$. By induction along the path, $T(q') \subseteq U(q') \subseteq U(q)$ for every $q'$ reachable by nullable moves. $\square$

## Part 3: Read and Follow

For a relation $R$ on $X$ and sets $F'(x)$, a family $F$ *solves* $(R, F')$ if $F(x) = F'(x) \cup \bigcup_{x R y} F(y)$ for all $x$. The family $\mathrm{Reach}(x) = \bigcup \{ F'(y) : y \text{ reachable from } x \text{ along } R \}$ solves it, and every solution contains it, by induction on the length of a path from $x$ to $y$. So $\mathrm{Reach}$ is the least solution; Part 4 shows that DIGRAPH returns it. Thus line L4 returns the least solution Read of $(\mathrm{reads}, \mathrm{DR})$ and line L6 the least solution Follow of $(\mathrm{includes}, \mathrm{Read})$.

**Lemma 3.** $\mathrm{Read}(p, A) = R(\mathrm{GOTO}(p, A))$, together with $\$$ when $(p, A) = (0, S)$.

*Proof.* A reads path from $(p, A)$ is $(p, A), (r_0, C_1), (r_1, C_2), \ldots, (r_{k-1}, C_k)$ with $r_0 = \mathrm{GOTO}(p, A)$, $r_j = \mathrm{GOTO}(r_{j-1}, C_j)$ and every $C_j$ nullable, and the terminals in DR along it are $T(r_0), T(r_1), \ldots, T(r_k)$. Their union over all such paths is $R(r_0)$. The marker $\$$ is in $\mathrm{DR}(x)$ only for $x = (0, S)$, the only transition whose target contains $S' \to S \cdot$, and no reads path enters $(0, S)$ from another node, since that would need a move into state 0. $\square$

**Lemma 4.** $\mathrm{Fol}$ solves $(\mathrm{includes}, \mathrm{Read})$, and $\mathrm{Fol} = \mathrm{Follow}$.

*Proof.* Split the union defining $\mathrm{Fol}(p, A)$ into the parts $\mathrm{FIRST}(\gamma)$ and the parts $M(p, B \to \beta \cdot A \gamma)$ with $\gamma$ nullable. The kernel items of $\mathrm{GOTO}(p, A)$ are the items $B \to \beta A \cdot \gamma$ for $B \to \beta \cdot A \gamma \in \overline{p}$, so by Lemmas 2 and 3 the first parts give $\mathrm{Read}(p, A)$ without $\$$. For $B = S'$ the item is $S' \to \cdot S$ in state 0 and contributes $\$$, which Read contains for $(0, S)$. For $B \ne S'$ with $\gamma$ nullable, (1) writes $M(p, B \to \beta \cdot A \gamma)$ as the union of $\mathrm{Fol}(p', B)$ over the states $p'$ with $\mathrm{GOTO}(p', \beta) = p$ and $B \to \cdot \beta A \gamma \in \overline{p'}$, that is over the $(p', B)$ that $(p, A)$ includes. Hence $\mathrm{Fol}(p, A) = \mathrm{Read}(p, A) \cup \bigcup_{(p, A) \text{ includes } (p', B)} \mathrm{Fol}(p', B)$, and since Follow is the least solution, $\mathrm{Follow} \subseteq \mathrm{Fol}$.

For the other inclusion define $M'$ from Follow: $M'(0, S' \to \cdot S) = M'(\mathrm{GOTO}(0, S), S' \to S \cdot) = \{\$\}$, and for $B \ne S'$ let $M'(q, B \to \beta \cdot \gamma)$ be the union of $\mathrm{Follow}(p, B)$ over the states $p$ with $\mathrm{GOTO}(p, \beta) = q$ and $B \to \cdot \beta \gamma \in \overline{p}$. Then $M'$ satisfies (a) and (b) by its definition. For (c), let $B \to \beta \cdot C \gamma \in \overline{p}$ and $C \to \eta$; then $M'(p, C \to \cdot \eta) = \mathrm{Follow}(p, C)$. By Lemmas 2 and 3, $\mathrm{FIRST}(\gamma) \subseteq R(\mathrm{GOTO}(p, C)) \subseteq \mathrm{Read}(p, C) \subseteq \mathrm{Follow}(p, C)$. If $\gamma$ is nullable and $B = S'$, then $(p, C) = (0, S)$ and $\$ \in \mathrm{Read}(0, S)$; if $B \ne S'$, each $\mathrm{Follow}(p', B)$ in $M'(p, B \to \beta \cdot C \gamma)$ comes from a pair that $(p, C)$ includes, so it is contained in $\mathrm{Follow}(p, C)$. By Lemma 1, $M \subseteq M'$, and therefore
$$\mathrm{Fol}(p, A) = \bigcup \mathrm{FIRST}(\gamma\, M(p, B \to \beta \cdot A \gamma)) \subseteq \bigcup \mathrm{FIRST}(\gamma\, M'(p, B \to \beta \cdot A \gamma)) \subseteq \mathrm{Follow}(p, A),$$
the last step by the same computation as in the first paragraph with $M'$ and Follow in place of $M$ and Fol. $\square$

**Theorem 5.** Line L7 sets $\mathrm{LA}(q, A \to \omega) = M(q, A \to \omega \cdot)$ for every completed item with $A \ne S'$.

*Proof.* Line L7 takes, for each transition $(p, A)$ and production $A \to \omega$, the state $q = \mathrm{GOTO}(p, \omega)$, which is defined because $A \to \cdot \omega \in \overline{p}$, and adds $\mathrm{Follow}(p, A)$. So it computes the union of Follow over the lookback pairs, which by Lemma 4 and (2) is $M(q, A \to \omega \cdot)$. Every completed item gets a set, because by (1) it has at least one lookback pair. $\square$

## Part 4: DIGRAPH

**Lemma 6.** DIGRAPH$(X, R, F')$ returns $F(x) = \mathrm{Reach}(x)$ for every $x$.

*Proof.* The search is Tarjan's strongly connected components algorithm, with $N(x)$ in the role of the low link and $N = \infty$ marking finished nodes, so that line L11 does not lower $N(x)$ through them. Tarjan's analysis gives three facts for it: when line L12 finds $N(x) = d$, the nodes popped are exactly the strongly connected component of $x$; every node of that component was first visited inside the call on $x$; and every component reachable from it by an edge leaving it was finished earlier.

Every set ever stored in $F(u)$ is contained in $\mathrm{Reach}(u)$: it starts as $F'(u)$ and grows only by $F(v)$ for an edge $u R v$, and $\mathrm{Reach}(v) \subseteq \mathrm{Reach}(u)$; the sets copied at line L12 go to nodes of one component, which all have the same Reach.

We show by induction on the order in which components finish that, when the component $Q$ with root $x$ finishes, $F(x) \supseteq \mathrm{Reach}(x)$. Each $u \in Q$ is visited inside the call on $x$, and when the call on a node returns, line L11 adds its set to its caller's set, so $F(x) \supseteq F(u) \supseteq F'(u)$ for the value of $F(u)$ when its call returned. During that call, line L11 was run for every edge $u R v$, after the call on $v$ if $v$ was new; if $v$ lies in a component other than $Q$, that component finished earlier and $F(v) = \mathrm{Reach}(v)$ by induction. So $F(x)$ contains $F'(u)$ for every $u \in Q$ and $\mathrm{Reach}(v)$ for every edge from $Q$ to another component, and these together make up $\mathrm{Reach}(x)$. With the previous paragraph, $F(x) = \mathrm{Reach}(x)$, and line L12 gives every member of $Q$ this set, which is its own Reach. Later steps never change the set of a finished node. $\square$

The implementation replaces the recursion by an explicit stack of frames $(x, d, i)$, where $i$ is the position of the next successor of $x$ to look at. When a frame is removed, the update of line L11 for the edge from its caller is done at once, so the order of operations is the same as in the recursive version.

**Conclusion.** By Lemma 6, lines L4 and L6 compute the least solutions Read and Follow; by Theorem 5, line L7 gives each completed item exactly its lookaheads in the canonical LR(1) states with the same core, which are the LALR(1) lookaheads. ∎
