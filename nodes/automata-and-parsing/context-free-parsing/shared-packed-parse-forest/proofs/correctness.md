---
title: The binarized shared packed parse forest represents every parse tree of the input exactly once, and its construction stops
proves: [correctness, termination]
status: full
---

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. The input is $w = a_1 \cdots a_n$, and $w[i:j] = a_{i+1} \cdots a_j$. The line numbers are those of BUILD-SPPF and EXPAND on the page.

For a production $p = A \to x_1 \cdots x_m$ and $0 \le l \le m$, write $p_l$ for the item $A \to x_1 \cdots x_l \cdot x_{l+1} \cdots x_m$. Line L1 computes two sets:

- $D$, the triples $(X, i, j)$ with $X$ a symbol, $0 \le i \le j \le n$, and $X \Rightarrow^* w[i:j]$ (for a terminal $X$, this means $j = i + 1$ and $a_j = X$);
- $P$, the triples $(p_l, i, j)$ with $x_1 \cdots x_l \Rightarrow^* w[i:j]$.

## Lemma 1: the chart

The bottom-up agenda of line L1 computes exactly these sets.

*Proof.* The agenda adds $(a_j, j - 1, j)$ for each token, $(p_0, i, i)$ for each production and position, $(p_{l+1}, i, k)$ from $(p_l, i, j)$ and $(x_{l+1}, j, k)$, and $(A, i, j)$ from $(p_m, i, j)$ for a production $p$ of $A$. Each rule keeps the meaning of the facts, so by induction on the order in which facts are added, every fact is true. Conversely, take a true fact. If it is $(X, i, j)$ with $X$ a nonterminal, take a parse tree for it, and if it is $(p_l, i, j)$, take parse trees for $x_1, \ldots, x_l$ over consecutive pieces of $w[i:j]$. Induction on the total number of nodes in these trees shows that the fact is added: the fact $(p_l, i, j)$ with $l \ge 1$ comes from $(p_{l-1}, i, k)$ and $(x_l, k, j)$, which have fewer nodes, and $(A, i, j)$ comes from $(p_m, i, j)$ with the same trees minus the root. Both rules fire whichever premise is found first, because a new prefix fact scans the completed facts already found and a new completed fact scans the prefix facts waiting for it. There are finitely many facts and each is processed once, so the agenda empties. $\square$

## The trees of a node

The forest has *symbol nodes* $(X, i, j)$, *intermediate nodes* $(p_l, i, j)$ with $l \ge 2$, and *packed nodes*. Lines L7, L8 and L11 give each packed node of a node $u$ an optional left child and an optional right child. We assign to each node a set of objects, defined as the least sets closed under the following rules (so every object is finite):

- a terminal symbol node $(a, j - 1, j)$ has the one tree $a$;
- an intermediate node $u$ has the sequences $\sigma \cdot t$, for a packed node of $u$ with left child $v$ and right child $r$, $\sigma$ a sequence of $v$ (or a tree of $v$, read as a sequence of length one, when $v$ is a symbol node) and $t$ a tree of $r$;
- a nonterminal symbol node $u = (A, i, j)$ has the trees $A(\sigma)$, the node $A$ with children $\sigma$, for each packed node of $u$, where $\sigma$ is the empty sequence for a packed node without children (line L7), a single tree of the right child when there is no left child (line L8), and $\sigma' \cdot t$ as above otherwise.

We say that such a tree is *represented* at $u$, and that the choice of one packed node at each node used is its *witness*.

## Lemma 2: soundness

Every node that is created satisfies its fact: $(X, i, j) \in D$ for a symbol node, $(p_l, i, j) \in P$ for an intermediate node. Every tree represented at a symbol node $(X, i, j)$ is a parse tree with root $X$ and yield $w[i:j]$, and every sequence represented at an intermediate node $(p_l, i, j)$ is a list of parse trees with roots $x_1, \ldots, x_l$ whose yields concatenate to $w[i:j]$.

*Proof.* The root is created at line L3 only when $(S, 0, n) \in D$. Line L11 creates a left node and a right node only after line L10 has checked $(p_{m-1}, i, k) \in P$ and $(x_m, k, j) \in D$, which are exactly their facts, and line L8 creates a node whose fact is $(x_1, i, j)$, which holds because $(p_1, i, j) \in P$. The trees and sequences are built by the rules above, and induction on their size shows the claim: at line L11 the left part covers $w[i:k]$ with the symbols $x_1, \ldots, x_{m-1}$, the right part covers $w[k:j]$ with $x_m$, and at a symbol node $(A, i, j)$ the packed nodes come from a production $p$ of $A$ with $(p_m, i, j) \in P$ (line L5), so $A(\sigma)$ applies a production of the grammar. $\square$

## Lemma 3: completeness

Every node that is created is expanded exactly once. If the symbol node $(X, i, j)$ is created and $t$ is a parse tree with root $X$ and yield $w[i:j]$, then $t$ is represented at $(X, i, j)$.

*Proof.* NODE creates a node only if its key is new, and pushes it onto the work stack at the same moment; line L4 pops each pushed node once and expands it at line L5 or L6 (a terminal symbol node has nothing to expand). So each node is expanded exactly once, after which its packed nodes are final.

Now induction on the height of $t$. If $X$ is a terminal, $t = X$ is represented. Otherwise the root of $t$ uses a production $p = X \to x_1 \cdots x_m$, and its children $t_1, \ldots, t_m$ have yields $w[b_0 : b_1], \ldots, w[b_{m-1} : b_m]$ with $b_0 = i$ and $b_m = j$. By Lemma 1, $(p_l, i, b_l) \in P$ for every $l$ and $(x_l, b_{l-1}, b_l) \in D$. When $(X, i, j)$ is expanded, line L5 calls EXPAND for $p_m$ because $(p_m, i, j) \in P$.

- If $m = 0$, line L7 adds the packed node without children, which represents $X()$, that is $t$.
- If $m = 1$, line L8 adds a packed node whose only child is the symbol node $(x_1, i, j)$.
- If $m \ge 2$, the loop of line L9 reaches $k = b_{m-1}$, and line L10 finds both facts, so line L11 adds a packed node with right child $(x_m, b_{m-1}, j)$ and left child $(x_1, i, b_1)$ when $m = 2$, or the intermediate node $(p_{m-1}, i, b_{m-1})$ when $m \ge 3$. That intermediate node is created now or was created before, and in either case it is expanded once, with EXPAND for $p_{m-1}$ over $(i, b_{m-1})$, where the same argument with $m - 1$ in place of $m$ applies.

Following the chain down to $l = 2$, every symbol node $(x_l, b_{l-1}, b_l)$ is a child of some packed node in the chain. Each $t_l$ has smaller height, so by induction $t_l$ is represented at $(x_l, b_{l-1}, b_l)$; then the rules for intermediate and symbol nodes put $t_1 \cdots t_l$ at the intermediate node $(p_l, i, b_l)$ for $l = 2, \ldots, m - 1$, and $X(t_1 \cdots t_m) = t$ at $(X, i, j)$. $\square$

## Lemma 4: one witness per tree

Each tree represented at a node $u$ has exactly one witness below $u$.

*Proof.* The packed nodes of one node are distinct pairs (production, split). Let $t$ be represented at the symbol node $(A, i, j)$. The production at the root of $t$ fixes $p$, and the yields of the children fix the boundaries $b_0, \ldots, b_m$. The packed node of $(A, i, j)$ in a witness must have production $p$ and split $b_{m-1}$, the start of the yield of the last child (or $i$ when $m \le 1$), and the packed node of the intermediate node $(p_l, i, b_l)$ must have split $b_{l-1}$. So the choices along the chain are forced, and by induction on the size of $t$, so are the choices in the subtrees. $\square$

## Theorem

BUILD-SPPF stops. The parse trees of $w$ with root $S$ are exactly the trees represented at the root node, each with exactly one witness. If the forest has no cycle, the number of parse trees is $c(\mathrm{root})$, where $c(a) = 1$ for a terminal node and $c(u) = \sum c(\ell) \cdot c(r)$ over the packed nodes of $u$ (a missing child counts as 1). If the forest has a cycle, $w$ has infinitely many parse trees.

*Proof.* Termination: the keys of nodes are symbol triples, at most $(|V| + |\Sigma|)(n + 1)^2$, and item triples, at most $|G|(n + 1)^2$; each node is expanded once (Lemma 3), and each expansion runs the loop of line L9 at most $n + 1$ times. The two inclusions are Lemmas 2 and 3 for the root $(S, 0, n)$; if $(S, 0, n) \notin D$, there is no tree and line L2 returns the empty forest, which is correct by Lemma 1.

For the count, Lemma 4 makes the map from witnesses to trees one to one, so the number of trees at $u$ equals the number of witnesses, and in an acyclic forest the witnesses below $u$ are counted by the recurrence for $c$ by induction in reverse topological order.

For a cycle: every node has at least one packed node and at least one represented tree, by Lemma 2 read backward and Lemma 3 (every created node satisfies its fact, and a true fact has a tree). A cycle passes through a symbol node $(X, i, j)$, since the left child of an intermediate node $(p_l, i, j)$ is an intermediate node of smaller $l$ or a symbol node, so no cycle uses intermediate nodes only. Following the cycle from $(X, i, j)$ back to itself, and completing every other child with any of its trees, gives a context $C$ with $C[t]$ represented at $(X, i, j)$ whenever $t$ is. Starting from any tree $t_0$ at $(X, i, j)$, the trees $t_0, C[t_0], C[C[t_0]], \ldots$ are all different (each is larger than the previous one). Every node is reachable from the root, since it was created as a child of a node already in the forest; completing a path from the root to $(X, i, j)$ in the same way gives a context $E$ with $E[t]$ a tree of $w$ whenever $t$ is represented at $(X, i, j)$. The trees $E[t_0], E[C[t_0]], E[C[C[t_0]]], \ldots$ are distinct parse trees of $w$. So $w$ has infinitely many parse trees, and $X \Rightarrow^+ X$ for a nonterminal $X$ that covers a piece of $w$. $\square$

## Remarks

**The operations.** COUNT applies the recurrence in a postorder found by an explicit depth-first search, after a depth-first search that looks for a back edge. TREE$(r)$ unranks: at each node it walks the packed nodes, subtracting $c(\ell) c(r)$ until the rank falls inside one, and splits the remaining rank into a quotient and a remainder for the two children; by Lemma 4 the ranks $0, \ldots, c(\mathrm{root}) - 1$ give each tree once. ONE-TREE also works for a cyclic forest: it marks a node as soon as one of its packed nodes has all its children marked, and uses that packed node. Each node is marked after all children of its chosen packed node, so the choices follow a well-founded order and the tree they describe is finite. CONTAINS recomputes the boundaries of a given tree and checks the forced witness of Lemma 4 node by node.

**The size.** There are $O(|G| n^2)$ symbol and intermediate nodes, and each node has at most $n + 1$ packed nodes, so the forest has $O(|G| n^3)$ nodes and edges. The grammar $S \to S S \mid a$ on $a^n$ shows that this is tight in $n$: it has $n + (n - 1) n (n + 1) / 6$ packed nodes, while the number of trees is the Catalan number $C_{n-1}$.
