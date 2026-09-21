# Arabian Kitchen — Data Cleaning Report
- Raw rows loaded: **79,796**
- Unique item-name spellings before cleaning: **40** -> after: **19**
- Missing `unit_price` values: **1606** (imputed with item-level median)
- Missing `payment_mode` values: **1199** (labeled UNKNOWN)
- Missing `platform` for non-delivery orders: **28225** (labeled N/A)
- Exact duplicate rows removed: **630**
- Refund/cancellation rows separated out: **397**
- Clean sales rows remaining: **78,769**

**Final clean dataset:** `arabian_kitchen_orders_clean.csv` — 78,769 rows, 14 columns
**Refunds dataset:** `arabian_kitchen_refunds.csv` — 397 rows
