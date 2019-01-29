# We want to analyse ballots based on several factors:
# (0) In which State were they cast?
# (1) Did they have a first preference for our selected ticket?
# (2) What was the later-preference order for certain other selected tickets?

import csv
from collections import defaultdict
import itertools
import os, os.path
import sys

from config import *


for STATE in STATES:

    FIRSTP = []
    firsty = ''

    for fbox in FIRSTS:
        for f in fbox:
            if f in TICKETS[STATE]:
                FIRSTP = TICKETS[STATE][f]
                firsty = f
                continue

        # this just refers to further prefs
        PARTIES = {}

        for nbox in FURTHERS:
            for n in nbox:
                if n == firsty:
                    print("Skipping "+n+" from furthers list because it's also the first pref", file=sys.stderr)
                    continue
                if n in TICKETS[STATE]:
                    PARTIES[n] = TICKETS[STATE][n]
                    continue
                
        print(STATE, "First pref:", {firsty : FIRSTP}, "Further prefs:", PARTIES, sep='\n')


        # Generate booth data structure (combinations hardcoded):
        fieldnames = ["ID", "Division", "Booth", "Latitude", "Longitude"]
        combinations = ["Not "+firsty+" 1", "Exhaust"] # special-casing the empties


        for r in range(len(PARTIES)):
            chooseN = list(itertools.combinations(sorted(PARTIES), r+1))
            for i in chooseN:
                combinations += ["".join(j) for j in list(itertools.permutations(i))]

        total_combos = len(combinations)

        ################################

        # Iterate over booth metadata

        booths = {}
        divisionOrdTotals = {}
        divisionSpecials = {}
        PPIds = {}

        boothfieldnames = ['State','DivisionID','DivisionNm','PollingPlaceID','PollingPlaceTypeID','PollingPlaceNm',
                           'PremisesNm','PremisesAddress1','PremisesAddress2','PremisesAddress3','PremisesSuburb',
                           'PremisesStateAb','PremisesPostCode','Latitude','Longitude']

        with open(POLLING_PLACES_PATH) as boothscsv:
            boothsreader = csv.DictReader(boothscsv, fieldnames=boothfieldnames)

            for boothrow in boothsreader:
        ##        print(boothrow)
                if(boothrow['State'] == STATE):
                    booths[boothrow['DivisionNm'] + boothrow['PollingPlaceNm']] = [boothrow['PollingPlaceID'],
                                                                                   boothrow['DivisionNm'], boothrow['PollingPlaceNm'],
                                                                                   boothrow['Latitude'], boothrow['Longitude']] + [0]*(total_combos)

        #with open(newpollingplacesfn, 'w') as fp:
        #    print(*fieldnames, sep=',', file=fp, flush=True)    

        print("*** Distributing Preferences from: "+firsty+" in: "+STATE+" ***", file=sys.stderr)

        # Iterate over prefs
        with open(FORMAL_PREFS_PATHS[STATE], newline='') as prefscsv:

            allrows = [row for row in prefscsv]
            
            prefsreader = csv.DictReader(allrows)

            progress = 0
            total_firsts = 0
            
            # Iterate over all the rows of the main thing
            for prefrow in prefsreader:

                progress += 1

##                if progress > 30:
##                    break

##                if examples > 10:
##                    break

                if (progress % 100000 == 0):
                    print("Preferencing:\t", progress, file=sys.stderr)
        ##            break

                divnm = str(prefrow['ElectorateNm'])
                boothnm = str(prefrow['VoteCollectionPointNm'])

                if divnm[0] == '-':
                    progress -= 1
                    continue
                
                seq = str(prefrow['Preferences']).split(',')

                # Need to convert all to ints and fill in empties

                seq_ints = [len(seq)+1] * len(seq)
                
                for i in range(len(seq)):
                    if seq[i].isnumeric():
                        seq_ints[i] = int(seq[i])
                    ## Follow dividebatur
                    if seq[i] == '*' or seq[i] == '/':
                        seq_ints[i] = 1

                #print(seq_ints)

                #Iterate over pref sequence.

                # But first, first-pref testing
                
                # Formality rules: 
                #     if both and BTL is formal (regardless of ATL), use BTL
                #     if both and only ATL is formal, use ATL
                # Very occasionally the BTL *and* ATL will be valid, with the BTL having a 1st pref of a different party to the ATL

                atl_valid = False
                btl_valid = False
                # ^^ at least one of these will be true
                
                is_firstpref = False
                pref = ''
                
                # first test ATL & BTL formality
                # ATL Formal iff there's one and only one 1st pref
                atl_valid = (seq_ints[0:ATLs[STATE]].count(1) == 1)

                # BTL formal iff there are one and only one of 1st through 6th prefs
                btl_valid = True
                for i in range(1,6+1):
                    btl_valid &= (seq_ints[ATLs[STATE]:].count(i) == 1)
                    
                # If both ATL and BTL are valid, BTL overrides
                if btl_valid:
                    for cand in FIRSTP[1:]:
                        if seq_ints[cand-1] == 1:
                            is_firstpref = True
                            break
                elif atl_valid: ## (and implicitly, not btl_valid)
                    if seq_ints[FIRSTP[0]-1] == 1:
                        is_firstpref = True
                else:
                    print("This shouldn't happen! Neither ATL nor BTL valid!", seq, sep='\n', file=sys.stderr)


                if is_firstpref:
                    total_firsts += 1
                    # Now to analyse further Party-Preferred. We categorise the preference sequence by its highest value for each group of candidates

##                    if divnm == 'Canberra' and boothnm.startswith('Isabella'):
##                        # print(divnm, boothnm, "selected for", firsty) #not every time
##                        print(*seq_ints, sep=',')

                    best = {}

                    for p in PARTIES:
                        best[p] = len(seq) + 2
                        for cand in PARTIES[p]:
                            if seq_ints[cand-1] < best[p]:
                                best[p] = seq_ints[cand-1]

                    order = sorted([(best[i], i) for i in PARTIES])
                    
                    # Now we test. Exploit the requirements of optional preferential:
                    #    items may only be ranked equal-last.

                    pref = "".join([i[1] for i in order if i[0] < (len(seq)+1)])

                    if pref == "":
                        pref = "Exhaust"

                else: # not is_firstpref
                    pref = "Not "+firsty+" 1"

                try:
                    booths[divnm+boothnm][5 + combinations.index(pref)] += 1
                except KeyError:
                    booths[divnm+boothnm] = ['', divnm, boothnm, '', ''] + [0] * (total_combos)
                    booths[divnm+boothnm][5 + combinations.index(pref)] += 1
                    
            # end row-by-row agg
        print("*** Aggregating Absents/Postals/Prepolls/Provisionals from: "+firsty+" in: "+STATE+" ***", file=sys.stderr)

        which = {"ABSENT" : "Absent", "POSTAL" : "Postal", "PRE_POLL" : "Pre-Poll", "PROVISIONAL" : "Provisional"}

        whichkeys = list(which.keys())
        boothkeys = list(booths.keys())

        toRemove = []

        for i in boothkeys:
            if booths[i][0] == '': # missing ID
                for w in whichkeys:
                    if booths[i][2].startswith(w):
                        try:
                            for j in range(5, len(booths[i])):
                                divisionSpecials[booths[i][1]+which[w]][j] += booths[i][j]
                        except KeyError:
                            divisionSpecials[booths[i][1]+which[w]] = booths[i][0:2] + [which[w]] + booths[i][3:]
                        toRemove.append(i)

        for i in toRemove:
            booths.pop(i)

        # print(divisionSpecials)

        booths.update(divisionSpecials)

        ### Sum over booths to generate totals column

        boothkeys = list(booths.keys()) #regen

        for i in boothkeys:
            booths[i].append(sum([int(j) for j in booths[i][5:]]))

        print("*** Writing File ***", file=sys.stderr)
##
        npp_fn = os.path.join(OUTPUTDIR, STATE, firsty+"_"+NPP_BOOTHS_FN)
        print("Output filename:", npp_fn, file=sys.stderr)

        try:
            os.makedirs(os.path.join(OUTPUTDIR, STATE))
        except FileExistsError:
            pass # sweet, nothing to do

        title_msg = "Senate analysis for "+str(YEAR)+" in "+STATE+" looking at further prefs for "+" ".join(PARTIES)+" given a first pref for "+firsty

        with open(npp_fn, 'w') as fp:
            print(title_msg, file=fp, flush=True)
            print(*(fieldnames + combinations + ["Total"]), sep=',', file=fp, flush=True)

            for ids in booths.keys():
                
                print(*booths[ids], sep=',', file=fp)
        print("total first preferences for", firsty+":", total_firsts)
    # end of the loop over parties
# end of the loop over states

print("*** Done! ***", file=sys.stderr)


        
            
        

                        

