---
tag: PN153Q
kind: model
slug: harrison-ruzzo-ullman-model
name: Harrison-Ruzzo-Ullman model
aliases:
- HRU model
area: security-and-privacy/access-control-and-information-flow
level: core
summary: Models a protection system as an access matrix changed by commands made of conditions on rights and primitive operations such as enter, delete, create and destroy.
model: word-ram
prereqs: [access-control-matrix]
see_also: [hru-safety-undecidability, take-grant-model, access-control-matrix, bell-lapadula-model, halting-problem, turing-machine, confinement-problem, np-complete]
sources:
  - paper: doi:10.1145/360303.360333
    title: "Michael A. Harrison, Walter L. Ruzzo and Jeffrey D. Ullman, Protection in operating systems, Communications of the ACM 19(8), 1976, pages 461 to 471"
    locator: "Section 3 (the protection system, the six primitive operations and the formal meaning of a command), Section 4 (the definition of safety and Theorem 1 on mono-operational systems), Section 5 (Theorem 2, undecidability, and Theorem 3, systems without create)"
  - paper: doi:10.1109/TDSC.2012.77
    title: "Mahesh V. Tripunitara and Ninghui Li, The foundational work of Harrison-Ruzzo-Ullman revisited, IEEE Transactions on Dependable and Secure Computing 10(1), 2013, pages 28 to 39"
    locator: the error in the proof that mono-operational safety is in NP and the corrected proof, and the two versions of safety
  - paper: "Michael A. Harrison and Walter L. Ruzzo, Monotonic protection systems, in R. A. DeMillo, D. P. Dobkin, A. K. Jones and R. J. Lipton (editors), Foundations of Secure Computation, Academic Press, 1978"
    locator: safety of monotonic systems with conditions of two tests and with conditions of one test
  - book: isbn:9780321712332
    title: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018"
    locator: "Chapter 2 (Access Control Matrix) and Chapter 3 (Foundational Results)"
---

The Harrison-Ruzzo-Ullman (HRU) model is a formal model of the protection system of an operating system: an [access control matrix](/access-control-matrix/) whose state changes only through a fixed, finite set of commands, and each command is a test on rights followed by a short list of primitive operations. Harrison, Ruzzo and Ullman made the model in 1976 to state the *safety question* exactly: can a given right ever reach a cell of the matrix where it was not before? Their main result, on the separate page [undecidability of safety in the HRU model](/hru-safety-undecidability/), is that this question has no general algorithm. This page describes the model itself: its states, its commands, the question it asks and the known decidable and hard cases.

## The machine

**Rights, subjects and objects.** A protection system has a finite set $R$ of *generic rights* (for example own, read, write, execute) and a finite set $C$ of commands. A *configuration* is a triple $(S, O, A)$. Here $O$ is the finite set of current objects, $S \subseteq O$ is the set of current subjects, and $A[s, o] \subseteq R$ for $s \in S$ and $o \in O$ is the access matrix. A subject is also an object, so subjects can hold rights over each other. HRU write the matrix as $P$; this page uses $A$, as in the other access control pages.

**Primitive operations.** There are six. Each one is defined only when its precondition holds.

| operation | precondition | effect |
|---|---|---|
| enter $r$ into $A[s, o]$ | $s \in S$, $o \in O$ | $A[s, o] \leftarrow A[s, o] \cup \{r\}$ |
| delete $r$ from $A[s, o]$ | $s \in S$, $o \in O$ | $A[s, o] \leftarrow A[s, o] \setminus \{r\}$ |
| create subject $s'$ | $s' \notin O$ | add $s'$ to $S$ and $O$, with an empty row and an empty column |
| create object $o'$ | $o' \notin O$ | add $o'$ to $O$, with an empty column |
| destroy subject $s'$ | $s' \in S$ | remove $s'$ from $S$ and $O$, with its row and column |
| destroy object $o'$ | $o' \in O \setminus S$ | remove $o'$ from $O$, with its column |

**Commands.** A command has formal parameters $X_1, \ldots, X_k$, which stand for objects. It has the form

$$\textbf{command } \alpha(X_1, \ldots, X_k)\ \ \textbf{if } r_1 \in A[X_{s_1}, X_{o_1}] \textbf{ and } \cdots \textbf{ and } r_m \in A[X_{s_m}, X_{o_m}]\ \ \textbf{then } op_1; \ldots; op_n\ \ \textbf{end}$$

The condition is a conjunction of presence tests. It cannot test that a right is absent. The body is straight-line code: no loops, no branches and no calls. The condition may be empty.

**One step.** Call $\alpha$ with actual objects $x_1, \ldots, x_k$ on the configuration $Q$. If some test of the condition fails, the step leaves $Q$ unchanged. Otherwise the primitive operations run in order, with $x_i$ in place of $X_i$. HRU define the step as a relation, and it holds only if each primitive operation is defined at the moment it runs. So a call whose body creates a name that already exists, or enters a right into a destroyed column, has no successor configuration at all. We write $Q \vdash Q'$ if some call of some command takes $Q$ to $Q'$, and $Q \vdash^* Q'$ for zero or more steps.

**A small system.** This is Example 1 of the paper, with read as the only shared right. The rights are own and read.

- CREATE(p, f): create object f; enter own into $A[p, f]$.
- CONFER(o, q, f): if own $\in A[o, f]$ then enter read into $A[q, f]$.
- REMOVE(o, q, f): if own $\in A[o, f]$ and read $\in A[q, f]$ then delete read from $A[q, f]$.

Start with two subjects, Sam and Joe, and an empty matrix. The steps CREATE(Sam, Data) and then CONFER(Sam, Joe, Data) give the matrix with own in $A[\text{Sam}, \text{Data}]$ and read in $A[\text{Joe}, \text{Data}]$.

**Cost of a step.** The model of computation for the cost of one step is the word RAM. Store the matrix as a hash map from pairs $(s, o)$ to sets of rights. Then a test, an enter and a delete cost $O(1)$ expected time, a create costs $O(1)$, and destroying a subject costs $O(s + o)$ to clear its row and column, where $s$ is the number of subjects and $o$ the number of objects. So a command with $m$ tests and $n$ operations runs in $O(m + n)$ expected time when it destroys nothing. The hard questions of the model are not about one step but about all sequences of steps.

## What it counts

The model answers one question: *safety*. HRU give two versions. This page and the theorem page use the first one, which is the formal definition of the paper.

**A leak.** A call of $\alpha$ *leaks* the generic right $r$ from $Q$ if, when it runs on $Q$, it executes "enter $r$ into $A[s, o]$" for a cell $A[s, o]$ that did not hold $r$ just before. This counts even if the same command deletes $r$ again later in its body.

**Safety.** The configuration $Q_0$ is *unsafe for $r$* if there is a configuration $Q$ with $Q_0 \vdash^* Q$ and a call that leaks $r$ from $Q$. Otherwise $Q_0$ is *safe for $r$*.

**The second version.** The second version asks whether $r$ can be entered into one given cell, or given to one given subject. HRU map it to the first version with a few extra rights and one extra command. Tripunitara and Li (2013) showed that this map is not a reduction, gave a correct reduction, and showed that the second version is also undecidable.

A leak is not always an error. The owner of a file is meant to confer read on others. HRU suggest this use: remove from the initial configuration the subjects that are trusted to hand out $r$, and then ask whether $r$ can still leak. If it can, an untrusted subject can obtain $r$ without the help of a trusted one.

In the small system above, the empty configuration with Sam and Joe is unsafe for read: CREATE(Sam, Data) and then CONFER(Sam, Joe, Data) leak read. If the CONFER command is removed from $C$, no command enters read at all, so every configuration is safe for read.

**What safety does not cover.** Safety is about rights in the matrix. A subject that may read a file and may write another file can copy the data from one to the other, and the model does not see this flow. That question is the [confinement problem](/confinement-problem/), and models such as [Bell-LaPadula](/bell-lapadula-model/) add rules for it.

## Relation to other models

- **Access control matrix.** The [access control matrix](/access-control-matrix/) of Lampson is the state of an HRU system. HRU add the commands, which are the transitions, and the safety question.
- **Take-Grant.** The [Take-Grant model](/take-grant-model/) is a protection system with four fixed rules on a graph, instead of a free choice of commands. Its safety question is decidable in linear time. The comparison shows that the undecidability of HRU comes from the free choice of commands, not from the matrix.
- **Bell-LaPadula.** The [Bell-LaPadula model](/bell-lapadula-model/) also has an access matrix in its state, but it adds security levels, and it asks a different question: does every transition keep a property of states? HRU ask whether some sequence of transitions reaches a state.
- **Turing machines.** An HRU system can simulate a [Turing machine](/turing-machine/): the subjects form the tape, the diagonal cells hold the symbols, and one command does one move. This is the proof of [undecidability](/hru-safety-undecidability/), by a reduction from the [halting problem](/halting-problem/).

## Known results in the model

Each item is a theorem, with $g = |R|$ generic rights.

- **General safety is undecidable** (HRU 1976, Theorem 2). There is no algorithm that takes a protection system, a configuration and a right and decides safety. There is even one fixed protection system, built from a universal Turing machine, for which safety is undecidable as a function of the initial configuration. Unsafety is recursively enumerable: list all finite sequences of calls. See [undecidability of safety in the HRU model](/hru-safety-undecidability/).
- **Mono-operational systems are decidable** (HRU 1976, Theorem 1). If the body of each command is one primitive operation, safety is decidable. Deletes and destroys can be dropped from a shortest leaking sequence, because conditions test only presence. The creates can be replaced by at most one create subject. So a shortest leaking sequence has length at most $g(|S_0| + 1)(|O_0| + 1) + 1$.
- **Mono-operational safety is NP-complete** when the commands are part of the input. HRU show hardness by a reduction from the [clique problem](/clique-problem/): one command tests that its $k$ parameters form a clique and then enters $r$. Tripunitara and Li (2013) found an error in the original proof of membership in NP: it assumed that a mono-operational system is monotonic for the purpose of safety. They gave a corrected proof, so the NP-complete result stands.
- **No create** (HRU 1976, Theorem 3). If no command creates a subject or an object, the set of configurations is finite, and safety is [PSPACE](/pspace/)-complete.
- **Monotonic systems** (Harrison and Ruzzo 1978). A system is monotonic if no command deletes a right or destroys a subject or an object. Safety stays undecidable for monotonic systems, and even for monotonic systems whose conditions have at most two tests (biconditional). For monotonic systems whose conditions have at most one test (monoconditional), safety is decidable.
- **Specific systems.** These results are about the class of all systems. The safety of one fixed system, or of a narrow class such as Take-Grant, can be decidable, and HRU point out that it can also be decidable but arbitrarily hard.

## References
