---
tag: KY4MQM
kind: theorem
slug: kleene-theorem
name: Kleene's theorem
aliases:
- Kleene's characterization
- Kleene's theorem on regular expressions and automata
- regex and finite automata equivalence
area: automata-and-parsing/finite-automata
level: intro
summary: Regular expressions, finite automata and regular languages describe exactly the same class of languages.
prereqs: [deterministic-finite-automaton, epsilon-nfa, regular-expression]
see_also: [thompson-construction, subset-construction, state-elimination, dfa-to-regex-conversion, regular-language, closure-properties-of-regular-languages, arden-lemma, glushkov-automaton]
sources:
  - paper: "Stephen C. Kleene, Representation of events in nerve nets and finite automata, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 3 to 41 (regular events and their representation by nerve nets)
  - paper: "Robert McNaughton and Hisao Yamada, Regular expressions and state graphs for automata, IRE Transactions on Electronic Computers EC-9(1) (1960)"
    locator: pp. 39 to 47
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, Regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 3.2, Finite Automata and Regular Expressions (the construction of the expressions R_ij^(k) and the conversion of expressions to epsilon-NFAs)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.3, Regular Expressions (Theorem 1.54 and the generalized NFA)
  - paper: "Andrzej Ehrenfeucht and Paul Zeiger, Complexity measures for regular expressions, Journal of Computer and System Sciences 12(2) (1976)"
    locator: pp. 134 to 146 (automata whose regular expressions must be exponentially long)
---

Kleene's theorem says that a language is described by a [regular expression](/regular-expression/) if and only if it is accepted by a finite automaton. So regular expressions, [deterministic finite automata](/deterministic-finite-automaton/), [NFAs](/nondeterministic-finite-automaton/) and [epsilon-NFAs](/epsilon-nfa/) all define one class, the [regular languages](/regular-language/). Each direction of the proof is a construction that programs use: a regex engine turns an expression into an automaton, and the reverse direction turns an automaton back into an expression.

## Statement

Fix a finite alphabet $\Sigma$. The regular expressions over $\Sigma$ and their languages $L(E)$ are defined by structural induction:

- $\emptyset$, $\varepsilon$ and each $a \in \Sigma$ are expressions, with $L(\emptyset) = \emptyset$, $L(\varepsilon) = \{\varepsilon\}$ and $L(a) = \{a\}$;
- if $E$ and $G$ are expressions, so are $(E + G)$, $(EG)$ and $(E^*)$, with $L(E + G) = L(E) \cup L(G)$, $L(EG) = L(E)L(G)$ and $L(E^*) = L(E)^*$.

Here $AB = \{xy : x \in A, y \in B\}$ and $A^* = \bigcup_{i \ge 0} A^i$, with $A^0 = \{\varepsilon\}$ and $A^{i+1} = A^i A$.

**Theorem (Kleene).** For each language $L \subseteq \Sigma^*$, the following are equivalent:

1. $L = L(E)$ for some regular expression $E$ over $\Sigma$;
2. $L = L(N)$ for some epsilon-NFA $N = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to 2^Q$;
3. $L = L(M)$ for some complete DFA $M = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to Q$ and no $\varepsilon$-moves.

The constructions are effective. An expression with $s$ symbols and operators gives an epsilon-NFA with at most $2s$ states, an epsilon-NFA with $n$ states gives a DFA with at most $2^n$ states, and a DFA with $n$ states gives an expression by $n$ rounds of a matrix recurrence.

## In plain words

There are two common ways to describe a set of words. One is a pattern built from letters with three operations: "this or that", "this followed by that", and "this repeated any number of times". The other is a machine with finitely many states that reads a word letter by letter and says yes or no at the end.

The theorem says that the two ways have the same power. For each pattern there is a machine that says yes to exactly the words of the pattern, and for each machine there is a pattern for exactly the words it accepts. Both directions are recipes that a program can follow. A pattern turns into a machine by gluing small machines together, one for each part of the pattern. A machine turns into a pattern by removing its states one at a time.

## Proof

The proof shows $1 \Rightarrow 2 \Rightarrow 3 \Rightarrow 1$. The full proof, with each induction written out, is in [the proof of Kleene's theorem](proofs/main.md). Its three steps:

- **$1 \Rightarrow 2$ (expressions to epsilon-NFAs).** By structural induction on $E$, build an epsilon-NFA with one start state $s$, one accepting state $f \neq s$, no transition into $s$ and no transition out of $f$. The base cases have two states. For $E + G$, a new start state has $\varepsilon$-moves to the two old start states, and the two old accepting states have $\varepsilon$-moves to a new accepting state. For $EG$, the accepting state of the first machine gets an $\varepsilon$-move to the start of the second. For $E^*$, new start and accepting states $s, f$ get the moves $s \to s_1$, $s \to f$, $f_1 \to s_1$ and $f_1 \to f$. The shape conditions make each case accept exactly the right strings. This is the [Thompson construction](/thompson-construction/).
- **$2 \Rightarrow 3$ (epsilon-NFAs to DFAs).** The DFA has the subsets of $Q$ as its states. Its start state is the [epsilon-closure](/epsilon-closure/) $\mathrm{Cl}(\{q_0\})$, its transition on $a$ maps $S$ to $\mathrm{Cl}(\bigcup_{q \in S} \delta(q, a))$, and $S$ is accepting when $S \cap F \neq \emptyset$. By induction on $|w|$, the DFA reaches on $w$ exactly the set of states that the epsilon-NFA can reach on $w$. This is the [subset construction](/subset-construction/).
- **$3 \Rightarrow 1$ (DFAs to expressions).** Number the states $1, \ldots, n$. Let $R^{(k)}_{ij}$ be the set of strings that lead from $i$ to $j$ such that every state that the run visits strictly between the start and the end is at most $k$. Then $R^{(0)}_{ij}$ is a finite set of symbols, plus $\varepsilon$ when $i = j$, and

$$R^{(k)}_{ij} = R^{(k-1)}_{ij} \,\cup\, R^{(k-1)}_{ik} \big(R^{(k-1)}_{kk}\big)^* R^{(k-1)}_{kj},$$

because a run that may pass through $k$ splits at its visits to $k$ into a first part, some loops from $k$ to $k$, and a last part. By induction on $k$ each $R^{(k)}_{ij}$ has an expression, and $L(M) = \bigcup_{j \in F} R^{(n)}_{q_0 j}$. This is the McNaughton-Yamada construction. [State elimination](/state-elimination/) computes the same sets in another order.

**Example.** Let $M$ accept the binary strings with an even number of 1s, with state 1 for "even" (start and accepting) and state 2 for "odd", and $\delta(i, 0) = i$, $\delta(1, 1) = 2$, $\delta(2, 1) = 1$. Then $R^{(0)}_{11} = R^{(0)}_{22} = \varepsilon + 0$ and $R^{(0)}_{12} = R^{(0)}_{21} = 1$. After simplification by $(\varepsilon + 0)^* = 0^*$, round 1 gives $R^{(1)}_{11} = 0^*$, $R^{(1)}_{12} = 0^*1$, $R^{(1)}_{21} = 10^*$ and $R^{(1)}_{22} = \varepsilon + 0 + 10^*1$. Round 2 gives

$$L(M) = R^{(2)}_{11} = 0^* + 0^*1\,(0 + 10^*1)^*\,10^*.$$

The shorter expression $(0 + 10^*1)^*$ denotes the same language. The construction does not find the shortest expression.

In the other direction, the expression $(a + b)^*a$ has three symbols, one union and one star. The Thompson construction gives an epsilon-NFA with $2 \cdot 5 = 10$ states and 12 transitions, 9 of them $\varepsilon$-moves, and it accepts the strings over $\{a, b\}$ that end in $a$.

## Consequences

- **One class, several descriptions.** The [regular languages](/regular-language/) can be given by whichever description is convenient. Closure under union, concatenation and star is immediate for expressions, and closure under complement and intersection is immediate for DFAs. Together they give all the [closure properties](/closure-properties-of-regular-languages/).
- **Decision procedures for expressions.** Questions about expressions, such as [regex equivalence](/regex-equivalence/) and [regex emptiness](/regex-emptiness/), become questions about automata.
- **Regex engines.** Matching an expression against a text uses the first two steps: [Thompson's construction](/thompson-construction/), then a simulation of the NFA ([Thompson NFA simulation](/thompson-nfa-simulation/)) or a DFA built on demand ([lazy DFA construction](/lazy-dfa-construction/)).
- **Lexer generators.** A lexer generator turns the expressions of the token types into one DFA by the same two steps, then minimizes it.
- **Algebra.** The recurrence of the third step solves a system of equations over languages. [Arden's lemma](/arden-lemma/) and [Kleene algebra](/kleene-algebra/) study these equations.

## Tightness

The three translations have very different costs.

- **Expression to epsilon-NFA: linear.** The Thompson automaton has at most $2s$ states for an expression of size $s$, and at most $4s$ transitions. The [Glushkov automaton](/glushkov-automaton/) has no $\varepsilon$-moves and one state more than the number of symbols in the expression.
- **Epsilon-NFA to DFA: exponential, and this is unavoidable.** Some NFAs with $n$ states need $2^n$ DFA states. See the [determinization blow-up lower bound](/determinization-blowup-lower-bound/).
- **DFA to expression: exponential, and this is unavoidable.** The expressions $R^{(k)}_{ij}$ can grow by a factor of about 4 in each round, so the expression that the construction outputs can have length of order $4^n$ times the size of the alphabet. Ehrenfeucht and Zeiger (1976) gave DFAs with $n$ states for which every equivalent regular expression has length exponential in $n$. See [DFA to regex conversion](/dfa-to-regex-conversion/).

## History

Kleene introduced regular expressions, under the name "regular events", in a RAND report of 1951 that appeared in the volume Automata Studies in 1956, where he proved that they describe exactly the events that McCulloch-Pitts nerve nets represent. McNaughton and Yamada (1960) gave the matrix construction of the third step and a direct construction from expressions to deterministic automata. Rabin and Scott (1959) introduced nondeterministic automata and the subset construction. Thompson (1968) gave the construction from expressions to automata with $\varepsilon$-moves for the text editor QED.

## References
