---
tag: VGQ79M
kind: technique
slug: address-space-layout-randomization
name: Address space layout randomization
aliases:
- ASLR
area: security-and-privacy/memory-safety-defenses
level: core
summary: Places code, stack, heap and libraries at random addresses at load time, so that an attacker cannot predict the target of a jump.
history:
  year: 2001
  people: [PaX Team, Hovav Shacham, Sandeep Bhatkar]
  note: PaX added ASLR to Linux in 2001. OpenBSD, Linux, Windows and macOS adopted forms of it in the following years. Shacham et al. (2004) showed the limits of 16 bits of entropy on 32-bit systems.
prereqs: [stack-smashing, data-execution-prevention]
see_also: [aslr-derandomization-attack, return-to-libc-attack, return-oriented-programming, shadow-stack, control-flow-integrity, uniform-distribution, geometric-distribution, side-channel-attack]
sources:
  - url: "https://pax.grsecurity.net/docs/aslr.txt"
    title: PaX Team, Address space layout randomization (design document)
    locator: the whole document (the randomized areas, the bits of randomness on i386, the remark on fork and brute force, and the threat model)
  - paper: doi:10.1145/1030083.1030124
    title: Hovav Shacham, Matthew Page, Ben Pfaff, Eu-Jin Goh, Nagendra Modadugu and Dan Boneh, On the effectiveness of address-space randomization, CCS 2004, pages 298-307
    locator: the analysis of the entropy of PaX ASLR, the measured time to find the offset, and the conclusions on 64-bit systems and rerandomization
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, 2013 IEEE Symposium on Security and Privacy, pages 48-62"
    locator: the section on address space randomization as a probabilistic defense and its weakness to memory leaks
---

Address space layout randomization (ASLR) loads the parts of a process at random addresses: the stack, the heap, the shared libraries and, in position-independent programs, the program image itself. An attacker who has hijacked control by a memory error, as in [stack smashing](/stack-smashing/), must still give a target address. Under [data execution prevention](/data-execution-prevention/) the target must be existing code, as in [return-to-libc](/return-to-libc-attack/) and [return-oriented programming](/return-oriented-programming/), and with ASLR the attacker does not know where that code is. A wrong guess usually crashes the process. The guarantee is probabilistic and rests on a secret: if the base of a region is uniform on $2^k$ values and the attacker has no information about it, one guess is right with probability $2^{-k}$. Two things break it. A memory leak of one pointer reveals the base of its region at once, and a low $k$ lets the attacker guess. Shacham et al. (2004) showed the second on 32-bit Linux with PaX, where the library base had 16 bits of randomness and a forking server let them find it in minutes; see the [derandomization attack](/aslr-derandomization-attack/). On 64-bit systems the entropy is much larger, so leaks are now the main threat. ASLR is cheap and on by default almost everywhere, but it is a layer, not a check like a [shadow stack](/shadow-stack/) or [control-flow integrity](/control-flow-integrity/).

## In plain words

To jump to useful code, an attacker must know where the code is. Without ASLR, a program and its libraries load at the same place every time, so the attacker can learn the addresses once, on a copy of the program, and use them everywhere.

ASLR moves the pieces to a random place each time the program starts. The attacker now has to guess. A wrong guess usually makes the program crash, which a monitor can notice.

The protection is only as good as the secret. If the program ever shows one address of a library, the attacker can work out where the rest of that library is. And if there are only a few thousand possible places, the attacker can try them all.

## When it applies

- **The threat is control-flow hijacking that needs a known address**: the target of a hijacked return or pointer, the address of data to reuse, or a pointer that the payload must contain.
- **The attacker cannot read memory.** There is no leak of pointers, no read of the layout through a side channel, and no local access to the process's own layout. PaX says it plainly: ASLR is meant against remote attackers who cannot observe the random values.
- **Enough entropy.** The number of random bits $k$ is large enough that guessing is impractical. On 32-bit layouts this fails; on 64-bit layouts it usually holds for user space.
- **The code is relocatable.** Libraries are position-independent. The program image moves only if it is built as a position-independent executable; otherwise it stays at a fixed address and gives the attacker known code.
- **Each attempt meets a fresh secret, or attempts are rare.** A server that creates workers by fork without a new layout gives every worker the same secret.

## The template

The defense has a part at load time and a security statement in a model. The named holes are the choices of each system.

```pseudo id=main
LOAD(process image with regions R₁, …, Rₘ)
L1  for each region Rᵢ chosen by ⟨randomized regions⟩ do
L2      δᵢ ← uniform on {0, 1, …, 2^kᵢ - 1}          ▷ kᵢ = ⟨entropy⟩ of region i, from the system's random source
L3      base(Rᵢ) ← ⟨default base⟩ᵢ + δᵢ · ⟨alignment⟩    ▷ page alignment keeps the low bits fixed
L4  map each Rᵢ at base(Rᵢ) and keep δᵢ secret from the process's inputs and outputs

ON-NEW-PROCESS(parent)
L5  if ⟨renewal rule⟩ says so then run LOAD again, else the child keeps the parent's δ values   ▷ fork keeps the layout

TARGET(attacker's guess g of the address of code at offset o in region Rᵢ)
L6  the hijacked control goes to g; it reaches the intended code only if g = base(Rᵢ) + o
L7  otherwise the process most likely faults, and ⟨crash response⟩ decides what happens next
```

**Walk-through.** Lines L1 to L3 draw a secret offset for each region. The entropy $k_i$ is the number of random bits, which depends on the size of the address space, on the alignment of line L3, and on how much room the system keeps between regions. Line L4 is where the secret must stay secret: any output that depends on a base, such as a printed pointer, an uninitialized buffer sent to the network, or a timing difference, leaks it. Line L5 is the renewal rule, which decides whether a new process meets a new secret. Lines L6 and L7 describe what the attacker faces: an address in the program's inputs works only if it is right for this run.

**The guarantee, as a statement in a model.** Fix one region with $k$ bits of entropy and an attacker who must name an address in it exactly. Assume that $\delta$ is uniform and independent of everything the attacker sees, and that a wrong guess ends the attempt.

- One guess succeeds with probability $2^{-k}$, whatever the attacker's strategy, by the [uniform distribution](/uniform-distribution/) of $\delta$.
- If each attempt meets the same $\delta$ (no renewal at line L5) and the attacker learns which guesses failed, the attacker tries distinct values, and the expected number of attempts to succeed is $(2^k + 1)/2$.
- If each attempt meets a fresh $\delta$ (renewal at line L5), each attempt succeeds with probability $2^{-k}$ independently, and the expected number is $2^k$, by the [geometric distribution](/geometric-distribution/).

So renewal only doubles the expected work against a blind guesser, which is about one bit of entropy, the conclusion of Shacham et al. (2004). Renewal matters much more against an attacker who learns the secret in parts from which attempts crash. And the statement needs both assumptions: one leaked address of the region makes the success probability 1.

**Cost.** In the [word RAM](/word-ram/) model the defense costs nothing per operation once the regions are mapped. Real costs come from position-independent code, which needs an extra register or indirection on some architectures, and from the loss of fixed addresses for prelinking.

## Classic examples

- **PaX ASLR (2001).** The PaX design randomizes the program image, the heap, the mapped area with the libraries, and the stack, each with its own delta. On i386 its document gives 16 bits for the program image and the mapped area and 24 bits for the stack, and it notes that a daemon that forks per connection keeps the same layout and so invites brute force. It recommends pairing ASLR with a response to crashes.
- **The 2004 study and the [derandomization attack](/aslr-derandomization-attack/).** Shacham et al. found the 16-bit offset of the library area of a forking server on 32-bit x86 in an average of 216 seconds, then ran a [return-to-libc](/return-to-libc-attack/) payload. Their conclusions: on 32-bit systems ASLR gives little protection, raising the entropy to 20 bits would only multiply the time by about 16, renewal adds about one bit, and real protection needs 64-bit address spaces.
- **Deployment.** OpenBSD, Linux, Windows (from Vista) and macOS added forms of ASLR in the years after PaX. Their early versions often left the program image at a fixed address, which gave [return-oriented programming](/return-oriented-programming/) a known code base; position-independent executables closed that gap.
- **Kernel ASLR.** Kernels randomize their own base. A local attacker can often learn it through a [side channel](/side-channel-attack/) in the processor, such as the time of an access, so kernel ASLR is weaker than its entropy suggests. This is part of the reason for the page-table isolation added after the [Meltdown attack](/meltdown-attack/).

## Variations

- **Fine-grained randomization.** Randomize the order of functions, basic blocks or even instructions, so that a leak of one address reveals less. It was answered by attacks that read code at run time through a leak, which led to execute-only memory combined with randomization.
- **Address obfuscation.** Bhatkar, DuVarney and Sekar (2003) added random gaps between objects and random padding in frames, a finer version of the same idea.
- **Rerandomization.** Draw a new layout for every worker, every request or at intervals. It stops attempts from adding up against a fixed secret, but it gives about one bit against blind guessing, as computed above, and it costs relocation work.
- **Leak resistance.** Combine ASLR with execute-only memory, with pointer encryption, or with a separate safe region for pointers, as in [code-pointer integrity](/code-pointer-integrity/), so that a leak gives less.

## Pitfalls

- **Treating ASLR as a check.** It does not stop a hijack; it makes the target uncertain. Combine it with checks whose guarantees do not depend on a secret: a [shadow stack](/shadow-stack/), [CFI](/control-flow-integrity/), bounds checks.
- **One leak breaks a whole region.** All objects of a region move together. A single leaked code pointer of a library reveals every address in that library. Treat every pointer leak as a full break of ASLR for its region.
- **Partial overwrites.** Page alignment keeps the low bits of every address fixed. A memory error that changes only the low part of a pointer keeps its random high part and needs no knowledge of the base. Only checks on the pointer stop this.
- **Fork without renewal.** A server that forks workers from one parent gives them all the same layout. Crashes then let an attacker learn the layout over many attempts. Monitor crashes and limit restarts, or renew the layout.
- **A fixed program image.** A program not built as position-independent stays at the same address in every run, and its code is enough for code reuse.
- **Low entropy.** 16 bits fall to guessing (Shacham et al. 2004). Count the real entropy: alignment, gaps and the address space size all reduce it.

## Exercises

1. Prove the three statements of the model in the template: one guess succeeds with probability $2^{-k}$; without renewal the expected number of attempts by an attacker who never repeats a value is $(2^k + 1)/2$; with renewal it is $2^k$.
2. With $k = 16$, compute the two expected numbers of attempts of Exercise 1. If each attempt takes the same time, how many bits of entropy does renewal add against a blind guesser?
3. A system has two regions with independent offsets of $k_1$ and $k_2$ bits, and an attack needs an exact address in both. Give the probability that a blind attempt succeeds. Then suppose a leak reveals the first base. What is the probability now?
4. Explain why page alignment at line L3 means that a write that changes only the lowest 12 bits of a code pointer is not affected by ASLR. Which defense of another page stops it?

## References
