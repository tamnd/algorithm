---
tag: BYX9WD
kind: algorithm
slug: weighted-reference-counting
name: Weighted reference counting
aliases:
- weighted RC
area: systems/garbage-collection
level: advanced
summary: "Reference counting for distributed heaps. Each reference has a weight, and a copy splits it with no message. A delete sends its weight back, and the object dies at total weight zero."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {f: the number of fields of the freed object, W: the initial weight of an object}
  time: {worst: O(1 + f), amortized: O(1)}
  space: {extra: O(log log W)}
properties: {online: true, deterministic: true, recursive: false, complete: false, moving: false, distributed: true}
history:
  year: 1987
  people: [D. I. Bevan, Paul Watson, Ian Watson]
  note: "Bevan, and Watson and Watson, published weighted reference counting independently at the PARLE 1987 conference, for distributed and parallel machines."
prereqs: [reference-counting]
see_also: [reference-counting, deferred-reference-counting, cycle-collection, automatic-memory-reclamation, lock-free-reference-counting, tracing-garbage-collection, gc-roots, garbage]
sources:
  - paper: doi:10.1007/3-540-17945-3_10
    title: "D. I. Bevan, Distributed garbage collection using reference counting, PARLE Parallel Architectures and Languages Europe, LNCS 259 (1987), 176-187"
    locator: the whole paper (weights in references and objects, splitting on copy, returning weight on delete)
  - paper: doi:10.1007/3-540-17945-3_25
    title: "Paul Watson and Ian Watson, An efficient garbage collection scheme for parallel computer architectures, PARLE Parallel Architectures and Languages Europe, LNCS 259 (1987), 432-443"
    locator: the whole paper (weighted reference counts, and indirection cells when a weight of 1 must be copied)
  - book: isbn:9780471941484
    title: "Richard Jones and Rafael Lins, Garbage Collection: Algorithms for Automatic Dynamic Memory Management, Wiley, 1996"
    locator: Chapter 12 (distributed garbage collection, weighted reference counting)
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Chapter 5 (reference counting and its variants)
---

Weighted reference counting is a form of [reference counting](/reference-counting/) for heaps that are spread over many processors or machines. Each reference carries a *weight*, and each object keeps a *total weight*, equal to the sum of the weights of all its references. To copy a reference, the holder splits its weight in two and gives half to the copy, which needs no message to the object's owner. To delete a reference, the holder sends its weight back, and the owner subtracts it. When the total weight reaches zero, no reference is left and the object is freed. Bevan (1987) and Watson and Watson (1987) published the method independently.

## In plain words

In plain reference counting, every copy of a reference must tell the object "one more reference". On one computer this is cheap. On many computers, it is a message over the network, and the messages can arrive in the wrong order.

Weighted counting gives each object a large number of tickets at its birth, for example 64, and gives all of them to the first reference. To copy a reference, you tear your stack of tickets in half and give half to the copy. Nobody else needs to know.

When you drop a reference, you mail your tickets back to the object. The object counts the tickets that come back. When all of them are back, no reference can exist, and the object is freed.

## The problem

Solve [automatic memory reclamation](/automatic-memory-reclamation/) for a heap whose objects live on different processors. A reference can be copied and deleted by any processor, but only the owner of an object can change its counts, and the other processors talk to it by messages. Messages arrive after an unknown delay, in any order. The goal is to free each object after its last reference is gone, with as few messages as possible.

## The algorithm

Let $W$ be a power of two. A reference $r$ is a pair $(\mathrm{target}(r), w(r))$ with $w(r) \ge 1$. Each object $x$ has a total weight $\mathrm{tw}(x)$.

```pseudo id=main
NEW(n)
L1  x ← allocate an object with n null fields
L2  tw(x) ← W
L3  return the reference (x, W)

COPY(r)                                    ▷ runs where r is held; no message
L4  if w(r) = 1 then                       ▷ weight cannot be split
L5      c ← allocate an indirection cell with one field; tw(c) ← W
L6      c[0] ← (target(r), 1)              ▷ the cell takes over the old reference
L7      r ← (c, W)
L8  h ← w(r) / 2
L9  w(r) ← w(r) − h
L10 return the reference (target(r), h)

DELETE(r)
L11 send DEC(target(r), w(r)) to the owner of target(r)

on receipt of DEC(x, w)                    ▷ runs at the owner of x
L12 tw(x) ← tw(x) − w
L13 if tw(x) = 0 then
L14     for each field reference s of x do DELETE(s)
L15     free(x)
```

Storing a reference into a field moves it; it changes no weight. Overwriting a field deletes the old reference. To use a reference whose target is an indirection cell, follow the cell's field. Because $W$ is a power of two and each split halves a weight, every weight is a power of two, so a weight can be stored as its exponent, in $\lceil \log_2 \log_2 W \rceil + 1$ bits.

## Example

Take $W = 4$ and one object $x$. The column "messages" counts the messages sent so far.

| step | operation | references | total weights | messages |
|---|---|---|---|---|
| 1 | $a \leftarrow$ NEW(0) | $a = (x, 4)$ | $\mathrm{tw}(x) = 4$ | 0 |
| 2 | $b \leftarrow$ COPY($a$) | $a = (x, 2)$, $b = (x, 2)$ | $\mathrm{tw}(x) = 4$ | 0 |
| 3 | $c \leftarrow$ COPY($a$) | $a = (x, 1)$, $b = (x, 2)$, $c = (x, 1)$ | $\mathrm{tw}(x) = 4$ | 0 |
| 4 | $d \leftarrow$ COPY($a$) | cell $k$ holds $(x, 1)$; $a = (k, 2)$, $d = (k, 2)$ | $\mathrm{tw}(x) = 4$, $\mathrm{tw}(k) = 4$ | 0 |
| 5 | DELETE $a, b, c, d$ | none in the program | messages in flight: $k{:}2$, $x{:}2$, $x{:}1$, $k{:}2$ | 4 |
| 6 | deliver all | | $\mathrm{tw}(k) = 0$, so $k$ is freed and deletes $(x, 1)$ | 5 |
| 7 | deliver the last | | $\mathrm{tw}(x) = 0$, so $x$ is freed | 5 |

In step 4, $a$ has weight 1, so COPY makes the indirection cell $k$. The weight of $x$ is still held in full: $b$ has 2, $c$ has 1, and the field of $k$ has 1, which is 4. Three copies cost no message. The five deletions cost one message each. Plain distributed reference counting would have sent three increment messages too.

## Correctness

The invariant is: for each unfreed object $x$, $\mathrm{tw}(x)$ equals the sum of the weights of all references to $x$, plus the sum of the weights in the DEC messages for $x$ that are not yet delivered. COPY splits one weight into two, and DELETE moves a weight from a reference into a message, so neither changes the sum. A delivery moves the weight from the message into the subtraction. Every reference and every message has a positive weight, so $\mathrm{tw}(x) = 0$ only if no reference to $x$ exists and no message for $x$ is in flight. Then no processor can reach $x$, and freeing it is safe, whatever the order of delivery was. The full proof is below.

## Complexity

- **COPY.** $O(1)$ time and no message. With a weight of 1, it also allocates one indirection cell.
- **DELETE.** $O(1)$ time and one message.
- **Delivery.** $O(1)$, plus $O(f)$ to delete the $f$ fields of an object that it frees.
- **Messages.** One message per deleted reference, and none per copy. Plain distributed reference counting sends one message per copy and one per delete.
- **Space.** Each reference carries its weight, which fits in $O(\log \log W)$ bits as an exponent, and each object carries its total weight in $O(\log W)$ bits.

## Properties

- **No increment messages.** Only deletes send messages, so there is no race between an increment and a decrement for the same object.
- **Order-independent.** DEC messages may arrive in any order, and none can free an object too early.
- **Weight underflow.** A reference that has been split many times has weight 1, and its next copy needs an indirection cell, which adds one step to each later use of the copies.
- **Not complete.** Like every form of reference counting, it never frees a cycle of garbage, and in a distributed heap such cycles can span many machines.

## Variants and improvements

- **Larger initial weight.** A larger $W$ makes indirection cells rarer, at the cost of larger count fields.
- **Asking for more weight.** Instead of an indirection cell, the holder of a weight of 1 can ask the owner to add weight to the object and send it back. This costs a round trip of messages.
- **Indirect reference counting.** Track the tree of copies instead of weights: each copy is counted at the processor that it was copied from, so a copy needs no message to the owner, and no weight can run out.
- **Cycle collection.** A distributed tracing collector, or a local [cycle collection](/cycle-collection/) method extended to many machines, frees the cycles.

## When to use it

Use weighted reference counting when references are copied often across processors or machines, when messages are expensive, and when the network can reorder them, as in distributed object systems and parallel graph reduction machines. On a single machine with shared memory, plain or [deferred reference counting](/deferred-reference-counting/) is simpler, because a count update is a local write.

## Pitfalls

- **Weights that are not powers of two.** If $W$ is not a power of two, halving rounds down, and a weight of 3 split as 1 and 1 loses weight. Then $\mathrm{tw}(x)$ never reaches 0. With a power of two, each split is exact.
- **Splitting a weight of 1.** A reference of weight 1 cannot give a positive weight to a copy. Copying it without an indirection cell, or with weight 0, breaks the invariant and can free a live object.
- **Copying a reference in a message.** A reference that is sent to another processor must take its weight with it. If the sender keeps the full weight and the receiver gets weight too, the total grows and the object never dies.
- **Chains of cells.** Repeated underflow builds chains of indirection cells, and each use of a reference must follow the chain.

## Implementations

## History

Bevan (1987) and Watson and Watson (1987) described weighted reference counting independently, in papers at the PARLE conference on parallel architectures and languages in 1987. Bevan worked on distributed garbage collection, and Watson and Watson designed a collector for a parallel graph reduction machine. Both removed the increment messages of distributed reference counting by putting the count into the references. Watson and Watson handled a weight of 1 with an indirection cell. Later methods, such as indirect reference counting, removed the limit on the number of copies.

## References
