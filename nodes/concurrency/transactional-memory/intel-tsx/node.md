---
tag: VR9D01
kind: concept
slug: intel-tsx
name: Intel TSX
aliases:
- TSX
- RTM
- Restricted Transactional Memory
- HLE
- Hardware Lock Elision
area: concurrency/transactional-memory
level: advanced
summary: "Intel's best-effort hardware transactional memory for x86: RTM (XBEGIN, XEND, XABORT, XTEST) and the HLE lock prefixes. Errata and the TAA attack led microcode to disable it on many processors."
prereqs: [best-effort-htm]
see_also: [transactional-lock-elision, hardware-transactional-memory, hybrid-transactional-memory, herlihy-moss-htm, spin-lock, transaction-abort, nested-transactions, stamp-benchmark-suite]
sources:
  - book: "Intel 64 and IA-32 Architectures Software Developer's Manual, Volume 1, Chapter 16, Programming with Intel Transactional Synchronization Extensions"
    locator: HLE with the XACQUIRE and XRELEASE prefixes, RTM with XBEGIN, XEND, XABORT and XTEST, the abort status in EAX (Table 16-1), nesting, and the causes of aborts
  - book: "Intel 64 and IA-32 Architectures Optimization Reference Manual, the chapter Intel TSX Recommendations"
    locator: guidance on retry policies, lock elision, and the causes of aborts on real processors
  - url: https://www.intel.com/content/www/us/en/content-details/604224/performance-monitoring-impact-of-intel-transactional-synchronization-extension-memory-ordering-issue.html
    title: "Intel, Performance Monitoring Impact of Intel Transactional Synchronization Extension Memory Ordering Issue, document 604224, revision 1.5, June 2023"
    locator: the October 2018 microcode that disabled the HLE prefix and forced RTM to abort in SGX and SMM; the 2021.1 update that disables TSX by default on the listed processors; the TSX_FORCE_ABORT MSR and the CPUID bits RTM_ALWAYS_ABORT and RTM_FORCE_ABORT
  - url: https://docs.kernel.org/admin-guide/hw-vuln/tsx_async_abort.html
    title: "The Linux kernel documentation, TAA, TSX Asynchronous Abort"
    locator: CVE-2019-11135, the processors it affects, the IA32_TSX_CTRL MSR with its RTM_DISABLE and TSX_CPUID_CLEAR bits, and the tsx= kernel option
  - paper: doi:10.1145/2503210.2503232
    title: "Richard M. Yoo, Christopher J. Hughes, Konrad Lai and Ravi Rajwar, Performance evaluation of Intel transactional synchronization extensions for high-performance computing, SC 2013"
    locator: measurements of RTM on Haswell with STAMP and other workloads, and the lock elision retry policy used there
  - paper: doi:10.1145/2576793
    title: "Andi Kleen, Scaling existing lock-based applications with lock elision, Communications of the ACM 57(3), 2014, pp. 52 to 56"
    locator: lock elision with TSX in the GNU C library and the lemming effect
---

**Intel Transactional Synchronization Extensions** (TSX) is the [hardware transactional memory](/hardware-transactional-memory/) of Intel x86 processors, first shipped in the Haswell processors of 2013. It has two interfaces: **Restricted Transactional Memory** (RTM), four instructions that start, end, abort and test a transaction, and **Hardware Lock Elision** (HLE), two instruction prefixes that let old lock code run as transactions. TSX is a [best-effort HTM](/best-effort-htm/): a transaction may always abort, and software must provide a fallback path. Since 2014, errata and the TAA side-channel attack have led Intel to disable TSX by microcode on many processors and to remove HLE.

## In plain words

TSX lets a program say "do these memory operations all at once, or not at all". The processor runs them, keeps the new values in its cache, and watches if any other core touches the same cache lines. If none does, the end instruction makes all the changes visible together. If one does, or if the cache runs out of room, or if something like an interrupt happens, the processor throws the changes away and jumps to a place that the program gave at the start, with a code that says roughly why.

The program must always have another way to do the work, usually a lock, because nothing guarantees that the transaction will ever succeed.

HLE did the same for an existing lock without new instructions, but Intel has removed it.

## The idea

**RTM.** Four instructions.

| instruction | effect |
|---|---|
| `XBEGIN rel` | start a transaction; `rel` gives the address of the fallback code |
| `XEND` | commit: make all writes of the transaction visible at once |
| `XABORT imm8` | abort explicitly; the 8-bit value goes into the abort status |
| `XTEST` | set the zero flag to say whether the processor is in a transaction (RTM or HLE) |

On an abort, the processor discards all transactional writes, restores the registers to their state at `XBEGIN`, puts a status word in EAX and jumps to the fallback address. The bits of the status word (SDM Volume 1, Table 16-1):

| bit | meaning |
|---|---|
| 0 | the abort came from `XABORT` |
| 1 | the transaction may succeed on a retry (always clear if bit 0 is set) |
| 2 | another logical processor conflicted with a memory address of the transaction |
| 3 | an internal buffer overflowed |
| 4 | a debug breakpoint was hit |
| 5 | the abort happened in a nested transaction |
| 31 to 24 | the argument of `XABORT`, if bit 0 is set |

The status can be 0, for example after an abort caused by an instruction such as CPUID that always aborts. Compilers provide the instructions as intrinsics. In C with GCC or Clang, the usual pattern, with a lock as the fallback, is:

```c
#include <immintrin.h>

void increment(volatile int *lock, long *counter) {
    for (int tries = 0; tries < 3; tries++) {
        while (*lock != 0)                 /* wait outside the transaction */
            _mm_pause();
        unsigned status = _xbegin();
        if (status == _XBEGIN_STARTED) {
            if (*lock != 0)                /* the lock joins the read set */
                _xabort(0xff);
            (*counter)++;
            _xend();
            return;
        }
        if (!(status & _XABORT_RETRY) &&
            !((status & _XABORT_EXPLICIT) && _XABORT_CODE(status) == 0xff))
            break;                         /* a retry will not help */
    }
    while (__sync_lock_test_and_set(lock, 1))
        while (*lock != 0)
            _mm_pause();
    (*counter)++;
    __sync_lock_release(lock);
}
```

This is [transactional lock elision](/transactional-lock-elision/) with RTM. The read of the lock inside the transaction is required: it is what makes the lock holder abort every transaction. The C code is for reading; it is not tested on this site, and on most current machines `_xbegin` aborts at once (see below), so the code takes the lock every time.

**Conflict detection.** TSX tracks the read set and the write set at the granularity of cache lines and finds conflicts through the cache coherence protocol. The manual does not fix a policy, but measurements show that the transaction that receives the conflicting request aborts, so the requester wins. Ordinary accesses by other cores count as well, so TSX gives strong isolation (see [strong atomicity](/strong-atomicity/)). Because it works on lines, two transactions that write different variables on the same line conflict (false sharing).

**Capacity and other aborts.** The sizes of the read and write sets are not part of the architecture. In the first implementations the write set was held in the first-level data cache, so a transaction could abort on capacity even if it was small, when it wrote more lines that map to one set of that cache than the set can hold. Many events abort a transaction: interrupts, exceptions (which are then not delivered), some instructions, and changes to some control state. The manual lists them; the abort status gives only a summary.

**Nesting.** RTM supports flat nesting: an `XBEGIN` inside a transaction increments a nesting count, the inner `XEND` only decrements it, and an abort anywhere aborts the outermost transaction (see [nested transactions](/nested-transactions/)). The depth is limited by an implementation constant.

**HLE.** The prefix `XACQUIRE` (F2H) goes on the locked instruction that takes a lock, and `XRELEASE` (F3H) on the instruction that releases it. A processor without TSX ignores these prefixes, so the same binary runs everywhere. With HLE, the processor does not write the lock: it adds the lock line to the read set and starts a transaction, and the thread itself sees the lock as taken. The release must write back the value that the lock had before the acquire. On an abort, the processor goes back to the `XACQUIRE` instruction and runs it again without elision, so it really takes the lock. This is the speculative lock elision of Rajwar and Goodman (2001) in a commercial processor.

## Examples

**History of the feature.** The table lists the main events; each row names the processors that the source names, and no more.

| date | event |
|---|---|
| 2012 | Intel publishes the TSX specification |
| June 2013 | first processors with TSX (Haswell) |
| August 2014 | a TSX erratum is found; a microcode update disables TSX on Haswell, Haswell-E and Haswell-EP, and on early Broadwell processors |
| October 2018 | for the processors of Intel document 604224 (Xeon Scalable, and some Xeon E3 v5 and v6 and 6th to 8th generation Core processors), a microcode update for the "TSX memory ordering issue" disables the HLE prefix and forces RTM to abort in SGX enclaves and System Management Mode |
| November 2019 | the TSX Asynchronous Abort attack (TAA, CVE-2019-11135): on processors that support TSX and are not marked TAA_NO, a transaction that aborts can leak data from internal buffers through a side channel. On processors that are not affected by the older MDS attacks, new microcode adds the IA32_TSX_CTRL register, which can make every RTM transaction abort and hide TSX in CPUID; operating systems use it to turn TSX off |
| June 2021 | the 2021.1 microcode for the Skylake, Kaby Lake, Coffee Lake and Whiskey Lake processors of document 604224 makes all RTM transactions abort by default; CPUID bit 7.EDX[11] (RTM_ALWAYS_ABORT) tells software that this is so |
| later | the SDM says that HLE has been removed from Intel products released in 2019 and later; RTM is not documented as removed, but many later processors do not support it |

The unsupported "software development" mode of the 2021 update can turn RTM on again, but Intel warns that RTM may then have memory-ordering correctness issues and must not be used in production.

**Checking at run time.** Software tests CPUID leaf 7, EBX bit 11 for RTM and bit 4 for HLE. After the 2021 update, these bits may still be set while every transaction aborts; RTM_ALWAYS_ABORT or an operating system that clears the bits tells the truth. A fallback path that is always correct is the only safe choice, and it is required by the manual anyway.

## Where it is used

- **Lock elision in libraries.** The GNU C library has RTM-based elision of its mutexes, and Java virtual machines and databases have used RTM for locks. See [transactional lock elision](/transactional-lock-elision/).
- **Research.** Many papers on hardware TM, [hybrid TM](/hybrid-transactional-memory/), and concurrent data structures measure on TSX. Yoo, Hughes, Lai and Rajwar evaluated it on the [STAMP](/stamp-benchmark-suite/) benchmarks and on HPC workloads in 2013.
- **Side channels.** Because an abort is fast, silent and leaves no fault, TSX was used in attacks to probe memory and to build timers, and TAA itself used it.

Because TSX is disabled or missing on many deployed machines, software that uses it must work, with good speed, when every transaction aborts.

## References
