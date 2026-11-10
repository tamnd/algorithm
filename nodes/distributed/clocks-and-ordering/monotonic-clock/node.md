---
tag: E8CEWW
kind: concept
slug: monotonic-clock
name: Monotonic clock
aliases:
- monotonic time
area: distributed/clocks-and-ordering
level: intro
summary: A clock whose readings never decrease and that nobody can set, such as POSIX CLOCK_MONOTONIC. Use it to measure intervals and timeouts; use the wall clock only for dates.
prereqs: [clock-drift]
see_also: [clock-drift, clock-skew, ntp, leader-lease, truetime, hybrid-logical-clocks, lamport-clocks]
sources:
  - url: https://pubs.opengroup.org/onlinepubs/9799919799/functions/clock_getres.html
    title: The Open Group Base Specifications Issue 8, IEEE Std 1003.1-2024, clock_getres, clock_gettime, clock_settime
    locator: the description of CLOCK_REALTIME and CLOCK_MONOTONIC, and the effect of setting CLOCK_REALTIME on absolute and relative time services
  - url: https://man7.org/linux/man-pages/man2/clock_gettime.2.html
    title: The Linux man-pages project, clock_gettime(2)
    locator: the entries for CLOCK_REALTIME, CLOCK_MONOTONIC, CLOCK_MONOTONIC_RAW and CLOCK_BOOTTIME
  - url: https://www.rfc-editor.org/rfc/rfc5905
    title: David Mills, Jim Martin, Jack Burbank and William Kasch, RFC 5905, Network Time Protocol Version 4, 2010
    locator: Section 11.3, the clock discipline (step above STEPT = 0.125 s, slew below it, PANICT = 1000 s)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 8, Unreliable Clocks (time-of-day clocks versus monotonic clocks)
---

A *monotonic clock* is a clock whose readings never decrease and that no program or administrator can set. POSIX names it `CLOCK_MONOTONIC`, and the wall clock `CLOCK_REALTIME`. The wall clock tells the date, but it can jump back or forward when [NTP](/ntp/) or a person corrects it. So a program must measure intervals, timeouts and [leases](/leader-lease/) with the monotonic clock.

## In plain words

A computer has two kinds of clock. The wall clock shows the date and the time of day. The system corrects it from time to time, and a correction can move it back. The monotonic clock counts the time since some fixed point, for example the last boot. Nobody can set it, and it never goes back.

If you measure how long a task takes with the wall clock, and a correction moves the wall clock back during the task, you can get a negative duration. A timeout can fire much too early or much too late. The monotonic clock does not have this problem. Its readings mean nothing as a date, and two computers do not share them. Use it only to measure time on one machine.

## The idea

**Two clocks in POSIX.** POSIX.1-2024 defines both clocks for `clock_gettime`. `CLOCK_REALTIME` "represents the clock measuring real time for the system", and `clock_settime` can set it. `CLOCK_MONOTONIC` gives "the amount of time (in seconds and nanoseconds) since an unspecified point in the past", and "cannot be set via clock_settime()". When `CLOCK_REALTIME` is set, POSIX requires that absolute timers use the new value, and that relative sleeps and timers still end when the requested interval has passed.

**Stepping and slewing.** A clock correction can take two forms.

- A *step* sets the clock to a new value at once. A step back makes the wall clock read a value that it already read before.
- A *slew* changes the rate of the clock for some time, so that the error goes away slowly. The clock stays increasing during a slew. At a slew rate of 500 ppm, a correction of 0.1 s takes $0.1 / (500 \cdot 10^{-6}) = 200$ s.

The NTP clock discipline in RFC 5905 slews offsets below STEPT = 0.125 s and steps larger ones. It gives up on offsets above PANICT = 1000 s and asks for help from an operator.

**What the monotonic clock still does.** A monotonic clock is not a perfect clock. It still has [clock drift](/clock-drift/). On Linux, `CLOCK_MONOTONIC` "is not affected by discontinuous jumps in the system time" but "is affected by frequency adjustments", so NTP can slew it. `CLOCK_MONOTONIC_RAW` is the raw hardware rate with no adjustment. Neither of them counts the time while the system is suspended; `CLOCK_BOOTTIME` does. These three are Linux additions, not POSIX.

**Why intervals must use it.** Let $C$ be a clock and let a task run from real time $s$ to real time $t$. The measured duration is $C(t) - C(s)$. If $C$ is $\rho$-bounded and is never stepped, then $(1-\rho)(t-s) \le C(t) - C(s) \le (1+\rho)(t-s)$, so the error is at most $\rho(t - s)$. If $C$ can be stepped by $\delta$ between $s$ and $t$, the measurement is off by $\delta$, which can be larger than the whole interval. Only a monotonic clock keeps the first bound for every interval.

**Readings mean nothing across machines.** The start point of `CLOCK_MONOTONIC` is unspecified and differs between machines and between boots. So a monotonic reading must never be sent to another process as a time. To order events between machines, use [Lamport clocks](/lamport-clocks/) or [hybrid logical clocks](/hybrid-logical-clocks/). To bound real time across machines, use an interval with an error bound, as [TrueTime](/truetime/) does.

## Examples

- **A negative duration.** A program reads the wall clock as 12:00:00.000 and starts a task that takes 0.2 s. During the task, NTP steps the wall clock back by 0.3 s. At the end the wall clock reads 11:59:59.900, so the program computes $-0.1$ s. The monotonic clock gives 0.2 s, with an error of at most $\rho \cdot 0.2$ s.
- **A timeout.** A client waits 5 s for a reply. If it computes the deadline from the wall clock and the wall clock jumps forward by 10 s, the timeout fires at once. If the wall clock jumps back by 10 s, the client waits 15 s.
- **A lease.** A leader holds a [lease](/leader-lease/) for 10 s. It must stop acting as leader when 10 s have passed on its own monotonic clock, minus a margin for drift. A wall clock step could make it believe that the lease is still valid after another leader took over.
- **Library calls.** Python has `time.monotonic()` next to `time.time()`. Java has `System.nanoTime()` next to `System.currentTimeMillis()`. The first call of each pair is the one to use for durations.

## Where it is used

- Timeouts, retries and heartbeats in distributed systems, and the failure detectors built on them.
- Leases and leader election with leases, where a wrong interval breaks safety.
- Rate limiters, benchmarks and profilers.
- [Cristian's algorithm](/cristian-algorithm/) and [NTP](/ntp/) measure the round trip time with a local clock. A step of that clock during the exchange corrupts the measurement.

## References
