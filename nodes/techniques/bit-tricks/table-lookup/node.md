---
tag: BFS2T5
kind: technique
slug: table-lookup
name: Table lookup
aliases:
- lookup tables
- precomputed tables
area: techniques/bit-tricks
level: intro
summary: Replacing computation with indexing into a precomputed table, as with popcount or de Bruijn tables.
prereqs: [bitwise-operations, bitmask]
see_also: [population-count, de-bruijn-bit-scan, table-driven-crc, bit-reversal, four-russians-method, tabulation-hashing, branchless-programming, memoization]
sources:
  - paper: doi:10.1145/63030.63037
    title: Dilip V. Sarwate, Computation of cyclic redundancy checks via table look-up, Communications of the ACM 31(8), 1988
    locator: pp. 1008 to 1013
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 5-1, Counting 1-Bits; Section 7-1, Reversing Bits and Bytes
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
---

Table lookup replaces a computation on a small input by one read from a table that holds the answer for every possible input. A function of a word of $w$ bits is usually too large to tabulate, so the word is cut into chunks of $b$ bits, often a byte, each chunk is looked up in a table of $2^b$ entries, and the partial answers are combined. The [population count](/population-count/) by byte table, [bit reversal](/bit-reversal/) by byte table, the [de Bruijn bit scan](/de-bruijn-bit-scan/) and the [table-driven CRC](/table-driven-crc/) of Sarwate (1988) are standard cases. When the chunk size grows with the input, as $b = \Theta(\log n)$, the same idea becomes the [Four Russians method](/four-russians-method/).

## In plain words

If you need the answer to the same small question many times, and the question has only a few hundred possible inputs, work out all the answers once and write them in a list. Then each later question is one look in the list.

For example, to count the ones in a 64-bit number, first make a list of 256 entries that says how many ones each byte has. Then cut the number into its 8 bytes, look up each byte, and add the 8 results. That is 8 lookups instead of 64 bit tests.

## When it applies

- The function, or a part of it, depends on a short input of $b$ bits, with $2^b$ small enough that the table fits in fast memory: $b \le 8$ fits easily in the L1 cache, and $b = 16$ needs 64K entries.
- The function of a long input combines the values for its chunks in a simple way: a sum (popcount), a reordering (bit reversal), an XOR (CRC, [tabulation hashing](/tabulation-hashing/)), or a lookup chained through a state (finite automata, CRC).
- The table is used many times, so the cost to build it is paid back.
- There is no single instruction for the job on the target machine, or the code must be portable.

## The template

1. **Choose the chunk size $b$.** Balance the number of lookups, $\lceil w / b \rceil$, against the table size, $2^b$ entries.
2. **Build the table once.** Often by a recurrence over the index, which costs $O(1)$ for each entry. For popcount, $T[0] = 0$ and $T[i] = T[\lfloor i / 2 \rfloor] + (i \bmod 2)$.
3. **Cut the input into chunks** with shifts and masks: chunk $k$ is $(x \gg bk) \mathbin{\&} (2^b - 1)$.
4. **Look up and combine.** Popcount adds: $\operatorname{pop}(x) = \sum_k T[\text{chunk } k]$. Bit reversal moves each reversed chunk to the mirror position. CRC feeds each byte, XORed with the state, into the table and XORs the result into the shifted state.

**Example.** For $x$ = 0xF00D1234ABCD5678, the bytes from the low end are 78, 56, CD, AB, 34, 12, 0D and F0, with table values 4, 4, 5, 5, 3, 2, 3 and 4. Their sum is 30, the number of ones in $x$.

**Cost.** $\lceil w / b \rceil$ lookups and $O(w / b)$ other operations for each call, plus $O(2^b)$ time and space once. With $b = \varepsilon w$, a constant number of lookups per word.

## Classic examples

- **Population count.** A byte table gives the count in 8 lookups for 64 bits; a 16-bit table, in 4. Warren compares this with the shift-and-add methods in Section 5-1. See [population count](/population-count/).
- **Bit reversal.** A table of the 256 reversed bytes reverses a 32-bit word in 4 lookups, with the reversed bytes placed in the opposite order (Warren, Section 7-1). See [bit reversal](/bit-reversal/).
- **Index of the lowest set bit.** Isolate the bit as $x \mathbin{\&} -x$, multiply by a de Bruijn constant, and take the top bits of the product as the index into a table of 32 or 64 entries. For 32 bits the constant 0x077CB531 and a shift by 27 give a distinct index for each of the 32 powers of 2. See [de Bruijn bit scan](/de-bruijn-bit-scan/).
- **CRC.** Sarwate's method processes one byte at a time: a table of 256 remainders gives the effect of 8 steps of the shift register at once. See [table-driven CRC](/table-driven-crc/) and [CRC-32C](/crc32c/).
- **Tabulation hashing.** Cut a key into $c$ chunks and XOR the entries of $c$ tables of random words. Here the tables hold random values, not answers. See [tabulation hashing](/tabulation-hashing/).
- **Four Russians.** Tables of all combinations of $\lg n$ rows speed up Boolean matrix products by a $\log n$ factor. See [Four Russians method](/four-russians-method/).

## Variations

- **Several tables.** Use a different table for each chunk position, so that the combination is a plain XOR or sum. The "slicing" CRC methods look up several bytes at once in different tables.
- **Tables in a register.** A table of 16 entries of 4 bits fits in one 64-bit word: $T[i] = (C \gg 4i) \mathbin{\&} 15$. Vector shuffle instructions such as PSHUFB look up 16 or more nibbles at once.
- **Compressed tables.** Store only half of a symmetric table, or derive entries with a cheap correction.
- **Lazy tables.** Fill an entry the first time it is needed. This is [memoization](/memoization/) with a dense index.
- **Tables built at compile time.** Generate the table in the source code or with constant evaluation, so that there is no start-up cost.

## Pitfalls

- **Cache misses.** A table that does not stay in the L1 cache can be slower than the computation. A 64K table of 16-bit entries takes 128 KB; in a benchmark it stays in cache, while in a real program it competes with the data.
- **Timing leaks.** The time of a lookup with a secret index depends on what is in the cache, which leaked keys of table-based AES. Use [branch-free](/branchless-programming/) or bit-sliced code for secret data.
- **Hardware instructions win.** Where POPCNT, TZCNT or a CRC instruction exist, they beat any table. Use the table as the portable fallback.
- **Wrong chunk order.** For bit reversal and CRC the order of the chunks matters: reversed bytes go to the mirror position, and the CRC table depends on whether the register shifts left or right.
- **Shifts of signed values.** Cutting a signed word into chunks with right shifts copies the sign bit into the top chunk. Use unsigned words.

## Exercises

1. Build the byte table for popcount with the recurrence $T[i] = T[\lfloor i/2 \rfloor] + (i \bmod 2)$ and prove that it is correct.
2. Find the constant $C$ and the 16-entry table that give the position of the single one-bit of a 16-bit power of 2 as $T[(x \cdot C \bmod 2^{16}) \gg 12]$, using a de Bruijn sequence of order 4.
3. Show how to reverse the bits of a 64-bit word with a table of 256 reversed bytes, and count the operations.
4. Derive Sarwate's byte-at-a-time CRC update from the bit-at-a-time shift register, for a register that shifts right with the reflected polynomial.
5. Choose the chunk size $b$ that minimizes the total time to count the ones in $N$ words of 64 bits each, if a lookup costs 1, building a table entry costs 1, and the table must be built once. Give the answer as a function of $N$.

## References
