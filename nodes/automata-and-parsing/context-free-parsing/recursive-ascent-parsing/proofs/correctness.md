---
title: The recursive ascent parser makes exactly the moves of the table-driven LR parser, so it accepts L(G), builds the right tree, and stops
proves: [correctness, termination]
status: full
---

We use the notation of the [context-free grammar](/context-free-grammar/) page and the pseudocode of the page: the driver RECURSIVE-ASCENT-PARSE (lines L1 and L2) and the procedures STATE$_q$ (lines L3 to L13). The grammar $G$ is SLR(1), so its ACTION table has at most one action per entry, and GOTO is the goto table of its LR(0) automaton. The reference is the table-driven parser SLR-PARSE of [SLR parsing](/slr-parsing/), which uses the same two tables.

## Configurations

A configuration of the table-driven parser is a stack of states $q_0 q_1 \cdots q_m$ with $q_0 = 0$, a list of trees $v_1, \ldots, v_m$ (the tree $v_t$ belongs to the symbol on the transition into $q_t$), and an input position $i$. A move is a shift, a reduction followed by a goto, an accept, or an error.

At any moment of the recursive ascent parser, the active procedure calls form a chain: STATE$_{q_0}$ called by the driver, STATE$_{q_1}$ called by it, and so on up to the running call STATE$_{q_m}$. Call $t$ received the argument $v_t$ (for $t = 0$, nothing). Every call except the last is suspended at one of the two call sites, line L4 or line L13, and when it resumes it continues at line L10. We say that the recursive ascent parser is **in configuration** $(q_0 \cdots q_m;\ v_1 \ldots v_m;\ i)$ when this is the chain, the input position is $i$, and the call STATE$_{q_m}$ is about to execute line L3.

## Lemma 1: one move

Suppose the recursive ascent parser is in configuration $C = (q_0 \cdots q_m;\ v_1 \ldots v_m;\ i)$, and let $a$ be the token at position $i$.

1. If ACTION$[q_m, a]$ = shift $j$, then it next reaches the configuration $(q_0 \cdots q_m j;\ v_1 \ldots v_m a;\ i + 1)$.
2. If ACTION$[q_m, a]$ = reduce $A \to \beta$ with $k = |\beta|$, then $k \le m$, and it next reaches the configuration $(q_0 \cdots q_{m-k}\, g;\ v_1 \ldots v_{m-k}\, u;\ i)$ with $g = \mathrm{GOTO}[q_{m-k}, A]$ and $u$ the node $A$ with the children $v_{m-k+1}, \ldots, v_m$.
3. If ACTION$[q_m, a]$ = accept, then every call returns ACCEPT$(v_m)$ and the driver returns $v_m$.
4. If the entry is empty, line L9 reports an error at position $i$.

These are exactly the next configurations of the table-driven parser.

*Proof.* Case 1: line L4 advances the input and calls STATE$_j$ with the leaf $a$; the new call is about to execute line L3. Case 4 is line L9.

Case 2 with $k = 0$: line L7 sets $r$ = REDUCE$(A, 0, \langle\rangle)$, and the loop of line L10 starts in the call $q_m = q_{m-k}$. Line L11 does nothing, and since $c = 0$, line L13 calls STATE$_g$ with the node $A$ over no children, which is $u$.

Case 2 with $k \ge 1$: we show by induction on $s = 1, \ldots, k$ that the call $q_{m-s}$ resumes at line L10 with $r$ = REDUCE$(A, k - s, \langle v_{m-s+1}, \ldots, v_m \rangle)$. For $s = 1$: line L6 of call $q_m$ returns REDUCE$(A, k - 1, \langle v_m \rangle)$, and its caller $q_{m-1}$ was suspended at a call site, so it resumes at line L10 with this value. The call $q_{m-1}$ exists because $m \ge k \ge 1$. For $s < k$: in call $q_{m-s}$, $c = k - s > 0$, so line L12 returns REDUCE$(A, k - s - 1, \langle v_{m-s}, v_{m-s+1}, \ldots, v_m \rangle)$, and call $q_{m-s-1}$ resumes with it. For $s = k$, the call $q_{m-k}$ has $c = 0$ and the children $\langle v_{m-k+1}, \ldots, v_m \rangle$ in order, and line L13 calls STATE$_g$ with $u$. The calls $q_{m-k+1}, \ldots, q_m$ have returned, so the chain is $q_0 \cdots q_{m-k}\, g$, and the new call is about to execute line L3.

Case 3: line L8 returns ACCEPT$(v_m)$. Each suspended call resumes at line L10, and line L11 returns the same value, so the value reaches the driver, and line L2 returns $v_m$. $\square$

The bound $k \le m$ holds because the table-driven parser in the same configuration pops $k$ states above $q_0$: by Lemma 2 of the [SLR proof](/slr-parsing/), its stack symbols form a viable prefix whose last $k$ symbols are $\beta$.

## Theorem

On every input $w$, the recursive ascent parser makes the same sequence of moves as the table-driven SLR(1) parser with the same tables. So it stops, it accepts exactly the sentences of $L(G)$, on acceptance it returns the same parse tree and the same sequence of reductions (a reverse rightmost derivation of $w$), and on rejection it reports the error at the same position.

*Proof.* Initially, line L1 calls STATE$_0$ with nothing, and the input position is 0: the recursive ascent parser is in configuration $(0;\ ;\ 0)$, the initial configuration of the table-driven parser. By Lemma 1 and induction on the number of moves, after each move both parsers are in the same configuration, and both make the same next move. The reductions are recorded at lines L6 and L7, at the same moves as at line L7 of SLR-PARSE.

The table-driven parser accepts exactly $L(G)$, with a correct tree, and stops after $O(n)$ moves for a fixed grammar; these are Theorems 4 and 7 of the [SLR parsing correctness proof](/slr-parsing/). Each move of the recursive ascent parser costs $O(1)$ calls and returns, plus $k$ returns for a reduction by a production with $k$ right-side symbols, the same as the $k$ pops of SLR-PARSE. So it stops after $O(n)$ steps too. $\square$

## Remarks

**Other tables.** The proof uses only that ACTION has at most one action per entry and that reductions find their right side on the stack. So the same procedures work with LR(0), LALR(1) or canonical LR(1) tables.

**The depth of the calls.** The chain of active calls is the LR stack, so its length is at most the largest stack height, which is $O(n)$ for a fixed grammar and can reach $n$ (for right recursion or nested parentheses). The implementation keeps the chain in a list of Python generators instead of on the machine stack, which changes nothing in the argument above: a `yield` is a call, and a `return` is a return.
