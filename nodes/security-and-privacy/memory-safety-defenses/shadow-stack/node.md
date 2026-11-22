---
tag: 5QQA10
kind: data-structure
slug: shadow-stack
name: Shadow stack
aliases:
- return address stack protection
area: security-and-privacy/memory-safety-defenses
level: core
summary: A protected second stack that keeps a copy of each return address and is compared with the normal stack on return.
model: word-ram
complexity:
  vars: {n: the number of calls and returns in a run, h: the largest number of pending calls}
  time: {worst: Θ(1)}
  space: {extra: Θ(h)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2005
  people: [Martin Abadi, Mihai Budiu, Ulfar Erlingsson, Jay Ligatti]
  note: Abadi et al. paired control-flow integrity with a protected shadow call stack in 2005. Intel CET put a shadow stack in hardware, with processors from 2020.
prereqs: [stack, stack-smashing]
see_also: [control-flow-integrity, stack-canary, control-flow-bending, return-oriented-programming, code-pointer-integrity, balanced-parentheses, activation-record, software-fault-isolation]
sources:
  - paper: doi:10.1109/SP.2019.00076
    title: Nathan Burow, Xinping Zhang and Mathias Payer, SoK, shining light on shadow stacks, 2019 IEEE Symposium on Security and Privacy, pages 985-999
    locator: the design space of shadow stacks (compact and parallel layouts, protection of the shadow region, the comparison policy) and their evaluation of performance, compatibility and security
  - paper: doi:10.1145/1609956.1609960
    title: Martin Abadi, Mihai Budiu, Ulfar Erlingsson and Jay Ligatti, Control-flow integrity, principles, implementations, and applications, ACM Transactions on Information and System Security 13(1), article 4, 2009
    locator: the section on a protected shadow call stack built on CFI, and its measured cost on SPEC benchmarks
  - paper: doi:10.1145/2714576.2714635
    title: Thurston H. Y. Dang, Petros Maniatis and David Wagner, The performance cost of shadow stacks and stack canaries, ASIA CCS 2015, pages 555-566
    locator: the traditional and the parallel shadow stack, and their measured overheads
  - paper: "Nicholas Carlini, Antonio Barresi, Mathias Payer, David Wagner and Thomas R. Gross, Control-flow bending, on the effectiveness of control-flow integrity, 24th USENIX Security Symposium, 2015, pages 161-176"
    locator: the results with and without a shadow stack on six programs
  - url: "https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html"
    title: Intel 64 and IA-32 Architectures Software Developer's Manual, Volume 1
    locator: the chapter on Control-flow Enforcement Technology (shadow stack pages, the shadow stack pointer and the control protection fault)
---

A shadow stack is a second stack, kept in memory that the program's normal stores cannot change, that holds a copy of every return address. At each call the return address goes on both the normal stack and the shadow stack. At each return the address read from the normal stack is compared with the top of the shadow stack, and a mismatch stops the program. If the shadow stack is truly protected, every return goes back to the call site that made the matching call, which is the most precise policy for returns there is. A buffer overflow that changes a saved return address, as in [stack smashing](/stack-smashing/), is then caught at the return, whatever the bytes of the overflow are. The shadow stack protects only returns, the backward edges of the control flow; [control-flow integrity](/control-flow-integrity/) checks the forward edges, and [control-flow bending](/control-flow-bending/) shows why a strong CFI needs both. This page gives the structure on an abstract trace of calls and returns, with labels in place of addresses.

## In plain words

When a function calls another, it leaves a note on the stack that says where to come back to. A bug that writes past the end of a local array can change that note. Then the function "returns" to a place that the program never meant to go.

A shadow stack keeps a second copy of each note, in a place that the bug cannot reach. When a function returns, the program reads the note on the normal stack and compares it with the copy. If they agree, the return goes ahead. If they differ, something changed the note, and the program stops.

The copy follows the same last-in, first-out rule as the calls themselves: the most recent call is the first to return. So a plain [stack](/stack/) of copies is all that is needed.

## The abstract type

A shadow stack is a [stack](/stack/) of return addresses with a check built into the pop. It has these operations:

- PUSH$(S, a)$, run at each call, saves the return address $a$.
- CHECK-RETURN$(S, r)$, run at each return, pops the top entry and compares it with the value $r$ that the return is about to use. It returns $r$ if they are equal, and raises a fault if not.
- RESTORE$(S, d)$, run at a non-local exit such as `longjmp` or the unwinding of an exception, drops the entries above depth $d$.

A capacity bound makes PUSH fault when the shadow stack is full. The structure has no operation that writes an entry other than the top one, and that is the point: the program has no way to change a saved address.

## Representation

The state is an array $S[0 \ldots c-1]$ of $c$ entries and an index $t$, the number of saved addresses. Both live in a region that ordinary stores of the program cannot write.

**Invariant (I).** Let the *intended stack* $P$ be the list of return addresses of the pending calls, oldest first, that the calls, returns and non-local exits of the run define. Then $t = |P|$ and $S[i] = P[i]$ for each $i < t$.

The normal stack of the program also holds these return addresses, inside its [activation records](/activation-record/), but a memory error can change them there. The invariant says that the shadow stack holds the values that the normal stack would hold if no memory error had happened.

## Operations

```pseudo id=main
CREATE(c)
L1  S ← an array of c entries in protected memory; t ← 0

PUSH(S, a)                                     ▷ at each call; a is the return address
L2  if t = c then fault "shadow stack full"
L3  S[t] ← a
L4  t ← t + 1

CHECK-RETURN(S, r)                             ▷ at each return; r is read from the normal stack
L5  if t = 0 then fault "shadow stack empty"
L6  t ← t - 1
L7  if S[t] ≠ r then fault "return address mismatch"
L8  return r

RESTORE(S, d)                                  ▷ at a non-local exit to a frame saved at depth d
L9  if d > t then fault "bad restore"
L10 t ← d
```

**Push.** Lines L2 to L4 append the return address. The call itself pushes the same value on the normal stack, so after the call both stacks agree on the top entry.

**Check on return.** Line L6 pops the saved copy and line L7 compares it with the value that the return instruction read from the normal stack. The comparison is on the value only, so a write that puts back the same value is not a fault, and a write that changes the value is caught however it was made: a linear overflow, a write through a stray pointer, or a format string error.

**Restore.** A `setjmp` saves the depth $t$ beside its normal state, and the matching `longjmp` calls RESTORE with that depth. Line L9 rejects a depth above the current one, which would make old entries valid again.

Each operation runs a fixed number of steps, so it costs $O(1)$.

## Example

Take a run where `main` calls `f` with return label r1, `f` calls `g` with label r2, `g` returns, `f` calls `h` with label r3, and then a memory error in `h` overwrites the saved return address of `h` with the label x. Steps are numbered from 1; the code numbers them from 0.

| step | event | normal stack | shadow stack | result |
|---|---|---|---|---|
| 1 | call, return label r1 | r1 | r1 | |
| 2 | call, return label r2 | r1 r2 | r1 r2 | |
| 3 | return | r1 | r1 | reads r2, top copy r2, returns to r2 |
| 4 | call, return label r3 | r1 r3 | r1 r3 | |
| 5 | memory error writes x at the top entry | r1 x | r1 r3 | the shadow stack is not touched |
| 6 | return | r1 | r1 | reads x, top copy r3, fault "return address mismatch" |

The run stops at step 6, before control reaches x. Without the write at step 5, step 6 returns to r3 and the last return goes to r1.

A non-local exit: `main` calls `f` with label r1, `f` runs `setjmp` at depth 1, then calls `g` with r2, and `g` calls `k` with r3. A `longjmp` back to `f` cuts both stacks to depth 1, and the next return of `f` reads r1 from both. Without RESTORE, the shadow stack would still hold r1 r2 r3, and that return would compare r1 with r3 and fault by mistake.

## Correctness

The invariant (I) holds after each event of the run, under three assumptions: only lines L1 to L10 change $S$ and $t$; the instrumentation runs at every call, return and non-local exit; and the capacity is large enough. A memory error changes the normal stack but not the shadow stack, so it leaves (I) intact. By (I), line L7 compares the value that the return read with the return address of the matching call. So CHECK-RETURN faults exactly when the return would go somewhere other than the call site that made the matching call, and it never faults on a run where no saved return address was changed. The full proof, by induction over the events, is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | memory accesses |
|---|---|---|
| create | $O(1)$, or $\Theta(c)$ to clear the array | none |
| push | $O(1)$ | 1 write to the shadow region |
| check on return | $O(1)$ | 1 read of the shadow region |
| restore | $O(1)$ | none |
| space | $c$ entries, at least $h$ | |

Here $h$ is the largest number of pending calls in a run, and a run of $n$ calls and returns costs $O(n)$ extra steps. The model is the [word RAM](/word-ram/), with one return address per word.

These are counts in the model. The real cost of a software shadow stack comes from the extra memory traffic on every call and return, and it is a measurement. Dang, Maniatis and Wagner (2015) measured roughly 10 percent for a traditional shadow stack with its own stack pointer on x86, and about 3.5 percent for a *parallel* shadow stack placed at a fixed offset from the normal stack. Abadi et al. measured an average of 21 percent on their SPEC benchmarks for CFI together with a protected shadow call stack (TISSEC 2009 version). With hardware support, as in Intel CET, the push and the compare are part of the call and return instructions.

## Variants

- **Compact and parallel layouts.** A compact shadow stack has its own stack pointer, which must itself be protected, for example in a reserved register; Clang's ShadowCallStack on AArch64 keeps it in register x18. A parallel shadow stack sits at a fixed offset from the normal stack and needs no second pointer, at the cost of as much memory as the normal stack. Burow, Zhang and Payer (2019) compare the layouts.
- **Protection of the region.** The guarantee rests on the region being unwritable by the program. Hardware gives the strongest form: Intel CET marks shadow stack pages with a special page type that ordinary stores cannot write, and raises a control protection fault on a mismatch. Software can use segmentation, [software fault isolation](/software-fault-isolation/) or memory protection keys. Hiding the region at a random address is the weakest form, because any leak of the address breaks it.
- **The policy on a mismatch.** Stop the program (the usual choice), or return to the saved copy instead of the value on the normal stack. The second keeps the program running but hides the bug.
- **Unwinding by search.** Some designs, instead of RESTORE, pop entries on a mismatch until one matches the target, to support `longjmp` and exceptions without changes to the library. This is weaker: it accepts a return to any pending call site, not only the top one.
- **Return address encryption.** Arm pointer authentication signs the return address with a key and the stack pointer, and checks the signature on return. It is not a shadow stack: a signed value can be reused at another point where the stack pointer has the same value.

## When to use it

Use a shadow stack when returns must go back exactly where they came from, with no secret that can leak and no false alarms on correct code. It is the natural complement of forward-edge [control-flow integrity](/control-flow-integrity/): Carlini et al. (2015) found that fully precise static CFI without a shadow stack still allowed strong attacks in five of six programs, and that adding a shadow stack stopped arbitrary code execution in three of the six. A [stack canary](/stack-canary/) is cheaper in software and needs no extra memory, but it detects only overflows that pass through the canary, and only while the canary value stays secret. A shadow stack does not stop attacks that change data and leave returns alone; see [data-oriented programming](/data-oriented-programming/) and [code-pointer integrity](/code-pointer-integrity/).

## Pitfalls

- **An unprotected region.** If the program can write $S$ or $t$, an attacker who can change a return address can change its copy too, and line L7 passes. The protection of the region is the whole guarantee.
- **Missing RESTORE on non-local exits.** Code that leaves frames without returning, such as `longjmp`, exception unwinding, coroutines and user-level thread switches, must call RESTORE (or switch to another shadow stack). Without it, line L7 raises false alarms on correct programs, and the usual reaction is to turn the defense off.
- **Instrumentation gaps.** A library compiled without the instrumentation pushes nothing at its calls and checks nothing at its returns. Mixed code must be handled at the boundary, or the check in line L7 compares the wrong entries.
- **Tail calls and unusual returns.** A [tail call](/tail-call-optimization/) replaces a return by a jump, and some code uses a return instruction to jump to a computed address. Both change the pairing of calls and returns that invariant (I) needs.
- **Treating it as full CFI.** The shadow stack says nothing about indirect calls and jumps, or about non-control data.

## Implementations

The Python class follows the main block on an abstract trace. A return address is a label such as "r1", and a modeled memory error writes a label into the normal stack, which is a Python list; the shadow stack is a separate object that the write cannot reach. The tests check the class against a list on random operations, and check the trace runner against the call and return matching computed by a backward scan, on random traces with writes and non-local exits.

## History

Software return address stacks appeared around 2000, for example in StackShield and in the return address repository of Chiueh and Hsu (ICDCS 2001). Abadi, Budiu, Erlingsson and Ligatti built a protected shadow call stack on top of control-flow integrity in 2005, and used CFI to make the region unwritable. Dang, Maniatis and Wagner (2015) measured why software shadow stacks were rarely deployed, and proposed the parallel layout. Intel published the Control-flow Enforcement Technology specification, with a hardware shadow stack and indirect branch tracking, and processors with it shipped from 2020. Burow, Zhang and Payer (2019) surveyed the design space and released implementations of the known schemes in LLVM.

## References
