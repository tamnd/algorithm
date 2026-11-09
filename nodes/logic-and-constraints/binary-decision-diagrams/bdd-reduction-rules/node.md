---
tag: KDQE4S
kind: definition
slug: bdd-reduction-rules
name: BDD reduction rules
aliases:
- redundant-test elimination
- isomorphic-node merging
- elimination rule
- merging rule
- Reduce
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: Delete nodes whose two children are equal and merge isomorphic nodes.
prereqs: [binary-decision-diagram, ordered-binary-decision-diagram]
see_also: [reduced-ordered-bdd, bdd-canonicity, ordered-binary-decision-diagram, hash-consing, zero-suppressed-bdd, minimal-dfa-uniqueness, dfa-minimization]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 2, Definition 5 (a reduced function graph has no vertex with low(v) = high(v) and no two distinct isomorphic subgraphs), and Section 4.2, the Reduce algorithm and Figure 5
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 3, OBDDs (the deletion rule and the merging rule, and the reduction algorithm)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (Algorithm R, reduction to a BDD)
---

The two BDD reduction rules shrink a [binary decision diagram](/binary-decision-diagram/) without changing the function of any node. The elimination rule removes a node whose low and high edges go to the same node, and the merging rule keeps only one of two nodes that test the same variable and have the same children. A diagram where neither rule applies is **reduced**. For an [ordered BDD](/ordered-binary-decision-diagram/), the reduced diagram is the [reduced ordered BDD](/reduced-ordered-bdd/), which the [canonicity theorem](/bdd-canonicity/) shows to be unique; this page gives the rules and the procedure Reduce that applies them.

## Definition

Let $B$ be a binary decision diagram: a directed acyclic graph with terminals labelled 0 or 1 and inner nodes $u$ with a variable $\mathrm{var}(u)$ and two children $\mathrm{lo}(u)$ and $\mathrm{hi}(u)$. Each node $u$ has a function $f_u$, defined by $f_u = (\neg x_i \wedge f_{\mathrm{lo}(u)}) \vee (x_i \wedge f_{\mathrm{hi}(u)})$ for $i = \mathrm{var}(u)$, and by its label for a terminal.

1. **Elimination rule** (also called the deletion rule, or redundant-test elimination). If an inner node $u$ has $\mathrm{lo}(u) = \mathrm{hi}(u) = w$, remove $u$ and redirect each edge that goes into $u$ to $w$. If $u$ is a root, $w$ becomes the root.
2. **Merging rule** (isomorphic-node merging). If two distinct nodes $u$ and $v$ are both terminals with the same label, or are both inner nodes with $\mathrm{var}(u) = \mathrm{var}(v)$, $\mathrm{lo}(u) = \mathrm{lo}(v)$ and $\mathrm{hi}(u) = \mathrm{hi}(v)$, remove $v$ and redirect each edge into $v$ to $u$.

$B$ is **reduced** when neither rule applies. Bryant's Definition 5 says this in another way: no node has $\mathrm{lo}(v) = \mathrm{hi}(v)$, and no two distinct nodes are the roots of isomorphic subgraphs. The two forms are equivalent. If two distinct nodes have isomorphic subgraphs, take such a pair $(u, v)$ where $u$ has the fewest nodes below it. Then the children of $u$ and $v$ are matched by the isomorphism, and by the choice of the pair they are equal, so the merging rule applies to $u$ and $v$. The converse is direct, since two nodes with the same triple have isomorphic subgraphs.

**Each rule keeps every function.** For the elimination rule, $f_u = (\neg x_i \wedge f_w) \vee (x_i \wedge f_w) = f_w$, so each edge now points to a node with the same function as before. For the merging rule, $u$ and $v$ have the same triple, so $f_u = f_v$ by the definition. In both cases the functions of all other nodes do not change, by induction from the bottom. Each step removes one node, so any sequence of steps stops after fewer than $|B|$ steps.

**Each rule keeps the order.** If $B$ is ordered, an edge into $u$ that now goes to $w$ goes to a node of a larger level than $u$, so it still goes down. The merging rule only identifies nodes on the same level. So reducing an ordered BDD gives an ordered BDD.

**The procedure Reduce.** Applying the rules one at a time is slow. Bryant's Reduce does it in one bottom-up pass, level by level. It gives each node an id so that two nodes get the same id exactly when they have the same function.

```pseudo
REDUCE(B)                         ▷ B is ordered, with levels 1 .. n + 1
1  give the terminal 0 the id 0 and the terminal 1 the id 1
2  for k ← n downto 1 do
3      Q ← empty list
4      for each node u on level k do
5          if id(lo(u)) = id(hi(u)) then id(u) ← id(lo(u))      ▷ elimination
6          else add the key (id(lo(u)), id(hi(u)), u) to Q
7      sort Q by the pair (id(lo), id(hi))
8      for each run of equal pairs in Q do                     ▷ merging
9          give all nodes of the run one new id, and keep one node for it
10 return the node with the id of the root
```

The keys of one level are sorted, so the nodes with equal children become neighbours. Bryant takes this idea from the minimization of tree-like structures in Aho, Hopcroft and Ullman. With a sort, Reduce takes $O(|B| \log |B|)$ time. With a [hash table](/hash-table/) from triples to ids in place of the sort, it takes $O(|B|)$ expected time, and the hash-table version is the REDUCE operation of the [ordered BDD](/ordered-binary-decision-diagram/) page. Sieling and Wegener (1993) gave a deterministic linear-time version that replaces the sort by bucket sort. A BDD package does not run Reduce at all: its MK operation applies both rules to each new node at the moment it is made, so the store is always reduced.

## Examples and non-examples

**The majority function.** Let $f = \mathrm{MAJ}(x_1, x_2, x_3)$ with the order $x_1 < x_2 < x_3$. Its decision tree has 7 inner nodes. On level 3 the four nodes have the children $(0, 0)$, $(0, 1)$, $(0, 1)$ and $(1, 1)$ for $(x_1, x_2) = (0,0), (1,0), (0,1), (1,1)$. The elimination rule removes the first and the last, and the merging rule makes the two middle ones one node $c = (x_3, 0, 1)$. On level 2, the node for $x_1 = 0$ becomes $(x_2, 0, c)$, which is $x_2 \wedge x_3$, and the node for $x_1 = 1$ becomes $(x_2, c, 1)$, which is $x_2 \vee x_3$. They differ, so both stay. The reduced diagram has 4 inner nodes and 2 terminals.

**Parity.** The decision tree of $x_1 \oplus x_2 \oplus x_3$ has 7 inner nodes. No node has equal children, since each subfunction of parity depends on all the remaining variables. The merging rule leaves two nodes per level below the root, one for the even case and one for the odd case. The result has $1 + 2 + 2 = 5$ inner nodes and 2 terminals, $2n + 1 = 7$ in all.

**Several roots.** If a store holds the BDDs of $x_1 \wedge x_2$ and of $x_2$, the merging rule shares the node $(x_2, 0, 1)$ between them. A reduced store with many roots is a shared BDD, and the functions are equal exactly when the roots are the same node.

**Non-examples.**

- Removing a node whose two children are different nodes is not a rule step, even when the children happen to have the same function. In a reduced ordered diagram that case cannot occur, but in a diagram that is not yet reduced it must wait until the children have been merged.
- Merging two nodes that have the same function but different triples is not a rule step. In an ordered diagram, the bottom-up rules reach the same result, since the children are merged first. In a general BDD this does not happen. For example, the nodes $(x_1, 0, (x_2, 0, 1))$ and $(x_2, 0, (x_1, 0, 1))$ both compute $x_1 \wedge x_2$, they are each reduced, and no rule merges them.
- The rule of a [zero-suppressed BDD](/zero-suppressed-bdd/) removes a node whose high edge goes to the terminal 0, not a node with equal children. With that rule the diagram is canonical for a different meaning of a skipped variable.
- A reduced diagram of an unordered BDD is not canonical, as the second non-example shows. Canonicity needs the order.

## Related definitions

- [Reduced ordered BDD](/reduced-ordered-bdd/): an ordered BDD to which no rule applies.
- [Canonicity of reduced ordered BDDs](/bdd-canonicity/): for a fixed order, the reduced diagram of a function is unique and minimal, whatever order of rule steps produced it.
- Quasi-reduced OBDD: an ordered BDD where only the merging rule is applied and every path tests every variable. It is also canonical.
- [Hash consing](/hash-consing/): the general technique behind the unique table, which applies the merging rule when a node is made.
- [Minimal DFA uniqueness](/minimal-dfa-uniqueness/) and [DFA minimization](/dfa-minimization/): the merging rule is the same as merging equivalent states of an acyclic automaton, and Reduce is a bottom-up form of minimization.

## References
