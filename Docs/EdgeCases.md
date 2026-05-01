# Detailed Edge Cases: AI-Powered Restaurant Recommendation System

This document lists high-priority and detailed edge cases for the restaurant recommendation project, aligned with the phase-wise architecture defined in `Docs/ProblemStatement.md` and `Docs/Architecture.md`.

## Phase 1: Data Foundation and Preprocessing

### EC-01: Missing critical fields
- **Scenario:** Restaurant records have null/empty `location`, `cuisine`, `cost`, or `rating`.
- **Impact:** Filtering and ranking become unreliable; valid restaurants may be excluded.
- **Mitigation:** Apply field-level validation, fallback defaults, and record-level quality scores.
- **Test case idea:** Inject rows with selective nulls and verify graceful degradation.

### EC-02: Duplicate restaurants with conflicting values
- **Scenario:** Same restaurant appears multiple times with different ratings/costs.
- **Impact:** Candidate list may contain duplicates or inconsistent ranking.
- **Mitigation:** Deduplicate by composite keys (`name + location + address`) and apply conflict resolution rules.
- **Test case idea:** Create conflicting duplicates and confirm deterministic merge behavior.

### EC-03: Non-standard cost and rating formats
- **Scenario:** Cost appears as text ranges ("cheap", "Rs. 200-400") and ratings as mixed strings.
- **Impact:** Numeric comparisons fail during filtering.
- **Mitigation:** Add robust parsing/normalization pipeline with parse-failure logs.
- **Test case idea:** Use mixed-format values and confirm normalization to numeric buckets.

### EC-04: Dataset drift after refresh
- **Scenario:** New dataset version changes column names or value conventions.
- **Impact:** Ingestion pipeline breaks silently or maps fields incorrectly.
- **Mitigation:** Schema version checks, mandatory field contracts, and data drift alerts.
- **Test case idea:** Run ingestion against changed schema and validate failure with clear diagnostics.

## Phase 2: User Preference Capture Layer

### EC-05: Contradictory preferences
- **Scenario:** User requests very low budget + premium cuisine + high minimum rating in a small location.
- **Impact:** Zero candidates or irrelevant fallback recommendations.
- **Mitigation:** Constraint relaxation strategy with transparent messaging ("No exact match; showing closest options").
- **Test case idea:** Submit impossible preference combinations and verify fallback sequence.

### EC-06: Ambiguous location input
- **Scenario:** User types abbreviations, misspellings, or landmark-only locations.
- **Impact:** Over-filtering or incorrect city mapping.
- **Mitigation:** Fuzzy matching, location normalization dictionary, and clarification prompts.
- **Test case idea:** Try "BLR", "Banglore", "near airport" and verify canonical mapping or clarification.

### EC-07: Out-of-range values
- **Scenario:** Negative budget, rating > max scale, or non-numeric entries.
- **Impact:** Invalid queries and unpredictable engine behavior.
- **Mitigation:** Strict input schema validation with user-friendly correction prompts.
- **Test case idea:** Submit invalid numeric ranges and assert validation errors.

### EC-08: Missing optional preferences interpreted as hard constraints
- **Scenario:** Empty optional fields are treated as mandatory filters.
- **Impact:** Overly narrow retrieval and reduced recommendation quality.
- **Mitigation:** Distinguish required vs optional fields explicitly in preference schema.
- **Test case idea:** Omit optional preferences and ensure broad but relevant retrieval.

## Phase 3: Candidate Retrieval and Filtering

### EC-09: Zero candidates after hard filtering
- **Scenario:** Strict filters remove all restaurants.
- **Impact:** No recommendation output.
- **Mitigation:** Tiered relaxation logic (expand budget/rating radius in controlled steps).
- **Test case idea:** Force zero-result query and validate progressive widening logic.

### EC-10: Excessive candidate count
- **Scenario:** Broad query returns very large candidate set.
- **Impact:** LLM prompt overload, latency spikes, and token cost increase.
- **Mitigation:** Pre-ranking + top-N truncation with diversity constraints.
- **Test case idea:** Query metro-wide "any cuisine" and verify bounded candidate count.

### EC-11: Bias toward highly reviewed chains only
- **Scenario:** Rule-based scoring heavily favors popular chains.
- **Impact:** Reduced recommendation diversity and user dissatisfaction.
- **Mitigation:** Add diversity re-ranking (different cuisines, price bands, neighborhoods).
- **Test case idea:** Ensure final list includes variety under broad preferences.

### EC-12: Stale availability/business status
- **Scenario:** Closed or temporarily unavailable restaurants remain in candidates.
- **Impact:** Poor user trust and recommendation utility.
- **Mitigation:** Periodic freshness checks and staleness penalties in scoring.
- **Test case idea:** Mark restaurants as closed and verify exclusion or warning label.

## Phase 4: LLM Recommendation and Ranking

### EC-13: Hallucinated restaurants or attributes
- **Scenario:** LLM invents restaurants, prices, or ratings not present in input.
- **Impact:** Factually incorrect recommendations.
- **Mitigation:** Strict grounding: allow output only from provided candidate IDs and post-generation validation.
- **Test case idea:** Inject adversarial prompt patterns and verify no fabricated entities.

### EC-14: Output format violations
- **Scenario:** LLM returns free-form narrative instead of structured ranked output.
- **Impact:** Parser failures and broken UI rendering.
- **Mitigation:** Strong output schema (JSON contract), retries with corrective prompts, fallback formatter.
- **Test case idea:** Simulate malformed outputs and verify retry/fallback path.

### EC-15: Prompt injection via restaurant/user text
- **Scenario:** Candidate text includes malicious instructions ("ignore previous rules").
- **Impact:** Compromised ranking logic and unsafe outputs.
- **Mitigation:** Input sanitization, instruction hierarchy, and content boundary markers.
- **Test case idea:** Insert injection strings in descriptions and confirm model ignores them.

### EC-16: Latency and timeout from LLM API
- **Scenario:** External LLM response is delayed or fails intermittently.
- **Impact:** Slow UX or failed recommendation request.
- **Mitigation:** Timeouts, retries with exponential backoff, and deterministic fallback ranking.
- **Test case idea:** Mock delayed API and verify timeout handling + fallback response.

## Phase 5: Response Presentation Layer

### EC-17: Missing explanation for selected restaurant
- **Scenario:** Restaurant appears in ranking without rationale.
- **Impact:** Reduced user trust and interpretability.
- **Mitigation:** Enforce non-empty explanation field and regenerate explanation if missing.
- **Test case idea:** Validate output contract for each recommendation item.

### EC-18: Inconsistent display units
- **Scenario:** Costs shown in different formats/currencies without normalization.
- **Impact:** Users cannot compare recommendations accurately.
- **Mitigation:** Unified display formatter for currency and price range labels.
- **Test case idea:** Verify all returned items follow the same cost display rule.

### EC-19: Ties in ranking with unstable order
- **Scenario:** Same score candidates reorder unpredictably between identical requests.
- **Impact:** Perceived instability and confusion.
- **Mitigation:** Deterministic tie-breakers (rating, review count, alphabetical fallback).
- **Test case idea:** Re-run same request and verify stable ordering.

## Phase 6: Monitoring and Continuous Improvement

### EC-20: Feedback loop contamination
- **Scenario:** Spam or low-quality feedback dominates online improvements.
- **Impact:** Recommendation quality degrades over time.
- **Mitigation:** Feedback quality filters, rate limits, and weighted learning signals.
- **Test case idea:** Inject spam feedback and confirm minimal impact on ranking updates.

### EC-21: Metric blind spots
- **Scenario:** System tracks only latency, not relevance/satisfaction.
- **Impact:** Fast but poor recommendations go unnoticed.
- **Mitigation:** Monitor balanced KPI set: CTR, conversion, dwell time, and explicit ratings.
- **Test case idea:** Validate dashboard includes both performance and quality metrics.

### EC-22: Silent production failures
- **Scenario:** Parser/retrieval fails but API still returns success with empty payload.
- **Impact:** Hidden degradation and delayed incident response.
- **Mitigation:** End-to-end health checks, error budgets, and alerting on abnormal empty-result rates.
- **Test case idea:** Force component failure and verify alerting pipeline triggers.

## Cross-Cutting Security and Reliability Edge Cases

### EC-23: PII leakage in logs/prompts
- **Scenario:** User details are logged or forwarded beyond required scope.
- **Impact:** Privacy and compliance risks.
- **Mitigation:** PII redaction in logs, least-privilege data handling, and retention controls.
- **Test case idea:** Scan logs/prompts for prohibited fields after test requests.

### EC-24: Rate-limit abuse and burst traffic
- **Scenario:** Sudden spike or scripted abuse hits recommendation endpoint.
- **Impact:** Service instability and increased LLM cost.
- **Mitigation:** Rate limiting, request throttling, and queue-based graceful degradation.
- **Test case idea:** Load test with burst traffic and verify controlled degradation.

### EC-25: Partial system outage
- **Scenario:** One component (DB/LLM/provider) is unavailable.
- **Impact:** End-to-end flow interruption.
- **Mitigation:** Circuit breakers, fallback modes, and clear user-facing status messages.
- **Test case idea:** Simulate component outage and confirm fallback behavior.

## Recommended Priority for Initial Implementation

1. EC-09 Zero candidates after filtering
2. EC-13 Hallucinated recommendations
3. EC-16 LLM timeout/failure
4. EC-14 Output format violations
5. EC-05 Contradictory preferences
6. EC-15 Prompt injection
7. EC-22 Silent failures
8. EC-24 Rate-limit abuse
