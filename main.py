import os
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