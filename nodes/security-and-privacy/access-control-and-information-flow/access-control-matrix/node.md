---
tag: 95ERZP
kind: model
slug: access-control-matrix
name: Access control matrix
aliases:
- Lampson access matrix
- protection matrix
area: security-and-privacy/access-control-and-information-flow
level: intro
summary: A model of protection state as a matrix whose rows are subjects, whose columns are objects, and whose cells list the rights a subject holds on an object.
model: word-ram
prereqs: [adjacency-matrix, sparse-matrix]
see_also: [access-control-list, capability-list, harrison-ruzzo-ullman-model, take-grant-model, discretionary-access-control, role-based-access-control, reference-monitor, hru-safety-undecidability]
sources:
  - paper: doi:10.1145/775265.775268
    title: Butler W. Lampson, Protection, Proceedings of the 5th Princeton Conference on Information Sciences and Systems, 1971, reprinted in ACM SIGOPS Operating Systems Review 8(1), 1974
    locator: pages 18 to 24 of the reprint (domains, objects, the access matrix, and its storage by rows as capability lists and by columns as access lists)
  - paper: doi:10.1145/1478873.1478928
    title: G. Scott Graham and Peter J. Denning, Protection, principles and practice, AFIPS Spring Joint Computer Conference, 1972
    locator: pages 417 to 429 (the protection rules with the owner and control rights and the copy flag, and the storage of the matrix)
  - paper: doi:10.1145/360303.360333
    title: Michael A. Harrison, Walter L. Ruzzo and Jeffrey D. Ullman, Protection in operating systems, Communications of the ACM 19(8), 1976
    locator: pages 461 to 471 (commands with conditions and primitive operations, the safety question, its undecidability, and the mono-operational case)
  - paper: doi:10.1109/TDSC.2012.77
    title: Mahesh V. Tripunitara and Ninghui Li, The foundational work of Harrison-Ruzzo-Ullman revisited, IEEE Transactions on Dependable and Secure Computing 10(1), 2013
    locator: pages 28 to 39 (the error in the proof that mono-operational safety is in NP, and a corrected proof)
  - paper: "Michael A. Harrison and Walter L. Ruzzo, Monotonic protection systems, in R. A. DeMillo, D. P. Dobkin, A. K. Jones and R. J. Lipton (editors), Foundations of Secure Computation, Academic Press, 1978"
    locator: the undecidability of safety for monotonic systems with two tests per condition, and its decidability with one test
  - paper: doi:10.1145/322017.322025
    title: Richard J. Lipton and Lawrence Snyder, A linear time algorithm for deciding subject security, Journal of the ACM 24(3), 1977
    locator: pages 455 to 464 (safety in the Take-Grant model in linear time)
  - paper: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018, ISBN 9780321712332"
    locator: Chapter 2 (the access control matrix, protection state transitions and copying, owning and attenuation of privilege) and Chapter 3 (the foundational results on safety)
---

The access control matrix is the basic model of a protection state: a table $A$ with one row for each subject, one column for each object, and in the cell $A[s, o]$ the set of rights that subject $s$ holds on object $o$. A request "may $s$ do $r$ to $o$?" is allowed exactly when $r \in A[s, o]$. Lampson (1971) proposed it, Graham and Denning (1972) gave rules that change it, and the [Harrison-Ruzzo-Ullman model](/harrison-ruzzo-ullman-model/) (1976) made those rules into a formal system whose [safety question is undecidable](/hru-safety-undecidability/). Real systems do not store the matrix as a table: they store its columns as [access control lists](/access-control-list/) or its rows as [capability lists](/capability-list/).

## The machine

**State.** A protection state is a triple $(S, O, A)$. $S$ is a finite set of subjects (users, processes, domains), $O$ is a finite set of objects (files, devices, memory segments, and also the subjects themselves), with $S \subseteq O$, and $R$ is a fixed finite set of generic rights, for example $\{own, r, w, x\}$. The matrix is a function $A : S \times O \to 2^R$. Write $s = |S|$, $o = |O|$ and $r = |R|$. The subjects are also columns so that rights over a subject, such as the right to stop a process, fit in the same table.

**Request.** A request is a triple $(s, o, r)$ with $s \in S$, $o \in O$ and $r \in R$. The decision is
$$\mathrm{allow}(s, o, r) \iff r \in A[s, o].$$
A [reference monitor](/reference-monitor/) is the component that receives each request and applies this test.

**Transitions.** The state changes through commands. In the HRU form, a command has parameters, a condition that is a conjunction of tests "$r \in A[x, y]$", and a body that is a sequence of six primitive operations: enter $r$ into $A[x, y]$, delete $r$ from $A[x, y]$, create subject $x$, create object $y$, destroy subject $x$, destroy object $y$. A command runs its body only when its condition holds. Two typical commands are:

```pseudo id=main
command CREATE-FILE(x, f)
L1  create object f
L2  enter own into A[x, f]
L3  enter r into A[x, f]
L4  enter w into A[x, f]

command GRANT-READ(x, y, f)
L5  if own in A[x, f] then
L6      enter r into A[y, f]
```

The commands are the policy of the system. A system where the owner of an object adds rights for others is [discretionary](/discretionary-access-control/); a system with no command that lets a user change rights on labeled objects is [mandatory](/mandatory-access-control/). Graham and Denning used a fixed set of eight rules: create and destroy an object, create and destroy a subject, read, grant, delete and transfer a right. Their rules use a right *own* on an object, a right *control* on a subject, and a copy flag: a holder of $r^*$ may pass $r$ or $r^*$ to another subject.

**Example.** Take three subjects alice, bob and carol, and three objects f1, f2 and p (a printer). The columns for the subjects are left out, because no right on a subject is used.

| | f1 | f2 | p |
|---|---|---|---|
| alice | own, r, w | r | |
| bob | r | own, r, w | w |
| carol | | r | w |

The request (bob, f2, w) is allowed. The request (carol, f2, w) is denied, because w is not in $A[\text{carol}, \text{f2}]$. The command GRANT-READ(alice, carol, f1) passes the test of line L5, because alice owns f1, and line L6 enters r into $A[\text{carol}, \text{f1}]$. The command GRANT-READ(carol, alice, f2) does nothing, because carol does not own f2.

## What it counts

The model answers two questions of very different cost.

**The access decision.** For a fixed state, the decision is one membership test. In the [word RAM](/word-ram/), with the matrix stored as an array of $s \cdot o$ cells and each cell as a bit mask of $r$ bits, the test takes $O(1)$ time and the state takes $s \cdot o \cdot r$ bits. Most cells are empty in practice, so systems store only the nonempty cells, as a [sparse matrix](/sparse-matrix/) does. The cost of the decision then depends on the storage:

| storage | what one object or subject keeps | cost of the decision |
|---|---|---|
| full table | nothing; one array | $O(1)$ |
| by column ([access control list](/access-control-list/)) | each object keeps the list of $(s, A[s, o])$ with $A[s, o] \ne \emptyset$ | a scan of one list, $O(s)$; $O(1)$ expected with a [hash table](/hash-table/) |
| by row ([capability list](/capability-list/)) | each subject keeps the list of $(o, A[s, o])$ | $O(1)$ when the subject names the entry; $O(o)$ to search the row |
| authorization relation | the set of triples $(s, o, r)$ with $r \in A[s, o]$ | $O(1)$ expected with a hash table |

The two views make different questions cheap. "Who can use object $o$?" is one column, so it is cheap with lists and costs a scan of all rows with capabilities. "What can subject $s$ use?" is one row, so it is cheap with capabilities and costs a scan of all lists with access lists. Revoking all rights of one subject, or all access to one object, has the same split.

**The safety question.** Given a set of commands, an initial state $Q_0$ and a right $r$, is there a sequence of commands that enters $r$ into a cell of the matrix that did not hold $r$ before? HRU call a state where some command does this a *leak* of $r$, and $Q_0$ is *unsafe for $r$* if a leak is reachable from it. This page uses the plain form, where every subject of $Q_0$ counts. HRU also discuss the form where the subjects that are trusted to pass rights are removed first, because those subjects leak rights by design. In the example, with the two commands above, the state is unsafe for r, because GRANT-READ(alice, carol, f1) leaks it. It is also unsafe for w in the plain form, because CREATE-FILE enters w into the new cell of the new file. This shows how coarse the plain question is. The question a defender asks, "can carol ever get w on f2?", has the answer no: line L6 enters only r, and line L4 enters w only into the column of a file that the command creates. The number of states over fixed sets $S$ and $O$ is $2^{s o r}$, which is $2^{27} = 134217728$ for the example; when commands can create subjects and objects, the set of reachable states can be infinite.

## Relation to other models

- **Graphs.** The matrix is the [adjacency matrix](/adjacency-matrix/) of a bipartite graph from subjects to objects, with each edge labeled by a set of rights. The [Take-Grant model](/take-grant-model/) works on this graph directly and adds the rights take and grant as edges between subjects.
- **HRU.** The [Harrison-Ruzzo-Ullman model](/harrison-ruzzo-ullman-model/) is the matrix with an arbitrary finite set of commands of the form above. Lampson's matrix is its state; the HRU commands are its transitions.
- **Policy models.** [Discretionary](/discretionary-access-control/) and [mandatory access control](/mandatory-access-control/) are classes of command sets. The [Bell-LaPadula model](/bell-lapadula-model/) keeps a matrix as its discretionary part and adds labels. [Role-based access control](/role-based-access-control/) gives a matrix when the user to role and role to permission relations are composed. [Attribute-based](/attribute-based-access-control/) and [relationship-based access control](/relationship-based-access-control/) compute each cell from attributes or from a graph when the request comes, so the matrix is never stored.
- **Storage.** The [access control list](/access-control-list/) is a column of the matrix and the [capability list](/capability-list/) is a row. Both hold the same information as the matrix, but they make different operations cheap.

## Known results in the model

- **Decision.** For a fixed stored state the access decision is a lookup, in $O(1)$ time in the word RAM with a full table.
- **General safety is undecidable.** HRU (1976) proved that the safety question is undecidable for arbitrary command sets, by a reduction from the halting problem of a [Turing machine](/turing-machine/): the matrix holds the tape on its diagonal and each command does one move. See [HRU safety undecidability](/hru-safety-undecidability/).
- **Mono-operational systems.** When each command has one primitive operation, safety is decidable, and HRU showed that it is NP-complete. Tripunitara and Li (2013) found an error in the proof that the problem is in NP and gave a corrected proof.
- **Monotonic systems.** Harrison and Ruzzo (1978) showed that safety stays undecidable when no command deletes a right or destroys a subject or object, and stays undecidable for monotonic systems with conditions of two tests. With one test per condition, the monotonic case is decidable.
- **Take-Grant.** In the [Take-Grant model](/take-grant-model/), safety is decidable in time linear in the size of the graph (Jones, Lipton and Snyder 1976; Lipton and Snyder 1977).
- **Storage is exact.** Both the set of access lists and the set of capability lists determine the matrix, and the matrix determines both. The proofs are on the [access control list](/access-control-list/) and [capability list](/capability-list/) pages, and their code checks the two views against the matrix by brute force.

## References
