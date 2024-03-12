import pantab
import os

hyper_location = "./hyper"
csv_location = "./csv"

if not os.path.exists(csv_location):
    os.makedirs(csv_location)

print("\n----- Converting hyper files to csv -----\n")
for hyper in os.listdir(hyper_location): 
    hyper_file = f"{hyper_location}/{hyper}"
    hyper = hyper.replace(".hyper", ".csv")
    #print("Writing", f"{hyper_location}/{hyper}")
    pt_dict = pantab.frames_from_hyper(hyper_file)
    assert len(pt_dict.values()) == 1
    df = list(pt_dict.values())[0]
    csv_file = f"{csv_location}/{hyper}"
    print(f"Creating {csv_file}")
    df.to_csv(csv_file, index=False)

