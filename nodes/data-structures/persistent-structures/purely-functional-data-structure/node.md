---
tag: TFJWAA
kind: concept
slug: purely-functional-data-structure
name: Purely functional data structure
aliases:
- functional data structure
- immutable data structure
area: data-structures/persistent-structures
level: core
summary: A data structure with no destructive updates, so every version is persistent by construction.
prereqs: [persistent-data-structure, structural-sharing, amortized-cost]
see_also: [persistent-stack, persistent-red-black-tree, banker-queue, real-time-queue, skew-binary-random-access-list, finger-tree, debit-analysis, lazy-rebuilding]
sources:
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 1 (functional versus imperative structures), Chapter 5 (amortization and its failure under persistence), Chapter 6 (lazy evaluation and the banker's and physicist's methods) and Chapter 7 (scheduling for worst-case bounds)
  - paper: doi:10.1145/244795.244798
    title: Nicholas Pippenger, Pure versus impure Lisp, ACM Transactions on Programming Languages and Systems 19(2), 1997
    locator: the separation between pure and impure strict Lisp for an online problem
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: Section 1 (the relation between persistence and functional programming)
  - paper: Haim Kaplan and Robert E. Tarjan, Purely functional, real-time deques with catenation, Journal of the ACM 46(5), 1999
    locator: the introduction (the purely functional model and its relation to the pointer machine)
---

A purely functional data structure is a data structure that is never changed in place: each update builds new nodes and returns a new value, and no field of an existing node is written again. Because no old node changes, every old value stays valid, so the structure is a [persistent data structure](/persistent-data-structure/) by construction, with full persistence. The new value shares the unchanged parts of the old one by [structural sharing](/structural-sharing/). Such structures are the native data structures of functional languages, and Okasaki's book of 1998 is their standard reference.

## In plain words

In most programs, a list or a table is a box whose contents you change. If you change it, the old contents are gone. A purely functional structure is a value, like the number 5. You never change it. When you want a list with one more item, you get a new list, and the old list is still there, as it was.

Making a full copy each time would be slow, so the new list reuses almost all of the old one. Only the few pieces that differ are new. This is safe because nobody ever changes a piece once it exists.

The price is that some tricks of ordinary programs, such as changing one cell of an array in one step, are not allowed. So the designs and the cost analysis are different.

## The idea

**The model.** Memory consists of nodes with a fixed number of fields. A node is made with all its fields at once, and then its fields can only be read. A data structure value is a pointer to a node. An operation reads nodes and makes new ones; it never writes to a node that exists. This is a [pointer machine](/pointer-machine/) without assignment, the model that Kaplan and Tarjan call purely functional.

**Persistence for free.** Let $v$ be a value that exists at some time. The nodes reachable from $v$ exist at that time, and none of their fields will change. So the contents of $v$ are fixed forever, whatever operations run later. Every version can be read and updated, so the structure is fully persistent, and with an operation that takes two values (such as list concatenation) it is confluently persistent.

**What it costs.** Three things change compared with imperative structures.

1. *No constant-time array.* There is no node with an unbounded number of fields that can be updated one at a time, so an array becomes a tree. A balanced tree gives index and update in $O(\log n)$ time, and update makes $O(\log n)$ new nodes. A wide tree, as in the [persistent vector](/persistent-vector/), lowers the depth to $\log_{32} n$ but not to a constant.
2. *Amortization can fail.* An [amortized bound](/amortized-cost/) charges an expensive operation to the cheap ones before it. With persistence, a program can go back to the version just before the expensive operation and run it again, as many times as it likes, and each run pays the full cost. So amortized bounds that are proved for one sequence of operations do not hold when versions are reused.
3. *Lazy evaluation repairs amortization.* If the expensive work is a suspended computation that runs at most once and stores its result (memoization), then all versions that share the suspension share its result, and the work is paid once. Okasaki's [debit analysis](/debit-analysis/) proves amortized bounds that hold under persistence in this way. With a schedule that forces a little of each suspension at each operation, the bounds become worst case, as in the [real-time queue](/real-time-queue/).

**Simulation.** Any imperative algorithm on a memory of $n$ cells can run in a purely functional way by keeping the memory in a balanced search tree keyed by address, which costs $O(\log n)$ time per memory access. Pippenger showed that for some online problems in strict pure Lisp (no lazy evaluation) a loss of a $\log n$ factor cannot be avoided: there is a problem that impure Lisp solves in $O(n)$ time while each strict pure solution needs $\Omega(n \log n)$ time.

## Examples

**Lists and stacks.** The [persistent stack](/persistent-stack/) is the basic example: push makes one node that points to the old list, and both lists stay valid. All of push, pop and top take $O(1)$ time.

**The two-list queue under persistence.** A queue kept as a front list and a reversed rear list does $O(1)$ amortized work per operation when each version is used once: a pop on an empty front reverses the rear, and the cost of that reversal is paid by the pushes that built the rear. Now build a version $q$ with an empty front and a rear of 1000 items, and pop from $q$ 1000 times, each time from $q$ itself. Each pop reverses the same 1000 items again, so the 1000 pops cost about $10^6$ steps, while 1000 pushes and 1000 pops in a single thread of versions cost about $3000$. The [banker's queue](/banker-queue/) uses a lazy reversal that is shared by all such pops, and it does $O(1)$ amortized work per operation even under persistence.

**Balanced trees.** The [persistent red-black tree](/persistent-red-black-tree/) gives an ordered set with $O(\log n)$ worst-case operations: each update rebuilds the nodes on one path and shares the rest.

**Random-access lists.** The [skew binary random-access list](/skew-binary-random-access-list/) keeps the $O(1)$ push and pop of a list and adds $O(\log n)$ index and update, using a number system to lay out complete binary trees.

**Finger trees.** The [finger tree](/finger-tree/) gives a sequence with amortized $O(1)$ access to both ends and $O(\log n)$ split and concatenation, by [bootstrapping](/bootstrapping/) a tree of nodes of size 2 or 3.

**A non-example.** A hash table with an array of buckets updated in place is not purely functional: an insert writes to a bucket of the shared array, so every old value of the table sees the change. A union-find forest with path compression is not purely functional either, because a find writes to parent pointers.

## Where it is used

- The standard collections of Haskell, OCaml, Standard ML, Clojure, Scala and Erlang, where most maps, sets and sequences are balanced trees, tries or lists.
- Compilers and interpreters, for symbol tables and environments that must be restored when a scope ends.
- Concurrent programs, where a reader can keep an old value with no locks while a writer makes a new one.
- Version control, undo histories and snapshots, where each state is a value that shares most of its parts with the states before it.
- The design methods of Okasaki: [lazy rebuilding](/lazy-rebuilding/), [bootstrapping](/bootstrapping/), the [banker's queue](/banker-queue/) and the numerical representations behind the [binary random-access list](/binary-random-access-list/).

## References
