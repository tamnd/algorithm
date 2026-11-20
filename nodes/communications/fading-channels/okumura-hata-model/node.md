---
tag: 1YM5F8
kind: model
slug: okumura-hata-model
name: Okumura-Hata model
aliases:
- Hata model
area: communications/fading-channels
level: core
summary: "Hata's closed-form fit to Okumura's 1968 Tokyo measurements: the median path loss in dB for 150 to 1500 MHz and 1 to 20 km, with corrections for suburban and open areas."
prereqs: [log-distance-path-loss-model, log-normal-shadowing]
see_also: [log-distance-path-loss-model, log-normal-shadowing, free-space-path-loss, multipath-fading, least-squares-problem, outage-probability]
sources:
  - paper: doi:10.1109/T-VT.1980.23859
    title: M. Hata, Empirical formula for propagation loss in land mobile radio services, IEEE Transactions on Vehicular Technology 29(3), 1980
    locator: pp. 317 to 325 (the formulas for the median loss in urban, suburban and open areas, fitted to the curves of Okumura et al., and their ranges of validity)
  - paper: "Y. Okumura, E. Ohmori, T. Kawano and K. Fukuda, Field strength and its variability in VHF and UHF land-mobile radio service, Review of the Electrical Communication Laboratory 16(9-10), 825 to 873, 1968"
    title: Field strength and its variability in VHF and UHF land-mobile radio service
    locator: pp. 825 to 873 (the measurements in and around Tokyo and the curves of median field strength)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 4.10.3 (Okumura model), Section 4.10.4 (Hata model) and Section 4.10.5 (PCS extension to Hata model)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 2.5.1 (Okumura model), Section 2.5.2 (Hata model) and Section 2.5.3 (COST 231 extension to Hata model)
---

The Okumura-Hata model gives the median path loss of a macrocell link in dB as a closed formula of the frequency, the distance and the two antenna heights. Okumura et al. measured the field strength in and around Tokyo in 1968 and published curves; Hata fitted formulas to those curves in 1980. The result is a fit to measurements, not a law of physics. It is a [log-distance model](/log-distance-path-loss-model/) whose slope and intercept depend on the antenna heights, and the spread around it is [log-normal shadowing](/log-normal-shadowing/).

## The machine

The inputs are the carrier frequency $f$ in MHz, the distance $d$ in km, the effective height $h_b$ of the base station antenna in m and the height $h_m$ of the mobile antenna in m. All logarithms are $\log_{10}$. The median loss in an urban area is

$$L_u = 69.55 + 26.16 \log f - 13.82 \log h_b - a(h_m) + (44.9 - 6.55 \log h_b) \log d \quad \text{dB}.$$

The correction $a(h_m)$ for the mobile antenna is

- small or medium city: $a(h_m) = (1.1 \log f - 0.7) h_m - (1.56 \log f - 0.8)$;
- large city: $a(h_m) = 8.29 (\log 1.54 h_m)^2 - 1.1$ for $f \le 200$ MHz, and $3.2 (\log 11.75 h_m)^2 - 4.97$ for $f \ge 400$ MHz.

Both give about 0 dB at $h_m = 1.5$ m. Two other kinds of area subtract a correction from $L_u$:

- suburban: $L_{su} = L_u - 2 (\log (f / 28))^2 - 5.4$;
- open (rural): $L_o = L_u - 4.78 (\log f)^2 + 18.33 \log f - 40.94$.

**Range of validity.** Hata gives $150 \le f \le 1500$ MHz, $1 \le d \le 20$ km, $30 \le h_b \le 200$ m and $1 \le h_m \le 10$ m (Rappaport, Section 4.10.4). The fit is good only inside this box.

**COST-231 extension.** For $1500 \le f \le 2000$ MHz, the COST-231 group fitted a new frequency term (Goldsmith, Section 2.5.3; Rappaport, Section 4.10.5):

$$L = 46.3 + 33.9 \log f - 13.82 \log h_b - a(h_m) + (44.9 - 6.55 \log h_b) \log d + C_M,$$

with $C_M = 0$ dB for medium cities and suburbs and $C_M = 3$ dB for large city centers.

**Okumura's original method.** Okumura's curves give the median loss as the free-space loss plus a median attenuation $A_{mu}(f, d)$ read from a chart for $h_b = 200$ m and $h_m = 3$ m, minus height gain terms and an area correction (Rappaport, Section 4.10.3). Hata's formulas remove the need to read charts.

## What it counts

The model predicts one number: the median loss over many places at the same distance, in a given kind of area. The received power at a point is this median plus a random shadowing term and a multipath fade, so a link budget adds a fade margin on top of it.

**Example.** Take $f = 900$ MHz, $h_b = 30$ m, $h_m = 1.5$ m, a medium city. Then $a(h_m) = 0.0159$ dB, and the slope is $44.9 - 6.55 \log 30 = 35.22$ dB per decade. The loss is

| distance | 1 km | 2 km | 5 km | 10 km | 20 km |
|---|---|---|---|---|---|
| $L_u$ (dB) | 126.40 | 137.01 | 151.02 | 161.63 | 172.23 |

At 1 km, the large-city correction gives 126.42 dB, the suburban formula 116.46 dB and the open-area formula 97.90 dB. [Free space](/free-space-path-loss/) gives 91.53 dB at the same point, so the city costs about 35 dB.

**Range from a budget.** With a maximum loss of 140 dB in the medium city above, $\log d = (140 - 126.40) / 35.22$, so $d = 2.43$ km.

## Relation to other models

- **Log-distance model.** For fixed $f$, $h_b$ and $h_m$, $L_u$ is the log-distance formula with $d_0 = 1$ km, $\mathrm{PL}(d_0)$ the value at 1 km and $n = (44.9 - 6.55 \log h_b) / 10$. This gives $n = 3.52$ for $h_b = 30$ m and $n = 3.18$ for $h_b = 100$ m.
- **Free space** has slope 20 dB per decade and grows by 20 dB per decade of frequency. Hata has the steeper slope of 30 to 35 dB per decade in distance and 26.16 dB per decade in frequency below 1500 MHz.
- **Shadowing.** The formula is the median; [log-normal shadowing](/log-normal-shadowing/) with $\sigma$ of several dB describes the spread around it. Okumura's paper also reports the spread of its measurements.
- **Fading.** [Multipath fading](/multipath-fading/) acts on a much smaller scale and is averaged out of the medians.
- **Newer models.** Site-specific ray tracing and the stochastic channel models of 3GPP replace Hata for small cells, high frequencies and antennas below the rooftops.

## Known results in the model

These are properties of the fitted formulas. They are exact for the formulas and approximate for real channels.

1. **Slope and base antenna height.** The loss grows by $44.9 - 6.55 \log h_b$ dB per decade of distance: 35.22 dB for $h_b = 30$ m and 31.80 dB for $h_b = 100$ m. A higher base antenna lowers the loss at 1 km by $13.82 \log(h_b'/h_b)$ dB and also flattens the slope. With $h_b = 100$ m, the loss at 1 km and 900 MHz is 119.18 dB.
2. **Mobile height.** In a medium city at 900 MHz, $a(3) = 3.84$ dB, so raising the mobile antenna from 1.5 m to 3 m lowers the loss to 122.58 dB at 1 km.
3. **Frequency.** The urban loss grows by $26.16 \log(f_2/f_1)$ dB, a little more than the free-space $20 \log(f_2/f_1)$. At 1800 MHz, COST-231 with $C_M = 0$ gives 136.20 dB at 1 km and 160.82 dB at 5 km for $h_b = 30$ m and $h_m = 1.5$ m.
4. **Two fits in a row.** Hata fitted Okumura's curves, and Okumura's curves are medians of measurements in one region. So the error of the formula against measurements in another city adds the fit error, the difference between the cities and the shadowing at each point.

### Pitfalls

- **Outside the box.** Do not use the formulas below 1 km, above 20 km, at 2.4 GHz or above, or for a base antenna below the rooftops. The log term in $h_b$ becomes meaningless for small cells, and the frequency term is wrong above 2 GHz.
- **Units.** $f$ is in MHz, $d$ in km and the heights in m. A distance in m gives a loss 105.66 dB too high at $h_b = 30$ m, because it adds three decades at 35.22 dB each.
- **Median, not mean.** The formula is a median in dB. The mean power in watts is higher by $\sigma^2 \ln 10 / 20$ dB under log-normal shadowing.
- **Effective height.** $h_b$ is the height above the average terrain, not above the ground at the mast.

## References
