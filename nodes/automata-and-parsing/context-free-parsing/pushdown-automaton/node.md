---
tag: EWQZZV
kind: model
slug: pushdown-automaton
name: Pushdown automaton
aliases:
- PDA
area: automata-and-parsing/context-free-parsing
level: core
summary: A finite automaton with a stack, recognizing exactly the context-free languages.
prereqs: [nondeterministic-finite-automaton, stack, context-free-grammar]
see_also: [cfg-pda-equivalence, cfg-to-pda-conversion, deterministic-context-free-language, context-free-language, turing-machine, pushdown-system, knuth-lr-theorem, shift-reduce-parsing]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Chapter 6, Pushdown Automata (6.1 Definition, 6.2 The Languages of a PDA, 6.3 Equivalence of PDA's and CFG's, 6.4 Deterministic Pushdown Automata, and the references at the end of the chapter); Section 8.5.2, Multistack Machines
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.2, Pushdown Automata (Definition 2.13, Theorem 2.20); Section 2.4, Deterministic Context-Free Languages
  - paper: doi:10.1016/S0304-3975(00)00285-1
    title: Géraud Sénizergues, L(A)=L(B)? decidability results from complete formal systems, Theoretical Computer Science 251(1-2) (2001)
    locator: pp. 1 to 166 (the equivalence problem for deterministic pushdown automata is decidable)
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (LR(k) grammars and deterministic pushdown recognition)
---

A pushdown automaton is a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) that also has an unbounded [stack](/stack/): at each step it reads one input symbol or none, looks at its state and at the top symbol of the stack, and replaces that top symbol by a string while it changes state. The stack gives it exactly enough memory to match nested structure, so the languages that pushdown automata accept are exactly the [context-free languages](/context-free-language/). Every parser for a [context-free grammar](/context-free-grammar/) is at heart a pushdown automaton, and the deterministic ones are the [LR](/lr-parsing/) and LL parsers that compilers use.

## The machine

A **pushdown automaton** (PDA) is a 7-tuple $P = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$ where

- $Q$ is a finite set of states, $q_0 \in Q$ is the start state and $F \subseteq Q$ is the set of accepting states;
- $\Sigma$ is the finite input alphabet and $\Gamma$ is the finite stack alphabet, with the start stack symbol $Z_0 \in \Gamma$;
- $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \times \Gamma \to$ the finite subsets of $Q \times \Gamma^*$ is the transition function.

A **configuration** (or instantaneous description) is a triple $(q, w, \gamma)$: the state $q$, the input $w$ that is not yet read, and the stack $\gamma \in \Gamma^*$, written with its top on the left. One **move** is

$$(q, aw, X\beta) \vdash (p, w, \alpha\beta) \quad \text{if } (p, \alpha) \in \delta(q, a, X), \text{ for } a \in \Sigma \cup \{\varepsilon\}.$$

So a move pops the top symbol $X$ and pushes the string $\alpha$, with the first symbol of $\alpha$ on top. With $a = \varepsilon$ the move reads no input (an $\varepsilon$-move). A machine with an empty stack has no move. The relation $\vdash^*$ is the reflexive and transitive closure of $\vdash$. There are two ways to accept:

$$L(P) = \{\, w : (q_0, w, Z_0) \vdash^* (q, \varepsilon, \gamma),\ q \in F \,\}, \qquad N(P) = \{\, w : (q_0, w, Z_0) \vdash^* (q, \varepsilon, \varepsilon) \,\}.$$

$L(P)$ is acceptance by final state and $N(P)$ is acceptance by empty stack. The machine is nondeterministic: it accepts $w$ if at least one sequence of moves accepts.

A PDA is **deterministic** (a DPDA) if for all $q$, $a \in \Sigma$ and $X \in \Gamma$: $|\delta(q, a, X)| \le 1$, $|\delta(q, \varepsilon, X)| \le 1$, and $\delta(q, a, X)$ and $\delta(q, \varepsilon, X)$ are not both nonempty. Then each configuration has at most one move.

This page uses the grammar notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the size of a grammar.

**Example: even palindromes.** The language $\{ w w^R : w \in \{0, 1\}^* \}$ is accepted by final state by the PDA with states $q_0, q_1, q_2$, $F = \{q_2\}$, and the moves, for each $a \in \{0, 1\}$ and $X \in \{0, 1, Z_0\}$:

- $\delta(q_0, a, X) \ni (q_0, aX)$: push the symbol that is read;
- $\delta(q_0, \varepsilon, X) \ni (q_1, X)$: guess that the middle of the input is here;
- $\delta(q_1, a, a) \ni (q_1, \varepsilon)$: pop a symbol that matches the input;
- $\delta(q_1, \varepsilon, Z_0) \ni (q_2, Z_0)$: the stack is back to its bottom, so accept.

An accepting computation on $1001$ is

$$(q_0, 1001, Z_0) \vdash (q_0, 001, 1Z_0) \vdash (q_0, 01, 01Z_0) \vdash (q_1, 01, 01Z_0) \vdash (q_1, 1, 1Z_0) \vdash (q_1, \varepsilon, Z_0) \vdash (q_2, \varepsilon, Z_0).$$

The machine guesses the middle. On $1001$ there are 14 reachable configurations in all, and only one path among them accepts. On $101$ none of the 9 reachable configurations accepts, since the length is odd.

**Example: a grammar as a PDA.** For a grammar $G$, the one-state PDA with stack alphabet $V \cup \Sigma$, start stack symbol $S$, a move $\delta(q, \varepsilon, A) \ni (q, \alpha)$ for each production $A \to \alpha$ (expand) and a move $\delta(q, a, a) \ni (q, \varepsilon)$ for each terminal $a$ (match) accepts $L(G)$ by empty stack. For $S \to aSb \mid \varepsilon$ and the input $aabb$:

$$(q, aabb, S) \vdash (q, aabb, aSb) \vdash (q, abb, Sb) \vdash (q, abb, aSbb) \vdash (q, bb, Sbb) \vdash (q, bb, bb) \vdash (q, b, b) \vdash (q, \varepsilon, \varepsilon).$$

The stack always holds the unread part of a [left-sentential form](/sentential-form/), so the accepting computations are the [leftmost derivations](/leftmost-derivation/). This is the construction of [CFG to PDA conversion](/cfg-to-pda-conversion/) and the idea of every [top-down parser](/top-down-parsing/).

## What it counts

The unit of work is one move. A move reads at most one input symbol and replaces one stack symbol by a string of bounded length, so with a fixed machine it is $O(1)$ work on a RAM. The questions about a PDA are of two kinds.

- **What it can decide.** Which languages a PDA or a DPDA accepts, under which acceptance mode. This is the main use of the model: it sorts languages into regular, deterministic context-free and context-free.
- **How many moves.** A nondeterministic PDA may have many computations, some of them infinite through $\varepsilon$-moves that push without bound, so its "time" is not a single number. To decide membership on a real machine, one simulates all computations at once, and the cost is counted in RAM steps as a function of $n$ and of the size of $P$. A DPDA that never loops runs in $O(n)$ moves for a fixed machine, which is the bound of the deterministic parsers.

The stack is the only unbounded memory, and only its top symbol is visible. A machine that could read deeper into its stack, or that had two stacks, is a different model.

## Relation to other models

- **Finite automata.** A PDA that never changes its stack is a [nondeterministic finite automaton](/nondeterministic-finite-automaton/), so every [regular language](/regular-language/) is the language of a PDA, even of a DPDA. The language $\{0^k 1^k : k \ge 0\}$ shows that the inclusion is strict.
- **Context-free grammars.** PDAs and grammars define the same class of languages ([CFG and PDA equivalence](/cfg-pda-equivalence/)). The grammar-to-PDA direction is the expand-and-match machine above. The other direction builds a nonterminal $[pXq]$ that derives the inputs that take the machine from state $p$ with $X$ on top to state $q$ with $X$ popped.
- **Deterministic PDAs.** DPDAs accept the [deterministic context-free languages](/deterministic-context-free-language/), a proper subclass: the even palindromes above need the guess of the middle, and no DPDA accepts them. A DPDA that accepts by empty stack accepts only languages with the prefix property (no word is a proper prefix of another word), so for DPDAs acceptance by final state is the stronger mode. The deterministic context-free languages are exactly the languages of [LR(1) grammars](/lr-grammar/), and an [LR parser](/lr-parsing/) is a DPDA whose states are sets of [LR items](/lr-item/).
- **Turing machines.** A machine with two stacks simulates a [Turing machine](/turing-machine/): one stack holds the tape to the left of the head and the other holds the rest. So two stacks give full computational power, and one stack does not: $\{a^k b^k c^k\}$ is not context-free by the [pumping lemma for context-free languages](/cfl-pumping-lemma/).
- **Pushdown systems.** A [pushdown system](/pushdown-system/) is a PDA without input, used in model checking to describe programs with recursive procedures. The stack holds the return addresses.

## Known results in the model

1. **The acceptance modes agree.** For each PDA $P$ there is a PDA $P'$ with $N(P') = L(P)$, and conversely. To go from final state to empty stack, put a new bottom symbol under $Z_0$, and from each accepting state add $\varepsilon$-moves to a state that pops everything. To go from empty stack to final state, put a new bottom symbol $X_0$ under $Z_0$; when $X_0$ is on top, the old machine has emptied its stack, so move to a new accepting state. The new bottom symbol in both constructions stops the machine from emptying its stack by accident.
2. **PDAs and grammars are equivalent.** A language is context-free if and only if some PDA accepts it (Sipser, Theorem 2.20). The conversions are polynomial: a grammar of size $|G|$ gives a PDA of size $O(|G|)$, and a PDA with $|Q|$ states gives a grammar with $O(|Q|^2 |\Gamma|)$ nonterminals, after the moves are put in a form that pushes at most two symbols.
3. **Membership is cubic.** Given a PDA and an input of length $n$, convert it to a grammar and run the [CYK algorithm](/cyk-algorithm/) or the [Earley parser](/earley-parser/). The time is $O(n^3)$ for a fixed machine and polynomial in its size. By [Valiant's algorithm](/valiant-algorithm/), $O(n^\omega)$ is possible for a fixed grammar.
4. **Emptiness is decidable, equivalence is not.** Whether $L(P) = \emptyset$ is decided in polynomial time on the grammar ([CFG emptiness](/cfg-emptiness-problem/)). Whether two PDAs accept the same language is undecidable ([CFG equivalence](/cfg-equivalence-undecidable/)).
5. **DPDA equivalence is decidable.** Sénizergues proved in 1997 that it is decidable whether two DPDAs accept the same language; the journal version appeared in 2001.
6. **DPDAs and LR grammars.** Knuth showed in 1965 that the languages of LR($k$) grammars are exactly the languages accepted by DPDAs, and that $k = 1$ is enough ([Knuth's LR theorem](/knuth-lr-theorem/)). The languages accepted by DPDAs have unambiguous grammars.
7. **Closure.** The class of context-free languages is closed under union, concatenation, star and intersection with a regular language, and not under intersection or complement ([closure properties](/cfl-closure-properties/)). The deterministic class is closed under complement and not under union.
8. **Reachability.** The set of configurations of a pushdown system reachable from a regular set of configurations is again regular, and [pushdown saturation](/pushdown-saturation/) builds a finite automaton for it in polynomial time ([pushdown reachability](/pushdown-reachability/)).

### Pitfalls

- **The top of the stack.** In the notation $(q, w, \gamma)$, the top is the first symbol of $\gamma$. A move $(p, XY)$ pushes $Y$ first and then $X$, so $X$ is on top.
- **An empty stack stops the machine.** A move needs a top symbol, so a PDA that pops $Z_0$ by mistake can make no more moves. The constructions above use a fresh bottom symbol for this reason.
- **Determinism is about the whole machine.** A PDA with $\delta(q, \varepsilon, X)$ and $\delta(q, a, X)$ both nonempty is not deterministic, even when each set has one element.
- **Infinite computations.** A PDA can push forever with $\varepsilon$-moves, so a breadth-first search of the configurations does not end on its own. A simulation must bound the stack height or work on the grammar.

## References
