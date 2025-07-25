import json
import logging
import sys

from core.clients.onboarding_client import OnboardingApiClient
from core.configs import cfg
from core.utils.logger import setup_logging

setup_logging()
log = logging.getLogger(__name__)


def main():
    """Deletes a partner account."""
    customer_email = cfg.NEW_CUSTOMER_PAYLOAD["email"]
    client = OnboardingApiClient(
        base_url=cfg.ONBOARDING_API_URL,
        email=cfg.ADMIN_EMAIL,
        password=cfg.ADMIN_PASSWORD,
    )

    try:
        # 1) Authenticate and get the necessary tokens
        log.info("Authenticating partner and customer tokens...")
        client.authenticate()

        partners = client.list_partners()
        log.debug(json.dumps(partners, indent=2))
        customer_id = next(
            (p["id"] for p in partners if p["email"] == customer_email),
            None,
        )
        log.info(f"Partner ID for {customer_email}: {customer_id}")
        deletion = client.delete_partner(customer_id)
        log.info(f"Partner deleted: {deletion}")

    except Exception as e:
        log.error(f"An error occurred during partner deletion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
