---
tag: 11NPNM
kind: technique
slug: meltdown-attack
name: Meltdown attack
aliases:
- Meltdown
- rogue data cache load
area: security-and-privacy/side-channel-attacks
level: advanced
summary: A transient execution attack class in which a load that should fault passes protected data to later transient instructions, which leave a cache trace before the fault is handled.
prereqs: [flush-and-reload, side-channel-attack]
see_also: [spectre-attack, flush-and-reload, prime-and-probe, address-space-layout-randomization, aslr-derandomization-attack, constant-time-verification, set-associative-cache, software-fault-isolation]
sources:
  - paper: "Moritz Lipp, Michael Schwarz, Daniel Gruss, Thomas Prescher, Werner Haas, Anders Fogh, Jann Horn, Stefan Mangard, Paul Kocher, Daniel Genkin, Yuval Yarom and Mike Hamburg, Meltdown, reading kernel memory from user space, 27th USENIX Security Symposium, 2018, pages 973-990"
    locator: the description of transient instructions after a fault, the processors the authors evaluated, and the section on countermeasures with KAISER
  - paper: doi:10.1007/978-3-319-62105-0_11
    title: "Daniel Gruss, Moritz Lipp, Michael Schwarz, Richard Fellner, Clémentine Maurice and Stefan Mangard, KASLR is dead, long live KASLR, ESSoS 2017, LNCS 10379, pages 161-176"
    locator: the KAISER design, which keeps the kernel out of the address space of user programs, and its measured cost
  - paper: "Claudio Canella, Jo Van Bulck, Michael Schwarz, Moritz Lipp, Benjamin von Berg, Philipp Ortner, Frank Piessens, Dmitry Evtyushkin and Daniel Gruss, A systematic evaluation of transient execution attacks and defenses, 28th USENIX Security Symposium, 2019, pages 249-266, arXiv:1811.05441"
    locator: the classification of transient execution attacks into Spectre-type and Meltdown-type, and the evaluation of the defenses against each class
  - paper: "Paul Kocher, Jann Horn, Anders Fogh, Daniel Genkin, Daniel Gruss, Werner Haas, Mike Hamburg, Moritz Lipp, Stefan Mangard, Thomas Prescher, Michael Schwarz and Yuval Yarom, Spectre attacks, exploiting speculative execution, IEEE Symposium on Security and Privacy 2019, pages 1-19"
    locator: the comparison of Spectre with Meltdown, which needs no misprediction but a fault
---

The Meltdown attack is a class of transient execution attacks in which a load that the processor will refuse, because the program may not read that memory, still passes the value to the instructions that follow it for a short time. Those transient instructions are later discarded, but they can leave a trace of the value in the cache, and a cache channel such as [Flush+Reload](/flush-and-reload/) reads the trace out. Lipp et al. (2018) showed that this let a user program on many processors of the time read memory of the operating system kernel. The main software defense is to keep the kernel out of the address space of user programs, the KAISER design of Gruss et al. (2017); the full fix is a processor that does not pass the value on. Unlike the [Spectre attack](/spectre-attack/), Meltdown needs no misprediction, only a fault that is raised late.

## In plain words

A modern processor does not wait for each instruction to finish before it starts the next one. It runs ahead and throws away the work if it turns out that an earlier step was not allowed. On some processors, a read of forbidden memory gave the value to the next instructions for a moment, before the processor noticed that the read was forbidden and threw the work away.

The thrown-away work cannot be seen directly. But it may have brought some memory into the cache, and the cache does not forget. A program that watches the cache can learn something about the forbidden value. Doing this again and again, it can learn the value itself.

## When it applies

### Threat model

The observer is an unprivileged program on the same machine. Memory protection says that he may not read some memory, usually the kernel, even though it is mapped in his address space with a supervisor-only mark. He sees only the architectural results of his own program and the effect of the cache on his own accesses. The defenses below are stated against this observer.

### Conditions

1. **MAPPED.** The protected value is in the address space of the observer, marked as not readable by him. Before 2018 most operating systems mapped all of the kernel into every process, for speed.
2. **FORWARD.** A load that fails its permission check passes its value to later instructions, and the fault is raised only when the load retires. This is a property of the design of the processor.
3. **ENCODE.** The transient instructions can change some state that survives their discard, such as the content of the cache.
4. **CHANNEL.** The observer can read that state, for example with a cache channel.
5. **SURVIVE.** The observer goes on running after the fault.

### What removes a condition

| defense | condition it removes | cost |
|---|---|---|
| kernel page table isolation (KAISER, KPTI): user programs run with a map that leaves out almost all of the kernel | 1 | work on each switch between user and kernel mode, which hardware support for address space tags reduces |
| processors that stop the value at the permission check | 2 | none at run time, but only on new hardware |
| defenses of the cache channel (partitioning, coarse timers, noise) | 4, partly (heuristic) | the channel can be rebuilt on other shared state |
| constant-time code | none | it protects against an observer of addresses, but Meltdown reads the data value itself |

Meltdown is a fault in the hardware, so constant-time code does not stop it. The software defense moves the secret out of reach of the transient load. The guarantee of KAISER is about the memory that is no longer mapped: whatever stays mapped for the switch into the kernel can still be reached.

## The template

The block is the shape of the class: each line is a condition that the attack needs, and the comment names the defense that removes it. It is not a recipe.

```pseudo id=main
MELTDOWN-CLASS(processor P, operating system O)
L1  require MAPPED: O maps the protected value into the observer's address space   ▷ removed by KAISER and KPTI
L2  require FORWARD: P passes the value of a refused load to later instructions     ▷ removed in hardware
L3  require ENCODE: transient instructions change state that their discard keeps   ▷ hole STATE: the cache, or other buffers
L4  require CHANNEL: the observer can read that state                              ▷ hole CHANNEL: Flush+Reload or Prime+Probe
L5  require SURVIVE: the observer continues after the fault                        ▷ no defense removes this alone
L6  if every condition holds then the observer learns a function of the protected value
```

### An abstract model

Take an abstract machine with registers, a memory with a permission bit on each cell and a cache that is a set of lines. After a refused load of a cell with value $v$, the machine runs one transient step that uses the line $f(v)$, for a made-up function $f$, and then it discards the registers of that step and raises the fault. The cache keeps $f(v)$. The observer sees the set of lines in the cache.

| machine | what the observer sees |
|---|---|
| FORWARD holds and the cell is mapped | the line $f(v)$, which depends on $v$ |
| the cell is not mapped (KAISER) | no transient line, for every $v$ |
| FORWARD fails: the refused load passes the constant 0 | the line $f(0)$, for every $v$ |

**Claim (theorem, in the abstract model).** If a refused load passes no value, or a value that does not depend on the protected cell, then the cache after the discard is the same for every value of the protected cell. *Proof.* The transient step is a function of its input. If the input is the same for every value of the cell, so is the line it uses, and every other line of the cache depends only on the observer's own steps. The statement is about the model; it does not cover other buffers of a real processor, which is why later variants of the class needed further fixes.

### Meltdown and Spectre

Canella et al. (2019) sort transient execution attacks into two classes. Meltdown-type attacks use the transient work after a fault or an assist: the value comes from memory that the observer may not read. Spectre-type attacks use the transient work after a misprediction: the victim itself reads a value it may read, on a path that it should not take. So the defenses differ. KAISER does nothing against Spectre, and speculation barriers in the victim do nothing against Meltdown.

## Classic examples

- **KASLR breaks, 2016 and 2017.** Several timing channels showed where the kernel was in the address space, which defeated [kernel address space layout randomization](/address-space-layout-randomization/); see [ASLR derandomization](/aslr-derandomization-attack/). Gruss et al. proposed KAISER in 2017 as a defense against those channels, before Meltdown was public.
- **Meltdown, 2018 (measurement).** Lipp et al. read kernel memory, and through the kernel's map of all physical memory also memory of other processes, from an unprivileged program on many Intel processors and on some other cores. The operating systems shipped kernel page table isolation, based on KAISER, at the time of the disclosure in January 2018.
- **Later Meltdown-type variants, 2018 and 2019.** Other refused or assisted loads were found to pass values from other buffers of the processor, such as the first-level data cache and the fill and store buffers. Each needed its own fix in microcode, in the operating system or in new hardware.
- **The channel.** Each of these uses a cache channel such as [Flush+Reload](/flush-and-reload/) or [Prime+Probe](/prime-and-probe/) at the end. The channel is old; the source of the value is new.

## Variations

- **Different fault sources.** The refused load can fail on the supervisor bit, on a page that is not present, or on a register that needs privilege. Each source is a separate variant in the classification of Canella et al.
- **Different buffers.** Variants differ in where the transient value comes from: the cache, the fill buffers, the store buffer or the load ports.
- **Different channels.** The trace can go through the cache or through other shared state, so defending one channel does not close the class.
- **Fault suppression.** The observer can avoid the fault ending the program in several ways, which is why condition 5 has no defense of its own.

## Pitfalls

- **Treating it as a software bug.** Meltdown is a property of the processor. Code that is correct and constant time is still exposed if the processor and the operating system meet conditions 1 and 2.
- **Confusing it with Spectre.** The defenses of one class do not stop the other.
- **Confusing the word speculation.** In distributed computing, speculative execution means running backup copies of slow tasks. That idea has nothing to do with transient execution in a processor.
- **Forgetting what stays mapped.** Kernel page table isolation keeps a small part of the kernel mapped for the switch into the kernel. That part must hold no secrets.
- **Turning off the defense for speed.** The cost of page table isolation led some systems to switch it off. That is safe only on processors where condition 2 does not hold.

## References
