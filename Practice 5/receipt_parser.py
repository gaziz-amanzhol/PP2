import re
import json


def parse_receipt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    receipt_data = {
        "store_info": {},
        "items": [],
        "totals": {},
        "payment": {}
    }

    # Extract store name
    store_match = re.search(r"^(.+?)(?:\n|Store)", content, re.MULTILINE)
    if store_match:
        receipt_data["store_info"]["name"] = store_match.group(1).strip()

    # Extract date
    date_match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", content)
    if date_match:
        receipt_data["store_info"]["date"] = date_match.group(1)

    # Extract time
    time_match = re.search(r"(\d{1,2}:\d{2}(?:\s?[AP]M)?)", content, re.IGNORECASE)
    if time_match:
        receipt_data["store_info"]["time"] = time_match.group(1)

    # Extract items with prices
    item_pattern = r"([A-Za-z\s]+?)\s+(\$?\d+\.\d{2})"
    items = re.findall(item_pattern, content)

    for item_name, price in items:
        item_name = item_name.strip()
        # Skip lines that are likely totals
        if not any(word in item_name.lower() for word in ['subtotal', 'tax', 'total', 'change', 'cash', 'card']):
            receipt_data["items"].append({
                "name": item_name,
                "price": price.replace('$', '')
            })

    # Extract all prices
    all_prices = re.findall(r"\$?(\d+\.\d{2})", content)
    receipt_data["all_prices"] = all_prices

    # Extract subtotal
    subtotal_match = re.search(r"Subtotal[:\s]+\$?(\d+\.\d{2})", content, re.IGNORECASE)
    if subtotal_match:
        receipt_data["totals"]["subtotal"] = subtotal_match.group(1)

    # Extract tax
    tax_match = re.search(r"Tax[:\s]+\$?(\d+\.\d{2})", content, re.IGNORECASE)
    if tax_match:
        receipt_data["totals"]["tax"] = tax_match.group(1)

    # Extract total
    total_match = re.search(r"Total[:\s]+\$?(\d+\.\d{2})", content, re.IGNORECASE)
    if total_match:
        receipt_data["totals"]["total"] = total_match.group(1)

    # Extract payment method
    if re.search(r"\bcash\b", content, re.IGNORECASE):
        receipt_data["payment"]["method"] = "Cash"
        cash_match = re.search(r"Cash[:\s]+\$?(\d+\.\d{2})", content, re.IGNORECASE)
        if cash_match:
            receipt_data["payment"]["amount"] = cash_match.group(1)
        change_match = re.search(r"Change[:\s]+\$?(\d+\.\d{2})", content, re.IGNORECASE)
        if change_match:
            receipt_data["payment"]["change"] = change_match.group(1)
    elif re.search(r"\bcard\b|\bcredit\b|\bdebit\b", content, re.IGNORECASE):
        receipt_data["payment"]["method"] = "Card"

    # Extract phone number
    phone_match = re.search(r"(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})", content)
    if phone_match:
        receipt_data["store_info"]["phone"] = phone_match.group(1)

    # Extract address
    address_match = re.search(r"(\d+\s+[\w\s]+(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard))", content, re.IGNORECASE)
    if address_match:
        receipt_data["store_info"]["address"] = address_match.group(1)

    return receipt_data


def display_receipt(data):
    print("=" * 50)
    print("RECEIPT RESULTS")
    print("=" * 50)

    if data["store_info"]:
        print("\nSTORE INFORMATION:")
        for key, value in data["store_info"].items():
            print(f"  {key.title()}: {value}")

    if data["items"]:
        print("\nITEMS:")
        for i, item in enumerate(data["items"], 1):
            print(f"  {i}. {item['name']:30s} ${item['price']}")

    if data["all_prices"]:
        print(f"\nALL PRICES FOUND: {', '.join(data['all_prices'])}")

    if data["totals"]:
        print("\nTOTALS:")
        for key, value in data["totals"].items():
            print(f"  {key.title():15s} ${value}")

    if data["payment"]:
        print("\nPAYMENT:")
        for key, value in data["payment"].items():
            print(f"  {key.title():15s} {value}")

    print("\n" + "=" * 50)


def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nsaved to {output_file}")


if __name__ == "__main__":
    receipt_data = parse_receipt("raw.txt")
    display_receipt(receipt_data)
    save_to_json(receipt_data, "parsed_receipt.json")
    if receipt_data["items"]:
        calculated_total = sum(float(item["price"]) for item in receipt_data["items"])
        print(f"\nCalculated total from items: ${calculated_total:.2f}")
