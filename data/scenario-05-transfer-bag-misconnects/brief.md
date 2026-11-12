# 05 · Harborline Ground Services: which transfer bags get a runner

*Six van crews, 5,700 transfer bags a day, and roughly one bag in fifteen that will not make its flight on its own.*

## The business

Harborline Ground Services is the ground handler at Calder Bay International, the hub of Larkspur Airways. It runs
Larkspur's transfer baggage: bags that arrive on one Larkspur flight and leave on another, about **2.1 million a year**,
some 5,700 a day. The five concourses, A to E, stand in a line along one airside road. A transfer bag is unloaded,
tugged to the transfer sort under Concourse C, scanned, sorted to the belt of its next flight and tugged out to that
aircraft. When the system works, nobody touches the bag by hand.

When Harborline took over the contract in January, Larkspur's old hot-transfer team, which drove tight bags straight
from one aircraft to the other, had been disbanded. The new contract pays for six van crews, which start this winter.
Until then every transfer bag goes through the belt system, and that is what the data record.

It has been a busy year on the airfield. Concourse E opened its first gates in the spring; its second phase opened in
July, and it now handles about one Larkspur flight in six. Summer brought the afternoon thunderstorms, when a lightning
alert stops all work on the open ramp until it clears.

## The people

**Marisol Ferreira, Station General Manager, Harborline.** Marisol negotiated the contract and answers for its costs.

> "Every transfer bag that misses its flight costs us $175. Larkspur recharges us the courier who delivers it, about $95,
> and the passenger's interim expenses, about $35, and takes a $45 service penalty off our invoice. A run costs us $16 a
> bag in crew and van time. I don't want a van moving for a bag that would have made it anyway, and I don't want a van
> parked while a bag we could have saved goes to the courier."

**Kwame Asante, Hot-Transfer Crew Chief.** Kwame ran the old runner team for eleven years and came back to build the new
one.

> "Six crews, two people and a van each. Over a day that is about 340 bags, six in every hundred transfer bags, and not
> one more: a crew out on a run can't take the next one. When we take a bag that's in trouble, we get it on the aircraft
> about four times in five; the fifth one, the door's already closed. A bag that would have made it on the belt makes it
> with us too.
>
> "And the minimum connect time is a fiction. The airport adds a flat five or ten minutes for any change of concourse,
> next door or end to end. A to E is a twenty-minute tug drive, and since the tunnel went to one lane, B to D crawls."

**Renata Szabo, Transfer Duty Manager, Harborline.** Renata runs the day-shift transfer desk and wrote the crews' plan.

> "We already know which bags are tight. The desk sees every bag's scheduled connection. The plan is to give the runners
> the shortest scheduled connections first and work down the list until the crews are full. It's connection time. It
> always has been.
>
> "Since January, about one transfer bag in fifteen has missed its flight. When we ran my list on paper against this
> year's bags, about a third of the bags on it did miss."

**Desmond Okafor, Hub Customer Service Director, Larkspur Airways.** Desmond is the airline's voice at the hub.

> "A premium passenger whose bag doesn't show up is a letter I answer personally. Put every priority-tagged bag with a
> tight connection on a runner, whatever your model says."

Marisol disagrees: "The contract charges us the same $175 for a priority bag as for any other. If Larkspur wants premium
bags first, that is a commercial conversation, not something the runners should guess at."

## The decision

About forty minutes before an inbound Larkspur flight lands, its arrival estimate firms up and its stand is assigned.
The transfer desk then sees every transfer bag on board and decides, bag by bag, whether to give it to a runner, who
meets it at the aircraft and drives it to its departing flight. Every other bag goes through the belt system.

Your model runs at that forty-minute point and can use only what the desk knows then. You are asked whether it can
choose better than Renata's list, how many bags the runners should take, and what that is worth to Harborline in a year.

A passenger who will plainly miss the connection is rebooked before landing, and the bag is rerouted with them
automatically. Those bags never reach the desk and are not in the data: every row is a bag whose passenger was still
booked on the connecting flight at the forty-minute point.

## The data

Each row is one transfer bag. The data are synthetic, generated for this course.

- `train.csv` and `test.csv`: a random sample of 7,200 bags from January to June 2026, with the outcome, split into
  5,400 training bags and 1,800 test bags.
- `holdout_features.csv`: 2,000 bags from July and August 2026, a later period, without the outcome.

The files are exports from the business's own systems, as they came out: nobody has cleaned them.

### Data dictionary

| Column | Meaning | Values or units | Recorded |
|---|---|---|---|
| `id` | Harborline's transfer-bag record number | `TRB-` and seven digits | When the record is created |
| `arrival_hour` | Scheduled arrival hour of the inbound flight | 6 to 23, local | Timetable |
| `day_of_week` | Day of the inbound flight | `Mon` to `Sun` | Timetable |
| `itinerary_type` | Inbound and outbound flights, domestic or international | `dom-dom`, `dom-intl`, `intl-dom`, `intl-intl` | At booking |
| `arrival_concourse` | Concourse where the inbound aircraft parks | `A` to `E` | Forty-minute point |
| `departure_concourse` | Concourse of the outbound flight | `A` to `E` | Forty-minute point |
| `outbound_region` | Region of the outbound flight's destination | ten regions | Timetable |
| `inbound_aircraft` | Size of the inbound aircraft | `regional`, `narrowbody`, `widebody` | Timetable |
| `remote_stand` | 1 when the inbound parks on a remote stand and its bags are tugged across the open apron | 0 or 1 | Forty-minute point |
| `scheduled_connection_min` | Inbound's scheduled arrival to outbound's scheduled departure | minutes | At booking |
| `inbound_delay_min` | Inbound's expected delay from its arrival estimate (negative: early) | minutes | Forty-minute point |
| `min_connect_min` | The airport's published minimum connect time for this itinerary and concourse change | minutes | Published table |
| `transfer_bags_on_inbound` | Transfer bags on the inbound flight. Blank where the sorting system's feed dropped the inbound count. | count | Forty-minute point |
| `sort_load_pct` | Bags planned through the transfer sort in the arrival hour, as a share of its design throughput | percent | The day before |
| `bsm_lead_min` | How long before the arrival estimate the origin station's baggage message for this bag arrived. Blank when none came: the passenger's record shows a checked bag, but the sort has no routing for it and it is read by hand when unloaded | minutes, or blank | Forty-minute point |
| `lightning_alert` | 1 when a lightning alert was in force on the ramp at the forty-minute point | 0 or 1 | Forty-minute point |
| `priority_tag` | 1 when the bag has a priority tag (premium cabin or elite passenger) | 0 or 1 | At check-in |
| `misconnected` | **Target.** 1 when the bag did not leave on the passenger's connecting flight | 0 or 1 | When the outbound departs |
| `delivered_by_courier` | 1 when the bag reached the passenger through a contracted courier | 0 or 1 | When the bag's file closes, days later |

## How you solve it

This brief describes the business, not the analysis. Nothing in it says how to prepare the data, which models to try, how to measure them or what decision rule to recommend: those choices are your team's, and making them well is what the project tests. The people quoted here are not data scientists, so treat what they say as evidence to test, not instructions to follow.

Justify every choice in your notebook: what you did, why it suits this business and this data, and what you considered and set aside. A choice without a reason earns little credit, even when it is a good one.

Use only the methods this course teaches; the project guide lists them. If an AI tool proposes a method that is not on that list, do not use it: work that relies on a method from outside the course loses marks, however well it scores.

## What you submit

A file named `TeamName_holdout_predictions.csv` with one row for each of the 2,000 holdout bags and three columns:
`id` (from `holdout_features.csv`); `score` (your model's probability that the bag misconnects); and `decision`
(1 = give the bag to a runner; 0 = leave it to the belt system).

The crews can take at most 6% of the holdout bags: 120 bags. If your file gives more than 120 bags to a runner, only the
120 with the highest `score` are counted as run, and the rest are treated as left to the belt system.

The instructor scores your holdout submission by what your decisions would have cost Harborline Ground Services on
those records, using the figures in this brief.

*This scenario and its data are fictional and were generated for teaching. Any resemblance to a real organization or person is coincidental.*
