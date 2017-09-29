import pandas as pd
import shutil
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import math
import logging

def split_data(data_df):
    '''
    splits the data based off a given key. Probably have to tweak this
    to make it more generic. handle the rounding outside?
    '''
    t_key = 'Temperature (K)'
    data_df = data_df
    data_df[t_key] = data_df[t_key].round(1)
    res = {}
    for temp in set(data_df[t_key].tolist()):
        res[temp] = data_df[data_df[t_key] == temp]

    return res

def subset(data_df):
    return data_df[['Field (Oe)', 'Temperature (K)', "m' (emu)", 'm\" (emu)', 'Wave Frequency (Hz)']]

def compute_chi(m, e_mass, y_mass,
                moles, dmc):
    """
    m', "" value
    eicosane mass
    Y complex mass
    moles
    diamagnetic correction
    """
    return ((m / 4) + (e_mass / 282548) * 0.00024306 +
            (y_mass / 698124) * 0.00040896) / moles - dmc


def calculate_chi(data_df, e_mass, y_mass,
                   moles, dmc):
    """
    Mutates the provided data_df, appending calculated
    chi' and chi" values
    """
    # calculate the emulated values. d1 is chi', d2 chi"
    d1 = compute_chi(data_df["m' (emu)"],
                     e_mass,
                     y_mass,
                     moles,
                     dmc)
    d2 = compute_chi(data_df['m" (emu)'],
                     e_mass,
                     y_mass,
                     moles,
                     dmc)
    return {"chi' (emu)": d1,
            'chi" (emu)': d2}

def compute_chi_p_fit(data_df, wave_freq,
                      chi_t, chi_s, alpha, tau):
    """
    Calculates the chi' (fit) value for a given row instance
    """
    return chi_s + (chi_t - chi_s) * (1 + (2 * math.pi * wave_freq * tau) ** (1 - alpha) * math.sin(math.pi * alpha / 2)) / (1 + 2 * (2 * math.pi * wave_freq * tau) ** (1 - alpha) * math.sin(math.pi * alpha / 2) + (2 * math.pi * wave_freq * tau) ** (2 - 2 * alpha))

def compute_chi_pp_fit(data_df, wave_freq,
                      chi_t, chi_s, alpha, tau):
    return (chi_t - chi_s) * ((2 * math.pi * wave_freq * tau) ** (1 - alpha) * math.cos(math.pi * alpha / 2)) / (1 + 2 * (2 * math.pi * wave_freq * tau) ** (1 - alpha) * math.sin(math.pi * alpha / 2) + (2 * math.pi * wave_freq * tau) ** (2 - 2 * alpha))

def insert_df_excel(df, sheet, rt, ct, skip_n=0):
    for r, row in enumerate(dataframe_to_rows(df), start=rt):
        if skip_n and r < rt + skip_n:
            continue
        # We need to handle the 
        for c, col in enumerate(row, start= ct - 1):
            if c < ct:
                continue
            sheet.cell(row=r, column=c, value=col)
    return 1

def make_excel(dat_path, out_path):
    shutil.copy('data/template.xlsx', out_path)
    wb = openpyxl.load_workbook(out_path)
    parsed = parse.parse_file(dat_path)
    header = parse.parse_header(parsed['header'])
    data = parse.parse_data(parsed['data'])
    data = process.subset(data)
    data = process.split_data(data)

    for temp in sorted(data):
        df = data[temp]
        # print(df)
        sheet = wb.copy_worksheet(wb['Sheet1'])
        sheet.title = "ac_varT-{}K".format(temp)
        insert_df_excel(df, sheet, 5, 1, skip_n=1)
    # wb.remove_sheet(wb['Sheet1'])
    wb.save(out_path)
