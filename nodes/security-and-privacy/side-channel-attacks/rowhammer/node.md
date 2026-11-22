---
tag: CCFEWD
kind: technique
slug: rowhammer
name: Rowhammer
aliases:
- DRAM disturbance error
- row hammering
area: security-and-privacy/side-channel-attacks
level: advanced
summary: A DRAM disturbance error in which many activations of one row in a short time flip bits in nearby rows, which breaks the isolation that memory protection assumes.
prereqs: [error-detection, side-channel-attack]
see_also: [differential-fault-analysis, rsa-fault-attack, hamming-code, error-detection, memory-safety, software-fault-isolation, meltdown-attack, spectre-attack]
sources:
  - paper: doi:10.1109/ISCA.2014.6853210
    title: "Yoongu Kim, Ross Daly, Jeremie Kim, Chris Fallin, Ji Hye Lee, Donghyuk Lee, Chris Wilkerson, Konrad Lai and Onur Mutlu, Flipping bits in memory without accessing them, an experimental study of DRAM disturbance errors, ISCA 2014, pages 361-372"
    locator: the cause of disturbance errors, the measured errors in modules of three manufacturers, and the analysis of the defenses, with the PARA proposal
  - paper: doi:10.1109/TCAD.2019.2915318
    title: "Onur Mutlu and Jeremie S. Kim, RowHammer, a retrospective, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 39(8), 2020, pages 1555-1571"
    locator: the survey of the attacks that followed 2014 and of the defenses, among them higher refresh rates, error correcting codes, target row refresh and PARA
---

Rowhammer is a fault in DRAM chips: when one row of memory cells is opened and closed many times in a short period, some cells in the rows next to it lose their charge and their bits flip, although no program wrote to them. Kim et al. (2014) measured these disturbance errors in most of the DRAM modules that they tested, and showed that an ordinary program can cause them. A bit flip in memory that belongs to another program or to the operating system breaks memory isolation without a software bug. It is a fault attack, like [differential fault analysis](/differential-fault-analysis/), but the fault source is software instead of a glitch or a laser. The defenses are in the memory controller and in the DRAM: more frequent refresh, extra refreshes of the neighbours of an often-used row, error correcting codes, and the separation of trust domains in physical memory.

## In plain words

Memory chips keep each bit as a tiny electric charge. The cells are packed so close that using one row of cells disturbs the rows next to it a little. Normally the chip refreshes every row often enough that this does not matter.

If a program uses the same row very many times before the next refresh, the disturbance adds up, and a few bits in the next rows change from 0 to 1 or from 1 to 0. The program did not write to those rows. If they hold data of another program, or the tables that the system uses to protect memory, a changed bit can give the program powers that it should not have.

## When it applies

### Threat model

The observer, here an attacker who causes faults, is an unprivileged program, or a script in a browser, on a machine with DRAM. He can read and write only his own memory. He cannot write the memory of other domains. The defenses below are stated against this attacker. The claims about which chips are affected are measurements, not theorems.

### Conditions

1. **DISTURB.** The DRAM has cells that lose charge faster when a nearby row is activated often. This is a property of dense chips, and Kim et al. found it more often in the newer modules that they tested.
2. **ACTIVATE.** The attacker can make one row open and close many times within one refresh interval. This needs memory accesses that are not served by the caches.
3. **ADJACENT.** Rows that the attacker can activate lie next to rows that hold data of another trust domain.
4. **USE.** The flipped bit changes data that matters: a protection table, a key, a check or code.

### What removes a condition

| defense | condition it removes | cost |
|---|---|---|
| a higher refresh rate | 1 and 2, as fewer activations fit in one interval | more power and less memory bandwidth; Kim et al. found that a much higher rate is needed to remove all errors |
| PARA: on each activation, refresh the neighbouring rows with a small probability | 2, with a probabilistic guarantee | a small number of extra refreshes |
| target row refresh in the DRAM: count activations and refresh the neighbours of rows that cross a limit | 2, for the patterns that the counters track | chip area; later work found patterns that the counters miss |
| error correcting codes on each memory word | 4, for one flipped bit in a word, as a [Hamming code](/hamming-code/) corrects | extra memory chips; several flips in one word can pass |
| guard rows and separation of trust domains in physical memory | 3 | memory that is left unused |
| integrity checks on protection data and keys | 4, for the data that is checked | the work of the checks |

**Claim (theorem, for the probabilistic defense, in a simple model).** Let each activation of a row refresh each of its neighbours with probability $p$, independently. Then the probability that a neighbour is not refreshed during $k$ consecutive activations is $(1 - p)^k$. If a bit needs at least $k$ activations within one interval to flip, the probability of a flip in one interval is at most $(1 - p)^k$, which falls exponentially in $k$. The model assumes that the refresh resets the disturbance and that the coins are independent of the attacker. This is the argument for PARA in Kim et al.

## The template

The block is the shape of the class: each line is a condition, and the comment names the defense that removes it. It is not a recipe and it has no access pattern, no address and no count.

```pseudo id=main
ROWHAMMER-CLASS(memory M, system S)
L1  require DISTURB: M has cells that lose charge when a nearby row is activated often   ▷ removed by DRAM that is not vulnerable
L2  require ACTIVATE: the attacker can activate one row often within one refresh interval ▷ removed by refresh, PARA or target row refresh
L3  require ADJACENT: the attacker's rows are next to rows of another domain             ▷ removed by guard rows and domain separation in S
L4  require USE: a flipped bit changes data that S trusts                               ▷ hole USE: removed by error correction or integrity checks
L5  if every condition holds then the attacker changes data of another domain
```

### Rowhammer and differential fault analysis

Rowhammer and [differential fault analysis](/differential-fault-analysis/) are both fault attacks. Differential fault analysis is a method to learn a key from faulty outputs of a computation, and it does not care where the fault comes from. Rowhammer is a way to make faults from software, with no physical access. So a Rowhammer flip in the data of a computation with a key can create the faulty output that a fault analysis needs, for example a faulty RSA signature as in the [RSA fault attack](/rsa-fault-attack/). The same defense helps against both: check a result before it leaves the device.

## Classic examples

- **Kim et al., 2014 (measurement).** On a test platform that controlled the memory directly, they found disturbance errors in 110 of 129 DRAM modules from three manufacturers, and in 836 of their 972 chips. They also caused errors with an ordinary user program on real systems. They proposed PARA as a low-cost fix.
- **Privilege escalation, 2015.** A team at Google showed that flips in the page tables of the operating system could give a user program write access to memory it should not reach, and that flips could break the checks of a sandbox. This turned the errors into a security problem; see [memory safety](/memory-safety/) for the isolation that is lost.
- **From a browser and from a phone, 2016.** Later work caused flips from JavaScript and on mobile devices, which showed that condition 2 needs no special instructions.
- **Target row refresh, 2020.** DRAM makers had added counters that refresh the neighbours of often-used rows. A study of many modules found access patterns that the counters did not track, so the errors came back on modules sold as protected.
- **Error correction, 2019.** Work on server memory showed that several flips can land in one word, so error correcting codes slow the attack and report it, but do not always stop it.
- **Reading with flips, 2020.** RAMBleed showed that the flips also depend on the values in nearby rows, so the effect can leak data, not only change it. This makes Rowhammer a side channel as well as a fault.

## Variations

- **One-sided and double-sided.** The attacker activates a row on one side of the victim row, or on both sides.
- **Many-sided.** Patterns with more rows defeat counters that track only a few rows.
- **Other memories.** Related disturbance effects exist in other dense memories, and the same conditions apply.
- **Remote.** Some systems let network packets write memory directly, which can give condition 2 without local code.

## Pitfalls

- **Trusting error correction.** A code that corrects one bit in a word detects two, but three or more flips can turn into a wrong word that looks valid.
- **Trusting a vendor claim.** A defense inside the DRAM is not visible to the system. Measure, and keep a defense in the system as well.
- **Forgetting physical layout.** Rows that are next to each other in the chip need not be next to each other in the address space. Domain separation must follow the physical layout.
- **Thinking only of the kernel.** Any trusted data in memory can be the target: keys, checks in a sandbox, the code of a library.

## References
