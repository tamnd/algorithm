---
tag: M4B9MB
kind: problem
slug: cfl-reachability
name: CFL reachability
aliases:
- Dyck reachability
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Given an edge-labeled graph, decide whether a path's label word belongs to a fixed context-free language.
model: word-ram
complexity:
  vars: {n: the number of vertices, g: the grammar size}
  time: {worst: O(g n^3)}
prereqs: [context-free-grammar, graph-reachability, dyck-language, chomsky-normal-form]
see_also: [pushdown-reachability, pushdown-system, transitive-closure, datalog, semi-naive-evaluation, cyk-algorithm, cfl-closure-properties, cfl-intersection-undecidable]
sources:
  - paper: doi:10.1145/298514.298576
    title: Mihalis Yannakakis, Graph-theoretic methods in database theory, Proceedings of the Ninth ACM Symposium on Principles of Database Systems (1990)
    locator: pp. 230 to 242 (chain queries as context-free path problems and the cubic algorithm)
  - paper: doi:10.1145/199448.199462
    title: Thomas Reps, Susan Horwitz and Mooly Sagiv, Precise interprocedural dataflow analysis via graph reachability, Proceedings of the 22nd ACM Symposium on Principles of Programming Languages (1995)
    locator: pp. 49 to 61 (interprocedural dataflow problems as reachability along realizable paths)
  - paper: doi:10.1016/S0950-5849(98)00093-7
    title: Thomas Reps, Program analysis via graph reachability, Information and Software Technology 40(11-12) (1998)
    locator: pp. 701 to 726 (the CFL-reachability problem, its dynamic-programming algorithm and applications)
  - paper: doi:10.1016/S0304-3975(00)00049-9
    title: David Melski and Thomas Reps, Interconvertibility of a class of set constraints and context-free-language reachability, Theoretical Computer Science 248(1-2) (2000)
    locator: pp. 29 to 98
  - paper: doi:10.1109/LICS.1997.614960
    title: Nevin Heintze and David McAllester, On the cubic bottleneck in subtyping and flow analysis, Proceedings of the Twelfth Annual IEEE Symposium on Logic in Computer Science (1997)
    locator: pp. 342 to 351 (the problem is complete for two-way nondeterministic pushdown automata)
  - paper: doi:10.1145/1328438.1328460
    title: Swarat Chaudhuri, Subcubic algorithms for recursive state machines, Proceedings of the 35th ACM Symposium on Principles of Programming Languages (2008)
    locator: pp. 159 to 169 (an O(n^3 / log n) algorithm)
  - paper: doi:10.1145/3158118
    title: Krishnendu Chatterjee, Bhavya Choudhary and Andreas Pavlogiannis, Optimal Dyck reachability for data-dependence and alias analysis, Proceedings of the ACM on Programming Languages 2(POPL) (2018)
    locator: pp. 1 to 30 (bidirected Dyck reachability in almost linear time)
  - paper: doi:10.1145/345099.345137
    title: Thomas Reps, Undecidability of context-sensitive data-dependence analysis, ACM Transactions on Programming Languages and Systems 22(1) (2000)
    locator: pp. 162 to 186 (reachability under two interleaved Dyck languages is undecidable)
---

CFL reachability asks, for a directed graph whose edges are labelled with terminal symbols and a [context-free grammar](/context-free-grammar/) $G$, which pairs of vertices are joined by a path whose sequence of labels is in $L(G)$. It generalizes both [graph reachability](/graph-reachability/), where every path counts, and context-free recognition, where the graph is a single path. A dynamic-programming algorithm that adds an edge $A(u, w)$ whenever $A \to BC$ and edges $B(u, v)$, $C(v, w)$ exist solves it in $O(|G| n^3)$ time, and it is the standard way to make program analyses match procedure calls with returns.

## In plain words

Take a map of one-way roads, with a letter on every road. A walk spells a word. Ordinary reachability asks whether one can walk from one place to another at all. CFL reachability asks whether one can walk there spelling a word of a given grammar.

The most common grammar is the one for balanced brackets. In a program, a call to a procedure is an opening bracket and the return to the caller is the matching closing bracket. A path that returns to a different caller than the one that called is impossible in a real run, and requiring balanced brackets removes exactly those paths.

The algorithm keeps a list of facts "this grammar symbol can be spelled from here to there" and combines two facts that meet at a vertex into a longer one, until nothing new appears.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. Here $n$ is the number of vertices of the graph; when the graph is a path labelled with a string, $n - 1$ is the length of that string.

**Input.** A directed graph $H = (N, E)$ with $|N| = n$ and edges $E \subseteq N \times \Sigma \times N$, and a context-free grammar $G$ over $\Sigma$.

**Output.** The set of pairs $(u, v)$ such that some path $u = v_0 \xrightarrow{a_1} v_1 \xrightarrow{a_2} \cdots \xrightarrow{a_k} v_k = v$ has $a_1 \cdots a_k \in L(G)$. The path may repeat vertices and edges, and $k = 0$ is allowed when $\varepsilon \in L(G)$.

When $L(G)$ is a [Dyck language](/dyck-language/) of $k$ kinds of brackets the problem is called *Dyck reachability*, $D_k$-reachability, or *realizable-path reachability* in program analysis.

## Variants

- **All pairs, single source, single pair.** The output is all pairs, all targets of one source, or a yes or no for one pair. The demand-driven versions explore less of the graph in practice but have the same cubic worst case.
- **All nonterminals.** Compute, for every nonterminal $A$, the relation $A(u, v)$ of pairs joined by a path spelling a string derivable from $A$. The algorithm below computes all of them at once.
- **Regular reachability.** If $L(G)$ is regular, given by an automaton with $q$ states, the problem is reachability in the product graph with $nq$ vertices, solvable in time linear in its size.
- **Bidirected Dyck reachability.** Every edge $u \xrightarrow{(_i} v$ has a reverse edge $v \xrightarrow{)_i} u$. The relation is then an equivalence relation, and Chatterjee, Choudhary and Pavlogiannis compute it in $O(m + n\,\alpha(n))$ time with [union-find](/disjoint-set/), for $m$ edges. Alias analyses often have this shape.
- **Interleaved Dyck reachability.** Require the labels to be balanced for two independent families of brackets, such as calls and returns together with field writes and reads. The path language is then the intersection of two context-free languages, and Reps showed that this reachability problem is undecidable, by the [undecidability of CFL intersection](/cfl-intersection-undecidable/).
- **Weighted and dataflow versions.** Edges carry functions or weights, and the answer is a combination over all valid paths. The IFDS framework of Reps, Horwitz and Sagiv reduces interprocedural finite distributive subset problems to Dyck reachability on an exploded graph.

## Examples

**Calls and returns.** A procedure $f$ with entry $f_0$ and exit $f_1$ is called from two sites. The first call goes from $a_0$ to $f_0$ and returns from $f_1$ to $a_1$, labelled $($ and $)$; the second goes from $b_0$ to $f_0$ and returns from $f_1$ to $b_1$, labelled $[$ and $]$. The body is an edge $f_0 \xrightarrow{e} f_1$. The grammar
$$S \to S S \mid ( S ) \mid [ S ] \mid e \mid \varepsilon$$
accepts the paths in which returns match calls. Ordinary reachability says $a_0$ reaches $b_1$, along the path $a_0\, f_0\, f_1\, b_1$ with labels $( e ]$. That path is not realizable, since the call from $a_0$ returns to $b_1$. CFL reachability finds the pairs $(v, v)$ for the six vertices, from $S \to \varepsilon$, then $S(f_0, f_1)$ from $S \to e$, and then $S(a_0, a_1)$ and $S(b_0, b_1)$ from the bracket productions, 9 pairs in all and not $(a_0, b_1)$. A script confirms the 9 pairs against enumeration of all paths of up to 6 edges.

**A path graph.** If the graph is the path $0 \xrightarrow{w_1} 1 \xrightarrow{w_2} \cdots \xrightarrow{w_\ell} \ell$, then $S(i, j)$ holds exactly when $S \Rightarrow^* w_{i+1} \cdots w_j$, which is the table of [CYK](/cyk-algorithm/) for $w$.

**Cycles.** On one vertex $v$ with loops labelled $($ and $)$, every string of brackets is the label of a path from $v$ to $v$, so $(v, v)$ is in the answer; the shortest witness is the empty path. Cycles are why the algorithm works with pairs of vertices and never enumerates paths.

## Known algorithms

- **Dynamic programming (worklist).** Bring $G$ into a form with right sides of length at most 2, by splitting longer right sides as in [Chomsky normal form conversion](/chomsky-normal-form-conversion/); unit and $\varepsilon$-productions may stay. Start with an edge $a(u, v)$ for each graph edge and $A(v, v)$ for each $A \to \varepsilon$ and vertex $v$. Take derived edges from a worklist: for $B(u, v)$, add $A(u, v)$ for each $A \to B$, add $A(u, w)$ for each $A \to B C$ and existing $C(v, w)$, and add $A(t, v)$ for each $A \to C B$ and existing $C(t, u)$. Each of the at most $|V| n^2$ derived edges is processed once, and each production that contains its symbol is combined with at most $n$ neighbours, so the time is $O(|G| n^3)$ and the space $O(|G| n^2)$. Keeping, for each edge, the two edges it came from gives a witness path. A script checks this algorithm on 600 random grammars and graphs, with $\varepsilon$-productions, unit productions and left recursion: every derived pair has a witness path whose label is in $L(G)$, and every pair found by enumerating paths of up to 7 edges is derived.
- **Subcubic.** Chaudhuri gives $O(n^3 / \log n)$ for a fixed grammar, by a [Four Russians](/four-russians-method/) style speed-up of the set operations.
- **Datalog.** The productions are the rules of a chain [Datalog](/datalog/) program, $A(u, w) \leftarrow B(u, v), C(v, w)$, and [semi-naive evaluation](/semi-naive-evaluation/) of that program is the worklist algorithm.
- **Pushdown systems.** Saturation algorithms for [pushdown reachability](/pushdown-reachability/) solve the same problem in another form, as described under Reductions.
- **Bidirected Dyck.** Union-find based algorithms, almost linear.

## Bounds

**Upper.** $O(|G| n^3)$ time in general, $O(n^3 / \log n)$ for a fixed grammar.

**Lower.** No truly subcubic algorithm is known, even for the one-bracket Dyck language $D_1$. Heintze and McAllester showed that the problem is complete for the class of languages recognized by two-way nondeterministic pushdown automata, for which no $O(n^{3 - \epsilon})$ recognition algorithm is known since the cubic algorithm of Aho, Hopcroft and Ullman in 1968. So a truly subcubic algorithm for CFL reachability would give one for these automata. Chatterjee, Choudhary and Pavlogiannis relate Dyck reachability on general graphs to [Boolean matrix multiplication](/boolean-matrix-multiplication/), so a fast combinatorial algorithm for it would give one for matrix multiplication.

**Special cases.** Linear time for regular languages after the product, and $O(m + n\,\alpha(n))$ for bidirected Dyck reachability. Interleaved Dyck reachability is undecidable.

## Reductions

- **From recognition.** A string $w$ is in $L(G)$ exactly when $S(0, |w|)$ holds on the path graph of $w$, so CFL reachability contains the [membership problem](/cfg-membership-problem/), and a reachability algorithm is a [chart parser](/chart-parsing/) for a graph.
- **From graph reachability.** With the grammar $S \to S a \mid \varepsilon$ for every label $a$, the answer is the [transitive closure](/transitive-closure/) of the graph.
- **To and from pushdown reachability.** A [pushdown system](/pushdown-system/) has configurations $(p, \gamma)$. The pairs $(p, q)$ such that it can go from $p$ with $X$ on the stack to $q$ with $X$ popped are the facts $[pXq]$ of the [triple construction](/cfg-pda-equivalence/), which form a CFL-reachability problem on the control states. Conversely a graph and a grammar give a pushdown system whose reachable configurations encode the answer.
- **Intersection with a regular language.** CFL reachability from $u$ to $v$ is non-emptiness of $L(G) \cap L(H_{u,v})$, where $H_{u,v}$ is the graph seen as an automaton with start $u$ and final state $v$. The [closure construction](/cfl-closure-properties/) for intersection with a regular language gives exactly the nonterminals $[uAv]$, and the reachability algorithm is the emptiness test on that grammar.
- **Set constraints.** Melski and Reps show that a class of set-constraint problems and CFL reachability can be converted into each other in linear time.

## Applications

- **Interprocedural dataflow analysis.** IFDS and its extensions find dataflow facts along realizable paths, where each call is matched with its return.
- **Alias and points-to analysis.** Field-sensitive analyses match writes and reads of the same field as brackets; context-sensitive ones match calls and returns; doing both exactly would need interleaved brackets, which is undecidable, so one of them is approximated.
- **Program slicing.** Summary edges of system dependence graphs are CFL-reachability facts, and they give precise interprocedural slices.
- **Type inference and flow analysis.** Polymorphic flow analyses and some type-based analyses reduce to Dyck reachability.
- **Graph databases.** Context-free path queries ask for pairs of nodes joined by a path in a context-free language, for example a chain of parent edges followed by the same number of child edges, to find nodes of the same generation.

## References
