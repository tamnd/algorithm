---
tag: 68B1G5
kind: data-structure
slug: tanner-graph
name: Tanner graph
aliases:
- factor graph of a code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: The bipartite graph of a parity-check matrix, with a variable node per code bit, a check node per row and an edge per 1. Iterative decoders pass messages on its edges.
model: word-ram
complexity:
  vars: {m: the number of checks, n: the code length, E: the number of ones in H}
  time: {worst: Θ(m n)}
  space: {extra: Θ(m + n + E)}
history:
  year: 1981
  people: [R. Michael Tanner, Niclas Wiberg]
  note: Tanner described codes by bipartite graphs of digits and subcodes in 1981. Wiberg in 1996 put the decoding algorithms of trellises and of LDPC codes on such graphs, which led to factor graphs.
prereqs: [parity-check-matrix, bipartite-graph]
see_also: [ldpc-code, belief-propagation-decoding, peeling-decoding, binary-erasure-channel, expander-codes, factor-graph, adjacency-list, cycle-detection]
sources:
  - paper: doi:10.1109/TIT.1981.1056404
    title: R. M. Tanner, A recursive approach to low complexity codes, IEEE Transactions on Information Theory 27(5), 1981, pages 533 to 547
    locator: The bipartite graph of digit nodes and subcode nodes, its girth, and iterative decoding on it
  - paper: "N. Wiberg, Codes and decoding on general graphs, PhD thesis, Linköping University, 1996"
    title: Codes and decoding on general graphs
    locator: Decoding on graphs with hidden state nodes, which covers trellises and Tanner graphs, and the min-sum and sum-product algorithms on them
  - paper: "C. Di, D. Proietti, I. E. Telatar, T. J. Richardson and R. L. Urbanke, Finite-length analysis of low-density parity-check codes on the binary erasure channel, IEEE Transactions on Information Theory 48(6), 2002, pages 1570 to 1579"
    title: Finite-length analysis of low-density parity-check codes on the binary erasure channel
    locator: The definition of stopping sets and the proof that iterative erasure decoding stops at the largest stopping set inside the erased positions
  - paper: "T. J. Richardson, Error floors of LDPC codes, Proceedings of the 41st Annual Allerton Conference on Communication, Control, and Computing, 2003"
    title: Error floors of LDPC codes
    locator: Trapping sets and their role in the error floor of iterative decoders
  - book: isbn:9780521852296
    title: Tom Richardson and Rüdiger Urbanke, Modern Coding Theory, Cambridge University Press, 2008
    locator: Chapter 3 (Tanner graphs, the peeling decoder and stopping sets on the binary erasure channel)
---

A Tanner graph is the [bipartite graph](/bipartite-graph/) of a [parity-check matrix](/parity-check-matrix/) $H$. It has one *variable node* for each code position, one *check node* for each row of $H$, and an edge between check $i$ and variable $j$ exactly when $H_{ij} = 1$. A word is a codeword when every check node sees an even number of ones among its neighbors. The graph is stored as two sets of [adjacency lists](/adjacency-list/), so its size is the number of ones of $H$, which is small for an [LDPC code](/ldpc-code/). Iterative decoders such as [belief propagation decoding](/belief-propagation-decoding/) send messages along its edges. Its short cycles, its stopping sets and its trapping sets decide how well those decoders work.

## In plain words

Draw one dot for each bit of a codeword in a row at the bottom, and one square for each parity rule in a row at the top. Connect a square to every bit that its rule adds up. A word is valid when every square sees an even number of ones.

The picture holds exactly the same information as the matrix of rules, but it shows who talks to whom. A decoder can let each bit and each rule exchange short notes along the lines, and each note costs one step. When the lines form only long loops, the notes that come back to a node carry mostly new information. Short loops make the notes echo, and the decoder gets worse.

## The abstract type

A Tanner graph of an $m \times n$ binary matrix $H$ supports:

- **Build(H):** make the graph.
- **Neighbors:** the checks of a variable node, and the variables of a check node, each as a list.
- **Syndrome(x):** the parity at each check node for a word $x$, that is $H x^T$.
- **Girth:** the length of a shortest cycle, or none if the graph is a forest.
- **Stopping set test and peeling:** whether a set of variable nodes is a stopping set, and the largest stopping set inside a given set.

The graph does not depend on a choice of generator matrix, but it does depend on $H$: two parity-check matrices of the same code, for example one with an extra row that is the sum of two others, give different graphs and different decoders.

## Representation

Two arrays of lists: `chk_adj[i]` holds the variables of check $i$ in increasing order, and `var_adj[j]` the checks of variable $j$ in increasing order. Each edge is in both arrays once. Message passing decoders also give each edge an index, so a message can be stored per edge in a flat array; the implementation keeps the lists and lets each decoder keep its own messages.

## Operations

```pseudo id=main
BUILD(H)                                ▷ H is an m × n matrix of 0 and 1
L1  m ← number of rows of H, n ← number of columns
L2  var_adj[j] ← empty list for each j, and chk_adj[i] ← empty list for each i
L3  for i ← 0 to m − 1 do
L4      for j ← 0 to n − 1 do if H[i][j] = 1 then
L5          append j to chk_adj[i]
L6          append i to var_adj[j]
```

- **Syndrome** adds, for each check, the bits of its neighbors mod 2.
- **Girth** runs a breadth-first search from each node. When the search from a root meets an edge from $u$ to an already labeled node $w$ that is not the parent of $u$, it has found a closed walk of length $d(u) + d(w) + 1$ through the root that contains a cycle. The least value over all roots is the girth. A search stops early when $2 d(u)$ reaches the best value so far.
- **Stopping set test** checks that no check node has exactly one neighbor in the set.
- **Peel(E)** keeps a count of the nodes of $E$ at each check. While some check has count 1, it removes its single node from $E$ and updates the counts of that node's checks. On the [binary erasure channel](/binary-erasure-channel/) this is [peeling decoding](/peeling-decoding/): the removed node is the erased bit that the check gives as the sum of its other bits.

## Example

**The Hamming [7, 4] code.** Take

$$H = \begin{pmatrix} 1&0&1&1&1&0&0 \\ 1&1&1&0&0&1&0 \\ 0&1&1&1&0&0&1 \end{pmatrix}.$$

The graph has 7 variable nodes, 3 check nodes and 12 edges. `chk_adj[0]` $= [0, 2, 3, 4]$ and `var_adj[2]` $= [0, 1, 2]$: bit 2 is in all three checks. Checks 0 and 1 share the bits 0 and 2, so $v_0, c_0, v_2, c_1, v_0$ is a cycle, and the girth is 4, the least possible.

The word 1011100 has syndrome 000, so it is a codeword. The word 0010000 has syndrome 111, since bit 2 is in every check.

**Stopping sets.** Suppose the bits 0, 1 and 4 are erased. Check 2 contains bit 1 and no other erased bit, so it gives bit 1. Then check 1 gives bit 0, and then check 0 gives bit 4: peeling recovers all three. Now suppose the bits 0, 1 and 2 are erased. Check 0 sees two of them, check 1 three and check 2 two, so no check can start, and peeling returns $\{0, 1, 2\}$. This set is a stopping set but not the support of a codeword: 1110000 has syndrome 010. A maximum likelihood erasure decoder would still recover it, since no nonzero codeword has its support inside $\{0, 1, 2\}$. No set of two bits is a stopping set here, since that would need two equal columns of $H$.

**A tree.** The matrix with rows 1100, 0110 and 0011 gives a path $v_0, c_0, v_1, c_1, v_2, c_2, v_3$, a tree, so the girth is none. On a tree, belief propagation computes exact posteriors.

## Correctness

Lines L3 to L6 visit each entry of $H$ once and add an edge in both directions exactly for the ones, so the lists are the graph of $H$, and the syndrome at check $i$ is the $i$th entry of $H x^T$. The girth search reports only lengths of closed walks with an edge used once, so every report is at least the girth, and from any node of a shortest cycle the search reports its length exactly at the node opposite the root. For peeling, the union of two stopping sets is a stopping set, so each set $E$ contains a largest one, $S^*(E)$. Peeling never removes a node of $S^*(E)$, and when it stops no check has count 1, so what is left is a stopping set inside $E$; together these show that it returns $S^*(E)$, in any order. The [correctness proof](proofs/correctness.md) has the details.

## Complexity

- **Build** from a dense $H$ takes $\Theta(m n)$ time; from a list of the positions of the ones it takes $\Theta(m + n + E)$. The space is $\Theta(m + n + E)$.
- **Syndrome**, the stopping set test and **peel** take $\Theta(m + n + E)$ time. In peeling, each check enters the queue at most twice, once at the start and once when its count drops to 1.
- **Girth** takes $O((m + n) E)$ time, one breadth-first search per node.
- For an LDPC code with bounded degrees, $E = \Theta(n)$, so the graph and every message passing iteration are linear in $n$.

## Variants

- **Generalized Tanner graphs.** Tanner's original graphs let a constraint node stand for any small code, not only a single parity check. [Expander codes](/expander-codes/) of the Zémor kind use this form.
- **Factor graphs.** A [factor graph](/factor-graph/) has variable nodes and factor nodes with arbitrary functions. The Tanner graph with a channel factor at each variable node is the factor graph of the posterior $P(c \mid y)$ of a code. Wiberg's graphs also add hidden state nodes, which give trellises as a special case.
- **Protographs and lifted graphs.** A small base graph is copied $Z$ times and the copies of each edge are permuted, often by cyclic shifts. This gives the quasi-cyclic LDPC codes of 5G NR and Wi-Fi.
- **Graphs with large girth.** Progressive edge growth adds the edges one at a time, each to a check that is as far as possible from the variable node, to avoid short cycles.

## When to use it

- Use it to decode LDPC codes and other codes with sparse parity-check matrices by message passing.
- Use it to analyze iterative decoders: girth for how many iterations behave as on a tree, stopping sets for the erasure channel, and trapping sets for the error floor on other channels.
- For a dense matrix, such as that of a Hamming or Reed-Solomon code, the graph has many short cycles, and a trellis or an algebraic decoder is usually better.

## Pitfalls

- **Short cycles.** A 4-cycle means two checks share two variables, so their messages to each other echo after two iterations. Construction methods remove 4-cycles first; a code with girth 6 or more is the usual goal.
- **Stopping sets.** On the erasure channel, iterative decoding fails exactly when the erased set contains a nonempty stopping set, even when the erasures are recoverable by Gaussian elimination. The smallest stopping set, the stopping distance, can be smaller than the minimum distance.
- **Trapping sets.** On the BSC and the AWGN channel, an $(a, b)$ trapping set is a set of $a$ variable nodes whose induced subgraph has $b$ check nodes of odd degree. When $b$ is small, a few wrong bits on such a set satisfy almost all their checks, and the decoder stays stuck there. These sets cause most of the error floor of LDPC codes.
- **Redundant rows.** Rows that are sums of other rows do not change the code, but they change the graph and can help or hurt the decoder.

## Implementations

## History

Tanner introduced the graphs in 1981 to build long codes from short ones and to decode them by iteration; Gallager's LDPC decoders of 1962 had used the same structure without the graph. Wiberg, Loeliger and Kötter generalized the graphs in 1995 and 1996 to include trellises, and Wiberg's thesis showed that the Viterbi, BCJR and LDPC decoders are all message passing on such graphs. This led to the factor graphs of Kschischang, Frey and Loeliger in 2001. Di, Proietti, Telatar, Richardson and Urbanke defined stopping sets in 2002, and Richardson introduced trapping sets in 2003.

## References
