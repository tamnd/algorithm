---
tag: F21NTX
kind: technique
slug: spectre-attack
name: Spectre attack
aliases:
- speculative execution attack
- Spectre
area: security-and-privacy/side-channel-attacks
level: advanced
summary: A transient execution attack class in which a mispredicted branch makes the victim run a wrong path that reads a secret and leaves a cache trace after the rollback.
prereqs: [flush-and-reload, side-channel-attack]
see_also: [meltdown-attack, flush-and-reload, prime-and-probe, constant-time-programming, constant-time-verification, software-fault-isolation, control-flow-integrity, return-oriented-programming]
sources:
  - paper: "Paul Kocher, Jann Horn, Anders Fogh, Daniel Genkin, Daniel Gruss, Werner Haas, Mike Hamburg, Moritz Lipp, Stefan Mangard, Thomas Prescher, Michael Schwarz and Yuval Yarom, Spectre attacks, exploiting speculative execution, IEEE Symposium on Security and Privacy 2019, pages 1-19"
    locator: the attack overview, the variants with conditional branches and with indirect branches, and the section on mitigation options
  - paper: "Claudio Canella, Jo Van Bulck, Michael Schwarz, Moritz Lipp, Benjamin von Berg, Philipp Ortner, Frank Piessens, Dmitry Evtyushkin and Daniel Gruss, A systematic evaluation of transient execution attacks and defenses, 28th USENIX Security Symposium, 2019, pages 249-266, arXiv:1811.05441"
    locator: the tree of Spectre-type and Meltdown-type attacks, and the table of defenses with the attacks each one stops
  - paper: "Moritz Lipp, Michael Schwarz, Daniel Gruss, Thomas Prescher, Werner Haas, Anders Fogh, Jann Horn, Stefan Mangard, Paul Kocher, Daniel Genkin, Yuval Yarom and Mike Hamburg, Meltdown, reading kernel memory from user space, 27th USENIX Security Symposium, 2018, pages 973-990"
    locator: the discussion of the difference between Meltdown and Spectre
  - paper: "José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupressoir and Michael Emmi, Verifying constant-time implementations, 25th USENIX Security Symposium, 2016, pages 53-70"
    locator: the constant-time policy, which describes only the paths that a program really takes
---

The Spectre attack is a class of transient execution attacks in which the processor predicts the outcome of a branch, runs the predicted path before it knows the outcome, and later rolls the path back. If the prediction is wrong, the victim has run code that it should not have run, and that code may have read a secret that the victim may read and left a trace of it in the cache. A cache channel such as [Flush+Reload](/flush-and-reload/) then carries the trace to the observer. Kocher et al. (2019) showed that the class affects processors of many vendors, and that it reaches across process and sandbox boundaries. Unlike the [Meltdown attack](/meltdown-attack/), Spectre needs no fault: the victim reads its own memory, on a path that its own checks should have blocked.

## In plain words

To save time, a processor guesses which way a branch will go and starts that work at once. If the guess was wrong, it undoes the work and takes the other way. The program gives the right answer in every case.

The undo is not complete. Work on the wrong path can bring memory into the cache, and the cache keeps it. If the wrong path read a secret and then used it to choose which memory to touch, the cache now holds a trace of the secret. A program that watches the cache can learn it. The victim's code was correct; the checks in it ran, but too late.

## When it applies

### Threat model

The victim is a program that has a secret in its own memory, such as a browser process, the kernel or a sandbox that runs untrusted code. The observer can run code on the same machine, or can send inputs to the victim. He sees only the architectural results of his own program and the effect of shared state such as the cache on his own accesses. The defenses below are stated against this observer.

### Conditions

1. **PREDICT.** The processor runs a predicted path of a branch, an indirect jump or a return before the outcome is known.
2. **STEER.** The prediction can be wrong in a way that the observer causes or can wait for, because the predictor state is shared or depends on inputs he controls.
3. **ACCESS.** On the wrong path, the victim reads a secret that it may read architecturally.
4. **ENCODE.** A later instruction on the wrong path changes state that the rollback keeps, such as the cache, as a function of the secret.
5. **CHANNEL.** The observer can read that state.

### What removes a condition

| defense | condition it removes | cost |
|---|---|---|
| a speculation barrier after a check | 1, at that place | the processor waits at every barrier; placing them by hand misses places |
| masking of indices or of loaded values on the wrong path (speculative load hardening) | 3 or 4, for loads that the compiler protects | extra instructions on many loads |
| retpoline for indirect jumps | 2, for indirect jumps | each indirect jump becomes slower |
| flushing or partitioning predictor state across trust domains (microcode and new hardware) | 2, across domains | work on each switch of domain |
| process isolation, for example one process for each site in a browser | 3: the secret is not in the address space of the victim that runs the observer's code | more memory and more processes |
| coarse timers in browsers | 5, partly (heuristic) | the channel can be rebuilt with a counting thread |

Constant-time code does not stop Spectre by itself. The [constant-time policy](/constant-time-programming/) is about the paths that the program really takes, and Spectre leaks on a path that it does not take. A program that is proved constant time by [constant-time verification](/constant-time-verification/) can still leak on a wrong path. Stronger policies that include the wrong paths have been defined and checked, under the name speculative constant time.

## The template

The block is the shape of the class: each line is a condition, and the comment names the defense that removes it. It is not a recipe and it names no code of any real program.

```pseudo id=main
SPECTRE-CLASS(processor P, victim V)
L1  require PREDICT: P runs a predicted path before the outcome is known          ▷ removed locally by a speculation barrier
L2  require STEER: the prediction can be wrong in a way the observer causes       ▷ hole PREDICTOR: removed across domains by predictor isolation, for indirect jumps by retpoline
L3  require ACCESS: on the wrong path, V reads a secret it may read              ▷ removed by process isolation, or by masking on the wrong path
L4  require ENCODE: a later wrong-path instruction changes kept state by the secret ▷ hole STATE: the cache, or another shared structure
L5  require CHANNEL: the observer can read that state                            ▷ hole CHANNEL: Flush+Reload or Prime+Probe
L6  if every condition holds then the observer learns a function of the secret
```

### An abstract model

Take an abstract machine that, at a branch with guard $g$, may first run a few steps of the path that $g$ does not choose and then roll the registers back. Its cache is a set of lines and the rollback keeps it. Let the wrong path read a secret value $v$ and use a line $f(v)$, for a made-up function $f$. The observer sees the set of lines.

| machine | what the observer sees after the rollback |
|---|---|
| wrong path runs, no defense | the line $f(v)$, which depends on $v$ |
| a barrier before the wrong path | no wrong-path line |
| the wrong path masks its address to a public value $c$ when $g$ is false | the line $f(c)$, for every $v$ |

**Claim (theorem, in the abstract model).** If every load on a wrong path uses an address that does not depend on the secret, the cache after the rollback is the same for every secret. *Proof.* The wrong path changes the cache only by its loads. If their addresses do not depend on the secret, the set of lines they add is the same for every secret, and the lines from the correct path are the same by the constant-time policy of that path. This is the reason that speculative load hardening works in the model; it does not cover other shared state, such as predictors.

### Spectre and Meltdown

Both classes use transient work and a covert channel. Meltdown-type attacks read data that the observer may not read, after a fault; the defense is in the operating system and the processor. Spectre-type attacks make the victim read its own data on a wrong path; the defense is in the victim's code, the compiler, the browser or the processor. Canella et al. (2019) give a tree of both classes and a table of which defense stops which variant.

## Classic examples

- **Spectre, 2018 (measurement).** Kocher et al. made the victim run a wrong path past a bounds check, and, in a second variant, past an indirect jump whose target the predictor guessed. They showed it on processors of several vendors, from native code and from JavaScript in a browser. The browsers answered with coarse timers, removed shared memory buffers for a time, and moved to a separate process for each site.
- **Retpoline and predictor isolation, 2018.** Compilers replaced indirect jumps with a construct that sends the prediction to a harmless loop, and processor vendors added controls that keep predictor state from crossing trust domains. These stop the indirect jump variant, which looks like [return-oriented programming](/return-oriented-programming/) on the wrong path.
- **Return and store variants, 2018.** Later work used the prediction of returns and the prediction that a load does not depend on an earlier store. Each needed its own defense.
- **NetSpectre, 2019.** A variant with an observer that only sends network packets and measures the answers, which showed that condition 5 does not need local code.
- **The channel.** Each variant ends with a channel such as [Flush+Reload](/flush-and-reload/) or [Prime+Probe](/prime-and-probe/).

## Variations

- **By the predictor.** Conditional branches, indirect jumps, returns and memory dependence each have their own predictor and their own variant.
- **By the place of the observer.** In the same process (a sandbox in a browser), in another process, in the kernel or over a network.
- **By the channel.** The cache is the common channel, but any state that survives the rollback can carry the trace.
- **Hardware fixes.** New processors limit what a wrong path can do, but the predictor itself stays, so the class is not removed by one change.

## Pitfalls

- **Trusting a check.** A bounds check stops the architectural read, not the transient one. This is the lesson of the first variant.
- **Assuming constant-time code is safe.** The constant-time policy covers only real paths. Use a speculative policy or add barriers for code that holds keys.
- **Placing barriers by hand.** Barriers in some places and not in others leave gaps. Compilers can place them, or mask loads, for a whole program.
- **Linking the wrong idea.** In distributed computing, speculative execution means running backup copies of slow tasks. That idea has nothing to do with this class.
- **Treating a sandbox as an isolation boundary.** Code in the same process as a secret can reach it on a wrong path, even when [software fault isolation](/software-fault-isolation/) or a language check stops every real access. A process boundary keeps the secret out of reach.

## References
