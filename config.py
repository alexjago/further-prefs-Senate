# N-Party-Preferred configuration
# You'll need to modify most of these values; hopefully it's straightforward.

# This is the 2016 format. Other years will likely differ.
YEAR = 2016

# Which states and territories would we like to analyse?
STATES = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']

# Which parties would we like to analyse as our first pref?
# (NB double-layer list to accommodate differing acronyms; the first successful one will be used.)
FIRSTS = [['Grn'], ['Lab']]

# For which (other) parties would we like to see further prefs?
# (NB double-layer list to accommodate differing acronyms; the first successful one will be used.)
FURTHERS = [['Grn'], ['Lab'], ['Lib', 'Lnp', 'Clp']]

### How many parties do we care about and where are those parties' candidates?
# Numbers are as follows: Group A Ticket, Group B Ticket, ... , final Ticket,
#   Group A Candidate 1, Group A Candidate 2, ... , final Ungrouped Candidate

# Included and commented out are nPP sets for 2016's winning parties. I've ordered
# them left to right. Hopefully the acronyms make sense - you can change them.

TICKETS = {
    'ACT' : {
       'Grn' : [8, 25, 26],
       'Lab' : [3, 15, 16],
       'Lib' : [6, 21, 22]
   },
    'NSW' : {
        'Grn' : [38, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166],
        'Lab' : [14, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95],
        'Ldp' : [4, 50, 51],
        'Lnp' : [6, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65],
        'Phn' : [19, 105, 106, 107]
    },
    'NT' : {
        'Grn' : [4, 14, 15],
        'Lab' : [6, 18, 19],
        'Clp' : [5, 16, 17]
    },
    'QLD' : {
         'Grn' : [37, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139],
         'Lab' : [4, 45, 46, 47, 48, 49, 50],
         'Lnp' : [7, 55, 56, 57, 58, 59, 60, 61, 62],
         'Phn' : [24, 99, 100, 101, 102]
     },
    'SA' : {
        'Grn' : [4, 34, 35, 36, 37],
        'Lab' : [2, 26, 27, 28, 29, 30, 31],
        'Nxt' : [6, 40, 41, 42, 43],
        'Lib' : [8, 46, 47, 48, 49, 50, 51],
        'Ffp' : [14, 62, 63]
    },
    'TAS' : {
        'Grn' : [3, 30, 31, 32],
        'Lab' : [2, 24, 25, 26, 27, 28, 29],
        'Jln' : [13, 56, 57, 58],
        'Lib' : [6, 37, 38, 39, 40, 41, 42]
    },
    'VIC' : {
        'Grn' : [37, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136],
        'Lab' : [4, 45, 46, 47, 48, 49, 50, 51, 52],
        'Dhj' : [1, 39, 40],
        'Lnp' : [32, 110, 111, 112, 113, 114, 115, 116]
    },
    'WA' : {
        'Grn' : [10, 54, 55, 56, 57, 58, 59],
        'Lab' : [4, 35, 36, 37, 38, 39, 40, 41],
        'Lib' : [24, 87, 88, 89, 90, 91, 92, 93],
        'Phn' : [18, 74, 85, 76]
    }
}

# This lets us know how many ATL tickets there are
ATLs = {
    'ACT' : 10,
    'NSW' : 41,
    'NT' : 7,
    'QLD' : 38,
    'SA' : 23,
    'TAS' : 21,
    'VIC' : 38,
    'WA' : 28
    }
    

### Paths to input spreadsheets ###

# The giant spreadsheets of formal preferences (one per state/territory)

FORMAL_PREFS_PATHS = {
    'ACT' : "/mnt/Narnia/Psephology/Results/AUS_2016/aec-senate-formalpreferences-20499-ACT.csv",
    'NSW' : "/mnt/Narnia/Psephology/Results/AUS_2016/aec-senate-formalpreferences-20499-NSW.csv",
    'NT' : "/mnt/Narnia/Psephology/Results/AUS_2016/aec-senate-formalpreferences-20499-NT.csv",
    'QLD' : "/mnt/Narnia/Psephology/Results/AUS_2016/aec-senate-formalpreferences-20499-QLD.csv",
    'SA' : "/mnt/Narnia/Psephology/Results/AUS_2016/aec-senate-formalpreferences-20499-SA.csv",
    'TAS' : "/mnt/Narnia/Psephology/Results/AUS_2016/aec-senate-formalpreferences-20499-TAS.csv",
    'VIC' : "/mnt/Narnia/Psephology/Results/AUS_2016/aec-senate-formalpreferences-20499-VIC.csv",
    'WA' : "/mnt/Narnia/Psephology/Results/AUS_2016/aec-senate-formalpreferences-20499-WA.csv"
}

# The relatively tiny spreadsheet detailing all the polling places (nationwide)
POLLING_PLACES_PATH = "/mnt/Narnia/Psephology/Results/AUS_2016/GeneralPollingPlacesDownload-20499.csv"

### Paths to output spreadsheets

# If blank, current directory
OUTPUTDIR = ""

# If you modify the below items, filenames won't match the README...

# This spreadsheet details NPP preferences by booth
# Will go in OUTPUTDIR/STATE/ ...
NPP_BOOTHS_FN = "NPP_Booths.csv"

# What version of this CFG format?
CFG_VERSION = 2
