---
tag: R5TC80
kind: algorithm
slug: hoffmann-odonnell-matching
name: Hoffmann-O'Donnell tree pattern matching
aliases:
- Hoffmann-O'Donnell algorithm
- bottom-up tree pattern matching
- match set automaton
area: automata-and-parsing/term-rewriting
level: research
summary: Compiles a set of tree patterns into a matching automaton for linear-time-per-node matching.
solves: [tree-pattern-matching]
model: word-ram
complexity:
  vars: {n: the size of the subject, F: the number of patterns, P: the number of distinct subpatterns, S: the number of match sets, q: the number of function symbols, r: the largest arity}
  time: {worst: O(q S^r r P + n^2 F), best: Θ(n + P)}
  space: {extra: O(q S^r + S P)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1982
  people: [Christoph M. Hoffmann, Michael J. O'Donnell]
  note: Hoffmann and O'Donnell gave bottom-up and top-down matchers for a fixed set of tree patterns in the Journal of the ACM in 1982; Chase made the bottom-up tables much smaller in 1987.
prereqs: [tree-pattern-matching, term-matching, linearity, subset-construction]
see_also: [discrimination-tree, aho-corasick, deterministic-finite-automaton, innermost-reduction, term-rewriting-system, lr-parsing, term-graph-rewriting, ac-matching]
sources:
  - paper: doi:10.1145/322290.322295
    title: Christoph M. Hoffmann and Michael J. O'Donnell, Pattern matching in trees, Journal of the ACM 29(1) (1982)
    locator: pp. 68 to 95 (pattern forests, match sets, the bottom-up table construction, simple pattern forests, and a top-down matcher based on path strings)
  - paper: doi:10.1145/41625.41640
    title: David R. Chase, An improvement to bottom-up tree pattern matching, 14th ACM Symposium on Principles of Programming Languages (POPL), 1987
    locator: pp. 168 to 177 (tables indexed by equivalence classes of match sets for each argument place, with costs close to those of LALR parser generators)
  - paper: doi:10.1145/69558.75700
    title: Alfred V. Aho, Mahadevan Ganapathi and Steven W. K. Tjiang, Code generation using tree matching and dynamic programming, ACM Transactions on Programming Languages and Systems 11(4) (1989)
    locator: pp. 491 to 516 (the twig code generator generator, which uses top-down tree pattern matching with an Aho-Corasick automaton and dynamic programming)
---

The **Hoffmann-O'Donnell** algorithm solves [tree pattern matching](/tree-pattern-matching/) for a fixed set of patterns: find every pair of a position in a subject term and a pattern that [matches](/term-matching/) the subterm there. It compiles the patterns once into a deterministic bottom-up tree automaton. Each state is a **match set**, the set of subpatterns that match a node, and a table for each function symbol gives the state of a node from the states of its children. Matching a subject of $n$ nodes is then one table lookup for each node, independent of the number of patterns. The price is in the preprocessing: the number of match sets can be exponential in the size of the patterns. The method is used in rewriting engines and in code generator generators for instruction selection.

## In plain words

Suppose you have a fixed list of tree shapes and you want to find every place in a big tree where one of the shapes fits. You could try every shape at every node, but that repeats work.

Instead, look at the small pieces of all the shapes. For any node of the big tree, the set of pieces that fit there depends only on the label of the node and on the sets of pieces that fit at its children. So before you see any big tree, make a table: for each label and each combination of child sets, write down the set for the parent. Then walk the big tree from the leaves up, and at each node look up its set in the table. If a whole shape is in the set, that shape fits at that node.

## The problem

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, rules $l \to r$, $\to^*$ for the reflexive transitive closure, positions as sequences of positive integers, $t|_p$ for the subterm of $t$ at position $p$, and substitutions $\sigma$. A pattern $l$ **matches** a term $u$ if $l\sigma = u$ for some $\sigma$; the variables of the subject are treated as constants.

**Input.** Patterns $p_1, \ldots, p_F \in T(\Sigma, V)$, known in advance, and then any number of subject terms $t$.

**Output.** For each subject $t$, the set of pairs $(p, j)$ such that $p_j$ matches $t|_p$.

A [term rewriting system](/term-rewriting-system/) needs this at each step: the patterns are the left sides of the rules, and a redex is a pair $(p, j)$. The classical setting is linear patterns, where no variable occurs twice (see [linearity](/linearity/)). The automaton treats every pattern as linear; for a non-linear pattern a final check compares the subterms that its repeated variables take.

## The algorithm

Write $v$ for a wildcard symbol, and $\bar l$ for $l$ with each variable replaced by $v$. The **pattern forest** $PF$ is the set of all $\bar q$ for subterms $q$ of the patterns, plus $v$. A member $w$ of $PF$ **fits** a subject node $u$ if $w = v$, or $w = f(w_1, \ldots, w_k)$ and $u = f(u_1, \ldots, u_k)$ with each $w_i$ fitting $u_i$. The **match set** of $u$ is $MS(u) = \{ w \in PF : w \text{ fits } u \}$. The key fact is that it is computed locally:

$$MS(f(u_1, \ldots, u_k)) = \delta_f(MS(u_1), \ldots, MS(u_k)) = \{v\} \cup \{ f(w_1, \ldots, w_k) \in PF : w_i \in MS(u_i) \}.$$

Preprocessing closes the set of states under the functions $\delta_f$ and stores them as tables. Matching evaluates the tables bottom-up, as a [deterministic](/deterministic-finite-automaton/) tree automaton does. Like the [subset construction](/subset-construction/), the states are sets, and only the reachable ones are built.

```pseudo id=main
HO-PREPROCESS(p_1, …, p_F)
L1  PF ← {v} ∪ {q̄ : q is a subterm of some p_j}                ▷ variables become v
L2  S ← [{v}]; each table T_f is empty, for each symbol f/k at the root of a member of PF
L3  repeat
L4      for each f/k and each tuple (M_1, …, M_k) ∈ S^k with no entry in T_f do
L5          M ← {v} ∪ {f(w_1, …, w_k) ∈ PF : w_i ∈ M_i for i = 1, …, k}
L6          T_f[M_1, …, M_k] ← M; if M ∉ S then add M to S
    until no table changed in the last round
L7  for each M ∈ S do report(M) ← {j : p̄_j ∈ M}

HO-MATCH(t)
L8  for each node u of t, children before parents do
L9      if u is a variable or no table T_f exists for its symbol f/k then state(u) ← {v}
L10     else state(u) ← T_f[state(u_1), …, state(u_k)]          ▷ u = f(u_1, …, u_k)
L11     for each j ∈ report(state(u)) do
L12         if p_j is linear or MATCH(p_j, u) ≠ FAIL then output (position of u, j)
L13 return the output
```

Line L5 computes $\delta_f$. Line L6 adds new states, and the loop repeats until every tuple of states has an entry. Line L7 records which whole patterns each state contains. In the matching phase, a node whose symbol is in no pattern can fit only $v$ (line L9). Line L12 is the check for non-linear patterns; for linear patterns line L11 is already exact.

## Example

Take the two linear patterns $p_1 = f(a, x)$ and $p_2 = f(x, g(a))$, over $f/2$, $g/1$ and $a/0$. The pattern forest is $PF = \{ v, a, g(a), f(a, v), f(v, g(a)) \}$. The preprocessing finds six states.

| state | match set | reports |
|---|---|---|
| $S_0$ | $\{v\}$ | none |
| $S_1$ | $\{v, a\}$ | none |
| $S_2$ | $\{v, f(a, v)\}$ | $p_1$ |
| $S_3$ | $\{v, g(a)\}$ | none |
| $S_4$ | $\{v, f(v, g(a))\}$ | $p_2$ |
| $S_5$ | $\{v, f(a, v), f(v, g(a))\}$ | $p_1$, $p_2$ |

The tables follow from line L5. $T_a = S_1$. $T_g[S_1] = S_3$, and $T_g[M] = S_0$ for the five other states. For $f$, the member $f(a, v)$ is in the result iff $a \in M_1$, that is $M_1 = S_1$, and $f(v, g(a))$ is in it iff $g(a) \in M_2$, that is $M_2 = S_3$. So $T_f[S_1, S_3] = S_5$, $T_f[S_1, M] = S_2$ for $M \ne S_3$, $T_f[M, S_3] = S_4$ for $M \ne S_1$, and $T_f[M_1, M_2] = S_0$ otherwise: 36 entries in all.

Match the subject $t = f(f(a, b), g(a))$. The constant $b$ is in no pattern.

| node | position | children's states | state | output |
|---|---|---|---|---|
| $a$ | $1.1$ | none | $S_1$ | |
| $b$ | $1.2$ | none | $S_0$ (line L9) | |
| $f(a, b)$ | $1$ | $S_1, S_0$ | $S_2$ | $(1, p_1)$ |
| $a$ | $2.1$ | none | $S_1$ | |
| $g(a)$ | $2$ | $S_1$ | $S_3$ | |
| $f(f(a, b), g(a))$ | $\varepsilon$ | $S_2, S_3$ | $S_4$ | $(\varepsilon, p_2)$ |

So $p_1$ matches at position 1 and $p_2$ at the root, and nothing else matches. For the subject $f(a, g(a))$ the root gets $S_5$, and both patterns match there.

**Exponential growth.** For the $k$ patterns $h(a, x_2, \ldots, x_k)$, $h(x_1, a, x_3, \ldots, x_k)$, …, each with $a$ at one place, a node $h(c_1, \ldots, c_k)$ with $c_i \in \{a, b\}$ matches exactly the patterns $i$ with $c_i = a$. Every subset occurs, so there are $2^k + 1$ states, and the table $T_h$ has $(2^k + 1)^k$ entries.

## Correctness

Three facts give the result. First, $\bar l$ fits $u$ iff $l$ with its variable occurrences renamed apart matches $u$, by induction on $l$: the arguments of a linear pattern have disjoint variables, so their matchers combine. Second, the match set of a node is $\delta_f$ of the match sets of its children, by the definition of fitting. Third, the preprocessing stops, since the states are subsets of $PF$, and when it stops every tuple of states has a table entry. By induction on the height of a node, line L10 then gives every node its match set. A pattern is offered at a node iff its linear form matches there, and line L12 removes exactly the non-linear candidates that do not match. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $P = |PF|$, $S$ the number of states, $q$ the number of function symbols, and $r$ the largest arity.

**Preprocessing.** There are $\sum_f S^{k_f} \le q S^r$ table entries. Each one costs $O(r P)$ at line L5 in the simple form above (each member of $PF$ with root $f$ checks $k$ memberships), so the time is $O(q S^r r P)$ and the tables take $O(q S^r)$ words. Since $S \le 2^P$, this is exponential in the worst case, and the example above shows that $S$ can indeed be about $2^F$. Hoffmann and O'Donnell show that for pattern sets they call simple, the match sets are much fewer, and the tables are small.

**Matching.** Each node costs one table lookup on a tuple of its children's states, so the lookups take $\Theta(n)$ time in total. Reporting costs $O(1)$ for each pattern listed in a state, at most $F$ for each node. For linear patterns the matching phase is $O(n + n F)$, and $O(n)$ plus the size of the output when the states list their patterns in a compact way. For a non-linear pattern, line L12 costs $O(|u|)$ at node $u$, so $O(n^2 F)$ in the worst case.

**Compared with naive matching.** Trying all $F$ patterns at all $n$ nodes costs up to $\Theta(n \sum_j |p_j|)$. The automaton replaces this by $\Theta(n)$ lookups, at the cost of the preprocessing, so it pays off when the same patterns are used on many subjects, as in a rewriting engine or a code generator.

## Properties

- **Deterministic.** Each node has one state, and the matching phase does no backtracking.
- **Not recursive.** The implementation computes the states with an explicit stack, children before parents, so deep subjects are safe.
- **Offline in the patterns.** The patterns must be known before matching; adding a pattern means a new preprocessing.
- **Bottom-up and incremental.** A node's state depends only on its subtree. After a rewrite step, only the states on the path from the changed subterm to the root change.

## Variants and improvements

- **Chase's table compression.** For each symbol $f$ and argument place $i$, only the members of $PF$ that occur as an $i$-th argument of an $f$-pattern matter. Chase (1987) indexes the tables by the classes of states that agree on these members, which reduces the tables by orders of magnitude, to costs comparable with those of LALR parser generators.
- **Top-down matching.** Hoffmann and O'Donnell also give a top-down method: each pattern is cut into its root-to-leaf path strings, the strings are matched with an [Aho-Corasick](/aho-corasick/) automaton during a walk of the subject, and a counter at each node checks that all paths of a pattern were found. The twig generator of Aho, Ganapathi and Tjiang uses this method.
- **BURS and code generation.** Bottom-up rewrite systems extend the states with costs, so that a code generator chooses a cheapest cover of an expression tree by machine instruction patterns. Tools in the iburg family compute these costs at matching time with dynamic programming.
- **Indexes for changing pattern sets.** When rules are added and removed often, as in completion, a [discrimination tree](/discrimination-tree/) is easier to update than a compiled automaton.
- **Non-linear patterns.** Line L12 handles them by a check. Tree automata with equality constraints between brothers decide them inside the automaton, at a higher cost.

## When to use it

Use it when a fixed set of patterns is matched against many large subjects: the left sides of a fixed rewrite system, instruction patterns in a compiler back end, or tree transformations. The matching cost is then one lookup per node, whatever the number of patterns. Do not use it when the pattern set changes often, or when it has many patterns with independent constant places, which make the number of states explode; a [discrimination tree](/discrimination-tree/) or a direct matcher is better there.

## Pitfalls

- **Exponential tables.** The number of match sets can be $2^F$ or more, and a table for a symbol of arity $k$ has $S^k$ entries. Build only reachable states, and use Chase's compression for large pattern sets.
- **Symbols that are not in the patterns.** A subject can have symbols that no pattern uses. They must get the state $\{v\}$ (line L9), not a table error.
- **Arity.** The same name with two arities, such as $f(a)$ and $f(a, b)$, must be two symbols with two tables.
- **Non-linear patterns.** The wildcard forgets equalities, so $f(x, x)$ is offered at $f(a, b)$. Without the check of line L12, a rewriting engine would apply a rule where it does not match.
- **Deep subjects.** A recursive bottom-up pass overflows the Python stack on terms of depth in the thousands, such as unary numbers. The implementation uses an explicit stack.

## Implementations

## History

Hoffmann and O'Donnell published "Pattern matching in trees" in the Journal of the ACM in 1982. They studied matching for the implementation of equational programs, defined pattern forests and match sets, gave the bottom-up table method and a top-down method based on path strings, and identified the simple pattern forests, for which the tables stay small. Chase (1987) made the bottom-up table construction practical for large pattern sets. The top-down method became the core of the twig code generator generator of Aho, Ganapathi and Tjiang (1989), and the bottom-up method, with costs added, became the basis of BURS code generators.

## References
