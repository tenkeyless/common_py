import glob
import os
import re
import shutil
from typing import Optional, Callable, List, Tuple, TypeVar
from pathlib import Path
import common_py
import toolz
from toolz import curry


def files_in_folder(
    folder_name: str,
    include_hidden_file: bool = False,
    filters: List[Callable[[str], bool]] = [],
) -> List[str]:
    """
    Get files in folder.

    Parameters
    ----------
    folder_name : str
        Folder name
    include_hidden_file : bool, optional
        Whether hidden files are included(starts with '.'), by default False
    filters : List[Callable[[str], bool]], optional
        Filters to apply to result, by default []

    Returns
    -------
    List[str]
        File list

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    # file only
    filters.append(lambda f: os.path.isfile(folder_name + "/" + f))
    # hidden file filter
    if include_hidden_file is False:
        filters.append(lambda file_name: not file_name.startswith("."))
    files: List[str] = toolz.pipe(
        folder_name, os.listdir, curry(common_py.list_filters)(filters), list, sorted,
    )  # type: ignore
    return files


def create_folder_if_not_exist(folder_path: str) -> None:
    """
    Create a folder if it doesn't exist.

    Parameters
    ----------
    folder_path : str
        Folder path to create.
    
    Notes
    -----
    .. versionadded:: 0.1.0
    """
    Path(folder_path).mkdir(parents=True, exist_ok=True)


# def move_all_file_to_folder(from_folder: str, _target_folder: str) -> None:
#     for file in get_files_only_in_folder(from_folder):
#         shutil.move(os.path.join(from_folder, file), _target_folder)


# def move_overwrite_all_file_to_folder(from_folder: str, _target_folder: str) -> None:
#     cwd = os.getcwd()
#     for file in get_files_only_in_folder(from_folder):
#         shutil.move(
#             os.path.join(cwd, from_folder, file),
#             os.path.join(cwd, _target_folder, file),
#         )


# def copy_all_file_to_folder(from_folder: str, _target_folder: str) -> None:
#     for file in get_files_only_in_folder(from_folder):
#         shutil.copy2(os.path.join(from_folder, file), _target_folder)


# def remove_files(starts_with_list: List[str], target_path: str) -> None:
#     for _file_starts_with in starts_with_list:
#         for _file in glob.glob("{}/{}*".format(target_path, _file_starts_with)):
#             os.remove(_file)


# def rename_files(
#     sorted_list1: List[str], sorted_list2: List[str], target_path: str
# ) -> None:
#     rename_files_from_list: List[Tuple[int, Tuple[str, str]]] = []
#     _rev_current_file_names = sorted_list1
#     for index, current_file_name in enumerate(sorted_list2):
#         rename_files_from_list.append(
#             (index, (current_file_name, _rev_current_file_names[index]))
#         )
#     for rename_files_for_prev_from_to in sorted(rename_files_from_list):
#         for old_name in glob.glob(
#             "{}/{}*".format(target_path, rename_files_for_prev_from_to[1][0])
#         ):
#             new_name = re.sub(
#                 r"(.*)(.{6}).*\.png",
#                 rename_files_for_prev_from_to[1][1] + r"\2.png",
#                 os.path.basename(old_name),
#             )
#             os.rename(old_name, os.path.join(target_path, new_name))
