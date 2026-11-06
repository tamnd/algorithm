---
tag: ABR1KQ
kind: theorem
slug: cfg-pda-equivalence
name: Equivalence of CFGs and pushdown automata
area: automata-and-parsing/context-free-parsing
level: core
summary: A language is context-free if and only if some pushdown automaton recognizes it.
prereqs: [context-free-grammar, pushdown-automaton, leftmost-derivation]
see_also: [cfg-to-pda-conversion, context-free-language, deterministic-context-free-language, kleene-theorem, cfl-closure-properties, top-down-parsing, shift-reduce-parsing, cfg-emptiness-problem]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 6.2.3 and 6.2.4 (from empty stack to final state and back), Section 6.3, Equivalence of PDA's and CFG's (6.3.1 From Grammars to Pushdown Automata, 6.3.2 From PDA's to Grammars), and Section 7.4.1, Complexity of Converting Among CFG's and PDA's
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.2, Pushdown Automata (Theorem 2.20, Lemma 2.21 and Lemma 2.27)
  - paper: doi:10.1016/S0019-9958(63)90306-1
    title: Marcel-Paul Schützenberger, On context-free languages and push-down automata, Information and Control 6(3) (1963)
    locator: pp. 246 to 264
  - paper: doi:10.1145/1463822.1463848
    title: R. James Evey, Application of pushdown-store machines, Proceedings of the AFIPS Fall Joint Computer Conference (1963)
    locator: from p. 215 (pushdown-store machines and the languages of grammars)
---

## Statement

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. A [pushdown automaton](/pushdown-automaton/) is $P = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$ with configurations $(q, w, \gamma)$, the top of the stack on the left, and the move relation $\vdash$. It accepts $L(P)$ by final state and $N(P)$ by empty stack:
$$L(P) = \{ w : (q_0, w, Z_0) \vdash^* (q, \varepsilon, \gamma),\ q \in F \}, \qquad N(P) = \{ w : (q_0, w, Z_0) \vdash^* (q, \varepsilon, \varepsilon) \}.$$

**Theorem.** For each language $L \subseteq \Sigma^*$, the following are equivalent:

1. $L = L(G)$ for some [context-free grammar](/context-free-grammar/) $G$;
2. $L = N(P)$ for some pushdown automaton $P$;
3. $L = L(P)$ for some pushdown automaton $P$.

The constructions are effective. A grammar $G$ gives a PDA with one state and $|R| + |\Sigma|$ moves. A PDA gives a grammar with $1 + |Q|^2 |\Gamma|$ nonterminals; a move that pushes $k$ symbols gives $|Q|^k$ productions, so after splitting the moves to push at most two symbols the grammar has polynomial size, $O(|Q|^3)$ productions per move.

## In plain words

A grammar describes a language by rules that build strings. A pushdown automaton is a machine that reads a string once, from left to right, with one stack. The theorem says the two ways describe exactly the same languages.

From a grammar, the machine keeps on its stack the part of the string it still expects. When the top is a rule symbol, it guesses a rule and replaces the symbol by the rule's right side. When the top is a letter, it checks the letter against the input. It accepts when the stack is empty at the end of the input.

From a machine, the grammar has one rule symbol for each question "can the machine go from state p to state q while it removes this one stack symbol?". The rules answer that question by splitting the run at the points where each pushed symbol is removed.

## Proof

The proof shows $1 \Rightarrow 2 \Leftrightarrow 3$ and $2 \Rightarrow 1$. The full proof, with each induction written out, is in [the proof of the equivalence](proofs/main.md). Its steps:

- **$1 \Rightarrow 2$ (top-down automaton).** The PDA $P_G$ has one state $q$, stack alphabet $V \cup \Sigma$ and start symbol $S$. It has an *expand* move $(q, \alpha) \in \delta(q, \varepsilon, A)$ for each production $A \to \alpha$ and a *match* move $(q, \varepsilon) \in \delta(q, a, a)$ for each terminal $a$. By induction, $(q, xy, \alpha) \vdash^* (q, y, \varepsilon)$ exactly when $\alpha \Rightarrow^*_{lm} x$, so the runs of $P_G$ are the [leftmost derivations](/leftmost-derivation/) of $G$, and $N(P_G) = L(G)$. This is the [CFG to PDA conversion](/cfg-to-pda-conversion/).
- **$2 \Leftrightarrow 3$ (kinds of acceptance).** A new bottom symbol $X_0$ marks the bottom. To go from empty stack to final state, move to a new final state when $X_0$ is on top. To go from final state to empty stack, let each final state move to a new state that pops everything, including $X_0$; the marker stops the original machine from emptying its stack by accident.
- **$2 \Rightarrow 1$ (the triple construction).** For states $p, q$ and a stack symbol $X$, the nonterminal $[pXq]$ derives exactly the strings $w$ with $(p, w, X) \vdash^* (q, \varepsilon, \varepsilon)$. A move $(r, Y_1 \cdots Y_k) \in \delta(p, a, X)$ gives the productions $[p X r_k] \to a [r Y_1 r_1][r_1 Y_2 r_2] \cdots [r_{k-1} Y_k r_k]$ for all states $r_1, \ldots, r_k$: the run after the move pops $Y_1$, then $Y_2$, and so on, and $r_i$ is the state when $Y_i$ is gone. The start productions are $S \to [q_0 Z_0 p]$ for all $p$.

**Example, grammar to automaton.** For $S \to a S b \mid \varepsilon$ the automaton has the moves $\delta(q, \varepsilon, S) = \{(q, aSb), (q, \varepsilon)\}$, $\delta(q, a, a) = \{(q, \varepsilon)\}$ and $\delta(q, b, b) = \{(q, \varepsilon)\}$. It accepts $aabb$ in 7 moves:
$$(q, aabb, S) \vdash (q, aabb, aSb) \vdash (q, abb, Sb) \vdash (q, abb, aSbb) \vdash (q, bb, Sbb) \vdash (q, bb, bb) \vdash (q, b, b) \vdash (q, \varepsilon, \varepsilon).$$
The three expand moves are the leftmost derivation $S \Rightarrow aSb \Rightarrow aaSbb \Rightarrow aabb$.

**Example, automaton to grammar.** Let $P$ have states $q, r$, stack symbols $Z, A$, start $(q, Z)$, and the moves
$$\delta(q, a, Z) \ni (q, AZ), \quad \delta(q, a, A) \ni (q, AA), \quad \delta(q, b, A) \ni (r, \varepsilon), \quad \delta(r, b, A) \ni (r, \varepsilon), \quad \delta(r, \varepsilon, Z) \ni (r, \varepsilon), \quad \delta(q, \varepsilon, Z) \ni (q, \varepsilon).$$
It pushes an $A$ for each $a$, pops one for each $b$, and $N(P) = \{a^n b^n : n \ge 0\}$. The triple construction gives 14 productions over the 8 nonterminals $[pXq]$. After removing the [useless symbols](/useless-symbol-elimination/), 8 productions remain:
$$S \to [qZq] \mid [qZr], \quad [qZq] \to \varepsilon, \quad [qZr] \to a [qAr][rZr], \quad [qAr] \to a [qAr][rAr] \mid b, \quad [rAr] \to b, \quad [rZr] \to \varepsilon.$$
A script confirms that the grammar generates $\varepsilon, ab, aabb, aaabbb, aaaabbbb$ and nothing else up to length 8, and that both constructions agree with a direct simulation of the automata on hundreds of random small grammars and automata.

## Consequences

- **Two views of one class.** The [context-free languages](/context-free-language/) can be handled with whichever description fits. Closure under union, concatenation and star is easy for grammars; closure under intersection with a regular language is easy for automata, by running a finite automaton beside the PDA. See [closure properties](/cfl-closure-properties/).
- **Parsers are pushdown automata.** The automaton $P_G$ is a nondeterministic [top-down parser](/top-down-parsing/). A [shift-reduce parser](/shift-reduce-parsing/) is another PDA for $L(G)$, which builds rightmost derivations in reverse. [LL](/ll1-parsing/) and [LR](/lr-parsing/) parsing make these automata deterministic for special grammars.
- **Decision procedures for automata.** Emptiness, finiteness and membership for PDAs reduce to the grammar problems ([emptiness](/cfg-emptiness-problem/), [finiteness](/cfg-finiteness-problem/), [membership](/cfg-membership-problem/)), and the undecidable grammar problems are undecidable for PDAs too.
- **One state is enough.** The construction $1 \Rightarrow 2$ gives a PDA with a single state, so every PDA that accepts by empty stack has an equivalent one-state PDA. The states can be moved into the stack symbols, as the triple construction shows.
- **The pumping lemma for automata.** Because of the equivalence, the [pumping lemma](/cfl-pumping-lemma/), proved on parse trees, also shows that some languages need more than one stack.

## Tightness

- **Determinism.** The theorem fails for deterministic machines. Deterministic PDAs accept the [deterministic context-free languages](/deterministic-context-free-language/), a proper subclass: the even palindromes $\{ w w^R \}$ are context-free but not deterministic. Deterministic PDAs that accept by empty stack accept only languages in which no string is a proper prefix of another, so the two kinds of acceptance differ for them.
- **The size of the grammar.** Without splitting, a move that pushes $k$ symbols gives $|Q|^k$ productions, so the triple construction is exponential in the length of the pushes. Splitting each push into pushes of at most two symbols first makes it polynomial (Hopcroft, Motwani and Ullman, Section 7.4.1).
- **More stacks.** A PDA with two stacks can simulate a [Turing machine](/turing-machine/), so the equivalence depends on having exactly one stack.

## History

Chomsky (1962), Evey (1963) and Schützenberger (1963) proved independently that the languages of pushdown-store machines are the context-free languages. The triple construction and the top-down automaton are presented in this form by Hopcroft, Motwani and Ullman and by Sipser, who uses a variant that pushes one symbol at a time and accepts by final state.

## References
