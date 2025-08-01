# 📜 Scripts Overview

This directory contains utility scripts used throughout the project. Each subfolder is responsible for a specific stage in the data pipeline.

## 📥 [`collecting_data`](collecting_data)
Scripts for scraping and collecting administrative unit data from multiple sources.

## 🧹 [`processing_data`](processing_data)
Cleans, merges, and enriches raw data into multiple useful datasets.  
Results can be found in the [`data/processed`](../data/processed) directory.

## 🧱 [`generating_module_data`](generating_module_data)
Generates structured data used by the core library [`vietnamadminunits`](../vietnamadminunits).  
Results can be found in the [`vietnamadminunits/data`](../vietnamadminunits/data) directory.


### Parser Strategy

For each administrative level (`province`, `district`, `ward`), generate a set of:

- **Keys**: Unique identifiers used internally (e.g., `thanhphohochiminh`)
- **Keywords**: Variations and aliases (e.g., `thanhphohochiminh`, `hochiminh`, `tphcm`, `hcm`)

The parser uses **regular expressions (regex)** to search the input address string for known keywords.  
Once a match is found, it infers the corresponding key for that administrative level.

```python
import re

DICT_PROVINCE = {
    'thanhphohochiminh': {'provinceKeywords': ['thanhphohochiminh', 'hochiminh', 'hcm']},
    'hanoi': {'provinceKeywords': ['hanoi', 'hn']},
}

# Step 1: Create keywords list, sorted by length desc
province_keywords = sorted(sum([DICT_PROVINCE[k]['provinceKeywords'] for k in DICT_PROVINCE], []), key=len, reverse=True)

# Step 2: Create regex pattern
PATTERN_PROVINCE = re.compile('|'.join(province_keywords), flags=re.IGNORECASE)

# Step 3: Find keyword in address key (normalized)
address_key = 'quan5,hcm'

province_keyword = next((m.group() for m in reversed(list(PATTERN_PROVINCE.finditer(address_key)))), None)

# Step 4: Translate keyword to key
province_key = next((k for k, v in DICT_PROVINCE.items() if province_keyword and province_keyword in [kw for kw in v['provinceKeywords']]), None)

print(province_key) # thanhphohochiminh
```

### Converter Strategy

1. **Parse** the original (63-province) address into its corresponding administrative unit object.
2. **Identify** the new province key and construct the `province_district_ward` composite key from the old address.
3. **Lookup** the new ward key:
   - If the old ward key is mapped, use the mapped new ward key.
   - If not found, attempt to find the new province only (fallback), instead of raising an error.
4. **Build** a new address using the new province and new ward key.
5. **Parse** it into a new (34-province) administrative unit.

####  Future-proof Strategy

- **Province-level changes**:  
  If another major administrative restructure occurs (e.g. merging 34 provinces into a new configuration), a new converter module will be added to support conversion from the current **34-province** model to the new one (e.g. **?-province**).

- **Ward-level updates**:  
  If ward boundaries or names change in the future, the latest **34-province** dataset will be updated accordingly.  
  Old ward names will be retained as aliases to ensure backward compatibility with historical data.


## 🧪 [`module_testing`](module_testing)
Scripts for testing and validating the [`vietnamadminunits`](../vietnamadminunits) module's functionality.