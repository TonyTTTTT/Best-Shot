## 2021/9/27
- Find out that you can solve pip requirements file problem by setting some option in the file, but must care that some option is global option, so best to create antother requirements file if using some global options just for some of the package
	- https://pip.pypa.io/en/stable/cli/pip_install/#install-find-links
- Fail to handle kera & tensorflow conflict directly in requirements files

## 2021/10/7
- Let the classPredictor output 5 labels instead of 1
- Next step
	- convert code about assessment pictore from tensorflow to pytorch
	- Let the user gave feedback about predicted score