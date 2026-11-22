---
tag: N3WHQ2
kind: concept
slug: buffer-overflow
name: Buffer overflow
aliases:
- buffer overrun
- out-of-bounds access
area: security-and-privacy/memory-safety-defenses
level: intro
summary: An access past the end or before the start of a buffer, which reads or overwrites nearby memory that belongs to other data.
prereqs: [memory-safety]
see_also: [memory-safety, stack-smashing, stack-canary, buffer-overrun-detection-by-range-analysis, addresssanitizer, fuzz-testing, data-execution-prevention, format-string-vulnerability]
sources:
  - paper: "Laszlo Szekeres, Mathias Payer, Tao Wei and Dawn Song, SoK: Eternal war in memory, IEEE Symposium on Security and Privacy 2013, pages 48-62"
    locator: "the general model of memory corruption, and the survey of defenses against spatial errors"
  - paper: "Richard W. M. Jones and Paul H. J. Kelly, Backwards-compatible bounds checking for arrays and pointers in C programs, AADEBUG 1997, pages 13-25"
    locator: the rules for pointer arithmetic in C and the run-time check that a derived pointer stays in its object
  - url: "https://cwe.mitre.org/data/definitions/119.html"
    title: "MITRE, CWE-119: Improper restriction of operations within the bounds of a memory buffer"
    locator: the description of the weakness and its child entries for out-of-bounds reads and writes
---

A buffer overflow is an access to memory outside the buffer that the program meant to use: past its end, or before its start. It is the most common [spatial memory safety](/memory-safety/) error. Languages that check array bounds turn it into an error that stops the program. C and C++ do not check, so the access goes through and reads or changes whatever is stored next to the buffer. The effect depends on that neighboring data and can be a wrong result, a crash, a leak of secret data, or a change in what the program does next.

## In plain words

A buffer is a row of boxes set aside for one piece of data, for example the characters of a name. The program puts items into the boxes one after another.

If the program does not count the boxes, a long name keeps going past the last box. The extra items land in the boxes after the row, which hold other data. That data is now wrong, and the program does not know it.

Reading works the same way. A program that reads too far gets data that is not part of the buffer, which can include secrets.

The fix is to check the count before each access, or to use a language or a tool that does this for you.

## The idea

A buffer is an object of $n$ elements at addresses $b$ to $b + n - 1$ (in units of the element size). An access at index $i$ is in bounds if $0 \le i < n$. A *buffer overflow* is an access with $i \ge n$; an access with $i < 0$ is sometimes called an *underflow*. Both are spatial errors in the sense of [memory safety](/memory-safety/): the pointer was derived from the buffer, but the access is not inside it.

Common causes:

- **A wrong count.** A copy uses the size of the source, not of the destination, or a loop runs one step too far, the off-by-one error.
- **An unchecked length from input.** The program trusts a length field in a message or a file.
- **Integer overflow in a size.** A size computed as a product or a sum wraps around and becomes small, so the buffer is allocated too short for the data later written into it.
- **A missing terminator.** A function that reads up to a terminating zero byte keeps reading when the zero is not there.

Where the buffer lives decides what the overflow can reach. A buffer on the stack lies next to other locals and to the data that the function uses to return; the special case is [stack smashing](/stack-smashing/). A buffer on the heap lies next to other heap objects and the data of the allocator. A global buffer lies next to other globals.

Defenses work at three points:

- **Before the run.** Static analysis, such as [buffer overrun detection by range analysis](/buffer-overrun-detection-by-range-analysis/), proves that indices stay in range or reports where they may not.
- **During testing.** [Fuzz testing](/fuzz-testing/) with a detector such as [AddressSanitizer](/addresssanitizer/) finds overflows on random inputs.
- **During the run.** Bounds checks, as in [fat pointers](/fat-pointer/), [baggy bounds checking](/baggy-bounds-checking/), [SoftBound](/softbound/) or the [CHERI capability model](/cheri-capability-model/), stop the access. Other defenses do not stop the overflow but make its use harder, such as [stack canaries](/stack-canary/), [data execution prevention](/data-execution-prevention/) and [address space layout randomization](/address-space-layout-randomization/).

## Examples

- **Off by one.** A buffer of 8 bytes holds a string of up to 7 characters and a terminating zero. A copy of an 8-character string writes 9 bytes, so one zero byte lands just past the buffer, in whatever the next variable is.
- **A read past the end.** A program keeps a table of 10 entries and gets an index from input. With index 12, a check-free lookup returns the contents of memory after the table. In a server, such a read can send other users' data back to the client; this is an out-of-bounds read, and it changes nothing.
- **An overflow caught by a check.** In a language with bounds checks, the same lookup with index 12 stops with an index error, which the program can handle or log. This is the behavior that run-time bounds checking gives to C.
- **A size that wraps.** A program allocates $n \cdot s$ bytes for $n$ records of $s$ bytes each, with 32-bit arithmetic. For a large $n$ the product wraps to a small number, the buffer is small, and writing the $n$ records overflows it. Checking the product before the allocation prevents the error.
- **Not an overflow.** Computing the address one past the end of an array, for example to stop a loop, is allowed in C. Only an access through that address is an overflow.

## Where it is used

The concept names one of the oldest classes of software flaws, and it is the reason for much of the work on [memory safety](/memory-safety/). The Morris worm of 1988 spread partly through an overflow in a network service, and the class has stayed near the top of lists of serious weaknesses since then; the Common Weakness Enumeration lists it as CWE-119, with children for out-of-bounds reads and writes. It drives the design of the checks on this site: per-pointer bounds in [fat pointers](/fat-pointer/) and [SoftBound](/softbound/), object lookup in [Jones and Kelly bounds checking](/jones-kelly-bounds-checking/), cheap bounds in [baggy bounds checking](/baggy-bounds-checking/), redzones in [AddressSanitizer](/addresssanitizer/), tags in [memory tagging](/memory-tagging/) and hardware bounds in the [CHERI capability model](/cheri-capability-model/). It also motivates the move to languages that check bounds and manage memory, such as languages with [borrow checking](/borrow-checking/).

## References
