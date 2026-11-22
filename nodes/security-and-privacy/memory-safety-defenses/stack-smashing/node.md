---
tag: 3MJ6EJ
kind: technique
slug: stack-smashing
name: Stack smashing
aliases:
- stack buffer overflow attack
area: security-and-privacy/memory-safety-defenses
level: intro
summary: Overflows a stack buffer to overwrite the saved return address, so that the function returns into code the attacker chose.
history:
  year: 1988
  people: [Robert T. Morris, Crispin Cowan]
  note: The Morris worm of 1988 used a stack buffer overflow in fingerd. Canaries (StackGuard, 1998) and non-executable stacks were the first general defenses.
prereqs: [buffer-overflow, activation-record]
see_also: [stack-canary, shadow-stack, data-execution-prevention, address-space-layout-randomization, return-to-libc-attack, return-oriented-programming, memory-safety, format-string-vulnerability]
sources:
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, 2013 IEEE Symposium on Security and Privacy, pages 48-62"
    locator: the general model of memory corruption attacks (the steps from a memory error to a control-flow hijack) and the policies that stop each step
  - paper: "Crispin Cowan, Calton Pu, Dave Maier, Heather Hinton, Jonathan Walpole, Peat Bakke, Steve Beattie, Aaron Grier, Perry Wagle and Qian Zhang, StackGuard, automatic adaptive detection and prevention of buffer-overflow attacks, 7th USENIX Security Symposium, 1998, pages 63-78"
    locator: the description of the attack class against the stack frame and the canary defense
  - paper: "Eugene H. Spafford, The Internet worm program, an analysis, ACM SIGCOMM Computer Communication Review 19(1), 1989"
    locator: the section on the fingerd attack (a stack buffer filled by gets with no length check)
  - url: "https://learn.microsoft.com/en-us/windows/win32/memory/data-execution-prevention"
    title: Microsoft, Data Execution Prevention, Win32 documentation
    locator: the whole page (stacks and heaps are not executable, and a violation raises an access violation)
---

Stack smashing is the oldest form of control-flow hijacking. A function copies input into a local array on the stack without checking its length, the copy runs past the end of the array, and it changes the saved return address that sits higher in the same [activation record](/activation-record/). When the function returns, control goes wherever the changed value points. It is the stack case of the [buffer overflow](/buffer-overflow/), a violation of spatial [memory safety](/memory-safety/). This page describes the class at the level of a textbook: the conditions it needs, the history, and above all the defenses, each of which breaks one condition. Most of these defenses are now on by default: [stack canaries](/stack-canary/), [data execution prevention](/data-execution-prevention/), [address space layout randomization](/address-space-layout-randomization/) and, in newer hardware, [shadow stacks](/shadow-stack/). The page gives no code and no details of any real program.

## In plain words

Each running function gets a small block of memory on the stack. The block holds its local variables and a note that says where to go back to when the function ends. The note sits just above the local variables.

Suppose a function keeps a name in a local array of 16 characters, and copies a name into it without checking the length. A longer name does not stop at the end of the array. It keeps going and writes over whatever comes next, including the note.

When the function ends, the program reads the note and jumps there. If the note was changed, the program now runs code that someone else chose.

Every defense on this page removes one link in that chain: check the length, notice that the note changed, keep a safe copy of the note, or make sure the jump cannot land on useful code.

## When it applies

The class needs all of these conditions. A defense works by removing one of them.

- **An unchecked write into a stack buffer.** The program writes past the end of a local array: a copy whose length comes from the input, a loop with an off-by-one bound, or a string function that does not take a length. Memory-safe languages and bounds checking ([fat pointers](/fat-pointer/), [SoftBound](/softbound/), [AddressSanitizer](/addresssanitizer/)) remove this condition.
- **Control data next to the buffer.** The saved return address, a saved frame pointer, a function pointer or an exception handler record lies above the buffer in the direction of the write. Compilers that put arrays above other locals, or that move arrays to a separate stack, as the safe stack of [code-pointer integrity](/code-pointer-integrity/) does, weaken this condition.
- **No check before the return uses the value.** A [stack canary](/stack-canary/) checks a secret value between the buffer and the return address. A [shadow stack](/shadow-stack/) compares the return address with a protected copy.
- **A useful target.** The new return address must lead to code that does what the attacker wants. Classic attacks put that code in the overflowing data itself, which [data execution prevention](/data-execution-prevention/) stops. Later attacks reuse code that is already there: [return-to-libc](/return-to-libc-attack/) and [return-oriented programming](/return-oriented-programming/). [ASLR](/address-space-layout-randomization/) hides where code lies, and [control-flow integrity](/control-flow-integrity/) limits where a return may go.

## The template

The class has the shape below. Each named hole is a condition from the list above, and each comment names the defense that breaks the chain at that line. It is a description of the class, not a procedure.

```pseudo id=main
STACK-SMASHING-CLASS(program P, function F with local buffer B)
L1  need ⟨unchecked write⟩: F writes data of length ℓ into B with ℓ > |B|     ▷ broken by bounds checks and safe languages
L2  need ⟨adjacent control data⟩: a saved code address A of F lies past the end of B   ▷ weakened by variable reordering and a safe stack
L3  effect: the write changes A to a new value A′                         ▷ a canary between B and A is changed too
L4  F returns: the epilogue checks the frame                              ▷ stack canary: fault if the canary changed
L5  the return reads A′ and jumps to it                                   ▷ shadow stack: fault if A′ ≠ the saved copy
L6  need ⟨useful target⟩: A′ is the address of code that runs             ▷ DEP: data is not executable; ASLR: addresses are unknown; CFI: A′ is not an allowed return site
```

**Walk-through.** Lines L1 and L2 are properties of the program: a missing bound and a frame layout. Line L3 is the memory error itself. It is a spatial error, so a defense that tracks the bounds of B stops it before any harm. Line L4 is the first point where a defense that does not track bounds can see the error: the canary lies between B and A, so a contiguous write that reaches A changes the canary too, unless it writes the same value back. Line L5 is where the changed address is used. A shadow stack catches every change of A, contiguous or not, because it compares values. Line L6 asks for a target that does what the attacker wants. Each defense of that line raises the cost in a different way: DEP removes injected code as a target, ASLR makes the address of reused code a secret, and CFI shrinks the set of allowed targets.

## Classic examples

- **The Morris worm (1988).** One of the ways the worm spread was an overflow of a stack buffer in the `fingerd` service, which read a request with `gets`, a function with no length bound (Spafford 1989). It is the standard first example of a [buffer overflow](/buffer-overflow/) used for control-flow hijacking.
- **Canaries as the first general answer.** After public descriptions of the technique in the mid-1990s, Cowan et al. (1998) built StackGuard, which places a [stack canary](/stack-canary/) before the return address and checks it at line L4. GCC and Microsoft compilers later adopted the idea by default.
- **Non-executable stacks and the move to code reuse.** Making the stack non-executable, and later all data, through [data execution prevention](/data-execution-prevention/), removed injected code as a target at line L6. Attackers moved to [return-to-libc](/return-to-libc-attack/) and then to [return-oriented programming](/return-oriented-programming/), which need no new code.
- **Randomization and its limits.** [ASLR](/address-space-layout-randomization/) made the targets of line L6 secret. Shacham et al. (2004) showed that 16 bits of randomness on 32-bit systems could be found by trial against a server that restarts after a crash; see [ASLR derandomization](/aslr-derandomization-attack/).
- **Exact return checks.** A [shadow stack](/shadow-stack/), now in hardware as Intel CET, checks line L5 without a secret. It does not stop overflows that change data other than return addresses; see [data-oriented programming](/data-oriented-programming/).

## Variations

- **Frame pointer and local variable overwrites.** The write may stop before the return address and change a saved frame pointer, a local pointer or a local flag. A canary does not see a change that stops short of it, which is why compilers put arrays above scalar locals.
- **Exception handler records.** On some platforms a record with a handler address lies on the stack. A write can change it and then cause an exception before the function returns, so the canary check at line L4 never runs. Handler validation in the runtime closes this path.
- **Non-contiguous writes.** An out-of-bounds index or a stray pointer can write the return address directly, without passing the canary. A [format string error](/format-string-vulnerability/) gives the same kind of direct write. Only line L5 (a shadow stack) or line L1 (bounds checking) catches it.
- **Overflows into other frames.** A write past the end of a buffer in one frame can reach the frames of its callers, which return later. The check of each frame still runs at its own return.
- **Heap overflows.** The same idea on the heap targets allocator metadata or function pointers instead of return addresses. It is a different page of the [buffer overflow](/buffer-overflow/) class.

## Pitfalls

These are mistakes defenders make about the class.

- **Fixing only the known function.** Replacing one call to an unbounded copy fixes one bug. The class goes away only when every write is bounded, by the language, by the library or by a checker.
- **Trusting one defense.** Each defense breaks one line of the template. A canary is bypassed by a non-contiguous write or a leak of its value, DEP by code reuse, ASLR by a leak of one address. Deploy them together.
- **Assuming 64-bit means safe.** A larger address space gives ASLR more entropy, but it does not remove lines L1 to L5.
- **Calling a crash harmless.** A crash at line L4 or L5 is the defense working, and the bug under it is still exploitable in other ways. Fix the bug, and do not let a server restart forever without a new random layout.
- **Measuring only return addresses.** An overflow that changes a decision variable, a length or a pointer can do harm with the return address intact. These are the non-control-data attacks of [data-oriented programming](/data-oriented-programming/).

## Exercises

1. A frame holds, from low to high addresses, a buffer of 16 cells, a canary of one cell, a saved frame pointer and a return address. A copy writes $\ell$ cells into the buffer starting at its first cell. For which $\ell$ does the canary change, and for which $\ell$ does the return address change? Explain why a contiguous write cannot change the return address and leave the canary as it was, unless it writes the canary value itself.
2. Repeat Exercise 1 for a write that starts at cell $i$ of the buffer and goes downward (toward lower addresses). Which control data can it reach on a stack that grows downward?
3. For each line L1 to L6 of the template, name one defense that breaks it and one condition under which that defense fails.
4. Explain why a non-executable stack alone does not stop a hijack of the return address. Which line of the template does it break, and which lines does it leave?

## References
