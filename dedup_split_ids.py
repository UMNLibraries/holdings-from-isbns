import pandas as pd
from itertools import islice


def dedup_ids(df, col='MMSID'):
    '''Dedups a column in a Pandas dataframe. 
    Parameters: dataframe containing the column to dedup, column to dedup (col=, default=MMSID)'''
    df = df[df[col] != 'none']
    uniq_ids = df[col].unique()
    return uniq_ids


def split_ids(idlist, length=9999):
    '''Returns multiple lists of a specified length from a single list.
    Parameters: list to divide, number of members in sublists (length=, default=9999)'''
    full_len = len(idlist)
    sublist_no = full_len // length
    lines_list = []
    while sublist_no > 0:
        lines_list.append(length)
        sublist_no -= 1
    last_list = full_len % length
    if last_list != 0:
        lines_list.append(last_list)
    id_list = iter(idlist)
    id_subs = [list(islice(id_list, x)) for x in lines_list]
    return id_subs


def main():
    pfile = input('Pandas pickle file? ')
    df = pd.read_pickle(pfile)
    uniq_ids = dedup_ids(df)
    idlist = list(uniq_ids)
    split_idlist = split_ids(idlist)
    split_count = 1
    for sublist in split_idlist:
        with open(f'unique_ids_{split_count}.txt', 'w') as f:
            for member in sublist:
                f.write(member + '\n')
        split_count +=1
    print(f'{split_count-1} files written.')


if __name__ == "__main__":
    main()