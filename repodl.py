import os, bz2
try:
	import requests
except Exception:
	exit("requests module is not installed. It is required in order to run this script.")
try:
	from tqdm import tqdm
except Exception:
	exit("tqdm module is not installed. It is required in order to run this script.")
def err_and_exit(dir, text):
	with open(dir + "/error.log", 'w') as e:
		e.write(text)
	exit(text)
headers={"X-Machine":"iPhone13,3", "X-Firmware":"14.3","X-Unique-ID":"00000000-0000000000000000"}
def dl(url, filename):
	if filename == 0:
		return requests.get(url, headers=headers).content
	else:
		open(filename, 'wb').write(requests.get(url, headers=headers).content)
repourl = input("Repo:")
if not repourl.startswith("https://") and not repourl.startswith("http://"):
		repourl = "https://" + repourl
		print("Warning. No protocol was provided in repo url so https is used.")
if not repourl.endswith("/"):
	repourl += "/"
repodir = repourl.split("//")[1].split("/")[0]
if not os.path.exists(repodir):
	os.makedirs(repodir)
else:
	if not os.path.isdir(repodir):
		exit("There is a file named '" + repodir + "' in the current folder. Remove it in order to run this script")
def parsePackages(pkgc):
	pkgc = pkgc.split("\n")
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
print("Trying to get " + repourl + "Packages")
out = parsePackages((dl(repourl + "Packages", 0)).decode())
debs = out[0]
packages = out[1]
versions = out[2]
if debs == []:
	print("File invalid.")
	print("Trying to download " + repourl + "Packages.bz2")
	try:
		out = parsePackages(bz2.decompress(dl(repourl + "Packages.bz2", 0)).decode())
	except OSError:
		print("File invalid.")
		err_and_exit(repodir, "Could not get Packages file (bz2 err)")
	debs = out[0]
	packages = out[1]
	versions = out[2]
	if debs == []:
		print("File invalid.")
		err_and_exit(repodir, "Could not get Packages file")
print("Successfully got Packages file")
#print("Debs: " + ", ".join(debs))
if len(debs) != len(packages) or len(debs) != len(versions) or len(packages) != len(versions):
	err_and_exit(repodir, "File format error")
if not os.path.exists(repodir + "/debs"):
	os.makedirs(repodir + "/debs")
for i in tqdm(range(len(debs))):
	dl(repourl + debs[i], repodir + "/debs/" + packages[i] + "-" + versions[i] + ".deb")