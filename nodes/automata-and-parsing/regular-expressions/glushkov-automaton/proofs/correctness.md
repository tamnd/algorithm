---
title: The Glushkov automaton accepts exactly the language of the expression
proves: [correctness, termination]
status: full
---

Let $r$ be a regular expression with $m$ nodes and symbol leaves numbered $1, \ldots, k$ from left to right, and let $\bar r$ be the marked expression, in which leaf $p$ is the letter $p$. For a node $x$, $\bar x$ is the marked subexpression, and $\mathrm{pos}(x)$ is the set of positions of the leaves below $x$. Let $h$ be the homomorphism with $h(p) = \mathrm{sym}(p)$.

**Termination.** The postorder walk visits each node of the finite tree once, and each visit does finitely many set operations on subsets of $\{1, \ldots, k\}$. Lines L15 to L18 are finite. So the algorithm stops.

**The computed sets.** For a node $x$, let $N(x)$, $\mathrm{First}(x)$ and $\mathrm{Last}(x)$ be the values set at lines L3 to L14, and let $\mathrm{Fol}(x)$ be the set of pairs $(p, q)$ added at line L8 or line L13 while visiting $x$ or a node below $x$. By the lines of the algorithm,

- $\mathrm{Fol}(x) = \emptyset$ for a leaf $x$;
- $\mathrm{Fol}(s \mid t) = \mathrm{Fol}(s) \cup \mathrm{Fol}(t)$;
- $\mathrm{Fol}(st) = \mathrm{Fol}(s) \cup \mathrm{Fol}(t) \cup \mathrm{Last}(s) \times \mathrm{First}(t)$;
- $\mathrm{Fol}(s^*) = \mathrm{Fol}(s) \cup \mathrm{Last}(s) \times \mathrm{First}(s)$.

Also $\mathrm{First}(x), \mathrm{Last}(x) \subseteq \mathrm{pos}(x)$ and $\mathrm{Fol}(x) \subseteq \mathrm{pos}(x) \times \mathrm{pos}(x)$, by induction. At the end, $\mathrm{Follow}(p) = \{q : (p, q) \in \mathrm{Fol}(r)\}$ for $p \ge 1$.

**Lemma 1.** $N(x)$ is true if and only if $\varepsilon \in L(x)$.

*Proof.* By induction on $x$. Leaves: $L(\emptyset)$ and $L(a)$ do not contain $\varepsilon$, and $L(\varepsilon)$ does. Then $\varepsilon \in L(s \mid t)$ if and only if $\varepsilon \in L(s)$ or $\varepsilon \in L(t)$; $\varepsilon \in L(st)$ if and only if $\varepsilon \in L(s)$ and $\varepsilon \in L(t)$; and $\varepsilon \in L(s^*)$ always. These are lines L6, L9 and L14. $\square$

**Lemma 2 (locality).** For every node $x$ and every nonempty word $u = p_1 \cdots p_n$ over the positions, $u \in L(\bar x)$ if and only if (a) $p_1 \in \mathrm{First}(x)$, (b) $p_n \in \mathrm{Last}(x)$ and (c) $(p_i, p_{i+1}) \in \mathrm{Fol}(x)$ for $1 \le i < n$.

*Proof.* By induction on $x$. Call $u$ *good for $x$* if (a), (b) and (c) hold.

- $x = \emptyset$ or $x = \varepsilon$: $L(\bar x)$ has no nonempty word, and $\mathrm{First}(x) = \emptyset$, so no word is good.
- $x$ is the position $p$: $L(\bar x) = \{p\}$. A good word has $p_1 = p_n = p$ and, since $\mathrm{Fol}(x) = \emptyset$, length 1; so it is $p$.
- $x = s \mid t$. If $u \in L(\bar s)$, then $u$ is good for $s$ by induction, hence good for $x$, since each set of $x$ contains that of $s$; the same for $t$. Conversely, let $u$ be good for $x$. Every pair of $\mathrm{Fol}(x)$ lies in $\mathrm{pos}(s)^2$ or in $\mathrm{pos}(t)^2$, and these sets are disjoint, so by (c) all letters of $u$ lie in $\mathrm{pos}(s)$, or all in $\mathrm{pos}(t)$. In the first case $p_1 \in \mathrm{First}(x) \cap \mathrm{pos}(s) = \mathrm{First}(s)$, $p_n \in \mathrm{Last}(s)$, and the pairs lie in $\mathrm{Fol}(x) \cap \mathrm{pos}(s)^2 = \mathrm{Fol}(s)$; so $u$ is good for $s$ and $u \in L(\bar s) \subseteq L(\bar x)$. The second case is the same.
- $x = st$. Let $u \in L(\bar x)$, so $u = vv'$ with $v \in L(\bar s)$ and $v' \in L(\bar t)$. If $v = \varepsilon$, then $\varepsilon \in L(s)$, so $N(s)$ holds by Lemma 1 and $\mathrm{First}(t) \subseteq \mathrm{First}(x)$; $u = v'$ is good for $t$, and hence for $x$. If $v' = \varepsilon$, the argument is symmetric with $N(t)$ and $\mathrm{Last}(s) \subseteq \mathrm{Last}(x)$. If both are nonempty, $v$ is good for $s$ and $v'$ for $t$, so $p_1 \in \mathrm{First}(s) \subseteq \mathrm{First}(x)$, $p_n \in \mathrm{Last}(t) \subseteq \mathrm{Last}(x)$, the pairs inside $v$ and $v'$ are in $\mathrm{Fol}(x)$, and the pair at the junction is in $\mathrm{Last}(s) \times \mathrm{First}(t) \subseteq \mathrm{Fol}(x)$. Conversely, let $u$ be good for $x$. No pair of $\mathrm{Fol}(x)$ goes from $\mathrm{pos}(t)$ to $\mathrm{pos}(s)$, so $u = vv'$ where $v$ has its letters in $\mathrm{pos}(s)$ and $v'$ in $\mathrm{pos}(t)$. If $v = \varepsilon$: $p_1 \in \mathrm{First}(x) \cap \mathrm{pos}(t)$, which is not empty only if $N(s)$ holds, and then it is a subset of $\mathrm{First}(t)$; also $p_n \in \mathrm{Last}(x) \cap \mathrm{pos}(t) = \mathrm{Last}(t)$ and the pairs are in $\mathrm{Fol}(t)$. So $u$ is good for $t$, $u \in L(\bar t)$, and $\varepsilon \in L(s)$ by Lemma 1, so $u \in L(\bar x)$. If $v' = \varepsilon$, the argument is symmetric. If both are nonempty, $v$ starts in $\mathrm{First}(x) \cap \mathrm{pos}(s) = \mathrm{First}(s)$, its pairs are in $\mathrm{Fol}(x) \cap \mathrm{pos}(s)^2 = \mathrm{Fol}(s)$, and its last letter is in $\mathrm{Last}(s)$ because the junction pair lies in $\mathrm{Fol}(x)$ and goes from $\mathrm{pos}(s)$ to $\mathrm{pos}(t)$, so it is in $\mathrm{Last}(s) \times \mathrm{First}(t)$. So $v$ is good for $s$, and in the same way $v'$ is good for $t$. By induction, $u = vv' \in L(\bar s) L(\bar t) = L(\bar x)$.
- $x = s^*$. Let $u \in L(\bar x)$, nonempty. Then $u = v_1 \cdots v_j$ with $j \ge 1$ and each $v_l$ a nonempty word of $L(\bar s)$ (drop the empty factors). Each $v_l$ is good for $s$; the pairs inside the factors are in $\mathrm{Fol}(s)$, and each pair at a junction is in $\mathrm{Last}(s) \times \mathrm{First}(s)$. So $u$ is good for $x$, since $\mathrm{First}(x) = \mathrm{First}(s)$ and $\mathrm{Last}(x) = \mathrm{Last}(s)$. Conversely, let $u$ be good for $x$; all its letters are in $\mathrm{pos}(s)$. Cut $u$ between $p_i$ and $p_{i+1}$ whenever $(p_i, p_{i+1}) \notin \mathrm{Fol}(s)$. Such a pair is in $\mathrm{Fol}(x) \setminus \mathrm{Fol}(s) \subseteq \mathrm{Last}(s) \times \mathrm{First}(s)$, so each piece starts in $\mathrm{First}(s)$ (the first piece by (a), the others by the cut), ends in $\mathrm{Last}(s)$ (the last piece by (b), the others by the cut), and has all its pairs in $\mathrm{Fol}(s)$. So each piece is good for $s$, is in $L(\bar s)$ by induction, and $u \in L(\bar s)^+ \subseteq L(\bar x)$. $\square$

**Lemma 3.** $L(x) = h(L(\bar x))$ for every node $x$.

*Proof.* $h$ is a homomorphism, so it commutes with union, concatenation and star of languages, and $h(\{p\}) = \{\mathrm{sym}(p)\}$ for a leaf. Induction on $x$. $\square$

**Theorem.** The automaton $G$ returned at line L18 accepts exactly $L(r)$.

*Proof.* The empty word is accepted if and only if $0 \in F$, that is, if and only if $N(r)$ holds, which by Lemma 1 means $\varepsilon \in L(r)$.

Let $w = a_1 \cdots a_n$ with $n \ge 1$. Every move into a state $q$ reads $\mathrm{sym}(q)$, and no move enters state 0. So an accepting run of $G$ on $w$ is a sequence of states $0, p_1, \ldots, p_n$ with $p_1 \in \mathrm{Follow}(0) = \mathrm{First}(r)$, $p_{i+1} \in \mathrm{Follow}(p_i)$, that is $(p_i, p_{i+1}) \in \mathrm{Fol}(r)$, $\mathrm{sym}(p_i) = a_i$ for each $i$, and $p_n \in F$; since $p_n \ne 0$, this means $p_n \in \mathrm{Last}(r)$. By Lemma 2, such a sequence exists if and only if some word $p_1 \cdots p_n \in L(\bar r)$ has $h(p_1 \cdots p_n) = w$. By Lemma 3, this holds if and only if $w \in L(r)$. $\blacksquare$
