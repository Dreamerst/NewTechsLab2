import os
import random
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


def copy_with_random_numbers(dataset_root, output_root, annotation_csv, max_num=10000):
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    files = []
    for class_dir in sorted(p for p in Path(dataset_root).iterdir() if p.is_dir()):
        for f in sorted(p for p in class_dir.iterdir() if p.is_file()):
            files.append((class_dir.name, f))

    numbers = random.sample(range(max_num + 1), len(files))
    rows = []
    for (cls, src), num in zip(files, numbers):
        dst = output_root / f"{num:05d}.jpg"
        shutil.copy2(src, dst)
        rows.append({
            "absolute_path": str(dst.resolve()),
            "relate_path": os.path.relpath(dst, Path.cwd()),
            "output_class": cls,
        })
    df = pd.DataFrame(rows, columns=["absolute_path", "relate_path", "output_class"])
    df.to_csv(annotation_csv, index=False)
    return df


def make_next_instance(dataset_root):
    queues: dict[str, list[Path]] = {}

    def next_instance(class_label):
        if class_label not in queues:
            files = [p for p in (Path(dataset_root) / class_label).iterdir() if p.is_file()]
            random.shuffle(files)
            queues[class_label] = files
        if not queues[class_label]:
            return None
        return queues[class_label].pop()

    return next_instance


class ClassIterator:
    def __init__(self, class_label, dataset_root):
        self.class_label = class_label
        self._files = [p for p in (Path(dataset_root) / class_label).iterdir() if p.is_file()]
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self) -> Path:
        if self._i >= len(self._files):
            raise StopIteration
        p = self._files[self._i]
        self._i += 1
        return p


class DatasetIterator:
    def __init__(self, dataset_root):
        classes = [p.name for p in Path(dataset_root).iterdir() if p.is_dir()]
        self._iterators = {c: ClassIterator(c, dataset_root) for c in classes}
        self._queue = list(classes)

    def __iter__(self):
        return self

    def __next__(self):
        while self._queue:
            cls = self._queue[0]
            try:
                return cls, next(self._iterators[cls])
            except StopIteration:
                self._queue.pop(0)
        raise StopIteration


if __name__ == "__main__":
    dataset_root = "D:\\Programming\\University\\Python\\NewTechsLab1\\dataset"
    create_annotation(dataset_root, "dataset/annotation.csv")

    copy_with_class_names(dataset_root, "dataset_flat", "dataset_flat/annotation.csv")

    copy_with_random_numbers(dataset_root, "dataset_shuffled", "dataset_shuffled/annotation.csv")

    nxt = make_next_instance(dataset_root)
    for i in range(5):
        print(nxt("rose"))

    for cls, path in DatasetIterator(dataset_root):
        print(cls, path)