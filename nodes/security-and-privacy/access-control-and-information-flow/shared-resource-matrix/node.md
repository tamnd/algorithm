---
tag: 3Z77T4
kind: algorithm
slug: shared-resource-matrix
name: Shared resource matrix method
aliases:
- Kemmerer shared resource matrix
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: Finds potential covert channels by tabulating which operations reference and modify each shared attribute, closing the table under indirect references, and keeping the rows with both.
model: word-ram
complexity:
  vars: {n: the number of attributes, m: the number of primitives}
  time: {worst: O(m n^2), best: Θ(m n)}
  space: {extra: O(n^2 + m n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1982
  people: [Richard A. Kemmerer]
  note: Kemmerer presented the method at the 1982 IEEE Symposium on Security and Privacy and published the journal version in ACM Transactions on Computer Systems in 1983.
prereqs: [covert-channel, transitive-closure, depth-first-search]
see_also: [confinement-problem, reachability, warshall-algorithm, access-control-matrix, bell-lapadula-model, noninterference, timing-attack, quantitative-information-flow]
sources:
  - paper: doi:10.1145/357369.357374
    title: Richard A. Kemmerer, Shared resource matrix methodology, an approach to identifying storage and timing channels, ACM Transactions on Computer Systems 1(3), 1983
    locator: pp. 256 to 277, the matrix, the transitive closure step, and the minimum criteria for storage and timing channels
  - paper: doi:10.1109/SP.1982.10007
    title: Richard A. Kemmerer, A practical approach to identifying storage and timing channels, Proceedings of the 1982 IEEE Symposium on Security and Privacy
    locator: the first presentation of the method
  - paper: doi:10.1109/CSAC.2002.1176284
    title: Richard A. Kemmerer, A practical approach to identifying storage and timing channels, twenty years later, Proceedings of ACSAC 2002
    locator: pp. 109 to 118, the file system example (Tables 1, 2 and 3), the closure rule, Section 4 on the results for a network front-end, and the later comments on covert flow trees
  - paper: doi:10.1109/RISP.1991.130770
    title: Phillip A. Porras and Richard A. Kemmerer, Covert flow trees, a technique for identifying and analyzing covert storage channels, Proceedings of the 1991 IEEE Symposium on Security and Privacy
    locator: pp. 36 to 51, covert flow trees as a follow-up that also produces the signaling scenarios
  - book: isbn:9780321712332
    title: Matt Bishop, Computer Security, Art and Science, second edition, Addison-Wesley, 2018
    locator: Chapter 18 (The Confinement Problem), Section 18.3 on covert channels, which covers the shared resource matrix
---

The shared resource matrix method of Kemmerer finds the places in a system design where two processes might signal each other through a shared resource. It writes a table with one row for each attribute of a shared resource and one column for each primitive operation, marks R where a primitive references an attribute and M where it modifies one, adds the R entries that indirect references imply, and keeps the rows that have both an R and an M. Each kept row is a candidate for a [covert channel](/covert-channel/) that an analyst must then confirm or rule out. With $n$ attributes and $m$ primitives the closure costs $O(m n^2)$ time on a word RAM.

## In plain words

A system has some shared state, such as a lock bit or a count of jobs, and some operations that processes may call. For a covert channel, one process must be able to change a piece of state, and another process must be able to see it, directly or through a chain of other state.

So you make a table. For each operation you note what state it looks at and what state it changes. Then you follow the chains: if an operation looks at the job count, and another operation sets the job count from the caller's level, then the first operation also learns about the level. At the end, every piece of state that some operation changes and some operation can see is a place to check by hand. The table does not prove that a channel exists. It tells you where to look.

## The problem

The input is a design given as a set $A$ of $n$ attributes of shared resources (fields of files, locks, queues, the clock), a set $P$ of $m$ primitives (the operations that a process can call), and for each primitive $q$ two sets: $R_0(q) \subseteq A$, the attributes that $q$ references, and $M(q) \subseteq A$, the attributes that $q$ modifies. A primitive references an attribute when its result, its effect or its timing depends on the value of the attribute.

The output has two parts:
- the closed matrix: for each primitive $p$, the set $R^*(p)$ of attributes that $p$ references directly or indirectly. Kemmerer's closure rule is: if $p$ references $a$ and some $q$ modifies $a$, then $p$ references every attribute that $q$ references. $R^*$ is the least family that contains $R_0$ and obeys this rule;
- the candidates: each attribute $a$ such that some primitive modifies $a$ and some primitive references $a$ in $R^*$, with its modifiers and its sensors.

The threat is two processes that cooperate: a sender that may see a secret and a receiver that may not, under a policy such as [Bell-LaPadula](/bell-lapadula-model/) that forbids the legal flow. The method covers channels through the attributes in the table. It says nothing about state that the table leaves out.

## The algorithm

The closure is reachability in a graph on the attributes. Put an edge $a \to b$ when some primitive $q$ modifies $a$ and references $b$: a reader of $a$ may learn about $b$, because $q$ wrote $a$ after it saw $b$. Then $R^*(p)$ is the set of attributes reachable from $R_0(p)$.

```pseudo id=main
SHARED-RESOURCE-MATRIX(A, P, R0, M)
L1   for each attribute a in A do E[a] ← ∅            ▷ a → b: a reader of a learns b
L2   for each primitive q in P do
L3       for each a in M[q] do
L4           E[a] ← E[a] ∪ R0[q]
L5   for each primitive p in P do
L6       R[p] ← R0[p];  S ← stack of the elements of R0[p]
L7       while S is not empty do
L8           a ← pop(S)
L9           for each b in E[a] with b ∉ R[p] do
L10              R[p] ← R[p] ∪ {b};  push b on S
L11  C ← empty list
L12  for each attribute a in A do
L13      if a ∈ M[q] for some q and a ∈ R[p] for some p then append (a, modifiers of a, sensors of a) to C
L14  return R, C
```

Lines L1 to L4 build the flow graph, one edge set per attribute. Lines L5 to L10 run a [depth-first](/depth-first-search/) style search from the direct references of each primitive; the stack holds the attributes whose edges are not yet followed. Line L13 keeps the rows of the closed matrix that have both an M and an R. The M entries never change: the closure only adds R entries.

The analyst then looks at each candidate row. Kemmerer's minimum criteria for a storage channel are: the sender and the receiver have access to the same attribute; the sender can make the attribute change; the receiver can detect the change; and there is a way to start the communication and to put the events in order. Each reference to a candidate then ends in one of four conclusions: a legal channel between the two processes already exists, so nothing more is lost; no useful information can pass; the sender and the receiver must be the same process; or a potential storage channel exists. For timing channels, the table has a row for a time reference such as the system clock, and a receiver must be able to see the sender change its response time.

## Example

A print spooler, made up for this page, has four attributes and four primitives. Level is the security class of the caller, Queue the list of jobs, Count the number of jobs, and Owner the owner of each job. SUBMIT reads the caller's level and the count (to check the limit), and adds a job, which changes the queue, the count and the owner field. CANCEL checks the owner and the level and removes a job. STATUS returns the count. LIST shows the queue entries that the caller's level allows.

The input matrix (rows are attributes):

| attribute | SUBMIT | CANCEL | STATUS | LIST |
| --- | --- | --- | --- | --- |
| Level | R | R | | R |
| Queue | M | M | | R |
| Count | R, M | M | R | |
| Owner | M | R | | |

Lines L1 to L4 give the edges. SUBMIT modifies Queue, Count and Owner and references Level and Count, so each of the three gets the edges to Level and Count. CANCEL modifies Queue and Count and references Level and Owner. The result is $E[\text{Level}] = \emptyset$, $E[\text{Queue}] = E[\text{Count}] = \{\text{Level}, \text{Count}, \text{Owner}\}$ and $E[\text{Owner}] = \{\text{Level}, \text{Count}\}$.

The search of lines L5 to L10, one primitive at a time:

| primitive | $R_0$ | pop | added (edge) | $R$ after |
| --- | --- | --- | --- | --- |
| SUBMIT | Level, Count | Count | Owner (Count → Owner) | Level, Count, Owner |
| CANCEL | Level, Owner | Owner | Count (Owner → Count) | Level, Owner, Count |
| STATUS | Count | Count | Level, Owner (Count → Level, Count → Owner) | Count, Level, Owner |
| LIST | Level, Queue | Queue | Count, Owner (Queue → Count, Queue → Owner) | all four |

The other pops add nothing. The closed matrix:

| attribute | SUBMIT | CANCEL | STATUS | LIST |
| --- | --- | --- | --- | --- |
| Level | R | R | R | R |
| Queue | M | M | | R |
| Count | R, M | R, M | R | R |
| Owner | R, M | R | R | R |

Line L13 keeps Queue, Count and Owner. Level is not a candidate, because no primitive modifies it. The analysis of Count is the classic one: a high process calls SUBMIT to change the count, and a low process calls STATUS and sees it, so the four criteria can hold and Count is a potential storage channel unless the design keeps one count per level. The new R entry of STATUS on Owner says the same thing in the closed table: the value that STATUS returns depends on who submitted jobs.

The implementation also reproduces Kemmerer's own file system example (Table 1 of the 2002 paper, 10 attributes and 8 primitives). The closure gives Table 2 of the paper, and line L13 returns five rows (Buffer, Locked By, Locked, In-use Set and Value). The analysis in the paper keeps two of them, In-use Set and Locked, as potential storage channels (Table 3). The other three end in one of the four conclusions above.

## Correctness

The main claim is that $R^*(p) = \mathrm{Reach}(R_0(p))$ in the flow graph. The set of reachable attributes obeys Kemmerer's rule: if $a$ is reachable and $q$ modifies $a$, then every direct reference $b$ of $q$ is one edge further, so everything reachable from the references of $q$ is reachable from those of $p$. And every family that obeys the rule contains the reachable sets, by induction on the length of the path. So the reachable sets form the least closed family. The search of lines L6 to L10 keeps the invariant "every attribute in $R[p]$ that is not on the stack has all its successors in $R[p]$", so when the stack is empty $R[p]$ is closed under the edges and equals the reachable set. The full proof is in proofs/correctness.md.

What the method guarantees is a statement about the model, not about the system: if the table lists every attribute and every reference and modification correctly, then a storage channel through these attributes can only use a candidate row. This is a theorem about the table. The completeness of the table itself is the analyst's job, and the method gives no guarantee about state that the table omits, about channels that need no shared attribute (such as power or electromagnetic emission), or about the bandwidth.

## Complexity

On a word RAM with sets stored as bit vectors or boolean arrays of size $n$:
- **Lines L1 to L4.** Each primitive $q$ adds the set $R_0(q)$ to $|M(q)| \le n$ edge sets, at cost $O(n)$ each, so $O(m n^2)$ in total. The graph has at most $n^2$ edges.
- **Lines L5 to L10.** For one primitive, each attribute is pushed at most once, and when it is popped its at most $n$ successors are checked. So one search costs $O(n^2)$, and all $m$ searches cost $O(m n^2)$.
- **Lines L11 to L13.** For each attribute, scan the $m$ columns twice: $O(m n)$.

The worst case is $O(m n^2)$, reached when every primitive references and modifies most attributes. The best case is $\Theta(m n)$, since the matrix itself has $m n$ cells and line L13 reads them all. The extra space is $O(n^2)$ for the graph and $O(m n)$ for the closed matrix.

An alternative is to compute the [transitive closure](/transitive-closure/) of the flow graph once, for example with [Warshall's algorithm](/warshall-algorithm/) in $O(n^3)$, and then form each $R^*(p)$ as a union of closure rows in $O(n^2)$ per primitive. That costs $O(n^3 + m n^2)$, no better in the worst case. Kemmerer's literal procedure, which rescans the whole matrix until nothing changes, can need many passes, and each pass costs $O(m^2 n^2)$ with plain loops.

## Properties

- **Only R entries are added.** The closure never adds or removes an M entry, and never removes an R entry.
- **Monotone.** Adding an R or an M entry to the input can only add entries to the closed matrix and rows to the candidate list.
- **Idempotent.** Closing a closed matrix changes nothing. The tests check this.
- **Over-approximation.** A candidate row is a possible channel. Most candidates in practice are removed by the analysis.
- **Any description.** Kemmerer applied the method to English requirements, a formal specification and an implementation, and says it can be used in all phases of the life cycle. He also notes that a matrix built from English or from a formal specification cannot uncover all channels, so the code must be analyzed too.

## Variants and improvements

- **Timing channels.** Add a row for each time reference, such as the system clock, which every primitive references. A primitive that can make the processor wait, such as a sleep call, modifies the attribute "current process", and the analysis then looks for a primitive whose response time the sender can change. Kemmerer's 2002 paper adds a PROC SLEEP primitive and a System Clock row to the file example.
- **Covert flow trees.** Porras and Kemmerer (1991) build a tree for each attribute, whose paths are the ways a sender can change it and a receiver can detect the change. The tree gives the signaling scenarios that the matrix leaves to the analyst.
- **Code-level analysis.** Later work builds the matrix from the source code of a kernel by an information flow analysis, which makes the R and M entries less dependent on the reading of a specification. The [dataflow analysis](/dataflow-analysis/) and [taint analysis](/taint-analysis/) pages describe the underlying tools.
- **Noninterference proofs.** A proof of [noninterference](/noninterference/) for the whole system rules out every channel inside the model at once, at a much higher cost than the matrix.

## When to use it

Use the matrix early in the design of a system with a multilevel policy, when the list of shared attributes and primitives is still small enough to check by hand. It is cheap, it scales to the size of an interface, and its negative answer (an attribute is not a candidate) holds for every scenario within the model. Do not use it as a proof of security: it gives candidates, not channels, it does not estimate bandwidth, and it depends on a complete table. For bandwidth, use the [quantitative information flow](/quantitative-information-flow/) view or Millen's capacity estimates. For a proof, use noninterference.

## Pitfalls

- **The standard transitive closure.** Line L4 must add the edge from the modified attribute to the referenced one, $a \to b$ with $a \in M(q)$ and $b \in R_0(q)$. The reverse edge, or a closure of the matrix as a relation between rows and columns, gives wrong entries: a reader of $b$ learns nothing about an attribute $a$ that $q$ writes. Kemmerer calls the result the transitive closure "with respect to references", which is not the transitive closure of the matrix read as a relation. The test `test_not_standard_transitive_closure` checks this case.
- **One pass only.** Running lines L6 to L10 with a single round of edge following, instead of a search until the stack is empty, misses chains of length two or more. The test with the primitives p, q and r shows such a chain.
- **Candidates are not channels.** Line L13 lists rows to analyze. Reporting them as channels overstates the risk, and dropping them without the four-way analysis can miss a real channel.
- **The missing clock.** Without a row for the clock, the table finds no timing channels at all, because no primitive is marked as referencing time.
- **Error codes and timing of failures.** A primitive that fails in a way the caller can see references the attributes that decide the failure. Leaving out such R entries is the most common way to make the table incomplete.

## Implementations

## History

Kemmerer presented the method at the 1982 IEEE Symposium on Security and Privacy and published the full version in ACM Transactions on Computer Systems in 1983, in the setting of the confinement problem of [Lampson](/confinement-problem/) and the multilevel policies of the time. In 2002 ACSAC reprinted the 1982 paper as a classic paper with a retrospective. Section 4 there reports a measurement on the design of a secure network front-end: the method found several storage and timing channels, the worst-case bandwidth among them was 5000 bits per second and a typical one 20 bits per second, the bandwidth in practice was lower because of noise, and the front-end was redesigned to block or slow the channels. Porras and Kemmerer extended the method with covert flow trees in 1991. The retrospective also reports that both methods were applied to a formal model of a system written in the Gypsy specification language, and that both found covert channels.

## References
