---
title: Correctness of the parsing table operations and of the LR driver
proves: [correctness]
status: full
---

We prove two claims about the operations of the [parsing table](/parsing-table/) page: the cells and the conflict record are exact, and the LR driver is sound for every deterministic table whose shift and goto entries come from the LR(0) automaton and whose reductions sit at completed items.

**Notation.** The grammar is $G = (V, \Sigma, P, S)$, augmented with $S' \to S$ as production 0, where $S'$ occurs on no right side. Each state $q$ of the LR(0) automaton is a set of items, $q_0$ is the closure of $[S' \to \cdot S]$, and $\delta(q, X)$ is its goto function. The input is $w = a_1 \cdots a_n$ followed by $\$$.

## Part 1: the cells and the conflict record

**Claim.** After any sequence of ADD calls on an initially empty table, for every cell $(r, c)$:

1. $T[r, c]$ is the list of distinct actions passed to ADD for $(r, c)$, in the order of their first addition;
2. $(r, c)$ is in the conflict set exactly when that list has two or more elements.

*Proof.* By induction on the number of calls. Both hold for the empty table: every cell is the empty list and the conflict set is empty. Consider a call $\mathrm{ADD}(r, c, x)$; cells other than $(r, c)$ and their membership in the conflict set do not change. If $T[r, c]$ is empty, line L1 makes it $(x)$, which is the list of distinct actions added to it, and the list has one element, so the cell is correctly not in the conflict set. If $T[r, c]$ is not empty and already holds $x$, nothing changes, and the list of distinct actions is also unchanged. Otherwise line L2 appends $x$, which is a new distinct action added after all the others, so the order of first addition is kept; the list now has at least two elements and L2 puts $(r, c)$ into the conflict set. In each case both statements hold after the call.

**RESOLVE.** Lines L4 and L5 visit exactly the cells of the conflict set, and give each one at most one action; line L6 empties the set. By part 2 of the claim, the cells outside the set had at most one action before the call and are not touched. So after RESOLVE every cell has at most one action and the conflict set is empty, which agrees with part 2. A deterministic table is one whose conflict set is empty, and only on such a table does LOOKUP in L8 return at most one action.

## Part 2: soundness of the LR driver

Let $T$ be a deterministic table in which

- (a) every entry shift $q'$ in $(q, a)$ and goto $q'$ in $(q, A)$ has $q' = \delta(q, a)$ or $q' = \delta(q, A)$;
- (b) every entry reduce $A \to \beta$ in row $q$ has the completed item $[A \to \beta \cdot]$ in $q$, with $A \ne S'$;
- (c) accept appears only in the column of $\$$ and only in rows that contain $[S' \to S \cdot]$.

The SLR(1), LALR(1) and canonical LR(1) constructions all satisfy (a) to (c) after mapping LR(1) states to their cores, whatever lookaheads they attach and whichever action RESOLVE keeps, because resolution only removes actions.

**Claim.** If the driver of lines L7 to L11 accepts $w$, then $S \Rightarrow^* w$.

*Invariant.* Before each iteration of L8, the stack is $q_0 q_1 \cdots q_m$, there are symbols $X_1, \ldots, X_m$ with $q_i = \delta(q_{i-1}, X_i)$ for $1 \le i \le m$, and $X_1 \cdots X_m \Rightarrow^* a_1 \cdots a_j$, where $a_1 \cdots a_j$ is the input consumed so far.

*Initialization.* Line L7 sets the stack to $q_0$ with $m = 0$ and $j = 0$; the empty string derives the empty string.

*Shift (L9).* The entry is shift $q'$ in $(q_m, a_{j+1})$, so by (a) $q' = \delta(q_m, a_{j+1})$. Set $X_{m+1} = a_{j+1}$; then $X_1 \cdots X_{m+1} \Rightarrow^* a_1 \cdots a_{j+1}$ by appending one terminal to the derivation.

*Reduce (L10).* The entry is reduce $A \to \beta$ with $|\beta| = \ell$. By (b), $[A \to \beta \cdot] \in q_m$. Every item of a state other than $q_0$ has been reached by goto, and goto moves the dot over the symbol it reads; items of the form $[B \to \cdot \eta]$ come from closure and have nothing before the dot. So if $\ell > 0$ then the item $[A \to \beta \cdot]$ in $q_m$ arose from items $[A \to \beta_1 \cdots \beta_{i} \cdot \beta_{i+1} \cdots \beta_\ell]$ in $q_{m-\ell+i}$ for $i = 0, \ldots, \ell$, and in particular $X_{m-\ell+1} \cdots X_m = \beta$ and $m \ge \ell$. Hence popping $\ell$ states leaves $q_0 \cdots q_{m-\ell}$, and the symbols $X_1 \cdots X_{m-\ell}\,A$ derive $X_1 \cdots X_{m-\ell}\,\beta = X_1 \cdots X_m \Rightarrow^* a_1 \cdots a_j$. The driver then pushes the goto entry of $(q_{m-\ell}, A)$, which by (a) is $\delta(q_{m-\ell}, A)$, so the invariant holds with $X_{m-\ell+1} = A$. If the cell has no goto entry the driver rejects, which does not affect soundness.

*Accept (L11).* Accept is read in the column of $\$$, so by (c) all of $w$ has been consumed, $j = n$, and $q_m$ contains $[S' \to S \cdot]$. First, no goto leads to $q_0$: an item in $\delta(q, X)$ either has its dot after at least one symbol or was added by closure, and closure adds only items $[B \to \cdot \eta]$ with $B \ne S'$, because $S'$ occurs on no right side; so the item $[S' \to \cdot S]$ of $q_0$ lies in no goto target. Hence $q_0$ is the only state that contains $[S' \to \cdot S]$, and the stack holds $q_0$ only at the bottom. Now $[S' \to S \cdot]$ has its dot after a symbol, so $m \ge 1$, and by the argument of the reduce case it came from $[S' \to \cdot S] \in q_{m-1}$ with $X_m = S$. Then $q_{m-1} = q_0$, which sits only at the bottom, so $m = 1$ and $X_1 = S$. The invariant gives $S \Rightarrow^* a_1 \cdots a_n = w$.

So every accepted string is in $L(G)$.

**What is not claimed.** The converse, that the driver accepts every $w \in L(G)$ and in $O(n)$ steps, needs the lookaheads to be correct and fails for some resolution policies: resolving the conflict of the dangling else in favour of the reduction, for instance, makes some sentences unparsable. For conflict-free SLR(1), LALR(1) and canonical LR(1) tables the converse is proved on the pages of those methods; the tests of this page check it on several hundred random grammars against a brute-force enumeration of $L(G)$ up to length 4, and check soundness for tables resolved by random choices. ∎
