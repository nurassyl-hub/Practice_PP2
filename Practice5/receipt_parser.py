import re
import json

def parse_europharma_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    price_pattern = r'(\d+[\s]?\d+,\d{2})'
    all_values = re.findall(price_pattern, content)
    
    total_match = re.search(r'ИТОГО:\s*\n\s*([\d\s]+,\d{2})', content)
    
    date_time = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})', content)

    payment_method = "Карта" if "Банковская карта" in content else "Наличные"

    data = {
        "items_found": len(all_values),
        "total_amount": total_match.group(1).replace(' ', '') if total_match else "Not found",
        "date_time": date_time.group(1) if date_time else "Not found",
        "payment_method": payment_method
    }
    
    return data

if __name__ == "__main__":
    result = parse_europharma_receipt('raw.txt')
    print(json.dumps(result, indent=4, ensure_ascii=False))
