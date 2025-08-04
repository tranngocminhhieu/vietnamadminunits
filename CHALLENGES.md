# CHALLENGES

## PARSE LEGACY ADMIN UNITS

### Có nhiều cuộc sáp nhập phường xã trong khoảng 2024-10 và 2025-02

Không phải sáp nhập 34 tỉnh thành, mà là sáp nhập trong khi vẫn còn 63 tỉnh thành.

Nhờ data admin units của Shopee mới thấy nhiều tên cũ còn sử dụng.

**Giải pháp**: Tìm kiếm trên Google với từ khóa _"{tên tỉnh} sáp nhập {danh sách tên phường cũ}"_, dựa vào thông tin trên các trang uy tính để bổ sung danh sách alias keywords.

[data/alias_keywords/legacy/legacy_ward.csv](data/alias_keywords/legacy/legacy_ward.csv)

### 12 huyện / thị xã / thành phố trùng tên ngắn trong cùng một tỉnh

| province        | district           | districtShort        |
|:----------------|:-------------------|:---------------------|
| Tỉnh Hà Tĩnh    | Huyện Kỳ Anh       | Kỳ Anh (Huyện)       |
| Tỉnh Hà Tĩnh    | Thị xã Kỳ Anh      | Kỳ Anh (Thị xã)      |
| Tỉnh Hậu Giang  | Huyện Long Mỹ      | Long Mỹ (Huyện)      |
| Tỉnh Hậu Giang  | Thị xã Long Mỹ     | Long Mỹ (Thị xã)     |
| Tỉnh Tiền Giang | Huyện Cai Lậy      | Cai Lậy (Huyện)      |
| Tỉnh Tiền Giang | Thị xã Cai Lậy     | Cai Lậy (Thị xã)     |
| Tỉnh Trà Vinh   | Huyện Duyên Hải    | Duyên Hải (Huyện)    |
| Tỉnh Trà Vinh   | Thị xã Duyên Hải   | Duyên Hải (Thị xã)   |
| Tỉnh Đồng Tháp  | Huyện Cao Lãnh     | Cao Lãnh (Huyện)     |
| Tỉnh Đồng Tháp  | Thành phố Cao Lãnh | Cao Lãnh (Thành phố) |
| Tỉnh Đồng Tháp  | Huyện Hồng Ngự     | Hồng Ngự (Huyện)     |
| Tỉnh Đồng Tháp  | Thành phố Hồng Ngự | Hồng Ngự (Thành phố) |

Ảnh hưởng đến việc sử dụng tên ngắn làm keyword.

**Giải pháp**:
- Thêm từ khóa có kèm type phía sau, và type viết tắt viết trước, ví dụ: kyanhthixa, txkyanh.
- Ưu tiên Thị xã và Thành phố là mặc định nếu không match type nào. Vì type cao hơn sẽ có diện tích và dân số nhiều hơn.
- Bổ dung giải pháp như phư Thành phố Huế (cũ).

### Thành phố Huế (cũ) chia thành 2 quận mới

**Giải pháp**:
- Dựa vào phường / xã để chọn quận.
- Nếu không có phường / xã, chọn quận mặc định là quận có nhiều phường / xã nhất.

## PARSE FROM-2025 ADMIN UNITS


## CONVERT 2025