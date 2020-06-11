import glob
import os
import re
import shutil
from typing import List, Tuple, TypeVar

from common_py.folder import files_in_folder
from common_py.functional.either import Either, Left, Right, sequences


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
        List of starting words of files to be deleted
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


def rename_file(
    original_filename: str, change_to: str, path: str
) -> Either[str, Exception]:
    """
    In `path` folder, change file name `original_filename` to `change_to`.

    Parameters
    ----------
    original_filename : str
        Original file name
    change_to : str
        File name to change
    path : str
        File path

    Returns
    -------
    Either[str, Exception]
        
        - Right(str) Success. Changed file path and name.
        - Left(FileNotFoundError) Failure. `original_filename` does not exist.
        - Left(Exception) Failure. Failed for another reason.
    
    Notes
    -----
    .. versionadded:: 0.1.0
    """
    try:
        os.rename(os.path.join(path, original_filename), os.path.join(path, change_to))
        return Right(os.path.join(path, change_to))
    except Exception as err:
        return Left(err)


def rename_files(
    original_filename__change_to_list: List[Tuple[str, str]], path: str
) -> Either[List[str], Exception]:
    """
    In `path` folder, change multiple file names.

    Even if an error occurs during the name change, the name change until the error occurs is applied.

    Parameters
    ----------
    original_filename__change_to_list : List[Tuple[str, str]]
        List of tuples, of original file name and file name to change
    path : str
        File path

    Returns
    -------
    Either[List[str], Exception]
        
        - Right(str) Success. Changed file path and name.
        - Left(FileNotFoundError) Failure. `original_filename` does not exist.
        - Left(Exception) Failure. Failed for another reason.

    Notes
    -----
    .. versionadded:: 0.1.0
    """
    results: List[Either[str, Exception]] = []
    for original_filename__change_to in original_filename__change_to_list:
        results.append(
            rename_file(
                original_filename=original_filename__change_to[0],
                change_to=original_filename__change_to[1],
                path=path,
            )
        )
    return sequences(results)


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
