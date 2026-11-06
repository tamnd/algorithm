---
tag: K7ZEFB
kind: algorithm
slug: recursive-ascent-parsing
name: Recursive ascent parsing
area: automata-and-parsing/context-free-parsing
level: advanced
summary: LR parser encoded as mutually recursive procedures, one per LR state.
solves: [context-free-language-recognition]
model: word-ram
complexity:
  vars: {n: the number of input tokens, for a fixed grammar}
  time: {worst: O(n), best: Θ(1)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, online: true}
history:
  year: 1988
  people: [Thomas J. Pennello, George H. Roberts, Frans E. J. Kruseman Aretz]
  note: Pennello compiled LR tables into fast assembly code in 1986; Roberts and Kruseman Aretz described LR parsers as recursive procedures, one per state, in 1988.
prereqs: [slr-parsing, recursive-descent-parsing, lr-parse-table]
see_also: [lr-parsing, lalr-parsing, canonical-lr-parsing, lr0-parsing, viable-prefix, left-corner-parsing, parser-generator, shift-reduce-parsing]
sources:
  - paper: doi:10.1145/12276.13326
    title: Thomas J. Pennello, Very fast LR parsing, Proceedings of the 1986 SIGPLAN Symposium on Compiler Construction (SIGPLAN Notices 21(7))
    locator: pp. 145 to 151 (LALR(1) tables and driver replaced by generated code, one code block per state)
  - paper: doi:10.1145/47907.47909
    title: George H. Roberts, Recursive ascent, an LR analog to recursive descent, ACM SIGPLAN Notices 23(8) (1988)
    locator: pp. 23 to 29 (one subroutine per state, shifts as calls, reductions as returns)
  - paper: "F. E. J. Kruseman Aretz, On a recursive ascent parser, Information Processing Letters 29(4) (1988)"
    title: F. E. J. Kruseman Aretz, On a recursive ascent parser
    locator: pp. 201 to 206 (the reduced nonterminal and a pop count passed back through the returns)
  - paper: doi:10.1016/0304-3975(92)90128-3
    title: René Leermakers, Lex Augusteijn and Frans E. J. Kruseman Aretz, A functional LR parser, Theoretical Computer Science 104(2) (1992)
    locator: the derivation of recursive ascent as a functional program
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 9.10.6, Recursive Ascent, and the annotated bibliography in Chapter 18
---

A recursive ascent parser is an [LR parser](/lr-parsing/) written as code instead of a table and a driver. Each state of the LR automaton becomes a procedure. Shifting a token, or moving to a new state after a reduction, is a call; reducing by a production with $k$ symbols on its right side is a chain of $k$ returns, which carry the nonterminal back to the procedure of the state that was below the right side. The machine call stack plays the role of the LR state stack. The name was chosen by analogy with [recursive descent](/recursive-descent-parsing/), where each nonterminal becomes a procedure. Pennello showed in 1986 that compiling LR tables to code can make parsing several times faster, and Roberts and Kruseman Aretz described the recursive form in 1988. The parser makes exactly the moves of the table-driven parser, so it runs in linear time for a fixed grammar.

## In plain words

A table-driven LR parser keeps a stack of states and looks up what to do in a table. Recursive ascent turns each row of the table into a small procedure. A procedure looks at the next token and does one thing: it reads the token and calls the procedure of the next state, or it decides that the last few symbols form a complete rule.

When a rule is complete, the procedures that read its symbols return one by one, each passing back the name of the rule's left side and a count of how many more must return. When the count runs out, the procedure that is now on top calls the procedure for the state after the left side, as if that symbol had just been read. The chain of active calls is exactly the stack of the table-driven parser, so nothing needs to be stored by hand.

## The problem

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size.

The input is an LR grammar $G$, given through its ACTION and GOTO tables (here the [SLR(1)](/slr-parsing/) tables, built as on that page), and a token string $w = a_1 \cdots a_n$, followed by the end marker $\$$. The output is a parse tree of $w$ and the sequence of reductions, a reverse rightmost derivation, or a syntax error at the first token that the table rejects. This is the problem of the table-driven parser; recursive ascent changes how the parser is written, not what it computes.

## The algorithm

There is one procedure STATE$_q$ for each state $q$ of the LR automaton. Its argument $v$ is the tree of the symbol on the transition into $q$. A call returns either ACCEPT$(t)$ or REDUCE$(A, c, ks)$: a reduction to $A$ is in progress, $c$ more calls must return before the goto, and $ks$ are the children collected so far, leftmost first.

```pseudo id=main
RECURSIVE-ASCENT-PARSE(w)
L1  append $ to w; r ← STATE_0(nothing)
L2  return the tree t of r = ACCEPT(t)

STATE_q(v)                                  ▷ one procedure for each LR state q
L3  a ← the next input token
L4  if ACTION[q, a] = shift j then advance the input; r ← STATE_j(the leaf a)
L5  else if ACTION[q, a] = reduce A → β then
L6      if |β| > 0 then return REDUCE(A, |β| − 1, ⟨v⟩)
L7      r ← REDUCE(A, 0, ⟨⟩)
L8  else if ACTION[q, a] = accept then return ACCEPT(v)
L9  else report a syntax error at a
L10 loop                                    ▷ a reduction to A is passing through q
L11     if r = ACCEPT(t) then return r
L12     let r = REDUCE(A, c, ks);  if c > 0 then return REDUCE(A, c − 1, ⟨v⟩ · ks)
L13     r ← STATE_GOTO[q, A](the node A with children ks)
```

A procedure looks at the input only once, at line L3. After a shift or an empty reduction, every call it makes eventually returns a reduction, and from then on the procedure only passes reductions down (line L12) or makes the goto for one that ends at its level (line L13). The procedure of state $q$ is specialized: a [parser generator](/parser-generator/) writes its line L4 as a branch on the few tokens with an action in row $q$, and its line L13 as a branch on the few nonterminals with a goto from $q$.

An empty production ($|\beta| = 0$) pops nothing, so line L7 makes the goto in the current procedure instead of returning.

## Example

Take $E \to E + T \mid T$, $T \to n$. Its LR(0) automaton has 6 states:

| state | items | procedure |
|---|---|---|
| 0 | $S' \to \cdot E$, $E \to \cdot E + T$, $E \to \cdot T$, $T \to \cdot n$ | on $n$: call STATE$_3$; goto $E$: 1, $T$: 2 |
| 1 | $S' \to E \cdot$, $E \to E \cdot + T$ | on $+$: call STATE$_4$; on $\$$: accept |
| 2 | $E \to T \cdot$ | on $+$, $\$$: return REDUCE$(E, 0, \langle v \rangle)$ |
| 3 | $T \to n \cdot$ | on $+$, $\$$: return REDUCE$(T, 0, \langle v \rangle)$ |
| 4 | $E \to E + \cdot T$, $T \to \cdot n$ | on $n$: call STATE$_3$; goto $T$: 5 |
| 5 | $E \to E + T \cdot$ | on $+$, $\$$: return REDUCE$(E, 2, \langle v \rangle)$ |

On $w = n + n$ the calls are:

1. STATE$_0$ sees $n$ and calls STATE$_3$, which sees $+$ and returns REDUCE$(T, 0, \langle n \rangle)$. State 0 has $c = 0$ and calls STATE$_2$ with $T(n)$.
2. STATE$_2$ sees $+$ and returns REDUCE$(E, 0, \ldots)$. State 0 calls STATE$_1$ with $E(T(n))$.
3. STATE$_1$ sees $+$ and calls STATE$_4$, which sees $n$ and calls STATE$_3$. STATE$_3$ sees $\$$ and returns REDUCE$(T, 0, \langle n \rangle)$; state 4 calls STATE$_5$ with $T(n)$.
4. STATE$_5$ sees $\$$ and returns REDUCE$(E, 2, \langle T \rangle)$. State 4 has $c = 2$ and returns REDUCE$(E, 1, \langle +, T \rangle)$. State 1 has $c = 1$ and returns REDUCE$(E, 0, \langle E, +, T \rangle)$. State 0 has $c = 0$ and calls a new STATE$_1$ with the tree $E(E(T(n)), +, T(n))$.
5. STATE$_1$ sees $\$$ and returns ACCEPT, which passes down through state 0 to the driver.

The procedures are entered in the order 0, 3, 2, 1, 4, 3, 5, 1: one call for each shift and each goto of the table-driven parser, plus the first. The reductions are $T \to n$, $E \to T$, $T \to n$, $E \to E + T$, a rightmost derivation read backwards. The trace and the table were produced by the implementation.

## Correctness

The chain of active calls, from STATE$_0$ to the running call, has the same states as the stack of the table-driven LR parser, and the arguments of the calls are the trees on that stack. A shift adds a call and a stack entry. A reduction by $A \to \beta$ makes the top $|\beta|$ calls return, which is the pop of $|\beta|$ states, and the call that receives $c = 0$ is the state uncovered by the pop, which makes the goto. An accept or an error happens in the same state on the same token. By induction on the number of moves, both parsers go through the same configurations, so recursive ascent accepts exactly $L(G)$, with the same tree and reductions as the table-driven parser. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** Each move of the table-driven parser costs $O(1)$ calls or returns, except a reduction by $A \to \beta$, which costs $|\beta|$ returns and one call, the same as popping $|\beta|$ states. For a fixed grammar, an LR parser makes $O(n)$ moves, so recursive ascent takes $O(n)$ time. The best case is $\Theta(1)$, an error at the first token. In practice it saves the table lookups and the decoding of actions; Pennello reported a speedup by a factor of about 6 for his generated code, at about twice the size of the tables.

**Space.** The call stack holds one frame per LR stack entry, $O(n)$ in the worst case: right recursion or nesting can make the stack as deep as the input is long. The code is $O(|\text{states}| + |\text{table entries}|)$, which is the size of the uncompressed table; the compression used for table-driven parsers is not available.

## Properties

- **Deterministic and online.** It reads the input once, left to right, and needs the grammar to be LR: ACTION must have one action per entry.
- **Recursive.** Its control state is the machine call stack. The implementation on this page runs each procedure as a Python generator and keeps the chain of generators in a list, so deep inputs do not hit the recursion limit.
- **Same language and same trees.** It is a different encoding of the same automaton, so any LR(0), SLR(1), LALR(1) or LR(1) table can be used.
- **The stack is implicit.** The parser cannot read its own stack below the top frame, which matters for error recovery.

## Variants and improvements

- **Global pop count.** Kruseman Aretz kept the nonterminal and the count in global variables, with every procedure decrementing the count and returning while it is positive; this page passes them as return values, which is the same scheme.
- **Return-stack adjustment.** Roberts's version can pop several frames at once by adjusting the return stack, which is fast but not expressible in most high-level languages.
- **Functional LR.** Leermakers, Augusteijn and Kruseman Aretz derived recursive ascent as a functional program over item sets, without an explicit automaton,; Leermakers also gave a recursive ascent version of [Earley parsing](/earley-parser/).
- **Recursive ascent-descent.** Horspool combined it with [recursive descent](/recursive-descent-parsing/): the parser descends in the parts of the grammar that are LL and ascends only where LR power is needed, which reduces the number of states that need procedures.
- **Directly executable code.** Pennello, and later Horspool and Whitney, generated assembly or C code for the states, with jumps instead of calls where possible, as the fastest way to run an LR table.
- **Toward recursive descent.** Roberts showed that for an LL(1) grammar, compiler optimizations of the recursive ascent procedures (inlining, merging states) give back a recursive descent parser.

## When to use it

Use recursive ascent when you generate an LR parser and want its speed, or want readable code that can be stepped through in a debugger, for example in a parser generator that emits code in a language with cheap calls. For a hand-written parser of an LL grammar, recursive descent is simpler. For a large grammar, the generated code is bigger than a compressed table, and a table-driven parser such as [LALR(1)](/lalr-parsing/) in yacc style is the usual choice. For inputs that nest very deeply, an explicit stack, as in the table-driven parser or the generator list of the implementation, avoids running out of call stack.

## Pitfalls

- **Stack overflow.** The call depth equals the LR stack height, which reaches $n$ on right-recursive lists ($S \to x\, S \mid x$) and on deeply nested parentheses. A plain recursive implementation fails on long inputs; the tests run 100000 tokens through the generator-based driver.
- **Empty productions.** A reduction by $A \to \varepsilon$ must not return: there is nothing to pop, and the goto belongs to the current procedure (line L7). Treating it like $|\beta| = 1$ pops one state too many.
- **Off by one in the count.** The reducing procedure is itself one of the $|\beta|$ calls to pop, so it returns $|\beta| - 1$. The tests compare every reduction with the table-driven parser on random grammars.
- **Losing the accept.** The accept is found deep in the call chain and must pass through every pending call; a procedure that treats any returned value as a reduction will make a goto on garbage.
- **The order of the children.** The children come back from the right end of the right side to the left. Prepend them, or append and reverse once at the goto, as the implementation does; prepending to an array at every step costs $O(|\beta|^2)$.
- **Error recovery.** Recovery schemes that pop the stack to a state with a known goto, such as [panic mode](/panic-mode-error-recovery/), need a way to unwind several frames, for example an exception that carries the target state.

## Implementations

## History

Pennello published "Very fast LR parsing" in 1986: the LALR(1) tables and driver of a parser generator were replaced by assembly code with one block per state, with a speedup of about 6. In 1988 Roberts and Kruseman Aretz independently described LR parsers as sets of mutually recursive procedures, one per state, and Roberts gave the name recursive ascent, by analogy with recursive descent; Barnard and Cordy described a related scheme the same year. Roberts later compared the methods (1989) and showed how to optimize recursive ascent into recursive descent for LL(1) grammars (1990). Leermakers, Augusteijn and Kruseman Aretz recast the method as a functional program in 1992, and Leermakers developed this view in his 1993 book on the functional treatment of parsing.

## References
