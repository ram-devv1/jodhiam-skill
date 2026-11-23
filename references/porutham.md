# Porutham (marriage matching)

All counts run **from the girl's star or rasi to the boy's, counting the girl's as 1**. Run
`jathagam.py match girl.json boy.json`.

| Porutham | Rule used | Weight |
|---|---|---|
| Dinam | count mod 9 ∈ {2, 4, 6, 8, 0} | normal |
| Ganam | Deva / Manushya / Rakshasa: same gana, or Deva with Manushya | normal |
| Mahendram | count ∈ {4, 7, 10, 13, 16, 19, 22, 25} (some drop 19) | minor |
| Stree Deergham | count > 13 good; > 9 average | minor |
| Yoni | animal pairs; sworn enemies fail (Horse–Buffalo, Elephant–Lion, Sheep–Monkey, Serpent–Mongoose, Dog–Deer, Cat–Rat, Cow–Tiger) | normal |
| Rasi | 6/8 fails; 2/12 average; same rasi, 7th, 3/11 and 5/9 good in Tamil practice | **important** |
| Rasi Athipathi | rasi lords not enemies | normal |
| Vasyam | rasi in the other's vasya list | minor |
| **Rajju** | same body group (Siro / Kanta / Nabhi / Kati / Paadha) fails | **critical: most jothidars reject the match on this alone** |
| **Vedhai** | mutually obstructing star pairs fail | **critical** |

Rajju groups: Paadha = Ashwini, Ayilyam, Magam, Kettai, Moolam, Revathi · Kati = Bharani, Poosam,
Pooram, Anusham, Pooradam, Uthirattathi · Nabhi = Karthigai, Punarpoosam, Uthiram, Visakam,
Uthiradam, Poorattathi · Kanta = Rohini, Thiruvathirai, Hastham, Swathi, Thiruvonam, Sadhayam ·
Siro = Mirugasirisham, Chithirai, Avittam.

Vedhai pairs: Ashwini–Kettai, Bharani–Anusham, Karthigai–Visakam, Rohini–Swathi,
Thiruvathirai–Thiruvonam, Punarpoosam–Uthiradam, Poosam–Pooradam, Ayilyam–Moolam, Magam–Revathi,
Pooram–Uthirattathi, Uthiram–Poorattathi, Hastham–Sadhayam, and Mirugasirisham, Chithirai and
Avittam with each other.

**Thresholds:** 6/10 or more with Rajju passing is the usual Tamil bar (some say 5–7). The North
Indian Ashtakoota needs 18/36. The script also computes Nadi: same Nadi is a dosham in North Indian
practice and gets less weight in Tamil practice. Bhakoot (2/12, 5/9 or 6/8 rasi) is cancelled when
both rasi lords are the same or mutual friends; the script reports `bhakoot_cancelled`.

**Chevvai dosham:** Mars in the 2nd, 4th, 7th, 8th or 12th from lagnam, Moon or Venus (the North
Indian rule adds the 1st). The traditional cancellations are: Mars in its own sign or exalted, and
both partners having it. Lagnam needs an accurate birth time, so don't call a dosham from an
uncertain lagnam.

**Reporting:** give both scores, then the meaning of the critical ones, then the ups and downs.
Star matching is one layer. Full jathagam matching (7th house, dasa sandhi) needs exact times.
For real couples, say that communication, family and practical factors outweigh porutham.
