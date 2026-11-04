---
tag: S2YFZ3
kind: technique
slug: node-copying
name: Node copying
aliases:
- node-copying method
- Driscoll et al. node copying
area: data-structures/persistent-structures
level: advanced
summary: Make a pointer structure of bounded in-degree partially persistent by logging changes in a few spare slots per node and copying a node only when its slots are full.
prereqs: [partial-persistence, fat-node]
see_also: [dsst-persistence-theorem, path-copying, full-persistence, persistent-red-black-tree, sarnak-tarjan-point-location, persistent-binary-search-tree, potential-method, historical-queries]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: pages 86 to 124, the section on partial persistence (the node-copying method and its amortized analysis) and the section on full persistence (node splitting)
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
    locator: pages 669 to 679 (a persistent search tree with extra pointer fields per node and O(1) amortized space per update)
  - paper: doi:10.7146/brics.v1i35.21608
    title: Gerth Stølting Brodal, Partially persistent data structures of bounded degree with constant update time, BRICS Report Series RS-94-35, 1994
    locator: the main theorem (node copying with worst-case O(1) cost per update step)
---

Node copying is the method of Driscoll, Sarnak, Sleator and Tarjan for making a linked data structure [partially persistent](/partial-persistence/) at a constant cost. Each node gets a constant number of spare slots. A change of a field is written into a free slot, stamped with the version number, as in the [fat node](/fat-node/) method. When a node has no free slot, it is copied with its newest values, and the few nodes that point to it are changed to point to the copy, which may copy them in turn. If every node has in-degree at most a constant $p$, an access step takes $O(1)$ time and an update step $O(1)$ amortized time and space. This is part 1 of the [DSST persistence theorem](/dsst-persistence-theorem/). For [full persistence](/full-persistence/) the same idea becomes node splitting.

## In plain words

Each box of the structure has a small margin where changes are written with their date. Reading a box as of some date means reading the box and the dated notes in its margin, which is quick because the margin is small. When the margin is full, you make a clean copy of the box with its newest content and an empty margin. The boxes that point to the old box must now point to the copy, and you write that change in their margins. Only a few boxes point to any one box, and a box is copied only after many changes have filled its margin, so the copying is paid for by the changes that came before it.

## When it applies

- **A linked structure with bounded in-degree.** Nodes have at most $d$ fields, and at most $p$ fields point to any node, for constants $d$ and $p$, at every moment of every update. Lists, trees without parent pointers, and trees with parent pointers ($p = 3$) qualify.
- **Partial persistence.** Old versions are read and only the newest version is changed. The method keeps one "live" copy of each node, which belongs to the newest version.
- **Amortized costs are acceptable.** One change can start a chain of copies. The total over a sequence is linear, but a single step is not bounded by a constant. Brodal's variant removes this.

## The template

Each node has its original fields, $k \ge p$ slots that hold triples (field, version, value), and a set $\text{back}(x)$ of the pairs (node, field) of the live nodes that point to $x$ in the newest version. $E[i]$ holds the entry pointers of version $i$, and $t$ is the version under construction.

```pseudo id=main
READ(x, f, i)
L1  for each filled slot (g, s, v) of x, from the last to the first do
L2      if g = f and s ≤ i then return v
L3  return the original field f of x

CHANGE(y, f, v, t)                      ▷ set field f of the live node y to v in version t
L4  if y has a free slot then
L5      write (f, t, v) into it; return
L6  y′ ← a new node with the values READ(y, ·, t), field f set to v, pointers to y set to y′, no filled slot
L7  for each field of y′ that points to a node z: replace y by y′ in back(z)
L8  replace y by y′ in E[t]
L9  for each (z, g) in back(y) with z ≠ y do CHANGE(z, g, y′, t)
```

A version $t$ starts with $E[t] \leftarrow E[t - 1]$, and then runs the ephemeral update with READ$(\cdot, \cdot, t)$ and CHANGE. A pointer change also moves one pair from the back set of the old target to that of the new one. After line L6, $y$ is no longer live, and no later version reaches it.

**Why it works.** No line writes an original field of an old node or a slot with a stamp below $t$, so a read in a version $i < t$ returns the same values as before. In version $t$, the copy $y'$ holds the same values as $y$ with $f$ changed, and lines L8 and L9 move every pointer to $y$ in version $t$ to $y'$, since such a pointer is an entry pointer or a pair of $\text{back}(y)$. The full proof is on the page [DSST persistence theorem](/dsst-persistence-theorem/).

**Cost.** Let $u$ be the number of ephemeral field changes, $W$ the number of slot writes and $C$ the number of copies. Each call of CHANGE does one write or one copy, and each call is one of the $u$ changes or one of the at most $p$ calls of line L9, so $W + C \le u + pC$. A node is copied at most once and only when its $k$ slots are full, so $W \ge kC$. Then $(k + 1 - p) C \le u$, so $C \le u$ and $W \le (p + 1) u$. A copy costs $O(d + k + dp)$ time and $O(d + k + p)$ space, and a write $O(p)$ time. So the total cost of the updates is $O(u)$ time and space, and a read is $O(k)$ time.

## Classic examples

### A trace on a linked list

Take a singly linked list with an entry pointer to its head: nodes $A, B, C$ with values $1, 2, 3$. Each node has in-degree at most $p = 1$, and we give it $k = 1$ slot.

| version | change | what happens |
|---|---|---|
| 1 | $B.\text{val} \leftarrow 20$ | write $(\text{val}, 1, 20)$ into $B$ |
| 2 | $B.\text{val} \leftarrow 21$ | $B$ is full: copy $B'$ with value 21; CHANGE$(A, \text{next}, B')$ writes $(\text{next}, 2, B')$ into $A$ |
| 3 | $B'.\text{val} \leftarrow 22$ | write $(\text{val}, 3, 22)$ into $B'$ |
| 4 | $C.\text{val} \leftarrow 30$ | write $(\text{val}, 4, 30)$ into $C$ |
| 5 | $C.\text{val} \leftarrow 31$ | $C$ is full: copy $C'$; $B'$ is full: copy $B''$ with value 22 and next $C'$; $A$ is full: copy $A'$ with next $B''$; $E[5] \leftarrow A'$ |

Version 5 shows the cascade: one change made three copies. The counts agree with the bound: $u = 5$ changes, $W = 4$ writes and $C = 4$ copies, so $W \ge kC$, $W + C = 8 \le u + pC = 9$ and $(k + 1 - p) C = 4 \le 5$. A read of version 1 starts at $E[1] = A$. The slot of $A$ has stamp $2 > 1$, so $A.\text{next}$ is $B$ in version 1. The slot of $B$ gives the value 20, and $B.\text{next} = C$ with the value 3. So version 1 is $1, 20, 3$, and version 5 is $1, 22, 31$.

### Other examples

- **Persistent red-black trees.** Sarnak and Tarjan applied the method to [red-black trees](/red-black-tree/), whose insertions and deletions change $O(1)$ fields amortized. The result is a partially persistent search tree with $O(\log n)$ time per search in any version and $O(1)$ amortized space per update. See [persistent red-black tree](/persistent-red-black-tree/).
- **Planar point location.** The persistent tree over a plane sweep gives [Sarnak-Tarjan point location](/sarnak-tarjan-point-location/) in $O(n)$ space and $O(\log n)$ query time, where [path copying](/path-copying/) would use $O(n \log n)$ space.
- **Multiversion B-trees.** Database indexes that keep old versions of a [B-tree](/b-tree/) use a similar rule: a node is copied with its live entries when it becomes full.

## Variations

- **Node splitting.** For full persistence, the slots are stamped with positions in a version list. A full node is split into two nodes for two ranges of the list instead of being copied. This gives the full-persistence part of the DSST theorem.
- **Worst-case bounds.** Brodal (1994) showed how to schedule the copies so that every update step costs $O(1)$ in the worst case, for partial persistence.
- **Fat nodes.** With unbounded slots, nothing is ever copied and the method becomes the [fat node](/fat-node/) method, with $O(\log m)$ reads.
- **Path copying.** Copying every node on the path to the change, with no slots, is [path copying](/path-copying/). It gives full persistence directly, at $O(\log n)$ space per update in a balanced tree.

## Pitfalls

- **Unbounded in-degree.** A node that many nodes point to, such as a shared sentinel or a header node in every list cell, makes each copy expensive. Remove such pointers, or treat that node separately.
- **Back pointers are not versioned.** The back sets describe only the newest version and are changed in place. Using them to navigate an old version gives wrong answers.
- **Too few slots.** The counting argument needs $k \ge p$. With fewer slots, a chain of copies can feed itself and the cost is not bounded.
- **Intermediate states.** The in-degree bound must hold also in the middle of an update. An ephemeral algorithm that points many nodes at one node for a moment breaks the analysis.
- **Amortized, not worst case.** A single update can copy many nodes, as version 5 of the trace does. A real-time application needs Brodal's method or a bound on the cascade.

## Exercises

1. Continue the trace with version 6: $A'.\text{val} \leftarrow 10$, then version 7: $A'.\text{val} \leftarrow 11$. Which nodes are copied, and what does version 6 read?
2. Redo the trace with $k = 2$ slots per node. How many copies are made?
3. Where does the counting argument fail when $k < p$? Which inequality still holds, and why does it no longer bound $C$?
4. A binary search tree with parent pointers has in-degree 3. Count the number of CHANGE calls made by one rotation, without the copies they cause.

## References
