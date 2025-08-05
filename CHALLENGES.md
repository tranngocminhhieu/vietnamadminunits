# CHALLENGES

## PARSE LEGACY ADMIN UNITS

### Có nhiều cuộc sáp nhập ward trong khoảng 2024-10 và 2025-02

Không phải sáp nhập 34 tỉnh thành, mà là sáp nhập trong khi vẫn còn 63 tỉnh thành.

Nhờ data admin units của Shopee mới thấy nhiều tên cũ còn sử dụng.

**Giải pháp**: Tìm kiếm trên Google với từ khóa _"{tên tỉnh} sáp nhập {danh sách tên phường cũ}"_, dựa vào thông tin trên các trang uy tính để bổ sung danh sách alias keywords.

**Triển khai**: [data/alias_keywords/legacy/alias_ward.csv](data/alias_keywords/legacy/alias_ward.csv)

### Một số district bị chia

Đây là những case bị chia:
1. Chia thành 2 district mới, ví dụ: Thành phố Huế (cũ) chia thành Thuận Hóa và Phú Xuân.
2. Chia vào 2 district khác, ví dụ: Huyện Lộc Hà thuộc Hà Tĩnh chia xã Hộ Độ cho Thành phố Hà Tĩnh, còn lại chia cho Huyện Thạch Hà.
3. Cắt vài ward cho district khác, ví dụ: Huyện Cẩm Xuyên thuộc Hà Tĩnh chia Xã Cẩm Vịnh và Xã Cẩm Bình cho Thành phố Hà Tĩnh.

**Giải pháp**:
- Dựa vào ward để chọn district.
- Nếu không có ward, chọn district mặc định. District mặc định sẽ là:
    - District có nhiều ward nhất.
    - District gốc bị cắt.

**Triển khai**:
[data/alias_keywords/legacy/divided_district.csv](data/alias_keywords/legacy/divided_district.csv)

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
- Triển khai dùng ward để chọn district như [Một số district bị chia](#một-số-district-bị-chia).



## PARSE FROM-2025 ADMIN UNITS


## CONVERT 2025

Vấn đề lớn của việc chuyển đổi chính là các ward cũ bị chia thành nhiều ward mới.

**Giải pháp**:

**Bước 1**: Thu thập data location (latitude, longitude) và polygon.
- Đối với 3321 ward mới thì đã có sẵn location và diện tích km2 ([sapnhap.bando.com.vn](https://sapnhap.bando.com.vn) ), có thể suy ra polygon.
- Đối với 10040 ward cũ thì thu thập location từ [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview).

**Bước 2**: So sánh location của ward với polygon và location của ward mới.
- Nếu có duy nhất một ward mới có polygon chứa location của ward cũ &rarr; Chọn nó làm ward mới mặc định.
- Các trường hợp còn lại, chọn ward mới có location gần với location của ward cũ nhất.

Đối với package [vietnamadminunits](vietnamadminunits) thì đặc biệt hơn một chút. Nếu có địa chỉ chi tiết (số nhà và tên đường) thì sẽ dùng [geopy](https://pypi.org/project/geopy/) để lấy location online, rồi tiếp tục làm như **Bước 2**.