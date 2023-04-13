import pandas as pd


def get_dd_info_DataFrame(info_path_excel):
    return pd.read_excel(info_path_excel, index_col=0)


def parse_dd_dump(path, archive_info: pd.DataFrame):
    res_path = "src/results/"

    with open(path, 'rb') as file:
        data = file.read()

    passing_val = 512
    for info_row in archive_info.iterrows():
        future_file_name = info_row[0]
        if str(future_file_name).__contains__("Fill"):
            continue
        file_name = future_file_name
        parsed_start = int(str(info_row[1]['start sector']).replace(',', '').replace('.', ''))
        parsed_end = int(str(info_row[1]['end sector']).replace(',', '').replace('.', ''))
        start = parsed_start * passing_val
        end = parsed_end * passing_val + passing_val

        with open(res_path + str(info_row[1]['dd_archive_name']) + file_name, 'wb') as res_file:
            res_file.write(data[start:end])

def main():
    files_dd_paths = ["src/archive/L5_Archive.dd",
                      "src/audio/L5_Audio.dd",
                      "src/documents/L5_Documents.dd",
                      "src/graphics/L5_Graphic.dd",
                      "src/vids/L5_Video.dd"]

    info_df = get_dd_info_DataFrame("src/dd_info.xlsx")
    for file_path in files_dd_paths:
        group = file_path.split('/')[-1]
        archive_info_df = info_df.loc[info_df['dd_archive_name'] == group]
        parse_dd_dump(file_path, archive_info_df)


if __name__ == '__main__':
    main()
