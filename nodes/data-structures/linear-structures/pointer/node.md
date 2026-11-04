---
tag: 0ZSAES
kind: concept
slug: pointer
name: Pointer
aliases:
- reference
- link
area: data-structures/linear-structures
level: intro
summary: A value that holds the address of another memory cell, the basis of linked structures.
prereqs: [random-access-machine]
see_also: [singly-linked-list, doubly-linked-list, sentinel-node, pointer-machine, free-list, xor-linked-list, rooted-tree-representation, reference-counting]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.1 (Introduction to information structures), nodes, fields, links and the null link Λ
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 10.3 (Implementing pointers and objects), the multiple-array and single-array representations and the free list
  - book: isbn:9780131103627
    title: Brian W. Kernighan and Dennis M. Ritchie, The C Programming Language, second edition
    locator: Chapter 5 (Pointers and Arrays)
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.3.2.3 (Pointers, the null pointer) and Section 6.5.6 (Additive operators, pointer arithmetic)
---

A pointer is a value that holds the address of a memory cell, so that a program can reach the object stored there without knowing in advance where it is. Following a pointer to its cell is called *dereferencing*, and a special value, nil or null, points to no cell. Pointers are the links of a [singly linked list](/singly-linked-list/), of trees and of graphs: each node stores the addresses of its neighbours, so the structure can grow, shrink and change shape without moving its items. Languages such as Java and Python call a pointer that allows no arithmetic a *reference*.

## In plain words

A computer memory is a long row of numbered boxes. The number of a box is its address. A pointer is a box that holds the address of another box, like a slip of paper with a house number on it.

With such a slip you can find the house without a search. You can also put a slip inside each house that gives the next house to visit. Then a chain of houses spread across the town can be walked in order, and a new house can join the chain by changing two slips, not by moving any house. This is how linked lists and trees are built. A special slip says "nowhere" and marks the end of a chain.

## The idea

Model the memory as an array $M[0 \ldots 2^w - 1]$ of words, as in the [random-access machine](/random-access-machine/). An address is an index $a$ with $0 \le a < 2^w$, and a pointer is a word whose value is used as an address.

- **Dereference.** For a pointer $p$, the cell $*p$ is $M[p]$. A read of $*p$ and a write to $*p$ each cost one step in the RAM model.
- **Address of.** For a cell or object $x$, $\&x$ is its address. So $*(\&x) = x$.
- **Fields.** An object with fields $f_0, \dots, f_{r-1}$ stored at address $p$ keeps field $f_i$ at $M[p + o_i]$ for fixed offsets $o_i$. The notation $p.f_i$ or `p->f` means $M[p + o_i]$. CLRS writes $x.next$ for the field `next` of the object that $x$ points to.
- **Nil.** A reserved value NIL that is the address of no object. C uses a null pointer, written `NULL`, and the standard guarantees that it compares unequal to a pointer to any object (C11, Section 6.3.2.3). Knuth writes the null link as $\Lambda$.
- **Arithmetic.** In C, if $p$ points to element $i$ of an array of objects of $s$ bytes each, then $p + j$ points to element $i + j$, at byte address $p + j s$. This is defined only inside one array and one past its end (C11, Section 6.5.6).
- **References.** A reference in a managed language allows dereference, assignment, copy and comparison for equality, but no arithmetic and no conversion from an integer. So it cannot point into the middle of an object or to freed memory, and a garbage collector can move objects and update the references.

The [pointer machine](/pointer-machine/) is the model of computation that allows only the reference operations: a step can create a node, follow a pointer field, copy a pointer, or compare two pointers for equality. It has no address arithmetic, so it cannot index an array in $O(1)$ time. Many lower bounds for linked data structures, for example for union-find, are proved in this model.

**Aliasing.** Two pointers are *aliases* when they hold the same address. A write through one is seen through the other. Code that changes a linked structure must account for this. A swap of two list nodes $x$ and $y$ that is correct when the nodes are far apart often breaks when they are next to each other, because then $x.next$ and $y$ are aliases.

**Pointers without hardware addresses.** A program can use array indices as pointers. Then $\text{next}[i]$ holds the index of the node after node $i$, and the index 0 or $-1$ plays NIL. This is how CLRS (third edition, Section 10.3) builds objects in a language without pointers, and it is how many fast programs store trees and lists: indices are smaller than addresses, the arrays are contiguous, and a whole structure can be copied or saved to a file without fixing any address.

## Examples

**Array addresses.** In C, let `int a[4]` start at byte address 1000, with 4-byte integers. Then `&a[2]` is $1000 + 2 \cdot 4 = 1008$, the pointer `a + 3` holds 1012, and `*(a + 3)` is the same cell as `a[3]`. The pointer `a + 4` holds 1016; it may be compared with other pointers into `a`, but not dereferenced.

**A list stored in arrays.** The list $3 \to 7 \to 1$ is stored in two arrays indexed $1$ to $6$, with 0 as NIL. The head is 4.

| index | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| key | 7 | | 1 | 3 | | |
| next | 3 | 5 | 0 | 1 | 6 | 0 |

Start at the head 4: key 3, next 1; key 7, next 3; key 1, next 0, so the walk ends. The free cells 2, 5 and 6 form a second chain, the [free list](/free-list/), with its head 2. To insert 9 at the front of the list, take the cell 2 from the free list (the free head becomes 5), set key[2] to 9 and next[2] to 4, and set the list head to 2. No item moves.

**Aliases in Python.** After `a = [1, 2]` and `b = a`, the names `a` and `b` refer to the same list object. The call `b.append(3)` makes `a` equal to `[1, 2, 3]` too. A copy `c = list(a)` makes a new object, so a change to `c` does not change `a`.

**A pointer to a link.** To delete the first node with key $k$ from a singly linked list, C code can walk a pointer to the link field itself, not to the node. Then the head needs no special case:

```c
struct node **pp = &head;
while (*pp != NULL && (*pp)->key != k)
    pp = &(*pp)->next;
if (*pp != NULL) { struct node *dead = *pp; *pp = dead->next; free(dead); }
```

The variable `pp` holds the address of the link that points to the current node: first the address of `head`, then the address of a `next` field. A [sentinel node](/sentinel-node/) removes the same special case in another way.

**Size.** On a machine with 64-bit addresses a pointer takes 8 bytes. A list node with a 4-byte key and one pointer then needs 12 bytes, and usually 16 after alignment. For small keys the pointers are most of the memory, which is why an [unrolled linked list](/unrolled-linked-list/) stores several keys in each node and an [XOR linked list](/xor-linked-list/) stores two links in one field.

## Where it is used

- Linked lists: the [singly linked list](/singly-linked-list/), the [doubly linked list](/doubly-linked-list/), the [circular linked list](/circular-linked-list/) and their [sentinel nodes](/sentinel-node/).
- Trees: the [binary tree](/binary-tree/) with left, right and parent pointers, and the [left-child right-sibling representation](/rooted-tree-representation/) of a [rooted tree](/rooted-tree/) with any number of children.
- Graphs and tables: the [adjacency list](/adjacency-list/), the chains of [separate chaining](/separate-chaining/) in a [hash table](/hash-table/), and the parent pointers of a [disjoint-set forest](/disjoint-set-forest/).
- Memory management: the [free list](/free-list/) of an allocator and [reference counting](/reference-counting/).
- Models and techniques: the [pointer machine](/pointer-machine/), [pointer jumping](/pointer-jumping/) in parallel [list ranking](/list-ranking/), and the [path copying](/path-copying/) of [persistent data structures](/persistent-data-structure/).

## References
