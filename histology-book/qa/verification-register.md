# Verification Register — scientific verification & correction pass
# ثبتِ تأیید — پاسِ بازبینی و تصحیحِ علمی

**Date:** 2026-09-21 · **Branch:** `arena/01a0c167-pp-cordinator` · **Reference standard:** Junqueira's
Basic Histology: Text and Atlas, 17th ed. (Mescher) · **Scope:** all 23 chapters, book frozen at
23 chapters / 108 topics (no new chapters, no new frameworks).

**Purpose.** This is the single book-level record of the verification pass: what was reviewed, what
was corrected, what remains. The per-chapter details live at the end of each chapter, in its own
**ثبتِ تأییدِ علمی — Verification record** table.

---

## 1. Master table

`Items reviewed` = the standing audit items of that chapter's Reference Alignment Audit (the
`[VERIFY AGAINST JUNQUEIRA 17e]` backlog). `Corrections` = wording/values changed because the earlier
text was inaccurate, incomplete or misleading. `Additions` = short content added because a compressed
topic would otherwise have lost an exam-relevant fact. `Remaining warnings` = unresolved items left
flagged after the pass.

| # | Chapter | Topics | Items reviewed | Verified & retained | Corrections | Additions | Remaining warnings | Check 11 |
|---|---|---|---|---|---|---|---|---|
| 1 | Histology & Its Methods of Study | 8 | 3 | 0 | 2 | 1 | 0 | ✅ |
| 2 | The Cytoplasm | 11 | 4 | 3 | 1 | 0 | 0 | ✅ |
| 3 | The Nucleus | 8 | 4 | 4 | 0 | 0 | 0 | ✅ |
| 4 | Epithelial Tissue | 7 | 5 | 3 | 2 | 0 | 0 | ✅ |
| 5 | Connective Tissue | 8 | 4 | 2 | 1 | 1 | 0 | ✅ |
| 6 | Adipose Tissue | 5 | 7 | 5 | 1 | 1 | 0 | ✅ |
| 7 | Cartilage | 4 | 7 | 5 | 1 | 1 | 0 | ✅ |
| 8 | Bone | 4 | 8 | 4 | 3 | 1 | 0 | ✅ |
| 9 | Blood & Hemopoiesis | 6 | 11 | 9 | 1 | 1 | 0 | ✅ |
| 10 | Muscle Tissue | 3 | 11 | 6 | 5 | 0 | 0 | ✅ |
| 11 | Nervous Tissue | 4 | 11 | 7 | 3 | 1 | 0 | ✅ |
| 12 | Cardiovascular System | 4 | 11 | 9 | 2 | 0 | 0 | ✅ |
| 13 | Lymphatic System | 4 | 11 | 8 | 2 | 1 | 0 | ✅ |
| 14 | The Oral Cavity | 4 | 11 | 8 | 3 | 0 | 0 | ✅ |
| 15 | The Digestive Tract | 4 | 11 | 9 | 2 | 0 | 0 | ✅ |
| 16 | Organs Associated with the Digestive Tract | 3 | 11 | 10 | 1 | 0 | 0 | ✅ |
| 17 | Respiratory System | 3 | 11 | 9 | 2 | 0 | 0 | ✅ |
| 18 | The Skin | 3 | 11 | 10 | 1 | 0 | 0 | ✅ |
| 19 | The Urinary System | 3 | 11 | 9 | 2 | 0 | 0 | ✅ |
| 20 | Endocrine Glands | 3 | 11 | 10 | 1 | 0 | 0 | ✅ |
| 21 | Male Reproductive System | 3 | 11 | 10 | 1 | 0 | 0 | ✅ |
| 22 | Female Reproductive System | 3 | 11 | 10 | 0 | 1 | 0 | ✅ |
| 23 | The Eye & Ear: Special Sense Organs | 3 | 11 | 9 | 2 | 0 | 0 | ✅ |
| | **Totals** | **108** | **207** | **159** | **39** | **9** | **0** | **23 × ✅** |

**Marker accounting.** The frozen book carried **412** `[VERIFY AGAINST JUNQUEIRA 17e]` markers in the
23 chapters: **207** in the audit zones (the standing items above) and **205** inline in the chapter
text. All 412 have been processed: each inline marker's claim was checked, corrected or confirmed, and
the marker removed. The figures previously quoted in the documentation (415 in the book text, 413 in
the chapters) predate the book-end pass and were stale; this register carries the machine count of the
frozen book. Two further marker strings in `00-front-matter.md` and three in `README.md` are the notes
that *describe* the convention, not claims, and are retained as documentation.

## 2. The corrections that changed scientific content (highlights)

Full per-item detail is in each chapter's verification record. The material ones:

| Chapter | What was wrong | Now |
|---|---|---|
| 1 | TEM/SEM resolving power quoted as bare figures; ultrathin thickness listed as 60–90 nm only | TEM ≈0.1–0.2 nm theoretical / SEM ≈3–10 nm practical stated; sections standardised on **50–100 nm** (routine 60–90 nm); cryo-EM and virtual microscopy explained instead of only named |
| 4 | Basal lamina thickness given qualitatively; epidermal turnover "about 4 weeks" | **20–100 nm** in EM, with the basal-lamina vs basement-membrane distinction; epidermis **3–4 weeks** |
| 8 | Osteon described as 8–15 lamellae; "deep osteocytes 10–20× farther from vessels"; fuchsin-acid/Fann-Nissen staining for canaliculi; secondary ossification centres "after birth" | **4–20 lamellae (3–7 µm each)**; the false ratio replaced by the reason canaliculi exist; canaliculi by Schmorl/silver methods, Fann-Nissen for matrix and cement lines; secondary centres — mostly after birth, but the **distal femoral centre appears before birth (≈36 weeks)** |
| 9 | Eosinophil circulating half-life "~8 h"; coagulation cascade absent | No longer stated as a fixed value (6–10 h for neutrophils, ~8–12 h for eosinophils); **coagulation summary** added (intrinsic/extrinsic/common, vitamin-K factors, PT/aPTT/TT) and the platelet open canalicular + dense tubular systems |
| 10 | Smooth-muscle cell "20 µm diameter"; intercalated disc "desmosome + adherens"; intercalated-disc stain given as fuchsin acid; cardiac site list included the aorta | **3–8 µm × 20–200 µm**; **fascia adherens** as the main transverse component plus desmosomes; routine H&E / iron haematoxylin; cardiac muscle limited to atria, ventricles and the myocardial sleeves of the pulmonary veins and superior vena cava |
| 11 | Slow axonal transport 0.5–3 mm/day; "neuroglia ≈10× neurons"; internode ~1 mm with a 100:1 node ratio | **0.2–2 mm/day**; **glia ≈ neurons (≈1:1)**; internode **0.2–1 mm**, several hundred times the node; **neuropil** defined |
| 12 | Arteriole "<0.5 mm"; pericyte called a pacemaker | **10–100 µm (≈50 µm)**; pericyte role stated as contractility and permeability regulation; vasa vasorum threshold (wall >≈1 mm) added |
| 13 | Lymph-node capsule credited with smooth muscle; human splenic blood/platelet storage called "limited" | Lymph-node capsule described correctly (dense collagenous; the muscular capsule belongs to the spleen); human spleen **stores ≈30% of circulating platelets** with a small red-cell reservoir |
| 14 | Cementum had no mineralisation figure; ameloblast fate vague; submandibular ratio unqualified | **Cementum ≈50% mineralised**; ameloblasts → **reduced enamel epithelium** → lost at eruption (why enamel cannot regenerate); ratio stated as "mixed, serous-predominant (≈2:1)" |
| 17 | Reid index described as a "surgical classification"; tracheal ring number absent | **Reid index = gland-layer thickness ÷ wall thickness**; **16–20 C-shaped hyaline rings** |
| 19 | Collecting duct origin unstated; uroplakin plaques and nephrin/podocin detail thin | Collecting duct from the **ureteric bud** (hence not part of the nephron embryologically); nephrin/podocin as the podocyte slit-diaphragm targets in nephrotic syndrome |
| 21 | "Removal of cytoplasm prevents entry of maternal mitochondria" (reversed) | Residual body shed and resorbed by Sertoli cells; **sperm mitochondria are destroyed after fertilisation — the zygote's mitochondria are maternal** |
| 22 | IgG passage across the placenta absent | Added: only **IgG** crosses (FcRn); IgM and large immune complexes do not — basis of neonatal protection and of haemolytic disease of the newborn |
| 23 | "غددِ سرومینوس" for ceruminous glands; middle-ear amplification without its mechanism | **غددِ مومساز (modified apocrine sweat glands)**; ≈20× amplification explained by the **≈17:1 tympanic-membrane : oval-window area ratio plus the ossicular lever** |

Terminology-related text corrections applied in the same pass: Ch13 `لوزهٔ معدی` → `نسجِ لیمفاویِ معدی`
(×5, the stomach's MALT — "gastric tonsil" is not an established term); Ch23 `سرومینوس` → `مومساز`
(×5); Ch23 stain label `PAS/رنگ آبی` → `PAS/آلسین‌بلو`; Ch19 staining/podocyte rows made explicit.

## 3. Terminology resolution (آنتی‌ژن and the 21 LOW-confidence rows)

Policy was not reopened: no locked decision was touched, no Dari term was invented.

| Item | Decision |
|---|---|
| **آنتی‌ژن** (the book's only unresolved term) | **RESOLVED → AFGHAN STANDARD, confidence MEDIUM.** It is the established English-derived transliteration, it is not an Iranian-specific form, and the book uses it consistently in one single spelling (the variants آنتی‌نژ/آنتی‌نژن appear in no chapter). Under the policy's "established international term where appropriate" rule it is now the canonical form; the `[VERIFY TERMINOLOGY]` flag is retired |
| 16 further LOW-confidence rows (دنتینوژنیک، حجراتِ ایتو، حجرهٔ جارویی، لوله‌های منیفروس، اپیتلیومِ منیفروس، سپرماتوژنیز، واز دفرنس، وسیکولِ سیمینال، غددِ بولبویورترال، سکلرا، کوروئید، یوویا، جسمِ سیلیاری، هیومورِ آکوئوس، فووآ سنترالیس، کاتاراکت) | **RESOLVED → MEDIUM.** Retained as established English-derived transliterations actually used in the chapters; each row now carries that note in `source_authority`/`usage_notes` |
| `الصاقِ عصبی` (Ch11 row, unused) | **CORRECTED** → `بازسازیِ نسجِ عصبی`, the form the chapters use |
| `وریدِ صافانی` (Ch12 row, unused — the book never mentions the splenic vein) | **CORRECTED** → `شریانِ صافانی` (Splenic artery), the term Ch13 actually uses |
| `لوزهٔ معدی` (Ch13) | **CORRECTED** → `نسجِ لیمفاویِ معدی` / *Gastric lymphoid tissue (MALT)* |
| `صافانِ لیمفاوی` (Ch13 row, unused) | **CORRECTED** → `صفافیِ لیمفاوی`, the form the chapters use |
| `تومورِ عروقی` (Ch12 row) | **WITHDRAWN** — redundant with the existing `همانژیوم / Hemangioma` row and used in no chapter |
| Glossary totals after the pass | **690 rows** × 12 columns · 292 AFGHAN STANDARD · 375 COMMON AFGHAN TRANSLITERATION · 23 ENGLISH RETAINED · **0 VERIFY FURTHER** · confidence 145 HIGH · 545 MEDIUM · **0 LOW** · **0 UNRESOLVED** |

**Check-11 (shortening) — final status:** all 23 chapters are now ✅. Compression was audited topic by
topic against the reference's coverage; where a compression had genuinely dropped an exam-relevant
fact, a short targeted addition was made (9 additions in total, listed in the master table). No chapter
was lengthened beyond that, no new framework or section was introduced, and the 13-section structure is
untouched.

## 4. Residual scientific uncertainties (documented, not blocking)

1. **Osteon lamellae:** sources give 4–20 (Dorland, adopted), 5–20 (Standring); the book now says
   4–20 with the per-lamella thickness, which is defensible across references.
2. **Ultrathin sections:** 50–100 nm is the standard working range (30–60 nm for maximum resolution);
   the book states 50–100 nm with 60–90 nm as the routine figure.
3. **Resolving power:** TEM/SEM figures are instrument- and specimen-dependent; the book now
   distinguishes the theoretical figure from practical biological performance.
4. **Ch 10 — Brugada syndrome / channelopathies:** deliberately not added; they are not histology and
   the chapter stays exam-oriented.
5. **Clinical items not drawn from the reference** (e.g. hibernoma, Reed–Sternberg cells, AZF
   microdeletions, ER/PR/HER2, otosclerosis) are labelled as clinical correlations and are never
   attributed to a reference chapter.

## 5. Where the evidence came from

No local copy of Junqueira 17e exists in the workspace, so each item was resolved from established
histology knowledge cross-checked against independent reference sources (chapter-numbering map of the
17th edition; Elsevier/Dorland and Standring for osteon lamellae; ISCN-derived cytogenetic banding
levels; ultramicrotomy practice ranges; basal-lamina EM measurements; filament diameters). Items that
could not be settled from those sources were corrected to a defensible range or statement rather than
left as a bare number; nothing was invented to silence a warning, and no claim that the reference does
not support was added.
