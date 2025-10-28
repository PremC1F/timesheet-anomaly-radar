# Timesheet Anomaly Radar

This repository demonstrates how a machine‑learning powered feature could be
integrated into **Rippling’s App Studio** using a simple external API. It
includes a synthetic timesheet dataset, a lightweight FastAPI service that
exposes anomaly records, and guidance on how this might be wired into
Rippling’s platform.

## What is Rippling’s App Studio?

Rippling’s **App Studio** is a no‑code builder that lets teams create custom
applications on top of their company’s **Employee Graph**—a unified
representation of people, teams and permissions. With App Studio you can:

- Build dashboards, forms and lists without writing frontend code.
- Leverage built‑in roles and permissions: managers only see their own team
  data, HR sees the entire company, etc.
- Pull data from external services via REST APIs and combine it with
  internal data.
- Trigger downstream actions using **Workflow Studio**, such as sending a
  Slack message when a button is clicked or updating a record when a form
  is submitted.

The result is a platform where non‑technical staff can build useful HR,
finance and IT tools that feel native to Rippling.

## What is this demo?

The **Timesheet Anomaly Radar** is a mini‑project that illustrates how you
might augment App Studio with a machine‑learning service. The idea:

1. **Detect unusual shifts.** We generate a synthetic dataset of 300
   timesheet entries for ten employees across four teams. Each entry
   includes scheduled start/end times, actual start/end times, location
   (office vs remote) and flags indicating whether the record is
   anomalous. An anomaly is triggered if the shift starts or ends more
   than one hour from schedule, if the duration is off by more than two
   hours, or if the location doesn’t match the expected one.
2. **Expose an external API.** A small [FastAPI](https://fastapi.tiangolo.com/)
   application reads the dataset and exposes two endpoints:
   - `GET /api/anomalies` returns a list of flagged records, optionally
     filtered by team or date. Each record includes the anomaly reason and
     a numeric score.
   - `POST /api/decision` lets a manager record a decision on a record
     (e.g., Approve, Escalate, Dismiss). Decisions are appended to a CSV
     file and could later be used to retrain the model.
3. **Wire it into App Studio.** In a real Rippling environment you would
   create a table‑style component that calls `GET /api/anomalies` to
   populate rows. Row actions would call `POST /api/decision` with the
   appropriate record ID and decision. Using Workflow Studio you could
   automate notifications: when a manager clicks “Escalate” the app could
   send them a Slack DM with a link back to the record.

This demo emphasises how to translate a product need—reducing payroll errors
and catching fraudulent shifts—into a mathematical formulation (anomaly
rules), implement it in code and ship it behind an API that App Studio
can consume.

## File structure

```
timesheet_anomaly_demo/
├── app.py       # FastAPI service exposing anomalies and decisions
├── data.csv     # Synthetic timesheet dataset with 300 records
└── README.md    # This documentation
```

## Running the service

1. **Install dependencies** (ideally in a virtual environment):

   ```bash
   pip install fastapi uvicorn pandas pydantic
   ```

2. **Start the API** from inside `timesheet_anomaly_demo`:

   ```bash
   uvicorn app:app --reload
   ```

   This will launch the service on `http://127.0.0.1:8000`. Navigate to
   `http://127.0.0.1:8000/docs` to explore the interactive Swagger UI.

3. **Example requests**:

   - List all anomalies:
     `curl image.pnghttp://127.0.0.1:8000/api/anomalies`
   - Filter by team:
     `curl 'http://127.0.0.1:8000/api/anomalies?team=Support'`
   - Record a decision:
     ```bash
     curl -X POST http://127.0.0.1:8000/api/decision \
          -H 'Content-Type: application/json' \
          -d '{"record_id": 42, "decision": "Escalate", "note": "Possible duplicate entry"}'
     ```

## Integrating with Rippling App Studio

While this repository cannot connect directly to Rippling’s infrastructure,
the following steps outline how you could integrate this API into an App
Studio application:

1. **External API definition:** In App Studio, define a new external API
   with the base URL pointing at your running service (e.g.,
   `https://your-domain.com/timesheet_api`). Define two methods:
   `GET /api/anomalies` and `POST /api/decision`.
2. **Table widget:** Create a table component bound to the `GET
   /api/anomalies` response. Map fields like `employee_name`,
   `scheduled_start` and `anomaly_reason` to columns. Add row actions
   “Approve”, “Escalate” and “Dismiss”.
3. **Row action wiring:** Configure each action to call `POST
   /api/decision` with the selected row’s `record_id` and the chosen
   decision. For example, the “Escalate” action might send `{ record_id:
   row.record_id, decision: 'Escalate' }`.
4. **Workflow automation:** Using Workflow Studio, attach a rule to the
   “Escalate” action that sends a Slack message to the manager of the
   employee (this is trivial in App Studio because you can reference the
   Employee Graph’s reporting structure). The message could include a
   short summary of the anomaly and a link back to the row in the table.

By following these steps you’ll have an end‑to‑end demo: a backend service
for scoring timesheet anomalies, an App Studio interface for reviewing
them, and automated notifications to streamline manager workflows.

## Extending this demo

This repository is intentionally lightweight. Here are some directions
you might explore to make it more realistic:

- **Replace the rule‑based anomaly detection** with a trained model. For
  instance, compute features (hours worked, deviation from schedule,
  location mismatch) and train an Isolation Forest or autoencoder. Store
  the model in the repository and load it in `app.py`.
- **Add authentication**. In production you’d secure the API with a token
  or OAuth, and App Studio would manage the credentials.
- **Persist decisions** to a database instead of a CSV file. Over time
  these labels could feed back into a retraining pipeline.
- **Visualise anomalies**. In App Studio you could add a chart showing
  anomaly count per team over time. The `/api/anomalies` endpoint can
  already be filtered by date, so it’s easy to plot trends.

We hope this project helps illustrate how machine learning and Rippling’s
App Studio can work together to deliver smarter HR tooling.
