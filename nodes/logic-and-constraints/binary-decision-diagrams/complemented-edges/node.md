---
tag: 30J7RA
kind: concept
slug: complemented-edges
name: Complemented edges
aliases:
- complement edges
- attributed edges
- negative edges
- negation attribute
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: Store negation on edges so that f and its complement share one node, roughly halving size.
prereqs: [reduced-ordered-bdd, bdd-canonicity, ite-operator]
see_also: [ite-operator, computed-table, bdd-canonicity, reduced-ordered-bdd, bdd-apply, bdd-satisfy-count, boolean-equivalence-checking, decision-diagram]
sources:
  - paper: doi:10.1109/DAC.1990.114826
    title: Karl S. Brace, Richard L. Rudell and Randal E. Bryant, Efficient implementation of a BDD package, Proceedings of the 27th ACM/IEEE Design Automation Conference, 1990, pages 40 to 45
    locator: Section 5.1 (complement edges, the rule that the then edge of every node is regular, one terminal 1, and the measured savings) and Section 5.2 (standard triples, and the four equivalent forms of an ITE call)
  - paper: doi:10.1145/123186.123225
    title: Shin-ichi Minato, Nagisa Ishiura and Shuzo Yajima, Shared binary decision diagram with attributed edges for efficient Boolean function manipulation, Proceedings of the 27th ACM/IEEE Design Automation Conference, 1990, pages 52 to 57
    locator: the negation attribute on edges and the restriction on its use that keeps the shared graph canonical
---

A complemented edge is an edge of a BDD with one extra bit that says "negate the function below". With such edges, $f$ and $\neg f$ are the same node reached through edges with different bits, so negation takes $O(1)$ time and a test of $f = \neg g$ is one comparison. To keep the form canonical, a rule fixes where the bits may be: in the convention of Brace, Rudell and Bryant (1990), the then-edge of every node is regular, and the only terminal is 1. Under this rule each function has exactly one edge, and the number of nodes is at least half of the number in a plain [reduced ordered BDD](/reduced-ordered-bdd/) and at most that number.

## In plain words

In a plain diagram, the answer "no" and the answer "yes" are two separate end boxes. A question and its opposite are drawn as two separate diagrams, even though one is the other with the ends swapped. Complemented edges add a small mark to an arrow. The mark means "swap yes and no for everything below this arrow". Now a question and its opposite share one drawing, and turning a question into its opposite only flips one mark. The diagram also gets smaller when many parts below are opposites of each other. A fixed rule says where marks are allowed, so each question still has exactly one drawing.

## The idea

**Representation.** An edge is a pair $(u, c)$ of a node $u$ and a bit $c$. It is regular if $c = 0$ and complemented if $c = 1$, and its function is $f_{(u,c)} = f_u$ if $c = 0$ and $\neg f_u$ if $c = 1$. There is one terminal node, whose function is $1$; the constant $0$ is the complemented edge to it. An inner node is $u = (i, e_0, e_1)$ with
$$f_u = (\neg x_i \wedge f_{e_0}) \vee (x_i \wedge f_{e_1}).$$
The bit is usually stored in the low bit of the pointer, so it costs no memory.

**The rule.** Without a rule the form is not canonical, because $(\neg x_i \wedge a) \vee (x_i \wedge b) = \neg\big((\neg x_i \wedge \neg a) \vee (x_i \wedge \neg b)\big)$: the same function has the node $(i, a, b)$ under a regular edge and the node $(i, \neg a, \neg b)$ under a complemented edge. A store with complemented edges is canonical if:

1. no node has $e_0 = e_1$,
2. each child of a node at level $i$ has a level larger than $i$,
3. the unique table holds at most one node per triple $(i, e_0, e_1)$,
4. the then-edge $e_1$ of every node is regular.

The node constructor enforces rule 4 by moving the bit to the edge above:

- MK$(i, e_0, e_1)$: if $e_0 = e_1$, return $e_0$. If $e_1$ is complemented, return the complement of MK$(i, \neg e_0, \neg e_1)$. Otherwise return the regular edge to the unique node $(i, e_0, e_1)$.

By the identity above, the edge that MK returns has the function $(\neg x_i \wedge f_{e_0}) \vee (x_i \wedge f_{e_1})$.

**Lemma 1.** Under rule 4, every node $u$ satisfies $f_u(1, \ldots, 1) = 1$.

*Proof.* By induction from the bottom. The terminal has the function $1$. For $u = (i, e_0, e_1)$, at the input of all ones $f_u$ follows the then-edge, so $f_u(1, \ldots, 1) = f_{e_1}(1, \ldots, 1)$. The edge $e_1$ is regular, so this is $f_v(1, \ldots, 1)$ for its node $v$, which is $1$ by induction. $\square$

So the bit of an edge for a function $h$ is forced: $c = 0$ if $h(1, \ldots, 1) = 1$ and $c = 1$ otherwise. The node of the edge has the function $\mathrm{norm}(h)$, which is $h$ or $\neg h$, the one with value 1 at the input of all ones.

**Theorem (canonicity).** In a store that obeys rules 1 to 4, two edges with the same function are the same edge.

*Proof.* We show by downward induction on $k$ the claim $P(k)$: two edges whose nodes have levels at least $k$ and that have the same function are equal, and the function of each inner node at a level $j \geq k$ depends on $x_j$ and on no $x_m$ with $m < j$. The terminal has level $n + 1$. $P(n + 1)$ holds, since the only edges are the two edges to the terminal, with the functions $1$ and $0$.

Assume $P(k + 1)$. Let $u = (k, e_0, e_1)$ be an inner node at level $k$. Its children have levels larger than $k$, so by $P(k + 1)$ and rule 1 their functions differ. These functions do not depend on $x_1, \ldots, x_k$, so $f_u$ depends on $x_k$ and on no earlier variable. Now let $e = (u, c)$ and $e' = (u', c')$ be edges at levels at least $k$ with $f_e = f_{e'}$. By Lemma 1, $c = c'$, so $f_u = f_{u'}$. If this function is constant, both nodes are the terminal, since an inner node depends on its variable. Otherwise both are inner nodes, and their level is the smallest index of a variable that $f_u$ depends on, so they have the same level $i$. Their cofactors by $x_i = 0$ give $f_{e_0} = f_{e'_0}$, and by $x_i = 1$ give $f_{e_1} = f_{e'_1}$. By $P(i + 1)$ the children are equal edges, so the triples are equal, and by rule 3, $u = u'$. $\blacksquare$

Every function has an edge, since MK keeps rules 1 to 4 and the BDD of any function can be built bottom up with MK. So a test of $f = g$ is one comparison of edges, and a test of $f = \neg g$ is one comparison of nodes and bits.

**Theorem (size).** Let $P$ be the number of inner nodes of the plain reduced ordered BDD of $f$, and $C$ the number of inner nodes reachable from the edge of $f$ with complemented edges. Then $C \leq P \leq 2C$.

*Proof.* Let $S$ be the set of the distinct non-constant subfunctions $f|_\alpha$, where $\alpha$ sets $x_1, \ldots, x_j$ for some $j$. By the [canonicity theorem](/bdd-canonicity/), the inner nodes of the plain BDD are in one-to-one correspondence with $S$. In the graph with complemented edges, the edge reached from the root edge along the path of $\alpha$ has the function $f|_\alpha$, and every reachable edge is reached in this way. So the reachable inner nodes are the nodes of the edges of the functions in $S$, and the node of the edge of $h$ is the node of $\mathrm{norm}(h)$. By canonicity, two nodes with different functions are different, so $C$ is the number of distinct values of $\mathrm{norm}$ on $S$. The map $\mathrm{norm}$ sends at most two functions, $h$ and $\neg h$, to one value. So $C \leq |S| = P \leq 2C$. $\square$

The plain BDD of a non-constant function also has two terminals, and the one with complemented edges has one. So the saving is at most a factor of 2. Brace, Rudell and Bryant report that on their 12 test circuits the final graph was 7% smaller, but the run time fell by almost a factor of 2, mostly because negation takes constant time.

**Operations.** Each operation must take the bit into account.

- **Negation** flips the bit of the edge: $O(1)$ time and no new nodes.
- **Cofactors.** The cofactors of the edge $(u, c)$ with $u = (i, e_0, e_1)$ are $e_0$ and $e_1$ with their bits flipped when $c = 1$. Forgetting to pass the bit down gives the cofactors of $\neg f$ in place of those of $f$.
- **ITE.** The [ITE operator](/ite-operator/) uses the identities $\mathrm{ite}(f, g, h) = \mathrm{ite}(\neg f, h, g) = \neg\,\mathrm{ite}(f, \neg g, \neg h) = \neg\,\mathrm{ite}(\neg f, \neg h, \neg g)$. Exactly one of these four forms has regular first and second arguments, and that form is the key in the [computed table](/computed-table/); for the last two forms the result is complemented before it is returned. Brace, Rudell and Bryant also simplify with $\mathrm{ite}(f, f, h) = \mathrm{ite}(f, 1, h)$, $\mathrm{ite}(f, g, f) = \mathrm{ite}(f, g, 0)$, $\mathrm{ite}(f, g, \neg f) = \mathrm{ite}(f, g, 1)$ and $\mathrm{ite}(f, \neg f, h) = \mathrm{ite}(f, 0, h)$, and add the terminal case $\mathrm{ite}(f, 0, 1) = \neg f$. With these rules, $\neg a \vee \neg b$ is computed as $\mathrm{ite}(\neg a, 1, \neg b)$, which becomes $\neg\,\mathrm{ite}(a, b, 0)$, the same key as $a \wedge b$.
- **Counting.** If a node of the plain diagram has $k$ satisfying assignments of its remaining variables among $2^m$, the complemented edge to it has $2^m - k$. [Satisfy-count](/bdd-satisfy-count/) must apply this at each complemented edge.

**Other conventions.** The proof uses only that one fixed edge of each node is regular, so that the bit of every edge is forced by the value at one fixed input. A rule with a regular else-edge works the same way, with the input of all zeros in place of all ones. Packages differ in which edge they keep regular, so diagrams from two packages cannot be compared bit for bit.

## Examples

**A function and its complement.** Let $a = x_1 \wedge x_2$. With complemented edges, its graph has the nodes $v = (2, \neg 1, 1)$ for $x_2$ and $u = (1, \neg 1, v)$ for $a$, and $a$ is the regular edge to $u$. The function $\neg a = \neg x_1 \vee \neg x_2$ is the complemented edge to $u$. A plain store that holds both $a$ and $\neg a$ needs four inner nodes ($x_2$, $\neg x_2$, $a$, $\neg a$) and two terminals. The store with complemented edges needs two inner nodes and one terminal.

**Parity.** The parity $x_1 \oplus \cdots \oplus x_n$ has two inner nodes at each level below the root in the plain BDD, one for the parity of the remaining variables and one for its complement: $2n - 1$ inner nodes and $2n + 1$ nodes in all. With complemented edges each pair is one node, so there are $n$ inner nodes and $n + 1$ nodes in all. Here $P = 2C - 1$, close to the upper bound of the size theorem.

**No saving.** For the majority of $x_1, x_2, x_3$ the subfunctions are $x_2 \wedge x_3$, $x_2 \vee x_3$ and $x_3$, and none is the complement of another, so both forms have four inner nodes. For a conjunction of literals the two forms also have the same number of inner nodes.

## Where it is used

- **BDD packages.** Brace, Rudell and Bryant (1990) used complemented edges with the then-edge rule. Minato, Ishiura and Yajima (1990) gave the same idea as a negation attribute on the edges of a shared BDD. Many later packages, such as CUDD, use complemented edges.
- **The [computed table](/computed-table/).** Calls related by De Morgan's laws, such as $a \wedge b$ and $\neg a \vee \neg b$, share one entry, which raises the hit rate.
- **[Boolean equivalence checking](/boolean-equivalence-checking/).** Both $f = g$ and $f = \neg g$ are tests in $O(1)$ time, so a check for an inverted output costs nothing extra.
- **XOR-rich functions.** Parity, adders and error-correcting codes have many subfunctions that are complements of each other. They gain the most, up to the factor of 2.

## References
