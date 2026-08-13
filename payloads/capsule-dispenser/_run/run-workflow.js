export const meta = {
  name: 'capsule-dispenser',
  description: 'Design the Quiver capsule dispenser payload: research-first mechanism survey, judged trade study, CAD critic loop, electronics, drop-ballistics sim gate, red team',
  phases: [
    { title: 'Research', detail: 'parallel mechanism survey across industries' },
    { title: 'Trade', detail: 'champion concepts + judge panel' },
    { title: 'CAD', detail: 'build/critic loop, cap 12, plateau exit' },
    { title: 'Electronics', detail: 'architect + safety critic + revision' },
    { title: 'Sim', detail: 'drop ballistics Monte Carlo gate' },
    { title: 'Finish', detail: 'red team, gap review, package' },
  ],
}

const ROOT = '/Users/hex/projects/payload-systems/payloads/capsule-dispenser'
const RUN = ROOT + '/_run'
const CTX = `MANDATORY FIRST: read ${RUN}/CONTEXT.md fully. Never invent facts; label assumptions. `

const VERDICT = {
  type: 'object', additionalProperties: false,
  properties: {
    score: { type: 'number' }, pass: { type: 'boolean' },
    issues: { type: 'array', items: { type: 'string' } },
    numbers: { type: 'string', description: 'the actual measured numbers backing this verdict' },
  }, required: ['score', 'pass', 'issues', 'numbers'],
}

// ---------- Phase 1: Research sweep ----------
phase('Research')
log('Research sweep: 5 domains in parallel')
const DOMAINS = [
  ['seed-metering', 'precision-agriculture seed metering: vacuum discs, finger pickup, brush/belt meters, singulation tech in planters (John Deere, Precision Planting etc.)'],
  ['projectile-feeders', 'airsoft/BB/paintball hopper + feed systems: spring followers, agitators, force-feed loaders, anti-jam geometry for ~6-17mm spheres'],
  ['pill-counting', 'pharmaceutical pill counting and dispensing: rotary disc counters, channel singulators, optical count verification, handling friable tablets'],
  ['bulk-dispensers', 'fish/pet feeders, candy/gumball vending, bulk part singulation (bowl feeders): simple robust metering of ~10-15mm roundish objects, bridging prevention'],
  ['drone-spreaders', 'existing drone spreading/dispensing systems (DJI Agras T-series spreader, granular applicators, prior drone capsule or tebuthiuron pellet dispenser attempts) AND commercial capsule / tebuthiuron pellet product data: pellet hardness, moisture behavior, dust, exact dimensions'],
]
const research = await parallel(DOMAINS.map(([key, brief]) => () =>
  agent(CTX + `You are a research agent. Domain: ${brief}. Find mechanisms/facts relevant to metering EXACTLY N (1-10) pellets of 12mm/1.18g molded herbicide pellets from a 250+ pellet hopper on a drone, in dusty ranch conditions. For each mechanism: how it works, count accuracy, jam behavior, complexity, adaptability to our pellet, cite URLs. Write ${RUN}/RESEARCH-${key}.md. Return a 10-line summary of the strongest candidates.`,
    { label: `research:${key}`, phase: 'Research' })))

const survey = await agent(CTX + `Read all ${RUN}/RESEARCH-*.md files (5 domains). Write ${RUN}/MECHANISM-SURVEY.md: a synthesis of ALL candidate metering mechanisms found, scored on count-accuracy potential, jam resistance (dust + fragments + bridging), buildability (3D print + COTS actuators), mass, and field serviceability with gloves. Then SELECT the 4 strongest, maximally-diverse champions to develop as concepts. Justify selections AND rejections. Summaries from researchers: ${research.filter(Boolean).map((r, i) => `[${DOMAINS[i][0]}] ${r}`).join('\n')}`,
  { label: 'survey-synthesis', phase: 'Research', schema: { type: 'object', additionalProperties: false, properties: { champions: { type: 'array', minItems: 4, maxItems: 4, items: { type: 'object', additionalProperties: false, properties: { key: { type: 'string' }, mechanism: { type: 'string' }, whyChosen: { type: 'string' } }, required: ['key', 'mechanism', 'whyChosen'] } } }, required: ['champions'] } })

// ---------- Phase 2: Trade study ----------
phase('Trade')
log('Champions: ' + survey.champions.map(c => c.key).join(', '))
const concepts = await parallel(survey.champions.map(c => () =>
  agent(CTX + `You are the honest advocate for dispenser concept "${c.key}": ${c.mechanism} (chosen because: ${c.whyChosen}). Read ${RUN}/MECHANISM-SURVEY.md and your domain's research file. Develop the concept in ${RUN}/CONCEPT-${c.key}.md: mechanism layout + actuator choice, hopper (250 pellets, anti-bridging/agitation), count-verification sensing point, mounting to the 50x50mm clip plate, mass estimate with breakdown, power draw vs the 2A/25W limits, failure modes (jam, dust, fragments, vibration, heat) with honest mitigations, and a frank "why this might lose" section. No CAD yet — dimensioned sketch-level (key dimensions in mm).`,
    { label: `concept:${c.key}`, phase: 'Trade' })))

const JUDGES = [
  ['count-reliability', 'Will it dispense EXACTLY N, every time, for 5000 cycles in dust? Jam modes, count verification integrity, recovery from a jam mid-mission.'],
  ['field-ops', 'Ubaldo test: refill with gloves in wind, clear a jam in the field, clean it, survive heat/dust/vibration. Simplicity wins.'],
  ['integration', 'Mass ledger realism, clip-plate mounting loads, envelope vs landing gear/props, power within ICD limits, drop-path geometry for accuracy.'],
]
const verdicts = await parallel(JUDGES.map(([lens, mandate]) => () =>
  agent(CTX + `You are a trade-study judge. Lens: ${lens} — ${mandate}. Read all 4 ${RUN}/CONCEPT-*.md files and MECHANISM-SURVEY.md. Score each concept 0-100 on your lens with written justification. Be adversarial; find what advocates soft-pedaled.`,
    { label: `judge:${lens}`, phase: 'Trade', schema: { type: 'object', additionalProperties: false, properties: { scores: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { key: { type: 'string' }, score: { type: 'number' }, argument: { type: 'string' } }, required: ['key', 'score', 'argument'] } } }, required: ['scores'] } })))

const tally = {}
for (const v of verdicts.filter(Boolean)) for (const s of v.scores) tally[s.key] = (tally[s.key] || 0) + s.score
const winner = Object.entries(tally).sort((a, b) => b[1] - a[1])[0][0]
log(`Trade winner: ${winner} (${JSON.stringify(tally)})`)
await agent(CTX + `Scribe: write ${RUN}/JUDGING.md recording the full trade study: tally ${JSON.stringify(tally)}, winner "${winner}", every judge's per-concept arguments VERBATIM from this JSON: ${JSON.stringify(verdicts.filter(Boolean))}. Record dissent honestly — where judges disagreed, say so.`,
  { label: 'scribe', phase: 'Trade', effort: 'low' })

// ---------- Phase 3: CAD loop ----------
phase('CAD')
const CAD_CRITICS = [
  ['interference', `Load the CAD exports plus the quiver airframe STEPs (/tmp/pq-main/src/quiver/, landing gear + lower plate + props). MEASURE numerically: ground clearance below dispenser at rest on gear (require >=40mm margin), prop-disk clearance, clip-plate footprint compliance. State every measured number.`],
  ['pellet-path', `Trace the complete pellet journey hopper->meter->exit in the actual geometry: minimum channel dimension vs 13mm worst-case pellet, hopper wall angles vs bridging (require >60 deg from horizontal at outlet or active agitation), pinch points, where a fragment/dust accumulates, can a jam be cleared in the field. Numbers for every claim.`],
  ['buildability', `Printability (overhangs, wall thickness >=2mm structural), COTS parts with real part numbers (actuator, bearings, fasteners), assembly/service: refill with gloves, jam access, count-sensor cleaning. Score honestly.`],
  ['mass-budget', `Rebuild the mass ledger from the CAD volumes (PETG ~1.27 g/cm3 at realistic infill, list every component + 295g pellets). Require total <=1.5kg; every 100g above 1.0kg justified. State the total.`],
]
let round = 0, lastTotal = -1, plateau = 0, cadDone = false
while (round < 12 && !cadDone) {
  round += 1
  await agent(CTX + `You are the CAD builder, round ${round}. Winning concept: "${winner}" — read ${RUN}/CONCEPT-${winner}.md, ${RUN}/JUDGING.md, and (round>1) ${RUN}/BUILD-NOTES-r${round - 1}.md with the critics' issues — fix every blocking issue or rebut in writing. Build/extend parametric build123d model ${ROOT}/cad/dispenser.py (venv python per CONTEXT): full dispenser mounted on the payload-side clip plate STEP, hopper sized for 250+ pellets (compute fill volume), metering mechanism with real actuator envelope, count-sensor location, drop tube/exit. Export STEP+STL to ${ROOT}/cad/exports/, at least 3 renders to ${ROOT}/cad/renders/ (r${round}_*.png, cream background). Run your own geometry checks (print measured numbers). Write ${RUN}/BUILD-NOTES-r${round}.md: what changed, measured numbers, open issues.`,
    { label: `build:r${round}`, phase: 'CAD' })
  const crits = await parallel(CAD_CRITICS.map(([key, mandate]) => () =>
    agent(CTX + `CAD critic "${key}", round ${round}. ${mandate} Read ${RUN}/BUILD-NOTES-r${round}.md, run the venv python against ${ROOT}/cad/ exports/source to MEASURE (do not trust the builder's claims). Score 0-10, pass only if no blocking issues.`,
      { label: `critic:${key}:r${round}`, phase: 'CAD', schema: VERDICT })))
  const ok = crits.filter(Boolean)
  const total = ok.reduce((s, c) => s + c.score, 0)
  const allPass = ok.length === CAD_CRITICS.length && ok.every(c => c.pass)
  log(`CAD r${round}: total ${total.toFixed(1)}/40, pass=${allPass}`)
  await agent(`Append a round-${round} critics section to ${RUN}/BUILD-NOTES-r${round}.md: ${JSON.stringify(ok.map((c, i) => ({ critic: CAD_CRITICS[i][0], ...c })))}. Verbatim, no softening.`,
    { label: `notes:r${round}`, phase: 'CAD', effort: 'low' })
  if (allPass) cadDone = true
  else if (total <= lastTotal) { plateau += 1; if (plateau >= 2) { log('CAD plateau — shipping with complaints recorded'); cadDone = true } }
  else plateau = 0
  lastTotal = Math.max(lastTotal, total)
}

// ---------- Phase 4: Electronics ----------
phase('Electronics')
const elec = await agent(CTX + `Electronics architect. Read the winning concept, final BUILD-NOTES, and ICD sections 3-5. Design ${ROOT}/electronics/ELECTRONICS.md: actuator drive off the blind-mate rails (12V_PL 25W / 12VSW 2A budgets — recommend which rail powers what and why; the K1/12VSW relay exists for this payload), break-beam pellet counter at the exit (real part numbers, dust-tolerance strategy), logic supply (buck from 12V, real part), the command interface contract ONLY (recommend FMU_CH1 PWM vs DroneCAN with tradeoffs; define signal -> "dispense N" -> count feedback semantics; NO software implementation), connector/wiring through the 10-circuit blind-mate, full BOM with prices. Worked calcs: stall current vs fuse, worst-case power.`,
  { label: 'elec-architect', phase: 'Electronics' })
const elecCrit = await agent(CTX + `Electronics safety critic. Attack ${ROOT}/electronics/ELECTRONICS.md with a written fault analysis: accidental dispense (power-up glitch, PWM noise, 12V_PL cycling per ICD — require a positive-interlock story), actuator stall/jam current vs the 2A fuse, dust/herbicide ingress on the count sensor, vibration, hot-restart mid-jam, ESD. Each: effect/detection/mitigation/residual. Score and verdict.`,
  { label: 'elec-safety', phase: 'Electronics', schema: VERDICT })
if (!elecCrit?.pass) {
  await agent(CTX + `Revise ${ROOT}/electronics/ELECTRONICS.md closing every blocking issue from the safety critic (or accept-with-mitigation, justified in a Residual Risks section): ${JSON.stringify(elecCrit?.issues || [])}. One pass, honest.`,
    { label: 'elec-revision', phase: 'Electronics' })
}

// ---------- Phase 5: Sim gate ----------
phase('Sim')
let simResult = null
for (let attempt = 1; attempt <= 2 && !simResult?.pass; attempt++) {
  simResult = await agent(CTX + `Drop-ballistics sim engineer (attempt ${attempt}). Write ${ROOT}/sim/drop_mc.py (venv numpy): Monte Carlo (>=20000 drops/case) of a 1.18g, 12mm sphere (Cd 0.47, label the model) released from the dispenser exit (get exit height below belly + any exit velocity from the CAD build notes) at 8m AGL hover. Sweep wind 0-8 m/s (steady + gust model, labeled), altitude 5-10m, include release-timing jitter and position hold error (ArduPilot hover: assume 0.3m 1-sigma horizontal, labeled assumption), simple prop-downwash advection labeled as assumption. Outputs: P(landing within 1m of target) per case, CEP, the MAX wind at which 8m AGL meets >=90% within 1m, and a recommended release altitude. Styled plot to ${ROOT}/sim/dispersion.png (cream/black/orange). Write ${ROOT}/sim/RESULTS.md with honest gates: PASS = a stated wind envelope exists where the 1m spec holds at 8m; FAIL if spec needs <2 m/s wind. ${attempt > 1 ? 'A geometry fix round just ran — re-verify against updated CAD.' : ''}`,
    { label: `sim:attempt${attempt}`, phase: 'Sim', schema: VERDICT })
  log(`Sim attempt ${attempt}: pass=${simResult?.pass} — ${simResult?.numbers || 'n/a'}`)
  if (!simResult?.pass && attempt === 1) {
    await agent(CTX + `Landing-fix CAD round: the sim failed the 1m@8m spec (issues: ${JSON.stringify(simResult?.issues || [])}). Modify ${ROOT}/cad/dispenser.py with geometry that improves drop precision (longer/lower drop tube, exit velocity control, whatever the physics supports), re-export, re-render (rfix_*.png), update ${RUN}/BUILD-NOTES-simfix.md with measured numbers. Do NOT regress the interference critic's clearances — re-run those checks and print them.`,
      { label: 'cad-simfix', phase: 'Sim' })
  }
}

// ---------- Phase 6: Red team, gap review, package ----------
phase('Finish')
const [redteam, gaps] = await parallel([
  () => agent(CTX + `Red team. Fresh eyes, attack the ENTIRE package (${ROOT}: _run docs, cad, electronics, sim). Hunt: count-verification integrity end to end, dust/fragment accumulation over a 250-pellet sortie, thermal (black box in TX sun with wax-bound pellets?), vibration, CG shift as hopper empties, refill workflow, mass creep, sim assumptions that flatter the result, anything renamed instead of fixed. Write ${RUN}/RED-TEAM.md: numbered findings, severity, each with a concrete test or fix. Return top 5 findings as text.`, { label: 'red-team', phase: 'Finish' }),
  () => agent(CTX + `Gap review ("what did everyone miss"). Compare the package against the mission and CONTEXT scope. Look OUTSIDE the shared assumptions: pellet-to-pellet variation, hopper behavior at 10% full, multi-drop missions (250 targets = battery?), interaction with the future dock (payload stays mounted!), anything with no owner. Write ${RUN}/GAP-REVIEW.md. Return top 3 gaps as text.`, { label: 'gap-review', phase: 'Finish' }),
])
await agent(CTX + `Packager. Assemble the shipped payload folder per ${ROOT}/../_template/README.md format: write ${ROOT}/README.md (status: design, port: bottom, ICD 1.0, mass/power table from the real numbers, folder map), ${ROOT}/docs/DESIGN.md (the full design story: survey -> trade -> CAD -> electronics -> sim, with the risk register folding in RED-TEAM + GAP-REVIEW findings NOT under the rug), verify cad/ electronics/ sim/ all have their deliverables (list what exists). Then git add the payloads/capsule-dispenser folder ONLY and commit on the current branch (capsule-dispenser) with message "capsule-dispenser: rev-0 design package (overnight run)" author thomasg <thomas@arrowair.com>. Do NOT push. Write ${RUN}/RUN-RESULT.md summarizing every phase with its key numbers. Red team top findings: ${redteam}. Gaps: ${gaps}.`,
  { label: 'packager', phase: 'Finish' })

return { winner, tally, cadRounds: round, simPass: simResult?.pass, simNumbers: simResult?.numbers }
