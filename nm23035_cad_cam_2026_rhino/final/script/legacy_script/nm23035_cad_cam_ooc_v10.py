"""nm23035_cad_cam_v1
εργασία συστημάτων cad/cam Drizis Athanasios nm23035
η εργασία γράφεται στο vs code και στη συνέχεια κάνει run στο script editor του rhino 8,
κατ αυτό το τρόπο κάνοντας bypass το περιβάλλον του grasshopper
σκοπός του παρακάτω script είναι η αυτόματη σχεδίαση της γεωμετρίας της γάστρας
και ο υπολογισμός των απαιτούμενων μεγεθών (βλέπε εκφώνηση), τα inputs θα είναι το πλήθος
γραμμάτων του ονόματος σας και το τελευταίο ψηφίο του αριθμού μητρώου
καλή μου τύχη"""

#NOTE FOR V2!!!
"""
noticing that in order to create the lists with the points (fob, fos, prof, offset etc)
i use very similar functions i will create a more broad one that will use an index input in order to know 
by which value (x y or z) the script must sort
in order to get the stations i will create an extra function that will take as input the output of the 
previously mentioned
"""
#NOTE FOR V3!!!
"""
having issues with the sorting of the points of the profile (i was getting a weird line because i was sorti
the points of the profile with ascending x value), i will sort for the first lbp/2 by descending z value and then
for the rest (front) lpb/2 i will sort by ascending 
"""
#NOTE FOR V5!!!
"""
when increasing the sample number the bending energy function outputs a bigger number
with v5 i will start by trying to fix this problem
"""
#NOTE FOR V6!!!
"""
in v6 i finish all of the station curves, respecting the hull limits, adding 
ghost points on the fos,fob,profile to try to have g2 continuity
g1 and g0 is achieved with the ghost points, also the stations are broken into 
segments in the aft and fore due to the complex geometry
"""
#NOTE FOR V7!!!
"""
starting the fair process
"""
#NOTE FOR V8!!!
"""
redid it but object oriented
"""
#NOTE FOR V9!!!
"""
continue the object oriented script
"""

#libraries
import rhinoscriptsyntax as rs
import math
import Rhino.Geometry as rg
import Rhino

#cleanup section
rs.EnableRedraw(False)
all_objs = rs.AllObjects()
if all_objs:
    rs.DeleteObjects(all_objs)
rs.EnableRedraw(True)

#input the dimensionless offsets from the text file given
offsets_nodim = """0.9766637367774244,0.05528901508730388,0.15702477034318776
0.9766637367774244,0.09051118511095542,0.2493988985720605
0.9766637367774244,0.0960213376349871,0.3565819647890076
0.9766637367774244,0.06074014241064569,0.44762207452876235
0.9766637367774244,0,0.4921218525552037
0.9766637367774244,0,0.9444771653402978
0.9766637367774244,0.014508362239383473,0.948167615100377
0.9766637367774244,0.02801116506368917,0.9575191076635652
0.9766637367774244,0.040470924337018654,0.9700639181813469
0.9766637367774244,0.05204917633093971,0.9846044408382192
0.9766637367774244,0.06318879739349444,0.9999999999999996
0.9657385976573585,0.057303404232722566,0.07274197993625428
0.9657385976573585,0.10262665289515636,0.14419091168121487
0.9657385976573585,0.14130220803519924,0.22029479699558574
0.9657385976573585,0.15633723570367838,0.3174694172124314
0.9657385976573585,0.1439542679921686,0.41552287677452193
0.9657385976573585,0.10610949209049621,0.4953379552621984
0.9657385976573585,0.06197454356404484,0.5668624485211804
0.9657385976573585,0.0590331618182266,0.6653217328803275
0.9657385976573585,0.06947894912187025,0.7609338635295815
0.9657385976573585,0.10532143904375914,0.844012230234192
0.9657385976573585,0.14422799018336355,0.923505081028086
0.9657385976573585,0.1854563847236857,0.9999999999999989
0.984092831379069,0.030477835515591332,0.2539294315922386
0.984092831379069,0.04058130982976711,0.3171124402918214
0.984092831379069,0.031743027259794145,0.38019136198301456
0.9438883194172262,0.08447882873534521,0.022942029859449455
0.9438883194172262,0.15478087854748646,0.08622699251773716
0.9438883194172262,0.21592326895066918,0.16147004994610592
0.9438883194172262,0.24102576589365102,0.27734900415621055
0.9438883194172262,0.2513331233836358,0.40265202499607894
0.9438883194172262,0.230329245145835,0.5255700934774266
0.9438883194172262,0.2268189324146305,0.6518705191575966
0.9438883194172262,0.250069549358842,0.7736509732527899
0.9438883194172262,0.28375084742312884,0.889282767981093
0.9438883194172262,0.32346391618814485,1.0000000000000002
0.9220380411770944,0.13965112847995353,0.015385645240674024
0.9220380411770944,0.2168220568613939,0.05813549900221324
0.9220380411770944,0.2828773585180177,0.13383432761991768
0.9220380411770944,0.32436096503420175,0.24513412020065412
0.9220380411770944,0.3370521373210842,0.37334859874437026
0.9220380411770944,0.3287410471994801,0.5029336459585899
0.9220380411770944,0.3298305881253386,0.6329663394444233
0.9220380411770944,0.34977048874585637,0.7592199292897073
0.9220380411770944,0.3792686946357171,0.8808098784587614
0.9220380411770944,0.41245952576241385,0.9999999999999999
0.900187762936962,0.20166867784760137,0.01376132315657797
0.900187762936962,0.2786641607167325,0.053797066172863554
0.900187762936962,0.34457721839497246,0.12772758306099274
0.900187762936962,0.3745328971510266,0.23833228480941576
0.900187762936962,0.39721247843944973,0.3657844745339545
0.900187762936962,0.39597615178716994,0.4950039434511852
0.900187762936962,0.4003184023604339,0.623922170254401
0.900187762936962,0.41675500470960986,0.7504475698126934
0.900187762936962,0.43874216498142793,0.874879573109195
0.900187762936962,0.4591149620427457,1.0000000000000002
0.8564872064566977,0.3212069976329856,0.01571193368268258
0.8564872064566977,0.39129722542891154,0.06442743834424455
0.8564872064566977,0.44349216305866246,0.15237368555487443
0.8564872064566977,0.46138058459698816,0.2682919449383453
0.8564872064566977,0.4726445184662236,0.3900961575668337
0.8564872064566977,0.47469822624170743,0.512335666664844
0.8564872064566977,0.48048306647792055,0.6342735743914006
0.8564872064566977,0.4886716836647107,0.7558636696557315
0.8564872064566977,0.4943388678354715,0.8778129993696635
0.8564872064566977,0.49734135927639395,0.9999999999999998
0.834636928216566,0.3690604224265437,0.017590326304058827
0.834636928216566,0.4316563205200214,0.072136469836227
0.834636928216566,0.47182424461141476,0.16535174175390344
0.834636928216566,0.48350006081681607,0.2767280445584355
0.834636928216566,0.4915534493443641,0.39082830686217296
0.834636928216566,0.4935407321957106,0.5051275341908472
0.834636928216566,0.4966777396528081,0.6193575935342068
0.834636928216566,0.49880941370051046,0.7336500431509381
0.834636928216566,0.4997132293052681,0.8479843330761776
0.8127866499764336,0.41084180092963685,0.021407012362137275
0.8127866499764336,0.46553532854305996,0.08860425639569054
0.8127866499764336,0.49160202466913405,0.19063245650645225
0.8127866499764336,0.4965640916593844,0.3012342336207469
0.8127866499764336,0.49951746610800607,0.4124117977421518
0.7909363717363014,0.437474862400838,0.02328236674216433
0.7909363717363014,0.482041994314705,0.09094376796244485
0.7909363717363014,0.4963183277983124,0.18615058322748118
0.76908609349617,0.4452920849668605,0.012239051865635038
0.76908609349617,0.47814149075253765,0.051414348855509294
0.76908609349617,0.4958505608205351,0.11056030538436341
0.7472358152560371,0.453125582143835,0.009020786419272498
0.7472358152560371,0.4790624580920608,0.03560085712634094
0.7472358152560371,0.4952933864968804,0.0773477130817408
0.7253855370159052,0.45868886607725673,0.007726980642445905
0.7253855370159052,0.48057198499885195,0.029285107263303543
0.7253855370159052,0.4952598243786984,0.06283854619657739
0.33430925707402104,0.45611744056367987,0.009215240256350109
0.33430925707402104,0.48287902470969396,0.04109997292411474
0.33430925707402104,0.4969588173349733,0.08971010286657335
0.29060870059375693,0.4240716337345114,0.011482943405142844
0.29060870059375693,0.4710393959126639,0.062271229609420116
0.29060870059375693,0.49488924191972095,0.14481852498183712
0.24690814411349266,0.35932199036432433,0.01988215102668823
0.24690814411349266,0.443752176286321,0.0829208585641827
0.24690814411349266,0.49070083904306644,0.20985293562549825
0.20320758763322855,0.2336170118102292,0.01388513587579399
0.20320758763322855,0.32111444773045417,0.05002097715454956
0.20320758763322855,0.3966079734673754,0.1183140631806367
0.20320758763322855,0.4638583206559752,0.2166789625403768
0.20320758763322855,0.493471935786405,0.3521413546166485
0.15950703115296422,0.14723203063853227,0.019272190990369715
0.15950703115296422,0.21279258565737758,0.0640733007302125
0.15950703115296422,0.27865260396222963,0.10781143895683735
0.15950703115296422,0.3445700567619275,0.15192236035478388
0.15950703115296422,0.40359871793327057,0.21558156806487147
0.15950703115296422,0.4455625706633687,0.302711102446027
0.15950703115296422,0.48079084590885857,0.40295251549990796
0.15950703115296422,0.49540413002709954,0.5140454893876906
0.11580647467270005,0.09197914652689991,0.028844505176862146
0.11580647467270005,0.13302223929391582,0.0821316047005757
0.11580647467270005,0.1723362145093909,0.1387556235044488
0.11580647467270005,0.2179070835343051,0.18155832128917032
0.11580647467270005,0.2672689945905352,0.21238526680491035
0.11580647467270005,0.31642619521029647,0.2496457166674334
0.11580647467270005,0.3631083488810822,0.2839235220654138
0.11580647467270005,0.40372072625990746,0.3379512622507417
0.11580647467270005,0.42964023519716316,0.40799946137116655
0.11580647467270005,0.46067438956600526,0.47942724193641134
0.11580647467270005,0.47737594375761383,0.5604620686306487
0.11580647467270005,0.49095729472349636,0.6408688326633252
0.11580647467270005,0.4973173658755653,0.7247009650258034
0.08303105731250196,0.07426295965334172,0.044587556832414596
0.08303105731250196,0.0978595553687547,0.13465210629762453
0.08303105731250196,0.11886702125344603,0.226443403527076
0.08303105731250196,0.1728869926599818,0.27331260268787055
0.08303105731250196,0.2330074241005382,0.2990797601341981
0.08303105731250196,0.29172756373361286,0.33190319044598543
0.08303105731250196,0.3470892658038844,0.37701455999678674
0.08303105731250196,0.38903011525442677,0.44304808545715657
0.08303105731250196,0.43250959408508993,0.5188260020959331
0.08303105731250196,0.45466601024563535,0.6096228969036344
0.08303105731250196,0.4756890450489168,0.7038650979224745
0.08303105731250196,0.4846021882030844,0.801979075756907
0.08303105731250196,0.4892835697732461,0.9008833306823312
0.08303105731250196,0.4915721106251062,0.9999999999999999
0.061180779072369865,0.06120786738235088,0.04698399566594247
0.061180779072369865,0.06989555377827039,0.1395959425684545
0.061180779072369865,0.0552304609832807,0.23332273228992556
0.061180779072369865,0.07694079862740513,0.317491746903384
0.061180779072369865,0.1353550980367487,0.3407643924962288
0.061180779072369865,0.19565700341428222,0.35118174009846653
0.061180779072369865,0.254222368556999,0.3763110738302669
0.061180779072369865,0.306477501336405,0.42479491006611053
0.061180779072369865,0.35949479135230156,0.4702887638909538
0.061180779072369865,0.39859404284040595,0.5451377439960102
0.061180779072369865,0.4347015248523833,0.6201735177136964
0.061180779072369865,0.45408859169136323,0.7115907743995569
0.061180779072369865,0.46095557512980406,0.8081913125188467
0.061180779072369865,0.46872699564462517,0.9033737868008113
0.061180779072369865,0.4710324511802206,0.9999999999999999
0.03933050083223777,0.0366314731014845,0.0892486003777022
0.03933050083223777,0.0355840467198406,0.17652011937066445
0.03933050083223777,0.016699967754488645,0.26133788766635513
0.03933050083223777,0.01584805915883131,0.350139266616151
0.03933050083223777,0.062131214614468216,0.3953913439158369
0.03933050083223777,0.1183911839623078,0.40356204484141717
0.03933050083223777,0.1744921727028037,0.4144484579156033
0.03933050083223777,0.22950371919736248,0.4391673762252524
0.03933050083223777,0.28219221689457186,0.46744095100907496
0.03933050083223777,0.32703185279719044,0.5161326540079547
0.03933050083223777,0.3725971094748415,0.5737613593237588
0.03933050083223777,0.39962044614654213,0.6504724372123114
0.03933050083223777,0.42537489814761226,0.7312061637002502
0.03933050083223777,0.4343625131981037,0.8200138168535163
0.03933050083223777,0.4373882124177008,0.9099446716756776
0.03933050083223777,0.43847643954913684,0.9999999999999999
0.028405361712171718,0.4195855927522622,0.9999999999999999
0.028405361712171718,0.4179354465541996,0.8941318312734445
0.028405361712171718,0.4130135748537329,0.7885376996209136
0.028405361712171718,0.3912949865838323,0.6888229150323464
0.028405361712171718,0.36034399378756865,0.5980630883385427
0.028405361712171718,0.30699306332798887,0.5350851862800428
0.028405361712171718,0.2501951356264528,0.4828282360288595
0.028405361712171718,0.18642453767662379,0.4533511910667879
0.028405361712171718,0.12084598651520263,0.4360576414238323
0.028405361712171718,0.055042827900927044,0.4209917970442904
0.028405361712171718,0.028930162400285706,0.4121971808048702
0.028405361712171718,0.006998799074228983,0.39535041388488784
0.028405361712171718,0,0.3744708321552827
0.028405361712171718,0,0.26207888310336264
0.028405361712171718,0.0049371767053317485,0.22846726100694473
0.028405361712171718,0.01613942246605259,0.19859488983768764
0.028405361712171718,0.022887853368678164,0.16606146370499492
0.028405361712171718,0.012644901487904,0.13586548553939495
0.01748022259210582,0.102993996940385,0.4730234615254965
0.01748022259210582,0.2051211196513269,0.49531127388096524
0.01748022259210582,0.2974600032794048,0.5604078753521162
0.01748022259210582,0.37174939599382656,0.6758422427624106
0.01748022259210582,0.39265238118205703,0.8354182186654564
0.01748022259210582,0.397594835520238,0.9999999999999998
"""
profile_nodim = """
-0.015295194768092466,0,0.9999999999999999
-0.015295194768092466,0,0.5743209876543209
-0.006322065658394941,0,0.5451327971480472
0.0026094358191492725,0,0.5143576916810313
0.011525803281306101,0,0.48302759920921234
0.0202333292699971,0,0.43401202256953186
0.027757265130161555,0,0.38395283685327863
0.02949661979011083,0,0.28600093702233503
0.023816803281743983,0,0.20493827160493827
0.023816803281743983,0,0.15061728395061727
0.02799005808853222,0,0.11176361348924684
0.032080876223558395,0,0.0716004392826148
0.03654387990469652,0,0.03710886846584171
0.041519747438229726,0,0.013012414121482749
0.046803295990362946,0,0
0.9513174140188712,0,0
0.9702390189881617,0,0.05233419385253368
0.9836938381498583,0,0.2057806035503044
0.9847048039504915,0,0.31383838997016045
0.9839707087606958,0,0.4224199334191785
0.9765777767995367,0,0.4927083203553446
0.9703077972008252,0,0.5753079276378199
0.9693046331168973,0,0.7274233465631432
0.9751344692297484,0,0.8952838242314358
0.9783243579236744,0,0.9999999999999999
"""
fob_nodim = """
0.046803295990362946,0,0
0.09488177265125301,0.028027683832017477,0
0.1428521542456544,0.06550664803800504,0
0.19051603573795406,0.11583538799137173,0
0.23574659135046544,0.23453013669994563,0
0.281210083837463,0.3299666068023233,0
0.32844198856824397,0.4176692318477868,0
0.37656769519043654,0.43822070675759456,0
0.7035352587757732,0.43822070675759456,0
0.7676940070709786,0.3833224346649633,0
0.8304677820367412,0.30763407017004424,0
0.8907770082818985,0.14880963808086775,0
0.9513174140188712,0,0
"""
fos_nodim = """
0.09548454408074683,0.5,0.9999999999999999
0.13638003422995,0.5,0.7094890285151072
0.18382797875938509,0.5,0.5567560139364724
0.23136418902844733,0.5,0.3981217141032458
0.2791475293614566,0.5,0.2715582751595531
0.3275238519604749,0.5,0.1551955806815926
0.37656769519043654,0.5,0.09382716049382715
0.7035352587757732,0.5,0.09382716049382715
0.7372772555773166,0.5,0.12538494079161092
0.7704843077100146,0.5,0.18096306030531792
0.799913330085632,0.5,0.3625769543271543
0.8187195353326798,0.5,0.6593005511319927
0.8363695901897498,0.5,0.9999999999999963
"""
transom_nodim = """
-0.015295194768092466,0,0.5743209876543209
-0.015295194768092466,0.0702995111440522,0.5779784992829621
-0.015295194768092466,0.13973318040242405,0.5989892105490435
-0.015295194768092466,0.20749643860103656,0.6236153616028733
-0.015295194768092466,0.2687941392720848,0.6793830693779345
-0.015295194768092466,0.3010183386706564,0.7769813235833926
-0.015295194768092466,0.30938755402225393,0.8880180736299116
-0.015295194768092466,0.3129882207067576,0.9999999999999999
"""


#rhino doesnt allow y=input(x), it freezes or something, so we must use rs.GetString() or rs.GetInteger
number_of_letters = rs.GetInteger("number of letters in first name")
last_number_of_nm = rs.GetInteger("last number of your nm")

#now we calculate lbp, b and d, see assignment, all 3 of them are in meters
L_BP0 = 225
B_HALF0 = 15.9
l_bp = L_BP0 + number_of_letters
b_half = B_HALF0 + (last_number_of_nm/10.0)
d = b_half * 0.62
b_whole = 2 * b_half #this is what will be used for most point functinos, not b_half

def get_limits(profile_data_string, L_scale, B_half, D_scale):
    """
    this function defines the 2 by 3 matrix with the limits of the ship, it takes as input the 
    profile data string in orger to find the minimum value of x, the length of the ship in order
    to get the min x in meters, b/2 to get the y max, and d to get the z max
    """
    if profile_data_string:
        lines = profile_data_string.strip().split('\n')
        min_raw_x = 2
        for line in lines:
            if not line.strip(): continue
            raw_x = float(line.split(",")[0])
            if raw_x < min_raw_x:
                min_raw_x = raw_x
        x_min = min_raw_x * L_scale
        x_max = None
        y_min = 0 
        y_max = B_half
        z_min = 0
        z_max = D_scale
        limits_matrix = [
            [x_min, x_max],  # Row 0: X minimum (Transom), X maximum None
            [y_min, y_max],    # Row 1: Y minimum (Centerline), Y maximum (Flat of Side)
            [z_min, z_max]     # Row 2: Z minimum (Baseline/Keel), Z maximum (Main Deck)
        ]
        return limits_matrix
    
    else:
        raise ValueError("Error: profile_data_string is empty. Cannot determine X_min.")

def get_points_from_data(data_string, L_scale, B_scale, D_scale, curve_type, ship_limits_matrix):
    """
    this is the above mentioned general point function, all raw data will go through this function
    """
    lines = data_string.strip().split('\n')
    all_points = []
    sorting_flag = False #if sorting flag become True then it will run a sorting in the end using the sort index provided 
    station_flag = False #will become true in case of stations
    for line in lines:
        if not line.strip(): continue
        raw_x, raw_y, raw_z = map(float, line.split(","))
        scaled_pt = [raw_x * L_scale, raw_y * B_scale, raw_z * D_scale]
        all_points.append(scaled_pt)

    if curve_type not in {"fob", "fos", "profile", "transom", "station"}:
        raise ValueError(f"Error: 'curve_type' is not a valid curve")
    
    if curve_type == "fob":
        plane = [0,0,1] #this is the vector perpendicular to the plane
        sort_index = 0 #sorts points by x
        sorting_flag = True


    if curve_type in {"profile", "fos"}:
        plane = [0,1,0] #this is the vector perpendicular to the plane
        #we will not define a sort index, due to more complex geometry we will sort the points differently
        if curve_type == "profile":
            aft_part = [p for p in all_points if p[0] < L_scale/2]
            fwd_part = [p for p in all_points if p[0] >= L_scale/2]
            aft_part.sort(key=lambda p: p[2], reverse=True)
            fwd_part.sort(key=lambda p: p[2])
            all_points = aft_part + fwd_part
        else: #in case of fos
            sort_index = 0
            sorting_flag = True
    if curve_type in {"transom", "station"}:
        plane = [1,0,0]
        #if its station we will use again a more complex way to sort 
        if curve_type == "station":
            stations = []
            if not all_points:
                return [] #αποφυγή crash, θα εμφανιστεί απλά IndexError: list index out of range
            all_points.sort(key=lambda p: p[0])
            current_station = [all_points[0]]
            for i in range(1, len(all_points)):
                #σε περίτωση που με τους πολλαπλασιασμούς έχει ξεφύγει κάποιο νούμερο δεν χρησιμοποιώ ισότητα, δέχομαι μια διαφορά στη τιμή του χ εώς 1 εκ, θα το δω και στη πορεία
                if abs(all_points[i][0]- all_points[i-1][0]) < 0.01:
                    current_station.append(all_points[i])
                #εαν η διαφορά είναι μεγαλύτερη της ανοχής,κάνουμε sort τα σημεία του νομέα που μόλις κλείσαμε βάση ύψους και πάμε στον επόμενο νομέα, άρα αλλάζει το current_station
                else:
                    current_station.sort(key=lambda p: p[2])
                    stations.append(current_station)
                    current_station = [all_points[i]]
            #ο τελευταίος νομέας δεν έχει άλλον μετά από αυτόν, επομένως η συνθήκη abs... δε θα λειτουτγήσει
            current_station.sort(key=lambda p: p[2])
            stations.append(current_station)
            station_flag = True
        else: #in case of transom
            sort_index = 2
            sorting_flag = True
    
    if sorting_flag is True: #the simpler lists of points will be sorted here
        all_points.sort(key=lambda p: p[sort_index]) #sort index tells us by which value to sort, 0 is sort by x, 1 is sort by y, 2 is sort by z 
    
    #at this point we have all of our points sorted in a list, remember, the stations list is a list of lists, we have the is_station flag to keep track of that
    if station_flag is True:
        #we unpack the list containing all the stations
        stations_rg_pts = []
        for station_number, curr_station in enumerate(stations):
            curr_station_rg = []
            for pt_index, pt in enumerate(curr_station):
                x_val = pt[0]
                y_val = pt[1]
                z_val = pt[2]
                rg_pt = rg.Point3d(x_val, y_val, z_val)
                curr_station_rg.append((rg_pt, pt_index, ship_limits_matrix, plane, curve_type, station_number, True, False))

            stations_rg_pts.append(curr_station_rg)
        return stations_rg_pts, station_flag
    
    #we convert into rg points for all other cases that are simpler to handle
    if station_flag is False:
        all_rg_pts = []
        for pt_index, pt in enumerate(all_points):
            rg_pt = rg.Point3d(pt[0], pt[1], pt[2])
            all_rg_pts.append((rg_pt, pt_index, ship_limits_matrix, plane, curve_type, None, True, False))
        return all_rg_pts, station_flag

def get_point_objects(point_data, station_flag):
    if point_data:
        if not station_flag:
            point_objects = []
            #create the point objects
            for data_tuple in point_data:
                new_point_object = MyPoint(*data_tuple)
                point_objects.append(new_point_object)

            #link objects with previous and next object
            for i in range(len(point_objects)):
                if i > 0:
                    point_objects[i].prev = point_objects[i-1]
                if i < len(point_objects) - 1:
                    point_objects[i].next = point_objects[i+1]
            return point_objects
        
        else:
            all_station_objects = []
    
            for station_list in point_data:
                current_station_objects = []
                #create objects
                for data_tuple in station_list:
                    new_point_object = MyPoint(*data_tuple)
                    current_station_objects.append(new_point_object)
    
                #link objects with previous and next object
                for i in range(len(current_station_objects)):
                    if i > 0:
                        current_station_objects[i].prev = current_station_objects[i-1]
                    if i < len(current_station_objects) - 1:
                        current_station_objects[i].next = current_station_objects[i+1]
                    
                all_station_objects.append(current_station_objects)
    
        return all_station_objects

def get_trapped_tangent(curve_plane, limit_plane, current_pt, limits):
    pass

# def build_station_segments(all_station_objects, fos_curve, fob_curve,
#                             profile_curve, ship_limits_matrix, station_plane_vector):
#     """
#     For every station list:
#       1. Find intercepts with fos, then fob (fallback: profile).
#       2. Inject intercept points (is_intercept=True) into the point list.
#       3. Discard points outside [z_bottom, z_top].
#       4. Sort by ascending z.
#       5. Return a new list-of-lists of MyCurve objects.
#     """
#     new_station_curves = []

#     for station_list in all_station_objects:
#         if not station_list:
#             continue

#         # all points in this station share the same x
#         station_x    = rs.PointCoordinates(station_list[0].id)[0]
#         station_num  = station_list[0].station_number

# # ── 1. find boundary intercepts ──────────────────────────────────────
#         fos_pt = fos_curve.get_intercept_with_plane(station_x)

#         if fos_pt is None:
#             z_max = ship_limits_matrix[2][1]
#             sorted_pts = sorted(
#                 [rs.PointCoordinates(pt_obj.id) for pt_obj in station_list],
#                 key=lambda c: c[2], reverse=True
#             )
#             top_y = sorted_pts[0][1] if sorted_pts else 0.0
#             fos_pt = rg.Point3d(station_x, top_y, z_max)

#         fob_pt    = fob_curve.get_intercept_with_plane(station_x)
#         bottom_pt = fob_pt if fob_pt is not None \
#                     else profile_curve.get_intercept_with_plane(station_x)

#         if bottom_pt is None:
#             continue   # no bottom boundary — skip silently

#         z_top    = fos_pt.Z
#         z_bottom = bottom_pt.Z

#         if z_top <= z_bottom:
#             continue   # degenerate station — skip

#         # ── 2. filter original points to valid z range ────────────────────────
#         tolerance = 0.001
#         interior_pts = []
#         for pt_obj in station_list:
#             coords = rs.PointCoordinates(pt_obj.id)
#             z = coords[2]
#             if (z_bottom + tolerance) < z < (z_top - tolerance):
#                 interior_pts.append(coords)   # plain [x, y, z] list

#         # ── 3. build data tuples — intercepts first/last ─────────────────────
#         # tuple layout matches what MyPoint.__init__ expects:
#         # (rg_pt, index, limits, plane, pt_type, station_number,
#         #  is_original, is_intercept)

#         def make_intercept_tuple(rg_pt, idx):
#             return (rg_pt, idx, ship_limits_matrix, station_plane_vector,
#                     "station", station_num, False, True)

#         def make_original_tuple(coords, idx):
#             rg_pt = rg.Point3d(coords[0], coords[1], coords[2])
#             return (rg_pt, idx, ship_limits_matrix, station_plane_vector,
#                     "station", station_num, True, False)

#         ordered_tuples = []
#         ordered_tuples.append(make_intercept_tuple(bottom_pt, 0))

#         for i, coords in enumerate(interior_pts, start=1):
#             ordered_tuples.append(make_original_tuple(coords, i))

#         ordered_tuples.append(
#             make_intercept_tuple(fos_pt, len(ordered_tuples))
#         )

#         # sort everything by ascending z (intercepts are already at extremes,
#         # but an explicit sort keeps things safe)
#         ordered_tuples.sort(key=lambda t: t[0].Z)

#         # ── 4. build MyPoint objects and link prev/next ───────────────────────
#         point_objects = [MyPoint(*tup) for tup in ordered_tuples]
#         for i, pt in enumerate(point_objects):
#             if i > 0:
#                 pt.prev = point_objects[i - 1]
#             if i < len(point_objects) - 1:
#                 pt.next = point_objects[i + 1]

#         # ── 5. create the curve ───────────────────────────────────────────────
#         curve = MyCurve(point_objects, ship_limits_matrix, station_plane_vector)
#         new_station_curves.append(curve)

#     return new_station_curves


class MyPoint:
    def __init__(self, rg_pt, index, limits, plane, pt_type, station_number, is_original, is_intercept):
        self.original_coords = rg_pt
        self.limits = limits
        self.index = index
        self.is_original = is_original
        self.pt_type = pt_type
        self.is_intercept = is_intercept
        self.station_number = station_number
        self.plane = plane
        self.id = rs.AddPoint(rg_pt)
        
        self.prev = None
        self.next = None

    @property 
    def distance_from_original_point(self):
        current_pos = rs.PointCoordinates(self.id)
        return rs.Distance(self.original_coords, current_pos)
    
    @property
    def limits_bool_list(self):
        bool_matrix = []
        tolerance = 0.001
        current_pos = rs.PointCoordinates(self.id)
        for j in [0,1,2]:
            row = []
            if self.plane[j] == 1:
                bool_matrix.append([0, 0])
                continue

            for i in [0,1]:
                if self.limits[j][i] is not None:
                    dif = abs(self.limits[j][i] - current_pos[j])
                    if dif <= tolerance:
                        row.append(1)
                    else:
                        row.append(0)
                else: row.append(0) 
            bool_matrix.append(row)
        return bool_matrix
        
    @property
    def is_constrained(self):
        if self.is_intercept:
            return 2
        
        hit_x = any(self.limits_bool_list[0])
        hit_y = any(self.limits_bool_list[1])
        hit_z = any(self.limits_bool_list[2])
        hit_line = any(self.is_line)
        hit_limit_count = int(hit_x) + int(hit_y) + int(hit_z) + int(hit_line)

        if hit_limit_count >= 2:
            return 2 #fixed point
        if hit_limit_count == 1:
            return 1 #one dof
        
        return 0 #free
        
    @property
    def is_line(self):
        line_matrix = [0, 0]
        neighbors = [self.prev, self.next]
        tolerance = 0.001
        current_coords = rs.PointCoordinates(self.id)

        for index, neighbor in enumerate(neighbors):
            if not neighbor:
                continue
            neighbor_coords = rs.PointCoordinates(neighbor.id)
            for axis in range(3):
                if self.plane[axis] == 0:
                    dif = abs(current_coords[axis] - neighbor_coords[axis])
                    if dif <= tolerance:
                        line_matrix[index] = 1
                        break
        return line_matrix
    
    @property
    def is_tangent(self):
        if self.is_line == [1,0] or self.is_line == [0,1]: 
            return True
        if self.is_line == [1, 1]: 
            return False
        if self.limits_bool_list[2][1]: 
            return False
        if any(any(row) for row in self.limits_bool_list): 
            return True
        return False
    

class MyCurve:
    def __init__(self, point_objects, limits, plane_vector, name="curve"):
        self.pts = point_objects
        self.limits = limits
        self.plane = plane_vector
        self.name = name
        
        # This list will hold highly structured dictionaries for every physical segment.
        # Format: {'type': 'LINE' or 'BSPLINE', 'id': rhino_guid, 'points': [MyPoint objects]}
        self.segments = [] 
        self.segment_matrix = []

        self.rebuild()

    def rebuild(self):
        """
        Calculates line vs spline segments and draws them independently.
        Does NOT join them. Keeps them separate for future fairing.
        """
        # Delete old segments if rebuilding
        if self.segments:
            for seg in self.segments:
                if rs.IsObject(seg['id']):
                    rs.DeleteObject(seg['id'])
        
        self.segments = []
        pts = self.pts 
        if len(pts) < 2: return None

        self.segment_matrix = []
        i = 0

        while i < len(pts) - 1:
            type_flag = 1 if pts[i].is_line[1] == 1 else 0
            row = [type_flag, pts[i]]
            while i < len(pts) - 1:
                current_seg_type = 1 if pts[i].is_line[1] == 1 else 0
                if current_seg_type != type_flag:
                    break
                row.append(pts[i+1])
                i += 1
            self.segment_matrix.append(row)

        for row in self.segment_matrix:
            seg_type = row[0] 
            pt_objs = row[1:]
            coords = [rs.PointCoordinates(p.id) for p in pt_objs]

            if seg_type == 1:
                crv_id = rs.AddLine(coords[0], coords[-1])
                t_str = "LINE"
            else:
                crv_id = rs.AddInterpCurve(coords)
                t_str = "BSPLINE"
                
            # Store the independent segment with all its data
            self.segments.append({
                'type': t_str,
                'id': crv_id,
                'points': pt_objs
            })
        
        return self.segments
    
    @property
    def segment_list(self):
        out = ["\n" + "="*30, f"SEGMENT REPORT: {self.name}", "-"*30]
        for idx, seg in enumerate(self.segments):
            ids = [p.index for p in seg['points']]
            out.append("Seg {}: {} | Indices: {}".format(idx, seg['type'], ids))
        out.append("="*30)
        return "\n".join(out)
    
    def get_intercepts_with_plane(self, station_x):
        """
        Returns ALL intersections (sorted by Z) to handle complex sterns.
        """
        if not self.segments:
            return []

        rhino_curves = [seg['id'] for seg in self.segments if rs.IsObject(seg['id'])]
        if not rhino_curves:
            return []

        origin = rg.Point3d(station_x, 0, 0)
        plane  = rg.Plane(origin, rg.Vector3d.XAxis)

        all_pts = []
        for crv_id in rhino_curves:
            rhino_curve = rs.coercecurve(crv_id)
            result = rg.Intersect.Intersection.CurvePlane(rhino_curve, plane, 0.001)
            if result:
                for x in result:
                    all_pts.append(x.PointA)

        all_pts.sort(key=lambda p: p.Z)
        return all_pts


def build_station_segments(all_station_objects, fos_curve, fob_curve, profile_curve, ship_limits_matrix, station_plane_vector):
    """
    Dynamically detects propeller gaps to split stern stations, applies boundary intercepts,
    and returns entirely separate MyCurve objects for disconnected parts.
    """
    new_station_curves = []
    depth = ship_limits_matrix[2][1]

    def make_intercept_tuple(rg_pt, idx, s_num):
        return (rg_pt, idx, ship_limits_matrix, station_plane_vector, "station", s_num, False, True)

    for station_list in all_station_objects:
        if not station_list:
            continue

        station_x = rs.PointCoordinates(station_list[0].id)[0]
        station_num = station_list[0].station_number

        fos_ints = fos_curve.get_intercepts_with_plane(station_x)
        prof_ints = profile_curve.get_intercepts_with_plane(station_x)
        fob_ints = fob_curve.get_intercepts_with_plane(station_x)

        fos_pt = fos_ints[-1] if fos_ints else None

        # 1. SPLIT LOGIC: Detect physical gaps in the offset data (Propeller area)
        groups = []
        current_group = [station_list[0]]
        for i in range(1, len(station_list)):
            p_prev = rs.PointCoordinates(station_list[i-1].id)
            p_curr = rs.PointCoordinates(station_list[i].id)
            
            # If Z jumps significantly (> 5% of ship depth), the station is split in two!
            if (p_curr[2] - p_prev[2]) > (depth * 0.05):
                groups.append(current_group)
                current_group = [station_list[i]]
            else:
                current_group.append(station_list[i])
        groups.append(current_group)

        # 2. CAP AND BUILD EACH GROUP INDEPENDENTLY
        for idx, grp in enumerate(groups):
            b_pt = None
            t_pt = None

            # Bottom cap logic
            if idx == 0:
                b_pt = fob_ints[0] if fob_ints else (prof_ints[0] if prof_ints else None)
            elif len(prof_ints) > 1:
                # Upper hull starts at the overhang profile intercept
                b_pt = prof_ints[-1]

            # Top cap logic
            if idx == len(groups) - 1:
                t_pt = fos_pt
            elif len(prof_ints) > 1:
                # Lower skeg ends at the skeg profile intercept
                t_pt = prof_ints[1] 

            # Build the new point tuple list for this specific group
            ordered_tuples = []
            if b_pt: ordered_tuples.append(make_intercept_tuple(b_pt, 0, station_num))
            
            for p_obj in grp:
                coords = rs.PointCoordinates(p_obj.id)
                rg_pt = rg.Point3d(coords[0], coords[1], coords[2])
                ordered_tuples.append((rg_pt, p_obj.index, ship_limits_matrix, station_plane_vector, "station", station_num, True, False))
                
            if t_pt: ordered_tuples.append(make_intercept_tuple(t_pt, len(ordered_tuples), station_num))

            # Instantiate final linked points
            point_objects = [MyPoint(*tup) for tup in ordered_tuples]
            for i, pt in enumerate(point_objects):
                if i > 0: pt.prev = point_objects[i - 1]
                if i < len(point_objects) - 1: pt.next = point_objects[i + 1]

            # Create an independent curve (Even if a station is split, they remain separate curves)
            curve_name = f"Station_{station_num}_Part_{idx}"
            curve = MyCurve(point_objects, ship_limits_matrix, station_plane_vector, curve_name)
            new_station_curves.append(curve)

    return new_station_curves

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

ship_limits_matrix = get_limits(profile_nodim, l_bp, b_half, d)

# 1. Profile
profile_plane_vector = [0,1,0]
profile_data_tuples, profile_is_station = get_points_from_data(profile_nodim, l_bp, b_whole, d, "profile", ship_limits_matrix)
my_profile_point_objects = get_point_objects(profile_data_tuples, profile_is_station)
my_profile_curve_object = MyCurve(my_profile_point_objects, ship_limits_matrix, profile_plane_vector, "Profile")

# 2. Flat of Side
fos_plane_vector = [0,1,0]
fos_data_tuples, fos_is_station = get_points_from_data(fos_nodim, l_bp, b_whole, d, "fos", ship_limits_matrix)
my_fos_point_objects = get_point_objects(fos_data_tuples, fos_is_station)
my_fos_curve_object = MyCurve(my_fos_point_objects, ship_limits_matrix, fos_plane_vector, "FOS")

# 3. Transom
transom_plane_vector = [1, 0, 0]
transom_data_tuples, transom_is_station = get_points_from_data(transom_nodim, l_bp, b_whole, d, "transom", ship_limits_matrix)
my_transom_point_objects = get_point_objects(transom_data_tuples, transom_is_station)
my_transom_curve_object = MyCurve(my_transom_point_objects, ship_limits_matrix, transom_plane_vector, "Transom")

# 4. Flat of Bottom
fob_plane_vector = [0, 0, 1]
fob_data_tuples, fob_is_station = get_points_from_data(fob_nodim, l_bp, b_whole, d, "fob", ship_limits_matrix)
my_fob_point_objects = get_point_objects(fob_data_tuples, fob_is_station)
my_fob_curve_object = MyCurve(my_fob_point_objects, ship_limits_matrix, fob_plane_vector, "FOB")

# 5. Stations (Dynamically Split)
station_plane_vector = [1, 0, 0]
station_data_tuples, station_is_station = get_points_from_data(offsets_nodim, l_bp, b_whole, d, "station", ship_limits_matrix)
my_station_point_objects = get_point_objects(station_data_tuples, station_is_station)

my_station_curves = build_station_segments(
    my_station_point_objects,
    my_fos_curve_object,
    my_fob_curve_object,
    my_profile_curve_object,
    ship_limits_matrix,
    station_plane_vector
)