try:
	import os
except Exception:
	exit("os module can not be loaded. This usually happens when running python in a sandboxed environment (e. g. pythonista). These kinds of environments are not supported.")
try:
	import requests
except Exception:
	exit("requests module is not installed. It is required in order to run this script.")
try:
	from tqdm import tqdm
except Exception:
	exit("tqdm module is not installed. It is required in order to run this script.")
def dl(url, filename):
	open(filename, 'wb').write(requests.get(url).content)
repourl = input("Repo:")
if not repourl.startswith("https://"):
	choice = input("Warning! Your repo url doesnt start with 'https://'. If the repo uses another protocol (e. g. http://) type 'c'. If you forgot to add 'https://' type 'a'. If you want to exit type 'e': ")
	if choice == "c":
		pass
	elif choice == "a":
		repourl = "https://" + repourl
	else:
		exit()
if not repourl.endswith("/"):
	repourl += "/"
if not os.path.exists("debs"):
	os.makedirs("debs")
else:
	if not os.path.isdir("debs"):
		exit("There is a file named 'debs' in the current folder. Remove it in order to run this script")
dl(repourl + "Packages", "Packages")
pkgf = open("Packages")
pkgc = pkgf.readlines()
pkgf.close()
debs = []
packages = []
versions = []
for i in range(len(pkgc)):
	if pkgc[i].startswith("Filename: "):
		debs.append(pkgc[i].replace("Filename: ", "").replace("\n", ""))
	elif pkgc[i].startswith("Package: "):
		packages.append(pkgc[i].replace("Package: ", "").replace("\n", ""))
	elif pkgc[i].startswith("Version: "):
		versions.append(pkgc[i].replace("Version: ", "").replace("\n", ""))
if len(debs) != len(packages) or len(debs) != len(versions) or len(packages) != len(versions):
	exit("'Packages' format error")
#print("Debs: " + ", ".join(debs))
for i in tqdm(range(len(debs))):
	dl(repourl + debs[i], "debs/" + packages[i] + "-" + versions[i] + ".deb")