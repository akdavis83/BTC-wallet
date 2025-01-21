import requests
import json
from datetime import datetime, timezone
import time

def get_last_transaction_time(address):
    """Fetches the last transaction time for a given Bitcoin address using the blockchain.com API."""
    url = f"https://blockchain.info/rawaddr/{address}"
    try:
      response = requests.get(url, timeout=5)
      response.raise_for_status() # raise exception for bad status codes
      data = response.json()
      if data.get("txs"):
        last_tx = data["txs"][0]
        timestamp = last_tx["time"]
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
      else:
        return None # Address has no transactions

    except requests.exceptions.RequestException as e:
      print(f"Error fetching data for {address}: {e}")
      return None

def find_and_sort_inactive_addresses(addresses):
  """Identifies inactive addresses based on last transaction time and sorts them."""
  address_info = []
  for address in addresses:
    print(f"Checking address: {address}")
    last_tx_time = get_last_transaction_time(address)
    if last_tx_time:
      address_info.append({"address": address, "last_activity": last_tx_time})
    else:
      address_info.append({"address": address, "last_activity": None})
    time.sleep(1) # Pause to prevent hitting API limits

  # Sort by inactivity (furthest in the past or None first)
  sorted_addresses = sorted(address_info,
      key=lambda item: item["last_activity"] if item["last_activity"] else datetime.min,
      reverse=False)

  print("\nResults (Sorted by Inactivity):")
  for item in sorted_addresses:
      address = item["address"]
      last_activity = item["last_activity"]
      if last_activity:
        print(f"- Address: {address}, Last Activity: {last_activity.strftime('%Y-%m-%d %H:%M:%S UTC')}")
      else:
          print(f"- Address: {address}, No Transactions Found")


if __name__ == "__main__":
    addresses_to_check = input("Enter a list of Bitcoin addresses, separated by commas: ").split(",")
    addresses_to_check = [address.strip() for address in addresses_to_check]
    find_and_sort_inactive_addresses(addresses_to_check)