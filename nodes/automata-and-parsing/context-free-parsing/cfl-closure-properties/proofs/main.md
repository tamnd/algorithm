---
title: Proof of the closure properties of context-free languages
proves: [statement]
status: full
---

Throughout, $G = (V, \Sigma, R, S)$, $G_1 = (V_1, \Sigma, R_1, S_1)$ and $G_2 = (V_2, \Sigma, R_2, S_2)$ are grammars for $L$, $L_1$ and $L_2$, renamed so that their nonterminal sets are disjoint from each other and from every new symbol. We use one fact about grammars many times.

**Fact (context-freeness).** If $X_1 \cdots X_k \Rightarrow^* w$, then $w = w_1 \cdots w_k$ with $X_i \Rightarrow^* w_i$ for each $i$, and each derivation $X_i \Rightarrow^* w_i$ uses at most as many steps as the whole. Conversely, derivations $X_i \Rightarrow^* w_i$ combine into $X_1 \cdots X_k \Rightarrow^* w_1 \cdots w_k$. This holds because a step rewrites one nonterminal and does not look at its neighbours, so the steps can be sorted by the symbol $X_i$ they descend from.

## 1. Union, concatenation and star

Let $S$ be a new start symbol.

- **Union.** Add $S \to S_1 \mid S_2$ to $R_1 \cup R_2$. A derivation from $S$ starts with one of the two productions and then uses only the productions of that grammar, because the nonterminal sets are disjoint. So the language is $L_1 \cup L_2$.
- **Concatenation.** Add $S \to S_1 S_2$. By the Fact, $S_1 S_2 \Rightarrow^* w$ exactly when $w = w_1 w_2$ with $S_1 \Rightarrow^* w_1$ and $S_2 \Rightarrow^* w_2$. The language is $L_1 L_2$.
- **Star.** Add $S \to S_1 S \mid \varepsilon$ to $R_1$. By induction on $k$, $S \Rightarrow^* S_1^k S$, so $S$ derives every string of $L_1^k$ for every $k \ge 0$. Conversely, a derivation from $S$ uses $S \to S_1 S$ some $k$ times and $S \to \varepsilon$ once, since that is the only way to remove $S$, so by the Fact the string is in $L_1^k$. The language is $L_1^*$.

## 2. Reversal

Replace each production $A \to X_1 \cdots X_k$ by $A \to X_k \cdots X_1$. By induction on the length of the derivation, $A \Rightarrow^* w$ in the old grammar exactly when $A \Rightarrow^* w^R$ in the new one: the first step $A \to X_1 \cdots X_k$ with $X_i \Rightarrow^* w_i$ becomes $A \to X_k \cdots X_1$ with $X_i \Rightarrow^* w_i^R$, and $w_k^R \cdots w_1^R = (w_1 \cdots w_k)^R$. The language is $L^R$.

## 3. Substitution and homomorphism

Let $s$ map each $a \in \Sigma$ to a context-free language $s(a) \subseteq \Delta^*$ with grammar $G_a = (V_a, \Delta, R_a, S_a)$, and extend it by $s(\varepsilon) = \{\varepsilon\}$, $s(xy) = s(x) s(y)$ and $s(L) = \bigcup_{x \in L} s(x)$. The grammar $G_s$ has nonterminals $V \cup \bigcup_a V_a$, start symbol $S$, the productions of every $G_a$, and each production of $G$ with every terminal $a$ replaced by $S_a$.

If $x = a_1 \cdots a_k \in L$ and $y_i \in s(a_i)$, then $S \Rightarrow^* S_{a_1} \cdots S_{a_k}$ in $G_s$, by the derivation of $x$ with the replaced productions, and then $S_{a_i} \Rightarrow^* y_i$, so $y_1 \cdots y_k$ is derived. Conversely, take a parse tree of $y$ in $G_s$. The nodes labelled by nonterminals of $V$ form a tree at the top whose leaves are labelled by symbols $S_{a_1}, \ldots, S_{a_k}$ in order, because the productions of $V$ only produce symbols of $V$ and start symbols $S_a$, and the productions of each $G_a$ never produce a symbol of $V$. Replacing each $S_{a_i}$ by $a_i$ turns the top tree into a parse tree of $x = a_1 \cdots a_k$ in $G$, and the subtree below each $S_{a_i}$ shows $y_i \in s(a_i)$, with $y = y_1 \cdots y_k$. So $L(G_s) = s(L)$.

A homomorphism $h$ is the substitution with $s(a) = \{h(a)\}$, and $\{h(a)\}$ has the grammar $S_a \to h(a)$. So $h(L)$ is context-free.

## 4. Intersection with a regular language

Let $D = (Q, \Sigma, \delta, q_0, F)$ be a DFA for $R$, with $\delta$ a partial function. The grammar $G_\cap$ has a new start symbol $S'$ and the nonterminals $[p X q]$ for $p, q \in Q$ and $X \in V \cup \Sigma$, with the productions

- $S' \to [q_0 S f]$ for each $f \in F$;
- $[p a q] \to a$ whenever $\delta(p, a) = q$;
- $[p A p] \to \varepsilon$ for each $A \to \varepsilon$ in $R$ and each $p \in Q$;
- $[p_0 A p_k] \to [p_0 X_1 p_1][p_1 X_2 p_2] \cdots [p_{k-1} X_k p_k]$ for each $A \to X_1 \cdots X_k$ in $R$ with $k \ge 1$ and all states $p_0, \ldots, p_k$.

**Claim.** $[p X q] \Rightarrow^* w$ in $G_\cap$ if and only if $X \Rightarrow^* w$ in $G$ (or $X = w$ for a terminal $X$) and $\delta^*(p, w) = q$.

*Proof.* "Only if", by induction on the length of the derivation. For a terminal $X = a$, the only production is $[p a q] \to a$ with $\delta(p, a) = q$. For $X = A$, the first step uses a production that comes from some $A \to X_1 \cdots X_k$. If $k = 0$ then $w = \varepsilon$, $q = p$, and $\delta^*(p, \varepsilon) = p$. Otherwise, by the Fact, $w = w_1 \cdots w_k$ with $[p_{i-1} X_i p_i] \Rightarrow^* w_i$ by shorter derivations, so by induction $X_i \Rightarrow^* w_i$ and $\delta^*(p_{i-1}, w_i) = p_i$. Then $A \Rightarrow X_1 \cdots X_k \Rightarrow^* w$ and $\delta^*(p, w) = p_k = q$.

"If", by induction on the length of the derivation $X \Rightarrow^* w$ in $G$, with terminals as the base case. If $X = A$ and the first step is $A \to X_1 \cdots X_k$, then $w = w_1 \cdots w_k$ with $X_i \Rightarrow^* w_i$ by shorter derivations. Let $p_0 = p$ and $p_i = \delta^*(p_{i-1}, w_i)$, which is defined because $\delta^*(p, w)$ is, and $p_k = q$. By induction $[p_{i-1} X_i p_i] \Rightarrow^* w_i$, and the production $[p A q] \to [p_0 X_1 p_1] \cdots [p_{k-1} X_k p_k]$, or $[p A p] \to \varepsilon$ when $k = 0$, finishes. $\square$

With $X = S$, $p = q_0$ and $q \in F$, the claim gives $L(G_\cap) = L \cap R$.

## 5. Inverse homomorphism

Let $g : \Delta^* \to \Sigma^*$ be a homomorphism, and let $P = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$ be a PDA with $L(P) = L$, which exists by the [equivalence of grammars and pushdown automata](/cfg-pda-equivalence/). Let $B$ be the finite set of suffixes of the strings $g(a)$, $a \in \Delta$, including $\varepsilon$. The PDA $P'$ has states $Q \times B$, start state $(q_0, \varepsilon)$, start symbol $Z_0$, final states $F \times \{\varepsilon\}$, and three kinds of moves, for all $X \in \Gamma$:

- (load) $((q, g(a)), X) \in \delta'((q, \varepsilon), a, X)$ for each $q \in Q$ and $a \in \Delta$;
- (step) $((p, u), \gamma) \in \delta'((q, b u), \varepsilon, X)$ whenever $(p, \gamma) \in \delta(q, b, X)$ with $b \in \Sigma$ and $b u \in B$;
- (silent) $((p, u), \gamma) \in \delta'((q, u), \varepsilon, X)$ whenever $(p, \gamma) \in \delta(q, \varepsilon, X)$, for each $u \in B$.

The second component is a buffer that holds the part of $g(a)$ that $P$ has not read yet.

**Claim.** $P'$ accepts $x \in \Delta^*$ if and only if $P$ accepts $g(x)$.

*Proof.* Given an accepting run of $P'$ on $x = a_1 \cdots a_k$, delete the load moves and drop the buffer from each state. A step move becomes the move of $P$ that reads the first symbol $b$ of the buffer, and a silent move becomes the same silent move of $P$. The buffer is loaded with $g(a_i)$ only when it is empty, and its symbols are removed in order, so the moves of $P$ read $g(a_1) g(a_2) \cdots g(a_k) = g(x)$. The run ends in a state $(q, \varepsilon)$ with $q \in F$, so all of $g(x)$ was read and $P$ accepts.

Conversely, take an accepting run of $P$ on $g(x)$. Build a run of $P'$ by induction along it, keeping the invariant: after the moves of $P$ that have read $g(a_1) \cdots g(a_{i-1})\, v$, where $v$ is a prefix of $g(a_i)$ and $g(a_i) = v u$, the run of $P'$ has read $a_1 \cdots a_i$ (or $a_1 \cdots a_{i-1}$ with an empty buffer if $v = \varepsilon$ and $a_i$ is not loaded yet), its state is $(q, u)$ for the current state $q$ of $P$, and its stack is that of $P$. A silent move of $P$ is copied as a silent move. Before a move of $P$ that reads a symbol $b$, while the buffer is empty, load the next symbols $a_i$ of $x$; loads of symbols with $g(a_i) = \varepsilon$ keep the buffer empty, and the first load with $g(a_i) \ne \varepsilon$ puts $g(a_i)$, which starts with $b$, into the buffer; then copy the move as a step move. At the end of the run of $P$, load the remaining symbols of $x$, whose images are all $\varepsilon$, since $P$ has read all of $g(x)$. The final state is $(q, \varepsilon)$ with $q \in F$, so $P'$ accepts $x$. $\square$

So $g^{-1}(L) = L(P')$ is context-free.

## 6. Failure for intersection, complement and difference

Let $L_1 = \{a^i b^i c^j : i, j \ge 0\}$, with the grammar $S \to X C$, $X \to a X b \mid \varepsilon$, $C \to c C \mid \varepsilon$, and $L_2 = \{a^i b^j c^j : i, j \ge 0\}$, with the grammar $S \to A Y$, $A \to a A \mid \varepsilon$, $Y \to b Y c \mid \varepsilon$. Both are context-free. Their intersection is $\{a^n b^n c^n : n \ge 0\}$, which is not context-free by the [pumping lemma](/cfl-pumping-lemma/). So the class is not closed under intersection.

If it were closed under complement, then by part 1 it would contain $\overline{\overline{L_1} \cup \overline{L_2}} = L_1 \cap L_2$, a contradiction. And $\overline{L} = \Sigma^* \setminus L$ with $\Sigma^*$ context-free, so closure under difference would give closure under complement. $\blacksquare$
