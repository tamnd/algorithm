---
title: The HMMER recurrences compute the Forward, Viterbi and MSV values of the search model
proves: [correctness]
status: full
---

Fix a configured search model (lines L5 and L10 to L19) and a target $x = x_1 \ldots x_L$. A *path* is a sequence of states that starts in $N$ before any residue is emitted, ends with $C \to T$, follows only transitions of positive probability, and emits $x$ in order: $M_k$, $I_k$, and $N$, $C$, $J$ on a self-loop each emit one residue, and $B$, $E$, $D_k$ and the first visit of $N$, $C$, $J$ emit nothing. In HMMER's convention $N$, $C$ and $J$ emit on the self-loop transition, so a state $N$, $C$ or $J$ "after $i$ residues" has emitted the residues up to $x_i$.

**Odds of a path.** The probability $P(x, \pi)$ is the product of its transition probabilities and emission probabilities. Divide by $\prod_{i=1}^{L} f(x_i)$. Each emitted residue $x_i$ appears once in the product, so we can divide each emission by $f(x_i)$: an emission of $M_k$ becomes $\hat e_k(x_i) = e_k(x_i)/f(x_i)$, and an emission of $I_k$, $N$, $C$ or $J$ becomes $f(x_i)/f(x_i) = 1$. Call the result the *odds* $w(\pi)$. It is a product of factors, one for each transition and one for each emission.

**Semiring.** Let $\oplus$ be $+$ or $\max$ on the nonnegative reals. In both cases $a \cdot (b \oplus c) = a b \oplus a c$ for $a \ge 0$, and $\oplus$ is associative and commutative. So for a finite set of paths $S$ and a factor $a \ge 0$, $\bigoplus_{\pi \in S} a\, w(\pi) = a \bigoplus_{\pi \in S} w(\pi)$.

**Prefixes.** For a state $q$ and $0 \le i \le L$, let $\Pi_q(i)$ be the set of path prefixes that start in $N$, emit exactly $x_1 \ldots x_i$, and end in $q$ (with the emission of $q$ included if $q$ emits). Let $W_q(i) = \bigoplus_{\pi \in \Pi_q(i)} w(\pi)$, with $W_q(i) = 0$ when the set is empty. We show that after row $i$ of the loop at line L11 (and, for $i = 0$, after line L10) each variable of the pseudocode equals the $W$ of its state.

**Order.** Inside row $i$, the code computes $M_k(i)$, $I_k(i)$, $D_k(i)$ for $k = 1, \ldots, m$, then $E(i)$, $J(i)$, $C(i)$, $N(i)$, $B(i)$. We prove the claim by induction on $i$, and inside a row in this order.

**Base, $i = 0$.** No residue is emitted. The only prefixes are $N$ itself, with odds 1, and $N \to B$, with odds move. $M_k$, $I_k$ emit, so their sets are empty. $D_k$ is reached only through some $M_j$ (the model has no $B \to D$), so its set is empty, and so are those of $E$, $J$ and $C$. Line L10 sets exactly these values.

**Step, row $i \ge 1$.** Assume the claim for row $i - 1$, and for the states of row $i$ already computed.

- *$M_k(i)$, line L13.* The last step of a prefix in $\Pi_{M_k}(i)$ is a transition into $M_k$ followed by the emission of $x_i$. The predecessor emitted $x_1 \ldots x_{i-1}$, so it lies in row $i - 1$. In Plan 7 the transitions into $M_k$ come from $B$ (probability $\text{entry}_k$), $M_{k-1}$, $I_{k-1}$ and $D_{k-1}$ (probabilities $t_{MM}$, $t_{IM}$, $t_{DM}$ of node $k-1$, present only for $k > 1$). The set $\Pi_{M_k}(i)$ is the disjoint union, over these predecessors $p$, of $\{\sigma \to M_k : \sigma \in \Pi_p(i-1)\}$, and a prefix of the union has odds $w(\sigma) \cdot a_{p M_k} \cdot \hat e_k(x_i)$. By the semiring law, $W_{M_k}(i) = \hat e_k(x_i) \bigoplus_p a_{p M_k} W_p(i-1)$, which is line L13 by the induction hypothesis.
- *$I_k(i)$, line L14.* The transitions into $I_k$ come from $M_k$ and $I_k$; Plan 7 has no $D_k \to I_k$. The predecessor is in row $i - 1$ and the emission has odds 1. The same argument gives line L14. For $k = m$ the model has no insert state, and the code leaves the value 0.
- *$D_k(i)$, line L15.* $D_k$ is silent, so its predecessor is in row $i$. Transitions into $D_k$ come from $M_{k-1}$ and $D_{k-1}$; Plan 7 has no $I \to D$, and $B$ does not enter delete states, so $D_1$ has no predecessor and stays 0. Both predecessors have index $k - 1 < k$ and are already computed in row $i$. This gives line L15.
- *$E(i)$, line L16.* $E$ is silent and is entered from every $M_k$ and every $D_k$ with $k \ge 2$ with odds 1 (the local exit). All of them are computed in row $i$. This gives line L16.
- *$J(i)$ and $C(i)$, line L17.* A prefix ending in $J$ after $i$ residues either was in $J$ after $i - 1$ residues and took the self-loop, emitting $x_i$ with odds 1 (factor loop), or entered $J$ from $E$ in row $i$ without emitting (factor 1/2). The two sets are disjoint. The same holds for $C$. This gives line L17.
- *$N(i)$ and $B(i)$, line L18.* $N$ is entered only from itself, so $W_N(i) = W_N(i-1) \cdot \text{loop}$. $B$ is silent and is entered from $N$ and from $J$ in row $i$ with factor move. This gives line L18.

This completes the induction. Note that each prefix is counted once: it is assigned to the set of its last state, and it splits uniquely into its last transition and the prefix before it.

**The result, line L19.** Every complete path ends with $C \to T$ after emitting all $L$ residues, so the set of complete paths is $\{\sigma \to T : \sigma \in \Pi_C(L)\}$ and $\bigoplus_\pi w(\pi) = W_C(L) \cdot \text{move}$. For $\oplus = +$ this is $\sum_\pi P(x, \pi) / \prod_i f(x_i) = P(x \mid \text{search model}) / \prod_i f(x_i)$. The null model gives $P(x \mid R) = \prod_i f(x_i) \cdot (L/(L+1))^L \cdot 1/(L+1)$, so $\log_2$ of the returned value minus $\log_2\bigl((L/(L+1))^L/(L+1)\bigr)$ is the bit score $\log_2 (P(x \mid \text{search model}) / P(x \mid R))$. For $\oplus = \max$ the same steps give the odds of the most probable path, and the Viterbi bit score.

**MSV, lines L20 to L23.** The MSV model has the same special states, no insert or delete states, $M_{k-1} \to M_k$ with factor 1, and $B \to M_k$ with factor $2/(m(m+1))$ for every $k$. Its prefixes ending in $M_k$ after $i$ residues come from $M_{k-1}$ or from $B$ in row $i - 1$, and the rest of the argument is the one above with $\oplus = \max$. So lines L20 to L23 return the odds of the best MSV path.

**The E-value, line L9.** Let $P(s)$ be the probability that a sequence drawn from the null model scores at least $s$. If the $Z$ targets were independent draws from the null model, the number of them that score at least $s$ is a sum of $Z$ indicator variables, each with mean $P(s)$, so its expectation is $Z \cdot P(s)$, which is line L9. The functions used for $P(s)$ at lines L6 to L8 are fitted approximations (Gumbel for MSV and Viterbi, exponential tail for Forward); the claim proved here is that, given $P(s)$, line L9 is the expected number of null targets at that score or better. The filters at lines L6 to L8 only remove targets, so every reported target has the Forward score and E-value defined above. $\blacksquare$
