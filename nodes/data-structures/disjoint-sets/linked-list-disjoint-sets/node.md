---
tag: JEF2AM
kind: data-structure
slug: linked-list-disjoint-sets
name: Linked-list disjoint sets
aliases:
- linked-list union-find
area: data-structures/disjoint-sets
level: core
summary: Representation of each set as a linked list with a head pointer, using weighted union by appending the smaller list.
implements: [disjoint-set]
model: word-ram
complexity:
  vars: {n: the number of elements, m: the number of operations}
  time: {worst: O(n), amortized: O(log n), total: O(m + n log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [disjoint-set, linked-list, amortized-cost]
see_also: [quick-find, disjoint-set-forest, union-by-size, singly-linked-list, dynamic-equivalence-problem, accounting-method, dsu-on-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.2, Linked-list representation of disjoint sets (the set objects with head and tail, the Θ(n²) sequence of simple unions, the weighted-union heuristic and its O(m + n lg n) bound)
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM, 1983
    locator: Chapter 2, Disjoint sets
  - paper: doi:10.1137/0202024
    title: "John E. Hopcroft and Jeffrey D. Ullman, Set merging algorithms, SIAM Journal on Computing 2(4) (1973), 294-303"
    locator: the merging of the smaller set into the larger and its O(n log n) bound
---

Linked-list disjoint sets store each set of a [disjoint-set](/disjoint-set/) structure as a [linked list](/linked-list/) of its members. Each member points to the object of its set, and the object points to the head and the tail of the list and keeps its size. A find follows one pointer, so it takes $O(1)$ time. A union appends one list to the other and updates the set pointer of each element of the appended list. With the *weighted-union* rule, which appends the shorter list, each element changes its set pointer at most $\lg n$ times, so $m$ operations on $n$ elements take $O(m + n \log n)$ time. The structure is also the only common union-find that lists the members of a set in time linear in its size.

## In plain words

Each group is a chain of its members, and a card at the front of the chain names the group. Each member holds a pointer to the card. To ask for the group of a member, you read its pointer.

To join two groups, you hook one chain onto the end of the other, and each member of the hooked chain must now point to the other card. That costs one step per member that moves. So always move the smaller group. A member that moves lands in a group at least twice as large as its old one. A group cannot double more than a few times before it holds everyone, so each member moves only a few times in total.

## The abstract type

The structure implements the [disjoint-set](/disjoint-set/) type: `make-set(x)`, `find(x)`, which returns the representative of the set of $x$, and `union(x, y)`. The representative is the head of the list. It also gives `size(x)` in $O(1)$ time and `members(x)`, which lists the set of $x$ in time proportional to its size.

## Representation

Each set $S$ has an object with three fields: $S.head$, the first element of its list, $S.tail$, the last one, and $S.size$, the length of the list. Each element $x$ has two fields: $x.set$, the object of its set, and $x.next$, the next element of the list, or NIL at the tail.

**Invariant (L).** For each set object $S$, the list $S.head, S.head.next, \ldots$ has exactly $S.size$ elements, ends at $S.tail$ with $S.tail.next = \mathrm{NIL}$, and each of its elements $x$ has $x.set = S$. Each element is in exactly one such list.

So the sets of the structure are the lists, and the representative of the set of $x$ is $x.set.head$.

## Operations

```pseudo id=main
MAKE-SET(x)
L1  S ← new set object; S.head ← x; S.tail ← x; S.size ← 1
L2  x.set ← S; x.next ← NIL

FIND(x)
L3  return x.set.head

UNION(x, y)
L4  S ← x.set; T ← y.set
L5  if S = T then return                  ▷ already in one set
L6  if S.size > T.size then swap S and T  ▷ weighted union: S is the smaller
L7  for each z in the list of S do z.set ← T
L8  T.tail.next ← S.head; T.tail ← S.tail
L9  T.size ← T.size + S.size; free S
```

**Make-set** (lines L1 and L2) makes a list of one element and its set object. It costs $O(1)$.

**Find** (line L3) reads two pointers. It costs $O(1)$ in the worst case.

**Union** (lines L4 to L9) gets the two set objects. If they are the same, nothing changes. Otherwise line L6 makes $S$ the smaller of the two, line L7 walks the list of $S$ and points each of its elements at $T$, and line L8 links the list of $S$ after the tail of $T$. The cost is $O(1 + S.size)$, the size of the smaller set. Without line L6, a union costs the size of the set of $x$, whatever it is.

**Members** walks the list from $x.set.head$, in $O(\text{size})$ time.

## Example

Make the sets $0$ to $6$, then do six unions. The lists are written from head to tail, and the last column counts the set pointers that line L7 changes.

| step | sizes of S and T | lists after the step | renamed |
|---|---|---|---|
| start | | (0) (1) (2) (3) (4) (5) (6) | |
| union(0, 1) | 1 and 1, no swap | (1 0) (2) (3) (4) (5) (6) | 1 |
| union(2, 3) | 1 and 1, no swap | (1 0) (3 2) (4) (5) (6) | 1 |
| union(1, 3) | 2 and 2, no swap | (3 2 1 0) (4) (5) (6) | 2 |
| union(4, 0) | 1 and 4, no swap | (3 2 1 0 4) (5) (6) | 1 |
| union(5, 4) | 1 and 5, no swap | (3 2 1 0 4 5) (6) | 1 |
| union(3, 6) | 6 and 1, swap | (3 2 1 0 4 5 6) | 1 |

In the last union, the set of 3 is the larger one, so line L6 swaps, and only the element 6 moves. Without the swap, the six elements of the set of 3 would move. In all, 7 set pointers change. Element 0 moves twice, into sets of sizes 2 and 4, and no element moves more than $\lfloor \lg 7 \rfloor = 2$ times.

## Correctness

Each operation keeps (L). MAKE-SET adds a new list of one element. FIND reads only. UNION with $S \ne T$ points every element of the list of $S$ at $T$, appends the list of $S$ after the tail of $T$, sets the tail and the size of $T$ to those of the joined list, and drops $S$. So the list of $T$ is the union of the two sets, its size and tail are right, and each element has the right set pointer. The swap of line L6 changes only which set is moved, not the result. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $n$ be the number of MAKE-SET operations and $m$ the number of all operations.

- **Find and make-set.** $O(1)$ in the worst case.
- **One union.** $O(1 + s)$, where $s$ is the size of the smaller set. This is $O(n)$ in the worst case: two sets of $n/2$ elements.
- **The sum, weighted union.** Each time line L7 changes $x.set$, $x$ was in the smaller set, so its new set has at least twice as many elements as its old one. A set has at most $n$ elements, so $x$ moves at most $\lfloor \lg n \rfloor$ times. The total work of line L7 over the whole sequence is at most $n \lfloor \lg n \rfloor$, and the rest of each operation costs $O(1)$. So $m$ operations take $O(m + n \log n)$ time (CLRS, Section 19.2). The proof is in [the complexity proof](proofs/complexity.md).
- **Tightness.** For $n = 2^k$, a tournament of unions, first of pairs, then of pairs of pairs, and so on, moves $n/2$ elements in each of $k$ rounds, so $(n/2) \lg n$ moves in all.
- **Without weighted union.** The unions $(0, 1), (1, 2), \ldots, (n - 2, n - 1)$, each of which moves the set of its first argument, move $1 + 2 + \cdots + (n - 1) = n(n - 1)/2$ elements, which is $\Theta(n^2)$.
- **Space.** Two fields per element and three per set: $\Theta(n)$.

| operation | worst case | amortized (weighted union) |
|---|---|---|
| make-set | $O(1)$ | $O(1)$ |
| find | $O(1)$ | $O(1)$ |
| union | $O(n)$ | $O(\log n)$ |
| size | $O(1)$ | $O(1)$ |
| members | $O(\text{size})$ | $O(\text{size})$ |
| space | $\Theta(n)$ | |

The amortized cost of a union is $O(\log n)$ in the sense of the [accounting method](/accounting-method/): charge $\lg n$ to each element when it is made, and let each move spend one unit.

## Variants

- **Arrays instead of lists.** With elements $0$ to $n - 1$, the fields are arrays `set`, `next`, `head`, `tail` and `size`. The set object can be named by its head, so `set[x]` is the head of $x$. This is [quick-find](/quick-find/) with member lists and weighted union.
- **No tail pointer.** Insert the shorter list right after the head of the longer one instead of at its end. This needs only $S.head$ and $T.head$, and the cost is the same.
- **Small to large on other containers.** The same argument, move the smaller collection into the larger, works for hash sets and sorted maps, where each move costs $O(1)$ or $O(\log n)$. This is the idea of [DSU on tree](/dsu-on-tree/).
- **The forest.** Replacing the set pointers by parent pointers gives the [disjoint-set forest](/disjoint-set-forest/), whose unions cost $O(1)$ after the finds and whose total is $O(m\,\alpha(n))$.

## When to use it

Use linked lists when finds must cost $O(1)$ in the worst case, or when the program must often list or iterate over the members of a set, for example to update data stored at each member after a merge. The total time $O(m + n \log n)$ is worse than the $O(m\,\alpha(n))$ of the [disjoint-set forest](/disjoint-set-forest/) when $m$ is close to $n$, but each find is a single read. For pure same-set queries, the forest is faster and smaller.

## Pitfalls

- **Appending the larger list.** Line L6 must compare the sizes and move the smaller set. Without it, the chain of unions of the complexity section takes $\Theta(n^2)$ time.
- **Saving an old representative.** A union can change the representative of a set: after `union(x, y)`, `find(x)` may be the head of the old set of $y$. A caller that stored an old result of line L3 as a key must call `find` again after each union.
- **Forgetting the tail.** Line L8 must set $T.tail \leftarrow S.tail$. Otherwise the next union appends after an element in the middle of the list and cuts off the rest of it.
- **One set with itself.** Without line L5, a union of two elements of one set links the list to itself and makes a cycle.

## Implementations

The Python class keys its maps by any hashable element. A set is named by its head, which is the representative. The class has `make_set`, `find`, `union`, `connected`, `size` and `members`, and `check_invariant` tests (L).

## History

Representing each class by a list of its members, and merging the smaller list into the larger, is the early method for equivalence and set merging problems. Hopcroft and Ullman (1973) analyzed the set merging algorithms of this kind together with tree-based ones, and CLRS presents the list form with its $O(m + n \lg n)$ bound as the first step to the disjoint-set forest.

## References
