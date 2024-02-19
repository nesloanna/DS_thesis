import pandas as pd
import os

os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())


def main():
    depth_file_path = "TARA_sample_enviro.tab"
    df = read_tab_file(depth_file_path)
    df.to_csv("Tara_Environmental_Depth.csv", index=False)

    bio_file_path = "TARA_sample_biodiv.tab"
    df = read_tab_file(bio_file_path)
    df.to_csv("Tara_Biodiversity.csv", index=False)

    meso_file_path = "TARA_registies_mesoscale.tab"
    df = read_tab_file(meso_file_path)
    df.to_csv("Tara_Environmental_Mesoscale.csv", index=False)

    meso_sl_file_path = "TARA_SAMPLES_CONTEXT_ENV-WATERCOLUMN.tab"
    df = read_tab_file(meso_sl_file_path)
    df.to_csv("Tara_Env_Meso_SampleLocation.csv", index=False)


def read_tab_file(tab_file_path):

    data_rows = []
    file = open(tab_file_path, 'r')
    while True:
        line = file.readline().strip()
        if line == '*/':
            break

    while True:
        line = file.readline().strip()
        if line.strip() == '':
            break
        data_rows.append(line.split("\t"))

    file.close()
    df = pd.DataFrame(data_rows[1:], columns=data_rows[0])

    return df


if __name__ == '__main__':
    main()
