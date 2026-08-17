"""
Đọc ghi bảng kê, EXIF, RAW và các tiện ích chung.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from PIL import ExifTags, Image

from .config import IMG_EXTS, RAW_EXTS

EXIF_TAGS = {v: k for k, v in ExifTags.TAGS.items()}


# ---------------------------------------------------------------------------
# Đọc / ghi ảnh an toàn với đường dẫn Unicode
# ---------------------------------------------------------------------------
#
# BẮT BUỘC dùng hai hàm này thay cho cv2.imread / cv2.imwrite.
#
# Lý do: trên Windows, cv2.imread dùng fopen theo bảng mã ANSI của hệ thống,
# nên mọi đường dẫn có dấu tiếng Việt đều đọc thất bại và trả về None:
#
#     imread_('Chanh d├óy t├¡m RP9\1_xanh\IMG_1282.JPG'):
#     can't open/read file: check file path/integrity
#
# Điều nguy hiểm là cv2.imread KHÔNG ném lỗi, chỉ trả về None. Nếu vòng lặp
# xử lý bỏ qua các ảnh None mà không đếm, toàn bộ ảnh trong thư mục có dấu
# sẽ biến mất âm thầm và bạn chỉ phát hiện ở cuối pipeline khi thấy tập
# kiểm tra còn vài ảnh.
#
# np.fromfile đọc theo byte nên không phụ thuộc bảng mã, cv2.imdecode giải
# mã từ bộ nhớ. Cách này chạy đúng trên mọi hệ điều hành.

def imread_unicode(path, flags=cv2.IMREAD_COLOR):
    """Đọc ảnh, hỗ trợ đường dẫn có dấu tiếng Việt trên Windows."""
    try:
        buf = np.fromfile(str(path), dtype=np.uint8)
        if buf.size == 0:
            return None
        return cv2.imdecode(buf, flags)
    except Exception:
        return None


def imwrite_unicode(path, img, params=None) -> bool:
    """Ghi ảnh, hỗ trợ đường dẫn có dấu tiếng Việt trên Windows."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        ok, buf = cv2.imencode(path.suffix or ".jpg", img, params or [])
        if not ok:
            return False
        buf.tofile(str(path))
        return True
    except Exception:
        return False


def unique_stem(path) -> str:
    """
    Tên file duy nhất, ổn định, suy từ đường dẫn đầy đủ.

    Máy ảnh đánh số lại từ đầu sau mỗi lần định dạng thẻ nhớ, và mỗi máy có
    dải số riêng, nên IMG_1689.JPG xuất hiện ở nhiều nguồn là chuyện bình
    thường. Nếu giữ nguyên tên khi ghi ảnh ra một thư mục phẳng theo lớp,
    ảnh sau sẽ đè ảnh trước mà không có thông báo nào — số ảnh trên đĩa ít
    hơn số ảnh đã xử lý, và sổ kế toán vẫn báo đủ.

    Hàm này gắn thêm sáu ký tự băm của đường dẫn gốc. Băm ổn định giữa các
    lần chạy nên chạy lại không sinh ra file mới.
    """
    p = str(path)
    h = hashlib.md5(p.encode("utf-8")).hexdigest()[:6]
    return f"{Path(p).stem}_{h}"


def count_files(root) -> int:
    """Đếm file thật trên đĩa. Dùng để đối chiếu với số ảnh đã xử lý."""
    root = Path(root)
    return sum(1 for p in root.rglob("*") if p.is_file()) if root.exists() else 0


def check_ascii_paths(paths, limit: int = 5) -> list:
    """
    Cảnh báo sớm về đường dẫn có ký tự ngoài ASCII.

    Không phải lỗi, vì hai hàm trên đã xử lý được, nhưng một số thư viện
    bên thứ ba (kể cả ultralytics ở vài phiên bản) vẫn vấp. Biết trước
    thì đỡ mất thời gian dò.
    """
    bad = [str(p) for p in paths if not str(p).isascii()]
    if bad:
        print(f"\nGHI CHÚ: {len(bad)}/{len(list(paths))} đường dẫn có dấu tiếng Việt.")
        for b in bad[:limit]:
            print(f"  {b}")
        print("  Pipeline này đọc ghi được, nhưng nếu ultralytics báo lỗi ảnh")
        print("  thì hãy đổi tên thư mục sang không dấu.\n")
    return bad

# Cột chuẩn của bảng kê. Ba cột đầu là bắt buộc cho mọi bước sau.
MANIFEST_COLUMNS = [
    "image_path", "fruit_id", "source_id",
    "label", "label_idx", "tinh_trang",
    "session_id", "capture_time", "camera_model", "lens",
    "iso", "exposure_time", "f_number", "white_balance",
    "width", "height", "raw_path", "old_split",
]


def iter_images(root, include_raw: bool = False):
    root = Path(root)
    exts = IMG_EXTS | (RAW_EXTS if include_raw else set())
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix.lower() in exts:
            yield p


def chan_doan_thu_muc(root, msg: str = "") -> str:
    """
    Sinh thông báo chẩn đoán khi không tìm thấy ảnh.

    Câu "không tìm thấy ảnh nào" tự nó không giúp được gì. Người dùng cần
    biết thư mục có tồn tại không, bên trong có gì, và ảnh của họ đang nằm
    ở đâu để trỏ đúng đường dẫn.
    """
    root = Path(root)
    d = [msg] if msg else []
    d.append(f"Không tìm thấy ảnh nào trong: {root.resolve()}")
    d.append("")

    if not root.exists():
        d.append("Thư mục này KHÔNG TỒN TẠI.")
        cha = root.parent
        if cha.exists():
            con = sorted(p.name for p in cha.iterdir() if p.is_dir())[:15]
            d.append(f"Thư mục cha {cha.resolve()} đang có: "
                     + (", ".join(con) if con else "(rỗng)"))
    else:
        muc = sorted(root.iterdir())
        if not muc:
            d.append("Thư mục TỒN TẠI nhưng RỖNG.")
        else:
            thu_muc = [p.name for p in muc if p.is_dir()][:15]
            duoi = sorted({p.suffix.lower() for p in root.rglob("*")
                           if p.is_file() and p.suffix})
            d.append(f"Thư mục con: " + (", ".join(thu_muc) if thu_muc else "(không có)"))
            d.append(f"Các đuôi file tìm thấy: "
                     + (", ".join(duoi[:20]) if duoi else "(không có file nào)"))
            if duoi and not (set(duoi) & (IMG_EXTS | RAW_EXTS)):
                d.append("")
                d.append("Có file nhưng không đuôi nào là ảnh mà script nhận.")
                d.append(f"Script nhận: {', '.join(sorted(IMG_EXTS))}")

    d += [
        "",
        "Cần làm:",
        "  1. Chép ảnh vào thư mục data/raw/ của dự án, ví dụ:",
        r'     Copy-Item -Recurse "D:\qua_chanh\Chanh day tim RP9" data\raw',
        "  2. Hoặc trỏ thẳng --data vào nơi ảnh đang nằm:",
        r'     python scripts\01_build_manifest.py --data "D:\qua_chanh\..." '
        r'--out data\manifest.csv',
        "",
        "Trên PowerShell, đường dẫn có dấu cách phải đặt trong dấu nháy kép.",
    ]
    return "\n".join(d)


# File nào do bước nào sinh ra. Dùng để chỉ đúng lệnh cần chạy khi thiếu file,
# thay vì ném ra một vệt traceback của pandas.
NGUON_FILE = [
    ("fruit_ids.csv",
     "python scripts/01b_tag_sheets.py --data <thư mục ảnh> --out data/tags"),
    ("manifest.csv",
     "python scripts/01_build_manifest.py --data <thư mục ảnh> --out data/manifest.csv"),
    ("_manifest.csv",
     "python scripts/02_preprocess.py --manifest data/manifest.csv "
     "--out data/proc_wb --whitebalance patches"),
    ("_ledger.csv",
     "python scripts/02_preprocess.py --manifest data/manifest.csv --out data/proc_wb"),
    ("predictions.csv",
     "python scripts/04_color_baseline.py ...  hoặc  scripts/05_train_yolo.py ..."),
    ("illum.csv",
     "python scripts/07_illuminant.py --mode extract --manifest data/manifest.csv "
     "--out outputs/illum.csv"),
    ("metrics.json",
     "python scripts/06_evaluate.py --pred <predictions.csv> --out <thư mục>"),
]


def _tim_file_cung_ten(ten: str, goc: Path, gioi_han: int = 5):
    """Tìm file cùng tên ở nơi khác trong dự án — thường là do dùng --out khác."""
    try:
        return [p for p in list(goc.rglob(ten))[:gioi_han] if p.is_file()]
    except Exception:
        return []


def doc_bat_buoc(path, mo_ta: str = ""):
    """
    Kiểm tra file đầu vào tồn tại, nếu không thì dừng với hướng dẫn cụ thể.

    Để pandas tự ném FileNotFoundError sẽ cho ra hai chục dòng traceback mà
    dòng hữu ích duy nhất nằm ở cuối, và vẫn không nói được bước nào sinh ra
    file đó. Người dùng buộc phải đi hỏi lại.
    """
    p = Path(path)
    if p.exists():
        return p

    d = [f"Không có file: {p.resolve()}"]
    if mo_ta:
        d.append(mo_ta)

    lenh = next((c for hau_to, c in NGUON_FILE if p.name.endswith(hau_to)), "")
    if lenh:
        d += ["", "File này do bước trước sinh ra. Chạy lệnh sau trước:",
              f"    {lenh}"]

    # Có thể người dùng đã chạy nhưng ghi ra chỗ khác
    goc = Path.cwd()
    tim = [q for q in _tim_file_cung_ten(p.name, goc) if q.resolve() != p.resolve()]
    if tim:
        d += ["", "Tìm thấy file cùng tên ở nơi khác, có thể bạn muốn dùng:"]
        d += [f"    {q}" for q in tim]

    cha = p.parent
    if not cha.exists():
        d += ["", f"Thư mục {cha} cũng chưa tồn tại."]
    else:
        co = sorted(q.name for q in cha.iterdir())[:12]
        d += ["", f"Thư mục {cha} đang có: " + (", ".join(co) if co else "(rỗng)")]

    raise SystemExit("\n".join(d))


def read_str_csv(path) -> pd.DataFrame:
    """
    Đọc CSV giữ mọi giá trị dạng chuỗi.

    Bắt buộc: nếu để pandas tự suy kiểu, cột fruit_id còn trống sẽ thành
    float64 và mọi mã dạng 'Q072' ghi vào sau đó sẽ báo lỗi kiểu dữ liệu.
    """
    return pd.read_csv(doc_bat_buoc(path), dtype=str,
                       keep_default_na=False, na_filter=False)


def write_csv(df: pd.DataFrame, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"[đã ghi] {path}  ({len(df)} dòng)")


def save_json(obj, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    def default(o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, Path):
            return str(o)
        return str(o)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=default)
    print(f"[đã ghi] {path}")


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# EXIF
# ---------------------------------------------------------------------------

def read_exif(path: Path) -> dict:
    out = dict.fromkeys(
        ["capture_time", "camera_model", "lens", "iso", "exposure_time",
         "f_number", "white_balance", "width", "height"], "")
    try:
        with Image.open(path) as im:
            out["width"], out["height"] = im.size
            ex = im.getexif()
            if not ex:
                return out
            make = ex.get(EXIF_TAGS.get("Make"), "") or ""
            model = ex.get(EXIF_TAGS.get("Model"), "") or ""
            out["camera_model"] = f"{make} {model}".strip()
            try:
                ifd = ex.get_ifd(0x8769)
            except Exception:
                ifd = {}

            def g(name, src=ifd):
                t = EXIF_TAGS.get(name)
                return src.get(t) if t else None

            out["capture_time"] = str(g("DateTimeOriginal")
                                      or ex.get(EXIF_TAGS.get("DateTime")) or "")
            out["lens"] = str(g("LensModel") or "")
            out["iso"] = str(g("ISOSpeedRatings") or "")
            out["exposure_time"] = str(g("ExposureTime") or "")
            out["f_number"] = str(g("FNumber") or "")
            wb = g("WhiteBalance")
            out["white_balance"] = {0: "auto", 1: "manual"}.get(wb, str(wb or ""))
    except Exception:
        pass
    return out


def find_raw_sibling(p: Path) -> str:
    """Tìm file RAW cùng tên. RAW cho phép đo màu tuyến tính, chính xác hơn JPEG."""
    for ext in RAW_EXTS:
        for cand in (p.with_suffix(ext), p.with_suffix(ext.upper())):
            if cand.exists():
                return str(cand)
    return ""


def read_raw_linear(path, half_size: bool = True):
    """
    Giải mã RAW ở không gian tuyến tính, không áp cân bằng trắng của máy.

    Dùng khi cần đo màu chính xác: JPEG đã qua cân bằng trắng và ánh xạ tông
    nên giá trị pixel không tỷ lệ tuyến tính với lượng ánh sáng tới.
    """
    import rawpy
    with rawpy.imread(str(path)) as raw:
        rgb = raw.postprocess(
            gamma=(1, 1), no_auto_bright=True, output_bps=16,
            use_camera_wb=False, use_auto_wb=False,
            user_wb=[1.0, 1.0, 1.0, 1.0], half_size=half_size,
        )
    bgr16 = rgb[:, :, ::-1]
    return (bgr16 / 257.0).astype(np.uint8), bgr16


# ---------------------------------------------------------------------------
# Đoán mã từ tên file
# ---------------------------------------------------------------------------

_FRUIT_PATTERNS = [
    re.compile(r"(?:^|[_\-])(?:qua|fruit|q)[_\-]?(\d+)", re.I),
    re.compile(r"(?:^|[_\-])(?:id)[_\-]?(\d+)", re.I),
]
_SOURCE_PATTERNS = [re.compile(r"(?:^|[_\-])(?:nguon|source|n)[_\-]?(\d+)", re.I)]


def guess_fruit_id(stem: str) -> str:
    for pat in _FRUIT_PATTERNS:
        m = pat.search(stem)
        if m:
            return f"Q{int(m.group(1)):04d}"
    return ""


def guess_source_id(stem: str) -> str:
    for pat in _SOURCE_PATTERNS:
        m = pat.search(stem)
        if m:
            return f"N{int(m.group(1))}"
    return ""


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    for c in MANIFEST_COLUMNS:
        if c not in df.columns:
            df[c] = ""
    return df
