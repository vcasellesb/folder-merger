# Folder merger for Mac

This project came about because of my nuisance at Google Drive splitting a folder I download into several folders, with overlapping subdirectories. This usually happens with big folders and, since I work in medical imaging, this is a fairly common thing for me.

For example, when trying to download a folder called `test-data` from Google Drive, it would get split into several subfolders with "`-i`" (where $i$ is a number) added, such as:

````bash
test-data
test-data-2
test-data-3
...
test-data-N
````

Where the subfolders in each `test-data-i` overlap, i.e.:
````bash
test-data/subfolder1/image1
test-data-2/subfolder1/image2
````
So you can see I want to have only one `subfolder1` with both files (`image`), instead of this mess. Therefore, my code tries to recursively merge all `test-data*` into a specific destination folder, which by default is `test-data`.

To use it, you have to call the script with the pattern string (which, in the above example, would be `test-data`). You can also specify the downloads folder where the pattern will be looked for using `glob` with the `--downloads_folder` flag (by default we assume its `$HOME/Downloads`), and the destination folder where everything will be moved to, with the `--destination` flag.

## DISCLAIMER
I am not a Computer Scientist, just a researcher in medical imaging that wants to learn how to code. Please use this code carefully and, if there is any improvements to make (there are), please open and issue. Also, this code has been created with a VERY specific use-case, which is related to downloading data from Google Drive and then recursively merging it into one folder when Drive splits it due to its size. **Therefore, I wouldn't recommend using it on ANY data that you don't have a backup for**. Please mark my words.

Also, as the title suggests, I don't know if the situation that inspired this code happens in any other OS, so the "design" is very geared towards MacOS. Keep that in mind also.