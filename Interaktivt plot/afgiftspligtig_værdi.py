import WhatIfAnalysis as WIA

# Link til generel CO2 udledning for hver biltype: https://www.dst.dk/Site/Dst/Udgivelser/nyt/GetPdf.aspx?cid=34728
# Link til CO2 takst i 2020: https://skat.dk/skat.aspx?oid=2302178

def pris_efter_reg_afgift_ben(afgiftspligtig_værdi, bundfradrag = 21700.0, reg_beloeb1 = 65000.0, reg_beloeb2 = 202200.0, 
                            part_1 = 0.25, part_2 = 0.85, part_3 = 1.5):
    CO2_NEDC = 111.6
    CO2_takst = 250
    CO2_tillaeg = CO2_NEDC * CO2_takst
    if afgiftspligtig_værdi < reg_beloeb1:
        reg_part1 = part_1 * afgiftspligtig_værdi
        endelig_reg_afgift = reg_part1 + CO2_tillaeg - bundfradrag # Find ud af om bundfradrag altid skal trækkes fra her
        return afgiftspligtig_værdi + endelig_reg_afgift
    else:
        reg_part1 = part_1 * reg_beloeb1
        if afgiftspligtig_værdi < reg_beloeb2:
            reg_part2 = part_2 * (afgiftspligtig_værdi - reg_beloeb1)
            endelig_reg_afgift = reg_part1 + reg_part2 + CO2_tillaeg - bundfradrag
            return afgiftspligtig_værdi + endelig_reg_afgift
        else:
            reg_part2 = part_2 * (reg_beloeb2 - reg_beloeb1)
            reg_part3 = part_3 * (afgiftspligtig_værdi - reg_beloeb2)
            endelig_reg_afgift = reg_part1 + reg_part2 + reg_part3 + CO2_tillaeg - bundfradrag
            return afgiftspligtig_værdi + endelig_reg_afgift

def pris_efter_reg_afgift_die(afgiftspligtig_værdi, bundfradrag = 21700.0, reg_beloeb1 = 65000.0, reg_beloeb2 = 202200.0,
                            part_1 = 0.25, part_2 = 0.85, part_3 = 1.5):
    CO2_NEDC = 113.9
    CO2_takst = 250
    CO2_tillaeg = CO2_NEDC * CO2_takst
    if afgiftspligtig_værdi < reg_beloeb1:
        reg_part1 = part_1 * afgiftspligtig_værdi
        endelig_reg_afgift = reg_part1 + CO2_tillaeg - bundfradrag # Find ud af om bundfradrag altid skal trækkes fra her
        return afgiftspligtig_værdi + endelig_reg_afgift
    else:
        reg_part1 = part_1 * reg_beloeb1
        if afgiftspligtig_værdi < reg_beloeb2:
            reg_part2 = part_2 * (afgiftspligtig_værdi - reg_beloeb1)
            endelig_reg_afgift = reg_part1 + reg_part2 + CO2_tillaeg - bundfradrag
            return afgiftspligtig_værdi + endelig_reg_afgift
        else:
            reg_part2 = part_2 * (reg_beloeb2 - reg_beloeb1)
            reg_part3 = part_3 * (afgiftspligtig_værdi - reg_beloeb2)
            endelig_reg_afgift = reg_part1 + reg_part2 + reg_part3 + CO2_tillaeg - bundfradrag
            return afgiftspligtig_værdi + endelig_reg_afgift

kWh = 45
def pris_efter_reg_afgift_el(afgiftspligtig_værdi, bundfradrag = 21700.0, ekstra_bundfradrag = 170000.0, indfasning = 0.40, 
                            reg_beloeb1 = 65000, reg_beloeb2 = 202200.0, el_fradrag = 1700.0,
                            part_1 = 0.25, part_2 = 0.85, part_3 = 1.5):
        samlet_el_fradrag = el_fradrag * kWh
        ny_afgiftspligtig_værdi = afgiftspligtig_værdi - samlet_el_fradrag
        if ny_afgiftspligtig_værdi < reg_beloeb1:
            reg_part1 = part_1 * ny_afgiftspligtig_værdi
            endelig_reg_afgift = reg_part1 - bundfradrag # Find ud af om bundfradrag altid skal trækkes fra her
            if endelig_reg_afgift < 0:
                return afgiftspligtig_værdi
            else: 
                return afgiftspligtig_værdi + endelig_reg_afgift
        else:
            reg_part1 = part_1 * reg_beloeb1
            if ny_afgiftspligtig_værdi < reg_beloeb2:
                reg_part2 = part_2 * (ny_afgiftspligtig_værdi - reg_beloeb2)
                reg_før_indfas = reg_part1 + reg_part2 - bundfradrag
                indfasning_reg_afgift = indfasning * reg_før_indfas
                endelig_reg_afgift = indfasning_reg_afgift - ekstra_bundfradrag
                if endelig_reg_afgift < 0:
                    return afgiftspligtig_værdi
                else: 
                    return afgiftspligtig_værdi + endelig_reg_afgift
            else:
                reg_part2 = part_2 * (reg_beloeb2 - reg_beloeb1)
                reg_part3 = part_3 * (ny_afgiftspligtig_værdi - reg_beloeb2)
                reg_før_indfas = reg_part1 + reg_part2 + reg_part3 - bundfradrag
                indfasning_reg_afgift = indfasning * reg_før_indfas
                endelig_reg_afgift = indfasning_reg_afgift - ekstra_bundfradrag
                if endelig_reg_afgift < 0:
                    return afgiftspligtig_værdi
                else: 
                    return afgiftspligtig_værdi + endelig_reg_afgift

def afgiftspligtig_veardi(dataset):
    goal_seeks = []
    for i in range(0, dataset.shape[0]):
        fuel = dataset.loc[i, 'Fuel']
        price = dataset.loc[i, 'Prices (2015-DKK)']
        if fuel == 'El':
            gs = WIA.GoalSeek(pris_efter_reg_afgift_el, goal = price, x0 = 1000000)
            goal_seeks.append(gs)
        elif fuel == 'Benzin':
            gs = WIA.GoalSeek(pris_efter_reg_afgift_ben, goal = price, x0 = 1000000)
            goal_seeks.append(gs)
        else:
            gs = WIA.GoalSeek(pris_efter_reg_afgift_die, goal = price, x0 = 1000000)
            goal_seeks.append(gs)
    return goal_seeks
