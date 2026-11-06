---
title: Epsilon-production elimination keeps every nonempty string
proves: [correctness]
status: full
---

We use the pseudocode of the page. $G = (V, \Sigma, P, S)$ is the input, $N$ the set computed by line L1, $P'$ the set built by lines L2 to L6, and $G'$ the output. For a production $p = A \to X_1 \cdots X_k$, the worklist keeps a counter $c_p$, initially $k$.

**Lemma 1 (line L1).** When the worklist is empty, $N = \{A \in V : A \Rightarrow^* \varepsilon\}$.

*Proof.* Invariant: $c_p$ equals $k$ minus the number of positions $i$ such that $X_i$ has already been taken off the worklist. Each nonterminal enters the worklist at most once, when it enters $N$, and is later taken off and decreases $c_p$ once for each of its occurrences in $p$. So at the end, $c_p$ is the number of positions of $p$ that hold a terminal or a nonterminal not in $N$.

*Every member of $N$ is nullable,* by induction on the order of entry. A left side of an empty production derives $\varepsilon$ in one step. Any other $A$ enters when $c_p = 0$ for some $p = A \to X_1 \cdots X_k$, so every $X_i$ is a nonterminal already taken off the worklist, hence already in $N$, hence nullable by induction; then $A \Rightarrow X_1 \cdots X_k \Rightarrow^* \varepsilon$.

*Every nullable $A$ is in $N$,* by induction on the length $m$ of a derivation $A \Rightarrow^m \varepsilon$. Its first step uses some $p = A \to X_1 \cdots X_k$. If $k = 0$, $A$ is in the initial worklist. Otherwise every $X_i$ is a nonterminal, and by the splitting lemma $X_i \Rightarrow^{m_i} \varepsilon$ with $m_i < m$, so each $X_i$ is in $N$ by induction. Every member of $N$ is taken off the worklist before the end, so at the end $c_p = 0$. The counter reaches 0 at the moment the last of these occurrences is processed, and then $A$ enters $N$ if it was not there already. $\square$

**Lemma 2 (soundness).** If $A \to \alpha'$ is in $P'$, then $A \Rightarrow^+_G \alpha'$. So $A \Rightarrow^*_{G'} w$ implies $A \Rightarrow^*_G w$ for every nonterminal $A$ of $G$ and every $w \in \Sigma^*$.

*Proof.* Line L6 adds $A \to \alpha'$ only when $\alpha'$ comes from a production $A \to X_1 \cdots X_k$ of $P$ by dropping some $X_i \in N$. Then $A \Rightarrow X_1 \cdots X_k$, and each dropped $X_i$ derives $\varepsilon$ by Lemma 1, so $A \Rightarrow^+ \alpha'$. A derivation in $G'$ is a sequence of steps with productions of $P'$; replacing each by the corresponding derivation in $G$ gives a derivation in $G$. $\square$

**Lemma 3 (completeness).** If $A \Rightarrow^m_G w$ with $w \neq \varepsilon$, then $A \Rightarrow^*_{(V, \Sigma, P', S)} w$.

*Proof.* Induction on $m \ge 1$. The first step uses some $A \to X_1 \cdots X_k$ in $P$, and by the splitting lemma $w = w_1 \cdots w_k$ with $X_i \Rightarrow^{m_i} w_i$, where $\sum m_i = m - 1$, so $m_i < m$. Let $K = \{i : w_i \neq \varepsilon\}$; it is not empty because $w \neq \varepsilon$. For $i \notin K$, $X_i \Rightarrow^* \varepsilon$, so $X_i$ is a nonterminal in $N$ by Lemma 1. Hence the choice "keep exactly the positions in $K$" is one of the choices of line L4, its right side $\alpha' = (X_i)_{i \in K}$ is nonempty, and line L6 adds $A \to \alpha'$ to $P'$. For $i \in K$, either $X_i$ is a terminal and $X_i = w_i$, or $X_i$ is a nonterminal with $X_i \Rightarrow^{m_i}_G w_i$, $w_i \neq \varepsilon$ and $m_i < m$, so $X_i$ derives $w_i$ with $P'$ by induction. Then $A \Rightarrow \alpha' \Rightarrow^* w$ with $P'$. $\square$

**Lemma 4 (cleanup).** Removing a production that mentions a nonterminal of $G$ with no production left does not change, for any nonterminal $B$, the set of terminal strings that $B$ derives.

*Proof.* Let $X$ be a nonterminal of $G$ with no production in the current set. No derivation of a terminal string can contain $X$ in a sentential form, because $X$ would have to be rewritten later and it has no production. So no production with $X$ on its right side occurs in a derivation of a terminal string, and removing such productions keeps every such derivation. Repeating the step keeps the sets as well, by induction on the number of rounds. $\square$

**Lemma 5.** No production in $P'$ has an empty right side, and every string that a nonterminal of $G$ derives with $P'$ is nonempty.

*Proof.* Line L6 adds only nonempty right sides. A derivation from a nonterminal starts with a nonempty right side, and each later step replaces a symbol by a nonempty string, so the length never drops below 1. $\square$

**Theorem.** Without line L7, $G'$ has no empty production and $L(G') = L(G) \setminus \{\varepsilon\}$. With line L7 applied (when keep_empty holds and $S \in N$), the only empty production is $S' \to \varepsilon$, $S'$ occurs on no right side, and $L(G') = L(G)$.

*Proof.* By Lemmas 2, 3 and 4, for every nonempty $w$, $S \Rightarrow^*_{G'} w$ if and only if $S \Rightarrow^*_G w$, and by Lemma 5, $S$ derives no empty string in $G'$. This gives $L(G') = L(G) \setminus \{\varepsilon\}$ without line L7. With line L7, $S'$ is fresh, so it is on no right side, $S' \to \varepsilon$ is its only empty production, and $S'$ derives $\varepsilon$ and every string of $L(G) \setminus \{\varepsilon\}$ through $S' \Rightarrow S$ (the production $S' \to S$ is omitted only when $S$ has no production left, in which case $S$ derives nothing and $L(G) = \{\varepsilon\}$). Since $S \in N$, $\varepsilon \in L(G)$ by Lemma 1, so $L(G') = L(G)$. If keep_empty holds but $S \notin N$, then $\varepsilon \notin L(G)$ and $L(G') = L(G) \setminus \{\varepsilon\} = L(G)$. $\blacksquare$
