# 13 - Killing engine/alternator noise (this car's audio setup)

Not a head-unit mod, just recording what actually worked on this car so it does not get lost.

Car has a stock **Harman Kardon** amplified system. Two noise sources showed up when feeding the FYT unit
into it:

1. **Ground-loop hum** - fixed with a **ground loop isolator** on the audio lines. That killed the hum
   but not everything.
2. **Alternator whine** (pitch rises with RPM) - the isolator did **not** fix this, and it comes in over
   the analog signal path / power.

Rather than mess with power-line noise filters / "power cleaners" (which may or may not have helped), the
fix that worked was to **get off analog out entirely**: a small **USB-powered TOSLINK (optical) DAC -
HiFime S2** hung off the back of the stereo. Optical is galvanically isolated, so the whine that was
riding the analog/ground path is gone.

Wiring detail: the stock harness had to be **modified to bridge the front and rear channels** onto the one
DAC's output (single stereo DAC feeding both). A cleaner alternative that was not tried: a **TOSLINK
splitter into two DACs** (one for front, one for rear) so front/rear stay independent. The single-DAC
bridge was good enough here.

Summary of what worked, in order:
- ground loop isolator -> kills hum
- USB TOSLINK DAC (HiFime S2) off the head unit's optical/USB out -> kills alternator whine (optical
  isolation beats fighting the power line)
- harness modified to bridge front+rear onto the one DAC (or split to two DACs if you want them separate)
