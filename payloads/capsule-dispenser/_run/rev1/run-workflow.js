export const meta = {
  name: 'brush-dispenser-rev1',
  description: 'Rev-1 CAD completion for the capsule agricultural granule dispenser: punch-list synthesis, build/critic loop until the CAD closes, verify pass, packager',
  phases: [
    { title: 'Punchlist', detail: 'synthesize blocking punch list from red team + directives' },
    { title: 'CAD', detail: 'builder vs 4 measuring critics, cap 8 rounds' },
    { title: 'Verify', detail: 'fresh-eyes re-measure of rev-0 blockers + directives' },
    { title: 'Finish', detail: 'docs, BOM, commit (no push)' },
  ],
}

const ROOT = '/Users/hex/projects/payload-systems/payloads/capsule-dispenser'
const RUN = ROOT + '/_run'
const R1 = RUN + '/rev1'
const CTX = `MANDATORY first step: read ${R1}/CONTEXT.md fully (it points at rev-0 context and the punch-list sources). Never invent facts; label assumptions. Your final text is data for the workflow, not a human-facing message.\n\n`

const VERDICT = {
  type: 'object',
  properties: {
    pass: { type: 'boolean' },
    score: { type: 'number' },
    blocking: { type: 'array', items: { type: 'string' } },
    nonblocking: { type: 'array', items: { type: 'string' } },
    numbers: { type: 'string' },
  },
  required: ['pass', 'score', 'blocking', 'numbers'],
}

// ---- Phase 1: punch list ----
phase('Punchlist')
const punch = await agent(CTX + `Punch-list synthesizer. Read ${RUN}/RED-TEAM.md, ${RUN}/GAP-REVIEW.md, ${RUN}/BUILD-NOTES-r6.md, ${ROOT}/electronics/ELECTRONICS.md, and the six directives in ${R1}/CONTEXT.md. Write ${R1}/PUNCHLIST.md: every item this run must fix, split BLOCKING vs NONBLOCKING, each item with its source (finding ID or directive number), the concrete acceptance test (a measurable geometric check), and which rev-0 findings are VOID per the directives (say why). Do not include simulation, software, or electrical pin/pad stack-up items.`,
  { label: 'punchlist', phase: 'Punchlist', schema: {
    type: 'object',
    properties: {
      blocking: { type: 'array', items: { type: 'string' } },
      nonblocking: { type: 'array', items: { type: 'string' } },
    },
    required: ['blocking'],
  } })
log(`Punch list: ${punch.blocking.length} blocking, ${(punch.nonblocking || []).length} non-blocking`)

// ---- Phase 2: build/critic loop ----
const CRITICS = [
  { key: 'assembly', brief: `Assembly-and-drive critic (rev-0 RT-1 owner). From the EXPORTED geometry (not the notes): derive and write a complete step-by-step assembly order proving every part can physically be installed (sweep the insertion paths; print swept-volume obstruction numbers); verify the torque path motor→gearbox→shaft→metering disc exists and every fastener has tool access (print each access corridor's obstruction volume). Any part that cannot be assembled or driven = blocking.` },
  { key: 'granule-path', brief: `Granule-path critic (carry rev-0 pellet-path mandate). Trace the full pellet journey hopper→pocket→exit on the exported geometry: pinch points vs Ø13 worst case, overfill-relief geometry before the housing arc, and adversarially construct the worst-case fragment jam (choose fragment size/position; show geometrically whether it wedges or is rejected/sheared, with the shear-margin number). Verify stall-recovery motion has the free travel it needs (agitator clash was a rev-0 blocker). Regressions on the fragment-jam requirement = blocking.` },
  { key: 'integration', brief: `Integration/serviceability critic. Measure on the exported assembly: (a) the gloved-hand access corridor to the quick-release per directive 3 — state the corridor dimensions you require (justify against a 95th-percentile gloved hand, label as assumption) and print the measured clearance; (b) electronics bay per directive 2 — exists, fits the control PCB envelope from ELECTRONICS.md, dust-tight to the hopper, wiring channels routed interface→bay→motor/sensor with NO wiring through the hopper volume (print channel cross-sections); (c) side-wall fill port / refill workflow per directive 4 + RT-14 acceptance test; (d) ground clearance on the landing-gear STEPs and overall envelope; (e) mass ledger rebuilt independently from the exports vs the ≤1500 g dry target (print the ledger).` },
  { key: 'count-sensor', brief: `Count-sensor geometry critic (rev-0 RT-3 owner). Verify the CAD contains the counting hardware ELECTRONICS.md §4.2-4.4 requires: ECO-3 dual staggered Ø3.2 apertures with ECO-9 6 mm vertical stagger (print the actual aperture positions/diameters from the export and diff them against the spec), ECO-4 sacrificial window, ECO-5 labyrinth, PCB/emitter/receiver mounting features that match the electronics bay. Check cad/BOM.md dropped the rejected TSSP4038 for the analog VBPW34FAS/OPA2320 chain. Spec'd-but-not-modelled hardware = blocking.` },
]

let round = 0
let closed = false
let lastBlockers = Infinity
let plateau = 0
let critVerdicts = []
while (round < 8 && !closed) {
  round++
  await agent(CTX + `CAD builder, rev-1 round ${round}. Read ${R1}/PUNCHLIST.md${round > 1 ? ` and ${R1}/CRITIQUE-r` + (round - 1) + '.md — fix every blocking issue or rebut in writing with measured numbers' : ''}. Extend/modify the parametric build123d model ${ROOT}/cad/dispenser.py. Keep the pocket-wheel mechanism as judged; change only what the punch list demands. Re-export STEP+STL to ${ROOT}/cad/exports/, at least 3 renders to ${ROOT}/cad/renders/ (v1r${round}_iso/section/detail.png, cream background). Run your own geometry checks and QUOTE the tool output verbatim in ${R1}/BUILD-NOTES-r${round}.md (rev-0 shipped narrated fixes the geometry didn't contain — every "measured" claim must be traceable to printed output). List remaining open issues honestly.`,
    { label: `build:r${round}`, phase: 'CAD' })

  critVerdicts = await parallel(CRITICS.map(c => () =>
    agent(CTX + c.brief + `\n\nThis is rev-1 round ${round}. Read ${R1}/PUNCHLIST.md and ${R1}/BUILD-NOTES-r${round}.md, then verify on the actual exports in ${ROOT}/cad/exports/ (venv python, trimesh/build123d — re-run measurements yourself; do not trust the notes). Append your findings with all printed numbers to ${R1}/CRITIQUE-r${round}.md under a "## ${c.key}" heading.`,
      { label: `critic:${c.key}:r${round}`, phase: 'CAD', schema: VERDICT })))

  const verdicts = critVerdicts.filter(Boolean)
  const blockers = verdicts.reduce((n, v) => n + (v.blocking?.length || 0), 0)
  const allPass = verdicts.length === CRITICS.length && verdicts.every(v => v.pass)
  log(`Round ${round}: ${verdicts.length}/${CRITICS.length} critics returned, ${blockers} blocking issues, allPass=${allPass}`)
  if (allPass) { closed = true; break }
  if (blockers >= lastBlockers) { plateau++ } else { plateau = 0 }
  lastBlockers = blockers
  if (plateau >= 2) {
    log(`Plateau: ${plateau} rounds without blocker-count improvement — shipping with complaints recorded`)
    break
  }
}

// ---- Phase 3: fresh-eyes verify ----
phase('Verify')
const verify = await agent(CTX + `Fresh-eyes verifier. You have NOT seen the build rounds. On the final exports in ${ROOT}/cad/exports/, independently re-measure: (1) every BLOCKING item in ${R1}/PUNCHLIST.md — state PASS/FAIL with your own printed numbers; (2) the three rev-0 red-team CAD blockers (RT-1 assembly/torque path, RT-3 count hardware in CAD; RT-2 void except the electronics-bay requirement) — confirm fixed or not; (3) the six directives in ${R1}/CONTEXT.md. Write ${R1}/VERIFY.md. Be adversarial: your job is to catch anything renamed instead of fixed.`,
  { label: 'verify', phase: 'Verify', schema: VERDICT })
log(`Verify: pass=${verify?.pass} blocking=${(verify?.blocking || []).length}`)

// ---- Phase 4: package ----
phase('Finish')
await agent(CTX + `Packager. Update ${ROOT}/README.md (status + mass/clearance numbers from the final round), ${ROOT}/docs/DESIGN.md (add a "Rev-1" section: what closed, what remains open, honest — fold in ${R1}/VERIFY.md findings NOT under the rug), verify ${ROOT}/cad/BOM.md is consistent with the final geometry. Write ${R1}/RUN-RESULT.md summarizing each round with its key numbers and the final verify verdict. Then git -C /Users/hex/projects/payload-systems add the payloads/capsule-dispenser folder ONLY and commit on branch capsule-dispenser, message "capsule-dispenser: rev-1 CAD completion", author thomasg <thomas@arrowair.com>. Do NOT push.`,
  { label: 'packager', phase: 'Finish' })

return {
  rounds: round,
  closed,
  verifyPass: verify?.pass ?? null,
  verifyBlocking: verify?.blocking || [],
}
