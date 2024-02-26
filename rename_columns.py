import pandas as pd
import os

os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df = pd.read_csv("Tara_Plot.csv")

# New column names for Meso SL
new_column_names = {
    'Sample ID (TARA_barcode#)': 'Sample ID',
    'Age [days] (number of days since the samp...)': 'Age',
    'BG province ([abbreviation] full name (MRG...)_D': 'BG province_D',
    'BG province ([abbreviation] full name (MRG...)_M': 'BG province_M',
    'Bathy depth [m] (at the sampling location and ...)': 'Bathy depth',
    'Chl a [mg/m**3] (in the selected environmental...)': 'Chlorophyll_D',
    'Chl a [mg/m**3] (in the selected environmental...).1': 'Chlorophyll_D_1',
    'Chl a conc [mg/m**2] (at the sampling location and ...)': 'Chlorophyll_M',
    'Cond [mS/cm] (in the selected environmental...)': 'Cond [mS/cm]',
    'D chl m [m] (in the selected environmental...)': 'D chl m',
    'Depth bot [m] (from which this sample was co...)': 'Depth bot',
    'Depth max Brunt Väisälä freq [m] (in the selected environmental...)': 'Depth max Brunt Väisälä',
    'Depth max O2 [m] (in the selected environmental...)': 'Depth max O2',
    'Depth min O2 [m] (in the selected environmental...)': 'Depth min O2',
    'Depth nitracline [m] (in the selected environmental...)': 'Depth nitracline',
    'Depth nominal (from which this sample was co...)': 'Depth nominal',
    'Depth ref [m] (in the selected environmental...)': 'Depth ref',
    'Depth top [m] (from which this sample was co...)': 'Depth top',
    'Distance [km] (from the closest geographic c...)': 'Distance',
    'FEve (originally reported as OG.Eve...)': 'FEve',
    'Fe std dev [±] (standard deviation value at a...)': 'Fe std dev',
    'Fe tot [µmol/l] (mean value at a depth of 5 m ...)': 'Fe tot',
    'Fraction lower [µm] (used on board to prepare samp...)': 'Fraction lower',
    'Fraction upper [µm] (used on board to prepare samp...)': 'Fraction upper',
    'Functional richness (originally reported as OG.Ric...)': 'Functional richness',
    'Latitude (of the closest geographic coo...)': 'Latitude (closest geo)',
    'Latitude (of the continental shelf with...)': 'Latitude (continental shelf)',
    'Latitude (of the geographic coordinate ...)': 'Latitude (geo coordinate)',
    'Longitude (of the closest geographic coo...)': 'Longitude (closest geo)',
    'Longitude (of the continental shelf with...)': 'Longitude (continental shelf)',
    'Longitude (of the geographic coordinate ...)': 'Longitude (geo coordinate)',

    'MLD [m] (in the selected environmental...)': 'MLD',
    'MLD [m] (in the selected environmental...).1': 'MLD.1',
    'MLE [1/day] (at the sampling location and ...)': 'MLE_M',
    'MLE [1/day] (indicates the presence of a t...)': 'MLE_D',
    'MP biome (Longhurst (2007))_D': 'Marine biome_D',
    'MP biome (Longhurst (2007))_M': 'Marine biome_M',

    'NO3 std dev [±] (standard deviation value at a...)': 'Nitrate std',
    'NPP C [mg/m**2/day] (at the sampling location and ...)': 'NPP C_M',
    'NPP C [mg/m**2/day] (at the sampling location for ...)': 'NPP C (30)_M',
    'NPP C [mg/m**2/day] (for a period of 30 days aroun...)': 'NPP C (30)_D',
    'NPP C [mg/m**2/day] (for a period of 8 days around...)': 'NPP C (8)_D',
    'O2 [µmol/kg] (in the selected environmental...)': 'Oxygen',
    'O2 [µmol/kg] (in the selected environmental...).1': 'Oxygen.1',

    'PIC [mol/m**3] (at the sampling location for ...)': 'PIC',
    'POC [µg/kg] (at the sampling location for ...)': 'POC',

    'RT [days] (of the water mass at the samp...)': 'RT_M',
    'RT [days] (of the water mass. Values>30 ...)': 'RT_D',
    'S (originally reported as miTAG....)': 'Species richness',
    'SSD [min] (at the sampling location and ...)': 'Sunshine duration_M',
    'SSD [min] (day length)': 'Sunshine duration_D',

    'Sal (in the selected environmental...)': 'Salinity',
    'Sample label (TARA_event-datetime_station#_...)': 'Sample label',
    'Samp mat (TARA_station#_environmental-f...)': 'Sample material',
    'Sample method (short label describing the ta...)': 'Sample method',
    'Sea Ice free period [days] (at the sampling location, sea...)': 'Sea ice free period',
    'Sea ice conc [%] (at the sampling location and ...)': 'Sea ice conc',
    'Sea ice free period end DOY [day] (at the sampling location, sea...)': 'Sea ice free end',
    'Sea ice free period start DOY [day] (at the sampling location, sea...)': 'Sea ice free start',

    'Si(OH)4 [µmol/l] (in the selected environmental...)': 'Silicate',
    'Sigma-theta [kg/m**3] (in the selected environmental...)': 'Sigma-theta',

    'Species div (originally reported as Shanno...)': 'Species div',
    'Species div (originally reported as Shanno...).1': 'Species div.1',
    'Species div (originally reported as Shanno...).2': 'Species div.2',
    'Species div (originally reported as Shanno...).3': 'Species div.3',
    'Species div (originally reported as Shanno...).4': 'Species div.4',
    'Species div (originally reported as Shanno...).5': 'Species div.5',
    'Species div (originally reported as miTAG....)': 'Species miTAG chao',
    'Species div (originally reported as miTAG....).1': 'Species miTAG ace',
    'Species div (originally reported as miTAG....).2': 'Species miTAG shannon',
    'Ssphi sat [%] (at the sampling location for ...)': 'Ssphi sat',

    'TSS [mg/l] (at the sampling location for ...)': 'Total suspended matter',
    'Tpot [°C] (in the selected environmental...)': 'Temperature',
    'Time of day (at the sampling location, dat...)': 'Time of day',

    '[NH4]+ [µmol/l] (mean value at a depth of 5 m ...)': 'Ammonium',
    '[NH4]+ std dev [±] (standard deviation value at a...)': 'Ammonium std',
    '[NO2]- [µmol/l] (in the selected environmental...)': 'Nitrite',
    '[NO2]- [µmol/l] (mean value at a depth of 5 m ...)': 'Nitrite_M',
    '[NO2]- std dev [±] (standard deviation value at a...)': 'Nitrite std_M',
    '[NO3]- + [NO2]- [µmol/l] (in the selected environmental...)': 'Nitrate and Nitrite',
    '[NO3]- [µmol/l] (in the selected environmental...)': 'Nitrate_D',
    '[NO3]- [µmol/l] (mean value at a depth of 5 m ...)': 'Nitrate_M',
    '[PO4]3- [µmol/l] (in the selected environmental...)': 'Phosphate',

    'bac660 [1/m] (in the selected environmental...)': 'bac660',
    'bacp [1/m] (in the selected environmental...)': 'bacp',
    'bb470 [1/m] (in the selected environmental...)': 'bb470',
    'bbp470 [1/m] (in the selected environmental...)': 'bbp470',
    'beta470 [m/sr] (in the selected environmental...)': 'beta470',
    'beta470 [m/sr] (in the selected environmental...).1': 'beta470.1',
    'beta470 [m/sr] (in the selected environmental...).2': 'beta470.2',

    "v [cm/s] (Calculated (d'Ovidio et al. 2...)": 'v_D',
    'v [cm/s] (at the sampling location and ...)': 'v_M',
    'wFDc (originally reported as miTAG....)': 'Functional richness'
}

# Rename the columns
df = df.rename(columns=new_column_names)

# Sort all columns (but Sample ID) alphabetically
columns_to_sort = sorted(
    [col for col in df.columns if col not in ['Sample ID']])

# Reorder the columns
desired_columns = ['Sample ID'] + columns_to_sort

# Create a new dataframe with the desired column order, sorted alphabetically
df = df[desired_columns]


df.to_csv("Tara_Cleaned.csv", index=False)
