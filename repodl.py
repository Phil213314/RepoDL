import os, bz2
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
def cleanf():
	if os.path.exists("Packages"):
		os.remove("Packages")
	if os.path.exists("Packages.bz2"):
		os.remove("Packages.bz2")
def parsePackages():
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
	return [debs, packages, versions]
print("Trying to download " + repourl + "Packages")
dl(repourl + "Packages", "Packages")
out = parsePackages()
debs = out[0]
packages = out[1]
versions = out[2]
if debs == []:
	print("File invalid.")
	print("Trying to download " + repourl + "Packages.bz2")
	os.remove("Packages")
	dl(repourl + "Packages.bz2", "Packages.bz2")
	open("Packages", 'wb').write(bz2.BZ2File("Packages.bz2").read())
	out = parsePackages()
	debs = out[0]
	packages = out[1]
	versions = out[2]
	if debs == []:
		print("File invalid.")
		cleanf()
		exit("Could not get Packages file.")
print("Successfully got Packages file")
#print("Debs: " + ", ".join(debs))
if len(debs) != len(packages) or len(debs) != len(versions) or len(packages) != len(versions):
	exit("'Packages' format error")
for i in tqdm(range(len(debs))):
	dl(repourl + debs[i], "debs/" + packages[i] + "-" + versions[i] + ".deb")
cleanf()