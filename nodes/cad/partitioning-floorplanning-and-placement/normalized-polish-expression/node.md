---
tag: 77DCRE
kind: data-structure
slug: normalized-polish-expression
name: Normalized Polish expression
aliases:
- Polish expression floorplan
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Wong and Liu's postfix word of blocks and cut operators H and V with no repeated operator in a row, which stands one to one for slicing floorplans.
model: word-ram
complexity:
  vars: {n: the number of blocks}
  time: {worst: O(n), average: O(n), best: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1986
  people: [D. F. Wong, C. L. Liu]
  note: Wong and Liu introduced normalized Polish expressions at the 1986 Design Automation Conference, as the search space of their annealing floorplanner.
prereqs: [slicing-floorplan, reverse-polish-notation, expression-tree]
see_also: [wong-liu-floorplanning, stockmeyer-floorplan-sizing, shape-function, slicing-floorplan, sequence-pair, b-star-tree-floorplan, mosaic-floorplan, postorder-traversal]
sources:
  - paper: "D. F. Wong and C. L. Liu, A new algorithm for floorplan design, Proceedings of the 23rd ACM/IEEE Design Automation Conference, 101 to 107, 1986"
    locator: the definition of Polish and normalized Polish expressions, the balloting property, the one to one correspondence with skewed slicing trees, and the moves M1, M2 and M3
  - paper: doi:10.1007/BF01553890
    title: D. F. Wong and C. L. Liu, Floorplan design of VLSI circuits, Algorithmica 4, 263 to 291, 1989
    locator: the journal version, with normalized Polish expressions and the extension to L-shaped blocks
  - paper: doi:10.1109/DAC.1982.1585510
    title: Ralph H. J. M. Otten, Automatic floorplan design, Proceedings of the 19th Design Automation Conference, 261 to 267, 1982
    locator: slicing structures and their trees
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (floorplan representations and Polish expressions; general locator)
---

A normalized Polish expression is a word that stores a [slicing floorplan](/slicing-floorplan/). It is the postorder of the slicing tree: each block is an operand, and each cut is an operator, $V$ for a vertical cut line and $H$ for a horizontal one. Wong and Liu added one rule in 1986: no two equal operators may stand next to each other. With this rule each slicing floorplan has exactly one word, so a search over the words, such as [Wong-Liu floorplanning](/wong-liu-floorplanning/), does not visit the same floorplan twice. A word of $n$ blocks has $2n - 1$ tokens, and it can be checked, evaluated and normalized in $O(n)$ time.

## In plain words

Write a floorplan the way a calculator with a stack reads a sum. A block name means "put this block on the stack". The letter V means "take the last two parts and put them side by side". The letter H means "take the last two parts and put the first one under the second one". At the end, one part is left, and it is the whole floorplan.

Three blocks in a row can be written in two ways: first join the first two, or first join the last two. The picture is the same. The rule "never two equal letters in a row" keeps only the first way, so each picture has exactly one word.

## The abstract type

The type stores a slicing floorplan of a set $B$ of $n$ blocks as a word $E = e_1 e_2 \cdots e_{2n-1}$. Each block of $B$ occurs one time, and the other $n - 1$ tokens are the operators $H$ and $V$. The operations are:

- VALID$(E)$: tell whether $E$ is a normalized Polish expression.
- EVALUATE$(E, w, h)$: given the width $w_i$ and the height $h_i$ of each block, return the width $W$ and the height $H$ of the floorplan and the lower-left corner of each block.
- NORMALIZE$(E)$: given any Polish expression, return the normalized expression of the same floorplan.
- TO-TREE$(E)$: return the slicing tree.

This page uses the convention that $E_1 E_2 V$ puts $E_1$ to the left of $E_2$, and $E_1 E_2 H$ puts $E_1$ below $E_2$. Wong and Liu write $*$ and $+$ for the two operators, and books do not agree on which operand of a horizontal cut goes on top. The structure is the same in all conventions.

## Representation

The word is an array of $2n - 1$ tokens. A *Polish expression* is the postorder of a [slicing tree](/slicing-floorplan/), a full binary tree whose leaves are the blocks and whose internal nodes carry $H$ or $V$. This is [reverse Polish notation](/reverse-polish-notation/) for an [expression tree](/expression-tree/) with two operators. A word with $n$ operands and $n - 1$ operators is a Polish expression exactly when it has the *balloting property*: each prefix $e_1 \cdots e_k$ has more operands than operators.

The two operators are associative on floorplans: $(a\,b\,V)\,c\,V$ and $a\,(b\,c\,V)\,V$ put $a$, $b$ and $c$ side by side in the same order. So a floorplan with a chain of three or more parts in one direction has several Polish expressions. A slicing tree is *skewed* if no right child has the same operator as its parent. A Polish expression is *normalized* if it has no two equal operators next to each other. In a postorder, an operator that comes just before another operator is the right child of that operator, so the normalized expressions are exactly the postorders of the skewed trees. Each floorplan has one skewed tree: its chains are written left-deep.

## Operations

```pseudo id=main
VALID(E, n)                                   ▷ E = e_1 ... e_m
L1  if m ≠ 2n − 1 or the operands of E are not the n blocks, each one time then return false
L2  c ← 0                                     ▷ operands minus operators so far
L3  for k ← 1 to m do
L4      if e_k is an operand then c ← c + 1
L5      else
L6          c ← c − 1
L7          if c < 1 or e_{k−1} = e_k then return false
L8  return true

EVALUATE(E, w, h)                             ▷ also TO-TREE, without the sizes
L9  S ← an empty stack
L10 for k ← 1 to 2n − 1 do
L11     if e_k is a block i then push the leaf i with W = w_i, H = h_i on S
L12     else pop b, then pop a, from S
L13         if e_k = V then W ← W_a + W_b, H ← max(H_a, H_b)
L14         else W ← max(W_a, W_b), H ← H_a + H_b
L15         push the node (e_k, a, b) with W and H on S
L16 r ← the only node in S; PLACE(r, 0, 0)
L17 return W_r, H_r and the corners

PLACE(t, x, y)
L18 if t is a leaf i then (x_i, y_i) ← (x, y); return
L19 PLACE(a, x, y)                            ▷ a and b are the children of t
L20 if t has V then PLACE(b, x + W_a, y) else PLACE(b, x, y + H_a)
```

VALID counts operands minus operators in $c$. The balloting property says that $c \ge 1$ after each token, and line L7 checks this after each operator. The same line rejects two equal operators in a row. EVALUATE is the stack evaluation of a postfix word. The values $W$ and $H$ of a node are the size of the smallest rectangle that holds its part of the floorplan. PLACE then goes down the tree and gives each part its corner.

```pseudo id=normalize
NORMALIZE(E)                                  ▷ E is any Polish expression
L21 T ← the tree of E, built as in lines L9 to L15
L22 return EMIT(the root of T)

EMIT(t)
L23 if t is a leaf i then return the word i
L24 o ← the operator of t; c_1, ..., c_k ← the highest subtrees below t, left to right, whose roots are not o-nodes
L25 return EMIT(c_1) EMIT(c_2) o EMIT(c_3) o ... EMIT(c_k) o
```

Line L24 collects the parts of the maximal chain of $o$-nodes through $t$. Line L25 writes the chain left-deep, so every right child in the new tree is a part $c_i$, which is a leaf or carries the other operator.

## Example

Take four blocks with the sizes $1: 2 \times 3$, $2: 3 \times 2$, $3: 4 \times 1$ and $4: 2 \times 2$ (width by height), and the word $E = 1\,2\,V\,3\,4\,H\,V$.

| $k$ | $e_k$ | $c$ | the stack after the step (width by height) |
|---|---|---|---|
| 1 | 1 | 1 | $1{:}\,2 \times 3$ |
| 2 | 2 | 2 | $2 \times 3$, $2{:}\,3 \times 2$ |
| 3 | V | 1 | $(1\,2\,V){:}\,5 \times 3$ |
| 4 | 3 | 2 | $5 \times 3$, $3{:}\,4 \times 1$ |
| 5 | 4 | 3 | $5 \times 3$, $4 \times 1$, $4{:}\,2 \times 2$ |
| 6 | H | 2 | $5 \times 3$, $(3\,4\,H){:}\,4 \times 3$ |
| 7 | V | 1 | $(1\,2\,V\,3\,4\,H\,V){:}\,9 \times 3$ |

The value $c$ never falls below 1, and the two operators at steps 6 and 7 differ, so VALID returns true. The floorplan is $9 \times 3$. PLACE puts block 1 at $(0, 0)$ and block 2 at $(2, 0)$. The part $3\,4\,H$ starts at $x = 5$, so block 3 is at $(5, 0)$ and block 4 is at $(5, 1)$, on top of block 3. The block area is $6 + 6 + 4 + 4 = 20$ of the 27 units of the floorplan.

The word $1\,2\,3\,V\,V$ is a Polish expression, but it is not normalized: the two $V$ are next to each other, because the second block group $2\,3\,V$ is the right child of a $V$ node. NORMALIZE turns it into $1\,2\,V\,3\,V$, with the same three blocks side by side. On three blocks there are $3! \cdot 6 = 36$ normalized expressions, and on four blocks $4! \cdot 22 = 528$.

## Correctness

By the stack argument, a word with $n$ operands is a Polish expression if and only if it has $2n - 1$ tokens and the balloting property, and the tree is unique. In a postorder, the token just before an internal node is the root of its right subtree. So two operators next to each other are a node and its internal right child, and VALID accepts exactly the postorders of skewed slicing trees. EVALUATE is correct by induction on the tree: a vertical cut adds the widths and takes the larger height, a horizontal cut does the opposite, and PLACE gives the two parts disjoint rectangles on the two sides of the cut. NORMALIZE keeps the floorplan because the operators are associative, and it returns a skewed tree. Two Polish expressions have the same normalized form exactly when they differ by the associative law. The count $n!\,S_{n-1}$ of normalized words, with the large Schröder numbers $S_k = 1, 2, 6, 22, 90, 394$, follows from this. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | extra space |
|---|---|---|
| VALID | $O(n)$ | $O(n)$, a set of the operands seen |
| EVALUATE | $O(n)$ | $O(n)$, the stack and the tree |
| NORMALIZE | $O(n)$ | $O(n)$ |
| TO-TREE | $O(n)$ | $O(n)$ |

The word itself takes $2n - 1$ tokens. With $\lceil \lg n \rceil$ bits for each block name and one bit for each operator, a slicing floorplan of $n$ blocks needs about $n \lg n + 3n$ bits. The number of normalized words is $n!\,S_{n-1}$, and $\lg S_{n-1} = \Theta(n)$, so the word is optimal up to the $O(n)$ term. The bound is on the word RAM with the block sizes as integers that fit in a word.

## Variants

- **Plain Polish expressions.** Without the normalization rule a floorplan with a chain of $k$ parts has $C_{k-1}$ words, a [Catalan number](/catalan-numbers/). Otten's slicing trees are of this kind. A search over them visits the same floorplan many times.
- **Right-deep chains.** One can also write every chain right-deep. Then the rule becomes "no left child with the operator of its parent". Both normal forms are in use.
- **Shapes and orientations.** If each block has several allowed shapes, EVALUATE carries a [shape function](/shape-function/) instead of one size at each node. [Stockmeyer's floorplan sizing](/stockmeyer-floorplan-sizing/) does this for the least area.
- **Moves.** Wong and Liu change a word by three moves: swap two neighbouring operands (M1), change every operator in a run of operators to the other one (M2), and swap a neighbouring operand and operator (M3) when the result is still normalized. The moves are on the page of [Wong-Liu floorplanning](/wong-liu-floorplanning/).
- **L-shaped blocks.** The journal version of Wong and Liu adds operators for L-shaped blocks.
- **Non-slicing floorplans.** A Polish expression cannot store a pinwheel of five blocks. The [sequence pair](/sequence-pair/), the [B*-tree](/b-star-tree-floorplan/) and the [O-tree](/o-tree-floorplan/) store packings that are not slicing.

## When to use it

Use a normalized Polish expression when the floorplans are slicing, as in many hierarchical flows, and when a search changes the floorplan many times. Each word is a different floorplan, the moves are simple, and evaluation with shape functions gives the best sizes of soft blocks. If the best packing may be non-slicing, use a [sequence pair](/sequence-pair/) or a [B*-tree](/b-star-tree-floorplan/).

## Pitfalls

- **Which operand goes on top.** The meaning of $H$ differs between sources. Fix one convention and use it in the evaluation and in the moves.
- **A swap that breaks the balloting property.** Swapping an operand with the operator after it reduces the operand count of that prefix by one. Check $c \ge 1$ again, and check the two new neighbours of the operator, or the word stops being a normalized expression.
- **Normalization is not checked by the stack.** The stack evaluation of $1\,2\,3\,V\,V$ works. A search that does not call VALID can count one floorplan many times.
- **Crossing cuts.** Two cut lines that cross at one point give two different words, for example $1\,2\,H\,3\,4\,H\,V$ and $1\,3\,V\,2\,4\,V\,H$, if the parts have the same sizes. The structure regards them as two floorplans, because the cut lines can slide apart.
- **Deep recursion.** A left-deep chain of $n$ blocks gives a tree of depth $n$. Write PLACE with an explicit stack.

## Implementations

The Python class stores the word as a list of ints and the strings "H" and "V". It checks the word, evaluates it with a stack and an explicit stack for PLACE, returns the slicing tree, and normalizes any Polish expression. The tests check every word of up to five blocks against the set of postorders of all skewed slicing trees, the counts $1, 4, 36, 528, 10800$, the evaluation of every slicing tree of up to five blocks against a recursive evaluation, and 600 random trees of up to 40 blocks for the absence of overlap.

## History

Polish notation is the work of Jan Łukasiewicz in the 1920s, and the postfix form is reverse Polish notation. Otten described slicing structures and their trees for floorplan design in 1982. Wong and Liu introduced normalized Polish expressions in 1986, together with an annealing algorithm that searches over them, and extended them to L-shaped blocks in the 1989 journal version.

## References
