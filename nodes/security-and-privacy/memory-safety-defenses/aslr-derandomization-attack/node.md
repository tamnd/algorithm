---
tag: AWQ9SW
kind: technique
slug: aslr-derandomization-attack
name: ASLR derandomization by brute force
aliases:
- Shacham ASLR attack
area: security-and-privacy/memory-safety-defenses
level: advanced
summary: Guesses the random offset of a forking server by repeated probes, showing that 16 bits of entropy fall in minutes.
history:
  year: 2004
  people: [Hovav Shacham, Matthew Page, Ben Pfaff, Eu-Jin Goh, Nagendra Modadugu, Dan Boneh]
  note: Shacham et al. (CCS 2004) found the 16-bit library offset of a forking server under PaX ASLR on 32-bit x86 in minutes, and concluded that ASLR on 32-bit systems gives little protection.
prereqs: [address-space-layout-randomization]
see_also: [return-to-libc-attack, return-oriented-programming, min-entropy, union-bound, geometric-distribution, side-channel-attack, stack-canary, shadow-stack]
sources:
  - paper: doi:10.1145/1030083.1030124
    title: Hovav Shacham, Matthew Page, Ben Pfaff, Eu-Jin Goh, Nagendra Modadugu and Dan Boneh, On the effectiveness of address-space randomization, CCS 2004, pages 298-307
    locator: the abstract, the threat model, the measured average time to find the offset, and the conclusions on entropy, rerandomization and 64-bit systems
  - url: "https://pax.grsecurity.net/docs/aslr.txt"
    title: PaX Team, Address space layout randomization (design document)
    locator: the remarks that fork keeps the layout, that this makes brute force practical against forking daemons, and that ASLR should be paired with a response to crashes
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK, eternal war in memory, 2013 IEEE Symposium on Security and Privacy, pages 48-62"
    locator: the section on address space randomization and the attacks that weaken it (guessing and leaks)
---

ASLR derandomization by brute force is the attack class that recovers the secret offset of [address space layout randomization](/address-space-layout-randomization/) by repeated guessing, and the name of the study that measured it. Shacham, Page, Pfaff, Goh, Modadugu and Boneh (CCS 2004) took a network server on 32-bit x86 Linux with PaX ASLR and a non-executable stack. The server created a worker for each connection by fork, so every worker had the same layout as its parent, and a crashed worker was replaced by another with the same secret. The offset of the library area had 16 bits of randomness, and a guess could be tested by whether the worker crashed. The authors found the offset in 216 seconds on average and then ran a [return-to-libc](/return-to-libc-attack/) payload. Their lessons are about the defense: on 32-bit systems the entropy of ASLR is too small, raising it to 20 bits would only multiply the time by about 16, drawing a new layout for each worker adds only about one bit against this attack, and the real fix is a 64-bit address space. This page describes the threat model, the conditions, the history and the defenses, with an abstract model in place of any real target. It gives no procedure, parameters or details of software.

## In plain words

ASLR hides where a program's code is by moving it to one of many places at start-up. An attacker who needs that address must guess.

If a wrong guess crashes the program, and the program simply starts again, the attacker can guess again. If the program comes back at the same place every time, each wrong guess crosses one place off the list. With 16 bits of randomness the list has 65,536 places, which a fast network connection can work through in minutes.

The lesson is about how to build the defense. The secret must be large, a crash must not be free, and a program that restarts should not keep the old secret.

## When it applies

The class needs all of these conditions. Each defense removes one.

- **A hijack that needs one randomized address.** The attacker already has a memory error that sends control to a chosen address, as in [stack smashing](/stack-smashing/), and the payload works once one secret offset is known. A [shadow stack](/shadow-stack/) or [CFI](/control-flow-integrity/) removes the hijack, and then no guess helps.
- **An observable outcome per guess.** The attacker can tell whether a guess was right, for example from whether the service stays alive or drops the connection. This is the oracle of the attack.
- **The same secret across attempts.** The service restarts or forks workers without drawing a new layout, so wrong guesses add up. Without this, each attempt is a fresh blind guess.
- **Few enough candidates.** The number of possible offsets, $2^k$, is small enough to try at the rate the service allows. On 32-bit layouts $k$ is small; on 64-bit layouts it is much larger.
- **No response to crashes.** Nothing notices the stream of crashes and slows or stops the service. The PaX design document recommends exactly such a response.

## The template

The block names the stages of the published method at the level of the paper's abstract, with the defense that breaks each stage. It is not a procedure.

```pseudo id=main
DERANDOMIZATION-STAGES(service S whose layout has a secret offset δ with k bits of entropy)
L1  stage 1: have a hijack whose effect depends on a guess g of δ                   ▷ shadow stack, CFI: no hijack, nothing to guess for
L2  stage 2: observe whether the guess was right from ⟨outcome⟩ of S                  ▷ crash response: detect and limit failed attempts
L3  stage 3: repeat with a new guess while S keeps the same δ                         ▷ renewal: draw a new δ for each worker
L4  the expected number of repeats grows with 2^k                                     ▷ 64-bit layouts: k large enough to make L3 impractical
L5  stage 4: with δ known, run the payload of the hijack                              ▷ least privilege and system call filters limit its effect
```

**Walk-through.** Line L1 is the precondition: the attack does not create a hijack, it only supplies the address that an existing hijack needs. Line L2 is the oracle. Line L3 depends on the renewal rule of the defense: if the layout stays the same, the attacker never needs to repeat a value. Line L4 is the cost, which is where the entropy of the defense enters. Line L5 is the original attack, now with the address it needed.

**Example: an abstract model.** Replace the service by an abstract box $B$. It holds a secret $\delta$, uniform on $\{0, 1, \ldots, N - 1\}$ with $N = 2^k$, so its [min-entropy](/min-entropy/) is $k$ bits (the quantitative information flow pages measure it in bits, with $\log_2$). A query names a value $g$, and the box answers "right" if $g = \delta$ and "wrong" otherwise. Three defenses give three statements, all about the box and none about a real system.

- *No renewal.* After a "wrong" answer the box keeps $\delta$. An attacker with $q$ queries succeeds with probability at most $q/N$, by the [union bound](/union-bound/), with equality for distinct guesses. The expected number of queries to succeed is $(N + 1)/2$.
- *Renewal.* After each "wrong" answer the box draws a fresh $\delta$. Each query succeeds with probability $1/N$, so $q$ queries succeed with probability $1 - (1 - 1/N)^q \le q/N$, and the expected number of queries is $N$, by the [geometric distribution](/geometric-distribution/). Against this attacker, renewal only doubles the expected work, which is the "about one bit" of the 2004 paper.
- *A crash limit.* The box stops answering after $c$ "wrong" answers. The attacker then gets at most $c$ queries, so it succeeds with probability at most $c/N$, whatever the strategy. A limit turns an attack of expected cost $N/2$ into one with a small fixed chance.

The model also shows why renewal still matters. If one query can reveal part of $\delta$, for example whether some of its bits are right, then without renewal the attacker can recover the parts one at a time, and the cost is a sum over the parts rather than a product. Renewal breaks that, because the parts learned in one attempt belong to an old secret.

## Classic examples

- **The 2004 study.** Against a forking web server with PaX ASLR on 32-bit x86, the authors found the 16-bit offset of the library area in 216 seconds on average, and then ran a [return-to-libc](/return-to-libc-attack/) payload. The PaX design document had already noted that fork keeps the layout and that brute force against forking daemons is practical.
- **The same shape against canaries.** A [stack canary](/stack-canary/) is also a secret that a forking server shares with every worker. The same oracle (does the worker crash) lets an attacker learn it, which is why canaries should be renewed in each child, as the canary page discusses.
- **Learning more than one address.** Later work used the same crash oracle against servers that restart with the same layout to learn enough about an unknown binary to build [return-oriented programming](/return-oriented-programming/) attacks without a copy of the program (Bittau et al. 2014). The lesson is the same: a restart without renewal turns crashes into information.
- **Side channels as oracles.** For kernel ASLR, the oracle need not be a crash. The time of a memory access can reveal whether an address is mapped, so a local attacker learns the kernel base without any failed attempt; see [side-channel attacks](/side-channel-attack/).

## Variations

- **Guessing the stack or the heap.** Other regions have their own offsets and entropy. PaX gave 24 bits to the stack on i386, more than the 16 bits of the library area, so the library was the weaker target.
- **Reducing the entropy with many copies.** An attacker who can place many copies of the same data in memory needs to hit any one of them, which reduces the effective entropy. The PaX document notes that this is often impractical for the stack.
- **Partial knowledge.** A leak of some bits of an address, or a write that changes only the low bits of a pointer, reduces the number of candidates before any guess.

## Pitfalls

These are mistakes defenders make about the class.

- **Counting nominal bits.** The entropy that matters is the number of candidates the attacker must try for this region, after alignment, gaps and any leak. 16 bits is not enough.
- **Restarting without a new layout.** A fork server, a supervisor that restarts a crashed process from a saved image, or a pool of workers made from one parent all share one secret.
- **Ignoring crashes.** A stream of crashes of the same service is the signal of this attack. Log it, slow the restarts, and stop the service if it goes on.
- **Thinking renewal is enough.** Against a blind guesser, renewal adds about one bit. It is the entropy and the crash response that make the attack expensive.
- **Relying on ASLR alone.** Under a [shadow stack](/shadow-stack/) and [CFI](/control-flow-integrity/), a known address gives the attacker far less. ASLR is a layer on top of those checks.

## Exercises

1. In the abstract model, prove that an attacker with $q$ queries succeeds with probability at most $q/N$ without renewal, and exactly $1 - (1 - 1/N)^q$ with renewal. Show that the second is at most the first.
2. Compute the expected number of queries with and without renewal for $N = 2^{16}$ and $N = 2^{20}$. By what factor does each grow when $k$ goes from 16 to 20?
3. In the model with a crash limit of $c$ wrong answers, show that no strategy succeeds with probability greater than $c/N$. What value of $c$ keeps the success probability below $10^{-6}$ when $k = 28$?
4. Suppose the secret is $\delta = (\delta_1, \delta_2)$ with $k/2$ bits each, and one query can check $\delta_1$ alone. Without renewal, what is the expected number of queries to learn $\delta$? Why does renewal of the whole secret after each wrong answer remove the gain?

## References
