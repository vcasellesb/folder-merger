import os
import shutil
from glob import glob

listdir = os.listdir

filesep = os.path.sep
join = os.path.join
basename = os.path.basename
dirname = os.path.dirname
abspath = os.path.abspath
isdir = os.path.isdir
isfile = os.path.isfile
exists = os.path.exists

def get_downloads_folder(downloads_folder: str=None) -> str:
    if downloads_folder is not None:
        downloads_folder = abspath(downloads_folder)
        assert isdir(downloads_folder), f'Yo?'
        return downloads_folder
    
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    if not isdir(downloads_folder):
        raise ValueError(f'Downloads folder not found in the default location: "{downloads_folder}". '
                         f'Please provide it using the downloads_folder flag. i.e.: "--downloads_folder <PATH>"')
    return downloads_folder

def recursively_list_all_files(folder_start: str,
                               exclusion: str='.DS_Store') -> list[str]:

    if isinstance(exclusion, str):
        exclusion = [exclusion]
    exclusion = list(exclusion)

    files = set()
    tmp = set([join(folder_start, i) for i in listdir(folder_start)])
    for t in tmp:
        if isdir(t) and all([basename(t) != e for e in exclusion]):
            files |= {t}
        else:
            files |= recursively_list_all_files(t, exclusion)
    
    return files

def recursively_remove_empty_folders(dir: str, 
                                     remove_root: bool=True, 
                                     exclusion_file: str='.DS_Store') -> None:
    """
    source: https://gist.github.com/jacobtomlinson/9031697?permalink_comment_id=3267924
    """
    if not isdir(dir):
        return

    # remove empty subfolders
    files = listdir(dir)
    if len(files):
        for f in files:
            if isdir(f): # I believe this can be removed
                recursively_remove_empty_folders(join(dir, f), remove_root, exclusion_file)

    # if folder empty, delete it
    files = listdir(dir)
    if remove_root and ((not len(files)) or ((len(files == 1) and files[0] == exclusion_file))):
        os.rmdir(dir)

def recursion(x: str, f: callable, exclusion: list[str]):
    if f(x): return x
    else:
        for j in [join(x, i) for i in listdir(x) if i not in exclusion]:
            return recursion(j, f, exclusion)

def isemptydir(dir: str, exclusion: str='.DS_Store') -> bool:
    return isdir(dir) and not len([i for i in listdir(dir) if i not in exclusion])

def least_common_denominator(path1: str, path2: str, nono: str) -> str:

    # to remove trailing slashes
    path1 = abspath(path1)
    path2 = abspath(path2)

    if path1 == path2:
        return path1
    nono_basenamed = basename(nono)
    shorter, longer = sorted([path1, path2])
    tmp = longer
    while (nono_basenamed not in basename(tmp)) and tmp != shorter:
        tmp = dirname(tmp)

    return tmp

def maybe_make_dir(dir: str) -> None:
    if not exists(dir):
        os.makedirs(dir)

def check_no_messed_up(list_after_split: list[str]) -> None:
    # TODO: delete

    beggining = list_after_split[0]
    end = list_after_split[-1]
    if beggining.startswith('/'):
        raise RuntimeError(f'Something went really wrong: {(" ".join(list_after_split))}')
    if end.startswith('/'):
        raise RuntimeError(f'Something went really wrong: {" ".join(list_after_split)}')

def main(folder_name: str, 
         downloads_folder: str=None,
         where_everything_will_be_moved_to: str=None) -> None:
    
    downloads_folder = get_downloads_folder(downloads_folder)
    targets = glob(join(downloads_folder, folder_name + '*'))
    
    n_targets = len(targets)
    assert n_targets, f'No file matching pattern "{folder_name}" found in the "{downloads_folder}" target folder.'

    print(f'I have found {n_targets} folders matching pattern "{folder_name}".')

    if where_everything_will_be_moved_to is None:
        where_everything_will_be_moved_to = join(downloads_folder, folder_name)
        assert isdir(where_everything_will_be_moved_to)
        targets.remove(where_everything_will_be_moved_to) # no need to parse it too
    else:
        maybe_make_dir(where_everything_will_be_moved_to)
    
    print(f'Everything will be moved to: "{where_everything_will_be_moved_to}"')

    for target in targets:
        files = recursively_list_all_files(target)
        for file in files:
            # we get to_add by finding everything that is after the matching pattern 
            first, second = file.split(folder_name)

            assert all([isinstance(i, str) and len(i) for i in [first, second]])

            myindex = second.index(filesep) # strip everything added by drive 

            to_add = second[myindex:].strip(basename(file))
            maybe_make_dir(where_everything_will_be_moved_to + to_add)
            shutil.move(file, where_everything_will_be_moved_to + to_add + filesep + basename(file))
        
        # the directory target now should be empty of files. This should work
        recursively_remove_empty_folders(target)

def tests() -> None:
    true_downloads_folder = '/Users/vicentcaselles/Downloads'
    downloads_folder = get_downloads_folder()
    assert downloads_folder == true_downloads_folder

    try:
        downloads_folder = get_downloads_folder('fake_downloads')
    except AssertionError as e:
        print(f'{e} \nYay!')
    
    downloads_folder = 'Downloads'
    downloads_folder = get_downloads_folder(downloads_folder)
    assert downloads_folder == true_downloads_folder


    downloads_folder = os.path.abspath('Downloads')
    files = recursively_list_all_files(downloads_folder + '/dataset_generated_new')
    assert len(files) == 29
    
    path1 = '/Users/vicentcaselles/Downloads/dataset_generated_new/generated_pseudomasks/subj2'
    path2 = '/Users/vicentcaselles/Downloads/dataset_generated_new/generated_pseudomasks/subj2'
    cd = least_common_denominator(path1, path2, '/Users/vicentcaselles')
    assert cd == path1

if __name__ == "__main__":
    # we test main
    main(
        folder_name='dataset_generated_new',
        downloads_folder='/Users/vicentcaselles/Downloads',
        where_everything_will_be_moved_to='/Users/vicentcaselles/work/research/project_MARCOS/dataset_generated_new'
    )