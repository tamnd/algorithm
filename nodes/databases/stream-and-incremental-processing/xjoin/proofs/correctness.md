---
title: XJoin emits every result pair exactly once, within its memory limit
proves: [correctness, termination, space.extra]
status: full
---

We use the line numbers of the pseudocode on the page. The inputs are $R$ and $S$ with the set $J$ of common attributes, under bag semantics: every arrival is a separate occurrence. A *pair* is $(a, b)$ with $a$ an occurrence of $R$, $b$ an occurrence of $S$, $a[J] = b[J]$, and no NULL in the key. The join $R \bowtie S$ has one result for each pair. A tuple with a NULL key is dropped at line L5 and is in no pair, so we only consider the other tuples. Two tuples with the same key are in the same partition $p = h(a[J])$, so all statements below are about one partition $p$.

**Clock.** Line L3 advances the clock once for each event, and a move to disk at line L7 advances it once more before it sets the departure times. So the arrival time $\mathrm{ATS}$ of each tuple, the time of each move to disk and the time $pt$ of each stage 2 run are distinct integers, and the clock only grows. A tuple has $\mathrm{DTS} = \infty$ until its part moves to disk; then $\mathrm{DTS}$ is the time of the move. Every tuple satisfies $\mathrm{ATS} < \mathrm{DTS}$.

**Lemma 1 (place of a tuple).** At a clock time $c$ that is not the arrival time of $x$, a tuple $x$ that has arrived is in memory if and only if $x.\mathrm{ATS} < c < x.\mathrm{DTS}$, and on disk if and only if $x.\mathrm{DTS} < c$. No tuple goes back from disk to memory.

*Proof.* Line L5 puts $x$ into memory at time $x.\mathrm{ATS}$. Only line L7 moves tuples, always from memory to disk, and it sets $\mathrm{DTS}$ to the time of the move. Stages 2 and 3 read the disk parts but do not move them back. $\square$

We say that a pair is *met in stage 1* if one of its tuples finds the other in memory at line L6, and *met at $pt$* if the stage 2 run at time $pt$ examines it at line L10, so that one of its tuples is in the chosen disk part and the other is in the memory part of the other input.

**Lemma 2 (stage 1).** A pair $(a, b)$ is met in stage 1 if and only if $a.\mathrm{ATS} < b.\mathrm{DTS}$ and $b.\mathrm{ATS} < a.\mathrm{DTS}$, the test of line L15. If it is met, it is met once, at the arrival of the later tuple.

*Proof.* Line L6 runs only at an arrival and probes only the other input, so the pair can be met only at the arrival of its later tuple, say $b$, with $a.\mathrm{ATS} < b.\mathrm{ATS}$. It is met if and only if $a$ is in memory at that moment, which by Lemma 1 means $b.\mathrm{ATS} < a.\mathrm{DTS}$. The other inequality, $a.\mathrm{ATS} < b.\mathrm{ATS} < b.\mathrm{DTS}$, then holds anyway. If $a$ arrives later, exchange the roles. $\square$

**Lemma 3 (stage 2).** Let the stage 2 run at time $pt$ use the disk part of input $X$ in partition $p$, and let $Y$ be the other input. A pair with $x$ from $X$ and $y$ from $Y$ is met at $pt$ if and only if $x.\mathrm{DTS} < pt$ and $y.\mathrm{ATS} < pt < y.\mathrm{DTS}$. This is the test of lines L16 and L17 for the entry $pt$ of the history of $(X, p)$.

*Proof.* Line L10 pairs exactly the tuples on disk in $(X, p)$ with the tuples in memory in $(Y, p)$ at time $pt$. Apply Lemma 1 with $c = pt$, which is not an arrival time. $\square$

**Lemma 4 (the tests are stable).** Once both tuples of a pair have arrived, the value of the stage 1 test never changes. For an entry $pt$ of a history, the value of its stage 2 test never changes after time $pt$.

*Proof.* The tests read only $\mathrm{ATS}$, which is fixed at arrival, and $\mathrm{DTS}$, which changes once, from $\infty$ to the time $d$ of a move. In the stage 1 test, if $a.\mathrm{DTS} = \infty$ when $b$ arrives, the later value $d$ is larger than the current clock, so $b.\mathrm{ATS} < d$ still holds. In the stage 2 test, if $y.\mathrm{DTS} = \infty$ at time $pt$, a later move gives $y.\mathrm{DTS} > pt$ again. A finite $\mathrm{DTS}$ never changes. $\square$

**Lemma 5 (DONE).** When DONE$(a, b)$ is called at time $c$, it returns true if and only if the pair was met in stage 1 or at some $pt < c$.

*Proof.* The history of $(X, p)$ holds the times of the earlier stage 2 runs on that part, because line L12 appends $pt$ after the run at $pt$ ends. By Lemmas 2, 3 and 4, the tests of lines L15 to L17 evaluated at time $c$ have the same values that they had when each meeting could happen. $\square$

**Theorem 1 (exactly once).** At the end of stage 3, every pair has been emitted exactly once, and nothing else has been emitted. So the output is $R \bowtie S$ as a bag.

*Proof.* Every emission is of a pair, because lines L6, L10 and L13 compare the keys. Take a pair and look at the events that meet it, in clock order.

If it is met in stage 1, this is its first meeting: before the arrival of its later tuple, the pair cannot be met at all. Line L6 emits it without a test. Each later stage 2 run that meets it calls DONE, which returns true by Lemma 5, so line L11 does not emit it again, and stage 3 skips it for the same reason.

If it is not met in stage 1 but is met in stage 2, let $pt_0$ be the first run that meets it. At $pt_0$, DONE returns false by Lemma 5, so line L11 emits it. Every later run and stage 3 call DONE after $pt_0$, which returns true.

If it is never met before stage 3, DONE returns false in stage 3, and line L14 emits it. Line L13 examines it, because it pairs all tuples of $R$ and $S$ in partition $p$, in memory or on disk. Stage 3 examines each pair once.

In all three cases the pair is emitted exactly once. $\blacksquare$

**Corollary 1 (safe early output).** After each event, the bag of tuples emitted so far is a sub-bag of $R_j \bowtie S_j$, the join of the inputs that have arrived.

*Proof.* Every emitted tuple comes from a pair of arrived tuples, and by Theorem 1 no pair is emitted twice. $\square$

**Theorem 2 (memory).** After each event, memory holds at most $M$ tuples.

*Proof.* Only line L5 adds a tuple to memory, one per event. If memory then holds $M + 1$ tuples, line L7 moves the largest memory part to disk. That part holds at least one tuple, because memory is not empty, so at most $M$ tuples remain. $\blacksquare$

**Termination.** Every event does a finite amount of work, and stage 3 pairs finitely many tuples. The history of a part grows by one entry per stage 2 run, so each call of DONE is finite.

**What the heuristics change.** The choice of the part to move at line L7 and of the part to use at line L9 does not occur in any proof above. A different choice changes when each result appears and how many disk reads are needed, but not the final output.
