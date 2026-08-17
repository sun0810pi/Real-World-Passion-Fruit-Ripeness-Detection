@echo off
REM Chay toan bo pipeline mot luot tren Windows.
setlocal
set PYTHONPATH=%CD%
set RAW=%1
if "%RAW%"=="" set RAW=data\raw

echo ===== 00: do bo cuc the =====
python scripts\00_calibrate_layout.py --data "%RAW%" || goto :err

echo ===== 01: lap bang ke =====
python scripts\01_build_manifest.py --data "%RAW%" --out data\manifest.csv || goto :err

echo.
echo Neu cot fruit_id chua dien, chay:
echo   python scripts\01b_tag_sheets.py --data "%RAW%" --out data\tags
echo   (dien data\tags\fruit_ids.csv)
echo   python scripts\01b_tag_sheets.py --fill-down data\tags\fruit_ids.csv
echo   python scripts\01b_tag_sheets.py --merge data\tags\fruit_ids.csv --manifest data\manifest.csv
echo.

echo ===== 02: tien xu ly =====
python scripts\02_preprocess.py --manifest data\manifest.csv --out data\proc_wb --whitebalance patches || goto :err
python scripts\02_preprocess.py --manifest data\manifest.csv --out data\proc_nowb --whitebalance none || goto :err

echo ===== 03: kiem toan + chia tap =====
python scripts\03_split.py --manifest data\proc_wb_manifest.csv --mode audit || goto :err
for %%s in (0 1 2) do python scripts\03_split.py --manifest data\proc_wb_manifest.csv --mode fruit --seed %%s || goto :err

echo ===== 04: duong co so mau =====
python scripts\04_color_baseline.py --split-dir data\splits\fruit_seed0 --out outputs\baseline_seed0 || goto :err
python scripts\06_evaluate.py --pred outputs\baseline_seed0\predictions.csv --out outputs\baseline_seed0 || goto :err

echo ===== 05 + 06: hoc sau =====
for %%s in (0 1 2) do (
  python scripts\05_train_yolo.py --data data\splits\fruit_seed%%s --name cungnguon_s%%s --seed %%s || goto :err
  python scripts\06_evaluate.py --pred outputs\runs\cungnguon_s%%s\predictions.csv --out outputs\cungnguon_s%%s || goto :err
)
python scripts\06_evaluate.py --aggregate outputs\cungnguon_s0 outputs\cungnguon_s1 outputs\cungnguon_s2

echo ===== 07 + 08 + 09 =====
python scripts\07_illuminant.py --mode extract --manifest data\manifest.csv --out outputs\illum.csv
python scripts\07_illuminant.py --mode baseline --illum outputs\illum.csv
python scripts\08_condition_head.py --manifest data\proc_wb_manifest.csv
python scripts\09_report_numbers.py

echo.
echo XONG. Ket qua nam trong outputs\
goto :eof

:err
echo.
echo LOI o buoc tren. Xem thong bao va sua truoc khi chay tiep.
exit /b 1
