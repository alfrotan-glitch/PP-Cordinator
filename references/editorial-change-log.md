# Editorial Change Log & Production Audit Trail
## Project: Provincial Coordinator 24-Hour Exam Master Guide (Shuhada Organization — Daikundi)

### Metadata
* **Publication Title:** MASTER BLUEPRINT — PROVINCIAL COORDINATOR: 24-HOUR EXAM MASTER GUIDE
* **Target Position:** Provincial Coordinator (هماهنگ‌کننده ولایتی)
* **Organization:** Shuhada Organization (شهدا ارگنیزیشن)
* **Duty Station:** Daikundi Province / Nilli (ولایت دایکندی — نیلی)
* **Editorial Standards:** `medical-dari-publishing.skill` (Afghan Dari Health Standards)
* **Date of Audit & Release:** September 20, 2026

---

### Record of Editorial Passes & Classifications

#### 1. Structural & Architectural Audit (Classification: Structural)
* **Original State:** The initial repository draft (`کتاب_Provincial_Coordinator_نسخه_ویرایش‌شده.docx`) comprised only 10 short chapters (~13,550 words) with basic descriptions and unstyled paragraphs.
* **Master Blueprint Expansion:** Fully expanded into the complete 62-chapter, 19-part architecture, including Part 0 through Part XIX, Appendices A through M, and the 24-Hour Study Map.
* **Structural Result:**
  * Part 0: The Opening Simulation (07:42 AM crisis triage in Nilli).
  * Part I: Enter the Role (Chapters 1 & 2).
  * Part II: Afghanistan Health System & Project Management (Chapters 3 & 4).
  * Part III: Health Data, HMIS, DHIS2 & Data Quality (Chapters 5, 6 & 7 with 10 data cases).
  * Part IV: Health Services, Clinic Management, EPI & Logistics (Chapters 8, 9 & 10).
  * Part V: Project Planning, Workplan & M&E (Chapters 11 & 12).
  * Part VI: Budget, Finance & Variance Analysis (Chapters 13 & 14).
  * Part VII: Procurement & Asset Management (Chapters 15 & 16).
  * Part VIII: HR, Recruitment & Administration (Chapters 17, 18 & 19).
  * Part IX: Reporting & Case Lab (Chapters 20 & 21 with 10 reporting cases).
  * Part X: Coordination, Stakeholders & Meetings (Chapters 22, 23 & 24 with 10 stakeholder cases).
  * Part XI: Prioritization & SAFE/R Framework (Chapters 25 & 26).
  * Part XII: Provincial Coordinator Simulation (Chapters 27, 28 & 29: Day 1, Week 1, Month 1).
  * Part XIII: Exam Mode (Chapters 30–35: 100 Things, 50 Hooks, 180 Questions Bank, Mock Exams 1, 2, 3).
  * Part XIV: Interview Mode (Chapters 36, 37 & 38: STAR method, 20 core interview questions, pressure simulation).
  * Part XV: Ethics & Professional Conduct (Chapter 39: 5 ethical dilemmas).
  * Part XVI: Excel & Office Skills (Chapters 40 & 41).
  * Part XVII: Integrated Master Case Lab (Chapters 42–51: 10 complex multi-domain cases).
  * Part XVIII: Final Revision System (Chapters 52–58: Facts, Terms, Frameworks, Cases, Interviews, Formulas, Mistakes).
  * Part XIX: The Final Night (Chapters 59–62: 3-Hour, 60-Minute, 15-Minute, One-Page Final Sheet).
  * Appendices A through M: Full templates and reference instruments.

#### 2. Terminological & Afghan Dari Audit (Classification: Terminological)
* **Standing Rule Applied:** Authentic Afghan Dari exclusively; Iranian Persian terminology strictly rejected per `medical-dari-publishing.skill`.
* **Substitutions and Normalizations Audited via Scanner:**
  * `گزارش` $\rightarrow$ Normalized to `راپور` (Report) / `راپوردهی` (Reporting).
  * `هزینه` $\rightarrow$ Normalized to `مصرف` / `مصارف` (Expenditure / Operational Cost).
  * `درمانگاه` $\rightarrow$ Strictly `کلینیک` (Clinic) / `مرکز صحی` (Health Facility - BHC/CHC/SHC).
  * `بیمارستان` $\rightarrow$ Strictly `شفاخانه` (Hospital).
  * `پزشک` $\rightarrow$ Strictly `داکتر` (Medical Doctor).
  * `ماما` $\rightarrow$ Strictly `قابله` (Midwife).
  * `داروساز` $\rightarrow$ Strictly `فارمسست` (Pharmacist) / مسئول دواخانه.
  * `حقوق` $\rightarrow$ Strictly `معاش` (Salary).
  * `غیبت` $\rightarrow$ Strictly `غیرحاضری` (Absenteeism).
  * `مرخصی` $\rightarrow$ Strictly `رخصتی` (Leave).
  * `زایمان` $\rightarrow$ Strictly `ولادت` (Delivery).
  * `سوء تغذیه` $\rightarrow$ Spelled `سوء تغذی` (Malnutrition).
  * `انبار` $\rightarrow$ Strictly `دیپو` / `گدام` / `ذخیره‌گاه` (Warehouse / Depot).
  * `بخش سرپایی` $\rightarrow$ Strictly `شعبه سراپا (OPD)`.
  * `بخش بستری` $\rightarrow$ Strictly `شعبه بستر (IPD)`.
* **Glossary Established:** Single source of truth populated at `assets/terminology-glossary.csv`.
* **Automated Audit:** Passed with zero violations via `scripts/terminology_scanner.py`.

#### 3. Medical, Public Health & Policy Validation (Classification: Scientific & Clinical)
* **EPI Schedule Checked:** Aligned with current Afghanistan MoPH/WHO/UNICEF national immunization schedule (BCG, OPV, IPV, Pentavalent, PCV, Rota, Measles-1 at 9 months, Measles-2 at 18 months, Td for pregnant women).
* **Cold Chain Temperature:** Verified standard +2°C to +8°C; freeze-sensitive vaccines explicitly identified (Penta, PCV, IPV, Td, HepB); Shake Test protocol detailed; VVM stages validated.
* **BPHS/EPHS Service Tiers:** Aligned with national health system standards: Health Post (HP: 1,000–1,500 population, CHW-F & CHW-M), Sub Health Center (SHC), Basic Health Center (BHC: 15,000–30,000 population), Comprehensive Health Center (CHC: 30,000–60,000 population), District Hospital (DH), Provincial Hospital (PH in Nilli).
* **HMIS Data Quality:** ACCT framework (Accuracy, Completeness, Consistency, Timeliness) embedded across data audits, registers, tally sheets, and DHIS2 reporting.
* **Shuhada Organization Context:** Established 1989 by Dr. Sima Samar & Abdul Rauf Nawid; core values (Transparency, Accountability, Gender Sensitivity, Professionalism); motto ("Working for a better tomorrow"); operations in Daikundi (Nilli, Shahristan, Miramor, Ashtarlay, Sang-e-Takht, Khadir, Pato, Kiti, Gizab).

#### 4. Typesetting & Multi-Format Generation (Classification: Prepress / Production)
* **Master Manuscript:** `manuscript/master.md` (25,983 words, 156,656 characters).
* **DOCX Deliverable:** Generated with full RTL paragraph/table direction, custom Word styles, accent headings (Navy & Deep Blue), light callout boxes with colored borders, striped tables, header/footer with page numbers. Output saved to:
  * `کتاب_Provincial_Coordinator_نسخه_ویرایش‌شده.docx` (primary workspace deliverable)
  * `build/Provincial_Coordinator_24Hour_Exam_Master_Guide.docx`
* **EPUB Deliverable:** Valid EPUB3 generated at `build/Provincial_Coordinator_24Hour_Exam_Master_Guide.epub`.
* **HTML Reader:** Interactive RTL edition with responsive styling generated at `build/index.html`.
