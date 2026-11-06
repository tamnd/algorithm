---
tag: Z0RM8G
kind: algorithm
slug: glr-parsing
name: Generalized LR parsing
aliases:
- GLR parsing
- Tomita parsing
- Tomita's algorithm
- generalized LR parsing
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Extends LR parsing to any context-free grammar by forking the parser on conflicts.
solves: [context-free-language-recognition, cfg-membership-problem, cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the length of the input string, p: the length of the longest right side or 2 if all right sides are shorter}
  time: {worst: O(n^(p+1)), best: O(n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1986
  people: [Masaru Tomita, Bernard Lang]
  note: Tomita published the algorithm with the graph-structured stack in a 1986 book and a 1987 journal paper. Lang had described the simulation of a nondeterministic LR parser with shared stacks in 1974.
prereqs: [lr0-parsing, graph-structured-stack, ambiguity]
see_also: [earley-parser, gll-parsing, shared-packed-parse-forest, lalr-parsing, cyk-algorithm, inherent-ambiguity, shift-reduce-conflict, reduce-reduce-conflict]
sources:
  - paper: url:https://aclanthology.org/J87-1004/
    title: Masaru Tomita, An efficient augmented-context-free parsing algorithm, Computational Linguistics 13(1-2) (1987)
    locator: pp. 31 to 46
  - paper: doi:10.1007/978-3-662-21545-6_18
    title: Bernard Lang, Deterministic techniques for efficient non-deterministic parsers, Automata, Languages and Programming (ICALP 1974), LNCS 14
    locator: pp. 255 to 269
  - paper: doi:10.1007/978-1-4615-4034-2_5
    title: Rahman Nozohoor-Farshi, GLR parsing for ε-grammars, in Masaru Tomita (ed.), Generalized LR Parsing, Kluwer (1991)
    locator: pp. 61 to 75
  - paper: doi:10.1145/1146809.1146810
    title: Elizabeth Scott and Adrian Johnstone, Right nulled GLR parsers, ACM Transactions on Programming Languages and Systems 28(4) (2006)
    locator: pp. 577 to 618
  - paper: doi:10.1007/s00236-007-0054-z
    title: Elizabeth Scott, Adrian Johnstone and Rob Economopoulos, BRNGLR, a cubic Tomita-style GLR parsing algorithm, Acta Informatica 44(6) (2007)
    locator: pp. 427 to 461
  - paper: doi:10.1016/j.scico.2006.04.004
    title: Adrian Johnstone, Elizabeth Scott and Giorgios Economopoulos, Evaluating GLR parsing algorithms, Science of Computer Programming 61(3) (2006)
    locator: pp. 228 to 244
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 11.1, Generalized LR Parsing (11.1.1, p. 382; 11.1.2 Necessary Optimizations, p. 383; 11.1.3 Hidden Left Recursion and Loops, p. 387)
---

Generalized LR (GLR) parsing runs an [LR parser](/lr-parsing/) on any [context-free grammar](/context-free-grammar/), also an [ambiguous](/ambiguity/) one, by following every action of a conflict in parallel. All the parallel stacks are kept in one [graph-structured stack](/graph-structured-stack/), where stacks that reach the same state at the same input position merge, so the work stays polynomial although the number of stacks can grow exponentially. On a grammar with few conflicts it runs almost like a deterministic LR parser, in linear time. Parser generators such as Bison offer it as a mode for grammars that are not LR.

## In plain words

An LR parser reads the input from left to right and keeps a stack that tells it what it has seen. For most grammars of programming languages, the next symbol tells it exactly what to do. For other grammars, the parser sometimes has two choices and cannot know which one is right. A GLR parser does not choose: it splits and follows both choices. A branch that meets an input symbol it cannot accept dies. When two branches arrive at the same situation at the same place in the input, they join again, and the parser does the remaining work once for both. At the end, the input is accepted if some branch has read all of it and built the start symbol.

## The problem

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$.

The input is a context-free grammar $G = (V, \Sigma, P, S)$, with any productions: empty right sides, unit productions, left recursion and cycles are allowed, and a word $w = a_1 \cdots a_n$ over $\Sigma$. The recognizer outputs yes when $S \Rightarrow^* w$ and no otherwise ([membership problem](/cfg-membership-problem/)). The parser also outputs one [parse tree](/parse-tree/) of $w$ ([parsing problem](/cfg-parsing-problem/)), and with packing it can output all of them as a [shared packed parse forest](/shared-packed-parse-forest/).

## The algorithm

**The LR(0) automaton.** Add a new start symbol $S'$ and the production $S' \to S$. An [LR(0) item](/lr-item/) is a production with a dot in its right side. The closure of a set of items adds $B \to \bullet \eta$ for every production of $B$ whenever an item $A \to \beta \bullet B \gamma$ is in the set. The start state is $q_0 = \mathrm{CLOSURE}(\{S' \to \bullet S\})$, and $\mathrm{GOTO}(q, X)$ is the closure of the items $A \to \beta X \bullet \gamma$ with $A \to \beta \bullet X \gamma \in q$, defined when this set is not empty. The states are the sets reachable from $q_0$, as in [LR(0) parsing](/lr0-parsing/). A state $q$ has a **reduction** $A \to \alpha$ when $A \to \alpha \bullet \in q$. A deterministic parser needs at most one action in each state for each input symbol; GLR accepts states with [shift-reduce](/shift-reduce-conflict/) and [reduce-reduce conflicts](/reduce-reduce-conflict/) and follows all their actions. Every state other than $q_0$ has an **accessing symbol**: all its items with the dot after the start have the same symbol $X$ just before the dot, the symbol on which it is entered.

**The stack graph.** A node of the GSS is a pair $(s, j)$ of a state and a level, the number of input symbols read. The set $U_j$ holds the nodes of level $j$. An edge $v \to x$ from $v = (s, j)$ to $x = (t, i)$ means that the cell $v$ lies directly on $x$; then $s = \mathrm{GOTO}(t, X)$ for the accessing symbol $X$ of $s$, and $X \Rightarrow^* a_{i+1} \cdots a_j$. Each edge carries one parse tree of $X$ for this part of the input. Every path from a node to the root $(q_0, 0)$ is one stack of an LR parser.

```pseudo id=main
GLR(G, w)                                          ▷ w = a1 … an
L1  build the LR(0) automaton of G with S′ → S: states, start state q0, GOTO, reductions R(q) = { A → α : A → α • ∈ q }
L2  create the node root = (q0, 0); U0 ← {root}
L3  for j ← 0 to n do
L4      Q ← { (u, r, none) : u ∈ Uj, r ∈ R(state(u)) }
L5      while Q ≠ ∅ do
L6          remove some (u, A → α, e) from Q
L7          for each path of |α| edges from u that uses e (any path if e = none), ending at node x do
L8              v ← (GOTO(state(x), A), j); if v ∉ Uj then add v to Uj and add (v, r, none) to Q for every r ∈ R(state(v))
L9              else if the edge v → x is new then add (u′, r, v → x) to Q for every u′ ∈ Uj and every r ∈ R(state(u′)) with a nonempty right side
L10             add the edge v → x if it is new, with the tree A(trees on the path, bottom first)
L11     if j < n then for each u ∈ Uj with GOTO(state(u), a_{j+1}) = s defined do
L12         add the node (s, j + 1) to U_{j+1} if needed, and the edge (s, j + 1) → u with the leaf a_{j+1}
L13 return true and the tree on the edge if the node (GOTO(q0, S), n) exists and has an edge to root, else false
```

Each phase $j$ first does all reductions at level $j$, then shifts $a_{j+1}$ from every node of level $j$. A reduction by $A \to \alpha$ from a node $u$ pops $|\alpha|$ cells along every path, as in an LR parser, and pushes the cell $\mathrm{GOTO}(\mathrm{state}(x), A)$ on the cell $x$ where the path ends. Line L7 uses POP of the [graph-structured stack](/graph-structured-stack/). A reduction by an empty production has a path of length 0, so $x = u$ and the new edge stays inside level $j$.

Line L9 is the step that makes the algorithm correct for all grammars. When a reduction adds a new edge to a node that already exists, the paths through this edge are new stacks. Reductions that ran earlier on nodes of level $j$ did not see them. So line L9 queues every reduction of level $j$ again, but only for the paths that use the new edge. Empty reductions need not be queued again, because their path of length 0 does not use any edge. The queue order does not matter.

If line L7 finds a path to $x$ when the edge $v \to x$ already exists, then the input between $x$ and $v$ can be read as $A$ in a second way. This is a local ambiguity. The implementation keeps the first tree; a parser that wants all trees adds the new tree to a packed node on the edge instead.

## Example

Take the ambiguous grammar $S \to S S \mid a$ and $w = a a a$. The LR(0) automaton has four states:

| State | Items | GOTO |
|---|---|---|
| $q_0$ | $S' \to \bullet S$, $S \to \bullet S S$, $S \to \bullet a$ | $S \mapsto q_1$, $a \mapsto q_2$ |
| $q_1$ | $S' \to S \bullet$, $S \to S \bullet S$, $S \to \bullet S S$, $S \to \bullet a$ | $S \mapsto q_3$, $a \mapsto q_2$ |
| $q_2$ | $S \to a \bullet$ | none |
| $q_3$ | $S \to S S \bullet$, $S \to S \bullet S$, $S \to \bullet S S$, $S \to \bullet a$ | $S \mapsto q_3$, $a \mapsto q_2$ |

The state $q_3$ has a shift-reduce conflict: it can reduce by $S \to S S$ and it can shift $a$. The run, phase by phase:

| Phase | Reductions | Shift of the next $a$ |
|---|---|---|
| 0 | none | $(q_2, 1) \to (q_0, 0)$ |
| 1 | $S \to a$ from $(q_2, 1)$: $(q_1, 1) \to (q_0, 0)$ | $(q_2, 2) \to (q_1, 1)$; the branch of $(q_2, 1)$ dies |
| 2 | $S \to a$ from $(q_2, 2)$: $(q_3, 2) \to (q_1, 1)$. $S \to S S$ from $(q_3, 2)$: $(q_1, 2) \to (q_0, 0)$ | $(q_2, 3) \to (q_3, 2)$ and $(q_2, 3) \to (q_1, 2)$ |
| 3 | $S \to a$ from $(q_2, 3)$: $(q_3, 3) \to (q_1, 2)$, then the new edge $(q_3, 3) \to (q_3, 2)$ on the existing node. $S \to S S$ through it: $(q_3, 3) \to (q_1, 1)$, again a new edge. $S \to S S$ through that: $(q_1, 3) \to (q_0, 0)$. $S \to S S$ on all paths from $(q_3, 3)$: no new edges | none, $j = n$ |

In phase 2, the two stacks that end in $q_3$ and $q_1$ both shift $a$ into the state $q_2$, so they merge into the single node $(q_2, 3)$, and the reduction $S \to a$ in phase 3 runs once for both. In phase 3, the edge $(q_1, 3) \to (q_0, 0)$ is found twice, once for the parse $a\,(a a)$ through $(q_3, 3) \to (q_1, 1)$, and once for the parse $(a a)\,a$ through $(q_3, 3) \to (q_1, 2)$. The GSS keeps one edge, a local ambiguity. Line L13 finds the node $(\mathrm{GOTO}(q_0, S), 3) = (q_1, 3)$ with an edge to the root, so $a a a$ is accepted, and the tree on that edge is the first one found, $S \to S S$ with $S \to a$ on the left and $S \to S S$ over $a a$ on the right. The final GSS, with 9 nodes and 11 edges, is shown on the [graph-structured stack](/graph-structured-stack/) page.

## Correctness

**Claim.** GLR returns true if and only if $S \Rightarrow^* w$, and the tree it returns is a parse tree of $w$.

*Soundness.* By induction on the order in which edges are made, every edge $v \to x$ from $(s, j)$ to $(t, i)$ has $s = \mathrm{GOTO}(t, X)$ for the accessing symbol $X$ of $s$, and its tree is a parse tree of $X$ for $a_{i+1} \cdots a_j$. For a reduction edge, the symbols on the path read from bottom to top lead from $\mathrm{state}(x)$ to $\mathrm{state}(u)$ in the automaton. An item with the dot at the end of a right side of length $m$ can only come from the same item with the dot at the start, $m$ GOTO steps before. So the path spells $\alpha$, and $A \to \bullet \alpha \in \mathrm{state}(x)$. The edge to the root that line L13 tests therefore carries a parse tree of $S$ for all of $w$.

*Completeness.* Take a [rightmost derivation](/derivation/) of $w$, and run it backwards as a sequence of shifts and reductions of a deterministic LR parser that always guesses right. Every stack of that run is a path in the GSS. A shift is possible because every stack of the run is a prefix of a stack that ends with a [handle](/handle/), whose item is valid and so is in the LR(0) state. A reduction is done because of a saturation lemma: at the end of phase $j$, for every node $u$ of level $j$, every reduction $A \to \alpha$ of its state and every path of $|\alpha|$ edges from $u$ to some $x$, the edge from $(\mathrm{GOTO}(\mathrm{state}(x), A), j)$ to $x$ exists. Its proof looks at the newest edge of the path: it existed before the phase, or it is the first edge of a new node, which then is $u$ and was queued by line L8, or it is a new edge of an old node, queued by line L9. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Fix the grammar. Then the automaton has a fixed number $|Q|$ of states, and each level has at most $|Q|$ nodes. Let $p$ be the length of the longest right side, or 2 if all right sides are shorter.

- **Nodes and edges.** The GSS has at most $|Q|\,(n + 1)$ nodes. An edge goes from a node of level $j$ to one of a level $i \le j$, so each node has $O(j)$ edges, and there are $O(n^2)$ edges in all.
- **Queue entries.** In phase $j$, line L4 and line L8 queue $O(1)$ entries, at most $|P|$ for each node. Line L9 queues $O(1)$ entries for each new edge whose source is at level $j$, and there are $O(j)$ such edges. So the phase has $O(j)$ entries.
- **Paths.** An entry without an edge visits at most $O(j^p)$ partial paths, one choice of $O(j)$ edges at each of at most $p$ steps. An entry with an edge $e$ follows only paths that stay in level $j$ until they use $e$. That part has $O(1)$ choices, with $O(j)$ edges tested at each step, and after $e$ there are at most $p - 1$ steps of $O(j)$ choices. So the entry costs $O(j + j^{p-1})$.
- **Total.** Phase $j$ costs $O(j^p)$, and the run costs $O(n^{p+1})$ time. It uses $O(n^2)$ space for the GSS and the trees on its edges, since each tree node only points to the trees of the edges below it.

**Best case.** On an [LR(0) grammar](/lr0-parsing/), every state has one action, so the GSS is a single stack plus finished cells, each level has $O(1)$ nodes, and the time is $O(n)$. On grammars with few conflicts, most levels behave in this way.

**The grammar.** The LR(0) automaton can have a number of states exponential in $|G|$, and the bounds above hide factors that depend on it. Earley's algorithm has a cubic bound $O(n^3 |G|)$ for every grammar. Binarized variants of GLR reach $O(n^3)$ for every grammar (see below).

## Properties

- **General.** It accepts every context-free grammar, with empty and unit productions, left recursion, hidden left recursion and cycles.
- **Online, with the prefix property.** Phase $j$ depends only on $a_1 \cdots a_j$. When $U_{j+1}$ is empty after a shift, no word of the language starts with $a_1 \cdots a_{j+1}$, and the parser stops with an error at that symbol.
- **Deterministic.** The GSS at the end of each phase does not depend on the order of the queue. Which tree the parser returns for an ambiguous input can depend on it.
- **Close to LR.** Where the automaton has no conflict, the GSS has a single top and GLR does what an LR parser does.

## Variants and improvements

- **Lookahead.** The algorithm on this page uses the LR(0) automaton with no lookahead. Tables with [LALR(1)](/lalr-parsing/) or [canonical LR(1)](/canonical-lr-parsing/) lookahead allow a reduction only before the right next symbol. This kills many branches early.
- **Tomita's algorithm.** Tomita's original version is not correct for some grammars with empty productions, among them grammars with hidden left recursion. Nozohoor-Farshi gave a correction in 1991, and Grune and Jacobs discuss the problem in Section 11.1.3 of their book.
- **Right nulled GLR (RNGLR).** Scott and Johnstone add reductions that skip a nullable end of the right side, so that the reductions caused by a new edge can start at that edge. This handles all grammars with fewer path searches.
- **Binary RNGLR (BRNGLR).** Each reduction pops at most two edges at a time, with extra nodes for the partial reductions. This gives $O(n^3)$ worst-case time for every grammar, like Earley's algorithm.
- **Parse forests.** Packing all trees of an edge into one node gives a [shared packed parse forest](/shared-packed-parse-forest/) of all parses, of polynomial size, even when the number of parses is exponential or infinite.
- **GLL.** [GLL parsing](/gll-parsing/) applies the same idea of a shared stack graph to recursive descent instead of LR.

## When to use it

Use GLR when the grammar is close to LR but not quite: a programming-language grammar with a few conflicts, a grammar that is easier to write in an ambiguous form with ambiguities resolved later, or a natural-language grammar. It keeps the speed of an LR parser where the grammar is deterministic and pays for generality only where it is not. For a grammar that is far from LR, or when the grammar changes often, an [Earley parser](/earley-parser/) needs no table construction and has a cubic bound. For an LALR(1) grammar, a plain [LALR(1) parser](/lalr-parsing/) is simpler and needs only $O(n)$ space.

## Pitfalls

- **Missing reductions through new edges.** A reduction that has already run from a node must run again on the paths through any edge added to that node later. With $S \to a S \mid \varepsilon$ and the input $a a$, the reduction $S \to a S$ in phase 2 adds an edge from the node of $\mathrm{GOTO}(q_a, S)$ to the node of $q_a$ at level 1, where $q_a = \mathrm{GOTO}(q_0, a)$. The node already exists, and only the stack through the new edge reaches the root. A parser without line L9 rejects $a a$.
- **Cycles in the GSS.** With empty productions, a reduction can add an edge from a node to itself, for example with $S \to A S \mid b$ and $A \to \varepsilon$. A path search that does not stop after $|\alpha|$ edges loops forever.
- **Infinitely many trees.** With a cyclic grammar such as $S \to S \mid a$, a word has infinitely many parse trees. Keep one tree per edge, or a packed forest with cycles, and never list all trees.
- **Exponentially many trees.** The number of parse trees of $a^n$ under $S \to S S \mid a$ is a Catalan number. Return a packed forest, not a list of trees.
- **Recursion depth.** Stacks and trees can have depth $n$. Search paths and walk trees with explicit stacks.

## Implementations

## History

Lang showed in 1974 how to run a nondeterministic LR parser in polynomial time by dynamic programming over shared stack configurations. Tomita gave the algorithm with the graph-structured stack and packed parse forests for natural-language parsing, in a 1986 book and a 1987 paper in Computational Linguistics. Nozohoor-Farshi corrected the treatment of empty productions in 1991. Scott and Johnstone gave right nulled GLR in 2006, and with Economopoulos the cubic BRNGLR algorithm in 2007. GLR parsers are used in Bison's GLR mode and in parsers for natural language.

## References
