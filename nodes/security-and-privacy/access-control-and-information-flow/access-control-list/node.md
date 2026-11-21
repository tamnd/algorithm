---
tag: 443DQ0
kind: data-structure
slug: access-control-list
name: Access control list
aliases:
- ACL
area: security-and-privacy/access-control-and-information-flow
level: intro
summary: Stores the access matrix by column, so that each object keeps the list of subjects that may use it and the rights of each.
model: word-ram
complexity:
  vars: {s: the number of subjects, o: the number of objects, r: the number of rights, n: the number of nonempty cells of the access matrix}
  time: {worst: O(s)}
  space: {extra: Θ(n + o)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [access-control-matrix, linked-list]
see_also: [capability-list, discretionary-access-control, reference-monitor, role-based-access-control, relationship-based-access-control, hash-table, principle-of-least-privilege]
sources:
  - paper: doi:10.1145/775265.775268
    title: Butler W. Lampson, Protection, Proceedings of the 5th Princeton Conference on Information Sciences and Systems, 1971, reprinted in ACM SIGOPS Operating Systems Review 8(1), 1974
    locator: pages 18 to 24 of the reprint (the access matrix, and the access list of an object as its column)
  - paper: doi:10.1145/361011.361067
    title: Jerome H. Saltzer, Protection and the control of information sharing in Multics, Communications of the ACM 17(7), 1974
    locator: pages 388 to 402 (the access control lists of Multics segments and directories, and the known weaknesses of the design)
  - paper: doi:10.1109/PROC.1975.9939
    title: Jerome H. Saltzer and Michael D. Schroeder, The protection of information in computer systems, Proceedings of the IEEE 63(9), 1975
    locator: pages 1278 to 1308, Section II (the list-oriented and ticket-oriented implementations, access control lists and their revocation)
  - paper: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018, ISBN 9780321712332"
    locator: Chapter 16, Section 16.1 (access control lists, their abbreviations, creation and maintenance, and revocation)
  - url: "https://www.usenix.org/conference/atc19/presentation/pang"
    title: Ruoming Pang and others, Zanzibar, Google's consistent, global authorization system, USENIX ATC 2019
    locator: pages 33 to 46 (access control lists stored as relation tuples, and checks at scale)
---

An access control list (ACL) stores the [access control matrix](/access-control-matrix/) by column: each object keeps a list of entries $(s, T)$, one for each subject $s$ that has some right on it, with $T$ the set of rights of $s$. To decide a request "may $s$ do $r$ to $o$?", the system scans the list of $o$ for the entry of $s$ and tests $r \in T$. Lampson (1971) named the structure, Multics used it for every segment, and it is the mechanism of almost every file system and many cloud services today. It makes "who can use this object?" cheap, and makes "what can this subject use?" and "remove this user everywhere" cost a scan of every list; the [capability list](/capability-list/) has the opposite trade-off.

## In plain words

Think of a guest list at the door of each room. The list names the people who may come in and what each may do inside: look, change things, or invite others. To check a visitor, the guard at the door reads the list of that room only. The guard does not care what other rooms the visitor can enter.

This makes it easy to answer "who can get into this room?": read one list. It also makes it easy for the room's owner to add or strike a name. It is hard to answer "which rooms can this person enter?", because the answer is spread over the lists of all rooms. To ban a person from the whole building, someone must visit every door and strike the name from each list.

## The abstract type

An ACL system stores a protection state $(S, O, A)$ with subjects $S$, objects $O$ and the matrix $A : S \times O \to 2^R$ over a finite set $R$ of rights. It supports these operations:

- CHECK$(s, o, r)$ returns true when $r \in A[s, o]$.
- GRANT$(s, o, r)$ sets $A[s, o] \leftarrow A[s, o] \cup \{r\}$.
- REVOKE$(s, o, r)$ sets $A[s, o] \leftarrow A[s, o] \setminus \{r\}$.
- REVOKE-SUBJECT$(s)$ sets $A[s, o] \leftarrow \emptyset$ for every object $o$.
- ENTRIES$(o)$ returns column $o$: the pairs $(s, A[s, o])$ with $A[s, o] \ne \emptyset$.
- CREATE-OBJECT$(o)$ and DELETE-OBJECT$(o)$ add or remove a column.

Who may call GRANT and REVOKE is not part of the structure. It is the policy: in [discretionary access control](/discretionary-access-control/) it is the owner of the object, in [mandatory access control](/mandatory-access-control/) it is only the system administrator, and a [reference monitor](/reference-monitor/) makes every call go through the check.

## Representation

For each object $o$ the structure keeps a list $\mathit{acl}[o]$ of entries $(s, T)$, where $s$ is a subject and $T \subseteq R$ is a set of rights stored as a bit mask of $r$ bits. A [hash table](/hash-table/) or an array maps each object to its list. The list is an array or a [linked list](/linked-list/); for this page it is a plain list that is scanned.

**Invariant (A).** For each object $o$: (A1) no two entries of $\mathit{acl}[o]$ have the same subject, and (A2) no entry has an empty set of rights.

**Abstraction.** The state stands for the matrix $M$ with $M[s, o] = T$ if $(s, T) \in \mathit{acl}[o]$, and $M[s, o] = \emptyset$ if $\mathit{acl}[o]$ has no entry for $s$. By (A1) this is a well-defined function. By (A2) the entries of $\mathit{acl}[o]$ are exactly the nonempty cells of column $o$, so the lists use space linear in the number $n$ of nonempty cells, plus one header for each object.

## Operations

```pseudo id=main
CHECK(acl, s, o, r)
L1  for each entry (s', R') in acl[o] do
L2      if s' = s then return r ∈ R'
L3  return false                               ▷ no entry: the cell is empty

GRANT(acl, s, o, r)
L4  for each entry (s', R') in acl[o] do
L5      if s' = s then R' ← R' ∪ {r}; return
L6  append (s, {r}) to acl[o]                  ▷ only when s has no entry yet

REVOKE(acl, s, o, r)
L7  for each entry (s', R') in acl[o] do
L8      if s' = s then
L9          R' ← R' \ {r}
L10         if R' = ∅ then remove the entry from acl[o]
L11         return

REVOKE-SUBJECT(acl, s)
L12 for each object o do
L13     remove the entry of s from acl[o], if there is one
```

**Check.** Lines L1 and L2 look for the entry of $s$ in the list of $o$. By (A1) there is at most one, so the first match is the only match. If there is none, the cell is empty and line L3 denies. An ACL denies by default: a subject that no list names gets nothing. The cost is the position of the entry in the list, at most $s$ steps.

**Grant.** Lines L4 and L5 add $r$ to the existing entry of $s$. Line L6 appends a new entry only when there is none, which keeps (A1). The new entry holds $\{r\}$, which is not empty, so (A2) holds. Cost: at most $s$ steps, plus $O(1)$ for the append.

**Revoke.** Lines L7 to L9 remove $r$ from the entry of $s$. Line L10 removes an entry that has become empty, which keeps (A2). If there is no entry, nothing changes. Cost: at most $s$ steps; removing from the middle of an array list costs another $O(s)$ moves, and $O(1)$ in a linked list.

**Revoke a subject.** Lines L12 and L13 visit every list. This is the cost of the column view: the rights of one subject are spread over all objects, so the operation takes time linear in $o + n$, even when $s$ has rights on only a few objects.

**Create and delete an object.** CREATE-OBJECT adds an empty list. DELETE-OBJECT removes the list with all its entries. Both take $O(1)$ time in the map, plus the time to free the entries.

## Example

Take the matrix of the [access control matrix](/access-control-matrix/) page, with subjects alice, bob and carol, objects f1, f2 and the printer p, and rights own, r and w. Its three columns are the three lists:

| object | its list |
|---|---|
| f1 | (alice, {own, r, w}), (bob, {r}) |
| f2 | (alice, {r}), (bob, {own, r, w}), (carol, {r}) |
| p | (bob, {w}), (carol, {w}) |

Now build the list of f2 from an empty state by a sequence of operations, and then change it.

| operation | the list of f2 after it | note |
|---|---|---|
| GRANT(bob, f2, own) | (bob, {own}) | line L6, new entry |
| GRANT(bob, f2, r) | (bob, {own, r}) | line L5 |
| GRANT(bob, f2, w) | (bob, {own, r, w}) | line L5 |
| GRANT(alice, f2, r) | (bob, {own, r, w}), (alice, {r}) | line L6 |
| GRANT(carol, f2, r) | (bob, {own, r, w}), (alice, {r}), (carol, {r}) | line L6 |
| CHECK(carol, f2, w) | unchanged | line L2 finds carol and returns false |
| REVOKE(alice, f2, r) | (bob, {own, r, w}), (carol, {r}) | line L10 removes the empty entry |
| GRANT(carol, p, w) | unchanged; the list of p is (carol, {w}) | |
| REVOKE-SUBJECT(carol) | (bob, {own, r, w}) | lines L12 and L13 also empty the list of p |

The last step visits both lists, f2 and p, although each holds only one entry of carol. In a system with a million files, the same step visits a million lists.

## Correctness

Each operation keeps invariant (A), and each one changes the matrix $M$ that the state stands for exactly as the abstract type says. CHECK reads the cell $M[s, o]$ because (A1) makes the entry of $s$ unique; GRANT adds $r$ to that cell and never makes a second entry; REVOKE and REVOKE-SUBJECT remove rights and drop entries that become empty, so (A2) holds and no empty cell is stored. It follows that the set of lists and the matrix determine each other: the lists of a matrix are its columns without the empty cells, and the matrix of the lists is given by the abstraction. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [word RAM](/word-ram/), with a set of rights as one word of $r$ bits, so a union, a difference and a membership test take $O(1)$ time. The map from objects to lists is a hash table, with $O(1)$ expected time for a lookup.

| operation | time with a scanned list | time with a hash table per object |
|---|---|---|
| CHECK | $O(s)$ worst | $O(1)$ expected |
| GRANT | $O(s)$ worst | $O(1)$ expected |
| REVOKE | $O(s)$ worst | $O(1)$ expected |
| ENTRIES (one column) | $O(\text{length of the list})$ | the same |
| REVOKE-SUBJECT | $O(o + n)$ | $O(o)$ expected |
| rights of one subject (one row) | $O(o + n)$ | $O(o)$ expected |
| space | $\Theta(n + o)$ entries | the same, times a constant |

A full matrix needs $s \cdot o \cdot r$ bits whatever the policy. The lists need space for the nonempty cells only, which is the reason for the column view when most subjects have no rights on most objects. Most real lists are short, so a scan is fast in practice; a long list, such as the list of a file shared with a whole company, is the case for a hash table, or for groups (see Variants).

## Variants

- **Groups and abbreviations.** An entry names a group, and a subject gets the rights of each group it is a member of. The Unix permission bits are the shortest form: three entries, for the owner, the owning group and all others, with three bits (r, w, x) each. Bishop calls these abbreviations of ACLs. A full ACL can then be needed in addition, as in the POSIX draft ACLs of Linux, which add named users and groups and a mask entry.
- **Negative entries and order.** Some systems add deny entries. The decision then depends on a rule for conflicts: "deny overrides", or "the first matching entry decides" as in Windows and NFSv4 ACLs, where tools put the deny entries first. The structure is then an ordered list, and the scan of line L1 is a first-match search.
- **Inheritance.** A directory carries a default ACL that new files in it copy. Multics and most current file systems have a form of this.
- **Propagated ACLs.** The ACL is attached to the data and follows it into copies, so that the creator keeps control. Bishop describes them as PACLs; the idea is close to the [decentralized label model](/decentralized-label-model/).
- **Relation tuples at scale.** Zanzibar stores each entry as a tuple (object, relation, user), where the user can be a set given by another tuple. A check then follows these links, which makes the ACL a form of [relationship-based access control](/relationship-based-access-control/).
- **Roles.** If the entries name roles instead of users, the ACL is the role to permission part of [role-based access control](/role-based-access-control/).

## When to use it

Use ACLs when objects are long-lived and named, when the owner of an object must see and change who can use it, and when the main audit question is "who can read this file?". This is the case in file systems and in most services with a sharing dialog. ACLs need the system to know who the subject is at each check, so they depend on authentication, and they give a program the rights of the user who runs it, which makes the confused deputy problem possible (see [capability list](/capability-list/)). Use [capability lists](/capability-list/) instead when rights must be passed between programs at run time, or when each program must hold only the rights it needs, as the [principle of least privilege](/principle-of-least-privilege/) asks.

## Pitfalls

- **A second entry for the same subject.** If GRANT appends at line L6 without the scan of lines L4 and L5, a subject can get two entries. Then CHECK reads the first one only, and REVOKE at line L10 removes one entry and leaves the other, so a revoked right stays. Always look for the entry first, as lines L4 and L5 do.
- **Revocation that waits for the next open.** Most file systems check the ACL when a file is opened, not on each read. After REVOKE, a process that opened the file earlier keeps its access through the open handle until it closes it. If revocation must be immediate, the reference monitor must check at each use, or the system must close the handles.
- **A removed user whose name comes back.** If REVOKE-SUBJECT is not run when a user is deleted, and a new user later gets the same identifier, the new user gets all the old entries. Run lines L12 and L13 at deletion, or never reuse identifiers.
- **An entry in the wrong order.** In a first-match list, a deny entry placed after an allow entry for the same subject is never reached. Keep a canonical order, or use "deny overrides" as the rule.
- **Empty entries.** If line L10 is left out, the list keeps entries with no rights. CHECK is still right, but ENTRIES lists subjects that have no access, and an audit of "who can use this object?" is wrong.

## Implementations

The Python class follows the main block with one scanned list for each object. It adds CREATE-OBJECT, DELETE-OBJECT, the conversions to and from a matrix, and a check of invariant (A). The tests compare every operation with a plain dictionary of matrix cells on random sequences, and check the column view against the matrix on every matrix over two subjects, two objects and two rights.

## History

Lampson's 1971 paper on protection described the access matrix and named its two storage forms, access lists for the columns and capability lists for the rows. Multics, designed from 1965, put an access control list on every segment, and Saltzer (1974) described the design and its weaknesses. Saltzer and Schroeder (1975) compared the list-oriented and the ticket-oriented forms. Unix (1970s) kept only the three abbreviated entries for owner, group and others. Large services now keep ACLs as relation tuples, as in Zanzibar (2019).

## References
