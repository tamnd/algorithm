---
tag: G7X6J2
kind: problem
slug: dfa-to-regex-conversion
name: DFA to regex conversion
aliases:
- automaton to regex conversion
area: automata-and-parsing/regular-expressions
level: core
summary: Compute a regular expression denoting the language of a given finite automaton.
prereqs: [deterministic-finite-automaton, regular-expression, kleene-theorem]
see_also: [state-elimination, arden-lemma, regex-to-nfa-conversion, floyd-warshall, regex-minimization, state-complexity, star-height-problem, nondeterministic-finite-automaton]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 3.2.1, From DFA's to Regular Expressions (the expressions R_ij^(k)), Section 3.2.2, Converting DFA's to Regular Expressions by Eliminating States, and Section 4.3.1, Converting Among Representations (the length of order 4^n)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.3, Lemma 1.60 (generalized nondeterministic finite automata and the removal of one state at a time)
  - paper: "Robert McNaughton and Hisao Yamada, Regular expressions and state graphs for automata, IRE Transactions on Electronic Computers EC-9(1) (1960)"
    title: Robert McNaughton and Hisao Yamada, Regular expressions and state graphs for automata
    locator: pp. 39 to 47
  - paper: "Janusz A. Brzozowski and Edward J. McCluskey, Signal flow graph techniques for sequential circuit state diagrams, IEEE Transactions on Electronic Computers EC-12(2) (1963)"
    title: Janusz A. Brzozowski and Edward J. McCluskey, Signal flow graph techniques for sequential circuit state diagrams
    locator: pp. 67 to 76 (the removal of states from a graph with expressions on its edges)
  - paper: "Andrzej Ehrenfeucht and Paul Zeiger, Complexity measures for regular expressions, Journal of Computer and System Sciences 12(2) (1976)"
    title: Andrzej Ehrenfeucht and Paul Zeiger, Complexity measures for regular expressions
    locator: pp. 134 to 146 (automata with n states whose regular expressions need length 2^(n-1), over an alphabet that grows with n)
  - paper: doi:10.1007/978-3-540-70583-3_4
    title: Hermann Gruber and Markus Holzer, Finite automata, digraph connectivity, and regular expression size, ICALP 2008, Lecture Notes in Computer Science 5126
    locator: pp. 39 to 50 (a lower bound of 2^Ω(n) for the conversion of DFAs over a binary alphabet, by star height and cycle rank)
---

DFA to regex conversion is the problem of turning a finite automaton into a [regular expression](/regular-expression/) for the same language. It is the harder direction of [Kleene's theorem](/kleene-theorem/), and the standard methods are [state elimination](/state-elimination/), the dynamic program of McNaughton and Yamada over the expressions $R^{(k)}_{ij}$, and the solution of language equations by [Arden's lemma](/arden-lemma/). All of them can produce expressions of size exponential in the number of states, and this is unavoidable: some DFAs with $n$ states over two letters need expressions of size $2^{\Omega(n)}$.

## In plain words

A finite automaton is a map of states with arrows labelled by letters. A regular expression is one formula. The problem asks for a formula that describes exactly the words the map accepts.

The usual method removes the states one at a time. When a state goes away, each way of passing through it, from an arrow coming in, around its loops any number of times, and out on an arrow going out, becomes one new arrow with a formula on it. When only the start and the end are left, the formula on the last arrow is the answer.

Each removal can copy the formulas on nearby arrows, so the answer can grow very fast. The order in which you remove the states changes the size of the answer a lot, and for some automata every formula is long.

## Definition

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. The size $|r|$ of an expression is the number of nodes of its syntax tree.

**Input.** A [deterministic finite automaton](/deterministic-finite-automaton/) $A = (Q, \Sigma, \delta, q_0, F)$ with $n = |Q|$ states.

**Output.** A regular expression $r$ over $\Sigma$ with $L(r) = L(A)$.

The problem always has a solution, by Kleene's theorem. It is a construction problem, not a decision problem, and its cost is measured in the size of $r$ and the time to build it, as functions of $n$ and $|\Sigma|$.

## Variants

- **From an NFA.** The same methods work for a [nondeterministic finite automaton](/nondeterministic-finite-automaton/), with $\varepsilon$-moves or not, since none of them uses determinism. An NFA can be exponentially smaller than any DFA for the same language, so starting from the NFA can give a much shorter expression.
- **Shortest expression.** Find an expression of minimum size for $L(A)$. This is a form of [regex minimization](/regex-minimization/), and no efficient algorithm is known.
- **Shared output.** Allow the output to share common subexpressions, as a directed acyclic graph instead of a tree. Then state elimination produces an output of polynomial size, $O(n^3)$ nodes.
- **Restricted output.** Ask for an expression of a special form, for example of minimum [star height](/star-height-problem/) or a [one-unambiguous expression](/one-unambiguous-regular-expression/). Such forms do not exist for every language, or they are much harder to compute.

## Examples

**Even number of $a$.** The DFA over $\{a, b\}$ has states 0 (start, accepting) and 1, with $\delta(0, b) = 0$, $\delta(0, a) = 1$, $\delta(1, b) = 1$ and $\delta(1, a) = 0$. Remove state 1: the only way through it is $a$ in, any number of $b$ loops, and $a$ out, so the loop on state 0 becomes $b \mid ab^*a$. The answer is

$$(b \mid ab^*a)^*,$$

which has 9 nodes. If state 0 is removed first, the answer is $b^* \mid b^* a (b \mid ab^*a)^* a b^*$, with 22 nodes. Both expressions agree with the DFA on all strings of length at most 8.

**Binary multiples of 3.** The DFA reads a binary number from the most significant bit, and its state is the value modulo 3: states 0 (start, accepting), 1 and 2, with $\delta(q, c) = (2q + c) \bmod 3$. Remove state 2 first: it has the loop $1$ and is entered and left by $0$ from and to state 1, so the loop on state 1 becomes $01^*0$. Remove state 1: the loop on state 0 becomes $0 \mid 1(01^*0)^*1$. The answer is

$$(0 \mid 1(01^*0)^*1)^*,$$

with 14 nodes; it accepts the empty string, which the DFA reads as the number 0. The other five orders of the three states give expressions with 21, 27, 27, 50 and 65 nodes, for example $0^* \mid 0^*1(10^*1)^*0(1 \mid 0(10^*1)^*0)^*0(10^*1)^*10^*$ when the states are removed in the order 0, 1, 2.

**The table of McNaughton and Yamada.** Number the states $1, \ldots, n$ and let $R^{(k)}_{ij}$ describe the strings that lead from state $i$ to state $j$ with all intermediate states in $\{1, \ldots, k\}$. Then $R^{(0)}_{ij}$ is the union of the letters $a$ with $\delta(i, a) = j$, plus $\varepsilon$ if $i = j$, and

$$R^{(k)}_{ij} = R^{(k-1)}_{ij} \mid R^{(k-1)}_{ik} \big(R^{(k-1)}_{kk}\big)^* R^{(k-1)}_{kj}.$$

The answer is the union of $R^{(n)}_{1f}$ over the accepting states $f$, where state 1 is the start. This is the same recursion as the [Floyd-Warshall algorithm](/floyd-warshall/), with union for the minimum, concatenation for the sum, and the star for the cost of going around a cycle.

## Known algorithms

- **State elimination** (Brzozowski and McCluskey, 1963). Add a new start state and a new accepting state, linked by $\varepsilon$-arrows, and let each arrow carry a regular expression. Remove the other states one at a time: for each pair of arrows $p \xrightarrow{x} k$ and $k \xrightarrow{z} q$, with $y$ the loop on $k$, add $x y^* z$ to the arrow from $p$ to $q$. Sipser presents this with generalized NFAs. See [state elimination](/state-elimination/).
- **The $R^{(k)}_{ij}$ table** (McNaughton and Yamada, 1960). Compute the $n^2$ expressions for $k = 0, 1, \ldots, n$ by the recursion above. It is state elimination in a fixed order, but it keeps the expressions for all pairs.
- **Language equations.** Give each state $q$ an unknown $X_q$, the set of strings that lead from $q$ to acceptance. Then $X_q = \bigcup_{a} a X_{\delta(q, a)} \cup E_q$, with $E_q = \{\varepsilon\}$ if $q \in F$ and $\emptyset$ otherwise. Solve the system by substitution, using [Arden's lemma](/arden-lemma/): $X = LX \cup M$ has the solution $X = L^*M$ when $\varepsilon \notin L$. This is Gaussian elimination over languages, and the answer is $X_{q_0}$.
- **Order heuristics.** The size of the output depends on the order of removal. A common rule removes first the state with the least product of in-arrows and out-arrows, or the least total size of the expressions that the removal creates; the examples above show factors of 2 to 5 between orders on three states.

## Bounds

- **Upper bound.** In the table, $|R^{(k)}_{ij}| \le 4 |R^{(k-1)}_{ij}| + 4$ in the worst case, since the formula uses four expressions of level $k - 1$ and four new nodes. With $|R^{(0)}_{ij}| = O(|\Sigma|)$ this gives $|R^{(n)}_{ij}| = O(4^n |\Sigma|)$, so the output has size $O(n \cdot 4^n |\Sigma|)$ and is built in time linear in its size (HMU, Section 4.3.1).
- **Lower bound, large alphabets.** Ehrenfeucht and Zeiger (1976) give automata with $n$ states, over an alphabet whose size grows with $n$, for which every equivalent regular expression has length at least $2^{n-1}$.
- **Lower bound, two letters.** Gruber and Holzer (2008) show that for each $n$ there is a DFA with $n$ states over a binary alphabet whose shortest regular expression has size $2^{\Omega(n)}$. Their method relates the size of an expression to the [star height](/star-height-problem/) of the language and the cycle rank of the automaton's graph.
- **Shared output.** With shared subexpressions, state elimination creates $O(n^2)$ new nodes for each removed state, so the output has $O(n^3 + n^2 |\Sigma|)$ nodes; the exponential size above comes only from writing it out as a tree.

## Reductions

- **Kleene's theorem.** Together with the [conversion from regular expressions to NFAs](/regex-to-nfa-conversion/), this problem shows that regular expressions and finite automata describe the same languages.
- **Algebraic path problems.** The $R^{(k)}_{ij}$ table is the Floyd-Warshall recursion in the algebra of languages, and the same algorithm computes shortest paths, [transitive closure](/transitive-closure/) and other path problems in a closed semiring. Regular languages with union, concatenation and star are the standard example of such an algebra, the free [Kleene algebra](/kleene-algebra/).
- **Linear systems.** The equation method is [Gaussian elimination](/gaussian-elimination/) in which division by $1 - L$ is replaced by the star, $L^*$.
- **Operations on expressions.** Regular expressions have no intersection or complement. To find an expression for $L(r) \cap L(s)$ or for the complement of $L(r)$, build automata, combine them, and convert back. The lower bounds above show that the last step can cost an exponential factor.

## Applications

- **Proofs.** It is the step "every regular language has a regular expression" of Kleene's theorem.
- **Tools.** Programs that build automata, for example from a product of two automata or a complement, convert the result back to an expression for display, for search tools such as [grep](/grep/), or for teaching tools.
- **Verification and synthesis.** Path expressions of programs and the regular expressions that describe the paths of a graph are computed by the same elimination, for example in data-flow analysis.
- **Size of descriptions.** The bounds above are a main result of descriptional complexity, which compares the sizes of automata and expressions for the same language; see [state complexity](/state-complexity/).

## References
