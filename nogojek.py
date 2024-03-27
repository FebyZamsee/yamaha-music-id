nmfile = input('nama file: ')
with open(nmfile,'r') as f:
    file = f.read().strip().splitlines()

for x in file:
    nomer = x.split('|')[0]
    print(nomer)
    with open(f'result.{nmfile}','a') as f:
        f.write(f"\n{nomer}")