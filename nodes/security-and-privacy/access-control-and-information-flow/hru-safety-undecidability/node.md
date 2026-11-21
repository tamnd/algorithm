---
tag: ANB1ZW
kind: theorem
slug: hru-safety-undecidability
name: Undecidability of safety in the HRU model
aliases:
- HRU safety theorem
- Harrison-Ruzzo-Ullman theorem
area: security-and-privacy/access-control-and-information-flow
level: core
summary: Whether some command sequence can enter a given right into a cell of the access matrix that lacked it is undecidable for HRU systems, and NP-complete for mono-operational ones.
prereqs: [harrison-ruzzo-ullman-model, halting-problem, turing-machine]
see_also: [harrison-ruzzo-ullman-model, take-grant-model, rice-theorem, undecidability, many-one-reducibility, access-control-matrix, pspace, np-complete]
sources:
  - paper: doi:10.1145/360303.360333
    title: "Michael A. Harrison, Walter L. Ruzzo and Jeffrey D. Ullman, Protection in operating systems, Communications of the ACM 19(8), 1976, pages 461 to 471"
    locator: "Section 4 (the definition of safety, Theorem 1 and its NP-completeness), Section 5 (Theorem 2, the simulation of a Turing machine, Figures 3 and 4, and Theorem 3)"
  - paper: doi:10.1109/TDSC.2012.77
    title: "Mahesh V. Tripunitara and Ninghui Li, The foundational work of Harrison-Ruzzo-Ullman revisited, IEEE Transactions on Dependable and Secure Computing 10(1), 2013, pages 28 to 39"
    locator: the error in the NP membership proof for mono-operational systems, the corrected proof, and the new reduction for the second version of safety
  - paper: "Michael A. Harrison and Walter L. Ruzzo, Monotonic protection systems, in R. A. DeMillo, D. P. Dobkin, A. K. Jones and R. J. Lipton (editors), Foundations of Secure Computation, Academic Press, 1978"
    locator: undecidability for monotonic biconditional systems and decidability for monotonic monoconditional systems
  - book: isbn:9780321712332
    title: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018"
    locator: "Chapter 3, Foundational Results"
---

The safety theorem of Harrison, Ruzzo and Ullman (1976) says that no algorithm can decide, for every protection system of the [HRU model](/harrison-ruzzo-ullman-model/), whether a given right can ever be entered into a cell of the access matrix that did not hold it. The proof builds, for each [Turing machine](/turing-machine/), a protection system whose commands do the moves of the machine, so a decision procedure for safety would solve the [halting problem](/halting-problem/). The same paper shows that the question becomes decidable, and NP-complete, when each command has only one primitive operation. The theorem is about the class of all HRU systems: one particular system can still have a decidable safety question, as the [Take-Grant model](/take-grant-model/) does.

## Statement

The definitions are those of the [HRU model](/harrison-ruzzo-ullman-model/). A protection system is a finite set $R$ of generic rights and a finite set $C$ of commands. A configuration $Q_0 = (S_0, O_0, A_0)$ is *unsafe for $r$* if some sequence of command calls reaches a configuration $Q$ from which some call leaks $r$, that is, enters $r$ into a cell that did not hold $r$. This is the first version of safety in the paper, where the leak may go to any cell.

**Problem SAFETY.** The input is a finite description of a protection system $(R, C)$, a configuration $Q_0$ and a right $r \in R$. The question is: is $Q_0$ safe for $r$? Decidability is in the [Turing machine](/turing-machine/) model.

**Theorem** (HRU 1976, Theorem 2). SAFETY is undecidable. The set of unsafe instances is recursively enumerable, so the set of safe instances is not recursively enumerable.

**Companion results** in the same paper:

- (Theorem 1) If every command is mono-operational, that is, its body has exactly one primitive operation, SAFETY is decidable. With the commands as part of the input, it is NP-complete. Tripunitara and Li (2013) corrected the proof of membership in NP.
- (Theorem 3) If no command creates a subject or an object, SAFETY is [PSPACE](/pspace/)-complete.

## In plain words

An operating system keeps a table of who may do what to which file. Programs change the table with a fixed list of simple commands. Each command checks some entries and then adds or removes rights, or makes or removes users and files. The safety question asks whether a right, such as read on a secret file, can ever end up somewhere new. You might hope that a tool could answer this for any list of commands. The theorem says no tool can. The reason is that such a table, with the right commands, can act as a general computer: each user is a cell of memory and each command is one step of a program. So asking whether a right leaks is the same as asking whether a program ever stops, and that question has no general answer.

## Proof

The proof reduces the halting problem to unsafety. It is the construction of HRU, Section 5.

**The machine.** Let $M$ have states $K$, tape symbols $\Gamma$ with blank $B$, start state $q_0$, a final state $q_f \ne q_0$ and a partial transition function $\delta : K \times \Gamma \to K \times \Gamma \times \{L, R\}$. The tape has a left end and is infinite to the right. We may assume three things, by the usual small changes to $M$: $M$ never moves left from cell 1, $\delta(q_f, X)$ is undefined for all $X$, and $M$ halts on the empty tape if and only if it enters $q_f$. Whether a given $M$ started on the empty tape enters $q_f$ is undecidable; this is the [halting problem](/halting-problem/) on the empty tape.

**The rights.** Let $R = K \cup \Gamma \cup \{own, end\}$, with the three parts disjoint.

**The encoding.** A configuration of $M$ with tape $X_1 X_2 \cdots X_k$ (the used cells), head on cell $j$ and state $q$ is encoded by subjects $s_1, \ldots, s_k$ and no other objects, with

- $X_i \in A[s_i, s_i]$ for each $i$, and $q \in A[s_j, s_j]$;
- $own \in A[s_i, s_{i+1}]$ for $1 \le i < k$, and $end \in A[s_k, s_k]$;
- no other rights in any cell.

**The commands.** For each pair with $\delta(q, X) = (p, Y, L)$:

$$C_{qX}(s, s'):\ \textbf{if } own \in A[s, s'] \textbf{ and } q \in A[s', s'] \textbf{ and } X \in A[s', s'] \textbf{ then } \text{delete } q, X \text{ from } A[s', s'];\ \text{enter } p \text{ into } A[s, s];\ \text{enter } Y \text{ into } A[s', s'].$$

For each pair with $\delta(q, X) = (p, Y, R)$, two commands. The first moves right inside the used part of the tape, and the second moves past the last used cell:

$$C_{qX}(s, s'):\ \textbf{if } own \in A[s, s'] \textbf{ and } q \in A[s, s] \textbf{ and } X \in A[s, s] \textbf{ then } \text{delete } q, X \text{ from } A[s, s];\ \text{enter } Y \text{ into } A[s, s];\ \text{enter } p \text{ into } A[s', s'].$$

$$D_{qX}(s, s'):\ \textbf{if } end \in A[s, s] \textbf{ and } q \in A[s, s] \textbf{ and } X \in A[s, s] \textbf{ then } \text{delete } q, X \text{ from } A[s, s];\ \text{enter } Y \text{ into } A[s, s];\ \text{create subject } s';\ \text{enter } B, p, end \text{ into } A[s', s'];\ \text{delete } end \text{ from } A[s, s];\ \text{enter } own \text{ into } A[s, s'].$$

The initial configuration $Q_0$ has one subject $s_1$ with $A[s_1, s_1] = \{q_0, B, end\}$. It encodes the start of $M$ on the empty tape. The right to ask about is $q_f$.

**Claim.** Every configuration reachable from $Q_0$ encodes a configuration of $M$ reachable from the start, up to the names of the subjects. A call changes the encoded configuration $c$ only if it does one move of $M$ from $c$.

*Proof of the claim*, by induction on the number of steps. $Q_0$ encodes the start. Let $Q$ encode $c$, with tape $X_1 \cdots X_k$, head on $j$ and state $q$. A call whose condition fails leaves $Q$ unchanged. Consider a call whose condition holds.

- $C_{q'X'}(s, s')$ for a left move needs $own \in A[s, s']$, so $s = s_i$ and $s' = s_{i+1}$ for some $i$. It needs $q', X' \in A[s_{i+1}, s_{i+1}]$, so $i + 1 = j$, $q' = q$ and $X' = X_j$, because only one state right and one symbol are present. Its body moves the state right to $s_{j-1}$ and replaces $X_j$ by $Y$. This is the left move of $M$. Since $j \ge 2$ here, the case $j = 1$ cannot arise, which matches the assumption that $M$ never moves left from cell 1.
- $C_{q'X'}(s, s')$ for a right move needs $own \in A[s, s']$ and $q', X' \in A[s, s]$, so $s = s_j$ with $j < k$, $s' = s_{j+1}$, $q' = q$ and $X' = X_j$. Its body is the right move of $M$.
- $D_{q'X'}(s, s')$ needs $end \in A[s, s]$, so $s = s_k$, and $q', X' \in A[s_k, s_k]$, so $j = k$, $q' = q$ and $X' = X_k$. The step is defined only if $s'$ is a new name, since "create subject $s'$" is defined only then. Its body writes $Y$ on cell $k$, adds a cell $k + 1$ holding $B$ with the head and state $p$ on it, and moves $end$ and the $own$ chain to the new cell. This is the right move of $M$ off the used part of the tape. Two choices of the new name give configurations that differ only in that name.

In each case the result encodes the next configuration of $M$, which proves the claim. Since $\delta$ is a function, from each reachable configuration at most one command, with at most one choice of existing parameters, changes the state.

**Leaks of $q_f$.** By the claim, a call that enters a right into a cell from a reachable configuration is one of the commands above, doing one move of $M$. The only enters of a state right are "enter $p$", where $p$ is the new state of the move. The right $q_f$ is not in any cell of an encoding until $M$ enters $q_f$, and $q_f \ne q_0$. So some reachable configuration leaks $q_f$ if and only if $M$, started on the empty tape, makes a move into $q_f$. By the assumption on $M$, this holds if and only if $M$ halts.

So $M \mapsto (R, C, Q_0, q_f)$ is a computable map from machines to instances, and $M$ halts on the empty tape if and only if $Q_0$ is unsafe for $q_f$. It is a [many-one reduction](/many-one-reducibility/) from the halting problem to unsafety. If SAFETY were decidable, so would be unsafety, and so the halting problem. Hence SAFETY is undecidable.

**Unsafety is recursively enumerable.** Enumerate the finite sequences of calls. At each step there are finitely many commands, and each parameter is an existing object or a new name; up to renaming of new names, there are finitely many choices. Run each sequence and check whether some call enters $r$ into a cell without $r$. If $Q_0$ is unsafe, this search stops. A set and its complement that are both recursively enumerable are decidable, so the safe instances are not recursively enumerable. $\blacksquare$

**Example of one move.** Take the tape $WXYZ$ with the head on cell 2 in state $q$, as in Figure 3 of the paper. The matrix has $A[s_1, s_1] = \{W\}$, $A[s_2, s_2] = \{X, q\}$, $A[s_3, s_3] = \{Y\}$, $A[s_4, s_4] = \{Z, end\}$ and $own$ in $A[s_1, s_2]$, $A[s_2, s_3]$ and $A[s_3, s_4]$. If $\delta(q, X) = (p, V, L)$, only the call $C_{qX}(s_1, s_2)$ has a true condition and changes the matrix. After it, $A[s_1, s_1] = \{W, p\}$ and $A[s_2, s_2] = \{V\}$: the tape is $WVYZ$ with the head on cell 1 in state $p$.

## Consequences

- **No general analysis tool.** A tool that checks arbitrary access control configurations for leaks must give up exactness: it can work on a restricted class, bound the search, or answer "unknown". This is why later models restrict the commands, as [Take-Grant](/take-grant-model/) does, or fix the rules, as [Bell-LaPadula](/bell-lapadula-model/) does.
- **One fixed system.** HRU strengthen the theorem with a universal Turing machine: there is one protection system, fixed once, for which safety is undecidable as a function of the initial configuration. So the hardness is not only in the choice of commands.
- **Relation to Rice's theorem.** The proof has the same shape as the proof of [Rice's theorem](/rice-theorem/): a semantic question about all runs of a system is reduced to halting. It is not an instance of Rice's theorem, because safety is a property of a protection system and a configuration, not of the language of a Turing machine.
- **The second version.** If the question is whether $r$ can reach one given cell, the problem is also undecidable. The map from this version to the first in the HRU paper is not a reduction; Tripunitara and Li (2013) gave a correct one.

## Tightness

The theorem cannot be extended to every restricted class, and the borders are known for several classes. All items are theorems.

- **One operation per command.** For mono-operational systems, safety is decidable: a shortest leaking sequence has at most $g(|S_0| + 1)(|O_0| + 1) + 1$ calls, where $g = |R|$. With the commands in the input, the problem is NP-complete; hardness is by a reduction from the [clique problem](/clique-problem/). The proof of membership in NP in the 1976 paper assumed that these systems are monotonic for safety, which is false; Tripunitara and Li (2013) gave a corrected proof.
- **No creates.** Without create operations, the set of configurations is finite, and safety is PSPACE-complete (HRU, Theorem 3).
- **Monotonic systems.** Removing delete and destroy is not enough. Harrison and Ruzzo (1978) showed that safety stays undecidable for monotonic systems, even when each condition has at most two tests. With at most one test per condition and no delete or destroy, safety is decidable.
- **The proof needs create.** The commands $D_{qX}$ create a subject for each new tape cell. This is necessary for undecidability, because without creates the problem is in PSPACE.

## History

Harrison, Ruzzo and Ullman presented the model and the theorem at a conference in 1975 and in Communications of the ACM in 1976. The paper gave the first precise statement of the safety question for an access matrix with commands, and it gave the undecidable case, the decidable mono-operational case and the PSPACE-complete case without creates. Harrison and Ruzzo studied monotonic systems in 1978. In 2013 Tripunitara and Li reexamined the paper, found the error in the NP membership proof and in the map between the two versions of safety, and repaired both.

## References
