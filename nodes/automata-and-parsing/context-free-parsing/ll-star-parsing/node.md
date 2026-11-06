---
tag: DGJMDA
kind: algorithm
slug: ll-star-parsing
name: LL(*) parsing
aliases:
- ALL(*)
- ANTLR parsing
- LL(*)
area: automata-and-parsing/context-free-parsing
level: research
summary: Top-down parsing with arbitrary-length lookahead decided by DFA simulation, used in ANTLR.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the number of input tokens, G: fixed}
  time: {worst: 2^(O(n)), worst with graph-structured stacks: O(n^4), best: O(n)}
  space: {extra: 2^(O(n))}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2011
  people: [Terence Parr, Kathleen Fisher, Sam Harwell]
  note: Parr and Fisher (2011) described LL(*), the static lookahead automata of ANTLR 3; Parr, Harwell and Fisher (2014) moved the analysis to parse time as ALL(*), the strategy of ANTLR 4.
prereqs: [ll1-parsing, ll-k-parsing, deterministic-finite-automaton]
see_also: [lookahead-parsing, top-down-parsing, recursive-descent-parsing, backtracking-parsing, packrat-parsing, gll-parsing, glr-parsing, graph-structured-stack]
sources:
  - paper: doi:10.1145/1993498.1993548
    title: Terence Parr and Kathleen Fisher, LL(*), the foundation of the ANTLR parser generator, PLDI 2011
    locator: pp. 425 to 436
  - paper: doi:10.1145/2660193.2660202
    title: Terence Parr, Sam Harwell and Kathleen Fisher, Adaptive LL(*) parsing, the power of dynamic analysis, OOPSLA 2014
    locator: pp. 579 to 598
  - paper: doi:10.1002/spe.4380250705
    title: T. J. Parr and R. W. Quong, ANTLR, a predicated-LL(k) parser generator, Software, Practice and Experience 25(7) (1995)
    locator: pp. 789 to 810
---

LL(*) parsing is top-down parsing in which each choice between the productions of a nonterminal may look as far ahead in the input as it needs, not a fixed number $k$ of tokens. The lookahead is read by a finite automaton for each decision: in LL(*) the automaton is computed from the grammar before parsing, and in its adaptive form ALL(*) it is built during parsing by simulating all alternatives at once, and kept for later decisions. ALL(*), the strategy of the ANTLR 4 parser generator, accepts every [context-free grammar](/context-free-grammar/) without [left recursion](/left-recursion/), resolves [ambiguity](/ambiguity/) in favour of the first alternative, and runs in linear time on the grammars of practical languages.

## In plain words

A top-down parser reads the input from left to right and must decide, each time a rule has several forms, which form the coming input follows. An [LL(1) parser](/ll1-parsing/) looks at one word to decide, and that fails as soon as two forms start alike.

LL(*) looks further, as far as needed. When a rule has several forms, it pretends to follow all of them at once on the coming words, and drops each form the moment a word does not fit it. When only one form is left, that is the choice. If two forms can never be told apart, the grammar is ambiguous there, and the parser takes the one written first.

The pretend runs are remembered as a small automaton for each rule, so the same question on similar input is answered by a table lookup next time.

## The problem

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area.

The input is a grammar $G$ without left recursion, direct or hidden ($A \Rightarrow^+ A \gamma$ for no $A$), and tokens $w = a_1 \cdots a_n$. The productions are numbered, and the number of a production is its *alternative*. Productions that use a nonterminal deriving no terminal string are removed first, since they occur in no parse tree. The output is a [parse tree](/parse-tree/) of $w$ with root $S$ when $w \in L(G)$, and otherwise an error at the first token where $w$ stops being a prefix of a sentence. When $w$ has several parse trees, the parser returns the one in which every choice takes the smallest alternative that still leads to a parse tree, among those it can tell apart (the precise rule is in the algorithm). No condition like LL(k) is needed: every grammar without left recursion is accepted.

## The algorithm

The parser is the [top-down](/top-down-parsing/) stack machine of an [LL(1) parser](/ll1-parsing/), with a prediction procedure in place of the table lookup.

```pseudo id=main
ALL-STAR-PARSE(G, w)                     ▷ w = a1 ⋯ an, G without left recursion
L1  i ← 1; stack ← [S]; the tree is empty
L2  while the stack is not empty
L3      pop X from the stack
L4      if X is a terminal then
L5          if i ≤ n and X = ai then add the leaf ai to the tree; i ← i + 1
L6          else error at ai, or at the end of the input if i = n + 1
L7      else if X has a single production then p ← that production
L8      else p ← ADAPTIVE-PREDICT(X, i, stack)
L9      add a node X to the tree; push the right side of p, last symbol first
L10 if i ≤ n then error at ai
L11 accept and return the tree
```

A *configuration* of a decision for $A$ is a pair $(p, \gamma)$: the alternative $p$ of $A$ and the string $\gamma$ that the rule body of $p$ still has to derive after the lookahead read so far. A set of configurations is a state of a [DFA](/deterministic-finite-automaton/) that is built on demand, as in [lazy DFA construction](/lazy-dfa-construction/): the start state of each nonterminal and each edge are computed the first time they are needed and cached for the rest of the run and for later inputs. This first stage is *SLL prediction*: it ignores what lies on the parser stack below $A$.

```pseudo id=sll
ADAPTIVE-PREDICT(A, i, stack)            ▷ SLL prediction on the cached DFA of A
L12 D ← start(A); on first use, start(A) ← CLOSURE({(p, α) : p is a production A → α})
L13 for t ← i, i + 1, …
L14     if every configuration in D has the same alternative p then return p
L15     if D contains some (p, ε) then return LL-PREDICT(A, i, stack)
L16     if all alternatives in D have the same set of strings γ then return the smallest of them
L17     if t = n + 1 then error at the end of the input
L18     D ← edge(D, at); on first use, edge(D, at) ← CLOSURE({(p, β) : (p, at β) ∈ D})
L19     if D = ∅ then error at at
```

A configuration $(p, \varepsilon)$ means that the lookahead has run past the end of the rule. What may follow depends on the stack, so the decision is repeated with the stack: the second stage is *LL prediction*. Its configurations $(p, \gamma, d)$ stand for the whole stack $\gamma X_{q-d+1} \cdots X_q$, where $X_1 \cdots X_q$ is the parser stack below $A$, top first. The index $d$ points into the parser stack, which is never copied.

```pseudo id=ll
LL-PREDICT(A, i, stack)                  ▷ full-context prediction
L20 C ← CLOSURE({(p, α, q) : p is a production A → α})
L21 for t ← i, i + 1, …
L22     if every configuration in C has the same alternative p then return p
L23     if all alternatives in C have the same set of pairs (γ, d) then return the smallest of them
L24     if t = n + 1 then return the smallest p with (p, ε, 0) ∈ C, or error at the end if there is none
L25     C ← CLOSURE({(p, β, d) : (p, at β, d) ∈ C}); if C = ∅ then error at at
```

Both stages use the same closure, which expands a leading nonterminal in every possible way. Without left recursion it stops.

```pseudo id=closure
CLOSURE(C)                               ▷ d is absent in SLL configurations
L26 repeat while some configuration (p, γ, d) ∈ C has not been processed
L27     if γ = ε and d > 0 then replace it by (p, X(q−d+1), d − 1)        ▷ LL only
L28     if γ = B β with B ∈ V then add (p, δ β, d) for every production B → δ
L29 return the configurations whose γ starts with a terminal, or is ε (with d = 0 in LL)
```

Lines L16 and L23 detect ambiguity: if every alternative has the same set of remaining stacks, then every continuation of the input fits all of them or none, and the choice no longer matters for acceptance. The implementation numbers tokens from 0, so its error positions are one less than the positions $e$ used here.

## Example

Take the grammar

$$0: S \to A \, c \qquad 1: S \to A \, d \qquad 2: A \to a \, A \qquad 3: A \to b$$

whose language is $a^* b \, c \cup a^* b \, d$. The choice at $S$ depends on the last token, after any number of $a$'s, so the grammar is not [LL(k)](/ll-k-parsing/) for any $k$. Its lookahead language, the inputs that select each alternative, is regular, and the DFA built for $S$ has three states with configurations and a loop:

| state | configurations | edges |
|---|---|---|
| $D_0 = \mathrm{start}(S)$ | $(0, a A c)$, $(0, b c)$, $(1, a A d)$, $(1, b d)$ | $a \to D_0$, $b \to D_1$ |
| $D_1$ | $(0, c)$, $(1, d)$ | $c \to \{(0, \varepsilon)\}$, $d \to \{(1, \varepsilon)\}$ |

After $a$ the configuration $(0, a A c)$ becomes $(0, A c)$, whose closure is again $(0, a A c), (0, b c)$, so the edge returns to $D_0$. The parser on $a \, a \, b \, d$:

| step | stack, top first | rest of the input | action |
|---|---|---|---|
| 1 | $S$ | $a a b d$ | predict at $S$: $D_0 \xrightarrow{a} D_0 \xrightarrow{a} D_0 \xrightarrow{b} D_1 \xrightarrow{d} \{(1, \varepsilon)\}$, four tokens, alternative 1 |
| 2 | $A \ d$ | $a a b d$ | predict at $A$: $(2, a A), (3, b) \xrightarrow{a} \{(2, a A), (2, b)\}$, one token, alternative 2 |
| 3 | $a \ A \ d$ | $a a b d$ | match $a$ |
| 4 | $A \ d$ | $a b d$ | predict at $A$ with the cached DFA: alternative 2 |
| 5 | $a \ A \ d$ | $a b d$ | match $a$ |
| 6 | $A \ d$ | $b d$ | predict at $A$: $\xrightarrow{b} \{(3, \varepsilon)\}$, alternative 3 |
| 7 | $b \ d$ | $b d$ | match $b$, match $d$, accept |

There are four decisions, none falls back to LL, and the longest lookahead is four tokens. A later input $a^m b \, d$ is predicted by the cached states and edges without computing any closure, and $a^m b \, c$ adds only the edge from $D_1$ on $c$. On $a \, a \, b$ the prediction at $S$ reaches $D_1$ at the end of the input and reports the error there; on $a \, a \, b \, a$ the edge from $D_1$ on the last $a$ leads to the empty set, and the error is reported at that token.

The fallback to LL is needed in the grammar

$$0: S \to x \, A \, a \qquad 1: S \to y \, A \, b \qquad 2: A \to a \qquad 3: A \to \varepsilon$$

At $A$ the SLL start state is $\{(2, a), (3, \varepsilon)\}$, and $(3, \varepsilon)$ sends the decision to LL-PREDICT. After $x$, the stack below $A$ is $a$, and the LL configurations are $(2, a, 1)$ and $(3, a, 0)$. On $x \, a \, a$ they become $(2, a, 0), (3, \varepsilon, 0)$ after one $a$, and only $(2, \varepsilon, 0)$ after the second, so $A \to a$ is chosen; on $x \, a$ the end of the input comes after one $a$, and line L24 chooses $A \to \varepsilon$, the only alternative with an empty stack. Without the stack, after $y$ the same decision would have to consider $a$ as a follower of $A$ too.

## Correctness

The configurations of SLL prediction are exactly the strings that the alternatives can reach by the moves of the nondeterministic top-down parser while reading the lookahead, and those of LL prediction the same for the whole stack. So an alternative that leads to a parse tree of the input is never dropped. When only one alternative is left, it is the right one; when all alternatives have the same configurations, any of them leads to a parse tree if one does. With the stack invariant of the top-down parser, this shows that the parser accepts exactly $L(G)$ and returns parse trees. Termination needs the absence of left recursion: then every closure is finite, by König's lemma, since an infinite chain of leading expansions would repeat a nonterminal. For errors, the parser on any sentence that agrees with the input up to the reported token would make the same moves, since no step looks beyond that token, so no such sentence exists. The [full proof](proofs/correctness.md) gives the details.

## Complexity

- **Practical grammars.** Each decision reads as many tokens as it needs, and in the grammars of programming languages that is a few tokens almost everywhere. With the DFA cache warm, a prediction costs one dictionary lookup for each token of lookahead, and the parse runs in $O(n)$ time. Parr, Harwell and Fisher report linear behaviour on grammars for several programming languages, among them Java, and speeds orders of magnitude above those of [GLR](/glr-parsing/) and [GLL](/gll-parsing/) parsers.
- **Worst case, as on this page.** A decision can look ahead to the end of the input. With explicit sets of stacks, a configuration set can also grow exponentially: for $S \to a S X \mid a S Y \mid b$, $X \to c$, $Y \to c$, after reading $a^m$ each alternative at the top $S$ has $3 \cdot 2^{m-1}$ configurations, one for each choice of $X$ or $Y$ at the levels already read, and the two sets stay different until the last tokens. So the time and space of the pseudocode are $2^{O(n)}$ in the worst case.
- **Worst case with shared stacks.** ALL(*) as published keeps the stacks of the configurations in a [graph-structured stack](/graph-structured-stack/), as in GLR parsing. Then a configuration set has polynomial size, and Parr, Harwell and Fisher prove that the parse takes $O(n^4)$ time in the worst case.

## Properties

- **No backtracking.** The parser makes each decision once, and every token is matched once. The work spent on lookahead is not undone, since it is stored in the DFA.
- **Any grammar without left recursion.** No grammar class must be checked first, and no conflict is reported. In place of conflicts there are ambiguities, resolved by the order of the alternatives.
- **Valid prefix property.** An error at $a_e$ means that $a_1 \cdots a_{e-1}$ starts a sentence and $a_1 \cdots a_e$ does not.
- **Left parse.** The expansions form a leftmost derivation, so the tree can be built, and actions run, top down. Semantic actions must not run during the simulated lookahead.
- **Not online.** A decision may read the input to its end before the first token is matched.
- **SLL suffices for most decisions.** The cached DFA describes only SLL prediction, which does not depend on the stack. LL prediction is not cached, since its result depends on the stack below the decision.

## Variants and improvements

- **LL(*) with static analysis.** In ANTLR 3, Parr and Fisher computed the lookahead DFA of each decision from the grammar before parsing. The analysis builds the DFA from an approximation of the lookahead language and can fail, since the exact one need not be regular; where it fails, or where the grammar asks for it, the parser falls back to backtracking guided by *syntactic predicates*, with [memoization](/memoization/) of the attempts, as in [packrat parsing](/packrat-parsing/).
- **ALL(*).** Parr, Harwell and Fisher moved the analysis to parse time, which removes the failure of static analysis, since a decision only has to handle the input at hand. Their SLL stage does not stop when the lookahead leaves the rule, as line L15 does: it continues into every place where the rule can be used, and falls back to LL only on a conflict, which keeps more decisions in the cache.
- **Two-stage parsing.** ANTLR 4 can parse a whole input in pure SLL mode, which is faster and correct for most inputs, and parse it again in full LL mode only when the first pass reports an error.
- **Predicates.** Semantic predicates, conditions on the parser state written in the grammar, remove alternatives during prediction. They let one grammar parse inputs whose structure depends on declarations, as in C, where a name can be a type.
- **Left recursion.** ANTLR 4 accepts rules with direct left recursion, such as $E \to E + E \mid E * E \mid x$, by rewriting them into loops with precedence before parsing, in the spirit of [left recursion elimination](/left-recursion-elimination/). Hidden and indirect left recursion are still rejected.
- **Predecessors.** The predicated LL(k) parsers of PCCTS and of the early versions of ANTLR (Parr and Quong, 1995) used fixed $k$ with syntactic and semantic predicates; [lookahead parsing](/lookahead-parsing/) describes the fixed-$k$ methods in general.

## When to use it

Use ALL(*), through ANTLR 4, when you want to write a grammar in the form that is natural for the language, without [left factoring](/left-factoring/) or checking a grammar class, and get a readable [recursive descent](/recursive-descent-parsing/)-style parser with good error messages. It fits programming languages, data formats and domain languages. For grammars with much ambiguity, or when every parse tree is wanted, a general parser such as [GLR](/glr-parsing/), [GLL](/gll-parsing/) or [Earley](/earley-parser/) is the better choice; for hard guarantees on time, an [LL(1)](/ll1-parsing/) or LR grammar gives linear time on every input.

## Pitfalls

- **Left recursion.** The closure never stops on a left-recursive grammar, so the grammar must be checked first, including hidden left recursion through nullable prefixes such as $S \to A \, S \, b$ with $A \to \varepsilon$.
- **Silent ambiguity.** Ambiguous grammars are accepted, and the first alternative wins without any report. A grammar whose intended trees depend on a different choice parses, but gives the wrong tree.
- **Cost on unusual input.** The linear behaviour holds for typical grammars and inputs. Decisions that read to the end of the input, or alternatives that stay alive for long, make the parse slower than linear, and with explicit stacks exponential.
- **The end of the rule.** Stopping SLL prediction when a configuration leaves the rule without the stack, and choosing anyway, is wrong: the follower of the rule depends on the place where it was used, as the second example shows.
- **Side effects during prediction.** The simulated lookahead must not run actions of the grammar, since the alternatives it explores are not the parse.

## Implementations

## History

Parr and Quong (1995) described ANTLR, a parser generator for predicated LL(k) grammars that grew out of PCCTS. Parr and Fisher (2011) presented LL(*), in which each decision has a lookahead DFA built by grammar analysis, with backtracking as a fallback; it was the parsing strategy of ANTLR 3. Parr, Harwell and Fisher (2014) introduced adaptive LL(*), which builds the lookahead automata during parsing, handles every grammar without left recursion, and takes $O(n^4)$ time in the worst case; it is the strategy of ANTLR 4, and the paper received the SIGPLAN Most Influential OOPSLA Paper Award in 2024.

## References
