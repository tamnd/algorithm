---
tag: WDNKY8
kind: algorithm
slug: thompson-construction
name: Thompson's construction
aliases:
- Thompson NFA construction
- regex to epsilon-NFA
area: automata-and-parsing/regular-expressions
level: core
summary: Builds an epsilon-NFA with O(m) states from a regex of size m by composing fragments.
solves: [regex-to-nfa-conversion]
model: word-ram
complexity:
  vars: {m: the size of the regular expression (nodes of its syntax tree)}
  time: {worst: Θ(m), best: Θ(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1968
  people: [Ken Thompson]
  note: Thompson's regular expression search compiled a pattern, in postfix form, into code that runs all states of its automaton at once.
prereqs: [regular-expression, epsilon-nfa]
see_also: [thompson-nfa-simulation, glushkov-automaton, regex-to-nfa-conversion, kleene-theorem, epsilon-closure, pike-vm, state-elimination, shunting-yard-algorithm]
sources:
  - paper: doi:10.1145/363347.363387
    title: Ken Thompson, Programming techniques, regular expression search algorithm, Communications of the ACM 11(6) (1968)
    locator: pp. 419 to 422 (the postfix form and the compiled code that follows all states in parallel)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 3.7.4, Construction of an NFA from a Regular Expression (the McNaughton-Yamada-Thompson algorithm and its properties)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.3, Regular Expressions (the proof that each regular expression describes a regular language, by NFAs for the six cases)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 3.2.3, Converting Regular Expressions to Automata
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast, 2007
    locator: section Converting Regular Expressions to NFAs (fragments with dangling arrows built from the postfix form)
---

Thompson's construction turns a [regular expression](/regular-expression/) $r$ of size $m$ into an [epsilon-NFA](/epsilon-nfa/) that accepts $L(r)$. It builds one small automaton, a *fragment* with one entry and one exit, for each node of the syntax tree, and glues the fragments together with $\varepsilon$-moves. The result has at most $2m$ states and $4m$ moves, each state has at most two outgoing moves, and the construction takes $\Theta(m)$ time. It is the first half of the linear-time matchers of grep and RE2, which run the automaton with [Thompson's NFA simulation](/thompson-nfa-simulation/).

## In plain words

A pattern is built from small pieces: single letters, "this or that", "this then that", and "this any number of times". The construction makes a tiny machine for each letter: a start point, an end point, and an arrow labelled with the letter. Then it builds bigger machines from smaller ones, following the shape of the pattern. For "this or that" it adds a new start with free arrows to both machines, and a new end that both machines reach by free arrows. For "this then that" it draws a free arrow from the end of the first machine to the start of the second. For "any number of times" it adds free arrows that skip the machine or go around it again.

Each piece of the pattern adds at most two points and four arrows, so the machine grows in proportion to the pattern.

## The problem

The input is a regular expression $r$ over an alphabet $\Sigma$, in the syntax of the [regular expression](/regular-expression/) page: symbols, $\varepsilon$, $\emptyset$, union $|$, concatenation and star $*$. Its size $m$ is the number of nodes of its syntax tree. The output is an $\varepsilon$-NFA $N = (Q, \Sigma, \delta, q_0, \{q_f\})$ with $L(N) = L(r)$. This is the [regex to NFA conversion](/regex-to-nfa-conversion/) problem.

## The algorithm

The algorithm reads $r$ in postfix form, where the operators come after their operands and concatenation is an explicit operator $\cdot$. For example, $(a \mid b)^* abb$ becomes $a\,b \mid {*}\; a \cdot b \cdot b \cdot$. The [shunting-yard algorithm](/shunting-yard-algorithm/) produces this form in $O(m)$ time with one stack. A fragment is a pair $(s, f)$ of an entry state and an exit state.

```pseudo id=main
THOMPSON(r)                                   ▷ r in postfix form, m tokens
L1  S ← an empty stack of fragments; N ← an NFA with no states
L2  for each token t of r, from left to right do
L3      if t is ∅, ε or a symbol a then
L4          s ← new state; f ← new state
L5          if t = a then add the move s --a--> f
L6          if t = ε then add the move s --ε--> f        ▷ for ∅ add no move
L7          push (s, f) on S
L8      else if t = | then
L9          pop (s2, f2); pop (s1, f1); s ← new state; f ← new state
L10         add s --ε--> s1, s --ε--> s2, f1 --ε--> f, f2 --ε--> f; push (s, f)
L11     else if t = · then
L12         pop (s2, f2); pop (s1, f1); add f1 --ε--> s2; push (s1, f2)
L13     else                                          ▷ t = *
L14         pop (s1, f1); s ← new state; f ← new state
L15         add s --ε--> s1, s --ε--> f, f1 --ε--> s1, f1 --ε--> f; push (s, f)
L16 pop (q0, qf); return N with start q0 and the one accepting state qf
```

At each moment, the entry of a fragment on the stack has no incoming move and its exit has no outgoing move. So the moves that lines L10, L12 and L15 add out of an exit $f_1$ or $f_2$ are the first moves of that state, and they cannot create a path that the subexpression does not allow. For a union and a star, the new entry and exit states keep this property for the larger fragment. A concatenation adds no state: its entry is the entry of the left part and its exit is the exit of the right part.

## Example

Take $r = (a \mid b)^* abb$, of size 10. Its postfix form has 10 tokens. The states are numbered in order of creation.

| token | moves added | stack after the token |
|---|---|---|
| $a$ | $0 \xrightarrow{a} 1$ | $(0, 1)$ |
| $b$ | $2 \xrightarrow{b} 3$ | $(0, 1), (2, 3)$ |
| $\mid$ | $4 \to 0$, $4 \to 2$, $1 \to 5$, $3 \to 5$ | $(4, 5)$ |
| $*$ | $6 \to 4$, $6 \to 7$, $5 \to 4$, $5 \to 7$ | $(6, 7)$ |
| $a$ | $8 \xrightarrow{a} 9$ | $(6, 7), (8, 9)$ |
| $\cdot$ | $7 \to 8$ | $(6, 9)$ |
| $b$ | $10 \xrightarrow{b} 11$ | $(6, 9), (10, 11)$ |
| $\cdot$ | $9 \to 10$ | $(6, 11)$ |
| $b$ | $12 \xrightarrow{b} 13$ | $(6, 11), (12, 13)$ |
| $\cdot$ | $11 \to 12$ | $(6, 13)$ |

Unlabelled arrows are $\varepsilon$-moves. The NFA has 14 states, start 6, accepting state 13, 5 symbol moves and 11 $\varepsilon$-moves, within the bounds $2m = 20$ and $4m = 40$. The [$\varepsilon$-closure](/epsilon-closure/) of the start is $\{0, 2, 4, 6, 7, 8\}$. Reading $abb$ gives the sets $\{0, 1, 2, 4, 5, 7, 8, 9, 10\}$, then $\{0, 2, 3, 4, 5, 7, 8, 11, 12\}$, then $\{0, 2, 3, 4, 5, 7, 8, 13\}$, which contains 13, so $abb$ is accepted. The NFA accepts exactly the strings over $\{a, b\}$ that end in $abb$.

## Correctness

Let $V(t)$ be the set of states of the fragment of a subexpression $t$. The proof shows three facts.

1. After the fragment $(s_t, f_t)$ is pushed, no state of $V(t)$ other than $f_t$ ever gains an outgoing move. Later steps add moves only out of new states and out of exits of popped fragments, and an exit that lies in $V(t)$ is $f_t$ itself.
2. So a path from $s_t$ that ends at its first visit to $f_t$ stays in $V(t)$ and uses only the moves that existed when the fragment was pushed.
3. By induction on $t$, such a path reads $w$ if and only if $w \in L(t)$. For a union, the path enters one branch and leaves it at that branch's exit. For a concatenation, it passes through $f_1 \to s_2$ exactly once. For a star, it is the skip move $s \to f$, or it cuts at the visits to $f_1$ into $k \ge 1$ paths of the inner fragment.

Applied to the whole expression, this gives $L(N) = L(r)$. The full proof is below.

## Complexity

- **States.** Lines L4, L9 and L14 add two states for each leaf, union and star, and line L12 adds none. So $|Q| = 2(m - c) \le 2m$, where $c$ is the number of concatenations.
- **Moves.** A leaf adds at most 1 move, a union 4, a concatenation 1 and a star 4, so there are at most $4m$ moves.
- **Degree.** A new entry gets two $\varepsilon$-moves or one symbol move, and an exit gets its outgoing moves at most once, when its fragment is popped: one move for a union or a concatenation, two for a star. After that it is no longer an exit on the stack. So each state has at most two outgoing moves, and a state with a symbol move has no other move.
- **Time and space.** Each token costs $O(1)$ time, and the parse to postfix costs $O(m)$, so the whole construction takes $\Theta(m)$ time and $\Theta(m)$ space on the [word RAM](/word-ram/). The stack holds at most $m$ fragments.

## Properties

- **One start, one accepting state.** The start has no incoming move and the accepting state has no outgoing move. This makes the fragments easy to compose, and it lets other constructions use the NFA as a building block.
- **Linear size.** The size is linear in $m$, with small constants, unlike the DFA of the expression, which can need $2^{\Theta(m)}$ states ([regex DFA state blowup](/regex-dfa-state-blowup/)).
- **Many $\varepsilon$-moves.** About half of the moves read no symbol. The simulation pays for them in the closure step.
- **Structure follows the syntax.** Each subexpression has its own fragment, so a matcher can attach the capture groups of the pattern to the entry and exit of a fragment, as in the [Pike VM](/pike-vm/).
- **No recursion.** The postfix form and one stack replace the recursion over the syntax tree, so the depth of nesting is not limited by the call stack.

## Variants and improvements

- **Merged states.** Aho, Lam, Sethi and Ullman merge the exit of the left fragment with the entry of the right one in a concatenation, which saves one state and one move per concatenation. Their NFA for $(a \mid b)^* abb$ has 11 states.
- **Glushkov automaton.** The [Glushkov automaton](/glushkov-automaton/) has no $\varepsilon$-moves and exactly one state per symbol occurrence plus one, but it can have $\Theta(m^2)$ moves.
- **$\varepsilon$-removal.** Removing the $\varepsilon$-moves of the Thompson NFA by [$\varepsilon$-closure](/epsilon-closure/) gives an NFA with the same states and up to $O(m^2)$ symbol moves.
- **Antimirov and derivatives.** [Antimirov's partial derivatives](/antimirov-derivatives/) give an NFA with at most one state per symbol occurrence plus one, and [Brzozowski derivatives](/brzozowski-derivatives/) give a DFA directly.
- **Extensions.** Bounded repetition $r\{i,j\}$ is expanded into copies of the fragment of $r$, so its cost is $j$ times the size of $r$. Anchors and word boundaries become moves with a test on the input position.

## When to use it

Use Thompson's construction when an expression must become an automaton quickly and the automaton will be simulated, as in a search tool that compiles one pattern per run. Its fragments map one to one to the syntax, which makes it the standard base for submatch extraction. When the automaton will be determinized, the Glushkov automaton is smaller to determinize because it has no $\varepsilon$-moves. When a pattern is used for very many inputs, convert it further to a DFA, eagerly or with a [lazy DFA](/lazy-dfa-construction/).

## Pitfalls

- **A star without new states.** Adding $s_1 \xrightarrow{\varepsilon} f_1$ and $f_1 \xrightarrow{\varepsilon} s_1$ to the inner fragment, instead of two new states, is wrong in context. For $(ab^*)^*$ it makes the inner $b^*$ and the outer star share their loop, and the NFA accepts $b$, which is not in the language. The new states keep the entry free of incoming moves.
- **The empty set and the empty string.** The fragment of $\emptyset$ has no move, so no path leads from its entry to its exit. The fragment of $\varepsilon$ has an $\varepsilon$-move. Mixing the two makes $\emptyset^*$ or $a\emptyset$ wrong.
- **Implicit concatenation.** The parser must insert $\cdot$ between two operands that follow each other: after a symbol, $\varepsilon$, $\emptyset$, $)$ or $*$, and before a symbol, $\varepsilon$, $\emptyset$ or $($. A missing case, such as $)($, joins two fragments wrongly.
- **$\varepsilon$-cycles.** The star creates cycles of $\varepsilon$-moves when the inner expression accepts $\varepsilon$, as in $(a^*)^*$. A simulation must mark visited states in the closure, and a recursive backtracking walk must guard against looping on them.
- **Recursion on the syntax tree.** A recursive builder fails on deeply nested patterns, such as 3000 nested parentheses. The stack form above has no such limit.

## Implementations

## History

Thompson (1968) described a regular expression search for the QED text editor that converted the expression to postfix form and compiled it into IBM 7094 machine code. The code followed all the states of the automaton at once, one input character at a time. The NFA that underlies this code is what textbooks call Thompson's construction. Aho, Lam, Sethi and Ullman name it the McNaughton-Yamada-Thompson algorithm, after McNaughton and Yamada's 1960 construction of automata from expressions. Cox (2007) gave a short modern presentation and showed its advantage over backtracking.

## References
