import json
import logging

from configs import cfg

from core.auth import authenticate
from core.customer import generate_customer_token
from core.metrics import fetch_compute_job_status

log = logging.getLogger(__name__)


job_id1 = "672ee90a-3873-4f9c-ab2f-f522bda949d0"
job_id2 = "0a126d5f-9cc6-4fa1-ad92-e9dd224a6fbc"

client = authenticate(cfg)
generate_customer_token(client, cfg.NEW_CUSTOMER_PAYLOAD["email"])
status = fetch_compute_job_status(client, job_id2, parentId=1)
print(json.dumps(status, indent=2))

timerange = client.compute_time_range(extBatchId=job_id2)
print(json.dumps(timerange, indent=2))
