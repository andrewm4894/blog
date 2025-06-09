---
title: "Stripe Webhook + GCP Functions Framework (Python)"
date: 2022-12-22
categories: 
  - "cloud"
  - "eng"
tags: 
  - "functions-framework"
  - "gcp"
  - "python"
  - "stripe"
  - "webhook"
coverImage: "stripe-functions-2.png"
---

This took a couple of days of messing around so decided to make a post out of it.

[Here](https://github.com/andrewm4894/stripe-webhook-gcp-function) is a minimal enough example repo using [Terraform](https://www.terraform.io/) and [GCP Functions Framework](https://cloud.google.com/functions/docs/functions-framework) to build a GCP Python function that will receive a [Stripe webhook](https://stripe.com/docs/webhooks) event, perform [signature verification](https://stripe.com/docs/webhooks/signatures), and then just [print the event](https://github.com/andrewm4894/stripe-webhook-gcp-function/blob/main/python-functions/stripe_webhook/main.py#L34). You can adapt and build whatever logic you want then on top of this.

**TL DR;** if you are looking at the stripe docs and cant figure out why you can run your python function locally but the signature verification fails once deployed to GCP functions (with this generic error message `error.SignatureVerificationError( stripe.error.SignatureVerificationError: No signatures found matching the expected signature for payload`) it could be that you need to replace `payload = request.data` with `payload = request.data.decode('utf-8')`. This i found out after a day or two thanks to [this SO comment](https://stackoverflow.com/a/71756270/1919374).

Most of what might be useful is in the [repo readme](https://github.com/andrewm4894/stripe-webhook-gcp-function#readme), but below i'll quickly walk through the structure and moving parts.

## Repo structure

Here are the main folders and files involved. Greyed out files are those that might have sensitive info and so are part of the [\`.gitignore\`](https://github.com/andrewm4894/stripe-webhook-gcp-function/blob/main/.gitignore) and so not to be committed to source control. I'll quickly walkthrough each folder and important files below.

![](/assets/images/2022-12-22-stripe-webhook-gcp-functions-framework-python/dir-1.png)

- `/python-functions` - The python code for the function lives in here.
    - `/stripe_webhook` - A folder just for the "stripe\_webhook" function.
        - `main.py` - Python source code for the function.
        
        - `requirements.txt` - Python libraries the function needs to run.
    
    - `/zipped` - A local folder of zipped up versions of the python function folders - this zip is what will be loaded to a GCS bucket as the source for the cloud function. This is ignored from source control and not needed.

- `/terraform` - All terraform related code and configuration files live in here to provision the cloud function and related cloud resources.
    - `conf.tf` - A file defining some confidential vars you want available to terraform but not in source control. See conf.example.tf for dummy example and instructions.
    
    - `gcp-cloud-functions.tf` - Terraform code to provision, configure and deploy all related cloud resources used by the function.
    
    - `gcp-secret-manager.tf` - Terraform code to define a GCP secret used by the cloud function. The Stripe secret will live in GCP secret manager.
    
    - `terraform.tf` - Some standard boilerplate used as part of Terraform set up and when initializing with \`terraform init\`
    
    - `variables.tf` - Some non-sensitive variables we want to use in defining our terraform resources.

- `/venv` - Our local python development virtual environment used for testing and debugging the function locally using the functions framework cli.

- `.env` - A env file that will be picked up when running the function locally so that the `stripe_endpoint_secret` environment variable will be available locally (coming from `.env` file) and when running in GCP cloud (from GCP secrets manager). Also make sure if not under source control, see `.example.env` for a dummy example.

- `.gitignore` - Things we want to make sure we don't add to source control.

- `requirements.txt` - Python libraries we want to install into our \`venv\` for local execution and debugging of the function.

## Run function locally

To run the function locally we can use the [functions framework cli](https://github.com/GoogleCloudPlatform/functions-framework-python#quickstart-http-function-hello-world) like below:

```bash
# run function locally in debug mode on port 8081
functions-framework --source=./python-functions/stripe_webhook/main.py \
  --target=stripe_webhook \
  --debug \
  --port=8081
```

This should return something like below to show the function running locally on port 8081 (you can use whatever port you want).

```powershell
(venv) PS > functions-framework --source=./python-functions/stripe_webhook/main.py \
  --target=stripe_webhook \
  --debug \
  --port=8081
 * Serving Flask app 'stripe_webhook'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8081
Press CTRL+C to quit
 * Restarting with watchdog (windowsapi)
 * Debugger is active!
 * Debugger PIN: XXX-XXX
```

## Stripe CLI

### Set up local forwarding

Once the function is running locally you can use the [stripe cli](https://stripe.com/docs/stripe-cli) to (1) forward events to a local endpoint and then (2) trigger some test events to see the response.

```powershell
# once function is running locally you can forward events to local endpoint
stripe listen --forward-to localhost:8081
```

You should see something like this when local forwarding is set up:

```powershell
PS C:\Users\andre> stripe listen --forward-to localhost:8081
> Ready! You are using Stripe API Version [2022-11-15]. Your webhook signing secret is xxx_xxxxxx (^C to quit)
```

### Create some test events

```bash
# create a test event
stripe trigger payment_intent.succeeded
```

You should see something like this for a successful test event creation:

```powershell
PS C:\Users\andre> stripe trigger payment_intent.succeeded
Setting up fixture for: payment_intent
Running fixture for: payment_intent
Trigger succeeded! Check dashboard for event details.
```

If the function as been invoked successfully then in the window from step 1 above you should see something like this:

```powershell
PS C:\Users\andre> stripe listen --forward-to localhost:8081
> Ready! You are using Stripe API Version [2022-11-15]. Your webhook signing secret is xxx_xxxxxx (^C to quit)
2022-12-22 12:31:10   --> charge.succeeded [evt_3MHnvQFE3Qfj39xW1UE7UhT6]
2022-12-22 12:31:10   --> payment_intent.succeeded [evt_3MHnvQFE3Qfj39xW1vzt9gAn]
2022-12-22 12:31:10   --> payment_intent.created [evt_3MHnvQFE3Qfj39xW1KR01wQ8]
2022-12-22 12:31:10  <-- [200] POST http://localhost:8081 [evt_3MHnvQFE3Qfj39xW1UE7UhT6]
2022-12-22 12:31:11  <-- [200] POST http://localhost:8081 [evt_3MHnvQFE3Qfj39xW1vzt9gAn]
2022-12-22 12:31:11  <-- [200] POST http://localhost:8081 [evt_3MHnvQFE3Qfj39xW1KR01wQ8]
```

Finally in the window where you triggered the functions framework to run you should just see the a json string with all the event info itself.

```powershell
(venv) PS C:\Users\andre\Documents\repos\stripe-webhook-gcp-function> functions-framework --source=./python-functions/stripe_webhook/main.py --target=stripe_webhook --debug --port=8081
 * Serving Flask app 'stripe_webhook'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8081

Press CTRL+C to quit
 * Restarting with watchdog (windowsapi)
 * Debugger is active!
 * Debugger PIN: 107-679-323
{"id": "evt_3MHnvQFE3Qfj39xW1UE7UhT6", "object": "event", "api_version": "2022-11-15", "created": 1671712265, "data": {"object": {"id": "ch_3MHnvQFE3Qfj39xW1ljeXQ0U", "object": "charge", "amount": 2000, "amount_captured": 2000, "amount_refunded": 0, 
...
"name": "Jenny Rosen", "phone": null, "tracking_number": null}, "source": null, "statement_descriptor": null, "statement_descriptor_suffix": null, "status": "requires_payment_method", "transfer_data": null, "transfer_group": null}}, "livemode": false, "pending_webhooks": 4, "request": {"id": "req_BsagVXD6LQwqjH", "idempotency_key": "e36a0855-a9e6-441a-b9ca-181632fd43ad"}, "type": "payment_intent.created"}
127.0.0.1 - - [22/Dec/2022 12:31:11] "POST / HTTP/1.1" 200 -
```

## Thats it

That's it, you can then add whatever additional logic you want to handle specific stripe webhook events and control what events make it to this webhook from within the stripe ui itself as needed.

The developer tools and experience with Stripe is really good and being able to so easily run a cloud function locally with realistic test data from stripe using these two cli's (`stripe` and `functions-framework`) is really nice, even if it did take me a few days to realize I needed to use that `.decode('utf-8')` once the function was deployed to GCP cloud - there's always going to be something that trips you up a little :)
