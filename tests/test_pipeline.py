"""
Kiểm thử nhanh. Chạy: pytest tests/ -v

Không cần dữ liệu thật — mọi thứ dựng bằng ảnh tổng hợp. Mục đích là bắt lỗi
hồi quy khi ai đó sửa code, nhất là các lỗi âm thầm như đổi thứ tự kênh màu
hay đảo chiều ma trận chi phí.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chanhday.cards import (angular_error, apply_von_kries,
                            illuminant_from_patches, illuminant_gray_world)
from chanhday.config import (CLASS_NAMES, N_CLASSES, build_cost_matrix)
from chanhday.features import extract
from chanhday.metrics import (cost_optimal_prediction, early_late_rates,
                              expected_cost, off_by_more_than_one,
                              quadratic_weighted_kappa)
from chanhday.segmentation import crop_to_mask, segment_fruit


# --------------------------------------------------------------------------
# Ma trận chi phí
# --------------------------------------------------------------------------

def test_ma_tran_chi_phi_duong_cheo_bang_khong():
    c = build_cost_matrix()
    assert np.allclose(np.diag(c), 0)


def test_hai_muon_dat_hon_hai_som():
    """Trọng số phải phản ánh đúng mục 4.6: hái muộn thiệt hại hơn hái sớm."""
    c = build_cost_matrix(late=3.0, early=1.0)
    # thật bậc 3 (idx 2), báo bậc 2 (idx 1) -> chờ thêm -> hái muộn
    hai_muon = c[2, 1]
    # thật bậc 3, báo bậc 4 (idx 3) -> hái ngay -> hái sớm
    hai_som = c[2, 3]
    assert hai_muon > hai_som
    assert hai_muon == pytest.approx(3.0)
    assert hai_som == pytest.approx(1.0)


def test_chi_phi_tang_theo_do_lech():
    c = build_cost_matrix()
    assert c[4, 0] > c[4, 2] > c[4, 3] > 0


def test_du_doan_toi_uu_theo_chi_phi_lech_ve_bac_cao():
    """
    Khi mô hình lưỡng lự giữa hai bậc kề nhau, quyết định tối ưu theo chi phí
    phải nghiêng về bậc CAO hơn, vì báo thấp gây hái muộn vốn đắt hơn.
    """
    proba = np.zeros((1, N_CLASSES))
    proba[0, 1] = 0.5
    proba[0, 2] = 0.5
    assert cost_optimal_prediction(proba)[0] == 2


# --------------------------------------------------------------------------
# Chỉ số
# --------------------------------------------------------------------------

def test_kappa_hoan_hao_bang_mot():
    y = np.array([0, 1, 2, 3, 4, 2, 1])
    assert quadratic_weighted_kappa(y, y) == pytest.approx(1.0)


def test_kappa_phat_lech_ba_bac_nang_hon_lech_mot_bac():
    y = np.array([0, 1, 2, 3, 4] * 4)
    gan = np.clip(y + 1, 0, 4)
    xa = np.clip(y + 3, 0, 4)
    assert quadratic_weighted_kappa(y, gan) > quadratic_weighted_kappa(y, xa)


def test_ty_le_hai_som_muon_cong_lai_bang_mot():
    y = np.array([0, 1, 2, 3, 4])
    p = np.array([1, 1, 0, 4, 4])
    r = early_late_rates(y, p)
    tong = r["ty_le_dung_bac"] + r["ty_le_hai_som"] + r["ty_le_hai_muon"]
    assert tong == pytest.approx(1.0)


def test_lech_qua_mot_bac():
    y = np.array([0, 0, 0, 0])
    p = np.array([0, 1, 2, 3])
    assert off_by_more_than_one(y, p) == pytest.approx(0.5)


def test_chi_phi_bang_khong_khi_du_doan_dung_het():
    y = np.array([0, 1, 2, 3, 4])
    assert expected_cost(y, y) == pytest.approx(0.0)


# --------------------------------------------------------------------------
# Nguồn sáng
# --------------------------------------------------------------------------

def test_o_xam_trung_tinh_cho_nguon_sang_trung_tinh():
    patches = np.array([[50.0, 50, 50], [100, 100, 100], [200, 200, 200]])
    ill = illuminant_from_patches(patches)
    assert angular_error(ill) == pytest.approx(0.0, abs=0.01)


def test_hieu_chinh_von_kries_khu_duoc_am_mau():
    """Đây là kiểm thử quan trọng nhất: hiệu chỉnh phải thực sự khử ám màu."""
    patches = np.array([[90.0, 100, 120], [180, 200, 240]])
    ill = illuminant_from_patches(patches)
    truoc = angular_error(ill)
    assert truoc > 3.0

    img = np.zeros((20, 20, 3), np.uint8)
    img[:, :] = [90, 100, 120]
    sau = apply_von_kries(img, ill)
    ill_sau = illuminant_from_patches(sau.reshape(-1, 3)[:5].astype(float))
    assert angular_error(ill_sau) < 1.0


def test_gray_world_tren_anh_trung_tinh():
    img = np.full((32, 32, 3), 128, np.uint8)
    assert angular_error(illuminant_gray_world(img, 1)) == pytest.approx(0.0, abs=0.01)


def test_sai_so_goc_doi_xung():
    a, b = np.array([1.0, 0.9, 0.8]), np.array([0.8, 0.9, 1.0])
    assert angular_error(a, b) == pytest.approx(angular_error(b, a))


# --------------------------------------------------------------------------
# Tách nền
# --------------------------------------------------------------------------

def _anh_gia_lap(mau=(60, 140, 90), r=40):
    img = np.zeros((300, 400, 3), np.uint8)
    cv_center = (200, 150)
    yy, xx = np.mgrid[:300, :400]
    m = (xx - cv_center[0]) ** 2 + (yy - cv_center[1]) ** 2 <= r ** 2
    img[m] = mau
    return img, m


def test_tach_duoc_qua_tron_tren_nen_den():
    img, m_that = _anh_gia_lap()
    mask = segment_fruit(img)
    assert mask is not None
    iou = ((mask > 0) & m_that).sum() / ((mask > 0) | m_that).sum()
    assert iou > 0.85


def test_cat_theo_hop_bao_nho_hon_anh_goc():
    img, _ = _anh_gia_lap()
    mask = segment_fruit(img)
    crop = crop_to_mask(img, mask)
    assert crop is not None
    assert crop.shape[0] < img.shape[0]
    assert crop.shape[1] < img.shape[1]


def test_loai_bo_vung_bi_exclude():
    """Thẻ nằm trong vùng exclude thì không được chọn làm quả."""
    img = np.zeros((300, 400, 3), np.uint8)
    img[240:290, 300:390] = 220          # "thẻ" sáng, diện tích lớn
    yy, xx = np.mgrid[:300, :400]
    m = (xx - 120) ** 2 + (yy - 100) ** 2 <= 35 ** 2
    img[m] = (60, 140, 90)               # "quả" nhỏ hơn

    exclude = np.zeros((300, 400), np.uint8)
    exclude[230:300, 290:400] = 1
    mask = segment_fruit(img, exclude)
    assert mask is not None
    assert mask[260, 340] == 0           # không chọn thẻ
    assert mask[100, 120] > 0            # chọn đúng quả


# --------------------------------------------------------------------------
# Đặc trưng
# --------------------------------------------------------------------------

def test_dac_trung_co_do_dai_dung():
    from chanhday.features import FEATURE_NAMES
    img, _ = _anh_gia_lap()
    assert len(extract(img)) == len(FEATURE_NAMES)


def test_qua_do_co_ty_le_chuyen_mau_cao_hon_qua_xanh():
    """Kiểm tra chiều của đặc trưng frac_vo_chuyen_mau — dễ sai dấu."""
    from chanhday.features import FEATURE_NAMES
    i = FEATURE_NAMES.index("frac_vo_chuyen_mau")
    xanh, _ = _anh_gia_lap(mau=(60, 160, 60))    # BGR: xanh lục
    do, _ = _anh_gia_lap(mau=(40, 60, 200))      # BGR: đỏ
    assert extract(do)[i] > extract(xanh)[i]


def test_dac_trung_khong_co_nan():
    img, _ = _anh_gia_lap()
    assert np.isfinite(extract(img)).all()


# --------------------------------------------------------------------------
# Cấu hình
# --------------------------------------------------------------------------

def test_ten_lop_khop_so_luong():
    assert len(CLASS_NAMES) == N_CLASSES == 5


def test_ten_lop_theo_dung_thu_tu_do_chin():
    assert CLASS_NAMES[0].startswith("1_")
    assert CLASS_NAMES[-1].startswith("5_")


# --------------------------------------------------------------------------
# Hồi quy: các lỗi đã gặp thật khi chạy trên Windows
# --------------------------------------------------------------------------

def test_doc_ghi_anh_duong_dan_co_dau_tieng_viet(tmp_path):
    """
    cv2.imread trả None với đường dẫn có dấu trên Windows, và trả None chứ
    không ném lỗi, nên ảnh biến mất âm thầm. Đây là nguyên nhân khiến một bộ
    200 ảnh chỉ còn 83 sau bước tiền xử lý.
    """
    import cv2
    from chanhday.io_utils import imread_unicode, imwrite_unicode

    d = tmp_path / "Chanh dây tím RP9" / "1_xanh"
    d.mkdir(parents=True)
    f = d / "ảnh_thử_nghiệm.jpg"

    img = np.zeros((40, 40, 3), np.uint8)
    img[10:30, 10:30] = (60, 140, 90)

    assert imwrite_unicode(f, img), "ghi ảnh vào đường dẫn có dấu thất bại"
    assert f.exists()

    back = imread_unicode(f)
    assert back is not None, "đọc lại ảnh ở đường dẫn có dấu thất bại"
    assert back.shape == img.shape


def test_thu_muc_hong_khong_thanh_bac_chin_thu_sau():
    """
    Nhét '6_hong' thành lớp thứ sáu sẽ dịch chỉ số của các bậc chín và làm
    hỏng toàn bộ Kappa, sai số theo bậc và chi phí kỳ vọng mà không báo lỗi.
    """
    from chanhday.config import CONDITION_DIR_ALIASES
    assert "6_hong" in CONDITION_DIR_ALIASES
    assert not any(c in CONDITION_DIR_ALIASES for c in CLASS_NAMES)
    assert len(CLASS_NAMES) == 5


def test_suy_nhan_tu_thu_muc(tmp_path):
    import importlib.util as ilu
    spec = ilu.spec_from_file_location(
        "s01", Path(__file__).resolve().parents[1] / "scripts" / "01_build_manifest.py")
    m = ilu.module_from_spec(spec)
    spec.loader.exec_module(m)

    root = tmp_path
    for sub in ("1_xanh", "6_hong", "3_chuyen_mot_phan"):
        (root / sub).mkdir(parents=True)

    lab, cond = m.infer_label(root / "1_xanh" / "a.jpg", root)
    assert (lab, cond) == ("1_xanh", "")

    lab, cond = m.infer_label(root / "6_hong" / "b.jpg", root)
    assert cond == "hong" and lab == "", "thư mục hỏng không được thành bậc chín"

    lab, cond = m.infer_label(root / "3_chuyen_mot_phan" / "c.jpg", root)
    assert lab == "3_chuyen_mot_phan"


def test_cost_matrix_khong_doi_khi_them_lop_hong():
    """Ma trận chi phí phải luôn 5x5, không nở ra theo trục tình trạng."""
    assert build_cost_matrix().shape == (5, 5)


# --------------------------------------------------------------------------
# Hồi quy: dò nhãn mã quả
# --------------------------------------------------------------------------

def _anh_co_the(tag_o_dau=(0.88, 0.745), seed=0):
    """
    Ảnh giả lập theo đúng bố cục thật: nền tối, dải bốn ô xám mỗi ô kèm một
    mã QR phía trên, và một mảnh giấy trắng phẳng ghi mã quả.

    Mã QR được sinh bằng nhiễu nhị phân để có mật độ biên cao đúng như mã QR
    thật — đây chính là dấu hiệu dùng để phân biệt với mảnh giấy.
    """
    rng = np.random.default_rng(seed)
    H, W = 800, 1200
    img = np.full((H, W, 3), 16, np.uint8)

    for i, v in enumerate((238, 195, 135, 75)):
        x = 700 + i * 60
        img[600:680, x:x + 45] = v                     # ô xám
        qr = rng.integers(0, 2, (20, 20), dtype=np.uint8) * 255
        img[556:596, x:x + 40] = np.kron(qr, np.ones((2, 2), np.uint8))[:40, :40][..., None]

    tx, ty = int(tag_o_dau[0] * W), int(tag_o_dau[1] * H)
    img[ty:ty + 90, tx:tx + 120] = 244                 # mảnh giấy, phẳng
    img[ty + 20:ty + 24, tx + 15:tx + 105] = 90        # hai nét kẻ
    img[ty + 66:ty + 70, tx + 15:tx + 105] = 90
    img[ty + 40:ty + 55, tx + 35:tx + 80] = 70         # chữ số
    return img


def test_do_duoc_nhan_ma_qua_khong_nham_dai_o_xam():
    """
    Dải ô xám luôn kèm mã QR nên mật độ biên cao gấp nhiều lần chữ viết tay.
    Nhầm hai vùng này khiến trang đọc mã hiện ra mã QR thay vì mã quả.
    """
    from chanhday.cards import detect_tag
    img = _anh_co_the()
    box = detect_tag(img)
    assert box is not None, "không dò ra mảnh giấy"
    x, y, w, h = box
    assert x > 950, f"dò nhầm sang dải ô xám (x={x})"


def test_do_duoc_nhan_khi_bo_cuc_doi_hoan_toan():
    """
    Đây là tình huống đã gặp thật: từ một nhóm ảnh nào đó, khung hình đổi nên
    toạ độ cố định cắt vào vỏ quả, và trang đọc mã trở nên vô dụng.
    """
    from chanhday.cards import crop_tag, detect_tag
    img = _anh_co_the(tag_o_dau=(0.05, 0.10))   # nhãn chuyển sang góc trái trên
    box = detect_tag(img)
    assert box is not None, "không dò ra nhãn khi bố cục đổi"
    assert box[0] < 300, "vẫn bám vào toạ độ cũ"

    _, auto = crop_tag(img)
    assert auto is True


def test_bao_hieu_khi_khong_do_ra_nhan():
    """Không dò ra thì phải báo, chứ không âm thầm trả về vùng cố định."""
    from chanhday.cards import crop_tag
    toi = np.full((800, 1200, 3), 12, np.uint8)
    crop, auto = crop_tag(toi)
    assert auto is False, "phải báo là không dò được để người điền biết mà bỏ qua"
    assert crop.size > 0


def test_nguong_doi_qua_tach_duoc_hai_nhom():
    """
    Ngưỡng tự tính phải tách được nhóm 'cùng quả' khỏi nhóm 'đổi quả'.
    Số liệu lấy từ bộ ảnh Canon thật.
    """
    import importlib.util as ilu
    spec = ilu.spec_from_file_location(
        "s01b", Path(__file__).resolve().parents[1] / "scripts" / "01b_tag_sheets.py")
    m = ilu.module_from_spec(spec)
    spec.loader.exec_module(m)

    cung_qua = [0.020, 0.020, 0.028, 0.034, 0.018, 0.029, 0.019, 0.038, 0.026, 0.012]
    doi_qua = [0.248, 0.177, 0.088, 0.152]
    ng = m.nguong_doi_qua(cung_qua + doi_qua)

    assert max(cung_qua) < ng < min(doi_qua), (
        f"ngưỡng {ng:.3f} không tách được hai nhóm")


# --------------------------------------------------------------------------
# Hồi quy: môi trường Windows
# --------------------------------------------------------------------------

def test_requirements_chi_dung_ascii():
    """
    pip trên Windows đọc requirements.txt bằng bảng mã hệ thống (cp1252 với
    Windows tiếng Việt), không phải UTF-8. Một chú thích có dấu là đủ làm
    `pip install -r requirements.txt` chết ngay từ bước cài đặt:
        UnicodeDecodeError: 'charmap' codec can't decode byte 0x8d
    """
    goc = Path(__file__).resolve().parents[1]
    for ten in ("requirements.txt", "requirements-minimal.txt"):
        f = goc / ten
        if not f.exists():
            continue
        data = f.read_bytes()
        xau = [(i, hex(b)) for i, b in enumerate(data) if b > 127]
        assert not xau, f"{ten} có byte ngoài ASCII tại {xau[:3]}"


def test_ep_dau_ra_utf8():
    """
    Cửa sổ lệnh Windows mặc định không phải UTF-8, nên mọi print có dấu
    tiếng Việt sẽ ném UnicodeEncodeError và làm script chết giữa chừng.
    Package phải tự ép lại khi được nạp.
    """
    import io
    import sys

    import chanhday

    luong = io.TextIOWrapper(io.BytesIO(), encoding="cp1252", errors="strict")
    cu = sys.stdout
    try:
        sys.stdout = luong
        with pytest.raises(UnicodeEncodeError):
            print("Không tìm thấy ảnh nào")
            luong.flush()
    finally:
        sys.stdout = cu

    luong2 = io.TextIOWrapper(io.BytesIO(), encoding="cp1252", errors="strict")
    cu = sys.stdout
    try:
        sys.stdout = luong2
        chanhday._ep_utf8()
        print("Không tìm thấy ảnh nào")   # không được ném lỗi
        luong2.flush()
    finally:
        sys.stdout = cu


def test_chan_doan_thu_muc_noi_ro_van_de(tmp_path):
    """Thông báo lỗi phải nói rõ vấn đề và việc cần làm, không chỉ 'không thấy ảnh'."""
    from chanhday.io_utils import chan_doan_thu_muc

    msg = chan_doan_thu_muc(tmp_path / "khong_ton_tai")
    assert "KHÔNG TỒN TẠI" in msg
    assert "--data" in msg

    (tmp_path / "co_file").mkdir()
    (tmp_path / "co_file" / "ghi_chu.txt").write_text("x")
    msg = chan_doan_thu_muc(tmp_path / "co_file")
    assert ".txt" in msg
    assert "Script nhận" in msg

    (tmp_path / "rong").mkdir()
    assert "RỖNG" in chan_doan_thu_muc(tmp_path / "rong")


def test_bao_loi_ro_khi_thieu_file_dau_vao(tmp_path, monkeypatch):
    """
    Thiếu file đầu vào phải cho thông báo chỉ đúng lệnh cần chạy, chứ không
    ném ra hai chục dòng traceback của pandas mà dòng hữu ích nằm ở cuối.
    """
    from chanhday.io_utils import doc_bat_buoc

    monkeypatch.chdir(tmp_path)
    (tmp_path / "data" / "tags").mkdir(parents=True)

    with pytest.raises(SystemExit) as e:
        doc_bat_buoc(tmp_path / "data" / "tags" / "fruit_ids.csv")
    msg = str(e.value)
    assert "01b_tag_sheets.py" in msg, "phải chỉ ra lệnh sinh file này"
    assert "Không có file" in msg


def test_goi_y_file_cung_ten_o_noi_khac(tmp_path, monkeypatch):
    """Người dùng hay ghi ra --out khác rồi đi tìm ở đường dẫn mặc định."""
    from chanhday.io_utils import doc_bat_buoc

    monkeypatch.chdir(tmp_path)
    (tmp_path / "cho_khac").mkdir()
    (tmp_path / "cho_khac" / "manifest.csv").write_text("a\n1\n", encoding="utf-8")

    with pytest.raises(SystemExit) as e:
        doc_bat_buoc(tmp_path / "data" / "manifest.csv")
    assert "cho_khac" in str(e.value), "phải gợi ý file cùng tên đã tìm thấy"


def test_phat_hien_lan_chup_chi_co_raw(tmp_path):
    """
    File RAW không có JPG đi kèm bị iter_images bỏ qua âm thầm. Trên thư mục
    mẫu ngày 14/8/2026, tỷ lệ này là 4/19 lần chụp, tức hơn hai mươi phần trăm.
    """
    from chanhday.io_utils import iter_images

    d = tmp_path / "dot1"
    d.mkdir()
    for ten in ("IMG_1689.JPG", "IMG_1698.JPG"):
        (d / ten).write_bytes(b"x")
    for ten in ("IMG_1689.CR3", "IMG_1685.CR3", "IMG_1686.CR3"):
        (d / ten).write_bytes(b"x")

    thuong = list(iter_images(tmp_path))
    assert len(thuong) == 2, "iter_images mặc định chỉ lấy ảnh thường"

    ca_raw = list(iter_images(tmp_path, include_raw=True))
    assert len(ca_raw) == 5

    stem_anh = {p.stem for p in thuong}
    stem_raw = {p.stem for p in ca_raw if p.suffix.lower() == ".cr3"}
    chi_raw = stem_raw - stem_anh
    assert chi_raw == {"IMG_1685", "IMG_1686"}


def test_include_raw_dua_them_file_raw_don_le(tmp_path, monkeypatch):
    """Chế độ --include-raw phải thêm đúng những lần chụp chỉ có RAW."""
    import importlib.util as ilu

    spec = ilu.spec_from_file_location(
        "s01", Path(__file__).resolve().parents[1] / "scripts" / "01_build_manifest.py")
    m = ilu.module_from_spec(spec)
    spec.loader.exec_module(m)

    d = tmp_path / "1_xanh"
    d.mkdir()
    (d / "A.JPG").write_bytes(b"x")
    (d / "A.CR3").write_bytes(b"x")
    (d / "B.CR3").write_bytes(b"x")

    n = m.bao_cao_raw_don_le(tmp_path)
    assert n == 1, "phải phát hiện đúng 1 lần chụp chỉ có RAW"
