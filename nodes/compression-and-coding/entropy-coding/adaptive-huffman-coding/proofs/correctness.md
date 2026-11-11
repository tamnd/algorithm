---
title: Correctness of adaptive Huffman coding
proves: [correctness]
status: sketch
---

The proof has three parts. The sibling property characterizes Huffman trees (Gallager 1978). The update of algorithm FGK keeps the sibling property. The decoder keeps the same tree as the encoder, so it decodes correctly. Vitter's update keeps a stronger invariant; we only state its proof idea at the end.

**Setting.** The tree has the NYT node of weight 0 and one leaf for each symbol seen so far, with its count as its weight. An inner node has two children and the sum of their weights as its weight. The nodes carry the numbers $0, 1, \ldots, 2m$ for a tree of $2m + 1$ nodes, the root has number $2m$, and the nodes with numbers $2j$ and $2j + 1$ are siblings.

**Definition.** A tree has the *sibling property* if the weights do not decrease as the number increases. Since siblings have the numbers $2j$ and $2j + 1$, this means: the nodes can be listed in order of non-increasing weight, with each node next to its sibling.

**Lemma 1 (Gallager).** A full binary tree with non-negative weights at the leaves is a Huffman tree for those weights if and only if it has the sibling property. Here a Huffman tree is a tree that the algorithm HUFFMAN can build with some rule for ties.

*Proof.* If the tree has the sibling property, the nodes with numbers 0 and 1 are siblings and have the two smallest weights among all nodes, so in particular among the leaves. HUFFMAN can merge them first. Remove both: their parent becomes a leaf with their summed weight, the numbers shift down by 2, and the smaller tree still has the sibling property. By induction on the number of leaves, HUFFMAN can build the rest of the tree. Conversely, number the nodes in the order in which HUFFMAN takes them out of the queue, with the root last. The two nodes of each merge are taken one after the other, so siblings get the numbers $2j$ and $2j + 1$. The queue gives out items in non-decreasing weight order, because each new item is at least as heavy as the two items it replaces. So the weights do not decrease with the number. $\square$

By Lemma 1 and the optimality of Huffman's algorithm, a tree with the sibling property is an optimal code tree for the current counts.

**Lemma 2.** If the tree has the sibling property before line L5 of FGK-ENCODE, it has the sibling property after the loop of lines L6 to L10.

*Proof.* Let $q_0$ be the leaf of the symbol, and let $q_0, q_1, \ldots, q_r$ be the nodes that the loop visits, where $q_{i+1}$ is the parent of $q_i$ after the swap in step $i$. We claim that before step $i$ the tree has the sibling property except that the nodes $q_0, \ldots, q_{i-1}$ have been incremented, and that this is consistent: the weights do not decrease with the number, and each inner node other than $q_i$ has the sum of its children as its weight, while $q_i$ has one less than this sum.

In step $i$, let $w = w(q_i)$ and let $b$ be the node of line L7. A swap exchanges two places in the tree, with the subtrees, and the two numbers. So it keeps the sibling pairs $2j, 2j + 1$, and since $q_i$ and $b$ have the same weight it keeps the weight order. The only exception is a swap of $q_i$ with its own parent, which line L7 forbids. After the swap, $q_i$ has the highest number among the nodes of weight $w$, except possibly for its parent $p$. All nodes with a higher number have weight at least $w + 1$, except $p$. So after line L9, which sets $w(q_i) = w + 1$, the weights still do not decrease with the number, except possibly at the place of $p$, which has weight $w$ and a number above $q_i$. This happens only if $p$ has the same weight as its child $q_i$, so the sibling of $q_i$ has weight 0. The next step increments $p$ with no swap, because $p$ is then the highest node of weight $w$, and the order is right again. The parent of $q_i$ is now one less than the sum of its children, which is the claim for step $i + 1$. At the root the loop stops, and all sums are right. $\square$

A new symbol first splits the NYT node into a new NYT node and a leaf of weight 0, both with the two smallest numbers. Both have weight 0, so the sibling property holds before line L5. By induction over the message, the tree has the sibling property after each symbol, so it is a Huffman tree for the counts so far.

**Lemma 3.** The decoder decodes each symbol correctly.

*Proof.* Encoder and decoder start with the same tree and run the same deterministic update after the same symbol, so by induction they have the same tree before each symbol. The encoder sends the path from the root to the leaf of the symbol, or to the NYT node followed by 8 raw bits. The tree is a prefix code, so the decoder walks the same path and stops at the same leaf. If this leaf is the NYT node, it reads the 8 raw bits. $\square$

**Vitter's algorithm.** Vitter (1987) uses the implicit numbering: the numbers follow the levels of the tree, from the bottom level to the root and from left to right on each level. His invariant adds to the sibling property that for each weight $w$, all leaves of weight $w$ come before all inner nodes of weight $w$. A slide moves a node over a block of nodes with the same weight before the increment (the inner nodes of weight $w$ for a leaf, the leaves of weight $w + 1$ for an inner node), so after the increment the order rule holds again. Vitter shows that the invariant makes the tree minimize both $\sum_j l_j$ and $\max_j l_j$ among all Huffman trees for the counts, and that this gives fewer than $S + t$ bits for a message of $t$ symbols, where $S$ is the cost of the two-pass Huffman code. We do not reproduce that proof; see his paper. The tests check the sibling property, the order rule and the level order after each update.
