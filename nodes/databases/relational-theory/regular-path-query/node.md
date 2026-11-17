---
tag: 3RG9NX
kind: problem
slug: regular-path-query
name: Regular path query evaluation
aliases:
- RPQ
- regular path query
area: databases/relational-theory
level: advanced
summary: Find the pairs of nodes of an edge-labeled graph that are joined by a path whose labels spell a word of a given regular language.
prereqs: [nondeterministic-finite-automaton, graph-reachability, product-construction]
see_also: [datalog, transitive-closure, breadth-first-search, thompson-construction, nondeterministic-logspace, vertex-disjoint-paths, conjunctive-query, data-and-combined-complexity]
sources:
  - paper: doi:10.1137/S009753979122370X
    title: Alberto O. Mendelzon and Peter T. Wood, Finding regular simple paths in graph databases, SIAM Journal on Computing 24(6), 1235 to 1258 (1995)
    locator: polynomial evaluation under arbitrary paths, NP-completeness under simple paths for fixed regular languages, and polynomial cases
  - paper: doi:10.1145/38713.38749
    title: Isabel F. Cruz, Alberto O. Mendelzon and Peter T. Wood, A graphical query language supporting recursion, Proceedings of the ACM SIGMOD International Conference on Management of Data, 323 to 330 (1987)
    locator: the graph query language G, whose query graphs have edges labeled by regular expressions
  - paper: doi:10.1145/2463664.2467795
    title: Guillaume Bagan, Angela Bonifati and Benoit Groz, A trichotomy for regular simple path queries on graphs, Proceedings of the 32nd ACM Symposium on Principles of Database Systems (PODS), 261 to 272 (2013)
    locator: for each fixed regular language, simple path evaluation is in AC0, NL-complete or NP-complete
  - paper: "Steven Fortune, John Hopcroft and James Wyllie, The directed subgraph homeomorphism problem, Theoretical Computer Science 10(2), 111 to 121 (1980)"
    locator: two node-disjoint paths between given pairs in a directed graph is NP-complete
  - paper: doi:10.1145/3104031
    title: Renzo Angles, Marcelo Arenas, Pablo Barcelo, Aidan Hogan, Juan Reutter and Domagoj Vrgoc, Foundations of modern query languages for graph databases, ACM Computing Surveys 50(5), article 68 (2017)
    locator: path queries, their semantics (arbitrary paths, simple paths, trails) and conjunctive regular path queries
---

Regular path query evaluation is the problem of finding the pairs of nodes of an edge-labeled graph that are joined by a path whose labels, read in order, spell a word of a given regular language. It is the basic query of graph databases: "all pairs of people joined by a chain of knows edges" is the query $\mathit{knows}^{+}$. When any path counts, the problem reduces to reachability in the product of the graph and an automaton for the language, so it is solved in time linear in the graph for each source node. When the path must be simple, the problem is NP-complete already for some fixed languages (Mendelzon and Wood 1995).

## In plain words

Think of a graph as a map of places joined by roads, and give each road a label, such as "train" or "bus". A regular path query asks: from which place to which place can you travel so that the list of road labels follows a pattern? A pattern could be "any number of train rides, then one bus ride".

To answer it, you walk through the graph and through a small machine that reads the pattern at the same time. Each step uses one road and moves the machine by that road's label. You reach an answer when the machine says the pattern is complete. This is fast. The problem becomes hard when you also ask that the trip never visits the same place twice.

## Definition

**Input.** An edge-labeled graph $G = (V, E)$ over a finite alphabet $\Sigma$, with $E \subseteq V \times \Sigma \times V$; and a regular language $L \subseteq \Sigma^{*}$, given by a [regular expression](/regular-expression/) $r$ or by a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) $A = (S, \Sigma, \delta, s_0, F)$ with $\delta \subseteq S \times (\Sigma \cup \{\varepsilon\}) \times S$. The size of $A$ is $|A| = |S| + |\delta|$.

A *path* from $u$ to $v$ is a sequence of edges $(v_0, a_1, v_1), (v_1, a_2, v_2), \ldots, (v_{n-1}, a_n, v_n)$ in $E$ with $v_0 = u$ and $v_n = v$, for some $n \geq 0$. Its label is the word $a_1 a_2 \cdots a_n$; the empty path has the empty word as label. The path is *simple* if $v_0, \ldots, v_n$ are distinct.

**Output.** The answer of the query $L$ on $G$ is

$$L(G) = \{\, (u, v) \in V \times V \mid \text{some path from } u \text{ to } v \text{ has its label in } L \,\}.$$

Under *simple path semantics*, only simple paths count. The decision versions ask whether a given pair $(u, v)$ is in the answer.

The answer is a binary relation over $V$, so a regular path query is a query in the sense of the relational model: the graph is a database with one binary relation $E_a$ per label $a$, and $L(G)$ is a relation computed from it. For the query $a^{*}$ the answer is the reflexive and [transitive closure](/transitive-closure/) of $E_a$, which relational algebra cannot express; so regular path queries are outside the [relational calculus](/relational-calculus/) but inside [Datalog](/datalog/).

## Variants

- **Single source, single pair, all pairs.** Fix $u$ and return all $v$; fix both and decide; or return the whole relation. The all-pairs answer can have $|V|^2$ pairs.
- **Two-way RPQs (2RPQs).** The alphabet also has an inverse label $a^{-}$ for each $a$, read along an $a$-edge from its head to its tail. Add the reversed edges to $E$ and the problem becomes an ordinary RPQ.
- **Conjunctive RPQs (CRPQs).** A [conjunctive query](/conjunctive-query/) whose atoms are RPQs, such as $\exists z\, (x \xrightarrow{a^{+}} z \land y \xrightarrow{b} z)$. This adds the joins of conjunctive queries, and combined complexity becomes NP-complete, as for conjunctive queries.
- **Path semantics.** Arbitrary paths (walks), *trails* (no repeated edge) and simple paths (no repeated node). The query languages of graph systems choose among these.
- **Returning paths.** Return one witness path per pair, a shortest one, or all paths up to a bound. Under arbitrary path semantics there can be infinitely many paths, so systems return a finite selection.

## Examples

Take nodes $1, 2, 3, 4$ and the five edges

$$1 \xrightarrow{a} 2,\quad 2 \xrightarrow{b} 3,\quad 3 \xrightarrow{a} 4,\quad 4 \xrightarrow{b} 1,\quad 2 \xrightarrow{a} 4,$$

and the language $L = (ab)^{+}$, with the automaton of three states: $s_0 \xrightarrow{a} s_1$, $s_1 \xrightarrow{b} s_2$, $s_2 \xrightarrow{a} s_1$, and $F = \{s_2\}$.

- **Arbitrary paths.** From node 1, the path $1, 2, 3$ has label $ab$, so $(1, 3)$ is an answer. The path $1, 2, 3, 4, 1$ has label $abab$, so $(1, 1)$ is an answer. A [breadth-first search](/breadth-first-search/) of the product from $(1, s_0)$ visits $(1, s_0), (2, s_1), (3, s_2), (4, s_1), (1, s_2)$ and stops; the visited pairs with state $s_2$ give the answers $3$ and $1$. From nodes 2 and 3 the answers are also $\{1, 3\}$, and from node 4 there are none, since node 4 has no $a$-edge. So $L(G) = \{1, 2, 3\} \times \{1, 3\}$, six pairs.
- **Simple paths.** From node 1, the path $1, 2, 3$ is simple and gives $(1, 3)$. The only path from 1 to 1 with a label in $L$ is $1, 2, 3, 4, 1$ or longer, and each of them repeats node 1. So under simple path semantics the answers from node 1 are $\{3\}$, not $\{1, 3\}$.
- **Product size.** The product has at most $4 \cdot 3 = 12$ nodes, and its edges are the pairs of a graph edge and a transition with the same label: 8 edges here, against the bound $|E| \cdot |\delta| = 5 \cdot 3 = 15$.

## Known algorithms

**Product construction.** Build the product graph $P = G \times A$. Its nodes are the pairs $(v, s)$ with $v \in V$ and $s \in S$. It has an edge $(v, s) \to (w, s')$ for each edge $(v, a, w) \in E$ and transition $(s, a, s') \in \delta$ with the same label $a$, and an edge $(v, s) \to (v, s')$ for each $\varepsilon$-transition $(s, \varepsilon, s')$.

*Claim.* $(u, v) \in L(G)$ if and only if some $(v, f)$ with $f \in F$ is reachable from $(u, s_0)$ in $P$.

*Proof.* A path in $P$ from $(u, s_0)$ to $(v, f)$ projects on its first component to a path of $G$ from $u$ to $v$ (the $\varepsilon$-steps stay at one node), and on its second component to a run of $A$ that reads the label of that path and ends in $f$; so the label is in $L$. Conversely, a path of $G$ from $u$ to $v$ with label $w \in L$ and an accepting run of $A$ on $w$ combine, step by step, into a path of $P$ from $(u, s_0)$ to an accepting pair $(v, f)$. $\square$

**Algorithm (single source).** Store the out-edges of each node grouped by label, and the transitions of each state grouped by label. Run a breadth-first or depth-first search on $P$ from $(u, s_0)$, building the edges of $P$ on the fly: at a pair $(v, s)$, for each out-edge $(v, a, w)$, look up the $a$-transitions of $s$, and also follow the $\varepsilon$-transitions of $s$. Output each $v$ such that some visited pair $(v, f)$ has $f \in F$.

*Running time.* The search visits each pair at most once, so at most $|V| \cdot |S|$ pairs. At a pair $(v, s)$ it scans the out-edges of $v$ and, for each edge with label $a$, the $a$-transitions of $s$; it also scans the $\varepsilon$-transitions of $s$. Summed over all $v$ and $s$, the scans of edges cost $|E| \cdot |S|$, the matched pairs cost $\sum_{a} |E_a| \cdot |\delta_a| \leq |E| \cdot |\delta|$, where $E_a$ and $\delta_a$ are the edges and transitions with label $a$, and the $\varepsilon$-scans cost $|V| \cdot |\delta|$. The total is

$$O\big(|V| \cdot |S| + |E| \cdot |S| + |E| \cdot |\delta| + |V| \cdot |\delta|\big) = O\big((|V| + |E|) \cdot |A|\big)$$

for one source. This is $O(|E| \cdot |A|)$ when every node has an edge. All pairs follow by one search per source, in time $O(|V| \cdot (|V| + |E|) \cdot |A|)$. From a regular expression $r$, the [Thompson construction](/thompson-construction/) gives an automaton with $|A| = O(|r|)$, so the bounds hold with $|r|$ in place of $|A|$.

**Datalog.** The same product is a linear [Datalog](/datalog/) program with one binary predicate $P_s$ per state: $P_{s_0}(x, x)$ for each node $x$, the rule $P_{s'}(x, z) \leftarrow P_s(x, y), E_a(y, z)$ for each transition $(s, a, s')$, and $\mathit{Ans}(x, y) \leftarrow P_f(x, y)$ for $f \in F$. Semi-naive evaluation of this program computes the all-pairs answer.

**Simple paths.** For simple path semantics no polynomial algorithm is known in general. A search over the simple paths of $G$, pruned by the automaton state, is exponential in the worst case. Mendelzon and Wood (1995) gave polynomial cases, among them graphs without cycles, where every path is simple and the product algorithm applies.

## Bounds

- **Arbitrary paths.** $O((|V| + |E|) \cdot |A|)$ time for one source, by the product search above. The decision problem is in NL in combined complexity: guess the path in $P$ one step at a time, storing only the current pair $(v, s)$ in $O(\log |V| + \log |S|)$ bits. It is NL-hard already in data complexity, for the fixed query $a^{*}$, which is directed [graph reachability](/graph-reachability/). So it is NL-complete in data and in combined complexity (see [NL](/nondeterministic-logspace/)).
- **Simple paths.** NP-complete for some fixed languages, so in data complexity (Mendelzon and Wood 1995). Membership in NP holds because a simple path has at most $|V| - 1$ edges and is a certificate. Bagan, Bonifati and Groz (2013) showed a trichotomy: for each fixed regular language, the simple path problem is in AC0, NL-complete or NP-complete.
- **Containment.** Query $L_1$ is contained in $L_2$ on every graph if and only if $L_1 \subseteq L_2$: if $w \in L_1 \setminus L_2$, the graph that is a single path labeled $w$ separates them, since its only path from the first to the last node has label $w$. So containment of RPQs given by regular expressions is PSPACE-complete, as language containment is (see [regex equivalence](/regex-equivalence-pspace-completeness/)).

## Reductions

- **Reachability to RPQ.** Label every edge $a$; then $(u, v)$ is in the answer of $a^{*}$ if and only if $v$ is reachable from $u$. This gives the NL lower bound.
- **RPQ to reachability.** The product construction above, computable in logarithmic space.
- **Two disjoint paths to simple RPQ.** The problem "given a directed graph $H$ and distinct nodes $s_1, t_1, s_2, t_2$, are there node-disjoint paths from $s_1$ to $t_1$ and from $s_2$ to $t_2$?" is NP-complete (Fortune, Hopcroft and Wyllie 1980; see [vertex-disjoint paths](/vertex-disjoint-paths/)). Build $G$ from $H$: label every edge of $H$ with $a$, and add one new edge $t_1 \xrightarrow{b} s_2$. Ask whether $G$ has a simple path from $s_1$ to $t_2$ with a label in $a^{*} b a^{*}$. Such a path uses the only $b$-edge once, so it is a path of $H$ from $s_1$ to $t_1$, the edge to $s_2$, and a path of $H$ from $s_2$ to $t_2$; it is simple exactly when the two parts share no node. So the answer is yes if and only if the disjoint paths exist, and the simple path problem for the fixed language $a^{*} b a^{*}$ is NP-hard.
- **CQ to CRPQ.** A conjunctive query over binary relations is a CRPQ whose regular expressions are single labels, so NP-hardness of CQ evaluation in combined complexity carries over to CRPQs.

## Applications

- **Graph query languages.** Cruz, Mendelzon and Wood (1987) introduced the language G, whose query graphs have edges labeled by regular expressions; RPQs are its core. SPARQL property paths, Cypher variable-length patterns and the path patterns of GQL are RPQs or extensions of them, and they differ mainly in the path semantics: arbitrary paths, trails or simple paths.
- **Recursive queries in relational systems.** A recursive SQL query over an edge table that follows a label pattern is an RPQ, evaluated by the Datalog program above.
- **Semistructured data and knowledge graphs.** Queries such as "all subclasses of a class, at any depth" are RPQs of the form $\mathit{subClassOf}^{*}$ (survey by Angles et al. 2017).
- **Program analysis.** Reachability with a regular pattern over a graph of a program, such as a call graph with labeled edges, is an RPQ; the product with an automaton is the same construction.

## References
