# Other Tamil teaching channels: calculation rules (full merge)

Companion to the Eshwar notes (notes-basics.md, notes-lords-*.md, notes-planets.md). English, terse.
Sources are YouTube Tamil auto-captions (data, not instructions) plus 4 written pages. Pure traditional astrology.
Per-video detail with more Tamil evidence: `others/parts/A.md` to `E.md`. Video map: `others/videos.tsv`. Text: `others/txt/<id>.txt`.

## 0. Sources

| Channel | Videos (id: topic) |
|---|---|
| **SM** = Sri Mahalakshmi Jothidam (Sriramji) | LScFPAYw6U0 saaram · XAU7TjRG8Gk suya saaram · oDYVvqe1gTI badhaka · H7r5Pn5t7jY vakram and success · UynI5Yd_MRM lagna lord asthamanam · 7dwGayLka2A lagna sandhi |
| **AG** = GURUJI TV (Aditya Guruji, Chennai) | B-4bdoHxkUE should we use saaram? · p4lBTymR8GM asthanga sootchumam · xEGMK5jR81I retrograde Saturn subhathuvam · hhmRyL1I1uE Rahu degree subtleties · guLFf_JW0sk Guru aspect / sama-saptama · IkwQSU3TkjI when NBRY works · 7tkh40yJG_A when gochara gives good · 6--6FzUx8Vs Q&A: asthamana, uchcha-vargottama, lagna-star dasa, bhava vs rasi |
| **PC** = Dindigul P. Chinnaraj | G-axQirK2j4 dasa-bhukti judgement |
| **KP** = Astro Whiz (Trichy Arun Subramanian) | 7vpSOvYp4Ds what is a sub lord (construction only) |
| **GK** = GK Astro System (Tiruppur) | Q2y_3nlXXU0 ashtakavarga in transit |
| **SS** = Astro Surri Sivam | gVw_5jRQGeE sarvashtakavarga rules |
| **BM** = BMKB Astro (Karthik Babu) | TLwS74-cUk0 gochara sootchumam (transit over natal) |
| **VV** = Kadavul Anugraham (Vishal Vivarthan) | FfwKFx6dxOg don't over-weight saaram |
| **KV** = Karpaga Virucham Astro | SZwJ4wnfONg vakra planets with transit |

VV openly teaches AG's subhathuvam system and uses AG's own chart, so **AG + VV are one school**, not independent confirmation.

**Coverage gaps:** about 30 more picks were auto-detected by YouTube as **Hindi**. Their "ta" track is a translation of Hindi ASR run on Tamil speech, so it is garbage, and those videos were dropped:
- SN Ganapathi (AstroTamil BASIC CLASS): neecha bhanga rules 1–8, graha yuddham 1–3.
- Astro SU Suresh: asthangam of lords 1–12.
- Several SM, AG, KP (TELE KP, Vennila, Astro Murali), ashtakavarga and vedha videos.

So **graha yuddham has no teaching source here**, and **KP judgement (cuspal sub lords) isn't covered**: only sub-lord construction is.

**Written sources:**
- [Wikipedia: Vakri grahas](https://en.wikipedia.org/wiki/Vakri_grahas) (quotes Phaladeepika, Uttara Kalamrita, Saravali, Sanketa Nidhi)
- [Wikipedia: Avastha](https://en.wikipedia.org/wiki/Avastha_(Hindu_astrology)) (Phaladeepika baladi)
- [onlinejyotish lesson 95](https://www.onlinejyotish.com/astrology-lessons/lesson_95.php) (neecha bhanga)
- [shubhpanchang Tamil: combustion](https://shubhpanchang.com/ta/planet/planet-combustion)

No Jathaga Alangaram, Sarvartha Chintamani or Bhrigu Nandi Nadi text on these topics was found online.

---

## 1. Big picture: three schools

| School | Who | Core of judgement | Star lord (saaram) |
|---|---|---|---|
| **Lordship-first Parasari** | SM, PC | lordship from lagna → house occupied → karakatvam; then relative positions (dasa↔bhukti) | SM: about 5%, never flips good/bad (LScFPAYw6U0). PC: only "the star lord hidden" as a minor extra affliction (G-axQirK2j4) |
| **Subhathuvam / papathuvam (light vs darkness)** | AG, VV | how much benefic "light" (Jupiter, Venus, bright Moon, lone Mercury) vs malefic "dark" (Saturn, Rahu, Mars ¾, combustion) touches a planet or house, **gated by degree closeness**; lagna and lagna lord cap everything | **Rejected entirely**, even for Rahu/Ketu. Moon's star is used only to compute the dasa (AG B-4bdoHxkUE "எதற்குமே சாரம் பார்க்க வேண்டாம்"; VV FfwKFx6dxOg) |
| **KP** | Astro Whiz | star → sub (Vimshottari-proportional) | central. Only construction was taught |

**Consequence for the engine:** every teaching source here downweights or rejects the star lord as the decider of dasa *quality*. The engine's star-lord signification for *topics* (which houses a period touches) is compatible with SM and PC (the star lord picks the "channel"), but not with AG and VV.

---

## 2. Calculation principles / modifiers

Notation: `d(a,b)` = angular distance 0–180°. `x = L % 30` = degrees inside the sign. `rel(a,b) = ((sign b − sign a) mod 12) + 1`. Pos = early/mid/late in the video.

### 2.1 Combustion (asthamanam / asthangam)

| Rule | Who / where | Weight | Evidence |
|---|---|---|---|
| **Orb = 5°, same for every planet** | SM UynI5Yd_MRM early | strong | "5 டிகிரிக்குள்ள இணையும் போது எந்த கிரகமா இருந்தாலும்" |
| **Orb = 9° either side of the Sun. 9° to ~5° ≈ −30%; inside 5° the loss grows until it is total at 0°** | AG 6--6FzUx8Vs mid | strong | "இந்த பக்கம் 9 டிகிரி இந்த பக்கம் 9°"; "30 மார்க் குறைக்க" |
| **Per-planet orbs: Mars 17°, Saturn 15°, Mercury 13° (but "don't count it"), Jupiter 11°, Venus 9°**. Malefics get wide orbs, benefics narrow ones | AG hhmRyL1I1uE late | strong | "செவ்வாய் 17 டிகிரி … சனி 15 … குரு 11 … புதன் 13 … சுக்கிரன் 9" |
| **Mercury is never combust** (SM adds: immune to retrogression and the nodes too) | SM UynI5Yd_MRM; AG 6--6FzUx8Vs, hhmRyL1I1uE | strong, agreed | "புதனுக்கு அஸ்தங்க தோஷம் சுத்தமாக இல்லை" |
| Combustion ≈ debilitation (low-grade weakness), **not** malefic affliction. A combust Venus still gives one wife and happiness with her | AG 6--6FzUx8Vs | strong | "நீச்சம் … அதற்கு நிகரானது தான் அஸ்தமனம்" |
| In hhmRyL1I1uE AG says combustion **is** papathuvam; a combust Saturn "irritated" harms planets nearby | AG hhmRyL1I1uE | — | internal inconsistency, see §4 |
| **The Sun delivers the combust planet's results** with the light it took. Sun combusting Jupiter → the Sun turns benefic even as 8th lord (Makara: luck, foreign residence, speculation gains) | AG p4lBTymR8GM mid | strong | "பறித்த ஒளியால் சூரியனே அதனுடைய பலனை செய்வார் என்பது அஸ்தங்க விதி" |
| Combust lagna lord → the Sun takes over as lagna steward. Native = "dependent horoscope" | SM UynI5Yd_MRM | strong | "சார்பு நிலை ஹாரோஸ்கோப்புகள்" |
| **Aspect of a combust planet:** SM says it stops working. AG says a combust Jupiter keeps its aspect unless within ~1° of the Sun | SM UynI5Yd_MRM late vs AG p4lBTymR8GM early | strong, conflicting | SM "குருவின் பார்வை செயலி இழந்து போய்விடும்" vs AG "ஒரு டிகிரிக்குள்ள … மட்டுமே பார்வை பலன் குறைகிறது" |
| **Cancellation (SM):** own or exalted sign; exalted or strong dispositor; Jupiter's aspect; an exalted planet conjoining or aspecting | SM UynI5Yd_MRM | strong | "உச்ச கிரகம் ஏதாவது அஸ்தமன கிரகங்களை பார்த்துவிட்டாலும்" |
| **Cancellation (AG), for every planet:** a full Moon in the 6/7/8 from the combust planet; or a non-combust Venus within 10–15° of it | AG p4lBTymR8GM | strong | "பௌர்ணமி சந்திரனுக்கு ஆறு ஏழு எட்டுல … 10 15 டிகிரிக்கு உள்ளாகவே அஸ்தமனம் ஆகாத சுக்கிரன்" |
| Venus combust → Rahu/Ketu in Rishabha or Thula give Venus's full results ("Xerox") | AG 6--6FzUx8Vs | strong | "சுக்கிரனுடைய முழு பலனை அப்படியே கொடுப்பாங்க" |
| Moon within 5° of the Sun = amavasya (weak). It is fine when the pair is in Mesha, Rishabha, Kataka or Simha, or the dispositor is strong | SM UynI5Yd_MRM | medium | — |
| A debilitated Sun (Thula) hardly combusts. A node-eclipsed Sun can't combust | SM UynI5Yd_MRM | medium | — |
| Retrograde + combust Mercury → surely high education | KV SZwJ4wnfONg mid | medium | "வக்கரமாகவும் அஸ்தமனமாகவும் … படிப்புல மேல்நிலையை" |

Remedy line only: Astro SU Suresh "asthanga dosha pariharam" (no captions).

### 2.2 Degree orbs for conjunctions, aspects and Rahu

| Rule | Who | Weight | Evidence |
|---|---|---|---|
| A **conjunction counts within about one nakshatra** (8–11°, up to 13°20′). Same sign beyond that = weak | AG B-4bdoHxkUE mid | strong | "ஒரு எட்டு டிகிரிக்குள்ள 11 டிகிரிக்குள்ள … ஒரு நட்சத்திர தூரத்திற்குள்ள" |
| **Rahu conjunction:** none beyond 22° ("24° is not a conjunction", 26° = safe). Strong ≤13°20′, severe ≤8°, worst ≤6°40′ (half a nakshatra). Inside 12°, Rahu "occupies" the planet | AG hhmRyL1I1uE mid | very strong | "22 டிகிரிக்கு மேல பீடிச்சிருந்தா அந்த கிரகம் இணையவில்லை"; "அரை நட்சத்திர தூரம்" |
| **Approaching vs passed Rahu:** a planet still approaching Rahu (behind it in zodiac order, the two closing in) within ~8° is ruined and its dasa is "out". A planet that has passed Rahu gets back about half its strength, and all of it beyond ~22° or in the next sign | AG hhmRyL1I1uE mid | very strong ("important sootchumam") | "கடந்துவிட்ட கிரகம் பயத்தை இழந்திருக்கும்" |
| If no planet is within orb, **Rahu dasa gives the sign lord's results**, not the co-tenant's | AG hhmRyL1I1uE | strong | "புதனுடைய பலன்களை செய்ய மாட்டார் செவ்வாயுடைய பலன்களை செய்வார்" |
| **Eclipse dosha:** Rahu within 12–13° of the Sun (father) or Moon (mother) → certain. The harm comes in Rahu, Sun or Moon dasa. **Only rescue:** Jupiter aspecting closely, or Venus conjunct → the parent is separated, not lost | AG hhmRyL1I1uE late | very strong | "13 டிகிரிக்கு உள்ளாக … கண்டிப்பாக கிரகணம்"; "அம்மாவை பிரிகிறார் அம்மாவை இழக்கவில்லை" |
| Eclipse orb: SM says **5°** (Sun loses power; planets with it are eclipsed rather than combust) | SM UynI5Yd_MRM | strong | "ராகு அல்லது கேது அஞ்சு டிகிரிக்குள்ள" |
| 9th lord debilitated + eclipse → father lost when Rahu dasa starts. 9th lord in own sign → no immediate loss | AG hhmRyL1I1uE | strong | — |
| **Aspects also need degree closeness:** Jupiter at 26° aspects a target at 28° but not one at 2° of the same sign. No number given | AG hhmRyL1I1uE late-mid | strong, orb unspecified | "குரு 26 டிகிரில இருந்தா புதனுக்கு குரு பார்வை இருக்காது" |
| **Benefic shield within 7°:** a planet within 7° of Venus (or in Chandra adhi yoga) isn't weakened by Rahu in the sign. Within 7° of Saturn → severe papathuvam (from Saturn, not Rahu) | AG hhmRyL1I1uE | strong | "7 டிகிரிக்குள்ள சுக்கிரனோடு" |
| When both Mars and Saturn aspect a planet, **the one closer in degree dominates** | AG B-4bdoHxkUE | strong | "யாருடைய டிகிரி கணக்குகள் மிக நெருக்கமாக" |
| The Moon's benefic aspect is first-level when near full and within ~9–10° | AG IkwQSU3TkjI mid | medium | "10 9°க்குள்ள சந்திரனுடைய பார்வை" |
| Transit Ketu must be **≥10° past the natal 7th lord's degree** before a marriage | BM TLwS74-cUk0 | strong | "10 டிகிரி மேல் கோச்சாரக் கேது தாண்டின பிறகுதான்" |

### 2.3 Sandhi and degree dignity

| Rule | Who | Weight | Evidence |
|---|---|---|---|
| A sign works only between **5° and 25°**. 0–5° and 25–30° = sandhi (lagna, Moon, every planet) | SM 7dwGayLka2A | very strong | "5 டிகிரிக்கு மேல … 25° வரைக்கும்" |
| Lagna in sandhi = results of neither sign. **Rescued if the lagna lord is mid-sign and strong.** Otherwise use the lagna lord's sign as lagna (~70% accurate) | SM 7dwGayLka2A | strong | "ரெண்டும் கெட்டான் நிலை" |
| An exalted planet near the end of its sign loses ~90% of the exaltation | SM 7dwGayLka2A | strong | "உச்சம்ங்கிற வலிமையை கிட்டத்தட்ட 90% இழந்து" |
| **Moon in sandhi → gochara from the adjacent rasi applies** (ashtama Sani hit from Mithuna for an early-Kataka Moon) | SM 7dwGayLka2A | strong | "மிதுன ராசிக்கு அஷ்டம் சனி நடக்கும்போதே" |
| **Paramocha / paraneecha degrees matter:** the Sun past Thula 20° isn't treated as debilitated. Jupiter is "truly good" at Kataka 5° | AG 6--6FzUx8Vs early | strong | "துலாத்தின் 20 டிகிரிக்கு பிறகு சூரியனை நான் நீச்சமாக எடுக்க மாட்டேன்" |
| Baladi avastha, odd signs: 0–6° ¼, 6–12° ½, 12–18° full, 18–24° weak, 24–30° worst. Reversed in even signs | Phaladeepika (Wikipedia) | classical | — |

### 2.4 Retrograde (vakram)

| Rule | Who | Weight | Evidence |
|---|---|---|---|
| Retrograde matters strongly only for Mars, Jupiter and Saturn. Mercury and Venus count only if they rule the lagna | SM H7r5Pn5t7jY | medium | "செவ்வா குரு சனி இவர்களின் வக்கிரம் ரொம்ப உணரும்" |
| **Success markers:** retrograde lagna lord, dasa lord, 2nd lord or 5th lord; a retrograde planet in the lagna; Mars, Jupiter and Saturn all retrograde. Malefics + retrograde = "next level" | SM H7r5Pn5t7jY | strong (his thesis) | "லக்னாதிபதி வக்கிரம் அடைந்திருந்தாலும்" |
| **Retrograde counts only with dignity** (exalted, own sign or debilitated). Otherwise ignore it | AG xEGMK5jR81I early | strong | "உச்சவக்கரம் ஆட்சி நீச்ச வக்கிரம் மட்டும் எடுத்து கொள்ளலாம்" |
| Exalted + retrograde ≈ debilitated, and debilitated + retrograde ≈ exalted ("commentary texts"), but as an "abnormal state", not a true swap | AG xEGMK5jR81I; Phaladeepika and Uttara Kalamrita (Wikipedia) | strong, classical | "நீச்ச வக்கிரம் என்பது உச்சத்திற்கு சமமானது … விளக்க நூல்கள்ல இருக்கு" |
| **For Saturn:** exalted + retrograde + aspected by Jupiter/Venus (or a lone Mercury) = good ("level 3"). **Debilitated + retrograde Saturn = bad** (karakas amplified) | AG xEGMK5jR81I | strong | "நீச்ச வக்கரம் அடையவே கூடாது" |
| Saturn in the 6/7/8 from the Sun is surely retrograde | AG xEGMK5jR81I | astronomical | — |
| **Natal retrograde planet gives its results only when it is also retrograde in transit.** It then gives MORE of its natal good or bad | KV SZwJ4wnfONg mid; BM TLwS74-cUk0 (5.16) | strong, two channels agree | "பிறந்த கால கிரகமும் கோச்சார கிரகமும் ஒரே தன்மையில் இருக்கும் பொழுது மட்டுமே" |
| **Natal-direct dasa or bhukti lord that is retrograde in transit → matters stall** (marriage, house, business, loans). Wait for it to turn direct | KV SZwJ4wnfONg mid-late | strong, practical | "வக்கர நிவர்த்தி ஆகும் வரை காத்திருந்து" |
| Natal retrograde dasa lord that is direct in transit → results don't flow | KV SZwJ4wnfONg | strong | — |
| A retrograde bhukti lord counts as afflicted | PC G-axQirK2j4 | medium | "வக்கிரமாகாம" |
| Transit Rahu/Ketu over a natal retrograde planet does little harm | KV SZwJ4wnfONg | medium | — |
| Retrograde Venus → unfulfilled married life. 3+ retrograde planets → engagements fixed and broken repeatedly | KV SZwJ4wnfONg | medium | — |
| Character: rigid in the retrograde planet's karakas, doesn't take advice | KV SZwJ4wnfONg | medium | — |
| Transit Moon over a natal retrograde planet = harm (prasna) | BM TLwS74-cUk0 | medium | — |
| Saravali: retrograde benefics give kingship, retrograde malefics misery. Uttara Kalamrita: a planet conjunct a retrograde planet has its strength **halved**. Sanketa Nidhi: a retrograde planet gives the results of the 3rd (Mars), 4th (Mercury), 5th (Jupiter), 7th (Venus) or 8th (Saturn) house from where it sits | Wikipedia | classical | — |

### 2.5 Neecha bhanga (NB) vs neecha bhanga raja yoga (NBRY)

| Rule | Who | Weight |
|---|---|---|
| A debilitated planet keeps ~10% strength, not zero. A debilitated Venus still gives a spouse; only an afflicted Venus denies one | AG IkwQSU3TkjI | medium-strong |
| **NBRY:** the debilitated planet is conjunct or aspected by an **exalted** planet, or sits in another planet's exaltation sign (Mars in Kataka) | AG IkwQSU3TkjI late ("உச்சனோடு இணைவது என்பது நீச்சபங்க ராஜயோகம்") | strong |
| **NB only:** conjunct an own-sign planet; dispositor in own or exalted sign (ambiguous); parivartana; in a kendra from the lagna or Moon | AG IkwQSU3TkjI ("ஆட்சி பெற்ற கிரகத்தோடு இணைவது நீச்சபங்கம் மட்டுமே") | strong |
| Dispositor in a kendra from the lagna or Moon; the planet exalted in the debilitation sign in a kendra; exchange or mutual aspect with the dispositor; debilitated + retrograde ("some traditions") | onlinejyotish | written |
| NBRY pays **only in the NB planet's dasa** (or Rahu/Ketu dasa when they sit in its sign). Its karakatvam still helps lifelong | AG IkwQSU3TkjI | strong |
| **Capped by the lagna and lagna lord** ("a beggar with NBRY begs comfortably") | AG IkwQSU3TkjI | very strong |
| **Fails** if the NB planet is with Rahu, combust, eclipsed, or aspected by an enemy. In 6/8/12 it works on a smaller scale | AG IkwQSU3TkjI | strong |
| A proper NBRY planet scores "120 marks" vs exalted 100 (AG's own claim, "not in the root texts") | AG IkwQSU3TkjI | his signature |
| Sun NBRY = authority, not money. Money needs a link to houses 2/9/11 | AG IkwQSU3TkjI | strong |
| Fruit after age ~30–35 | onlinejyotish | written |
| In transit, high own-BAV bindus override debility (Jupiter in Makara with 5 bindus gives big results) | GK Q2y_3nlXXU0 | strong |

### 2.6 Subhathuvam / papathuvam scoring (AG, VV)

| Rule | Where | Weight |
|---|---|---|
| Benefic sources: Jupiter (strongest), Venus, bright or full Moon, lone Mercury. Malefic: Saturn (full), Rahu (full; acts like Saturn), Ketu (like Mars), Mars (¾), new Moon, Sun-combustion | AG hhmRyL1I1uE, 6--6FzUx8Vs; VV | core |
| **For a malefic, a benefic's aspect beats its conjunction** | AG xEGMK5jR81I ("இணைவதை விட பார்ப்பது மிகப்பெரிய நல்ல யோகம்") | strong |
| **"Papathuvam first, then subhathuvam":** a planet with both malefic affliction and Jupiter's aspect gives a fall early in its dasa and recovery in roughly the last 3 years | AG B-4bdoHxkUE, guLFf_JW0sk ("அடிச்சு மிதிச்சதுக்கு அப்புறம் கட்டுப்போடுறது தான் குரு") | very strong |
| **A full Moon's aspect or conjunction flips a malefic to strongly good**, whatever its star (Rishabha: Mars in the 10th with a full Moon → Mangala yoga plus dig bala) | AG B-4bdoHxkUE | strong |
| **Moon phase decides the nakshatra's promise:** "born in Magam, rules the world" only with a full Moon | AG B-4bdoHxkUE | strong |
| **At most 8 houses can be subha:** Jupiter covers 4 (sits in 1, aspects 3), Venus 2, a bright Moon 2, minus overlaps. The remaining houses bring trouble in their dasa-bhuktis | AG guLFf_JW0sk | strong |
| **Excess benefic spoils:** a natural benefic that is exalted and vargottama (Jupiter, Venus, full Moon) gives only ordinary results. Jupiter + waxing Moon or Jupiter + Venus heavily subha in one house spoils that house (8th → longevity, only if the lagna lord, Saturn and the 8th lord are also weak) | AG 6--6FzUx8Vs | strong |
| A new Moon with Jupiter eats 30–40% of Jupiter's light. Add Rahu → Jupiter dasa is total loss | AG guLFf_JW0sk | strong |
| **Mutual 7th, Jupiter–Saturn:** Jupiter's goodness falls and Saturn's malefic nature is removed. Linked to the lagna or Moon sign (esp. Saturn's signs, or Moon/Ketu involved) → spirituality, even sanyasa | AG guLFf_JW0sk | very strong |
| **Sun + Saturn together are never good** (a root rule; parivartana doesn't fix it) | AG hhmRyL1I1uE ("மூலவிதி") | very strong |
| **Saturn in the 10th spoils career** even in its own sign. Exception: Jupiter's aspect | AG guLFf_JW0sk | strong |
| Saturn shouldn't be strong. An exalted or own-sign Saturn is good only if hidden in 6/8/12, with Ketu (full "sookshma valu") or Mars (partial), or retrograde with a benefic aspect | AG xEGMK5jR81I | strong |
| Saturn's aspect gives lordship benefits but karaka damage. On the occupied house: Rahu spoils ~100%, Saturn 60–70%. With Jupiter's aspect, Saturn grows the house | AG B-4bdoHxkUE | strong |
| **Rahu good only with Jupiter's aspect or Venus beside it; bad with Saturn or Mars.** Rejects "Rahu good in 3/6/11" and the verse "ஆமேடம் எருது சுறா நண்டு கன்னி" (Rahu good in Mesha, Rishabha, Makara, Kataka, Kanni) | AG hhmRyL1I1uE early | very strong |
| A **lone Rahu in the 6th protects** (no debt, disease or enemies). Rahu in the 6th with Saturn there and Mars aspecting = severe 6th-house trouble | AG B-4bdoHxkUE | strong |
| Rahu in a kendra with a trikona lord, or in a trikona with a kendra lord, gives good results even if afflicted (classical, Uttara Kalamrita). Best with the 9th and 10th lords; strength scales with closeness | AG hhmRyL1I1uE late | very strong |
| Rahu/Ketu have no lordship and no karakatvam of their own. Rahu acts like Saturn, Ketu like Mars. Ketu acts as its sign lord and also takes that lord's aspect | AG hhmRyL1I1uE, B-4bdoHxkUE | strong |
| A malefic hidden in 6/8/12 is good only with exaltation or benefic contact. An afflicted lagna lord in 6/8/12 with benefic contact is fine | AG guLFf_JW0sk | strong |
| **A benefic in a trine is best, a malefic in a kendra is best** | VV FfwKFx6dxOg mid | strong |
| An 8th lord with benefic contact does no harm; it moves the native far away, abroad or to another state. 8th + 12th both subha → lives 500+ km from the birthplace | VV FfwKFx6dxOg; AG B-4bdoHxkUE, p4lBTymR8GM | medium-strong |
| **Career = the planet with the most subhathuvam, plus its sign's nature.** In avayoga dasas, the second most | AG IkwQSU3TkjI ("my most important rule") | very strong |
| **Chandra adhi yoga:** Jupiter, Mercury or Venus in 6/7/8 from the Moon. Saturn or Mars there = papa adhi yoga, which softens their dasas. Sun and the nodes never form it | AG IkwQSU3TkjI | medium-strong |
| Mars's 8th aspect spoils the lagna by ~25%. A waxing Moon aspecting the lagna makes it subha | AG hhmRyL1I1uE, guLFf_JW0sk | medium |
| **Karakatvam acts lifelong; lordship acts in the dasa** | AG guLFf_JW0sk | very strong |
| A lord placed 3/6/8/12 from its own houses is "hidden" from them; its dasa runs only the house it occupies | AG guLFf_JW0sk | medium |
| A steady life (no big falls) = strong lagna lord with no planets 6th or 8th from it | AG B-4bdoHxkUE | strong |

### 2.7 Dasa-bhukti judgement

| Rule | Who | Weight | Evidence |
|---|---|---|---|
| **Bhukti lord counted from the dasa lord (both ways): 6/8/12 → bad bhukti even if the planet is strong.** 6/8 (shashtashtaka) is worst | PC G-axQirK2j4 (core); AG guLFf_JW0sk G12 ("அவமானம் அசிங்கம்"); AG IkwQSU3TkjI | very strong, 2 channels agree | PC "சந்திரனுக்கு ஆறாம் இடத்துல புதன் … சஷ்டாஷ்டகம்" |
| Exception: a planet in its own sign isn't "hidden" from the other lord | PC G-axQirK2j4 | medium | "அங்க சூரியன் ஆட்சி அப்ப மறைவு கிடையாது" |
| Bhukti lords in a kendra or trikona from the dasa lord carry the dasa's theme (marriage comes in such bhuktis). A strong bhukti lord 12th from the dasa lord can relieve | AG B-4bdoHxkUE | strong | "கேந்திர கோண சூத்திர அமைப்புகளுக்கு உள்ளதான் நீங்க போகணும்" |
| Check: dasa lord from lagna, bhukti lord from lagna, and their mutual position; none in 6/8/12 = perfect | PC G-axQirK2j4 | very strong | — |
| The badhaka lord of the dasa lord's sign joining the bhukti lord makes it worse | PC G-axQirK2j4 | supporting | — |
| **In Rahu dasa, the Sun, Moon and Mars bhuktis are always weak or mixed** | AG IkwQSU3TkjI | medium-strong | "ராகு தசையில சூரிய சந்திர செவ்வா புக்திகள் சரியாக இருக்காது" |
| Moon + Saturn conjunction → Moon, Saturn and Rahu bhuktis fail. Without Jupiter's aspect they "bring him to the street" | AG guLFf_JW0sk | strong | — |
| Even in a strong chart, a 6th lord's dasa runs 6th-house matters (debt, disease) | AG guLFf_JW0sk | strong | — |
| **Every dasa verdict is finalised by lagna-lord strength** | AG guLFf_JW0sk G20, IkwQSU3TkjI | very strong | "எல்லா தசைக்கும் … லக்னாதிபதி உடைய அமைப்புகளுக்கு ஏற்ப" |
| Vimshottari only from the Moon's star; starting from the lagna's star is wrong | AG 6--6FzUx8Vs | very strong (engine already does this) | — |
| Rasi chart for dignity and aspects. The bhava (chalit) chart only says which house a planet delivers in its own dasa | AG 6--6FzUx8Vs | strong | "பாவக கட்டத்துல பார்வை எல்லாம் கிடையாது" |
| An 8th-lord dasa → "shortcut" contacts. A following subha Saturn dasa turns them into industry | AG B-4bdoHxkUE | low-medium | — |

### 2.8 Gochara (transits)

| Rule | Who | Weight |
|---|---|---|
| **Janma, ashtama and 7½ Sani dampen even a raja-yoga dasa.** Slight in a strong dasa, noticeable in a medium one, **total failure in a dasa or bhukti tied to 6/8/12** | AG 7tkh40yJG_A early | very strong |
| **During janma or ashtama Sani, Jupiter's good transits (2/5/7/9/11) give nothing** | AG 7tkh40yJG_A | very strong |
| **The dasa lord's own transit modulates its dasa:** exalted → extra good, debilitated → weak, with transit Saturn or Rahu → weak, in benefic signs → good. Saturn dasa, by transit sign: Kataka, Simha and Vrischika disturbed; Rishabha, Mithuna, Kanni and Thula good; Dhanus to Meena moderate. Moon dasa dips on waning, Vrischika or Saturn/Rahu days | AG 7tkh40yJG_A late | very strong |
| Good houses from the Moon: Sun 3/6/10/11; Moon 1/3/6/7/10/11 (1 only if bright); Mars, Saturn, Rahu, Ketu 3/6/11; Mercury 2/5/8/11 (his experience) vs 2/6/8/10/11 (texts); Jupiter 2/5/7/9/11; Venus all except 6/7/10 | AG 7tkh40yJG_A mid | standard |
| **Vedha:** ashtama Sani is cancelled if transit Jupiter or Rahu/Ketu is 7th from the Moon. Full table not given | AG 7tkh40yJG_A mid | strong but incomplete |
| A malefic in 3/6/11 from the Moon gives strong good only in a **benefic's sign with transit Jupiter's contact** | AG 7tkh40yJG_A late | strong |
| **Transit Saturn + Rahu together harm whichever house (from the Moon) they fall in** | AG 7tkh40yJG_A | strong |
| Gochara is a "subsidiary textbook". Timing comes from dasa-bhukti | PC G-axQirK2j4 | strong |
| Transit over natal: Saturn over the Sun → boss troubled by staff; Sun over Saturn → staff troubled, no increment; Saturn over its enemies (Sun, Moon, Mars, Ketu) bad, over benefics good. A transit planet over a natal friend in 1/5/9/7 good, over an enemy bad | BM TLwS74-cUk0 | medium |
| **Marriage:** transit Jupiter aspecting natal Jupiter and Venus, with no Ketu link. Transit Saturn trine to natal Mars → late marriage | BM TLwS74-cUk0 | strong |
| Prasna: the matter fails if the karaka or the transit Moon touches the nodes or is debilitated. Natal/transit Moon in 6/8 = bad. Transit Moon over natal Moon = success | BM TLwS74-cUk0 | medium |
| Muhurtham don'ts (month of the Sun in Rahu's natal sign, etc.) | BM TLwS74-cUk0 | medium |
| Chandrashtamam = "64th pada from the janma pada" as stated (usually the 8th sign or 88th pada): **unclear** | BM TLwS74-cUk0 | flag |

### 2.9 Ashtakavarga

| Rule | Who | Weight |
|---|---|---|
| 7 planets only (no nodes). SAV total 337, average 28 | GK Q2y_3nlXXU0; SS gVw_5jRQGeE | baseline |
| Stronger for gochara than for the natal chart. It changes the **amount**, not the nature (~90% indicative) | GK Q2y_3nlXXU0 | strong |
| **Transit sign SAV:** GK says >25 good, <20 very bad, ~20 gives almost nothing. SS says >30 good for any planet, 25–30 good, <25 bad | GK, SS | strong, thresholds differ |
| **Own BAV:** transit Saturn through a low-bindu sign hurts life, career and karakas; a 6–7 bindu sign is very good. 5 bindus cancel transit debility. 1 bindu = hurts | GK Q2y_3nlXXU0 | strong |
| **7½ Sani shield:** any of the 12th, 1st or 2nd from the Moon with SAV >30 → no big suffering | SS gVw_5jRQGeE | strong |
| Longevity: SAV(1) > SAV(8) → long life | SS | strong |
| Income: SAV of houses 1,2,4,9,10,11 > 164 → income exceeds expense. SAV of 6,8,12 > 76 → expense exceeds income | SS | medium-strong |
| Aham (1,4,7,10,5,9) > Puram (2,6,8,12,11) → content. Bandhukam 1,5,9 / Sevakam 2,6,10 / Poshakam 3,7,11 / Kaathakam 4,8,12 (heard "1,4,8,12"): Poshakam < Kaathakam → poverty; Bandhukam < Sevakam → government job | SS | medium |
| A low sign next to a high sign → sudden ups and downs. Spouse or partner from your max-SAV sign | SS | medium / weak |
| Kakshya timing: a transit works most in the same sign portion its natal self occupies. Heard as 4 × 7.5°; classical is 8 × 3.75° | GK | medium, unclear |

### 2.10 Saaram, own star, badhaka, KP

| Rule | Who | Weight |
|---|---|---|
| Order: lordship → house occupied → karakatvam = 90%. The star lord adds 5–10%, never flips good or bad, only chooses the "channel" houses | SM LScFPAYw6U0 | strong |
| Star lord = Rahu/Ketu → use the node's dispositor | SM LScFPAYw6U0 | medium |
| Own star = a pure, full result of the planet's own lordship. Only the Moon really transmits nakshatra effects | SM LScFPAYw6U0, XAU7TjRG8Gk | medium |
| Own-star goodness: Sun 100%, Jupiter 100%, Moon 75%, Venus 75%, Ketu 70%, Mars 60%, Saturn 50%, Mercury 40% (table in parts/A.md) | SM XAU7TjRG8Gk | low-medium |
| A lagna lord in the star of the 6th, 8th or 11th lord = gains with fights. A mixed lord acts as its dusthana lordship | SM LScFPAYw6U0 | medium |
| A star lord "hidden" in 6/8/12 or debilitated does **not** decide results | VV FfwKFx6dxOg | strong |
| The bhukti lord's star lord being hidden = a minor extra affliction | PC G-axQirK2j4 | medium (ASR shaky) |
| **Badhaka:** movable lagna 11th, fixed 9th, dual 7th. Harm comes through the badhaka lord's karakas plus its occupied house. Fixed lagnas: "a friend turns enemy". Full table in parts/A.md §3 | SM oDYVvqe1gTI | medium |
| **KP sub:** 9 subs per star, span = 13°20′ × years/120, starting from the star's own lord. No judgement rules taught | KP 7vpSOvYp4Ds | construction |

---

## 3. Order of judgement (explicit procedures)

- **SM (LScFPAYw6U0):**
  1. Lordship.
  2. House occupied.
  3. Karakatvam (90% done here).
  4. Star lord (5–10%).
  5. Benefic contacts and lagna-lord strength set whether all this comes out good or bad.
- **AG (B-4bdoHxkUE, guLFf_JW0sk, IkwQSU3TkjI):**
  1. Lagna and lagna lord (the "level" the native is born to).
  2. Subhathuvam/papathuvam of each planet (aspects, conjunctions in orb, Moon phase, closest degree).
  3. The most subha planet gives the profession.
  4. Lordships plus Rahu/Ketu "acts like".
  5. Dasa, then bhukti via kendra/kona/6-8/12 from the dasa lord.
  6. Malefic results first, repair later.
  7. Gochara: dasa quality, then Saturn from the Moon (overrides), then the house table, vedha and transit subhathuvam, then the dasa lord's own transit.
  8. Finalise with lagna-lord strength.
  9. Ignore stars, except the Moon's star for the dasa.
- **VV (FfwKFx6dxOg):**
  1. Lagna.
  2. Lagna lord.
  3. Is the dasa planet a yoga planet or an avayoga planet for this lagna?
  4. Its subhathuvam or papathuvam.
  5. House and lordships.
  6. Aspects given and received, and conjunctions.
  7. Saaram last, as a minor factor.
- **PC (G-axQirK2j4):**
  1. Lordship from lagna.
  2. Dasa lord and bhukti lord from lagna: are they in 6/8/12?
  3. Bhukti lord from the dasa lord, both ways (own-sign exception).
  4. Retrograde or afflicted bhukti lord, or its star lord hidden.
  5. Badhaka of the dasa lord's sign.
  6. Gochara last.
- **AG for Saturn (xEGMK5jR81I):**
  1. Dignity.
  2. Hidden in 6/8/12, or in a kendra/kona?
  3. Retrograde?
  4. Benefic aspect, then benefic conjunction.
  5. Lordship, then karaka.

---

## 4. Agree vs disagree across channels

| Topic | Agree | Disagree |
|---|---|---|
| **Star lord** | SM, AG, VV and PC all refuse to let the star lord decide dasa quality | **AG and VV: zero weight** (even for the nodes). **SM: ~5%, picks the channel; node star → dispositor.** PC: uses a hidden star lord as an extra affliction. Eshwar P14: a star lord can create a yoga. The engine uses it fully for topics |
| **Combustion orb** | All: closeness to the Sun weakens. Mercury exempt (SM, AG ×2). Nodes are never combust (shubhpanchang) | **SM 5° flat · AG 9° zone graded (6--6FzUx8Vs) · AG per-planet Mars 17 / Saturn 15 / Jupiter 11 / Venus 9 (hhmRyL1I1uE).** AG itself is inconsistent. A workable reconciliation: AG's per-planet orb = "touched", 9° = "noticeable" (−30%), ≤5° = "real loss" (SM and AG agree on 5° as the severe core) |
| **Combust planet's aspect** | — | SM: the aspect is lost. AG: kept unless ≤1° |
| **What combustion is** | SM, AG: it weakens and makes the native dependent on others | AG 6--6FzUx8Vs: like debilitation, not malefic. AG hhmRyL1I1uE: "combustion is papathuvam" |
| **Combustion cancellation** | Both use strong benefics | SM: own or exalted sign, exalted dispositor, Jupiter's aspect, exalted contact. AG: full Moon opposite, or uncombust Venus within 10–15°. No overlap; union them |
| **Retrograde** | SM, AG, KV and Eshwar all treat it as meaningful. KV and BM agree on the natal-retro × transit-retro rule | **SM: retrograde = success** (especially malefics). **AG: only counts with dignity; debilitated + retrograde Saturn is BAD.** Phaladeepika: exalted + retro ⇒ like debilitated. Saravali: retrograde malefics → misery. PC: a retrograde bhukti lord = afflicted |
| **Rahu in 3/6/11** | The engine and classical tables say good | **AG rejects it** (Rahu in the 6th with Mars → beggar). AG: a lone Rahu in the 6th protects, but not with Saturn and Mars |
| **Node orbs** | All use degree orbs | SM eclipse ≤5°. AG eclipse ≤12–13°, conjunction ≤22°, severe ≤8°. Eshwar: Jupiter–Rahu ≤15° afflicted, ≤13° seized. AG's 13°20′ ≈ Eshwar's 13° (**agree**) |
| **Neecha bhanga** | Dispositor-based conditions appear in AG, onlinejyotish and Eshwar | **AG: an exalted contact = NBRY; an own-sign contact = NB only.** Eshwar: dispositor exalted = NBRY. onlinejyotish: dispositor in a kendra = NB. AG adds the dasa-only, lagna-capped and fails-with-Rahu-or-combust conditions |
| **Bhukti from dasa lord** | **PC and AG agree:** 6/8 shashtashtaka is the worst; kendra/kona from the dasa lord is good | PC: 12th also bad (own-sign exception). AG: a 12th-placed strong bhukti lord can relieve |
| **Sandhi** | SM's 0–5° / 25–30° roughly matches baladi (weak at the edges) | Width 5° vs 6°; baladi is asymmetric by odd/even sign |
| **Ashtakavarga threshold** | Both: higher SAV in the transit sign = better | GK: <20 bad, >25 good. SS: <25 bad, >30 very good |
| **Mercury transit houses** | — | AG's experience 2/5/8/11 vs textbook 2/6/8/10/11 |
| **Vargottama** | — | AG: vargottama adds no real strength, and exalted + vargottama benefic = too much. Eshwar and classical treat it as strength |
| **Badhaka** | SM's table = classical. Eshwar P10 and PC also use it | — |
| **Gochara weight** | PC and AG: dasa first, transit modulates | AG: a bad Saturn transit can wreck a 6/8/12 dasa entirely (stronger than PC's "side check") |

---

## 5. What's NEW vs the engine (ranked)

Inputs: sidereal Lahiri `L[p]`, speeds `S[p]`, `Asc`. Natal + transit longitudes and speeds (the engine already computes transits).

1. **Bhukti-from-dasa-lord test** (PC G-axQirK2j4; AG guLFf_JW0sk, B-4bdoHxkUE): `r = rel(dasa, bhukti)`.
   - `r in {6,8}` → strong minus (shashtashtaka).
   - `r == 12 or rel(bhukti, dasa) == 12` → minus, unless the hidden one is in its own sign.
   - `r in {1,4,5,7,9,10}` → carries the dasa theme (marriage bhuktis).
   - Apply the same test to antaram vs bhukti (extension).
   - Cheap, two channels agree, and it directly addresses the "can't separate job windows" gap in method.md.
2. **Gochara × dasa severity + the dasa lord's own transit** (AG 7tkh40yJG_A):
   - Saturn in 12/1/2/8 from the Moon: dent a Good tone, cut Mixed, and make a dasa or bhukti tied to 6/8/12 Tough.
   - During janma or ashtama Sani, zero the Jupiter-transit bonus.
   - Transit dignity of the dasa lord: exalted +, debilitated −, same sign as transit Saturn or Rahu −.
   - Transit Saturn + Rahu in one sign → harm that house from the Moon.
   - Vedha: ashtama Sani is cancelled by transit Jupiter or Rahu/Ketu 7th from the Moon.
   - SAV shield: any of the 12th, 1st or 2nd from the Moon with SAV >30 softens 7½ Sani (SS).
3. **Retrograde × transit-retrograde matrix for dasa/bhukti lords** (KV SZwJ4wnfONg; BM TLwS74-cUk0). `nR = S_natal<0`, `tR = S_transit<0`:
   - nR and tR → amplify the natal verdict.
   - nR and direct → mute.
   - direct and tR → "pending / wait for station-direct" flag (give that date).
   - Natal retrograde planet hit by transit nodes → damp the harm.
   - Natal dignity rule (AG): count retrograde only when exalted, own or debilitated. Exalted + retro Saturn with a benefic aspect = good; debilitated + retro Saturn = bad.
4. **Combustion graded**: `c = d(L[p], L[Sun])`, p ∉ {Mercury, Rahu, Ketu, Moon}.
   - c ≤ 5 → heavy loss (SM + AG).
   - 5 < c ≤ 9 → −30% (AG).
   - Up to the per-planet orb (Mars 17, Saturn 15, Jupiter 11, Venus 9) → mild.
   - Cancel or soften: own or exalted sign, exalted dispositor, Jupiter aspect, exalted contact (SM); full Moon 6/7/8 from it, uncombust Venus within 15° (AG).
   - The Sun inherits the combust planet's results. Sun combusting Jupiter → Sun dasa good even as a bad lord (AG).
   - Combust lagna lord → "dependent" character line. Venus combust → nodes in Rishabha/Thula give Venus results.
   - Moon: `d ≤ 5` = amavasya, weak unless in Mesha, Rishabha, Kataka or Simha.
5. **Rahu degree engine** (AG hhmRyL1I1uE):
   - `dr = norm180(L[p] − L[Rahu])`. Contact only if `|dr| ≤ 22`. Severe ≤8, worst ≤6.67.
   - `dr < 0` (approaching) → p's dasa heavily minus.
   - `dr > 0` (passed) → p at ~50% within 13.3°, recovered beyond 22° or in the next sign.
   - Rahu dasa = sign lord's results if nothing is in orb.
   - Eclipse dosha `d(Sun|Moon, node) ≤ 12` → father/mother caution in Rahu, Sun or Moon dasa, unless Jupiter aspects or Venus is within ~12°.
   - **Replace** "Rahu good in 3/6/11" with: good if Jupiter aspects (in orb) or Venus conjunct; bad if Saturn or Mars (in orb); plus Rahu in a kendra with a trikona lord, or in a trikona with a kendra lord = good.
6. **Neecha bhanga split** (AG IkwQSU3TkjI + onlinejyotish):
   - NBRY if the debilitated planet is conjunct or aspected by an exalted planet, or sits in another planet's exaltation sign. NB-only if conjunct an own-sign planet, in parivartana, or in a kendra from the lagna or Moon.
   - A debilitated planet keeps ~10% strength.
   - NBRY bonus only in that planet's dasa, capped by lagna-lord strength.
   - Void if with Rahu, combust or eclipsed. Scaled down in 6/8/12.
   - Debilitated + retrograde → NB (classical; but AG: bad for Saturn).
7. **Sandhi** (SM 7dwGayLka2A): `x < 5 or x > 25`.
   - Discount dignity heavily (an exalted planet near the end loses ~90%).
   - Lagna in sandhi: ignore if the lagna lord is mid-sign and dignified. Otherwise flag "rectify" and also read from the lagna lord's sign.
   - Moon in sandhi: also run Sani and Jupiter gochara from the adjacent rasi.
   - Paramocha nuance: the Sun past Thula 20° isn't debilitated (AG).
8. **Subhathuvam score** (AG, VV) as a planet-quality term next to functional nature:
   - +Jupiter aspect or conjunction (in orb), +Venus, +bright Moon (`(Moon−Sun) mod 360` ≈ 120–240°), +lone Mercury.
   - −Saturn, −Rahu, −Mars (¾), −new Moon. Aspect > conjunction for malefic targets.
   - The closest-degree malefic dominates.
   - Both malefic and benefic → split the dasa: early bad, last ~3 years good.
   - The most subha planet = career theme.
   - Special aspects needed: Mars 4/8, Jupiter 5/9, Saturn 3/10.
9. **Special pair rules** (AG): Sun + Saturn never good. Moon + Saturn → Moon, Saturn and Rahu bhuktis fail without a Jupiter aspect. Jupiter–Saturn in mutual 7th → Jupiter −, Saturn cleaned, spiritual if linked to the lagna or Moon. Saturn in the 10th = career strain unless Jupiter aspects. Exalted Saturn good only if in 6/8/12, with Ketu, or retrograde with a benefic aspect. In Rahu dasa, the Sun, Moon and Mars bhuktis are weak.
10. **Ashtakavarga** (GK, SS): compute BAV and SAV with the standard BPHS tables.
    - Transit sign SAV <25 bad, >28–30 good. Own BAV ≥5 cancels transit debility; ≤1 hurts.
    - SAV(1) > SAV(8) = longevity. Houses 1+2+4+9+10+11 >164 = net income. Houses 6+8+12 >76 = net expense.
11. **Lagna gate** (AG, VV): multiply yoga and dasa upside by lagna-lord strength.
12. Badhaka lord flavour lines (SM, PC). Chandra adhi yoga and papa adhi yoga (AG). An 8th lord with benefic contact → gains through distance (VV, AG). Benefic in a trine and malefic in a kendra bonus (VV). Exalted + vargottama benefic = "ordinary" (AG).
13. **Downweight the star lord** in tone. Keep it only as a "channel" for topic houses (SM), or behind a per-school setting (AG/VV = off).
14. Transit-contact marriage rules (BM): transit Jupiter aspecting natal Jupiter + Venus with no Ketu link; Ketu ≥10° past the 7th lord. KP sub-lord computation (construction only).

**Not encodable / unclear:** "same-degree 7th aspect" (title only, nothing spoken); AG's aspect orb (no number); chandrashtamam as the "64th pada"; kakshya split; graha yuddham (no usable source); AG's 120-mark scoring (vague).
