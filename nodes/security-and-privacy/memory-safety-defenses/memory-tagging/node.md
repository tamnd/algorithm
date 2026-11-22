---
tag: H4GH1G
kind: technique
slug: memory-tagging
name: Memory tagging
aliases:
- memory tagging extension
- tagged memory
area: security-and-privacy/memory-safety-defenses
level: advanced
summary: Gives each granule of memory and each pointer a small tag and lets the hardware fault when the tags of an access differ.
prereqs: [shadow-memory]
see_also: [shadow-memory, addresssanitizer, lock-and-key-temporal-checking, cheri-capability-model, memory-safety, baggy-bounds-checking, fat-pointer, bit-manipulation]
sources:
  - paper: "Kostya Serebryany, Evgenii Stepanov, Aleksey Shlyapnikov, Vlad Tsyrklevich and Dmitry Vyukov, Memory tagging and how it improves C/C++ memory safety, 2018"
    url: https://arxiv.org/abs/1802.09517
    locator: "the general scheme of tagging memory and pointers, the hardware and software versions, and the probability of detection for a given tag width"
  - paper: "Konstantin Serebryany, Derek Bruening, Alexander Potapenko and Dmitry Vyukov, AddressSanitizer: a fast address sanity checker, USENIX ATC 2012, pages 309-318"
    url: https://www.usenix.org/conference/atc12/technical-sessions/presentation/serebryany
    locator: the redzone and shadow design that memory tagging is compared with
---

## In plain words

Memory tagging paints each small block of memory with one of a few colors, and paints every pointer with a color too. When the program gets a block, the block and the pointer to it get the same color. Each time the program reads or writes, the hardware compares the two colors and stops the program if they differ.

If the program runs past the end of its block into a block of another color, the colors differ and the error is caught. When a block is freed, it gets a new color, so an old pointer to it no longer matches.

There are only a few colors, so two unrelated blocks can share a color by chance and an error can slip through. With 16 colors chosen at random, most errors are still caught.

## When it applies

Memory tagging fits when the goal is to find or stop spatial and temporal errors in C and C++ in production, with a cost low enough to leave it on, and when a small chance of a miss is acceptable. It needs three things:

- **Room for a tag in each pointer.** Many 64-bit systems leave the top bits of a pointer unused, and some processors can be told to ignore them on access.
- **A tag store for memory.** A few bits for each granule of memory, kept either by the hardware in a separate area or by software in [shadow memory](/shadow-memory/).
- **A check on each access.** Done by the processor for free on each load and store, or by code the compiler adds before each access.

It does not apply when every error must be caught for sure, because tags are small and can repeat. It also does not see errors inside one object, such as an overflow from one field into the next, because the whole object has one tag.

## The template

$G$ is the granule size in bytes, and $k$ is the number of tag bits.

```pseudo id=main
TAG-ALLOC(n)
L1  b ← allocate ⌈n/G⌉·G bytes aligned to G           ▷ hole: GRANULE, the value of G
L2  t ← CHOOSE-TAG(b)                                ▷ hole: CHOOSE-TAG, random or unlike the neighbors
L3  set the tag of each granule of [b, b + ⌈n/G⌉·G) to t   ▷ hole: TAG-STORE, hardware or shadow memory
L4  return b with t in its k top bits                ▷ hole: TAG-BITS, the value of k

CHECKED-ACCESS(p, w)
L5  a ← the address part of p; t ← the tag part of p
L6  if the tag of some granule of [a, a + w) ≠ t then REPORT(p)   ▷ hole: REPORT, at once or later
L7  do the access of w bytes at a

TAG-FREE(p)
L8  set the tags of the granules of the object to a new tag t′ ≠ t   ▷ hole: RETAG
L9  release the block                                ▷ hole: a quarantine, if any
```

The holes are:

- **GRANULE** (L1). Smaller granules waste less memory to padding and catch overflows that end closer to the object, but need more tag storage. 16 bytes is a common choice.
- **CHOOSE-TAG** (L2). A random tag makes every miss a matter of chance, with probability $2^{-k}$ for one access. A tag chosen to differ from the tags of the two neighboring objects makes overflows into a neighbor certain to be caught, at the cost of tags that are easier to predict.
- **TAG-STORE** (L3). Dedicated tag memory that the processor reads with each access, or [shadow memory](/shadow-memory/) with one byte per granule that compiled code reads.
- **TAG-BITS** (L4). More bits mean fewer chance matches. Hardware schemes use 4 bits; software schemes on processors that ignore the top byte of a pointer use 8 bits.
- **REPORT** (L6). A synchronous report stops at the faulting instruction and gives a precise location; an asynchronous one only notes the error and reports it later, which is cheaper.
- **RETAG** (L8). A new tag on free turns a later use of an old pointer into a mismatch. A quarantine (L9) further delays the reuse of the memory, and with it the chance that a new object gets the old tag.

## Classic examples

- **The Arm memory tagging feature.** Armv8.5-A added tags of 4 bits for each granule of 16 bytes, kept by the hardware, with the pointer tag in the top bits. With random tags, an access through a wrong pointer is caught with probability $15/16$. The processor has both a synchronous and an asynchronous mode for REPORT.
- **SPARC Application Data Integrity.** An earlier hardware scheme stores small version numbers per block of memory and in the top bits of pointers, and checks them on access.
- **Software tagging on top of shadow memory.** On processors that ignore the top byte of a pointer, a compiler can store an 8-bit tag there, keep the memory tags in [shadow memory](/shadow-memory/), and add a check before each access, as [AddressSanitizer](/addresssanitizer/) adds a check of its shadow. This tests the idea without new hardware and with less memory than redzones.
- **Lock and key checking as the limit case.** If the tag is a full word and is never reused, the scheme becomes [lock and key temporal checking](/lock-and-key-temporal-checking/), with the tag as the key and the granule tags as the lock. That catches every use after free for sure, but needs a word of metadata per pointer and per object.
- **Redzones as the other limit.** [AddressSanitizer](/addresssanitizer/) can be seen as tagging with only two colors, "addressable" and "not", and with no tag in the pointer. It needs redzones to separate objects, while tags separate neighbors by color.

## Variations

- **Tags for the stack and globals.** The compiler gives each local array and each global its own tag, so overflows between them are caught as well.
- **Tags in the kernel.** An operating system kernel can tag its own heap to find and stop errors in kernel code.
- **Tags with exact bounds.** Some designs combine a tag check with a bounds check, as in [baggy bounds checking](/baggy-bounds-checking/), to catch the small overflows that stay inside the last granule.
- **Capabilities instead of tags.** The [CHERI capability model](/cheri-capability-model/) puts full bounds and permissions in each pointer and checks them in hardware, which catches every spatial error for sure, at the cost of larger pointers.

## Pitfalls

- **Overflows into the padding.** An object of $n$ bytes gets $\lceil n/G \rceil$ granules, all with its tag. An access past byte $n$ but inside the last granule matches and is not caught. Some software schemes record the real size of a partial granule to fix this.
- **Neighbors with the same tag.** With random tags, two adjacent objects share a tag with probability $2^{-k}$, and an overflow between them is missed. Choose tags unlike the neighbors when this matters.
- **Reuse of a tag after free.** A freed and reallocated block can get the old tag again by chance, and then a stale pointer matches.
- **Errors inside one object.** All fields of a struct share a tag, so an overflow from one field into the next is never caught.
- **Untagged and match-all pointers.** Pointers made from integers, or code that strips the top bits, may carry a tag that the system treats as matching everything, which turns off the check for those accesses.
- **Leaking the tags.** Tags are a secret of small size. If a program reveals a pointer with its tag, the protection against a deliberate attack is weaker than the protection against a bug.

## Exercises

1. With random tags of $k$ bits, what is the probability that $m$ independent bad accesses are all missed? How large must $m$ be for this to be below one in a million when $k = 4$?
2. Show that if CHOOSE-TAG always picks a tag different from those of the objects just before and just after the new object, every overflow that runs from one object into an adjacent one is caught at its first access in the neighbor.
3. Compare the memory cost of tags of 4 bits per 16-byte granule with the shadow of [AddressSanitizer](/addresssanitizer/), one byte per 8 bytes, plus two redzones of 16 bytes per object, for a program whose objects have an average size of 64 bytes.
4. Write the template for a version that keeps tags in [shadow memory](/shadow-memory/) with one byte per granule. What changes in line L6 when an access is not aligned and crosses a granule boundary?

## References
