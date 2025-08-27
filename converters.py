
import os
import re
import subprocess
from pathlib import Path

# Конвертация DOC/DOCX в PDF с помощью LibreOffice (Linux)
# Возвращает путь к созданному PDF. Исключение — если не удалось конвертировать.
def convert_to_pdf(input_path: str) -> str:
    input_path = str(input_path)
    src = Path(input_path)
    if not src.exists():
        raise Exception(f"Файл не найден: {input_path}")

    ext = src.suffix.lower()
    if ext == ".pdf":
        return str(src)
    if ext not in (".doc", ".docx"):
        raise Exception("Поддерживаются только файлы DOC/DOCX/PDF")

    outdir = str(src.parent)
    args = ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", outdir, str(src)]
    try:
        proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    except FileNotFoundError:
        raise Exception("Не найден исполняемый файл 'libreoffice'. Установите LibreOffice в системе Linux.")

    stdout = (proc.stdout or b"").decode(errors="ignore")
    stderr = (proc.stderr or b"").decode(errors="ignore")
    if proc.returncode != 0:
        raise Exception(f"Ошибка LibreOffice (код {proc.returncode}). Подробнее: {stderr or stdout}")

    # Ожидаемое имя выходного файла
    pdf_path = Path(outdir) / (src.stem + ".pdf")
    if not pdf_path.exists():
        # Попробуем вытащить путь из stdout формата: "-> /path/file.pdf using filter"
        m = re.search(r"->\s*(.*?\.pdf)", stdout)
        if m:
            candidate = Path(m.group(1).strip())
            if candidate.exists():
                pdf_path = candidate

    if not pdf_path.exists():
        raise Exception("Не удалось создать PDF-файл.")

    return str(pdf_path)

# Заглушка (если где-то вызывалась очистка временных файлов)
def cleanup_temp_files():
    try:
        pass
    except Exception:
        pass
