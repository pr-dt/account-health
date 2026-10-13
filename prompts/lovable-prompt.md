Update this existing app so it matches the spec below exactly. Keep the three routes (/, /hold, /plan). Replace the current page content and styling with what is described here. Do not add pages, features, charts or text that are not listed.

Lines that start with "Rule:" are instructions for you. Never show them on screen. Everything in quotes is exact on-screen text.

==================================================
1. DESIGN SYSTEM (apply everywhere)
==================================================
- Stack: use the existing shadcn/ui components: Card, Badge, Button, Table, Sheet (for the drawer), Dialog (for modals), RadioGroup, Progress, Tooltip, Toast (sonner).
- Font: Inter. Sizes: page title 24px semibold; card title 16px semibold; body 14px; small text 12px. Use tabular numbers for all figures.
- Colours: page background #F5F7FA; cards white with a 1px #E4E7EC border, 12px radius, no heavy shadows; text #0F172A; secondary text #475569; primary #2563EB; top bar #0B1F44.
- Status colours, always paired with an icon AND a word, never colour alone: red #B42318 (lucide XCircle) for "Over limit" and "Paused"; amber #B54708 on #FFFAEB (lucide AlertTriangle) for "At risk", "Watch" and "Missing"; green #067647 on #ECFDF3 (lucide CheckCircle2) for "Working", "Tracking found" and completed steps.
- Spacing on an 8px grid. Card padding 24px. 24px between cards. Content max-width 1040px, centred, 32px page padding.
- Buttons 40px tall, 8px radius. At most one primary (solid blue) button per card; others are outline or link style.
- Every interactive element has a visible keyboard focus ring. Dialog and Sheet close on Esc and on overlay click (both count as Cancel) and trap focus while open.
- Responsive: below 900px the sidebar collapses behind a menu button in the top bar, two-column rows stack, and the tables scroll horizontally inside their card.
- Rule: no lorem ipsum, no emoji, no gradients, no placeholder images, no dead buttons. Every clickable thing in this spec must work.
- Rule: keep all interaction state in React state shared across the three pages (a context provider at the app root). Do not use localStorage or sessionStorage. Moving between pages keeps the state; a browser reload resets everything.
- Rule: the link to /hold#disputes scrolls the element with id "disputes" into view after the page renders. Every other navigation scrolls to the top.
- Browser tab titles: "Overview · Account Health", "Hold details · Account Health", "Action plan · Account Health".

==================================================
2. SHELL (all pages)
==================================================
- Top bar, 56px, #0B1F44, white text. Left: "Payments" (semibold) and, in lighter text, "Lumière Skincare". Right: "Updated 11 Oct, 9:40 AM" in small light text, then an outline pill "Sample data · Demo only".
- Left sidebar, 232px, white, right border. Items in order: Home, Transactions, Settlements, Account Health, Reports, a small uppercase group label "PAYMENT PRODUCTS", Payment Links, Payment Pages, Razorpay.me Link, Account & Settings. Each item has a small lucide icon.
- "Account Health" is the active item (light blue background, blue text) with a small "New" badge, and links to /.
- Rule: the other sidebar items are visual only: no hover pointer, not focusable, no link.
- Breadcrumb at the top of the content on every page: "Account Health" › "Hold details" › "Action plan", showing only up to the current page. Earlier parts are links (/ and /hold).

==================================================
3. PAGE /  (Overview)
==================================================
- Title "Account Health". Sub-line: "Your account's risk standing, and what to do about it."

A. Alert card (amber background, AlertTriangle icon):
   A small red badge "Urgent" above the title.
   Title "₹12,40,000 in settlements is on hold since 6 Oct"
   Text "Your chargeback rate is above the limit. New payments and refunds are still working."
   Primary button "See why and what to do" → /hold

B. Two cards side by side (score card one-third width, drivers card two-thirds):
   Score card:
   - Label "Health score"
   - Large "62" with a smaller "/ 100" beside it, and an amber Badge "At risk"
   - A small line chart (no axes, no gridlines) falling from 84 to 62 over 30 days, with aria-label "Score fell from 84 to 62 over the last 30 days"
   - Caption "Down from 84 over the last 30 days"
   - Small text "Healthy 70–100 · At risk 40–69 · Critical 0–39"
   - Small text under it: "A hold can be placed when any one driver is over its limit, whatever the total score."
   Drivers card, title "What is driving your score". Four rows, each with a name, a detail line and a status badge on the right:
   1. "Chargeback rate" / "1.8% in the last 30 days (14 of 778 orders). Limit is 1.0%." / red badge "Over limit". Under the detail line, a link "View the 9 linked chargebacks" → /hold#disputes.
   Rule: the red badge has background #FEF3F2.
   2. "Refund rate" / "9% this month. Your usual is 4%." / amber badge "Watch"
   3. "Delivery proof on file" / "71% of orders. Target is 95%." / amber badge "Watch"
   4. "KYC documents" / "GST certificate expires on 23 Oct." / amber badge "Watch"

C. Card "Early warning":
   "We first flagged your chargeback rate on 30 Sep, when it passed 0.8%. It has been above the 1.0% limit for 6 days and is still rising."

D. Small secondary text at the bottom: "Your score is calculated from fixed rules, not by AI. AI investigates patterns and suggests a plan, and you approve every step."

==================================================
4. PAGE /hold  (Hold details)
==================================================
- Title "Why ₹12,40,000 is on hold". Sub-line: "Held since 6 Oct · Includes every settlement due since then"

A. Key finding card (light blue background #EFF4FF, lucide Search icon):
   Small label "Likely driver"
   Text, semibold: "9 of your 14 chargebacks say 'item not received', and all 9 were shipped with Partner A."
   Primary button "See your action plan" → /plan
   Below the button, small text "Was this finding useful?" with two small outline buttons "Yes" and "No".
   Rule: clicking either replaces the question and buttons with small grey text "Thanks. This helps improve future findings." Nothing else changes.

B. Two cards side by side:
   "The reason": "Your chargeback rate reached 1.8% (14 of 778 orders in the last 30 days), above the 1.0% limit. Settlements are paused while your account is reviewed."
   "What is affected", three rows with a status on the right:
   - "Settlements to your bank" — red "Paused"
   - "Accepting new payments" — green "Working"
   - "Refunds to customers" — green "Working"

C. Card with id "disputes", title "The 9 'item not received' chargebacks", and on the right in small text "Shipping data updated 11 Oct, 9:40 AM".
   Table columns: Order | Opened | Reason | Courier | Tracking record
   LS-4102 | 14 Sep | Item not received | Partner A | Tracking found
   LS-4117 | 17 Sep | Item not received | Partner A | Tracking found
   LS-4125 | 19 Sep | Item not received | Partner A | Tracking found
   LS-4131 | 22 Sep | Item not received | Partner A | Tracking found
   LS-4140 | 24 Sep | Item not received | Partner A | Tracking found
   LS-4158 | 27 Sep | Item not received | Partner A | Tracking found
   LS-4163 | 29 Sep | Item not received | Partner A | Tracking found
   LS-4170 | 5 Oct | Item not received | Partner A | Missing
   LS-4186 | 7 Oct | Item not received | Partner A | Missing
   Rule: "Tracking found" is a green badge with a check icon; "Missing" is an amber badge with a warning icon.
   Under the table, two columns:
   "What we know": bullets "9 of 14 chargebacks share one reason and one courier." / "Tracking records exist for 7 of the 9." / "2 orders have no delivery proof yet." / "The other 5 chargebacks have mixed reasons and no shared pattern."
   "What we don't know yet": bullets "Whether the courier caused every chargeback." / "How each chargeback will be decided." / "How long the review will take."

D. Card "Timeline", a vertical list with a dot per entry, newest at the bottom:
   - "30 Sep" — "Early warning sent: chargeback rate passed 0.8%"
   - "5 Oct" — "Chargeback rate crossed the 1.0% limit"
   - "6 Oct" — "Settlements held and review opened"
   - "Now" — "Waiting for delivery proof on 2 orders"
   - "Next" — "Review time varies by case"
   Rule: the "Now" entry's dot is blue and filled; past dots are grey; "Next" is hollow.

E. Bottom row: small secondary text on the left "Some review details can't be shared for regulatory reasons." and on the right an outline button "See your action plan" → /plan.

==================================================
5. PAGE /plan  (Action plan)
==================================================
- Small badge "Prepared by AI · You approve every step"
- Title "Your plan to resolve the hold". Sub-line: "Ordered by the evidence you already have, then by effort. Nothing is sent until you approve it."

A. Progress card (full width, above the steps), three parts in a row:
   - "Progress": "X of 3 steps reviewed" (X = number of steps completed or skipped) with a Progress bar. A step counts once it is completed or skipped.
   - "Score now": "62"
   - "Projected if completed steps succeed": the projected score (62 plus points) plus the band word ("At risk" if below 70, "Healthy" if 70 or more). Under it, small text: "If every step succeeds: 73 · Healthy".
   Small text under the whole card: "Estimated with the same fixed rules as your score. Your actual score updates after the next account check."
   Rule: points = 9 when step 1 is completed, plus 1 for each order in step 2 given proof (0, 1 or 2). Step 3 adds nothing. Skipped steps add 0. Animate the number change briefly.
   Rule: show computed numbers only; never show braces, variable names or the formula.

B. Completion banner, shown only when all three steps are completed or skipped (green background, CheckCircle2 icon). If step 1 was completed: "Plan reviewed. We'll alert you when the Dispute Responder drafts are ready or your hold status changes." If step 1 was skipped: "Plan reviewed. We'll alert you when your hold status changes." If all three were skipped, show a grey banner instead: "All steps skipped. Undo any step to act on it."
   Rule: hide the banner again as soon as any step is undone.

C. Three step cards. Each card: a numbered circle (1, 2, 3), a title, a reason, two small badges, then an action row with a primary button and an outline "Skip" button.
   Rule: when a step is completed, replace its action row with a green CheckCircle2 icon and the step's status text, and give the card a light grey background (#F9FAFB). When skipped, replace the action row with grey "Skipped" and a link "Undo" that restores the step's buttons. Each card's state is independent.
   Rule: every completion shows a short toast with the same status text.
   Rule: only the first step that is not yet completed or skipped has a solid primary button; the other steps' primary buttons use the outline style.

   STEP 1
   Title: "Send 7 chargebacks to Dispute Responder with tracking attached"
   Reason: "Tracking records exist for 7 of the 9 linked orders. Dispute Responder, Razorpay's dispute agent, drafts a reply for each in review mode, so nothing is submitted until you approve it."
   Badges: "Est. score +9", "Evidence ready"
   Primary button "Review and hand off" opens a right-side Sheet:
     Title "7 chargebacks ready for Dispute Responder"
     Text "Tracking records will be attached to each chargeback."
     List of LS-4102, LS-4117, LS-4125, LS-4131, LS-4140, LS-4158, LS-4163, each with "Item not received · Partner A" and a green "Tracking found" badge
     Footer buttons: primary "Hand off 7 chargebacks", outline "Cancel"
   Rule: Cancel, Esc or overlay click closes with no change. "Hand off 7 chargebacks" closes the Sheet and completes the step.
   Status text: "Handed to Dispute Responder. 7 drafts will be ready for your review. Outcome pending."

   STEP 2
   Title: "Add delivery proof for the 2 remaining orders"
   Reason: "No usable proof was found for LS-4170 and LS-4186 at the last update. It may exist outside your connected records."
   Badges: "Est. score +1 per order", "Needs your input"
   Primary button "Add proof" opens a Dialog:
     Title "Add delivery proof"
     For each of LS-4170 and LS-4186, a RadioGroup with three options: "Delivery photo", "Signed receipt", "Not available"
     Helper text under the groups: "Choose an option for both orders. You will attach the file when you review the draft."
     Buttons: primary "Confirm", outline "Cancel"
   Rule: "Confirm" stays disabled until both orders have an option chosen. Cancel, Esc or overlay click closes with no change and clears the choices.
   Status text depends on the choices:
     both have proof → "Proof added for 2 orders. Outcome pending."
     one has proof → "Proof added for 1 order; 1 marked not available. Outcome pending."
     neither has proof → "No proof available for 2 orders. Outcome pending." Rule: in this case show a grey info icon instead of the green check, and a grey card background.

   STEP 3
   Title: "Review the courier partner linked to these disputes"
   Reason: "All 9 chargebacks are linked to Partner A. That is a pattern to check, not proof of cause. Compare couriers before changing anything."
   Badges: "No score change", "Check before changing"
   Primary button "Compare couriers" opens a Dialog:
     Title "Item-not-received chargebacks by courier, last 30 days"
     Table columns: Courier | Orders | Chargebacks | Chargeback rate | Delivery proof on file
       Partner A | 230 | 9 | 3.9% | 25%
       Partner B | 340 | 0 | 0% | 90%
       Partner C | 208 | 0 | 0% | 90%
     Rule: highlight the Partner A row with a light amber background.
     Text under the table: "A pattern to check with your courier, not proof of cause. Order mix can differ between couriers."
     Buttons: primary "Mark as reviewed", outline "Close"
   Rule: "Close", Esc or overlay click closes with no change. "Mark as reviewed" closes the Dialog and completes the step.
   Status text: "Comparison reviewed. No courier settings were changed."

D. Two cards side by side below the steps:
   "Also worth doing": "Your GST certificate expires on 23 Oct." Outline button "Mark for follow-up" → becomes grey text "Marked for follow-up" and a link "Undo".
   "What Account Health can do", three lines with the first word bold:
     "Read: your payment, chargeback and shipping records."
     "Prepare: recommendations and drafts for you to review."
     "Act: only on steps you approve. It cannot release settlements or change risk decisions."

E. Card "Why this order": "Account Health finds the likely cause and the order of work, and agents you already have, such as Dispute Responder, do the individual jobs. It starts with evidence you already have, then the missing records, then the courier check, so no costly change is made on a pattern alone. The order improves as outcomes from similar cases come in."

F. Small secondary text at the bottom: "Recommendations do not guarantee a chargeback or settlement outcome."
