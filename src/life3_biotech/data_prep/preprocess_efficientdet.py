import os
import pandas as pd
from pathlib import Path, PurePath
from typing import Dict, List, Tuple
from json import load
from collections import defaultdict
from csv import DictWriter, writer
from pconst import const


class EfficientDetPipeline:

    def generate_annotations(self, logger, base_filename, annotations: pd.DataFrame = None) -> None:
        """
        Convert annotations into a CSV format required by the EfficientDet model implementation, where CSV file should be in this format:

        path/to/image.jpg,x1,y1,x2,y2,class_name

        where x1 = xmin, y1 = ymin, x2 = x max, y2 = ymax
        Args:
            logger (logging.Logger): Logger object to log events to
            annotations (DataFrame): 
        """
        annot_filepath = Path(const.INTERIM_DATA_PATH, const.COMBINED_ANNOTATIONS_FILENAME)
        if annotations is None:
            if annot_filepath.exists():
                annotations = pd.read_csv(annot_filepath, index_col=0)
            else:
                logger.error(f"Annotations file missing @ {annot_filepath}! No annotations to generate.")
                return
    
        data_value = []
        for _, annotation in annotations.iterrows():
            image_file_path = Path(const.RAW_DATA_PATH, annotation["file_name"])
            class_name = annotation["category_name"]
            x1 = int(annotation["bbox_x_min"])
            y1 = int(annotation["bbox_y_min"])
            x2 = int(annotation["bbox_x_max"])
            y2 = int(annotation["bbox_y_max"])
            data_value.append(
                [
                    image_file_path,
                    x1,
                    y1,
                    x2,
                    y2,
                    class_name,
                ]
            )
        with open(
            PurePath(const.PROCESSED_DATA_PATH, f"{base_filename.split('.')[0]}_efficientdet_b{const.ED_TRAIN_BACKBONE}.csv"), "w", newline=""
        ) as csv_file:
            csv_writer = writer(csv_file, delimiter=",")
            for data in data_value:
                csv_writer.writerow(data)


if __name__ == "__main__":
    pipeline = EfficientDetPipeline()
    pipeline.generate_annotations()
