---
tag: DR6BS2
kind: problem
slug: cfg-emptiness-problem
name: CFG emptiness problem
area: automata-and-parsing/context-free-parsing
level: core
summary: Decide whether a context-free grammar generates any string at all.
model: word-ram
complexity:
  vars: {g: the grammar size}
  time: {worst: O(g)}
prereqs: [context-free-grammar, derivation, parse-tree]
see_also: [useless-symbol-elimination, cfg-finiteness-problem, cfg-membership-problem, horn-sat-forward-chaining, circuit-value-problem, dfa-emptiness, cfl-intersection-undecidable, pushdown-automaton]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.1.2, Eliminating Useless Symbols (computing the generating symbols), and Section 7.4.3, Testing Emptiness of CFL's (the linear-time version with counts)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 4.1, Decidable Languages (Theorem 4.8, E_CFG is decidable, by marking the variables that generate terminal strings)
  - paper: doi:10.1016/0304-3975(76)90068-2
    title: Neil D. Jones and William T. Laaser, Complete problems for deterministic polynomial time, Theoretical Computer Science 3(1) (1976)
    locator: pp. 105 to 117 (emptiness of a context-free grammar is complete for P under logspace reductions)
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3) (1984)
    locator: pp. 267 to 284 (the counter technique that gives linear time)
---

The CFG emptiness problem asks whether a [context-free grammar](/context-free-grammar/) generates no string at all. It is decidable in time linear in the size of the grammar: mark the nonterminals that derive a terminal string, starting from the productions with only terminals on the right, and answer "empty" when the start symbol stays unmarked. The same marking is the first step of [useless symbol elimination](/useless-symbol-elimination/), and it is the forward chaining of [Horn satisfiability](/horn-sat-forward-chaining/) in other clothes. The problem is complete for polynomial time, so it is unlikely to have a fast parallel algorithm.

## In plain words

A grammar is a set of rules for building strings. A rule may say "an A is an a followed by a B". If no rule ever lets you finish, the grammar describes no string at all: every attempt keeps asking for one more piece.

To find out, work from the bottom. A rule whose right side has only letters gives a finished string, so its left side can be finished. Then a rule whose right side has only letters and pieces that you know how to finish gives a finished string too. Repeat until nothing changes. The grammar describes some string exactly when the start symbol is among the pieces you can finish.

You never need to write a string down, which matters, because the shortest one can be extremely long.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, and $|G|$, written $g$ in the front matter, is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$.

**Input.** A context-free grammar $G$.

**Output.** "Empty" if $L(G) = \emptyset$, and "not empty" otherwise.

A symbol $X \in V \cup \Sigma$ is *generating* (or *productive*) if $X \Rightarrow^* x$ for some $x \in \Sigma^*$. Every terminal is generating. The set $\mathrm{Gen}$ of generating symbols is the least set that contains $\Sigma$ and contains $A$ whenever some production $A \to X_1 \cdots X_k$ has all $X_i \in \mathrm{Gen}$, with $k = 0$ allowed. Then

$$L(G) \ne \emptyset \iff S \in \mathrm{Gen}.$$

*Proof.* If $A$ enters $\mathrm{Gen}$ by $A \to X_1 \cdots X_k$, then by induction on the order of entry each $X_i \Rightarrow^* x_i$, so $A \Rightarrow^* x_1 \cdots x_k$. Conversely, if $A \Rightarrow^* x$, take a [parse tree](/parse-tree/) of $x$ with root $A$ and use induction on its height: the children of the root derive terminal strings by smaller trees, so they are in $\mathrm{Gen}$, and the production at the root puts $A$ in. $\square$

## Variants

- **Search.** Output a string of $L(G)$ when there is one. The marking gives a parse tree for each generating nonterminal, made of the production that marked it. Its yield can have length $2^{\Theta(|G|)}$, so an explicit string is not a polynomial output, but the tree, shared as a DAG, has size $O(|G|)$.
- **The shortest string.** Compute the length $\ell(A)$ of a shortest string derived from each $A$, by a variant of Dijkstra's algorithm on the hypergraph of productions, in $O(|G| \log |V|)$ time, with $\ell(A) = \min$ over $A \to X_1 \cdots X_k$ of $\sum_i \ell(X_i)$ and $\ell(a) = 1$.
- **The generating set.** Output all of $\mathrm{Gen}$. This is the first pass of [useless symbol elimination](/useless-symbol-elimination/) and is needed before many other constructions.
- **Emptiness of a pushdown automaton.** For a [pushdown automaton](/pushdown-automaton/), convert it to a grammar, or decide directly whether some accepting configuration is reachable with [pushdown saturation](/pushdown-saturation/). Both take polynomial time.
- **Emptiness of the intersection with a regular language.** For a grammar $G$ and a finite automaton $A$, the language $L(G) \cap L(A)$ is context-free, with a grammar of nonterminals $[pXq]$ for states $p, q$ of $A$. Its emptiness takes polynomial time. With two grammars, the emptiness of $L(G_1) \cap L(G_2)$ is [undecidable](/cfl-intersection-undecidable/).
- **Universality.** Whether $L(G) = \Sigma^*$ is undecidable, unlike emptiness. Context-free languages are not closed under complement, so the test for emptiness does not carry over.

## Examples

| grammar | generating nonterminals | answer |
|---|---|---|
| $S \to a S b \mid \varepsilon$ | $S$ | not empty, shortest string $\varepsilon$ |
| $S \to a S$ | none | empty |
| $S \to A B$, $A \to a$, $B \to b B$ | $A$ | empty |
| $S \to A B \mid C$, $A \to a A \mid b$, $B \to B a$, $C \to A A$ | $A$, then $C$, then $S$ | not empty, shortest string $bb$ |
| $S \to A_1 A_1$, $A_i \to A_{i+1} A_{i+1}$ for $i < k$, $A_k \to a$ | all | not empty, shortest string $a^{2^k}$ |

In the third row every string from $B$ would need another $B$, so $B$ is not generating, and $S \to A B$ never completes. In the fourth row $B$ is not generating either, but $S$ is generating through $C$. The last grammar has size $3k + 2$ and a single string, of length $2^k$. An algorithm that searches for a string by generating them in order of length takes exponential time on it; the marking takes $O(k)$.

## Known algorithms

- **Iterated marking.** Repeat passes over all productions, and mark the left side of each production whose right side is all marked or terminal, until a pass marks nothing. At most $|V| + 1$ passes, so $O(|V| \cdot |G|)$ time. This is the algorithm of Sipser and of most textbooks.
- **Marking with counters, $O(|G|)$.** Give each production a count of the occurrences of unmarked nonterminals in its right side, and keep for each nonterminal the list of its occurrences in right sides. Put the left side of each production with count 0 on a queue. When a nonterminal is marked, decrease the count of each production where it occurs, and queue the left side when a count drops to 0. Each occurrence is handled once. This is the method of Dowling and Gallier for Horn formulas, and of Section 7.4.3 of Hopcroft, Motwani and Ullman.
- **Through other problems.** The test is also a [fixed-point iteration](/fixed-point-iteration/), or the evaluation of a [Datalog](/datalog/) program with the rules $A \leftarrow X_1, \ldots, X_k$.

## Bounds

**Upper bound.** $O(|G|)$ time on a word RAM, by the counter method. This is optimal up to a constant, because an algorithm that does not read a production can miss the only production that completes $S$.

**P-completeness.** Jones and Laaser proved that the emptiness of a context-free grammar is complete for P under logspace reductions. So it is in NC, the class of problems with fast parallel algorithms, only if P = NC, which is believed false. The [circuit value problem](/circuit-value-problem/) reduces to it: a gate $x = y \wedge z$ becomes $X \to Y Z$, a gate $x = y \vee z$ becomes $X \to Y \mid Z$, a true input becomes $X \to \varepsilon$, and a false input gets no production. Then the output gate is true exactly when its nonterminal is generating. The circuit value problem stays P-complete for monotone circuits, which have no negation gates, so this map is enough.

**Space.** The problem is P-complete, so it is not in [logspace](/logspace/) unless L = P.

## Reductions

- **To and from Horn satisfiability.** A production $A \to X_1 \cdots X_k$ is the Horn clause $A \leftarrow B_1 \wedge \cdots \wedge B_j$, where $B_1, \ldots, B_j$ are the nonterminals among the $X_i$. A nonterminal is generating exactly when its variable is forced true by forward chaining, so $L(G) \ne \emptyset$ exactly when the clauses together with the goal clause $\neg S$ are unsatisfiable. The converse map turns each Horn clause into a production. Both maps take linear time, so the two problems have the same complexity.
- **From the circuit value problem**, in logarithmic space, as above.
- **Emptiness of PDA.** Converting a pushdown automaton with $s$ states into a grammar gives $O(s^2)$ nonterminals, and emptiness of the grammar answers emptiness of the automaton.
- **Finiteness reduces to emptiness and cycles.** The [finiteness problem](/cfg-finiteness-problem/) first removes the useless symbols, which uses the generating set, and then looks for a cycle.

## Applications

- **Grammar cleaning.** Parser generators warn about nonterminals that derive no string, and the [Chomsky normal form conversion](/chomsky-normal-form-conversion/) and [useless symbol elimination](/useless-symbol-elimination/) start with this test.
- **Decision procedures.** Emptiness of a [pushdown automaton](/pushdown-automaton/) or of the intersection of a grammar with a regular language answers questions of program analysis, such as whether a bad state is reachable along a path with matched calls and returns.
- **Testing grammars.** A grammar for an input format that turns out to be empty, or to have a nonterminal that is not generating, is a bug that this test finds at once.
- **Automata on trees.** A grammar is a tree automaton for its parse trees, so the test decides emptiness of tree automata in the same linear time.

## References
