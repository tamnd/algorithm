---
title: The Herlihy-Moss machine runs committed transactions as if one at a time
proves: [correctness]
status: full
---

**Model.** There are $n$ processors and a memory `mem`. Each processor $P$ has the flags $\mathrm{TACTIVE}(P)$ and $\mathrm{TSTATUS}(P)$ and a transactional cache $\mathrm{tc}(P)$, a map from addresses to pairs (mode, value) with mode $S$ (shared) or $X$ (exclusive) and at most $C$ entries. One step is one of the instructions L1 to L28 of the page, executed atomically. The transaction of $P$ starts at the first transactional instruction after $P$ ended its previous one, and ends at a COMMIT (L16 to L19), an ABORT (L20) or a VALIDATE that returns false (L21 to L23). It *commits* if its COMMIT returns true. A LOAD or a STORE is a one-step transaction that always commits (footnote 1 of the paper). The *commit step* of a transaction is the step of its COMMIT, or the step of the LOAD or STORE.

We say that $P$ is *live* if $\mathrm{TSTATUS}(P)$ is true. Only ABORT-SELF (L24) sets TSTATUS to false, and only the end of a transaction (L18, L20, L22) sets it to true again.

**Invariant.** After every step, for all processors $P \ne Q$ and every address $a$:

1. if $P$ is not live, then $\mathrm{tc}(P)$ is empty;
2. if $a$ has mode $X$ in $\mathrm{tc}(P)$, then $a \notin \mathrm{tc}(Q)$;
3. if $a \in \mathrm{tc}(P)$ and $P$ added $a$ at step $t_a$, then no step after $t_a$ has changed $\mathrm{mem}[a]$;
4. if $a$ has mode $S$ in $\mathrm{tc}(P)$, its value is $\mathrm{mem}[a]$.

*Proof.* At the start all caches are empty. Consider one step.

- ABORT-SELF (L24), COMMIT (L18), ABORT (L20) and a false VALIDATE (L22) empty the cache of their processor. Emptying a cache keeps 2 to 4, and ABORT-SELF also keeps 1. Every other step that makes $P$ not live is an ABORT-SELF, so 1 holds.
- LT adds $a$ in mode $S$ (L7) only if no other live processor holds $a$ in mode $X$ (L4); by 1, a processor that is not live holds nothing. The value it stores is $\mathrm{mem}[a]$. This keeps 2 and 4, and 3 holds for the new entry from now on.
- LTX and ST add $a$ in mode $X$, or change $S$ to $X$ (L14), only if no other live processor holds $a$ in any mode (L11). This keeps 2. An entry that changes from $S$ to $X$ keeps its step $t_a$.
- The only steps that change `mem` are COMMIT (L17) and STORE (L26). A COMMIT of $P$ writes only addresses $a$ with mode $X$ in $\mathrm{tc}(P)$; by 2 no other cache holds $a$, so 3 and 4 hold for all other processors, and the cache of $P$ is emptied in the same step. A STORE to $a$ first runs ABORT-SELF on every other processor that holds $a$ (L25), so after the step no cache holds $a$, except possibly the cache of the storing processor, which by the precondition does not hold $a$.
- A LOAD changes no memory. It aborts the holders in mode $X$ (L27), which only empties caches.

So all four parts hold after the step. $\square$

**Lemma 1 (what a live transaction has read).** Let $T$ be a transaction of $P$ and let $s$ be a step at which $P$ is still live in $T$. For every address $a$ that $T$ has read before $s$ as a *first access* (an LT or LTX of $a$ when $a \notin \mathrm{tc}(P)$), the value returned equals $\mathrm{mem}[a]$ at step $s$.

*Proof.* $P$ is live, so it never ran ABORT-SELF since $T$ began, and no entry left its cache: entries leave only at L18, L20, L22 and L24, and the first three end $T$. The first access to $a$ returned $\mathrm{mem}[a]$ at that step $t_a$ (L7, or L14 and L15) and added $a$ to the cache. By part 3, $\mathrm{mem}[a]$ did not change between $t_a$ and $s$. $\square$

Every other read of $T$ hits its own cache (L3, L10): it returns the value of the first access, or the last value that $T$ itself wrote with ST. These are the values that a run of $T$ alone would see.

**Theorem 1 (serializability).** Order the committed transactions by their commit steps: $T_1, T_2, \ldots$. Run them one after the other, alone, from the initial memory. Then each $T_i$ reads the same values as in the real run, and after $T_i$ the memory equals `mem` in the real run just after the commit step of $T_i$. Hence the committed transactions are serializable, and the order respects real time.

*Proof.* By induction on $i$. Suppose the claim holds for $T_1, \ldots, T_{i-1}$. Between the commit steps of $T_{i-1}$ and $T_i$, no step changes `mem`, since only commit steps do. So just before the commit step $s$ of $T_i$, `mem` equals the memory of the serial run before $T_i$.

If $T_i$ is a LOAD or a STORE, it is one step and the claim is clear. Otherwise $T_i$ is a transaction of $P$ whose COMMIT returns true, so $P$ is live at $s$ (L16). By Lemma 1, each first access of $T_i$ returned $\mathrm{mem}[a]$ at $s$, which is the value the serial run gives. Every later read of $T_i$ returns a value that $T_i$ itself fixed, as it would alone. A transaction is a deterministic program of its processor, so $T_i$ alone performs the same reads and the same tentative writes. At $s$, L17 writes exactly the final tentative values of the addresses in mode $X$: the addresses that $T_i$ accessed with LTX or ST. These are the writes of $T_i$ alone, and the claim holds after $T_i$.

The commit step of a transaction lies between its first and its last instruction, so if $T$ ends before $T'$ begins, $T$ comes first in the order. $\square$

**Theorem 2 (VALIDATE).** If VALIDATE of $P$ returns true at step $s$, then all values that the current transaction of $P$ has read come from one state: the memory at step $s$, which is the state after the committed transactions before $s$, with the own writes of the transaction applied.

*Proof.* VALIDATE returns $\mathrm{TSTATUS}(P)$ (L21, L23), so $P$ is live at $s$. Apply Lemma 1 at step $s$ and Theorem 1. $\square$

Values read after an abort and before the next VALIDATE are arbitrary (L1, L5, L6, L8). Theorem 2 is the guarantee that the paper states: "All values read before a successful VALIDATE are guaranteed to be consistent."

**Theorem 3 (capacity).** A transaction that accesses more than $C$ distinct addresses never commits.

*Proof.* Entries leave the cache of a live processor only when its transaction ends. A first access to the $(C+1)$-th distinct address finds $C$ entries and aborts (L6 or L13), so TSTATUS is false until the transaction ends, and its COMMIT returns false. $\square$

**Theorem 4 (no deadlock, no livelock freedom).** No step waits, so no set of processors can block each other. There is a run of two processors in which both take infinitely many steps and none commits.

*Proof.* Every instruction finishes in one step. For the second part, let $T_0$ access $x$ then $y$ with LTX, and $T_1$ access $y$ then $x$, each followed by VALIDATE, and retried when VALIDATE is false. Run: $T_0$ takes $x$; $T_1$ takes $y$; $T_0$ asks for $y$, gets BUSY (L11) and aborts; its VALIDATE is false and it restarts and takes $x$ again, which is free since its cache was emptied; $T_1$ asks for $x$ and gets BUSY in the same way, validates, restarts and takes $y$. The state is the same as after the first two steps, so the round can repeat for ever. The test `test_requester_loses_can_livelock` replays four rounds. $\blacksquare$
