---
title: Copy propagation keeps the outcome of every run
proves: [correctness]
status: full
---

**Setting.** $P$ is a program of the toy IR with no phi-functions. A *point* is a position just before an instruction or a terminator of a block. A *state* is the environment of the running frame, the memory (the heap and the variables of all frames), and the position. We assume, as for the test programs of the toy IR, that no run of $P$ reads a name before it is defined. $T$ is the set of address-taken names, the names $x$ of the instructions `p = &x`. A pair $(x, y)$ stands for the copy `x = y`, with $y$ a name other than $x$. We say that a pair $(x, y)$ *holds* in a state when $x$ and $y$ are both defined there and have the same value.

The *outcome* of a run is its return value, a trap, or no end. The theorem is: $P$ and the program that COPY-PROPAGATION returns have the same outcome on every input. It follows from three lemmas, one for the analysis, one for the rewrite of one round, and one for the removal of dead copies, because the algorithm is a sequence of rounds and one removal.

## Lemma 1: the transfer function is sound

**Claim.** Let $I$ be an instruction, $S$ a set of pairs, and $\sigma$ a state in which every pair of $S$ holds. If $I$ runs from $\sigma$ without a trap and reaches the state $\sigma'$, then every pair of $\mathrm{TRANSFER}(I, S)$ holds in $\sigma'$.

**Proof.** Take a pair $(x, y)$ of the result. Either it was in $S$ and survived lines L19 and L20, or line L21 added it.

- *It survived.* Then $x$ and $y$ held the same value in $\sigma$. The instruction writes its destination $d$, if it has one, and line L20 removed every pair that mentions $d$, so $d \ne x$ and $d \ne y$. A store writes one memory cell. In the toy IR a pointer is made by `alloc`, which gives a heap cell, or by `p = &z`, which gives the variable $z$ of the frame that ran it, with $z \in T$. So a store changes no name outside $T$. A call runs its function in a new frame, and that function changes the names of our frame only through pointers, which again point to names in $T$ or to heap cells. Line L19 removed the pairs that mention a name of $T$ when $I$ is a store or a call, so $x, y \notin T$ in that case. In each case $I$ changes neither $x$ nor $y$, and the pair still holds in $\sigma'$.
- *Line L21 added it.* Then $I$ is `x = y`. The run read $y$, so $y$ is defined, and $I$ wrote that value to $x$. The pair holds in $\sigma'$. $\square$

## Lemma 2: the available copies hold

**The fixed point.** The sets OUT start at the full set $C$ of the copies in $P$. TRANSFER only adds pairs of $C$, and it is monotone: $S_1 \subseteq S_2$ gives $\mathrm{TRANSFER}(I, S_1) \subseteq \mathrm{TRANSFER}(I, S_2)$, because removing the pairs that mention a name and adding one fixed pair both keep inclusion. Intersection is monotone too. By induction on the visits, every new value of OUT[B] is a subset of the one before, so the sets only shrink, and since $C$ is finite the loop of line L16 stops. In the last pass no OUT changes, so every IN in that pass was computed from the final OUT sets. So for every reachable block $B$ the final sets satisfy

$$\mathrm{IN}[B] = \emptyset \text{ if } B \text{ is the entry}, \qquad \mathrm{IN}[B] = \bigcap_{p \in \mathrm{pred}(B)} \mathrm{OUT}[p] \text{ otherwise}, \qquad \mathrm{OUT}[B] = \mathrm{TRANSFER}(B, \mathrm{IN}[B]),$$

where $\mathrm{TRANSFER}(B, \cdot)$ applies TRANSFER to the instructions of $B$ in order. A block that the entry does not reach keeps $\mathrm{IN} = \emptyset$.

For a point $q$ inside a block $B$, let $S(q)$ be the set that TRANSFER gives from IN[B] over the instructions of $B$ before $q$.

**Claim.** In every run of $P$ and at every point $q$ that the run reaches, every pair of $S(q)$ holds.

**Proof.** By induction on the number of steps of the run. At the first point the set is $\mathrm{IN}[\text{entry}] = \emptyset$, and there is nothing to show. Inside a block, a step from $q$ to the next point $q'$ runs one instruction $I$, and $S(q') = \mathrm{TRANSFER}(I, S(q))$. Lemma 1 gives the claim at $q'$. A step from the end of a block $p$ to the start of a successor $B$ goes along an edge, so $p$ is a predecessor of $B$, and both blocks are reachable. The set at the end of $p$ is $\mathrm{OUT}[p]$, and every pair of it holds by induction. If $B$ is the entry, its set is empty. Otherwise $\mathrm{IN}[B] \subseteq \mathrm{OUT}[p]$, and every pair of $\mathrm{IN}[B]$ holds. The step does not change the state. $\square$

**The sets have no cycle.** Call a set *proper* if no name is the destination of two of its pairs and the map $x \mapsto y$ of its pairs has no cycle. The empty set is proper, and a subset of a proper set is proper. TRANSFER keeps a set proper: line L21 adds $(x, y)$ only after line L20 has removed every pair $(x, \cdot)$ and every pair $(\cdot, x)$, so $x$ is the destination of one pair, and no pair leads back to $x$. Visit the reachable blocks in reverse postorder. Each block other than the entry has a predecessor that comes earlier in this order, its parent in the depth-first search. By induction its final OUT is proper, so the intersection IN[B] is proper. So every set that the rewrite uses is proper, and the loop of line L8 stops after at most as many steps as there are pairs.

## Lemma 3: one round keeps the outcome

Let $P'$ be the program after one round, lines L2 to L10. The round keeps every instruction in its place and only changes operands.

**Claim.** For every input, the runs of $P$ and $P'$ go through the same states, step for step, until both end in the same way.

**Proof.** Inside a block $B$, the round starts from $s_0 = \mathrm{IN}[B]$ and sets $s_{j+1} = \mathrm{TRANSFER}(I'_j, s_j)$, where $I'_j$ is the rewritten instruction $j$. We show by induction on the steps that both runs are in the same state, and that every pair of $s_j$ holds in that state when the runs are before instruction $j$.

At the start of a block both runs are in the same state, which is a state of a run of $P$. By Lemma 2 every pair of $\mathrm{IN}[B]$ holds. Before instruction $j$, every operand $u$ that line L8 replaces is followed along pairs $(u, u_1), (u_1, u_2), \ldots, (u_{k-1}, y)$ of $s_j$. Each of them holds, so $u$ and $y$ have the same value. So $I'_j$ reads the same operand values as $I_j$. It does the same thing: it writes the same value to the same destination, stores the same value to the same cell, calls the same function with the same arguments, or traps on the same zero divisor or bad shift count. A terminator with a replaced operand takes the same branch or returns the same value. So the two states after the step are equal. By Lemma 1, applied to the run of $P'$ that executes $I'_j$, every pair of $s_{j+1}$ holds after it.

So the runs never differ, and they have the same outcome. Also $P'$ reads only names that hold the value of a defined name, so $P'$ again reads no undefined name, and the next round may use the same lemmas. $\square$

## Lemma 4: removing dead copies keeps the outcome

One pass of line L12 deletes some instructions `x = y` from a program $Q$ and gives $Q''$. A deleted copy has $x \notin T$, and it is `x = x` or $x$ is not in the set $L$ of names live after it. The set $L$ comes from the liveness of $Q$ at the end of each block, and inside a block it is updated backward over the kept instructions only:

$$L_{\text{before}} = \mathrm{uses}(I) \cup (L_{\text{after}} \setminus \{d\}) \text{ for a kept } I \text{ that defines } d, \qquad L_{\text{before}} = L_{\text{after}} \text{ for a deleted copy}.$$

**$L$ is enough at the block ends.** Let $\mathrm{live}_Q$ be the liveness of $Q$. Going backward through a block, $L(q) \subseteq \mathrm{live}_Q(q)$ at every point $q$: it holds at the end, where both sets are equal, a kept instruction applies the same rule to both sets, and a deleted `x = y`, which has $x \notin L_{\text{after}}$ or $y = x$, gives $L_{\text{before}} = L_{\text{after}} \subseteq (\mathrm{live}_Q \setminus \{x\}) \cup \{y\}$. So for every edge from $b$ to $s$, $L(\text{start of } s) \subseteq \mathrm{live}_Q(\text{start of } s) \subseteq \mathrm{live}_Q(\text{end of } b) = L(\text{end of } b)$.

**Claim.** Run $Q$ and $Q''$ on the same input, and match the points of $Q''$ with the points of $Q$, skipping the deleted copies. At matched points the memory is the same, the call stack is the same, and the environments agree on every name of $L(q) \cup T$.

**Proof.** At the start the two environments are equal. A deleted copy runs in $Q$ only. It cannot trap, because $y$ is defined. A deleted `x = x` changes nothing. Any other deleted copy changes only $x$, which is neither in $L_{\text{after}} = L_{\text{before}}$ nor in $T$. In both cases the claim still holds after it. A kept instruction reads names of $L_{\text{before}}$, which agree, so in both programs it traps in the same way or writes the same value to the same name or cell. After it the names of $L_{\text{after}} \setminus \{d\}$ agree, because they were in $L_{\text{before}}$ and did not change, and $d$ got the same value in both. The names of $T$ and the memory change in the same way in both, also inside a called function, which is not changed and gets the same arguments and the same memory. A terminator reads names of $L$ at the block end, so it takes the same branch or returns the same value, and on an edge $L$ only shrinks, by the inclusion above. So the runs trap together, return the same value, or both never end. $\square$

**Line L12.** It repeats such passes until a pass deletes nothing. Each pass deletes at least one instruction or ends the loop, so there are at most $c + 1$ passes for $c$ copies, and the outcome does not change.

## The theorem

COPY-PROPAGATION runs some number of rounds, then line L12. By Lemma 3 every round keeps the outcome and keeps the property that no name is read before it is defined. By Lemma 4 line L12 keeps the outcome. So the result has the same outcome as $P$ on every input. The argument does not depend on how many rounds run, so stopping after a fixed number of rounds is also safe.

**The cost does not grow.** A round changes no instruction into a more costly one, and line L12 only deletes copies. So on every input the new program executes at most as many instructions and terminators as $P$.
