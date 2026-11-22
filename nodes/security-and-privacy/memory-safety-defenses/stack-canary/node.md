---
tag: 828D84
kind: technique
slug: stack-canary
name: Stack canary
aliases:
- stack cookie
- StackGuard
area: security-and-privacy/memory-safety-defenses
level: intro
summary: Places a secret value before the return address and checks it before the function returns, to detect a linear stack overflow.
history:
  year: 1998
  people: [Crispin Cowan, Calton Pu, Hiroaki Etoh]
  note: StackGuard (Cowan et al., 1998) introduced the canary. ProPolice added the reordering of local variables, and GCC and Microsoft compilers made the check standard.
prereqs: [stack-smashing]
see_also: [shadow-stack, buffer-overflow, data-execution-prevention, address-space-layout-randomization, memory-tagging, addresssanitizer, format-string-vulnerability, uniform-distribution]
sources:
  - paper: "Crispin Cowan, Calton Pu, Dave Maier, Heather Hinton, Jonathan Walpole, Peat Bakke, Steve Beattie, Aaron Grier, Perry Wagle and Qian Zhang, StackGuard, automatic adaptive detection and prevention of buffer-overflow attacks, 7th USENIX Security Symposium, 1998, pages 63-78"
    locator: the canary word next to the return address, the terminator and random canaries, and the measured cost
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, 2013 IEEE Symposium on Security and Privacy, pages 48-62"
    locator: the section on stack cookies among the defenses against control-flow hijacking, and what they leave open
  - paper: doi:10.1145/2714576.2714635
    title: Thurston H. Y. Dang, Petros Maniatis and David Wagner, The performance cost of shadow stacks and stack canaries, ASIA CCS 2015, pages 555-566
    locator: the comparison of canaries with shadow stacks in cost and in the attacks each one stops
---

A stack canary is a secret value that the compiler places in each protected stack frame, between the local arrays and the saved return address, and checks just before the function returns. A [buffer overflow](/buffer-overflow/) that writes past the end of a local array toward the return address must write over the canary first. Unless the overflow writes the exact secret value back, the check fails and the program stops before the changed return address is used. This is the defense against [stack smashing](/stack-smashing/) that Cowan et al. built into StackGuard in 1998, and every major C compiler now has it. The guarantee is narrow and exact: against an attacker who cannot read memory and who overflows a buffer contiguously, a uniformly random canary of $b$ bits lets one attempt pass with probability $2^{-b}$. It does not stop writes that skip the canary, it does not survive a leak of the canary, and it does nothing for data that the overflow changes before the return. A [shadow stack](/shadow-stack/) checks the return address itself and needs no secret.

## In plain words

Coal miners took a canary into the mine. If the air went bad, the bird died first, and the miners got out before it reached them.

A stack canary works the same way. The compiler puts a secret number in each function's block of stack memory, between the local arrays and the note that says where to return. An overflow of an array runs upward through memory. It hits the secret number before it can reach the note.

Just before the function returns, the program checks that the secret number is still there. If it changed, something overflowed. The program stops at once, instead of jumping to wherever the changed note points.

The trick works only while the number is secret, and only for overflows that run through it in order.

## When it applies

- **The threat is a contiguous overflow of a stack buffer** toward the saved return address: a copy, a string operation or a loop that writes past the end of a local array, one cell after the next.
- **The attacker cannot read the canary.** There is no information leak that reveals the stack, and no way to learn the value from crashes, for example from a server that forks children with the same canary.
- **The damage happens at the return.** The overflow is used through the return address or through data the epilogue protects, not through a pointer or a variable that the function uses before it returns.
- **Source or compiler control.** The canary is inserted by the compiler, so the code must be rebuilt. A binary without the instrumentation gets no protection.

When the threat includes arbitrary writes, use a [shadow stack](/shadow-stack/) or bounds checking ([AddressSanitizer](/addresssanitizer/), [SoftBound](/softbound/)). When it includes leaks, a canary alone is not enough.

## The template

The defense has three parts: a value chosen once per process, a store in the prologue of each protected function, and a check in its epilogue. The named holes are the choices that implementations make.

```pseudo id=main
INIT()                                        ▷ once, at process start
L1  C ← ⟨canary source⟩, for example a random word from the operating system
L2  keep C in ⟨protected storage⟩ that the program's buffers cannot overflow into

PROLOGUE(F)                                   ▷ at entry, for each F chosen by ⟨function selection⟩
L3  arrange the frame by ⟨layout rule⟩: arrays next to the canary, scalars and pointers below the arrays
L4  write ⟨canary value⟩ (C, or C xor the return address) into the canary slot between the arrays and the saved return address

EPILOGUE(F)                                   ▷ before each return of F
L5  v ← the value in the canary slot
L6  if v ≠ ⟨canary value⟩ then ⟨failure action⟩: report and end the process, without returning
L7  return through the saved return address
```

**Walk-through.** Line L1 draws the secret. Line L2 keeps the reference copy away from every buffer, in a global or thread-local word, so that an overflow cannot change both copies. Line L3 is the layout rule that ProPolice added: if arrays sit directly below the canary and scalar locals and copies of pointer arguments sit below the arrays, then an overflow of an array cannot reach a scalar or a pointer before it reaches the canary. Line L4 writes the canary into the frame. Lines L5 and L6 run before the return uses the saved address. The failure action must not return and must not trust anything in the damaged frame; it reports and ends the process.

**The guarantee, as a statement in a model.** Model the frame as a sequence of cells, with the canary cell between the last array cell and the saved return address. Let the attacker write a contiguous run of cells that starts inside an array of the frame and goes toward higher addresses, choosing every value without knowledge of $C$. If $C$ is uniform on $2^b$ values and independent of the attacker's choices, then any run that reaches the return address also writes the canary cell, with some value $v$ chosen independently of $C$, and $\Pr[v = C] = 2^{-b}$. So the probability that one such overflow changes the return address and passes line L6 is at most $2^{-b}$. Each assumption matters: a non-contiguous write need not touch the canary cell, and an attacker who knows $C$ can write it back.

**Cost.** Each protected call does one load and one store in the prologue and one load, one compare and one branch in the epilogue: $O(1)$ extra operations per call in the [word RAM](/word-ram/) model, and one word of stack per frame. The real overhead is a measurement and depends on how many functions the selection rule protects; Dang, Maniatis and Wagner (2015) compare it with the cost of shadow stacks.

## Classic examples

- **StackGuard (1998).** Cowan et al. put a canary word next to the return address in GCC-compiled code. They offered a *terminator* canary, made of bytes that end strings and lines (zero, carriage return, line feed and end of file), so that a string copy cannot write it back, and a *random* canary chosen at program start. It is the first general defense against [stack smashing](/stack-smashing/).
- **ProPolice and the GCC stack protector.** Etoh's ProPolice added the layout rule of line L3. GCC adopted it as `-fstack-protector`, with variants that protect only functions with character arrays, a wider set of functions, or all functions. Some C libraries set one byte of the random canary to zero, so the canary is both random and a terminator; then a $w$-bit canary has $w - 8$ random bits.
- **Microsoft /GS.** The Visual C++ compiler inserts a security cookie, combined with the frame address, and also orders locals. On platforms with exception handler records on the stack, an overflow could change a handler and raise an exception before the epilogue runs, which led to separate handler validation; see the variations of [stack smashing](/stack-smashing/).
- **The comparison with shadow stacks.** A [shadow stack](/shadow-stack/) checks the return address by value, with no secret, and catches non-contiguous writes too. Dang, Maniatis and Wagner (2015) measured why compilers kept the cheaper canary as the default for so long.

## Variations

- **XOR canary.** Store $C \oplus a$ where $a$ is the return address, and check it against the current return address in the epilogue. A write that changes $a$ but skips the canary slot now fails the check too, because the stored value no longer matches. An attacker who knows $C$ can still compute the right value.
- **Per-frame or per-call canaries.** Derive the canary from $C$ and the frame, so that a leaked canary of one frame does not give the canary of another. The cost is a few more operations per call.
- **Renewing the canary in child processes.** A server that forks children with the same canary lets an attacker learn about the value from which requests crash a child. Choosing a fresh canary in each child removes that channel; then the probability bound of the template holds for each attempt again.
- **Heap canaries and guard values.** Allocators put check values in chunk headers to detect heap overflows on free. The idea is the same; the check point is the allocator, not the return.
- **Memory tagging.** [Memory tagging](/memory-tagging/) gives each allocation a small tag and checks it on every access, which catches the overflow at the first wrong cell rather than at the return. With 4-bit random tags, a mismatch is caught with probability $15/16$.

## Pitfalls

- **A canary that is not secret.** A fixed or predictable value, a value printed by a [format string error](/format-string-vulnerability/), or a value read through any memory leak makes the check pass for the attacker. The bound $2^{-b}$ needs a uniform value that the attacker cannot see.
- **Non-contiguous writes.** An out-of-bounds index, a write through a corrupted pointer, or a format string write can change the return address without touching the canary slot. A plain canary does not see it.
- **Damage before the return.** The check runs only in the epilogue. If the overflow changes a local function pointer, a pointer argument, or a decision variable that the function uses before it returns, the harm is done first. The layout rule of line L3 reduces this, but it cannot reorder fields inside a structure.
- **Functions left out.** A selection rule that protects only functions with character arrays leaves functions with other arrays or with arrays inside structures unprotected.
- **A failure action that trusts the frame.** The handler must not return, unwind with the damaged frame, or call code reached through data on the damaged stack.
- **Too few random bits.** On a 32-bit system with a zero byte, a canary has 24 random bits, and one blind attempt passes with probability $2^{-24} \approx 5.96 \times 10^{-8}$. That is small per attempt, but a process that is restarted without a fresh canary gives the attacker many attempts.

## Exercises

1. In the cell model of the template, the frame from low to high addresses is: an array of 8 cells, the canary, a saved frame pointer, the return address. List the write runs $[i, j]$ (start and end cell, with $0 \le i \le 7$) that change the return address. Show that each of them also writes the canary cell.
2. Prove the bound of the template: if $C$ is uniform on $\{0, \ldots, 2^b - 1\}$ and the value $v$ written into the canary cell is independent of $C$, then $\Pr[v = C] = 2^{-b}$, whatever the distribution of $v$.
3. For an XOR canary $C \oplus a$, show that a write that changes the return address from $a$ to $a' \ne a$ and leaves the canary slot unchanged always fails the check. What does an attacker who knows $C$ need to write?
4. A canary has 24 random bits. If every child of a server has the same canary, a blind attacker who never repeats a whole guess needs $(2^{24} + 1)/2$ attempts on average. If every child gets a fresh uniform canary, each attempt passes with probability $2^{-24}$ independently; give the expected number of attempts with the [geometric distribution](/geometric-distribution/). Explain why renewal gains only a factor of about 2 against blind whole guesses, and why it gains much more against an attacker who learns the canary in parts from which attempts crash.

## References
