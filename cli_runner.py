"""
Standalone CLI runner for kiro-register-en
Uses their registration logic with built-in temp email
"""
import sys
import os
sys.path.insert(0, 'B:/Project B/kiro-register-en')
sys.path.insert(0, 'B:/Project B/kiro-farmer')

import asyncio
from kiro_register import register_kiro_account
from email_service import EmailService
import json
from datetime import datetime

async def run_registration(num_accounts=1):
    """Run Kiro registration using their module"""

    print(f"\n{'='*60}")
    print(f"KIRO AUTO-REGISTRATION (using nopperabbo's module)")
    print(f"{'='*60}\n")
    print(f"Target: {num_accounts} accounts\n")

    created = []

    for i in range(1, num_accounts + 1):
        print(f"\n{'='*60}")
        print(f"Account #{i}/{num_accounts}")
        print(f"{'='*60}")

        # Get temp email
        email_service = EmailService('guerrillamail')
        email = email_service.get_email()

        if not email:
            print("ERROR: Failed to get temp email")
            continue

        print(f"Email: {email}")

        try:
            # Call their registration function
            # This uses playwright-stealth + anti-detection
            result = await register_kiro_account(
                email=email,
                mail_provider=email_service,
                captcha_solver=None,  # Manual captcha if needed
                headless=False,  # Visible for debugging
                proxy=None
            )

            if result and result.get('success'):
                account_data = {
                    'email': email,
                    'password': result.get('password'),
                    'token': result.get('token'),
                    'created_at': datetime.now().isoformat(),
                    'credits': 50
                }

                created.append(account_data)

                # Save
                with open('B:/Project B/kiro-register-en/accounts_created.txt', 'a') as f:
                    f.write(json.dumps(account_data) + '\n')

                print(f"\nSUCCESS! {len(created)}/{num_accounts} complete")
            else:
                print(f"\nFAILED: {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"\nERROR: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"COMPLETE!")
    print(f"{'='*60}")
    print(f"Created: {len(created)}/{num_accounts} accounts")
    print(f"Total credits: {len(created) * 50}")
    print(f"Saved to: B:/Project B/kiro-register-en/accounts_created.txt\n")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--accounts', type=int, default=1)
    args = parser.parse_args()

    asyncio.run(run_registration(args.accounts))
