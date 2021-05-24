# Morphontogeny


Analysis scripts for morphometry and spacial transcriptomic data.

___

## Installing this repository as a python package

```pip install git+https://github.com/BioProteanLabs/Morphontogeny.git ```

This will install the latest commit to the main branch of this repository. Bear in mind that the latest commit to the main branch will change over time!


If you'd like to install a specific version of the package, you can use the commit hash of the version you want:

```pip install git+https://github.com/BioProteanLabs/Morphontogeny.git@dfc041dc4a31d4833bce7d304c61a078ceb994d9```

Now you should be able to just

```import morphontogeny```

and use its tools!
___

## Adding your own tools to this repository

You'll need git installed on your local machine. Check to see if it's already installed with

```git --version```

If it isn't installed, you'll need to install it. On Mac, this is [evidently](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) as easy as running the above command. If that doesn't work, you can download an installer from the [git website](https://git-scm.com/download/mac). There's an installer for [Windows](https://git-scm.com/download/win) as well.

You'll now need to clone the repo onto your local machine. On the page for the repository, click the green "Code" button, select HTTPS, and copy the URL. Open a terminal in the directory where you want the repo, and run 
``` git clone <URL> ```

The repo is now on your local machine!

Because multiple people are going to be committing to this repository, we need to use branches in order to avoid overwriting each others' work. There should already be a "momo" and a "naren" branch made, so after you've cloned the repo, you'll need to

```git checkout <branch name> ```

to switch to your own branch.

You'll notice there's a file called `.gitignore` in your repo. This file tells git to ignore certain files - don't add them, don't commit them, don't push them up to github. If you have a large data file in your repo, you'll want to add its name to this file. Same thing goes for things like virtual environments made with `venv`, editor settings like `.vscode`, and so on.

When you'd like to push your changes back up to Github, you'll do the following:

```git status```

This command will tell you about all the unstaged files that have been created or had changes made since your last commit.

```git add <file>```

This command adds the file to the commit you're about to make. You can specify a specific file or directory, or you can use `.` in place of `<file>` to add all the files in your current directory.

```git commit -m "<your message here>"```

This command takes the changes you've staged with `add`, and commits them to your branch, with the commit message you've specified.

```git push origin <branch name>```

This command pushes the committed changes up to Github! You're done!

___

## Retrieving updated versions of this repository

This is the dangerous part. The command `git pull` retrieves changes from Github and merges them into your local repo. When this happens, uncommitted local changes can be overwritten, or you can run into a merge conflict. We can avoid this by simply making changes to our own branches - if you only ever alter your own branch, the only changes to your own branch that there are to be pulled are the ones you made!

If you're concerned that you might overwrite your own work by `git pull`-ing (we've all done it, don't fret), just don't `git pull` - we'll fix it.

___

## Other errata

We'll need to keep track of the dependencies that the library uses (they need to be in `setup.py` so that they are installed with the library.) If you use a tool like `venv` or `pipenv` to manage dependencies for each project, then a requirements.txt or Pipfile in your local repo is fine (but put it in the .gitignore). If you use `conda`, you're probably used to using a few global environments for all your work. You may want to create an environment specifically for this project, and do something similar - or manually keep track of the dependencies you use and their versions in a text file (whose name should also be in the gitignore).

We'll want to avoid filename collisions, so making a subdirectory below "morphontogeny" (the inner directory!) and then adding your python files to that is probably wise.