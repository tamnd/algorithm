---
tag: YZV6WS
kind: theorem
slug: mosaic-floorplan-baxter-theorem
name: Mosaic floorplans and Baxter numbers
aliases:
- Baxter number count of floorplans
area: cad/partitioning-floorplanning-and-placement
level: research
summary: The number of mosaic floorplans with n rooms is the nth Baxter number, as Yao, Chen, Cheng and Graham showed by a bijection with twin binary trees.
prereqs: [mosaic-floorplan, binary-tree, inorder-traversal, catalan-numbers]
see_also: [slicing-floorplan, normalized-polish-expression, bijective-proof, floorplan-constraint-graphs, sequence-pair, permutation]
sources:
  - paper: "Bo Yao, Hongyu Chen, Chung-Kuan Cheng and Ronald L. Graham, Floorplan representations: complexity and connections, ACM Transactions on Design Automation of Electronic Systems 8(1), 55 to 80, 2003"
    locator: the bijection between mosaic floorplans and twin binary trees, the count of mosaic floorplans by Baxter numbers, and the count of slicing floorplans by Schröder numbers
  - paper: "Bo Yao, Hongyu Chen, Chung-Kuan Cheng and Ronald L. Graham, Revisiting floorplan representations, Proceedings of the International Symposium on Physical Design, 138 to 143, 2001"
    locator: the first version of the twin binary tree bijection and the Baxter number count
  - paper: doi:10.1016/S0012-365X(97)00112-X
    title: Serge Dulucq and Olivier Guibert, Baxter permutations, Discrete Mathematics 180(1-3), 143 to 156, 1998
    locator: twin binary trees and their bijection with Baxter permutations
  - paper: "F. R. K. Chung, R. L. Graham, V. E. Hoggatt and M. Kleiman, The number of Baxter permutations, Journal of Combinatorial Theory, Series A 24(3), 382 to 394, 1978"
    locator: the closed formula for the number of Baxter permutations of n
  - paper: doi:10.1109/ICCAD.2000.896442
    title: Xianlong Hong, Gang Huang, Yici Cai, Jiangchun Gu, Sheqin Dong, Chung-Kuan Cheng and Jun Gu, Corner block list, an effective and efficient topological representation of non-slicing floorplan, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 8 to 12, 2000
    locator: the representation of mosaic floorplans by the removal of corner rooms one at a time
---

The Baxter number theorem counts the [mosaic floorplans](/mosaic-floorplan/): with $n$ rooms there are exactly $B(n)$ of them, where $B(n)$ is the $n$th Baxter number $1, 2, 6, 22, 92, 422, 2074, \ldots$. Yao, Chen, Cheng and Graham proved it in 2001 with a bijection between mosaic floorplans and twin binary trees, pairs of [binary trees](/binary-tree/) that Dulucq and Guibert had already put in bijection with Baxter permutations. The theorem fixes the size of the search space of every floorplanner that works with mosaic floorplans: it grows like $8^n$, against about $5.83^n$ for [slicing floorplans](/slicing-floorplan/), and any code for a mosaic floorplan needs about $3 n$ bits.

## Statement

A mosaic floorplan with $n$ rooms is a division of a rectangle into $n$ rectangular rooms in which no four rooms meet at a point, taken up to sliding of its segments (see [mosaic floorplan](/mosaic-floorplan/)). The Baxter numbers are

$$
B(n) = \frac{1}{\binom{n+1}{1}\binom{n+1}{2}} \sum_{k=1}^{n} \binom{n+1}{k-1}\binom{n+1}{k}\binom{n+1}{k+1}, \qquad n \ge 1.
$$

For a binary tree $\tau$ with $n$ nodes, list its nodes in [inorder](/inorder-traversal/) $v_1, \ldots, v_n$, and let its *canopy* be the word $c(\tau) = c_1 \cdots c_{n-1}$ with $c_i = 1$ if $v_i$ has a right child and $c_i = 0$ if it does not. A *twin binary tree* pair is a pair $(\tau_1, \tau_2)$ of binary trees on the same $n$ nodes with the same inorder and complementary canopies: $c(\tau_2)$ is $c(\tau_1)$ with each bit flipped. As unlabeled objects, a twin pair is a pair of tree shapes with $n$ nodes each whose canopies are complementary.

**Theorem (Yao, Chen, Cheng and Graham).** There is a bijection between the mosaic floorplans with $n$ rooms and the twin binary tree pairs with $n$ nodes. So the number of mosaic floorplans with $n$ rooms is $B(n)$.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $B(n)$ | 1 | 2 | 6 | 22 | 92 | 422 | 2074 | 10754 | 58202 | 326240 |

## In plain words

Count the ways to cut a chip into a given number of rectangular rooms, where only the pattern matters and not the exact sizes. The answer is a known sequence, the Baxter numbers. The proof turns each pattern into two binary trees. The first tree hangs each room on the room below it or on the room to its left, as seen from the lower left corner of the room. The second tree does the same from the upper right corner, with the rooms above and to the right. The two trees visit the rooms in the same order, and at each room exactly one of the two trees goes on to the right. Pairs of trees with this property were already known and counted, so the floorplans are counted as well. The count grows by a factor of about eight for each extra room.

## Proof

Fix a mosaic floorplan $F$ in the rectangle $[0, W] \times [0, H]$. Each corner of a room other than the four corners of the rectangle is a T-junction: exactly one of the two lines through it goes on past it on both sides, and the other one ends there.

**The two trees.** The tree $\tau_1$ has its root at the room with the lower-left corner $(0, 0)$. For each other room $r$, let $p$ be its lower-left corner.

- If the vertical line through $p$ goes on below $p$, the parent of $r$ is the room below $p$ whose left side is on that line, and $r$ is its right child.
- Otherwise the horizontal line through $p$ goes on to the left of $p$, the parent of $r$ is the room to the left of $p$ whose bottom side is on that line, and $r$ is its left child.

The tree $\tau_2$ is the same from the upper-right corner. Its root is the room with the corner $(W, H)$. For each other room $r$ with upper-right corner $q$: if the vertical line through $q$ goes on above $q$, the parent of $r$ is the room above $q$ whose right side is on that line, and $r$ is its left child. Otherwise the parent of $r$ is the room to the right of $q$ whose top side is on that line, and $r$ is its right child.

These are binary trees. A T-junction makes exactly one case hold, so each room except the root has one parent. The parent's lower-left corner is lower, or at the same height and further left, so the parent relation has no cycle and leads to the root. A room $u$ has at most one right child in $\tau_1$, the room whose lower-left corner is the upper-left corner of $u$, and at most one left child, the room whose lower-left corner is the lower-right corner of $u$. The same holds for $\tau_2$. Sliding segments does not change which room is at which corner, so $\tau_1$ and $\tau_2$ depend only on the equivalence class.

**The corner room.** Let $R = [a, W] \times [0, d]$ be the room at the lower-right corner. The rooms on the bottom side of the rectangle form a chain of left children from the root of $\tau_1$, and $R$ is the last of them. The rooms on the right side form a chain of left children from the root of $\tau_2$, and $R$ is again the last. No room is a left child of $R$ in either tree, so $R$ is the first node in the inorder of both trees. Let $q = (a, d)$ be the upper-left corner of $R$. If $n \ge 2$, exactly one of two cases holds at $q$.

- *Case top.* The vertical line through $q$ goes on above $q$. Then the room $X$ with lower-left corner $q$ is the right child of $R$ in $\tau_1$. The top side of $R$ is a whole segment, and the rooms above it are $X$ and the chain of left children that starts at $X$ in $\tau_1$. In $\tau_2$, a right child of $R$ would be a room whose upper-right corner is $q$ and whose right side ends at $q$, which the line above $q$ forbids, so $R$ has no right child in $\tau_2$.
- *Case left.* The horizontal line through $q$ goes on to the left of $q$. Then no room has its lower-left corner at $q$, so $R$ has no right child in $\tau_1$. The left side of $R$ is a whole segment. The room just to the left of $q$ and below it has upper-right corner $q$, its right side ends at $q$, and its top side is on the line of the top side of $R$, so it is the right child of $R$ in $\tau_2$.

So the first canopy bit of $\tau_1$ is $1$ and that of $\tau_2$ is $0$ in case top, and the other way round in case left.

**Removing the corner room.** In case top, delete $R$ and stretch the rooms above it down to the bottom side. The result $F'$ is a mosaic floorplan with $n - 1$ rooms. In $F'$, the room $X$ takes the place of $R$ as the left child of the parent of $R$ in $\tau_1$, and all other parents in $\tau_1$ stay the same, so $\tau_1(F')$ is $\tau_1$ with $R$ spliced out. In $\tau_2$, the room $R$ is a leaf, and no other room has its upper-right corner moved, so $\tau_2(F')$ is $\tau_2$ with the leaf $R$ removed. Case left is the same with the two trees swapped and the rooms to the left of $R$ stretched to the right side. Splicing out a first node keeps the inorder of the others, and it keeps the right children of all other nodes, so the canopies of $F'$ are those of $F$ with the first bit removed. By induction on $n$, the two trees of $F'$ have the same inorder and complementary canopies, and with $R$ in front the same holds for $F$. So the map $\Phi(F) = (\tau_1, \tau_2)$ sends mosaic floorplans to twin binary tree pairs.

**One to one.** From $(\tau_1, \tau_2)$ the floorplan is rebuilt. The first node in the inorder is $R$, and the tree in which $R$ has a right child tells the case. In case top, the number $k$ of rooms above $R$ is the length of the chain of left children that starts at the right child of $R$ in $\tau_1$. Splicing out $R$ gives the twin pair of $F'$, which by induction gives $F'$. Then $F$ is $F'$ with a new room $R$ put under the last $k$ rooms along the bottom side, below a new segment that ends on the left at the left side of the first of these $k$ rooms. Case left is the same with $\tau_2$ and the right side. So $\Phi$ is one to one.

**Onto, and the count.** Yao, Chen, Cheng and Graham show that every twin binary tree pair is $\Phi(F)$ for some mosaic floorplan $F$, by building $F$ from the pair. Dulucq and Guibert give a bijection between twin binary tree pairs with $n$ nodes and Baxter permutations of $\{1, \ldots, n\}$, and Chung, Graham, Hoggatt and Kleiman prove that the number of Baxter permutations of $\{1, \ldots, n\}$ is $B(n)$. So the number of mosaic floorplans with $n$ rooms is $B(n)$. $\blacksquare$

## Consequences

- **Growth rate $8$.** Each term of the sum is at most $(2^{n+1})^3 = 8^{n+1}$, so $B(n) \le n \cdot 8^{n+1}$. For the middle index $k = \lfloor (n+1)/2 \rfloor$, the middle binomial coefficient is at least $2^{n+1} / (n+2)$, and its two neighbors are at least a third of it, so $B(n) \ge 8^{n+1} / (9 (n+2)^3 (n+1)^3)$. Hence $B(n)^{1/n} \to 8$. The ratios $B(n+1) / B(n)$ are about $5.77$ at $n = 10$ and $7.84$ at $n = 200$.
- **Slicing floorplans are rare.** The slicing floorplans are counted by the large Schröder numbers $S_{n-1}$, whose growth rate is $3 + 2 \sqrt{2} \approx 5.83$. The generating function $t(x)$ of the trees with no node of one child, which the slicing floorplan page uses for the count, satisfies $t = x + t^2 / (1 - t)$, that is $2 t^2 - (1 + x) t + x = 0$, and the discriminant $1 - 6 x + x^2$ vanishes first at $x = 3 - 2\sqrt{2}$. So the fraction of mosaic floorplans that are slicing goes to $0$ exponentially.
- **Code length.** A code that tells apart all mosaic floorplans with $n$ rooms needs at least $\log_2 B(n) = 3 n - O(\log n)$ bits, and with $n$ labeled blocks at least $\log_2 (n! \, B(n))$ bits.
- **Search spaces.** A floorplanner that enumerates or samples mosaic floorplans works in a space of size $n! \, B(n)$ for labeled blocks. The [sequence pair](/sequence-pair/), which describes packings with empty space, has $(n!)^2$ codes, and the ratio $(n!)^2 / (n! \, B(n)) = n! / B(n)$ grows faster than any exponential function of $n$.

## Tightness

The theorem is an exact count, so there is no gap to close. The comparison with slicing floorplans is also exact at the start: $B(n) = S_{n-1}$ for $n \le 4$, with the values $1, 2, 6, 22$, so every mosaic floorplan with at most four rooms is slicing. The first difference is at $n = 5$, where $B(5) = 92$ and there are $90$ slicing floorplans, and the two missing ones are the pinwheel and its mirror image. Without the rule that no four rooms meet, the class changes: a division with a point where four rooms meet is not a mosaic floorplan, and it is counted as two mosaic floorplans, one for each way to pull the four rooms apart.

## History

Baxter permutations are named after Glen Baxter, who met them in 1964 in a question about fixed points of commuting functions. Chung, Graham, Hoggatt and Kleiman found the closed formula for their number in 1978. Dulucq and Guibert gave the bijection with twin binary trees in 1998. In floorplanning, Hong and others gave the corner block list for mosaic floorplans in 2000, which also takes corner rooms away one at a time, as the proof above does. Yao, Chen, Cheng and Graham showed in 2001, and in the journal version of 2003, that mosaic floorplans are in bijection with twin binary trees, so their number is the Baxter number, and that slicing floorplans are counted by the Schröder numbers.

## References
