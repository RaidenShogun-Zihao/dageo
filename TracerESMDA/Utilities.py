import os
import subprocess
import UTCHEMresult
import math
import os
import shutil
def UTCHEMsim(index,x):
    file_address=f"D:\IWTT\{index}"
    os.chdir(file_address)
    Updateinput(x)
    subprocess.call("UTCHEM.exe", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"finished case{int(index)}")
    simresult = UTCHEMresult.result(file_address)
    return simresult


def Updateinput(x):
    f=open('PERMX','w')
    f.write('*----PERMX\n')
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            #f.write(f'{x[0][i,j]}\n')
            f.write(f'{math.exp(x[i,j])}\n')
    f.close()

def createfile():
    for i in range(50):
        # Define the folder path
        destination_folder = f"D:\IWTT\{i}"
        # Create the folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)
        # Define the path to the original UTCHEM directory
        source_folder = r"D:\IWTT\sample\UTCHEM.exe"  # Change this to the actual path
        # Copy UTCHEM to the new folder
        shutil.copy(source_folder, os.path.join(destination_folder, "UTCHEM.exe"))

        source_folder = r"D:\IWTT\sample\INPUT"  # Change this to the actual path
        # Copy UTCHEM to the new folder
        shutil.copy(source_folder, os.path.join(destination_folder, "INPUT"))


        print("UTCHEM copied successfully.")


if __name__=='__main__':
    createfile()
