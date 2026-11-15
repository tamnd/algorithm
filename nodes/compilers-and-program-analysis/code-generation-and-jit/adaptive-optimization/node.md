---
tag: 5Z1RMA
kind: technique
slug: adaptive-optimization
name: Adaptive optimization
aliases:
- tiered compilation
- mixed-mode execution
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Starts in an interpreter or quick compiler and recompiles methods with more optimization as profiles show them to be hot.
prereqs: [just-in-time-compilation, profile-guided-optimization]
see_also: [type-feedback, on-stack-replacement, deoptimization, function-inlining, inline-caching, tracing-jit-compilation, ski-rental-problem, profile-guided-optimization]
sources:
  - paper: "Urs Hölzle, Adaptive optimization for SELF: reconciling high performance with exploratory programming, PhD thesis, Stanford University, 1994 (report STAN-CS-TR-94-1520)"
    locator: Chapter 5, Section 5.2 (adaptive recompilation and Figure 5-1), Section 5.3 (counters with exponential decay and the rate N(1 - 1/p)), Section 5.4 (the recompilation process and the choice of the method to recompile, with MinInvocations, TinySizeLimit and MaxVersion)
  - paper: doi:10.1145/353171.353175
    title: Matthew Arnold, Stephen Fink, David Grove, Michael Hind and Peter F. Sweeney, Adaptive optimization in the Jalapeño JVM, OOPSLA 2000, 47-65
    locator: the sampling profiler, the controller and its cost-benefit model that picks the optimization level with the least sum of compile time and expected future run time, and the multi-level recompilation
  - paper: doi:10.1109/JPROC.2004.840305
    title: Matthew Arnold, Stephen J. Fink, David Grove, Michael Hind and Peter F. Sweeney, A survey of adaptive optimization in virtual machines, Proceedings of the IEEE 93(2), 2005, 449-466
    locator: the sections on selective optimization, counters against sampling, and feedback-directed optimization
  - paper: doi:10.1145/178243.178478
    title: Urs Hölzle and David Ungar, Optimizing dynamically-dispatched calls with run-time type feedback, PLDI 1994, 326-336
    locator: the recompilation system of SELF-93, which recompiles hot methods with the type feedback that unoptimized code collected
  - paper: doi:10.1109/CGO.2003.1191549
    title: Stephen J. Fink and Feng Qian, Design, implementation and evaluation of adaptive recompilation with on-stack replacement, CGO 2003, 241-252
    locator: on-stack replacement as part of the adaptive system of the Jikes RVM, for long-running loops and for deferred compilation
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 14, Section 14.2.2 (compilation triggers) and Section 14.5 (levels of optimization, on-stack replacement and code cache management)
---

Adaptive optimization runs a program first in an interpreter or with a quick compiler, measures where the time goes, and recompiles the hot methods with more and more optimization. The program uses several *tiers* of code for the same method, from cheap code that is fast to make to good code that is slow to make, and each method moves up only when its profile shows that the better code will pay for itself. Hölzle built this for SELF in 1994, the Jalapeño virtual machine (later the Jikes RVM) gave it a cost-benefit controller in 2000, and Java and JavaScript engines use it today. The general idea of compiling at run time is on the page on [just-in-time compilation](/just-in-time-compilation/). This page is about the policy: which method to compile, when, and at which level.

## In plain words

Most programs spend almost all their time in a small part of their code. A good optimizing compiler is slow, so it is a waste to use it on code that runs only once.

So the system starts with a cheap way to run the code. It counts how often each method runs, or looks now and then at which method is running. When a method turns out to be busy, the system compiles it again with more care. A very busy method can go up again to the best compiler. The cheap code also notes what it sees, such as the types of values, and the better compiler uses those notes. If an assumption of the good code later turns out false, the method goes back down and can climb again.

## When it applies

- The language runs on a virtual machine that loads code at run time, so there is no complete program to compile ahead of time.
- The program runs long enough for a compilation to pay for itself, and its time is concentrated in a small set of methods.
- Start-up time matters, so compiling everything with the best compiler first is too slow.
- The best optimizations need run-time facts, such as receiver types for [inlining](/function-inlining/) through [type feedback](/type-feedback/), that only the lower tiers can collect.
- There is a way to move a running method between tiers: [deoptimization](/deoptimization/) to go down, and [on-stack replacement](/on-stack-replacement/) to go up in the middle of a long loop.

## The template

### Tiers, profile and controller

Number the tiers $0, 1, \dots, m$. Tier 0 is the interpreter or a baseline compiler that makes code at once and records a profile. Tier $j$ has a compile cost $C_j$ per unit of code and a speed $s_j$ relative to tier 0, with $C_0 = 0$, $s_0 = 1$, and both growing with $j$. The system has three parts:

1. A *profiler*. Either it keeps counters at method entries and loop back edges, or it samples the running method at a fixed time interval. The lower tiers also record receiver types and branch directions.
2. A *controller*. It looks at the profile and decides to recompile a method $u$ at a tier $j$.
3. A *compile queue* with one or more compiler threads. When a compilation ends, the new code goes into the code cache, and the next call of $u$ uses it.

The controller of Jalapeño picks the tier by a cost-benefit model. Let $T$ be an estimate of how long $u$ will still run at its current tier $i$. Then

$$\text{cost}(j) = C_j \cdot \text{size}(u) + T \cdot \frac{s_i}{s_j}, \qquad j \ge i,$$

with $C_i$ taken as 0 for the current tier, because that code exists already. The controller picks the $j$ with the least cost, and does nothing if that is $j = i$. The estimate $T$ comes from the samples of $u$ so far, on the idea that code that ran a long time will go on running a long time.

### Counters with decay

A counter that only grows will in the end trigger on every method, even one that runs once an hour. The SELF system divided all counters by a factor $p > 1$ at a fixed interval, so a counter measures a rate, not a total (Hölzle 1994, Section 5.3).

**Claim.** Let the threshold be $N$, let the counter start at 0, and let the method run $r$ times in each interval, after which the counter is divided by $p$. Then the counter reaches $N$ in some interval if and only if $r > N(1 - 1/p)$.

*Proof.* Let $c_t$ be the counter at the start of interval $t$, so $c_0 = 0$ and $c_{t+1} = (c_t + r)/p$. By induction, $c_t = r(1 - p^{-t})/(p - 1)$: this holds for $t = 0$, and $(c_t + r)/p = r\big((1 - p^{-t}) + (p - 1)\big)/\big(p(p - 1)\big) = r(1 - p^{-t-1})/(p - 1)$. The counter is largest at the end of an interval, just before the division, where it equals $c_t + r$. So the largest value in interval $t$ is
$$c_t + r = \frac{r p}{p - 1} - \frac{r p^{-t}}{p - 1}.$$
This is strictly less than $rp/(p - 1)$ for each $t$, and it tends to $rp/(p-1)$ as $t$ grows. If $r \le N(1 - 1/p)$, then $rp/(p - 1) \le N$, so the counter never reaches $N$. If $r > N(1 - 1/p)$, then $rp/(p - 1) > N$, so for $t$ large enough the value is at least $N$. $\square$

With $N = 10000$ and $p = 2$, the half-life is one interval and the critical rate is 5000 calls per interval. A method with 5000 calls per interval tends to 10000 but never reaches it. A method with 5001 calls per interval reaches it in interval 13, because $5001(2 - 2^{-t}) \ge 10000$ first holds at $t = 12$, counting from 0.

### Why switching tiers keeps the meaning

Each tier must be correct by itself: every version of $u$ in the code cache, run from the encoding of an interpreter state $\sigma$ that can enter $u$, has the same outcome as interpreting $u$ from $\sigma$, or it reaches an exit point whose map rebuilds the matching interpreter frames (see [just-in-time compilation](/just-in-time-compilation/) for this contract). Then the policy cannot change what the program does.

**Claim.** If every version that the controller installs has this property, then each run of the program under adaptive optimization has the same observable behavior as the run in the interpreter alone, for any choice of when and what to compile.

*Proof.* Take a finite prefix of the run, and induct on the depth of nesting of the calls that finish inside it. A call of $u$ starts in some version $K$ chosen at the time of the call, from a state that encodes the same interpreter state $\sigma$ as in the interpreted run, by the induction hypothesis on the steps before it. A frame that runs $K$ keeps running $K$ even if the controller installs a new version during the call, because the system frees old code only when no frame uses it. The inner calls that $K$ makes finish inside the prefix and are nested less deeply, so by the induction hypothesis each returns the value and heap that the interpreter gives. Between them, $K$ is equivalent to the interpreter on $u$, or it exits through a map that gives the exact interpreter state, from which the interpreter continues. So the call ends in the state that interpreting $u$ from $\sigma$ gives, and the prefix of the run is the same step for step at each call boundary. Since this holds for every finite prefix, it holds for the whole run, also when the run does not end. $\square$

The claim shows why tiers do not need to know about each other. The only shared contract is the one at entry and at exit points.

## Classic examples

- **SELF-93.** Methods are first compiled by a fast compiler that makes unoptimized code with counters and [polymorphic inline caches](/polymorphic-inline-cache/). When a counter goes over its limit, the system does not just recompile that method. It walks up the stack to choose a caller to recompile, so that the hot method can be inlined into it with the receiver types from the caches. The thesis gives MinInvocations = 10000 as the counter limit, prefers a caller when the method is smaller than TinySizeLimit = 50 instructions, and stops after MaxVersion = 7 versions of the same method (Hölzle 1994, Section 5.4).
- **Jalapeño and the Jikes RVM.** The system has a baseline compiler and an optimizing compiler with three levels. A timer samples the running methods, and the controller uses the cost-benefit model above to pick a level, with a separate thread for the compiler. Fink and Qian added [on-stack replacement](/on-stack-replacement/) for methods that are stuck in a long loop.
- **Java HotSpot and JavaScript engines.** They use an interpreter, a quick compiler and an optimizing compiler, with counters at method entries and at back edges, and they fall back to a lower tier through [deoptimization](/deoptimization/). The survey of Arnold and others describes these designs.

As a worked example of the cost-benefit model, take a method of size 1 with tiers $(C_1, s_1) = (5, 2)$ and $(C_2, s_2) = (30, 3)$, in milliseconds, and a method now at tier 0. These numbers are made up to show the arithmetic.

| estimate $T$ | stay at tier 0 | tier 1 | tier 2 | choice |
|---|---|---|---|---|
| 100 ms | 100 | 5 + 50 = 55 | 30 + 33.3 = 63.3 | tier 1 |
| 1000 ms | 1000 | 5 + 500 = 505 | 30 + 333.3 = 363.3 | tier 2 |

A method that is expected to run longer can pay for a more expensive compiler.

## Variations

- **Counters or sampling.** Counters are exact and cheap to test in compiled code, but they cost a little on every call. Sampling costs almost nothing and finds where time goes, not how many calls there were, but it needs enough samples to be reliable.
- **Background compilation.** The program keeps running in the old tier while a compiler thread works. A method that becomes hot while the queue is full waits.
- **A profiling tier.** Some systems add a middle tier that is compiled code but still collects types and branch counts, so the top tier has a good profile without the cost of the interpreter.
- **Going down.** When an assumption fails, [deoptimization](/deoptimization/) returns the method to a lower tier. The method can then climb again with the new profile.
- **Code cache eviction.** When the cache is full, cold code is thrown away and recompiled when needed again, as already in the Smalltalk-80 system of Deutsch and Schiffman.
- **With ahead-of-time code.** A system can start from code compiled before the run and use adaptive recompilation only for hot methods.

## Pitfalls

- **A method that is called once but loops for a long time.** Counters at method entry never trigger. Count loop back edges as well, and switch the running frame to new code by [on-stack replacement](/on-stack-replacement/).
- **Counters without decay.** Without decay, every method that runs often enough over a long run is compiled at last, even when it is not hot. With decay, the threshold is a rate, as in the claim above.
- **Deoptimization loops.** If an assumption fails again and again, the method goes down, climbs with the same profile, and fails again. Count the deoptimizations per method and compile without the failed assumption, or stop at a limit such as the MaxVersion of SELF.
- **Profiles from the start of the run.** The first phase of a program can differ from its main phase. Code optimized for the start-up phase can then be wrong in its guesses for the rest of the run.
- **Free code too early.** Old code can still be running in a frame on some stack. Free it only when no frame uses it, or move the frames first.
- **Speed claims.** The gain of adaptive optimization depends on the program, the machine and the tuning. Report it as a measurement with its setting, not as a property of the method.

## Exercises

1. In the claim on counters with decay, take $N = 1000$ and $p = 4$. What is the critical rate, and in which interval does a method with 800 calls per interval reach the threshold?
2. Show that if the controller of Jalapeño always takes $T$ equal to the time that $u$ has run so far, then a method is compiled at tier 1 once its run time so far exceeds $C_1 s_1 / (s_1 - 1)$, for a method of size 1 at tier 0 with only one higher tier. Relate this to the break-even rule of the [ski rental problem](/ski-rental-problem/).
3. Give a program for which a profile from the first phase leads the optimizing tier to a guard that fails in every later call. What should the system do after the second failure?
4. Explain why the proof that tier switching keeps the meaning needs the rule that old code is freed only when no frame uses it. Give a run that goes wrong without the rule.
5. SELF does not recompile the method whose counter overflowed, but a caller of it. Why does this give better code when the hot method is small?

## References
