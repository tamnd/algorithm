---
tag: 9GBB1W
kind: definition
slug: ephemeral-data-structure
name: Ephemeral data structure
aliases:
- ordinary data structure
area: data-structures/persistent-structures
level: intro
summary: A structure in which an update destroys the previous version, the usual non-persistent case.
prereqs: [array, linked-list]
see_also: [persistent-data-structure, partial-persistence, full-persistence, confluent-persistence, amortized-cost, purely-functional-data-structure, structural-sharing, undo-log]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: pages 86 to 124, the introduction (the terms ephemeral, partially persistent and fully persistent)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 2, Persistence, and Section 5.6, The Bad News (amortized bounds of ephemeral structures under persistent use)
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
    locator: pages 669 to 679, the introduction and the section on persistent search trees
---

An ephemeral data structure is a data structure in which each update changes the structure in place, so that the state before the update is lost. Only the current version can be queried or updated. Almost every structure of a first course, such as an [array](/array/) with assignment, a [linked list](/linked-list/) with pointer changes or a [hash table](/hash-table/), is ephemeral. The word comes from the paper of Driscoll, Sarnak, Sleator and Tarjan, which contrasts it with a [persistent data structure](/persistent-data-structure/).

## Definition

Fix a data structure with a set of operations. Each operation is either a *query*, which returns an answer and does not change the state, or an *update*, which changes the state. A *version* is the state of the structure between two updates. A sequence of updates $u_1, u_2, \ldots, u_m$ applied to an initial version $D_0$ gives versions $D_0, D_1, \ldots, D_m$, where $D_i = u_i(D_{i-1})$ for $1 \le i \le m$.

The structure is **ephemeral** if, at each time $t$ with $0 \le t \le m$, the only version that the operations can access is the current version $D_t$:

- a query at time $t$ answers with respect to $D_t$;
- an update at time $t$ takes $D_t$ as its input, and after it returns, $D_t$ is no longer accessible.

So the versions form a single sequence, and at each moment only its last element exists. Contrast the three persistent cases, which keep old versions accessible:

| kind | which versions can be queried | which versions can be updated | shape of the versions |
|---|---|---|---|
| ephemeral | the current one | the current one | one version at a time |
| [partially persistent](/partial-persistence/) | all | the newest | a sequence (a path) |
| [fully persistent](/full-persistence/) | all | all | a tree |
| [confluently persistent](/confluent-persistence/) | all | all, and two can be combined | a directed acyclic graph |

The definition is about which versions the *interface* gives access to, not about how the memory is used. An implementation that keeps a log of old values but offers no operation to read an old version is still ephemeral.

## Examples and non-examples

- **An array with assignment.** After `A[3] ← 7`, the old value of `A[3]` is gone. To answer "what was `A[3]` before the assignment" the program must have saved a copy itself.
- **A singly linked list with in-place insertion.** Inserting after a node $x$ changes the field `next` of $x$. A program that kept a pointer to the head of the list now sees the new list through that pointer, not the old one.
- **A [binary heap](/binary-heap/).** Extract-min moves the last item to the root and sifts it down, so the array no longer holds the old heap.
- **An [undo log](/undo-log/) or a [rollback](/rollback-technique/).** A structure that can undo its last updates is still ephemeral at each moment: an undo is one more update, from the current version to a version equal to an older one. It is a restricted form of going back, in stack order only, not access to several versions at once.
- **Non-example: a persistent stack.** In a [persistent stack](/persistent-stack/) made of immutable cons cells, push creates a new cell that points to the old top. The old top pointer still describes the old stack, so both versions can be used. This is the basic case of [structural sharing](/structural-sharing/).
- **Non-example: copy on each update.** A structure that copies its whole state before each update and keeps all copies is [fully persistent](/full-persistence/), at a cost of $\Theta(n)$ time and space for each update on a structure of size $n$. Persistent structures exist to avoid this cost.
- **Non-example: a purely functional value.** In a language without assignment, such as the purely functional part of Haskell or ML, every data structure is persistent by construction, because no update can destroy a value. See [purely functional data structure](/purely-functional-data-structure/).

### Amortized bounds assume ephemeral use

An [amortized](/amortized-cost/) bound on an ephemeral structure counts the cost of one sequence of operations, in which each update consumes the version before it. If old versions can be reused, the bound can fail. Take a [binary counter](/binary-counter-increment/) of bits, where an increment flips the trailing 1 bits to 0 and the next 0 bit to 1. From zero, 1024 increments flip 2047 bits in total, so the amortized cost is less than 2 flips for each increment. Now keep the version with value 1023, which is ten 1 bits, and increment that same version again and again: each such increment flips 11 bits. With $k$ ones at the bottom, each increment of that version costs $k + 1$, and no cheap operation pays for it in advance. Okasaki (Section 5.6) shows the same failure for the two-list queue and explains that the amortized analyses of ephemeral structures do not carry over to persistent use. Chapter 6 of his book repairs it with lazy evaluation and the [debit analysis](/debit-analysis/).

## Related definitions

- [Persistent data structure](/persistent-data-structure/): a structure that keeps old versions accessible; the opposite of ephemeral.
- [Partial persistence](/partial-persistence/), [full persistence](/full-persistence/) and [confluent persistence](/confluent-persistence/): the three degrees of persistence, by which versions can be updated and combined.
- [Path copying](/path-copying/), the [fat node](/fat-node/) method and [node copying](/node-copying/): general ways to turn an ephemeral pointer structure into a persistent one. The [DSST persistence theorem](/dsst-persistence-theorem/) gives their cost.
- [Retroactive data structure](/retroactive-data-structure/): a structure that allows changes to the past sequence of updates, which is a different notion from access to old versions.
- [Amortized cost](/amortized-cost/): the cost measure whose usual analyses assume ephemeral use.

## References
