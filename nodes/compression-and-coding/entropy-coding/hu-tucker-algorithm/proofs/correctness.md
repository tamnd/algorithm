---
title: Correctness of the Hu-Tucker algorithm
proves: [correctness]
status: sketch
---

The Hu-Tucker algorithm has three phases: combination (lines L1 to L4), levels (line L5) and recombination (line L6). We prove the recombination phase in full and the easy facts about the combination phase, and give the structure of the optimality proof, which is long. The original proof of Hu and Tucker (1971) was later simplified by Hu (1973) and by Hu, Kleitman and Tamaki (1979); Karpinski, Larmore and Rytter (1997) gave a new, shorter proof. Knuth's account is in The Art of Computer Programming, Volume 3, Section 6.2.2.

**Notation.** Leaves $1, \ldots, n$ have weights $w_i > 0$. A *square node* is an original leaf not yet combined, and a *circle node* is a node made by a combination. Two nodes of the current list are *compatible* if no square node lies strictly between them.

**Lemma 1 (the combination phase ends with one binary tree).** Each step removes one node from the list, and some pair is always compatible while the list has two or more nodes, since neighbours in the list are compatible. After $n - 1$ steps one node remains. It is the root of a full binary tree whose leaves are the $n$ original leaves, since every node made is a circle node with two children, and each node of the list is used as a child at most once. $\square$

**Lemma 2 (the cost of the levels).** Let $d_i$ be the depth of leaf $i$ in the tree of the combination phase. Its weighted path length $\sum_i w_i d_i$ is the sum of the weights of all circle nodes made, since leaf $i$ adds $w_i$ to the weight of each of its $d_i$ ancestors. $\square$

The tree of phase 1 is not in general alphabetic. For the weights 3, 2, 2, 3, the two middle leaves are combined into a circle node of weight 4, after which the outer leaves, of weight 3 each, are compatible across the circle node and are combined, because $3 + 3 < 3 + 4$. The leaves of that tree are not in the order 1, 2, 3, 4. Only the depths are kept.

**Lemma 3 (recombination).** Let $d_1, \ldots, d_n$ be the leaf depths, from left to right, of some full binary tree $T$ with its leaves in this order. The stack method (push each leaf with its depth; while the two top items have equal depth $\delta$, replace them by one item of depth $\delta - 1$ that has them as left and right children) returns $T$.

*Proof.* By induction on the number of leaves. If $n = 1$, then $d_1 = 0$ and the stack holds the single leaf. Otherwise, consider the leftmost pair of sibling leaves of $T$: leaves $i$ and $i + 1$ with a common parent, and with $i$ least. Such a pair exists, since a deepest leaf has a sibling, and that sibling must be a leaf because it can not have deeper descendants. First we show that no two neighbouring leaves $a$ and $a + 1$ with $a + 1 \le i$ have equal depth. Suppose they do. If $a$ were a left child, its sibling would be the subtree that starts with leaf $a + 1$; this subtree is not the single leaf $a + 1$, by the choice of $i$, so $a + 1$ would be deeper than $a$. So $a$ is a right child, and its sibling is a subtree that ends with leaf $a - 1$. If that subtree is a leaf, then $a - 1$ and $a$ are sibling leaves; if not, it contains two sibling leaves, since every full binary tree with two or more leaves does. Either way there are sibling leaves to the left of $i$, against the choice of $i$. So, until leaf $i + 1$ is pushed, the stack holds the leaves $1, \ldots, i$ and no combination takes place. When leaf $i + 1$ is pushed, the top two items have the depth $d_i = d_{i + 1}$ and are combined into their parent. From then on the method runs as on the tree $T'$ in which the parent of $i$ and $i + 1$ is a leaf of depth $d_i - 1$, which has $n - 1$ leaves, and the induction hypothesis applies. $\square$

The same method detects depths that no alphabetic tree has: it then ends with more than one item, or with an item of nonzero depth.

**Theorem (optimality), structure of the proof.** The depths $d_1, \ldots, d_n$ of phase 2 are the depths of some alphabetic tree, and $\sum_i w_i d_i$ equals the cost of an optimal alphabetic tree. With Lemma 3, the tree built in line L6 is then an optimal alphabetic tree.

The proof has two parts.

1. *Feasibility.* The depths from the combination phase can be realized by an alphabetic tree. The key fact is that the least compatible pair is *locally minimal*: the two nodes are not heavier than their compatible neighbours. One shows that combining such a pair never crosses a pair made later in a way that the stack in Lemma 3 can not undo, so the depths satisfy the condition of Lemma 3.

2. *Optimality.* Let $\mathcal{T}$ be the set of trees that the combination phase could build, with compatibility as the only constraint, that is the trees that need not be alphabetic but in which each combination is allowed by the square nodes left. Every alphabetic tree is in $\mathcal{T}$ in a suitable order of combinations, so the least cost over $\mathcal{T}$ is at most the least alphabetic cost. One shows, by an exchange argument in the style of the proof for Huffman's algorithm, that combining the least compatible pair first leads to a tree of least cost in $\mathcal{T}$. By part 1, that tree has the same depths, hence the same cost by Lemma 2, as an alphabetic tree. So its cost equals the optimal alphabetic cost.

The exchange argument of part 2 is the delicate step. Unlike in Huffman's proof, the two lightest compatible nodes can not always be made siblings at the deepest level of an optimal tree, because compatibility changes as square nodes disappear. Hu and Tucker handle this by a careful analysis of how the weights of nodes on a level change during the combination; Hu (1973) and Hu, Kleitman and Tamaki (1979) reorganize the argument, and Karpinski, Larmore and Rytter (1997) give a proof based on the structure of locally minimal pairs.

**Ties.** The rule for ties (least sum, then the leftmost left node, then the leftmost right node) is part of the algorithm. The tests compare this implementation with the interval dynamic program on 1500 random inputs, half of them with many equal weights, and find the same cost every time.
