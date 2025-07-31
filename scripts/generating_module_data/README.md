# Parser Idea

```python
import re

data = {
    'thanhphohochiminh': {'keywords': ['thanhphohochiminh', 'hochiminh', 'hcm']},
    'hanoi': {'keywords': ['hanoi', 'hn']},
}

# Step 1: Create keywords list, sorted by length desc
keywords = sorted(
    [kw for v in data.values() for kw in v['keywords']],
    key=len,
    reverse=True
)

# Step 2: Create regex pattern
pattern = re.compile('|'.join(re.escape(k) for k in keywords), flags=re.IGNORECASE)

# Step 3: Find keyword in address
address = 'quan 5, hcm'

match = pattern.search(address)
keyword = match.group(0) if match else None

# Step 4: Translate keyword to key
key = next((k for k, v in data.items() if keyword and keyword.lower() in [kw.lower() for kw in v['keywords']]), None)

print(key) # thanhphohochiminh
```


# Converter Idea
