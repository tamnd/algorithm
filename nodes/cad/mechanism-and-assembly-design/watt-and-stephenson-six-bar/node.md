---
tag: 9ZDAJD
kind: definition
slug: watt-and-stephenson-six-bar
name: Watt and Stephenson six-bar linkages
aliases:
- six-bar linkage types
area: cad/mechanism-and-assembly-design
level: core
summary: The two kinds of one degree of freedom six-bar chains, which differ in whether the two ternary links are joined directly (Watt) or not (Stephenson).
prereqs: [grubler-formula, kinematic-chain, four-bar-linkage]
see_also: [degrees-of-freedom-analysis, kinematic-pair, roberts-chebyshev-theorem, instant-center-of-velocity, aronhold-kennedy-theorem, vector-loop-closure, coupler-curve, kinematic-synthesis]
sources:
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Sections 2.7 (p. 42, number synthesis), 2.9 (p. 47, isomers) and 2.14 (p. 62, linkages of more than four bars, the sixbar on p. 63)
  - book: isbn:9780190264482
    title: John J. Uicker, Gordon R. Pennock and Joseph E. Shigley, Theory of Machines and Mechanisms, 5th edition, Oxford University Press, 2017
    locator: Chapter 1, the sections on mobility, number synthesis and the Watt and Stephenson six-bar chains
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 6 (pp. 125 to 154), multiloop planar linkages, the Watt and Stephenson six-bars
  - book: isbn:9780198561248
    title: Kenneth H. Hunt, Kinematic Geometry of Mechanisms, Oxford University Press, 1978
    locator: the chapter on mobility and the enumeration of planar chains (general locator)
---

A six-bar linkage is a closed planar chain of six rigid links joined by seven revolute joints, with one degree of freedom. There are exactly two such chains up to the way the links are connected. Both have two ternary links, with three joints each, and four binary links, with two joints each. In the **Watt chain** the two ternary links are joined to each other directly; in the **Stephenson chain** they are not. Fixing different links gives the inversions, two for Watt and three for Stephenson, and these five are the basic one degree of freedom six-bar mechanisms.

This page classifies the chains. The count of degrees of freedom that the classification starts from is the [Grübler formula](/grubler-formula/), and the general question of when that count is right is on the [degrees of freedom analysis](/degrees-of-freedom-analysis/) page.

## Definition

A **planar kinematic chain** here is a finite set of rigid links in the plane, joined by revolute joints, each joint joining exactly two links (a [kinematic pair](/kinematic-pair/) with one degree of freedom). Its **graph** has a vertex for each link and an edge for each joint. A link with $k$ joints is *binary*, *ternary* or *quaternary* for $k = 2, 3, 4$. A chain is **closed** when every link has at least two joints, and **connected** when its graph is.

By the [Grübler formula](/grubler-formula/), a chain of $n$ links and $j$ such joints, with one link fixed, has the mobility

$$M = 3(n - 1) - 2j.$$

A sub-chain of $k$ links, with the $j'$ joints among them, has the count $3(k - 1) - 2j'$. If that count is $0$ or less for some sub-chain with $k \ge 2$, the sub-chain is rigid in general and acts as one link, so the chain is really a chain with fewer links. A chain is called **proper** here when no sub-chain with $k \ge 2$ links has a count of $0$ or less.

**Definition.** A *six-bar chain* is a connected, closed, proper planar chain with $n = 6$ links and $M = 1$. The **Watt chain** is the one whose two ternary links share a joint. The **Stephenson chain** is the one whose two ternary links do not.

### Theorem: there are exactly two

**Claim.** Up to relabeling the links, the Watt chain and the Stephenson chain are the only six-bar chains.

*Proof.* **Step 1, the joint count.** $M = 1$ and $n = 6$ give $1 = 15 - 2j$, so $j = 7$. Let $n_k$ be the number of links with $k$ joints. Each joint has two ends, so $\sum_k k n_k = 14$, and $\sum_k n_k = 6$ with $k \ge 2$. Subtract twice the second sum from the first: $\sum_k (k - 2) n_k = 2$. So either one quaternary link and five binary links, or two ternary links and four binary links.

**Step 2, what properness forbids.** Two links with two joints between them have the count $3 - 4 = -1$. Three links joined in a triangle have $6 - 6 = 0$. So a proper chain has no double joint and no triangle.

**Step 3, the quaternary case is impossible.** Remove the quaternary link $Q$. The five binary links keep $7 - 4 = 3$ joints among themselves, and each has at most two, so they form paths and cycles. A cycle of binary links has no joint left for anything else and would be cut off from $Q$, which contradicts connectedness. So they form $5 - 3 = 2$ paths, and the four ends of these paths take the four joints of $Q$, so each path has both ends on $Q$. A path of one binary link gives a double joint with $Q$. So the paths have 2 and 3 links. The path of 2 links closes a triangle with $Q$. Both are forbidden by step 2.

**Step 4, the two ternary links.** Let $T_1$ and $T_2$ be the ternary links. As in step 3, the binary links form paths, now with ends on $T_1$ or $T_2$, and a direct joint between $T_1$ and $T_2$ counts as a path of $0$ binary links. The six joint ends of $T_1$ and $T_2$ are used by three paths.

*A path from $T_1$ back to $T_1$.* Then $T_1$ has one end left, and $T_2$ has three, so the other two paths are one from $T_2$ back to $T_2$ and one from $T_1$ to $T_2$. A path of $m$ binary links from a ternary link back to itself closes a loop of $m + 1$ links. By step 2, $m = 1$ is a double joint and $m = 2$ a triangle, so $m \ge 3$. Two such loops need at least 6 binary links, but there are only 4.

*Three paths from $T_1$ to $T_2$.* Let them have $m_1 \le m_2 \le m_3$ binary links, with $m_1 + m_2 + m_3 = 4$. Two of the paths close a loop of $m_i + m_k + 2$ links, so step 2 needs $m_i + m_k \ge 2$ for every pair, and also not two paths with $m = 0$. The partitions of 4 into three parts are:

| $(m_1, m_2, m_3)$ | loops | verdict |
|---|---|---|
| $(0, 0, 4)$ | a double joint | forbidden |
| $(0, 1, 3)$ | a triangle | forbidden |
| $(0, 2, 2)$ | 4, 4 and 6 links | Watt: $T_1$ and $T_2$ share a joint |
| $(1, 1, 2)$ | 4, 5 and 5 links | Stephenson: $T_1$ and $T_2$ do not |

**Step 5, the two survivors are proper.** The graph has $7 - 6 + 1 = 2$ independent cycles. A sub-chain of $k$ links whose graph has $c$ independent cycles has $j' = k - 1 + c$ joints if it is connected, and fewer otherwise. If $c = 0$, its count $3(k - 1) - 2(k - 1) = k - 1$ is positive for $k \ge 2$. If $c = 1$, its count is $3(k - 1) - 2k = k - 3$, which is $0$ or less only for a loop of at most 3 links, and the table shows there is none. A sub-chain with $c = 2$ must contain all three paths, because removing any link of a path breaks the two loops through it, so it is the whole chain. So both chains are proper, and they are different because in one the ternary links share a joint and in the other they do not. $\blacksquare$

A brute-force check agrees. Of the $\binom{15}{7} = 6435$ graphs with 7 edges on 6 labeled vertices, 5700 are connected, 990 of those have every degree at least 2, and 360 are proper. Sorted by a canonical relabeling, the 360 fall into exactly two classes, the Watt and the Stephenson graph, and the 630 rejected graphs into three classes, each with a triangle.

### Inversions

An inversion is the choice of the fixed link. Two choices give the same mechanism when a symmetry of the graph maps one to the other. The Watt graph has 4 symmetries and its links fall into 2 classes: the two ternary links, and the four binary links. So there are 2 Watt inversions, often called Watt I and Watt II. The Stephenson graph has 4 symmetries and 3 classes of links: the two ternary links, the two binary links that form a path alone, and the two binary links of the path of 2. So there are 3 Stephenson inversions, often called Stephenson I, II and III. Books do not all number them in the same way, so here they are named by the fixed link.

- **Watt, ternary link fixed.** The fixed ternary link carries three pivots. The two loops of 4 links are two four-bars in series: the output of the first is the other ternary link, which is also the input of the second.
- **Watt, binary link fixed.** One loop of 4 links is a four-bar with a grounded ternary link and a ternary coupler, and a two-link dyad joins the grounded ternary link to the coupler.
- **Stephenson, ternary link fixed.** A four-bar whose coupler is the other ternary link, with a dyad from the coupler back to a pivot on the ground.
- **Stephenson, a binary link of a one-link path fixed.** Both ternary links pivot on the ground and form a four-bar with the other one-link path, and a dyad joins the two ternary links.
- **Stephenson, a binary link of the path of 2 fixed.** One ternary link and one binary link pivot on the ground. The other ternary link hangs from the grounded binary link and from two binary links to the grounded ternary link. Both loops through the fixed link have 5 links, so no four-bar contains the ground.

## Examples and non-examples

**Counting checks.** Both chains have $n = 6$ and $j = 7$, so $M = 3 \cdot 5 - 2 \cdot 7 = 1$. They have $j - n + 1 = 2$ independent loops, so a [vector loop closure](/vector-loop-closure/) analysis has two complex loop equations in four unknown angles, which leaves one free angle. They have $\binom{6}{2} = 15$ [instant centers](/instant-center-of-velocity/), of which the 7 joints give 7 directly, and the [Aronhold-Kennedy theorem](/aronhold-kennedy-theorem/) gives the others.

**Watt with a ternary link fixed, two four-bars in series.** Fix $T_1$ with pivots $O_2$, $O_4$ and $O_6$. The input turns about $O_2$, a coupler joins it to $T_2$, which turns about $O_4$, and $T_2$ drives the second coupler and the output about $O_6$. The position analysis is two four-bar analyses one after the other: the output angle of the first four-bar is, up to a constant, the input angle of the second. Each stage has two assemblies, so the whole linkage has up to 4 assemblies at a given input angle.

**Stephenson with a ternary link fixed.** Here the input is part of a four-bar whose coupler is the ternary link $T_2$, and a dyad joins a point of that coupler to a third ground pivot. The analysis is a four-bar followed by a dyad: the coupler point comes from the four-bar, and the dyad from the intersection of two circles. Six-bars of this kind are used to add a dwell to a coupler-curve motion: when the [coupler curve](/coupler-curve/) has a part that is nearly a circular arc, a dyad whose length is the radius of that arc stays almost still while the point moves along it.

**Stephenson with a binary link of the path of 2 fixed, driven at the ternary link.** Now the grounded ternary link $T_1$ is the input. The other ternary link $T_2$ is held by three binary links, two to $T_1$ and one to the ground, like the platform of a small planar parallel manipulator. Its position satisfies the two loop equations together and is not found by one four-bar and one dyad in turn, so this inversion needs a joint solution of both loops, for example by [Newton's method for systems](/newton-method-for-systems/) from a nearby known position.

**Non-example: a six-link chain with a triangle.** The graph with ternary links $T_1$, $T_2$ joined directly, and paths of 1 and 3 binary links between them, has $n = 6$, $j = 7$ and $M = 1$ by the count. But $T_1$, $T_2$ and the single binary link form a rigid triangle, so the chain is a four-bar in disguise. The Grübler count alone does not see this, which is why the definition asks for a proper chain.

**Non-example: one quaternary link.** Six links with one quaternary link and five binary links also have $j = 7$ and $M = 1$ by the count, but by step 3 every such chain has a double joint or a triangle.

**Non-example: the five-bar.** Five links in one loop have $j = 5$ and $M = 3 \cdot 4 - 10 = 2$, so a five-bar needs two inputs. If a pair of gears ties two of its links together, as in the geared five-bar cognates of the [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/) page, the mobility drops to 1, but the gear pair is a different kind of joint and the chain is not one of the two above.

**Non-example: special lengths.** The classification is by the graph alone. For special lengths, such as links that form parallelograms, a chain can move more than its count says. Those exceptions belong to the [degrees of freedom analysis](/degrees-of-freedom-analysis/) page.

## Related definitions

- [Grübler formula](/grubler-formula/): the count $M = 3(n - 1) - 2j$ that gives $j = 7$.
- [Kinematic chain](/kinematic-chain/) and [kinematic pair](/kinematic-pair/): the chain and joint types used here.
- [Four-bar linkage](/four-bar-linkage/): the only proper chain with $M = 1$ and four links, and the loops of every six-bar.
- [Degrees of freedom analysis](/degrees-of-freedom-analysis/): when the count is wrong for special lengths.
- [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/): cognates, which give six-bars with parallel motion.
- [Kinematic synthesis](/kinematic-synthesis/): design methods for six-bars, often built from a four-bar and a dyad.

### Number synthesis

The enumeration above is a case of number synthesis: list the graphs with given $n$ and $M$, and remove those with rigid sub-chains or that are the same up to relabeling. For $M = 1$ the same method gives 1 chain with 4 links, 2 with 6 links and 16 with 8 links. The 8-link count is a standard result in Hunt and in Norton Section 2.7, and is not checked on this page.

### History

The two chains are named after James Watt and George Stephenson, engineers of the steam engine and the locomotive. The classification of planar chains by their graphs, and the counts for 6 and 8 links, were worked out in the 19th and early 20th centuries and are given in the texts of Hunt and of Uicker, Pennock and Shigley.

## References
