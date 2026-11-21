---
tag: P22TZC
kind: data-structure
slug: capability-list
name: Capability list
aliases:
- c-list
- capability-based access control
area: security-and-privacy/access-control-and-information-flow
level: intro
summary: Stores the access matrix by row, so that each subject holds unforgeable tokens that name an object and the rights on it.
model: word-ram
complexity:
  vars: {s: the number of subjects, o: the number of objects, r: the number of rights, n: the number of capabilities}
  time: {worst: O(1)}
  space: {extra: Θ(n + s)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [access-control-matrix, depth-first-search]
see_also: [access-control-list, principle-of-least-privilege, take-grant-model, reference-monitor, confinement-problem, discretionary-access-control, message-authentication-code, cheri-capability-model]
sources:
  - paper: doi:10.1145/365230.365252
    title: Jack B. Dennis and Earl C. Van Horn, Programming semantics for multiprogrammed computations, Communications of the ACM 9(3), 1966
    locator: pages 143 to 155 (capabilities, the capability list of a computation, and the meta-instructions that grant and remove them)
  - paper: doi:10.1145/775265.775268
    title: Butler W. Lampson, Protection, Proceedings of the 5th Princeton Conference on Information Sciences and Systems, 1971, reprinted in ACM SIGOPS Operating Systems Review 8(1), 1974
    locator: pages 18 to 24 of the reprint (the access matrix, and the capability list of a domain as its row)
  - paper: doi:10.1145/361011.361070
    title: Robert S. Fabry, Capability-based addressing, Communications of the ACM 17(7), 1974
    locator: pages 403 to 412 (capabilities as the names of segments, and their protection from forgery)
  - paper: doi:10.1109/PROC.1975.9939
    title: Jerome H. Saltzer and Michael D. Schroeder, The protection of information in computer systems, Proceedings of the IEEE 63(9), 1975
    locator: pages 1278 to 1308, Section II (ticket-oriented protection, capabilities and the problem of revocation)
  - paper: "David D. Redell and Robert S. Fabry, Selective revocation of capabilities, Proceedings of the IRIA International Workshop on Protection in Operating Systems, 1974"
    locator: revocation by indirection through a capability that the owner can destroy
  - paper: doi:10.1145/54289.871709
    title: Norm Hardy, The confused deputy, or why capabilities might have been invented, ACM SIGOPS Operating Systems Review 22(4), 1988
    locator: pages 36 to 38 (the compiler that writes over the billing file, and how capabilities avoid it)
  - url: "https://sel4.systems/Info/Docs/seL4-manual-latest.pdf"
    title: seL4 Reference Manual
    locator: Section 3.1.5 (the capability derivation tree) and Section 3.2 (deletion and revocation)
  - paper: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018, ISBN 9780321712332"
    locator: Chapter 16, Section 16.2 (capabilities, their implementation, copying and amplifying, and revocation)
---

A capability list (c-list) stores the [access control matrix](/access-control-matrix/) by row: each subject holds a list of capabilities, and each capability names one object and a set of rights on it. To use an object, a subject presents a capability from its own list; the system checks that the capability names the object and holds the right. A capability must be unforgeable, so the system keeps the lists and a subject names a capability only by its position, its slot, in its own list. Dennis and Van Horn (1966) introduced the idea. Capabilities make "what can this subject use?" cheap, and make it easy to pass a right, or only part of it, from one program to another. "Who can use this object?" and revocation are the hard part, which the [access control list](/access-control-list/), the column view, makes easy.

## In plain words

Think of the keys on a key ring. Each key opens one door, and some keys only let you look, not change things. A guard does not ask who you are; you show a key, and the guard checks that it fits this door. Keys are made by a locksmith that nobody can copy, so you cannot cut your own.

You can give a friend a copy of one of your keys, or a weaker copy that only lets them look. You cannot make a copy that does more than your own key does.

Taking keys back is harder. The locksmith keeps a record of who copied which key from whom. To take back a key, the locksmith takes it and every copy made from it, and copies of those copies, wherever they are.

## The abstract type

A capability system stores a protection state $(S, O, A)$. Each subject $s$ has a c-list, a table of numbered slots. A slot holds a capability $(o, T)$ with $o \in O$ and $T \subseteq R$. The matrix is the union over the row: $A[s, o]$ is the union of the sets $T$ of the capabilities $(o, T)$ in the c-list of $s$. The operations are:

- CREATE$(s, o, T)$: the system gives $s$ a new capability $(o, T)$, for example when $s$ creates $o$, and returns its slot.
- CHECK$(s, i, o, r)$: true when slot $i$ of $s$ holds a capability for $o$ with $r$ in its rights.
- DELEGATE$(s, i, t, T)$: give $t$ a copy of the capability in slot $i$ of $s$, with the rights $T$; refuse if $T$ is not a subset of its rights.
- REVOKE$(s, i)$: remove the capability in slot $i$ of $s$ and every capability that was copied from it, directly or through other copies.
- SLOTS$(s)$: the c-list of $s$, which is the row of $s$.

The request names a slot, not only an object. This is the difference from the matrix test $r \in A[s, o]$: a subject uses the authority it chooses to present, and nothing else. A subject that holds two capabilities for $o$ uses one of them at a time.

## Representation

The system holds two tables, out of reach of the subjects:

- for each subject $s$, its c-list: a map from slot numbers to capability records, as an array or a [hash table](/hash-table/);
- for each capability record $c$: its holder and slot, its object $\mathrm{obj}(c)$, its rights $\mathrm{rights}(c)$ as a bit mask of $r$ bits, its parent (the capability it was copied from, or none for a root), and the set of its children.

The parent links form a forest, the derivation tree: each root comes from CREATE, and each other node from one DELEGATE. The seL4 kernel keeps such a tree and calls it the capability derivation tree.

**Invariant (C).** (C1) Each record is in exactly one slot, the slot of its holder that it names. (C2) The parent of each record is a stored record, with the same object, and the rights of the record are a subset of the rights of its parent (attenuation). (C3) The children of each record are exactly the records whose parent it is. Slot numbers of a subject are never reused, so an old slot number can never name a new capability.

## Operations

```pseudo id=main
CREATE(s, o, T)
L1  T ← T as a set of rights
L2  put a new root (o, T) in the next slot of the c-list of s; return the slot

CHECK(s, i, o, r)
L3  if slot i of s is empty then return false
L4  (o', T') ← the capability in slot i of s
L5  return o' = o and r ∈ T'

DELEGATE(s, i, t, T)
L6  if slot i of s is empty then return none
L7  c ← the capability in slot i of s
L8  if T ⊄ rights(c) then return none            ▷ a copy never gains rights
L9  put a new child (obj(c), T) of c in the next slot of t; return the slot

REVOKE(s, i)
L10 if slot i of s is empty then return 0
L11 stack ← [the capability in slot i of s]; detach it from its parent
L12 while stack is not empty do
L13     c ← pop stack; push the children of c
L14     clear the slot of c in the c-list of its holder
```

**Create.** Lines L1 and L2 make a root of the derivation tree. Which subject may call CREATE is policy, outside the structure: usually the system calls it when a subject creates a new object, with all rights.

**Check.** Line L3 denies an empty slot, so a guessed slot number gives nothing. Lines L4 and L5 test the object and the right of the one capability that the subject presented. Both steps are one lookup, $O(1)$ time with an array c-list. The check needs no identity of the subject beyond whose c-list to read; the system knows that, because it runs the subject.

**Delegate.** Line L8 is attenuation: the new rights must be a subset of the rights of the capability that is copied. With rights as a bit mask the test is one AND, $O(1)$ time. Line L9 links the copy to its parent, which REVOKE needs later. The receiver $t$ gets a new slot number in its own c-list; the slot number of $s$ means nothing to $t$.

**Revoke.** Lines L11 to L14 are a [depth-first search](/depth-first-search/) of the subtree of the derivation tree under the revoked capability, and they clear each slot they visit. Each capability has one parent, so it is pushed once, and the time is linear in the number of capabilities removed. This REVOKE also removes the capability itself; seL4 splits the two steps, and its revoke removes only the copies and keeps the capability that it is called on.

## Example

Take the matrix of the [access control matrix](/access-control-matrix/) page. The system creates three roots: alice gets f1 with {own, r, w}, and bob gets f2 with {own, r, w} and the printer p with {w}. Then the owners delegate: alice gives bob r on f1, bob gives alice and carol r on f2, and bob gives carol w on p. The c-lists are the rows of the matrix:

| subject | slot | object | rights | parent |
|---|---|---|---|---|
| alice | 0 | f1 | own, r, w | root |
| alice | 1 | f2 | r | bob slot 0 |
| bob | 0 | f2 | own, r, w | root |
| bob | 1 | p | w | root |
| bob | 2 | f1 | r | alice slot 0 |
| carol | 0 | f2 | r | bob slot 0 |
| carol | 1 | p | w | bob slot 1 |

CHECK(carol, 1, p, w) is true. CHECK(carol, 0, p, w) is false: slot 0 holds a capability for f2, not for p, so carol cannot use her right on f2 to print. DELEGATE(carol, 0, alice, {w}) returns none, because {w} is not a subset of {r}.

Now carol passes her copy on: DELEGATE(carol, 0, alice, {r}) puts a copy of a copy in alice slot 2. Bob then calls REVOKE(bob, 0). The search starts at bob slot 0, finds its children alice slot 1 and carol slot 0, and under carol slot 0 it finds alice slot 2. It clears all four slots and returns 4. After this nobody holds a capability for f2, alice has only slot 0, and carol has only slot 1. A later CHECK(alice, 2, f2, r) is false, and slot 2 of alice is never used again.

The question "who can use f2?" needs a scan of all c-lists, or of the derivation tree under all roots for f2. Here it is alice, bob and carol before the revoke, and nobody after it.

## Correctness

Invariant (C) holds after each operation: CREATE adds a root, DELEGATE adds a child with a subset of its parent's rights, and REVOKE removes a whole subtree, so no stored record has a removed parent. By induction on (C2), the rights of every capability are a subset of the rights of the root it comes from, and each root was made by CREATE. So a subject can hold a right on an object only through a chain of delegations from a capability that the system created; this is the precise sense of "unforgeable" here. CHECK returns true exactly when the presented slot holds a capability for the object with the right. REVOKE removes exactly the capability and its descendants, which is the set of capabilities that would not exist if the revoked one had never been made. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/), with the rights of a capability in one word, and the c-lists as arrays indexed by slot. With hash tables for the c-lists, the times below are expected times.

| operation | time |
|---|---|
| CREATE | $O(1)$ |
| CHECK | $O(1)$ |
| DELEGATE | $O(1)$ |
| REVOKE | $O(k)$ for $k$ capabilities removed, at most $O(n)$ |
| SLOTS (one row) | $O(\text{length of the c-list})$ |
| holders of one object (one column) | $O(n)$, a scan of all c-lists |
| space | $\Theta(n + s)$ records |

Revocation is cheap here because the derivation tree is kept. Without it, as in a system where capabilities are bit strings that a subject can copy freely, revocation needs a scan of every c-list, or it is not possible at all.

## Variants

- **Protection in hardware.** The machine keeps capabilities in segments that only special instructions can write, as the CAP computer at Cambridge did, or it marks each word that holds a capability with a tag bit that only those instructions can set, as the [CHERI architecture](/cheri-capability-model/) does. Then a program can keep capabilities in its own memory and still cannot forge one.
- **Sparse capabilities.** A capability is a bit string that holds the object name, the rights and a secret check field, for example a [message authentication code](/message-authentication-code/) of the other fields under a key of the server. A subject can store and send it as plain data, and forgery is as hard as guessing the check field. Such capabilities can be copied without the system knowing, so revocation needs a new key or a new object.
- **Revocation by indirection.** Redell and Fabry proposed to give out a capability that points to an indirect object, which points to the real one. The owner revokes all copies at once by destroying the indirect object, with no derivation tree. This is selective: each holder can get a separate indirect object.
- **Amplification.** Some systems let a trusted procedure add rights to a capability that it receives, for example to read the inside of an abstract data type. This is the controlled exception to line L8.
- **File descriptors.** An open file descriptor in Unix works as a capability: it is an index into a table that the kernel holds, and it can be passed to another process. Capability modes of operating systems build on this.
- **Object capabilities.** In a memory-safe language, a reference to an object is a capability for its methods. A program can only use what it was given, which makes the [principle of least privilege](/principle-of-least-privilege/) a matter of what references a module gets.

## When to use it

Use capabilities when rights must move between programs at run time, and when each program should run with only the rights it was handed. They avoid the confused deputy of Hardy (1988): a compiler that had the right to write a billing file was asked by a user to write its output to a file with the name of that billing file, and it did, because its own authority allowed it. With capabilities the user passes a capability for the output file, and the compiler writes only through it, so it cannot use its own right by mistake. Use [access control lists](/access-control-list/) instead when owners must review and change who can use each object, when the main audit question is "who can read this file?", or when revocation must be immediate and simple.

## Pitfalls

- **Forgeable names.** If a capability is a plain object name or an address that a subject can write, anyone can make one. The slot number of line L3 is safe only because the table is out of reach of the subject; a sparse capability is safe only if the check field is long and secret.
- **No attenuation test.** If line L8 is left out, DELEGATE can make a copy with more rights than its parent, and any holder of a read capability can give itself a write capability.
- **Reused slot numbers.** If a revoked slot is filled again with a new capability, a program that still holds the old number gets the new authority. This code never reuses a slot number; a system that does must make sure no stale number can be presented.
- **Revocation without the tree.** Without parent links, REVOKE removes only one copy and the others stay. The holder may also have passed copies through channels that the system does not see, so plan revocation before handing out capabilities.
- **Confinement.** Capabilities control which objects a program can use, but not where the information it reads goes. A program that holds a capability for a secret file and one for a public channel can copy the one to the other; this is the [confinement problem](/confinement-problem/).

## Implementations

The Python class keeps a hash table of slots for each subject and a record for each capability with its parent and its children. It never reuses slot numbers, and it gives views of the rows, the matrix and the holders of one object. The tests compare it with an oracle that keeps every capability ever made and a flag for each explicit revoke, and treats a capability as live when it and all its ancestors are not revoked; they run random sequences of create, delegate, revoke and check.

## History

Dennis and Van Horn (1966) defined capabilities and the c-list of a computation as part of a design for a multiprogrammed system. Lampson (1971) showed that the c-lists are the rows of the access matrix. Hardware and operating systems with capabilities followed in the 1970s, among them Hydra at Carnegie Mellon and the CAP computer at Cambridge, and Fabry (1974) argued for capabilities as the general form of addresses. Saltzer and Schroeder (1975) compared them with access lists and named revocation as their main problem, and Redell and Fabry (1974) gave revocation by indirection. Hardy (1988) gave the confused deputy as the case that capabilities solve and access lists do not. The seL4 microkernel keeps a capability derivation tree for revocation.

## References
