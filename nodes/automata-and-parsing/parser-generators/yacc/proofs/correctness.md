---
title: Correctness of the yacc construction and of its parser
proves: [correctness]
status: full
---

We prove three things about the algorithm on the [yacc](/yacc/) page: lines L1 to L4 build the LALR(1) table, lines L5 to L7 keep one action per cell by the stated rules, and for an LALR(1) grammar the parser with default reductions accepts exactly $L(G)$ and reports its first error at the earliest possible token.

**Notation and assumptions.** $G = (V, \Sigma, P, S)$ is augmented with $S' \to S$ as production 0, and $S'$ occurs on no right side. $G$ is reduced: every nonterminal is reachable from $S$ and derives some terminal string. An LR(1) item is $[i, a]$ with $i$ a dotted production and $a \in \Sigma \cup \{\$\}$; the LR(1) closure adds $[B \to \cdot \eta,\ b]$ for every item $[A \to \alpha \cdot B \beta,\ a]$, every production $B \to \eta$ and every $b \in \mathrm{FIRST}(\beta a)$. The *core* of a set of LR(1) items is the set of its dotted productions. For an LR(0) state $s$ and a kernel item $i$ of $s$, let
$$\mathrm{LA}(s, i) = \{ a : [i, a] \in J \text{ for some canonical LR(1) state } J \text{ whose core is the closure of } s \}.$$
The LALR(1) table is, by definition, the table of the canonical LR(1) states merged by core.

## Part 1: the lookaheads

**Lemma 1 (closure is linear in the lookahead).** Let $\#$ be a symbol outside $V \cup \Sigma \cup \{\$\}$, used as a terminal. For a kernel item $i$ and a lookahead $b$, the closure of $\{[i, b]\}$ is obtained from the closure of $\{[i, \#]\}$ by replacing $\#$ with $b$ in every item. The closure of a set of items is the union of the closures of its elements.

*Proof.* The closure rule acts on one item at a time and computes $\mathrm{FIRST}(\beta a)$, which is $\mathrm{FIRST}(\beta)$, together with $a$ when $\beta$ is nullable. The symbol $a$ is used only as a terminal that is copied, so renaming $\#$ to $b$ maps each application of the rule for $\#$ to an application for $b$ and back; since $\#$ is in no FIRST set, no other lookahead is affected. Because each rule application looks at one item only, a closure of a union is the union of the closures. $\square$

Lemma 1 justifies the classification of line L2: in the closure of $\{[i, \#]\}$, an item $[B \to \gamma \cdot X \delta,\ c]$ with $c \ne \#$ contributes $c$ to the successor kernel item $j = [B \to \gamma X \cdot \delta]$ of $t = \mathrm{GOTO}(s, X)$ whatever the lookahead of $i$ is (spontaneous), and an item with $c = \#$ contributes exactly the lookaheads of $i$ (a link from $(s, i)$ to $(t, j)$).

Two standard facts about the canonical collections are used. (F1) The core of $\mathrm{GOTO}_1(J, X)$ for an LR(1) state $J$ is the LR(0) state $\mathrm{GOTO}(\mathrm{core}(J), X)$, because both GOTO functions move the dot over $X$ in the same dotted productions and close in the same way, the LR(1) closure adding a dotted production exactly when the LR(0) closure does: the lookahead set $\mathrm{FIRST}(\beta a)$ is never empty, since every symbol derives a terminal string. (F2) For the same reason every LR(0) state is the core of some LR(1) state, and in an LR(1) state $J$ every kernel dotted production carries at least one lookahead.

Let $\ell(s, i)$ be the set that line L3 leaves for the kernel item $i$ of state $s$.

**Theorem 1.** $\ell(s, i) = \mathrm{LA}(s, i)$ for every state $s$ and kernel item $i$.

*Proof of $\subseteq$.* By induction on the steps that add a lookahead to some $\ell$.

- *Start.* $\$$ is put on $[S' \to \cdot S]$ in state 0; the canonical start state contains $[S' \to \cdot S,\ \$]$.
- *Spontaneous.* Suppose $c$ is spontaneous for $(t, j)$, coming from the kernel item $i$ of $s$ through an item $[B \to \gamma \cdot X \delta,\ c]$ in the closure of $\{[i, \#]\}$. By (F2) there is an LR(1) state $J$ with core $s$ and an item $[i, b] \in J$. By Lemma 1 the closure of $\{[i, b]\}$, which is part of $J$, contains $[B \to \gamma \cdot X \delta,\ c]$, so $\mathrm{GOTO}_1(J, X)$ contains $[j, c]$, and its core is $t$ by (F1). Hence $c \in \mathrm{LA}(t, j)$.
- *Link.* Suppose $a$ is copied along a link from $(s, i)$ to $(t, j)$, with $a \in \ell(s, i)$. By induction $a \in \mathrm{LA}(s, i)$, so some LR(1) state $J$ with core $s$ has $[i, a]$. By Lemma 1 its closure contains $[B \to \gamma \cdot X \delta,\ a]$, and $\mathrm{GOTO}_1(J, X)$, of core $t$, contains $[j, a]$.

*Proof of $\supseteq$.* By induction on the order in which the canonical LR(1) states are discovered, we show that every kernel item $[j, a]$ of an LR(1) state $K$ with core $t$ has $a \in \ell(t, j)$. The start state has the single kernel item $[S' \to \cdot S,\ \$]$, and $\$ \in \ell(0, [S' \to \cdot S])$. Any other state is $K = \mathrm{GOTO}_1(J, X)$ for an earlier state $J$ of core $s$, with $t = \mathrm{GOTO}(s, X)$ by (F1). A kernel item $[j, a]$ of $K$ comes from an item $[B \to \gamma \cdot X \delta,\ a]$ of $J$, which by Lemma 1 lies in the closure of some single kernel item $[i, b]$ of $J$. Again by Lemma 1, the closure of $\{[i, \#]\}$ contains $[B \to \gamma \cdot X \delta,\ c]$ with either $c = a$ and $a \ne \#$, so that $a$ is spontaneous for $(t, j)$, or $c = \#$ and $a = b$, so that $(s, i)$ is linked to $(t, j)$. In the first case $a \in \ell(t, j)$ from the start of L3. In the second, $b \in \ell(s, i)$ by induction, and since L3 stops only when no link can enlarge its target, $b \in \ell(t, j)$. $\square$

**Corollary 2.** The cells filled by line L4 are the cells of the canonical LR(1) table merged by core.

*Proof.* Shift entries depend only on the cores, and the LR(0) GOTO equals the merged LR(1) GOTO by (F1). For reductions, line L4 closes the kernel of $s$ with the sets $\ell(s, i)$. By Lemma 1 and Theorem 1 this closure is the union, over the LR(1) states $J$ with core $s$, of the closures of their kernels, that is, of the states $J$ themselves. So a completed item gets lookahead $a$ in L4 exactly when it has $a$ in some LR(1) state of that core, which is the merged table. Accept is the reduction by production 0 on $\$$. $\square$

## Part 2: resolution

**Lemma 3.** After L5 to L7 every cell holds at most one action, and:

1. a cell with a single action keeps it;
2. a cell with a shift on $a$ and one reduction by $p$, where $a$ and $p$ have precedences $\pi(a)$ and $\pi(p)$, keeps the shift if $\pi(a) > \pi(p)$ or if they are equal and declared `%right`, keeps the reduction if $\pi(a) < \pi(p)$ or if they are equal and declared `%left`, and becomes an error if they are equal and declared `%nonassoc`; no conflict is reported;
3. a cell where a shift and a reduction remain after L5 keeps the shift and reports a shift-reduce conflict, and a cell with only reductions keeps the one of the smallest production number and reports a reduce-reduce conflict.

*Proof.* Single actions skip resolution. In L5 the loop over the reductions of the cell compares each one with the shift while the shift is present and both precedences are defined; the three branches implement the comparisons of item 2, dropping the reduction, dropping the shift, or dropping both. Equal precedence means the same declaration line, so the associativity is that of the token. Reductions without a precedence, or met after the shift was dropped, are kept. If a shift and at least one kept reduction remain, L6 returns the shift; otherwise if two or more reductions remain, L7 returns the first, and they are sorted by production number. Every branch returns one action or none. $\square$

## Part 3: the parser with default reductions

Assume now that the table of Corollary 2 has no conflict, that is, $G$ is LALR(1), so Part 2 changes nothing. Write $\mathcal{P}$ for the parser that uses only the table, and $\mathcal{D}$ for the parser of lines L8 to L11, which takes the default reduction of a state whose only action, over all tokens, is one reduction $r$.

Two facts are taken from the [LALR(1) parsing](/lalr-parsing/) page: $\mathcal{P}$ halts on every input and accepts exactly $L(G)$. A third fact is the soundness of the driver proved on the [parsing table](/parsing-table/) page: any driver whose shifts and gotos follow the LR(0) automaton and whose reductions are by completed items of the top state accepts only strings of $L(G)$; it applies to $\mathcal{D}$, since a default reduction is a table entry of its state.

**Lemma 4.** On every input, until $\mathcal{P}$ reports an error, $\mathcal{D}$ makes the same moves as $\mathcal{P}$.

*Proof.* In a configuration where $\mathcal{P}$ has an action $x$ for the top state $q$ and the token $a$, if $q$ has a default reduction $r$ then every action of row $q$ is $r$, so $x = r$, and $\mathcal{D}$ also reduces by $r$; otherwise $\mathcal{D}$ reads the same cell. The moves change the configuration in the same way. $\square$

**Lemma 5.** If $\mathcal{D}$ or $\mathcal{P}$ shifts the token $a_j$ of the input $a_1 \cdots a_n$, then $a_1 \cdots a_j$ is a prefix of a sentence of $G$.

*Proof.* At the shift the state stack spells, by the soundness invariant, symbols $X_1 \cdots X_m$ with $X_1 \cdots X_m \Rightarrow^* a_1 \cdots a_{j-1}$, and the shift entry exists only if the LR(0) state reached on $X_1 \cdots X_m$ has an item $[A \to \alpha \cdot a_j \beta]$. That state is the set of items valid for the viable prefix $X_1 \cdots X_m$ ([LR item sets](/lr-item-sets/)), so $X_1 \cdots X_m a_j$ is a viable prefix: $S' \Rightarrow_{rm}^* X_1 \cdots X_m a_j \beta w$ for some $\beta$ and $w$. Since $G$ is reduced, $\beta$ derives some terminal string $v$, so $a_1 \cdots a_j v w \in L(G)$. $\square$

**Theorem 6.** $\mathcal{D}$ accepts exactly $L(G)$. Let $w = a_1 \cdots a_n \notin L(G)$, and let $k$ be the largest number such that $a_1 \cdots a_k$ is a prefix of a sentence. Then $\mathcal{D}$ shifts $a_1, \ldots, a_k$ without reporting an error, never shifts $a_{k+1}$, and never accepts; so if it reports an error, the first one is at position $k$, counting positions from 0 and with position $n$ meaning the end marker.

*Proof.* If $w \in L(G)$ then $\mathcal{P}$ accepts $w$ without an error, and by Lemma 4 $\mathcal{D}$ makes the same moves and accepts. If $w \notin L(G)$, $\mathcal{D}$ does not accept it, by soundness.

Now let $w \notin L(G)$ and choose a sentence $a_1 \cdots a_k v \in L(G)$. On that sentence $\mathcal{D}$ accepts, so it shifts each of $a_1, \ldots, a_k$ without an error. Every decision that $\mathcal{D}$ takes before shifting $a_k$ depends only on its stack and on the current token, which is one of $a_1, \ldots, a_k$; so on $w$ it makes exactly the same moves up to and including the shift of $a_k$, and reports no error before. If $k < n$, Lemma 5 shows that $\mathcal{D}$ never shifts $a_{k+1}$, since $a_1 \cdots a_{k+1}$ is not a prefix of a sentence. From then on its only possible moves are reductions, an accept, which soundness excludes, and an error. So the first error, if one is reported, is reported while $a_{k+1}$ is the current token, at position $k$. If $k = n$, the same argument with the end marker in place of $a_{k+1}$ applies: $\mathcal{D}$ cannot accept and can no longer shift, so the first error is at position $n$. $\square$

**Halting.** Theorem 6 does not by itself say that $\mathcal{D}$ reaches the error: after $\mathcal{P}$ would report it, $\mathcal{D}$ may still make default reductions. These reductions are table entries of their states, so each is a move that $\mathcal{P}$ would make with some token, and in every run of the tests the parser halts, but the proof above does not bound their number. The implementation therefore stops with an exception after a fixed number of steps; for the same reason, the claims about error recovery on the page, which concern what happens after the first error, are checked by tests rather than proved here. ∎
