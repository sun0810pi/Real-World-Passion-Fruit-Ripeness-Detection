"""
Pipeline dự đoán độ chín quả chanh dây (Passiflora edulis Sims).
Công trình dự thi Giải thưởng Sinh viên Nghiên cứu khoa học Euréka 2026.

Nguyên tắc thiết kế xuyên suốt: mọi con số báo cáo phải đến từ một phép
đánh giá không rò rỉ. Chia tập theo nguồn, rồi theo quả — không bao giờ
chia ngẫu nhiên theo ảnh.
"""
import sys

__version__ = "1.3.0"


def _ep_utf8():
    """
    Ép đầu ra chuẩn sang UTF-8.

    Trên Windows, bảng mã mặc định của cửa sổ lệnh là cp1252 hoặc cp437 chứ
    không phải UTF-8. Mọi lệnh print có dấu tiếng Việt sẽ ném UnicodeEncodeError
    và làm script chết giữa chừng, kể cả khi phần xử lý ảnh hoàn toàn bình
    thường. Người dùng khi đó thấy một vệt traceback khó hiểu thay vì kết quả.

    Đặt errors="replace" để trường hợp xấu nhất cũng chỉ mất vài dấu chứ
    không dừng chương trình.
    """
    for luong in (sys.stdout, sys.stderr):
        try:
            if luong is not None and hasattr(luong, "reconfigure"):
                luong.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_ep_utf8()

from .config import (CFG, CLASS_NAMES, CLASS_TO_IDX, N_CLASSES,  # noqa: E402
                     CONDITION_NAMES, build_cost_matrix)

__all__ = ["CFG", "CLASS_NAMES", "CLASS_TO_IDX", "N_CLASSES",
           "CONDITION_NAMES", "build_cost_matrix", "__version__"]
