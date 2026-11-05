---
title: The partial derivative automaton accepts L(r) and has at most k + 1 states
proves: [correctness, termination]
status: full
---

Throughout, expressions are compared as terms (trees), $\nu$ and $S \odot t$ are as on the main page, and $\partial_a x$ is the set computed by lines L9 to L13. For a set $S$ of expressions write $L(S) = \bigcup_{z \in S} L(z)$, and let $\#x$ be the number of symbol occurrences in $x$.

**Lemma 1.** $\nu(x)$ is true if and only if $\varepsilon \in L(x)$.

*Proof.* By induction on $x$: $\varepsilon \notin L(\emptyset)$ and $\varepsilon \notin L(b)$; $\varepsilon \in L(\varepsilon)$ and $\varepsilon \in L(s^*)$; $\varepsilon \in L(s) \cup L(t)$ iff it is in one of them; and $\varepsilon \in L(s) L(t)$ iff it is in both, since $uv = \varepsilon$ forces $u = v = \varepsilon$. $\square$

**Lemma 2.** $L(S \odot t) = L(S)\, L(t)$.

*Proof.* If $t = \emptyset$, both sides are empty. If $t = \varepsilon$, both sides are $L(S)$. Otherwise each $z \in S$ contributes $L(zt) = L(z) L(t)$, or $L(t) = L(\varepsilon) L(t)$ when $z = \varepsilon$, and the union over $z$ is $L(S) L(t)$. $\square$

**Lemma 3.** For every expression $x$ and symbol $a$, $L(\partial_a x) = a^{-1} L(x)$, where $a^{-1}L = \{v : av \in L\}$.

*Proof.* By induction on $x$. For $\emptyset$ and $\varepsilon$, no word of $L(x)$ starts with $a$, and line L9 returns $\emptyset$. For a symbol $b$, $a^{-1}\{b\}$ is $\{\varepsilon\}$ if $b = a$ and empty otherwise, as at line L10. For $s \mid t$, $a^{-1}$ distributes over union (line L11). For $st$: $av \in L(s) L(t)$ iff either $av = (au) v'$ with $au \in L(s)$ and $v' \in L(t)$, so $v \in (a^{-1}L(s)) L(t)$, or $\varepsilon \in L(s)$ and $av \in L(t)$. By the induction hypothesis, Lemma 1 and Lemma 2, this is $L(\partial_a s \odot t) \cup L(\partial_a t)$ when $\nu(s)$ holds and $L(\partial_a s \odot t)$ otherwise, as at line L12. For $s^*$: $av \in L(s^*)$ iff $av = u_1 u_2 \cdots u_j$ with all $u_i \in L(s)$; dropping the empty factors, the first factor is $a u$ with $au \in L(s)$ and the rest is in $L(s^*)$. So $a^{-1}L(s^*) = (a^{-1}L(s)) L(s^*)$, which is $L(\partial_a s \odot s^*)$ by Lemma 2, as at line L13. $\square$

For a word $u$, $\partial_\varepsilon x = \{x\}$ and $\partial_{ua} x = \bigcup_{y \in \partial_u x} \partial_a y$. By induction on $u$ and Lemma 3, $L(\partial_u x) = u^{-1} L(x)$, since $(ua)^{-1} L = a^{-1}(u^{-1} L)$ and $a^{-1}$ distributes over union.

**Definition.** $\pi(\emptyset) = \pi(\varepsilon) = \emptyset$, $\pi(b) = \{\varepsilon\}$, $\pi(s \mid t) = \pi(s) \cup \pi(t)$, $\pi(st) = (\pi(s) \odot t) \cup \pi(t)$ and $\pi(s^*) = \pi(s) \odot s^*$.

**Lemma 4.** $|\pi(x)| \le \#x$.

*Proof.* By induction, using $|S \odot t| \le |S|$, which holds because $\odot$ maps each member of $S$ to at most one term: $|\pi(st)| \le |\pi(s)| + |\pi(t)| \le \#s + \#t$, and the other cases are similar. $\square$

**Lemma 5.** For every expression $x$ and symbol $a$: (i) $\partial_a x \subseteq \pi(x)$, and (ii) $\partial_a y \subseteq \pi(x)$ for every $y \in \pi(x)$.

*Proof.* By induction on $x$. Note that $S \subseteq S'$ implies $S \odot t \subseteq S' \odot t$.

- $x = \emptyset$ or $\varepsilon$: $\partial_a x = \pi(x) = \emptyset$.
- $x = b$: $\partial_a b \subseteq \{\varepsilon\} = \pi(b)$, and the only $y \in \pi(b)$ is $\varepsilon$, with $\partial_a \varepsilon = \emptyset$.
- $x = s \mid t$: both parts follow from the induction hypothesis for $s$ and $t$, since $\pi(x)$ is the union of $\pi(s)$ and $\pi(t)$.
- $x = st$: (i) $\partial_a x$ is $\partial_a s \odot t$, possibly with $\partial_a t$, which are subsets of $\pi(s) \odot t$ and $\pi(t)$ by (i) for $s$ and $t$. (ii) If $y \in \pi(t)$, use (ii) for $t$. Otherwise $y \in \pi(s) \odot t$, so $t \ne \emptyset$ and $y$ comes from some $z \in \pi(s)$. If $t = \varepsilon$, then $y = z$ and $\partial_a y \subseteq \pi(s) = \pi(s) \odot t$ by (ii) for $s$. If $z = \varepsilon$, then $y = t$ and $\partial_a t \subseteq \pi(t)$ by (i) for $t$. Otherwise $y$ is the term $zt$, and $\partial_a y$ is $\partial_a z \odot t$, possibly with $\partial_a t$; by (ii) for $s$, $\partial_a z \subseteq \pi(s)$, and by (i) for $t$, $\partial_a t \subseteq \pi(t)$.
- $x = s^*$: (i) $\partial_a x = \partial_a s \odot s^* \subseteq \pi(s) \odot s^*$. (ii) $y$ comes from some $z \in \pi(s)$, and $s^*$ is neither $\emptyset$ nor $\varepsilon$. If $z = \varepsilon$, then $y = s^*$ and (i) applies. Otherwise $y$ is the term $z s^*$, and $\partial_a y$ is $\partial_a z \odot s^*$, possibly with $\partial_a(s^*) = \partial_a s \odot s^*$; both are subsets of $\pi(s) \odot s^*$ by (ii) and (i) for $s$. $\square$

**Lemma 6.** Every set $Q$ built by lines L1 to L7 satisfies $Q \subseteq \{r\} \cup \pi(r)$, so $|Q| \le k + 1$.

*Proof.* Line L1 starts with $\{r\}$. A term $y$ is added at line L7 only when $y \in \partial_a x$ for some $x \in Q$, and by Lemma 5, $\partial_a r \subseteq \pi(r)$ and $\partial_a x \subseteq \pi(r)$ for $x \in \pi(r)$. The size bound is Lemma 4. $\square$

**Termination.** Each pass of the loop at lines L2 to L7 pops one term, and a term is pushed only when it is added to $Q$, at most once. By Lemma 6, at most $k + 1$ terms are ever pushed, so the loop runs at most $k + 1$ times. Each call `PARTIAL`$(x, a)$ ends: it processes the finitely many nodes below $x$, each once per symbol because of the memo. The loop at lines L16 to L17 runs $n$ times.

**Lemma 7.** After line L8, for every $x \in Q$ and symbol $a$, the moves of $T$ from $x$ on $a$ lead exactly to $\partial_a x$; for a symbol $c$ that does not occur in $r$, $\partial_c x = \emptyset$.

*Proof.* Every $x \in Q$ is pushed once and popped once, and when it is popped, lines L4 to L6 add the moves $(x, a, y)$ for all $y \in \partial_a x$ and all symbols $a$ of $r$. A term $x \in Q$ is $r$ or a member of $\pi(r)$, whose symbols all occur in $r$; by Lemma 3, $L(\partial_c x) = c^{-1} L(x) = \emptyset$, and by line L10, a term without the symbol $c$ has $\partial_c x = \emptyset$. $\square$

**Theorem.** PD-MATCH$(r, w)$ returns true if and only if $w \in L(r)$.

*Proof.* By Lemma 7 and induction on $i$, the set $S$ after $i$ rounds of line L17 is $\partial_{a_1 \cdots a_i} r$. If line L17 returns false, $S$ is empty, so $L(\partial_{a_1 \cdots a_i} r) = (a_1 \cdots a_i)^{-1} L(r)$ is empty and no word that starts with $a_1 \cdots a_i$ is in $L(r)$, in particular not $w$. Otherwise, line L18 returns whether some $x \in \partial_w r$ has $\nu(x)$, which by Lemma 1 holds iff $\varepsilon \in L(\partial_w r) = w^{-1} L(r)$, that is, iff $w \in L(r)$. $\blacksquare$
