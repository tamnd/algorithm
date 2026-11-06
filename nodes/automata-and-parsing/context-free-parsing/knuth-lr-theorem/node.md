---
tag: HGF411
kind: theorem
slug: knuth-lr-theorem
name: Knuth's theorem on LR languages
area: automata-and-parsing/context-free-parsing
level: advanced
summary: A language has an LR(k) grammar exactly when it is a deterministic context-free language.
prereqs: [lr-grammar, deterministic-context-free-language, canonical-lr-parsing]
see_also: [pushdown-automaton, cfg-pda-equivalence, lr-parsing, lr0-parsing, viable-prefix, lr-item, inherent-ambiguity, useless-symbol-elimination]
sources:
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (LR(k) grammars, their parsers as deterministic pushdown machines, and the result that every deterministic language has an LR(1) grammar)
  - paper: doi:10.1016/S0019-9958(66)80019-0
    title: Seymour Ginsburg and Sheila Greibach, Deterministic context free languages, Information and Control 9(6) (1966)
    locator: pp. 620 to 648
  - paper: doi:10.1016/S0022-0000(73)80008-X
    title: Michael A. Harrison and Ivan M. Havel, Strict deterministic grammars, Journal of Computer and System Sciences 7(3) (1973)
    locator: pp. 237 to 277
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, Addison-Wesley, 1979
    locator: Chapter 10, Deterministic Context-Free Languages
---

Knuth's theorem says that the languages of [LR(k) grammars](/lr-grammar/) are exactly the [deterministic context-free languages](/deterministic-context-free-language/), the languages that a deterministic [pushdown automaton](/pushdown-automaton/) accepts. One token of lookahead is always enough: every such language has an LR(1) grammar, so the strict hierarchy of LR(k) grammars collapses for languages. Knuth proved the result in 1965, in the paper that introduced LR parsing.

## Statement

**Notation.** Grammars are written as on the other pages of this area: productions $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the input length and $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$. The augmented grammar adds $S' \to S$, and LR(k) is defined with it, as on the [LR(k) grammar](/lr-grammar/) page; there $\mathrm{FIRST}_k(w)$ pads $w$ with the marker $\$$. A pushdown automaton is $M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$ with configurations $(q, w, \gamma)$, the top of the stack on the left, as on the [pushdown automaton](/pushdown-automaton/) page. It is *deterministic* (a DPDA) if each configuration has at most one move; we then write $\delta(p, a, X) = (r, \alpha)$ for the move from state $p$ with $X$ on top that reads $a \in \Sigma \cup \{\varepsilon\}$, enters $r$ and replaces $X$ by $\alpha$. $L(M)$ is acceptance by final state and $N(M)$ acceptance by empty stack. A language is a *deterministic context-free language* (DCFL) if it is $L(M)$ for a DPDA $M$. For an end marker $\dashv \notin \Sigma$ write $L{\dashv} = \{ w{\dashv} : w \in L \}$.

**Theorem (Knuth 1965).** For every language $L \subseteq \Sigma^*$ the following are equivalent.

1. $L = L(G)$ for an LR(k) grammar $G$, for some $k \ge 0$.
2. $L = L(G)$ for an LR(1) grammar $G$.
3. $L$ is a deterministic context-free language.
4. $L{\dashv} = L(G)$ for an LR(0) grammar $G$.

The proof is constructive in both directions: an LR(k) grammar gives a DPDA, and a DPDA gives an LR(0) grammar for $L{\dashv}$ and an LR(1) grammar for $L$.

## In plain words

An LR parser reads the input once, from left to right. It keeps a stack, and it looks at a few tokens ahead before each decision. A deterministic pushdown automaton can do the same if it keeps the tokens it has seen ahead in its finite memory. So every language with an LR grammar is deterministic.

The theorem also goes the other way. From any deterministic pushdown automaton we can build an LR grammar for its language, and the grammar needs only one token of lookahead. For languages, the lookahead is only needed to see where the input ends: if every input carries an end marker, a grammar with no lookahead at all is enough.

## Proof

The proof shows $2 \Rightarrow 1 \Rightarrow 3 \Rightarrow 4 \Rightarrow 3 \Rightarrow 2$. The implication $2 \Rightarrow 1$ is clear. We use one fact about LR(k) grammars and six lemmas.

**Fact K (Knuth).** Let $G$ have no useless symbols. Then $G$ is LR(k) if and only if no state of its canonical LR(k) automaton has a conflict. This is the equivalent form on the [LR(k) grammar](/lr-grammar/) page. The states are the sets of [LR(k) items](/lr-item/) $\mathrm{st}(\gamma)$ for the [viable prefixes](/viable-prefix/) $\gamma$, built by closure and goto from $[S' \to \cdot S]$. For $k = 0$ the items carry no lookahead, and a state has a conflict if it has two complete items, or a complete item and an item with a terminal after the dot. We also use Theorems 1 and 2 of the [canonical LR parsing](/canonical-lr-parsing/) page: if no state has a conflict, the parser accepts exactly the words of $L(G)$. Those proofs are written for $k = 1$ and hold word for word with lookahead strings of length $k$. Deleting the [useless symbols](/useless-symbol-elimination/) of a grammar keeps its language and keeps the LR(k) property, because it only removes rightmost derivations.

### The automaton side

**Lemma 1 (no endless $\varepsilon$-runs).** Every DPDA $M$ has a DPDA $M_1$ with $L(M_1) = L(M)$ that has no infinite sequence of $\varepsilon$-moves. If every move of $M$ pushes at most two symbols, so does every move of $M_1$.

*Proof.* A move sees only the state and the top symbol. So for a state $p$ and a symbol $X$, the run of $\varepsilon$-moves from $(p, \varepsilon, X\beta)$ does the same moves for every $\beta$ until it pops $X$. Call $(p, X)$ *looping* if this run is infinite and never pops $X$. Add two states $d_1$, which is final, and $d_0$, which is not, both without moves. For each looping $(p, X)$, replace its move by the $\varepsilon$-move to $d_1$ if the endless run passes through a final state (counting $p$), and to $d_0$ otherwise, with the stack unchanged. A run of $M$ that reaches $(p, x, X\beta)$ with $(p, X)$ looping never reads again, so it accepts exactly when $x = \varepsilon$ and the endless run passes through $F$; $M_1$ moves to $d_1$ or $d_0$ there and accepts in exactly the same case. Before such a configuration the two runs are equal, so $L(M_1) = L(M)$. Now suppose $M_1$ had an infinite run of $\varepsilon$-moves. Let $h \ge 1$ be the least stack height on it, and take a configuration $(p, \varepsilon, X\beta)$ of the run with $|X\beta| = h$. From there on the run never pops $X$, and it uses no new move, because $d_0$ and $d_1$ have no moves. So it is an infinite run of $M$ above $X$, and $(p, X)$ is looping. But then $M_1$ moves from $(p, X)$ to $d_0$ or $d_1$ and stops, a contradiction. $\square$

The looping pairs can be computed: the pairs $(p, X)$ whose run pops $X$, and those whose run stops above $X$, are least fixed points over the finite set $Q \times \Gamma$, and the looping pairs are the rest.

**Lemma 2 (removing the end marker).** If $L{\dashv}$ is a DCFL, then $L$ is a DCFL.

*Proof.* Let $M$ be a DPDA with $L(M) = L{\dashv}$. For a state $p$ and a stack $\gamma$ let $\mathrm{acc}(p, \gamma) = 1$ if $(p, {\dashv}, \gamma) \vdash^* (q, \varepsilon, \gamma')$ for some $q \in F$, and let $\mathrm{fin}(p, \gamma) = 1$ if $(p, \varepsilon, \gamma) \vdash^* (q, \varepsilon, \gamma')$ for some $q \in F$; both are $0$ otherwise. Let $T(\gamma)$ be the pair of maps $p \mapsto \mathrm{acc}(p, \gamma)$ and $p \mapsto \mathrm{fin}(p, \gamma)$. There are at most $4^{|Q|}$ such pairs.

*$T(X\gamma)$ depends only on $X$ and $T(\gamma)$.* The run from $(p, {\dashv}, X\gamma)$ does the same moves for every $\gamma$ until it pops $X$. So the following case depends only on $p$ and $X$. (i) After reading ${\dashv}$ it passes a final state before it pops $X$: then $\mathrm{acc}(p, X\gamma) = 1$. (ii) It pops $X$ before reading ${\dashv}$ and enters $r$: then $\mathrm{acc}(p, X\gamma) = \mathrm{acc}(r, \gamma)$. (iii) It reads ${\dashv}$, passes no final state after that, and pops $X$ into $r$: then $\mathrm{acc}(p, X\gamma) = \mathrm{fin}(r, \gamma)$. (iv) Otherwise it stops or runs forever above $X$ without accepting: $\mathrm{acc}(p, X\gamma) = 0$. In the same way, the run from $(p, \varepsilon, X\gamma)$ gives $\mathrm{fin}(p, X\gamma) = 1$ if it passes a final state before it pops $X$, $\mathrm{fin}(r, \gamma)$ if it then pops $X$ into $r$, and $0$ otherwise. So $T(X\gamma) = \Phi(X, T(\gamma))$ for a fixed function $\Phi$. For the empty stack, $\mathrm{acc}(p, \varepsilon) = 0$, because a machine with an empty stack has no move, and $\mathrm{fin}(p, \varepsilon) = 1$ exactly when $p \in F$.

*The automaton for $L$.* $M_2$ has the stack symbols $(X, t)$, where $t$ is the value of $T$ for the stack below the cell. Its states are $(p, b)$ with $b \in \{0, 1\}$ and $(p, ?)$, and its final states are the $(p, 1)$. Its start state is $(q_0, b_0)$, its start symbol is $(Z_0, T(\varepsilon))$, and $b_0$ is the $\mathrm{acc}$ part of $\Phi(Z_0, T(\varepsilon))$ at $q_0$. For each move $\delta(p, a, X) = (r, Y_1 \cdots Y_j)$ of $M$ with $a \in \Sigma \cup \{\varepsilon\}$ and each $t$, $M_2$ has the move from $((p, b), (X, t))$ on $a$ that pushes $(Y_1, t_1) \cdots (Y_j, t_j)$, where $t_j = t$ and $t_i = \Phi(Y_{i+1}, t_{i+1})$. If $j \ge 1$ it enters $(r, b')$, where $b'$ is the $\mathrm{acc}$ part of $\Phi(Y_1, t_1)$ at $r$. If $j = 0$ it enters $(r, ?)$, and from $(r, ?)$ with $(Y, t)$ on top an $\varepsilon$-move enters $(r, b')$ with $b'$ the $\mathrm{acc}$ part of $\Phi(Y, t)$ at $r$, and leaves the stack as it is. By induction on the number of moves, whenever $M_2$ is in a state $(p, b)$, its stack is the stack $X_1 \cdots X_m$ of $M$ with $T(X_{i+1} \cdots X_m)$ in cell $i$, and $b = \mathrm{acc}(p, X_1 \cdots X_m)$. $M_2$ is deterministic because $M$ is.

*Correctness.* Let $u \in \Sigma^*$. If $M$ stops before it reads all of $u$, then $u{\dashv} \notin L(M)$ and $M_2$ stops too. Otherwise let $(p, {\dashv}, \gamma)$ be the configuration of $M$ on $u{\dashv}$ just after it reads the last symbol of $u$ (the start configuration if $u = \varepsilon$). Then $u{\dashv} \in L(M)$ if and only if $\mathrm{acc}(p, \gamma) = 1$. After it reads $u$, $M_2$ passes through this configuration and then through the ones that follow by $\varepsilon$-moves. If $c \vdash c'$ is an $\varepsilon$-move of $M$, then $\mathrm{acc}(c) = \mathrm{acc}(c')$, because $M$ is deterministic and must make this move before it can read ${\dashv}$. So every state $(q, b)$ that $M_2$ passes after reading $u$ has $b = \mathrm{acc}(p, \gamma)$, and the states $(q, ?)$ are not final. Hence $u \in L(M_2)$ if and only if $u{\dashv} \in L(M)$, that is, $u \in L$. $\square$

**Proof of $1 \Rightarrow 3$.** Let $G$ be LR(k) with $L(G) = L$. An LR(k) grammar is also LR(k+1), because the premise $\mathrm{FIRST}_{k+1}(w) = \mathrm{FIRST}_{k+1}(y)$ implies $\mathrm{FIRST}_k(w) = \mathrm{FIRST}_k(y)$. So we may take $k \ge 1$, and we delete the useless symbols. By Fact K, no state of the canonical LR(k) automaton has a conflict. We build a DPDA $M$ over $\Sigma \cup \{\dashv\}$ that runs the LR(k) parser. Its stack holds the parser's stack of states, and its finite control holds a buffer $v$ of at most $k$ input symbols and a counter for reductions.

- *Fill.* While $|v| < k$ and $v$ does not contain ${\dashv}$, read one symbol and append it to $v$.
- *Act.* Let $u$ be $v$ padded with $\$$ to length $k$, with the ${\dashv}$ in $v$ read as $\$$. Do the parser's action for the top state and $u$, with $\varepsilon$-moves. A shift of the first symbol of $v$ pushes the goto state, removes the symbol from $v$ and returns to Fill. A reduction by $A \to \beta$ pops $|\beta|$ states one at a time, counting in the control, and then pushes the goto state on $A$ of the uncovered state. Accept enters a final state $f$ that has no moves. Error stops.

In Fill the moves read input, in Act they are $\varepsilon$-moves, and each table entry holds one action, so $M$ is deterministic. On an input $w{\dashv}$ with $w \in \Sigma^*$, $v$ always holds the next $k$ symbols of $w{\dashv}$, or all of them up to ${\dashv}$ if fewer remain, so $u$ is the lookahead string of the parser, and $M$ reaches $f$ exactly when the parser accepts $w$, that is, when $w \in L$. It has then read all of $w{\dashv}$, because accept needs the lookahead $\$^k$, so ${\dashv}$ is in the buffer. An input without ${\dashv}$ never gives the lookahead $\$^k$ and is not accepted. On an input $w{\dashv}z$ with $z \ne \varepsilon$, $M$ never reads past ${\dashv}$, so it does not accept. So $L(M) = L{\dashv}$, and $L$ is a DCFL by Lemma 2. $\square$

**Lemma 3 (an automaton for $L{\dashv}$ by empty stack).** If $L$ is a DCFL, there is a DPDA $M'$ with $N(M') = L{\dashv}$, whose moves push at most two symbols, and with a state $e$ such that: the moves that read ${\dashv}$ are exactly the moves that enter $e$ from another state, each of them pops, and the only moves from $e$ are $\delta'(e, \varepsilon, Y) = (e, \varepsilon)$ for all stack symbols $Y$.

*Proof.* Let $L = L(M)$. First make every move push at most two symbols: a move $\delta(p, a, X) = (r, Y_1 \cdots Y_j)$ with $j \ge 3$ becomes $\delta(p, a, X) = (t_1, Y_{j-1} Y_j)$ and $\delta(t_i, \varepsilon, Y_{j-i}) = (t_{i+1}, Y_{j-i-1} Y_{j-i})$ for $i = 1, \ldots, j-2$, with new states $t_1, \ldots, t_{j-2}$ that are not final and $t_{j-1} = r$. Then apply Lemma 1. Call the result $M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$ again.

$M'$ has the states $(p, f)$ for $p \in Q$ and a flag $f \in \{0, 1\}$, and two more states $s$ (the start) and $e$. Its stack alphabet is $\Gamma \cup \{X_0\}$ with start symbol $X_0$. Write $[\![ r \in F ]\!]$ for $1$ if $r \in F$ and $0$ otherwise. The moves are:

- $\delta'(s, \varepsilon, X_0) = ((q_0, [\![ q_0 \in F ]\!]), Z_0 X_0)$;
- for $\delta(p, \varepsilon, X) = (r, \alpha)$: $\delta'((p, f), \varepsilon, X) = ((r, \max(f, [\![ r \in F ]\!])), \alpha)$;
- for $\delta(p, a, X) = (r, \alpha)$ with $a \in \Sigma$: $\delta'((p, f), a, X) = ((r, [\![ r \in F ]\!]), \alpha)$;
- if $X = X_0$, or $X \in \Gamma$ and $M$ has no $\varepsilon$-move at $(p, X)$: $\delta'((p, 1), {\dashv}, X) = (e, \varepsilon)$;
- $\delta'(e, \varepsilon, Y) = (e, \varepsilon)$ for every $Y$.

$M'$ is deterministic: it reads ${\dashv}$ only where $M$ has no $\varepsilon$-move. On an input $w \in \Sigma^*$, $M'$ follows the run of $M$ with $X_0$ below, and the flag is $1$ exactly when the run has passed a final state since it read the last symbol (since the start, if $w = \varepsilon$). By Lemma 1, after $M$ reads $w$ it makes finitely many $\varepsilon$-moves and then reaches a configuration $c_w$ with no $\varepsilon$-move or with an empty stack. $M$ accepts $w$ if and only if one of the configurations from the last read up to $c_w$ is final, that is, if and only if the flag is $1$ at $c_w$. At $c_w$, $M'$ can read ${\dashv}$ exactly when the flag is $1$, and then $e$ empties the stack. So $w{\dashv} \in N(M')$ for every $w \in L$. Conversely, $X_0$ is popped only from $e$ or by a move on ${\dashv}$, so $M'$ empties its stack only after reading one ${\dashv}$, and then it stops. It reads ${\dashv}$ only at $c_w$ with the flag $1$, where $w$ is the input before ${\dashv}$, so $w \in L$. Hence $N(M') = L{\dashv}$. $\square$

### The grammar side

**The triple grammar.** For a DPDA $M'$ whose moves push at most two symbols, the triple grammar $G$ has the start symbol $S$, the nonterminals $[pXq]$ for states $p, q$ and stack symbols $X$, and these productions, where $a \in \Sigma \cup \{{\dashv}, \varepsilon\}$:

- $S \to [s X_0 q]$ for every state $q$, where $s$ and $X_0$ are the start state and start symbol;
- for $\delta'(p, a, X) = (r, \varepsilon)$: $[pXr] \to a$;
- for $\delta'(p, a, X) = (r, Y)$: $[pXq] \to a\,[rYq]$ for every $q$;
- for $\delta'(p, a, X) = (r, YZ)$: $[pXq] \to a\,[rYs]\,[sZq]$ for all $s, q$.

By the [triple construction](/cfg-pda-equivalence/), $[pXq] \Rightarrow^* w$ if and only if $(p, w, X) \vdash^* (q, \varepsilon, \varepsilon)$, and $L(G) = N(M')$. More precisely, a parse tree of $w$ from $[pXq]$ is such a run: each inner node is one move, and the node of $[pXq] \to a\,[rYs]\,[sZq]$ is the move from $(p, X)$ followed by the run of its first child, which pops $Y$ and ends in $s$, and the run of its second child, which pops $Z$ and ends in $q$. So the inner nodes in preorder are the moves in the order of time, and a nonterminal $[pXq]$ starts its run in $p$ and ends it in $q$.

**Strict deterministic grammars.** A grammar is *strict deterministic* (Harrison and Havel) if there is a partition of its symbols into blocks, with the terminals forming one block, such that for any equivalent nonterminals $A \equiv A'$ and productions $A \to \alpha\beta$ and $A' \to \alpha\beta'$:

- either $\beta \ne \varepsilon$, $\beta' \ne \varepsilon$ and their first symbols are equivalent,
- or $\beta = \beta' = \varepsilon$ and $A = A'$.

Deleting productions keeps this property, so deleting useless symbols does.

**Lemma 4.** The triple grammar of a DPDA whose moves push at most two symbols is strict deterministic.

*Proof.* Take the blocks: the terminals; $\{S\}$; and for each pair $(p, X)$ the block $\{[pXq] : q \text{ a state}\}$. Two equivalent nonterminals $[pXq]$ and $[pXq']$ get their productions from the moves at $(p, X)$. If two productions come from different moves, these moves read different terminals, because a DPDA with an $\varepsilon$-move at $(p, X)$ has no other move there. So the right sides start with different terminals, the common prefix $\alpha$ is $\varepsilon$, and the first symbols are equivalent. If both come from the same move, the right sides are $a$, or $a\,[rYq]$ and $a\,[rYq']$, or $a\,[rYs]\,[sZq]$ and $a\,[rYs']\,[s'Zq']$. After a common prefix, the next symbols are both $a$, or both in the block of $(r, Y)$, or both in the block of $(s, Z)$; or the common prefix is a whole right side, and then the two right sides are equal, so $q = q'$ and the left sides are equal. The productions $S \to [s X_0 q]$ are handled in the same way. $\square$

**Lemma 5 (Harrison and Havel).** A strict deterministic grammar without useless symbols, augmented with $S' \to S$ and with $S'$ in a block of its own, is LR(0).

*Proof.* For a block $B$ of nonterminals, apply the definition with $\alpha = \varepsilon$. Either the first symbols of all right sides of the members of $B$ lie in one block, which we call $\mathrm{next}(B)$; or some member $A$ has $A \to \varepsilon$, and then $B = \{A\}$ and $A \to \varepsilon$ is the only production of $B$. We call $B$ an *$\varepsilon$-block* in the second case.

*The chain $B, \mathrm{next}(B), \mathrm{next}(\mathrm{next}(B)), \ldots$ never repeats a block.* It stops at the terminal block or at an $\varepsilon$-block. If it repeated, it would go around a cycle of blocks that are neither. Take a member of a block on the cycle and a parse tree of some terminal string from it, which exists because there are no useless symbols. The first child of every inner node on the leftmost path lies in the next block of the cycle, so it is again an inner node, and the path is infinite, a contradiction.

*The kernels.* For a viable prefix $\gamma$, let the kernel $K(\gamma)$ be the items of $\mathrm{st}(\gamma)$ whose dot is not at the start, and $K(\varepsilon) = \{[S' \to \cdot S]\}$. We show by induction on $|\gamma|$: all items of $K(\gamma)$ have the same string $\mu$ before the dot, and their left sides lie in one block. This holds for $\gamma = \varepsilon$. Let it hold for $\gamma$. By the strict determinism of the items of $K(\gamma)$, either $K(\gamma)$ is a single complete item, or all its items have a symbol after the dot, and these symbols lie in one block $B_1$. In the second case, the closure of $K(\gamma)$ adds the items $[C \to \cdot \rho]$ in layers: layer $i \ge 1$ has its left sides in $B_i$ and its symbols after the dot in $B_{i+1} = \mathrm{next}(B_i)$. The blocks $B_1, B_2, \ldots$ are all different, so a symbol $X$ lies in at most one of them, and all items of $\mathrm{st}(\gamma)$ with $X$ after the dot lie in one layer: the kernel, or layer $i$. The items of $K(\gamma X)$ come from these items by moving the dot over $X$, so they all have the same string before the dot ($\mu X$, or $X$) and left sides in one block.

*No conflicts.* If $K(\gamma)$ has a complete item, strict determinism says that all items of $K(\gamma)$ are this one item, so $\mathrm{st}(\gamma)$ is one complete item. Otherwise the only complete item that the layers can add is $[E \to \cdot]$, when the chain $B_1, B_2, \ldots$ ends at an $\varepsilon$-block $\{E\}$. Then no block of the chain is the terminal block, so no item has a terminal after the dot, and there is only one complete item. If the chain ends at the terminal block, there is no complete item. In all cases there is no conflict, and $G$ is LR(0) by Fact K. $\square$

**Proof of $3 \Rightarrow 4$.** Let $L$ be a DCFL. Lemma 3 gives $M'$ with $N(M') = L{\dashv}$. Its triple grammar generates $L{\dashv}$ and is strict deterministic by Lemma 4. After deleting its useless symbols it is LR(0) by Lemma 5. (If $L = \emptyset$, the grammar with no productions is LR(0).) $\square$

**Proof of $4 \Rightarrow 3$.** Let $G$ be LR(0) with $L(G) = L{\dashv}$. By $1 \Rightarrow 3$, applied to $L{\dashv}$ over the alphabet $\Sigma \cup \{\dashv\}$, $L{\dashv}$ is a DCFL. By Lemma 2, $L$ is a DCFL. $\square$

**Lemma 6 (deleting the end marker from the grammar).** Let $G$ be the grammar of the proof of $3 \Rightarrow 4$, without useless symbols, and let $G'$ be $G$ with ${\dashv}$ deleted from every right side. Then $L(G') = L$ and $G'$ is LR(1).

*Proof.* Write $h(\psi)$ for $\psi$ with ${\dashv}$ deleted.

*(a) $h$ is one to one on productions.* The moves that read ${\dashv}$ pop and enter $e$, so the productions with ${\dashv}$ are $[pXe] \to {\dashv}$. The other productions of $[pXe]$ come from moves at $(p, X)$ on terminals of $\Sigma$, because there is no $\varepsilon$-move at $(p, X)$. Their right sides start with a terminal of $\Sigma$, so none of them is $\varepsilon$. So each production of $G'$ comes from exactly one production of $G$, and each rightmost derivation in $G'$ is the image under $h$ of exactly one rightmost derivation in $G$.

*(b) $L(G') = L$.* The image of a derivation of $w{\dashv}$ derives $w$. Conversely, a derivation of $w$ in $G'$ is the image of a derivation in $G$ of a word of $L{\dashv}$ whose image is $w$, and this word is $w{\dashv}$.

*(c) The sentential forms of $G$.* Let $\psi$ be a sentential form of $G$ derived from $S$, and complete it to a parse tree of a word of $L{\dashv}$; this word has one ${\dashv}$, at its end. The state $e$ is entered only by the move on ${\dashv}$ and is never left. So a nonterminal of $\psi$ to the right of a ${\dashv}$ in $\psi$ starts its run after that move: it is $[eXe]$. A nonterminal $[pXq]$ of $\psi$ to the left of it ends its run before that move, so $q \ne e$. If $\psi$ has no ${\dashv}$, the ${\dashv}$ of the word comes from a nonterminal $[pXq]$ of $\psi$ whose run contains the move on ${\dashv}$, so $q = e$ and $p \ne e$. Hence $\psi$ is determined by $h(\psi)$: if $h(\psi)$ contains a nonterminal $[pXe]$ with $p \ne e$, then $\psi = h(\psi)$; otherwise $\psi = u\,{\dashv}\,v$, where $v$ is the longest suffix of $h(\psi)$ made of nonterminals $[eXe]$.

*(d) $G'$ is LR(1).* Take rightmost derivations in $G'$

$$S' \Rightarrow_{rm}^* \alpha A w \Rightarrow_{rm} \alpha\beta w \qquad \text{and} \qquad S' \Rightarrow_{rm}^* \gamma B x \Rightarrow_{rm} \gamma\delta x = \alpha\beta y$$

with $\mathrm{FIRST}_1(w) = \mathrm{FIRST}_1(y)$. By (a) they are the images of derivations in $G$ that end with the right sentential forms $\psi_1 = \tilde\alpha\tilde\beta\tilde w$ and $\psi_2 = \tilde\gamma\tilde\delta\tilde x$, with $h(\tilde\alpha) = \alpha$ and so on. We show that $\psi_2 = \tilde\alpha\tilde\beta\tilde y$ for a terminal string $\tilde y$. If $w = \varepsilon$, then $y = \varepsilon$, so $h(\psi_1) = \alpha\beta = h(\psi_2)$, and $\psi_1 = \psi_2$ by (c). If $w \ne \varepsilon$, then $h(\psi_1) = \alpha\beta w$ ends with a terminal of $\Sigma$. It contains no $[pXe]$ with $p \ne e$, since otherwise $\psi_1 = h(\psi_1)$ would have a terminal of $\Sigma$ after a nonterminal that derives ${\dashv}$. So by (c), $\psi_1 = \alpha\beta w{\dashv}$, with $\tilde\alpha\tilde\beta = \alpha\beta$ and $\tilde w = w{\dashv}$. Also $y \ne \varepsilon$, and $h(\psi_2) = \alpha\beta y$ ends with a terminal of $\Sigma$ and contains no $[pXe]$ with $p \ne e$, so $\psi_2 = \alpha\beta y{\dashv}$. In both cases $G$, which is LR(0), gives $\tilde\gamma = \tilde\alpha$, $B = A$ and $\tilde x = \tilde y$. Applying $h$ gives $\gamma = \alpha$, $B = A$ and $x = y$. $\square$

**Proof of $3 \Rightarrow 2$.** Lemma 6. $\blacksquare$

### An example

Let $M$ have the states $p, q, r, f$ with $F = \{p, f\}$, start state $p$, start symbol $Z$ and the moves $\delta(p, a, Z) = (q, AZ)$, $\delta(q, a, A) = (q, AA)$, $\delta(q, b, A) = (r, \varepsilon)$, $\delta(r, b, A) = (r, \varepsilon)$ and $\delta(r, \varepsilon, Z) = (f, Z)$. Then $L(M) = \{a^m b^m : m \ge 0\}$, and $M$ has no endless $\varepsilon$-run. Write $p^1$ for the state $(p, 1)$ of $M'$, $q^0$ for $(q, 0)$, and so on. After the useless symbols are deleted, the triple grammar of $M'$ has 10 productions:

$$\begin{aligned} S &\to [s X_0 e] & [s X_0 e] &\to [p^1 Z e]\,[e X_0 e] & [e X_0 e] &\to \varepsilon \\ [p^1 Z e] &\to a\,[q^0 A r^0]\,[r^0 Z e] \mid {\dashv} & [r^0 Z e] &\to [f^1 Z e] & [f^1 Z e] &\to {\dashv} \\ [q^0 A r^0] &\to a\,[q^0 A r^0]\,[r^0 A r^0] \mid b & [r^0 A r^0] &\to b \end{aligned}$$

It generates $L(M){\dashv}$ and its canonical LR(0) automaton has no conflict. Deleting ${\dashv}$ turns $[p^1 Z e] \to {\dashv}$ and $[f^1 Z e] \to {\dashv}$ into $\varepsilon$-productions. The result generates $\{a^m b^m : m \ge 0\}$, is LR(1), and is not LR(0): after $a^m b^m$ the parser must see whether the input has ended.

## Consequences

- **One token of lookahead is enough for languages.** A parser generator that accepts only LR(1) grammars loses no deterministic language; it may only force the user to rewrite the grammar.
- **Deterministic languages are unambiguous.** Every LR(k) grammar is unambiguous (see the [LR(k) grammar](/lr-grammar/) page), so every DCFL has an unambiguous grammar. An [inherently ambiguous](/inherent-ambiguity/) language, such as $\{a^i b^j c^k : i = j \text{ or } j = k\}$, is therefore not deterministic.
- **Linear-time parsing.** Every DCFL is parsed in $O(n)$ time by the [canonical LR(1) parser](/canonical-lr-parsing/) of an LR(1) grammar for it.
- **LR(0) languages.** The languages of LR(0) grammars are exactly the DCFLs with the *prefix property*: no word is a proper prefix of another. If $G$ is LR(0), $L(G)$ is a DCFL by $1 \Rightarrow 3$, and it has the prefix property by the argument under Tightness. Conversely, let $L = L(M)$ have the prefix property, with $M$ as in the proof of Lemma 3, and let $M''$ be $M$ with a new bottom symbol in which every final state $p$ has, instead of its moves, the $\varepsilon$-moves that pop to a state $e$ that pops everything. $M''$ empties its stack the first time $M$ passes a final state. That happens after it reads $w$ exactly when $w \in L$, since no proper prefix of $w$ is in $L$. So $N(M'') = L$, and by Lemmas 4 and 5 the triple grammar of $M''$ is LR(0).
- **The end marker is the only gap.** Statement 4 shows that the step from LR(0) to LR(1) is, for languages, the same as adding an end marker. This matches the common convention of augmenting with $S' \to S\,\$$ and shifting $\$$ like a token, under which, for example, the [LR(0) parser](/lr0-parsing/) handles languages without the prefix property.

## Tightness

- **LR(1) cannot be lowered to LR(0).** The language $\{a, aa\}$ is a DCFL, and $S \to a \mid a\,a$ is an LR(1) grammar for it, but no LR(0) grammar generates it. Let $G$ be LR(0) with $w$ and $wz$ in $L(G)$, $z \ne \varepsilon$. Its LR(0) parser chooses each action from the top state alone. On $w$ and on $wz$ it does the same actions until it has shifted all of $w$ and made the reductions that follow, since these do not look at the input. On $w$ it then accepts, so the state on top has the item $[S' \to S \cdot]$ and, with no conflict, no shift. On $wz$ it reaches the same state, where the only action is accept, so it cannot shift the first symbol of $z$ and never accepts $wz$, which contradicts Theorem 2 of the canonical LR page. So an LR(0) language has the prefix property, and $\{a, aa\}$ does not.
- **The collapse holds for languages, not for grammars.** The grammar $S \to A\,a\,b \mid B\,a\,c$, $A \to c$, $B \to c$ is LR(2) and not LR(1) (see the [LR(k) grammar](/lr-grammar/) page), while its language $\{cab, cac\}$ has the LR(0) grammar $S \to c\,a\,b \mid c\,a\,c$. Lemma 6 changes the grammar completely; it does not turn a given LR(k) grammar into an LR(1) grammar with the same parse trees.
- **Unambiguous is not enough.** The language $\{a^m b^m : m \ge 1\} \cup \{a^m b^{2m} : m \ge 1\}$ has an unambiguous grammar but is not a DCFL (proof on the [deterministic context-free language](/deterministic-context-free-language/) page), so it has no LR(k) grammar for any $k$. The even palindromes are another example.
- **Size.** The DPDA built from an LR(k) grammar has one state per state of the canonical LR(k) automaton, which can be exponential in $|G|$. The triple grammar has up to $|Q'|^2$ productions for each move of $M'$, and $M'$ has about twice as many states as $M$.

## History

Knuth introduced LR(k) grammars in 1965. In the same paper he showed that an LR(k) grammar has a parser that works like a deterministic pushdown machine, that the languages of LR(k) grammars are exactly the languages of deterministic pushdown automata, and that every such language already has an LR(1) grammar. Ginsburg and Greibach (1966) studied the deterministic context-free languages as a class, including their closure under complement. Harrison and Havel (1973) introduced strict deterministic grammars, showed that they are LR(0), and showed that their languages are the deterministic languages with the prefix property; Lemma 5 above is their result, with a proof through LR(0) items. Hopcroft and Ullman (1979, Chapter 10) give a textbook treatment of deterministic pushdown automata, LR(0) grammars and the role of the end marker.

## References
