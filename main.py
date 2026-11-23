import os
import shutil
from pathlib import Path
import pandas as pd


def create_annotation(dataset_root, annotation_csv):
    project_root = Path.cwd()
    rows = []
    for class_dir in sorted(p for p in Path(dataset_root).iterdir() if p.is_dir()):
        for f in sorted(p for p in class_dir.iterdir() if p.is_file()):
            abs_path = f.resolve()
            rows.append({
                "absolute_path": str(abs_path),
                "relate_path": os.path.relpath(abs_path, project_root),
                "output_class": class_dir.name,
            })
    df = pd.DataFrame(rows, columns=["absolute_path", "relate_path", "output_class"])
    df.to_csv(annotation_csv, index=False)
    return df


def copy_with_class_names(dataset_root, output_root, annotation_csv):
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    rows = []
    for class_dir in sorted(p for p in Path(dataset_root).iterdir() if p.is_dir()):
        cls = class_dir.name
        files = sorted(p for p in class_dir.iterdir() if p.is_file())
        for idx, src in enumerate(files):
            dst = output_root / f"{cls}_{idx:04d}.jpg"
            shutil.copy2(src, dst)
            rows.append({
                "absolute_path": str(dst.resolve()),
                "relate_path": os.path.relpath(dst, Path.cwd()),
                "output_class": cls,
            })
    df = pd.DataFrame(rows, columns=["absolute_path", "relate_path", "output_class"])
    df.to_csv(annotation_csv, index=False)
    return df