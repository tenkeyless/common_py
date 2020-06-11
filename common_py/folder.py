from common_py.functional.either import Either, Right, Left
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
    filters2: List[Callable[[str], bool]] = filters.copy()
    filters2.append(lambda f: os.path.isfile(folder_name + "/" + f))
    # hidden file filter
    if include_hidden_file is False:
        filters2.append(lambda file_name: not file_name.startswith("."))
    filtered_function: Callable[[List[str]], List[str]] = toolz.compose_left(
        os.listdir, curry(common_py.list_filters)(filters2), list
    )
    files: List[str] = filtered_function(folder_name)  # type: ignore

    return files


def create_folder(folder_path: str, exist_ok: bool = True) -> Either[str, Exception]:
    """
    Create a folder if it doesn't exist.

    Parameters
    ----------
    folder_path : str
        Folder path to create.
    exist_ok : bool
        Create folder if does not exist, by defaults True
    
    Returns
    -------
    Either[str, Exception]
        
        - Right(str) Success. Created folder_path.
        - Left(FileExistsError) Failure. When exist_ok is False and the folder already exists.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    try:
        Path(folder_path).mkdir(parents=True, exist_ok=exist_ok)
        return Right(folder_path)
    except FileExistsError as err:
        return Left(err)
    except Exception as err:
        return Left(err)


def move_all_file(
    from_folder: str, target_folder: str, overwrite: bool = True
) -> Either[int, Exception]:
    """
    Move all files from `from_folder` to `target_folder`.


    Parameters
    ----------
    from_folder : str
        Original folder
    target_folder : str
        Target folder
    overwrite : bool
        If this is True, the files are overwritten if they exist. by default True.

    Returns
    -------
    Either[int, Exception]
        
        - Right(int) Success. Number of files moved.
        - Left(FileNotFoundError) Failure. If there is no `from_folder` or `target_folder`.
        - Left(Exception) Failure. Failed for another reason.
    
    Notes
    -----
    .. versionadded:: 0.1.0
    """
    try:
        cwd = os.getcwd()
        files: List[str] = files_in_folder(from_folder, include_hidden_file=True)
        for file in files:
            if overwrite:
                shutil.move(
                    os.path.join(cwd, from_folder, file),
                    os.path.join(cwd, target_folder, file),
                )
            else:
                shutil.move(os.path.join(from_folder, file), target_folder)
        return Right(len(files))
    except FileNotFoundError as err:
        return Left(err)
    except Exception as err:
        return Left(err)


def copy_all_file(from_folder: str, target_folder: str) -> Either[int, Exception]:
    """
    Copy all files from `from_folder` to `target_folder`.

    Parameters
    ----------
    from_folder : str
        Original folder
    target_folder : str
        Target folder

    Returns
    -------
    Either[int, Exception]
        
        - Right(int) Success. Number of files copied.
        - Left(Exception) Failure. Failed for another reason.
    
    Notes
    -----
    .. versionadded:: 0.1.0
    """
    try:
        files: List[str] = files_in_folder(from_folder, include_hidden_file=True)
        for file in files:
            shutil.copy2(os.path.join(from_folder, file), target_folder)
        return Right(len(files))
    except Exception as err:
        return Left(err)


def remove_all_files(target_folder: str) -> Either[int, Exception]:
    """
    In `target_folder`, remove all files.

    Parameters
    ----------
    target_folder : str
        Target folder

    Returns
    -------
    Either[int, Exception]
        
        - Right(int) Success. Number of files deleted.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    try:
        count = 0
        for file in files_in_folder(target_folder, True):
            os.remove(os.path.join(target_folder, file))
            count += 1
        return Right(count)
    except Exception as err:
        return Left(err)


def remove_files(
    starts_with_list: List[str], target_folder: str
) -> Either[int, Exception]:
    """
    In `target_folder`, Remove files starting with those defined in `starts_with_list`.

    Parameters
    ----------
    starts_with_list : List[str]
        [description]
    target_folder : str
        [description]

    Returns
    -------
    Either[int, Exception]
        
        - Right(int) Success. Number of files deleted.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    starts_with_list2: List[str] = starts_with_list.copy()
    try:
        count = 0
        for starts_with in starts_with_list2:
            for file in glob.glob("{}/{}*".format(target_folder, starts_with)):
                os.remove(file)
                count += 1
        return Right(count)
    except Exception as err:
        return Left(err)


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
