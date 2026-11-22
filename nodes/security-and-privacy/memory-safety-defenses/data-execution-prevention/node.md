---
tag: NS1DRS
kind: technique
slug: data-execution-prevention
name: Data execution prevention
aliases:
- W xor X
- non-executable memory
area: security-and-privacy/memory-safety-defenses
level: intro
summary: Marks each page either writable or executable but never both, so that injected data cannot run as code.
history:
  year: 2004
  people: [Solar Designer, PaX Team, Theo de Raadt]
  note: Non-executable stack patches (1997) and PaX (2000) came first. Hardware no-execute bits on x86 (2003 and 2004), OpenBSD W^X (2003) and Windows DEP (2004) made the policy standard.
prereqs: [stack-smashing]
see_also: [return-to-libc-attack, return-oriented-programming, control-flow-integrity, software-fault-isolation, just-in-time-compilation, address-space-layout-randomization, stack-canary, memory-safety]
sources:
  - url: "https://learn.microsoft.com/en-us/windows/win32/memory/data-execution-prevention"
    title: Microsoft, Data Execution Prevention, Win32 documentation
    locator: the whole page (non-executable data pages, the access violation on a violation, and the rules for code generated at run time)
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, 2013 IEEE Symposium on Security and Privacy, pages 48-62"
    locator: the section on non-executable data among the defenses against code injection, and why code reuse goes around it
  - paper: "Hovav Shacham, The geometry of innocent flesh on the bone, return-into-libc without function calls (on the x86), 14th ACM Conference on Computer and Communications Security (CCS 2007), pages 552-561"
    locator: the introduction and conclusion (W xor X stops code injection but not code reuse)
  - paper: doi:10.1145/1609956.1609960
    title: Martin Abadi, Mihai Budiu, Ulfar Erlingsson and Jay Ligatti, Control-flow integrity, principles, implementations, and applications, ACM Transactions on Information and System Security 13(1), article 4, 2009
    locator: the assumptions of non-writable code and non-executable data on which the CFI guarantee rests
---

Data execution prevention (DEP), or the W xor X policy, gives each page of memory permission to be written or to be executed, but never both. Code pages are readable and executable; the stack, the heap and other data pages are readable and writable, with a no-execute bit set. The processor checks the bit on every instruction fetch, so a jump into a data page faults. An attacker who places machine code in a buffer by a [buffer overflow](/buffer-overflow/) and then redirects control to it, as in classic [stack smashing](/stack-smashing/), gets a fault instead of a run. DEP stops code *injection*. It does not stop code *reuse*: [return-to-libc](/return-to-libc-attack/) calls library functions that already exist, and [return-oriented programming](/return-oriented-programming/) chains short pieces of existing code into any computation, with no new code at all (Shacham 2007). So DEP is a base layer, and its main value today is as an assumption of stronger defenses: [control-flow integrity](/control-flow-integrity/) and [software fault isolation](/software-fault-isolation/) are sound only if code cannot be written and data cannot run.

## In plain words

A program's memory holds two kinds of things: instructions, which the processor runs, and data, which the program reads and writes. To the processor both are bytes. If an attacker can write bytes into a data area and then make the program jump there, the processor runs those bytes as instructions.

DEP gives every page of memory a label. A page of instructions may be run but not changed. A page of data may be changed but not run. The processor checks the label every time it fetches an instruction. If the page is a data page, it stops the program.

So writing new instructions into a buffer no longer helps an attacker. But the program's own instructions can still run, and an attacker who controls where the program jumps can reuse them. DEP closes one door, not all of them.

## When it applies

- **The threat is code injection**: the attacker can write bytes into memory and can redirect control to them.
- **The hardware has a no-execute permission per page**, such as the NX or XD bit of x86-64, or the execute-never bits of Arm. Without it, systems emulated the policy in software with segment limits or with tricks on the translation buffers, at a higher cost.
- **The program does not need to write and then run code**, or it does so only in regions that it marks and manages, as a [just-in-time compiler](/just-in-time-compilation/) does.
- **Another defense depends on it.** CFI assumes that code cannot change and that data cannot run; SFI assumes the same for the sandboxed module.

## The template

The policy has a load-time part, a part that governs changes of permissions, and a check that hardware runs on every fetch and store. The named holes are where systems differ.

```pseudo id=main
MAP(region R)                                    ▷ at load time and on each allocation
L1  if R holds code from the program image then perm(R) ← {read, execute}
L2  else perm(R) ← {read, write}                 ▷ no-execute set: stack, heap, globals, mapped data

CHANGE-PERMISSION(R, p)                          ▷ a request from the program to change perm(R) to p
L3  if write ∈ p and execute ∈ p then refuse     ▷ strict W xor X at every moment
L4  if execute ∈ p and R was writable before then apply ⟨code generation rule⟩
L5  perm(R) ← p

FETCH(x)                                         ▷ in hardware, at each instruction fetch from address x
L6  if execute ∉ perm(page of x) then fault "no-execute violation"

STORE(x)                                         ▷ in hardware, at each store to address x
L7  if write ∉ perm(page of x) then fault "write to a read-only page"
```

**Walk-through.** Lines L1 and L2 set the initial labels: only the code of the program image and its libraries is executable. Line L3 forbids a page that is writable and executable at once. Line L4 is the choice for memory that was written and then becomes code, which a just-in-time compiler or a loader needs. Strict systems refuse it unless the region was created for that purpose; others allow it, which weakens the guarantee over time. Lines L6 and L7 are the checks that make the labels mean something: they run in the memory management unit on every access, at no extra instruction cost.

**The guarantee, as a statement in a model.** Suppose that every instruction fetch passes line L6, that every store passes line L7, and that line L4 refuses every change. Then the only bytes that ever run are the bytes that were mapped as code at line L1, and those bytes never change after load, because every store to them faults at line L7. So no byte written by the program, and so no byte written by an attacker through a memory error, ever runs as an instruction. The statement says nothing about which of the original instructions run, or in what order. Control flow is still open to the attacker.

**Cost.** In the [word RAM](/word-ram/) model the checks are free: they are part of address translation, one permission test per access. Systems without a hardware bit paid a measurable cost to emulate it.

## Classic examples

- **Stopping injected code in [stack smashing](/stack-smashing/).** The classic attack writes machine code into a stack buffer and points the return address at it. With a non-executable stack, the jump faults at line L6.
- **The answer of code reuse: [return-to-libc](/return-to-libc-attack/).** In 1997, the same year as the first non-executable stack patch for Linux, Solar Designer showed that a hijacked return could call an existing library function instead. DEP does not see this, since the target is in a code page.
- **[Return-oriented programming](/return-oriented-programming/).** Shacham (2007) showed that short instruction sequences that end in a return, found in existing code, give a Turing-complete set of operations. His lesson was that W xor X alone does not stop an attacker who controls the stack.
- **An assumption of [control-flow integrity](/control-flow-integrity/).** Abadi et al. state the CFI guarantee under non-writable code and non-executable data. Without DEP, an attacker could write new code with no label checks, or change the checks themselves.
- **An assumption of [software fault isolation](/software-fault-isolation/).** SFI rewrites the code of a module so that its stores and jumps stay inside its region. If the module could write code and run it, the rewritten checks could be bypassed.

## Variations

- **Strict W xor X over time.** Some systems refuse line L4 entirely: a page that was ever writable never becomes executable. PaX called this restriction MPROTECT. It stops an attacker who can call the permission change function from making injected data executable, at the cost of breaking programs that generate code.
- **Code generation at run time.** A [just-in-time compiler](/just-in-time-compilation/) must write code and then run it. Safe designs keep the two permissions apart in time (write, then flip to execute) or in space (two virtual mappings of the same physical page, one writable and one executable, at addresses that the program does not leak). JIT spraying, the placement of attacker-chosen constants in generated code, showed that the generated code itself is a target.
- **Execute-only memory.** Some architectures can mark code pages executable but not readable. This hides the code from an attacker who can read memory, which makes code reuse harder when combined with randomization.
- **Kernel versions.** Supervisor mode execution prevention stops the kernel from running code in user pages, and supervisor mode access prevention stops it from reading or writing user pages without an explicit step. They apply the same idea to the boundary between kernel and user space.

## Pitfalls

- **Thinking DEP stops hijacking.** It stops one kind of payload. Control flow is still hijacked, and code reuse needs no new code. Combine DEP with [ASLR](/address-space-layout-randomization/), [stack canaries](/stack-canary/), a [shadow stack](/shadow-stack/) and [CFI](/control-flow-integrity/).
- **Writable and executable regions.** A single region with both permissions, often left by an old JIT or a plug-in, gives injected code a home again. Line L3 must hold for every region, not only for the stack.
- **An open permission change.** If line L4 allows every change, an attacker who can call the permission function through code reuse can make a buffer executable and then run it. Restrict the change, or allow it only for regions created for code generation.
- **Opting out.** Many systems let a program opt out of DEP for compatibility. One old library that needs executable data can turn the protection off for the whole process.
- **Code in data sections.** Executables that keep small code stubs in data sections fail under DEP, as the Microsoft documentation notes. Move such code to a code section rather than mark the data executable.

## Exercises

1. Show that the guarantee of the template fails if line L4 allows any change: give a sequence of permission changes, stores and fetches, on abstract regions R1 and R2, in which a byte written by a store is later fetched as an instruction while lines L3, L6 and L7 all hold.
2. A JIT keeps two virtual mappings of the same physical page, one with {read, write} and one with {read, execute}. Does this system satisfy line L3? Does it satisfy the guarantee of the template? What must stay secret?
3. Explain why CFI needs non-writable code. Describe what an attacker who can write one byte of a code page could do to the label check at an indirect call.
4. List the lines of the [stack smashing](/stack-smashing/) template that DEP breaks and the lines it leaves open.

## References
