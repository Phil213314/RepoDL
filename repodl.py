import requests
def dl(url, filename):
	open(filename, 'wb').write(requests.get(url).content)
repourl = input("Repo:")
if not repourl.startswith("https://"):
	choice = input("Warning! Your repo url doesnt start with 'https://'. If the repo uses another protocol (e. g. http://) type 'c' if you forgot to add 'https://' type 'a' if you want to exit type 'e': ")
	if choice == "c":
		pass
	elif choice == "a":
		repourl = "https://" + repourl
	else:
		exit()
if not repourl.endswith("/"):
	repourl += "/"
dl(repourl + "Packages", "Packages")
pkgf = open("Packages")
pkgc = pkgf.readlines()
pkgf.close()
debs = []
for i in range(len(pkgc)):
	if pkgc[i].startswith("Filename: "):
		debs.append(pkgc[i].replace("Filename: ", "").replace("\n", ""))
print("Debs: " + ", ".join(debs))
for i in range(len(debs)):
	dl(repourl + debs[i], debs[i])