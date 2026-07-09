import os
import re
import typing as ty
from pathlib import Path
import tempfile

import mne.io

from fileformats.core import extra_implementation, FileSet
from fileformats.biosig.base import Biosig
from fileformats.vendor.neuroscan import Neuroscan

from fileformats.extras.biosig.utils import mne_deidentify


@extra_implementation(FileSet.read_metadata)
def neuroscan_read_metadata(cdt_fname: str, **kwargs: ty.Any) -> ty.Mapping[str, ty.Any]:
    return mne.io.read_raw_curry(fname=cdt_fname, preload=False, verbose=False).info.to_json_dict()  # type: ignore[no-any-return]


@extra_implementation(Biosig.deidentify)
def neuroscan_deidentify(
    dpa_fname: str,
    dpo_fname: str,
    spec: ty.Any = None,
    out_dir: os.PathLike[str] | None = None,
):
    out_dir = Path(tempfile.mkdtemp() if out_dir is None else out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if dpa_fname is not None:
        clear_comments_filehistory(input_path=dpa_fname, output_path=dpa_fname, overwrite=True)
    if dpo_fname is not None:
        clear_comments_filehistory(input_path=dpo_fname, output_path=dpo_fname, overwrite=True)
    

def clear_comments_filehistory(input_path: str, output_path: str = None, overwrite: bool = False):
    """
    Clear all content after "Comments = " and "FileHistory = " in dpa text file
    :param input_path: Path of the original input dpa txt file
    :param output_path: Path to save cleaned file; ignored if overwrite=True
    :param overwrite: If True, overwrite the original input file directly
    :return: Cleaned text string if no file output is set
    """
    # Read full content from source file with utf-8 encoding
    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Regex pattern to match entire content after Comments = (supports multi-line)
    pattern_comments = re.compile(r"(Comments\s*=).*", re.DOTALL)
    # Regex pattern to match entire content after FileHistory = (supports multi-line file list)
    pattern_filehistory = re.compile(r"(FileHistory\s*=).*", re.DOTALL)

    # Replace matched content, only keep "Comments =" / "FileHistory =" prefix
    clean_text = pattern_comments.sub(r"\1", raw_text)
    clean_text = pattern_filehistory.sub(r"\1", clean_text)

    # Handle file output logic
    if overwrite:
        # Overwrite original source file
        with open(input_path, "w", encoding="utf-8") as f_out:
            f_out.write(clean_text)
        print(f"Original file overwritten: {input_path}")
    elif output_path is not None:
        # Write cleaned content to new specified file
        with open(output_path, "w", encoding="utf-8") as f_out:
            f_out.write(clean_text)
        print(f"Cleaned file saved to: {output_path}")