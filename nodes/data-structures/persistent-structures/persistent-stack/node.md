---
tag: WF0RT5
kind: data-structure
slug: persistent-stack
name: Persistent stack
aliases:
- persistent linked stack
- cons list
area: data-structures/persistent-structures
level: intro
summary: An immutable linked list in which push shares the existing tail and pop returns the tail.
implements: [stack]
model: pointer-machine
complexity:
  vars: {n: the number of items in the version, k: the number of items in the first stack of an append, p: the number of pushes done}
  time: {push: Θ(1), pop: Θ(1), top: Θ(1), is_empty: Θ(1), size: Θ(1), append: Θ(k)}
  space: {total: Θ(p)}
history:
  year: 1960
  people: [John McCarthy]
  note: Lisp lists, built from cons cells that share their tails, are persistent stacks.
prereqs: [stack, singly-linked-list, persistent-data-structure]
see_also: [structural-sharing, purely-functional-data-structure, version-tree, path-copying, real-time-queue, skew-binary-random-access-list, banker-queue, zipper]
sources:
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.1 Lists (the stack signature, sharing of tails, and the cost of append and update)
  - paper: doi:10.1145/367177.367199
    title: John McCarthy, Recursive functions of symbolic expressions and their computation by machine, Part I, Communications of the ACM 3(4), 1960
    locator: the representation of S-expressions by list structure, and the functions car, cdr and cons
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: Section 1 (the definitions of persistence for linked data structures)
  - url: https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/
    title: Erik Demaine, MIT 6.851 Advanced Data Structures, Spring 2012
    locator: Lecture 1, Persistent data structures
---

A persistent stack is a [stack](/stack/) stored as a [singly linked list](/singly-linked-list/) whose nodes never change after they are made. Push makes one new node that points to the old top, and pop returns the node below the top, so each operation takes $\Theta(1)$ time and the old version stays valid. All versions share their common tails, so $p$ pushes use $\Theta(p)$ nodes in total, however many versions they make. It is the simplest [persistent data structure](/persistent-data-structure/), and it is the list of Lisp and of each functional language.

## In plain words

Think of a chain of cards, where each card names the card below it. The top of a stack is one card, and you read the stack by following the names down.

To push an item, write it on a new card that names the old top card. Nothing on the old cards changes, so the person who holds the old top card still has the old stack. To pop, hand back the card that the top card names. Again nothing changes.

Many people can hold different top cards that lead into the same chain. They all share the cards below the point where their stacks split. No card is ever copied and no card is ever changed.

## The abstract type

A persistent stack implements the [stack](/stack/) type with the value semantics of the signature $\text{push}(S, x) \to S$ and $\text{pop}(S) \to (x, S)$: each update returns a new stack and leaves its argument as it was. The operations are `new`, `push`, `pop`, `top`, `is_empty` and `size`. Since every version stays valid, the structure is fully persistent: any version can be the input of any operation.

## Representation

A stack is either $\text{nil}$ (the empty stack) or a pointer to a node $s$ with three fields: the item $s.item$, the pointer $s.next$ to the rest of the stack, and the count $s.size$.

**Invariant.** (I1) No field of a node changes after the node is made. (I2) For each node, $s.size = 1 + \text{size}(s.next)$, where $\text{size}(\text{nil}) = 0$. (I3) The pointers $next$ never form a cycle.

The nodes of all versions together form a tree in which each node points to its parent, the node below it. The empty stack is the root, and each version is a path from one node to the root. Such a tree of stacks is sometimes called a *cactus stack*.

## Operations

```pseudo id=main
PUSH(s, x)
L1  return a new node with item x, next s and size 1 + SIZE(s)    ▷ s is shared, not copied

POP(s)                                       ▷ returns the top item and the rest
L2  if s = nil then error "underflow"
L3  return (s.item, s.next)

TOP(s)
L4  if s = nil then error "underflow"
L5  return s.item
```

`IS-EMPTY(s)` tests $s = \text{nil}$, and `SIZE(s)` returns $s.size$, or 0 for nil. Each of these procedures reads or makes a constant number of cells and changes none, so each takes $\Theta(1)$ time in the worst case.

PUSH is the only procedure that allocates. It writes the fields of the new node once, at the moment the node is made, which keeps (I1). POP and TOP only read.

**Append.** To put a stack $s$ of $k$ items on top of a stack $t$, the result must contain new nodes for all items of $s$, because the last node of $s$ points to nil, and a new version needs it to point to $t$ instead. So APPEND$(s, t)$ copies the $k$ nodes of $s$ and shares all of $t$. It takes $\Theta(k)$ time and space. The same holds for a change of the item at depth $d$: the $d + 1$ nodes from the top down to it are copied, and the rest is shared. This is [path copying](/path-copying/) on a list.

```pseudo id=append
APPEND(s, t)                                 ▷ the items of s, then the items of t
A1  collect the items of s, from the top down, in a list L
A2  r ← t
A3  for each item x of L, from the bottom of s up to its top do
A4      r ← PUSH(r, x)
A5  return r
```

## Example

Start with the empty stack $v_0$ and run these operations. The column "new nodes" counts the nodes that the operation makes; a stack is written with the top on the left.

| step | operation | result | new nodes | stack |
|---|---|---|---|---|
| 1 | $v_1 \gets \text{push}(v_0, 1)$ | | 1 | $v_1 = [1]$ |
| 2 | $v_2 \gets \text{push}(v_1, 2)$ | | 1 | $v_2 = [2, 1]$ |
| 3 | $v_3 \gets \text{push}(v_1, 3)$ | | 1 | $v_3 = [3, 1]$ |
| 4 | $(x, v_4) \gets \text{pop}(v_2)$ | $x = 2$ | 0 | $v_4 = [1]$ |
| 5 | $v_5 \gets \text{push}(v_4, 4)$ | | 1 | $v_5 = [4, 1]$ |

After step 5 all six versions are valid, and $v_0$ is still empty. The four nodes hold the items 1, 2, 3 and 4. The node of 1 is the bottom of $v_2$, $v_3$ and $v_5$, and $v_4$ is that same node, not a copy of it. If each version were a separate array, the six versions would need $0 + 1 + 2 + 2 + 1 + 2 = 8$ cells instead of 4 nodes.

The append of $v_3 = [3, 1]$ on top of $v_2 = [2, 1]$ gives $[3, 1, 2, 1]$. It makes 2 new nodes (copies of 3 and 1) and shares both nodes of $v_2$.

## Correctness

Let $\text{seq}(s)$ be the sequence of items from the top down: $\text{seq}(\text{nil}) = \langle \rangle$ and $\text{seq}(s) = \langle s.item \rangle \cdot \text{seq}(s.next)$. By (I3) the recursion ends. PUSH returns a node whose sequence is $\langle x \rangle \cdot \text{seq}(s)$, and POP returns $s.item$ and $s.next$, whose sequence is the rest. So each operation meets the stack laws on the sequence. Because no procedure writes to an old node, $\text{seq}(v)$ never changes for a version $v$ that already exists. The full proof is in the proofs folder.

## Complexity

| operation | time | new space |
|---|---|---|
| push | $\Theta(1)$ worst case | one node |
| pop, top, is_empty, size | $\Theta(1)$ worst case | none |
| append of $k$ items | $\Theta(k)$ worst case | $k$ nodes |
| change the item at depth $d$ | $\Theta(d)$ worst case | $d + 1$ nodes |

The model is the [pointer machine](/pointer-machine/): a node is a record of a constant number of fields, and following a pointer costs one step. These bounds hold for each version, also when many operations use the same old version, because no operation does any deferred work.

**Space.** Each push makes one node, so after $p$ pushes the structure has $p$ nodes, whatever the number of versions. With a garbage collector, a node whose versions are all unreachable can be freed, so the live space is the number of distinct nodes reachable from the versions that the program still holds.

## Variants

- **Random access.** A list gives the item at index $i$ in $\Theta(i)$ time. The [skew binary random-access list](/skew-binary-random-access-list/) and the [binary random-access list](/binary-random-access-list/) keep push and pop in $O(1)$ and give index in $O(\log n)$.
- **Queues.** Two persistent stacks give a queue with $O(1)$ amortized operations when only the newest version is used, as in the [two-stacks queue](/two-stacks-queue/). With full persistence, the same old version can be popped many times, and each pop can redo the reversal. The [banker's queue](/banker-queue/) and the [real-time queue](/real-time-queue/) fix this with lazy evaluation.
- **Catenable lists.** Lists that join in $O(1)$ need a different representation, see [catenable deque](/catenable-deque/).
- **Zipper.** Two persistent stacks, one for the items to the left of a cursor and one for the items to the right, give a list with $O(1)$ moves and edits at the cursor: the [zipper](/zipper/).
- **Min-stack.** Store in each node the minimum of its list as well as the size; then the minimum of each version is available in $O(1)$.

## When to use it

Use a persistent stack when a program must keep many related stacks that grow from a common base: the stack of open choices in a backtracking search, the environments of an interpreter, the call stacks of threads that fork, or the undo history of an editor. It is also the right tool whenever a function returns a stack and the caller still needs the old one. If only one version is ever used, an array-based stack has better locality and less memory per item.

## Pitfalls

- **Changing a node in place.** An in-place reversal or an in-place append that sets $next$ of the last node of $s$ breaks (I1). Each other version that shares the node then changes without warning. Every update must make new nodes, as PUSH does in line L1.
- **Pop of the empty stack.** Lines L2 and L4 must test for nil. A version can be empty even after many operations, because pop returns an older node.
- **Amortized bounds do not survive persistence.** A queue made from two stacks has $O(1)$ amortized time only when each version is used once. Calling pop many times on a version with a long front reversal costs that reversal each time.
- **Deep recursion.** A recursive length, print or equality test on a list of $10^5$ items fails in a language with a small call stack. Use a loop, as the implementation does.
- **Size by walking.** Without the field $size$, the size takes $\Theta(n)$ time. Storing it in each node keeps size at $O(1)$ and does not break sharing, because the size of a node depends only on the nodes below it.

## Implementations

## History

The list of Lisp, defined by John McCarthy in 1960, is a persistent stack: `cons` makes a new cell that points to an existing list, and `car` and `cdr` read a cell. Lists in pure Lisp code are never changed, so many lists share their tails. Driscoll, Sarnak, Sleator and Tarjan gave the general theory of persistence for linked structures in 1989, and Okasaki's book of 1998 opens its chapter on persistence with this structure.

## References
