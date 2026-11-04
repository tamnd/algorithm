---
tag: 4Y8RH2
kind: definition
slug: sentinel-node
name: Sentinel node
aliases:
- dummy node
- header node
area: data-structures/linear-structures
level: intro
summary: Dummy node that removes boundary cases from list insertion and deletion.
prereqs: [pointer]
see_also: [singly-linked-list, doubly-linked-list, circular-linked-list, red-black-tree, linear-search, sequential-search-symbol-table]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.2 (Linked lists), the part on sentinels, with the circular doubly linked list with the sentinel L.nil
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition
    locator: Section 6.1 (Sequential searching), Algorithm Q (Quick sequential search), which puts the key in an extra record at the end
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.2.4 (Circular lists) and Section 2.2.5 (Doubly linked lists), the list head
  - url: https://opendatastructures.org/
    title: Pat Morin, Open Data Structures
    locator: Section 3.2 (DLList), the dummy node
---

A sentinel node is an extra node of a linked structure that holds no item, is present for the whole life of the structure, and stands where a NIL [pointer](/pointer/) would stand at a boundary. With it, the first and the last real nodes have a neighbour like every other node, so insertion and deletion need no special case for the head, the tail or the empty structure. The cost is one node of memory per structure. The same idea, a value placed at the end of the data so that a loop stops without a bound test, is a *sentinel value*.

## Definition

Let a [doubly linked list](/doubly-linked-list/) represent the sequence $\langle a_1, \dots, a_n \rangle$, $n \ge 0$, with the nodes $x_1, \dots, x_n$, where $x_i.key = a_i$. A *sentinel* for this list is a node $s$, distinct from each $x_i$, such that, with $x_0 = x_{n+1} = s$,

$$x_i.next = x_{i+1} \text{ and } x_{i+1}.prev = x_i \quad \text{for each } i \text{ with } 0 \le i \le n.$$

So the nodes form one cycle $s, x_1, \dots, x_n, s$, and no link is NIL. The list holds the single pointer $L.nil = s$; the head is $s.next$ and the tail is $s.prev$. The list is empty exactly when $s.next = s$, and then also $s.prev = s$. The key field of $s$ is not an item of the list.

For a [singly linked list](/singly-linked-list/), a sentinel at the front (a *dummy head*) is a node $s$ with $s.next = x_1$, or NIL when $n = 0$. A sentinel at the end is a node that replaces the NIL after $x_n$. In a tree, a sentinel is one node that replaces every NIL child and the NIL parent of the root, as the node $T.nil$ of the CLRS [red-black tree](/red-black-tree/).

The words *dummy node* and *header node* name the same thing. Some authors use *header* only for a sentinel at the front that also stores data about the list, such as its length; then the header still holds no item.

## Examples and non-examples

**Deletion with no cases.** In the cyclic list with a sentinel, every node $x$ of the list has $x.prev$ and $x.next$ that are nodes. So deleting $x$ is two assignments, the same for the head, the tail, a middle node and the only node:

$$x.prev.next \leftarrow x.next, \qquad x.next.prev \leftarrow x.prev.$$

Without a sentinel, $x.prev$ is NIL at the head and $x.next$ is NIL at the tail. Then the code needs two tests: if $x.prev = \text{NIL}$, set $L.head \leftarrow x.next$, else set $x.prev.next$; and if $x.next = \text{NIL}$, set $L.tail \leftarrow x.prev$, else set $x.next.prev$. These give four cases. Insertion of $x$ after a node $y$ is also four assignments with no case when $y$ may be $s$: $x.next \leftarrow y.next$, $x.prev \leftarrow y$, $y.next.prev \leftarrow x$, $y.next \leftarrow x$. Insertion at the front is the case $y = s$.

**A trace.** Take the list $\langle 4, 9 \rangle$ with sentinel $s$: the cycle is $s \to 4 \to 9 \to s$. Delete the node of 4. Its prev is $s$ and its next is the node of 9, so the two assignments set $s.next$ to the node of 9 and the prev of the node of 9 to $s$. The cycle is $s \to 9 \to s$. Delete the node of 9: its prev and next are both $s$, so both assignments write to $s$, and $s.next = s.prev = s$, the empty list. No step tested for the head, the tail or the last node.

**A dummy head in a singly linked list.** With a node $s$ in front of $x_1$, each real node has a predecessor node. Deleting the first node with key $k$ walks $p$ from $s$ while $p.next \ne \text{NIL}$ and $p.next.key \ne k$, then sets $p.next \leftarrow p.next.next$. The case "the match is the head", which changes $L.head$ in the plain list, is gone: there, $p = s$.

**A sentinel key for search.** To search the cyclic list for key $k$, store $k$ in $s.key$ first. Then the loop "$x \leftarrow s.next$; while $x.key \ne k$ do $x \leftarrow x.next$" always stops, at a real node on a hit or at $s$ on a miss. A miss in a list of $n$ nodes makes $n + 1$ key tests. The loop without the sentinel, "while $x \ne \text{NIL}$ and $x.key \ne k$", makes $2n + 1$ tests on a miss. Knuth's Algorithm Q in Section 6.1 does the same on an array by putting the key in an extra record after the last one; this is the sentinel form of [linear search](/linear-search/).

**Sentinel values.** The merge of two sorted runs can put $\infty$ at the end of each run, so the merge loop needs no test for an exhausted run. The $\infty$ is a sentinel value, not a sentinel node, but it plays the same role.

**Non-example: NIL.** The NIL pointer is not a sentinel node: it is not a node, it has no fields, and a write to $\text{NIL}.next$ is an error. The point of a sentinel is that such writes are legal and harmless.

**Non-example: the first real node.** A list that treats its first item as a fixed head, and never deletes it, has no sentinel: that node holds an item, so the represented sequence must skip it, and code that forgets this reads a value that is not in the list.

**Non-example in cost.** A sentinel per list costs one node. For a [hash table](/hash-table/) with [separate chaining](/separate-chaining/), one sentinel per chain adds one node per slot, which is a large share of the memory when most chains are short or empty; CLRS notes that the sentinels of many small lists waste memory. One shared sentinel suffices for all the NIL leaves of a tree, as in the CLRS red-black tree, so there the cost is one node for the whole tree.

## Related definitions

- A [pointer](/pointer/) and its NIL value, which the sentinel replaces.
- The [singly linked list](/singly-linked-list/), the [doubly linked list](/doubly-linked-list/) and the [circular linked list](/circular-linked-list/), the structures that most often use a sentinel.
- The [red-black tree](/red-black-tree/) of CLRS, with one sentinel $T.nil$ for all its leaves and for the parent of the root.
- [Linear search](/linear-search/) and the [sequential search symbol table](/sequential-search-symbol-table/), where a sentinel key removes the bound test from the loop.

## References
