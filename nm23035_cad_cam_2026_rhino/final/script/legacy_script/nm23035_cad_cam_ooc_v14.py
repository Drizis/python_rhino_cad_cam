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
#NOTE FOR V12!!!
"""
v10-v11 were major failures, we continue with v12, in v12 i fixed the tangent condition on the limits of the curve, also i saw that some stations get confused because they have a final point that is not part of the profile curve
now all stations end in a curve or a zmax limit, thus there are no holes in the ships geometry, i did this by ignoring very close original points that are very close to intercept points, this is a very trashy fix, but if it works it works. (for now)

"""

#libraries
import rhinoscriptsyntax as rs
import math
import Rhino.Geometry as rg
import Rhino
import System

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

def build_station_segments(all_station_objects, fos_curve, fob_curve, profile_curve, ship_limits_matrix, station_plane_vector):
    new_station_curves = []
    z_max_global = ship_limits_matrix[2][1]

    def make_intercept_tuple(rg_pt, idx, s_num, b_tag):
        # Added b_tag at the end
        return (rg_pt, idx, ship_limits_matrix, station_plane_vector, "station", s_num, False, True, b_tag)

    def make_original_tuple(coords, idx, s_num):
        rg_pt = rg.Point3d(coords[0], coords[1], coords[2])
        # Passes None for b_tag since it's an original point
        return (rg_pt, idx, ship_limits_matrix, station_plane_vector, "station", s_num, True, False, None)

    for station_list in all_station_objects:
        if not station_list:
            continue

        station_x = rs.PointCoordinates(station_list[0].id)[0]
        station_num = station_list[0].station_number

        # 1. Gather all geometric intersections
        fos_ints = fos_curve.get_intercepts_with_plane(station_x)
        fob_ints = fob_curve.get_intercepts_with_plane(station_x)
        prof_ints = profile_curve.get_intercepts_with_plane(station_x)

        # 2. Pool them together WITH TAGS and sort by Z
        boundaries = []
        if fob_ints:
            for pt in fob_ints: boundaries.append((pt, "FOB"))
        if prof_ints:
            for pt in prof_ints: boundaries.append((pt, "PROFILE"))
        if fos_ints:
            for pt in fos_ints: boundaries.append((pt, "FOS"))

        boundaries.sort(key=lambda b: b[0].Z)

        # 3. Remove duplicates (checking the Z of the rg.Point3d inside the tuple)
        unique_boundaries = []
        for b in boundaries:
            if not unique_boundaries or abs(b[0].Z - unique_boundaries[-1][0].Z) > 0.001:
                unique_boundaries.append(b)

        # 4. Extract original points sorted by Z
        orig_coords = sorted([rs.PointCoordinates(p.id) for p in station_list], key=lambda c: c[2])

        # 5. Fallback logic
        if len(unique_boundaries) % 2 != 0:
            top_y = orig_coords[-1][1] if orig_coords else 0.0
            unique_boundaries.append((rg.Point3d(station_x, top_y, z_max_global), "Z_MAX_CAP"))

        # 6. Process the boundaries in PAIRS
        i = 0
        while i < len(unique_boundaries) - 1:
            start_pt, start_tag = unique_boundaries[i]     # Unpack point and tag
            end_pt, end_tag = unique_boundaries[i+1]       # Unpack point and tag
            
            chunk_coords = [c for c in orig_coords if start_pt.Z + 0.001 < c[2] < end_pt.Z - 0.001]
            
            ordered_tuples = []
            ordered_tuples.append(make_intercept_tuple(start_pt, 0, station_num, start_tag))
            
            for idx, c in enumerate(chunk_coords, start=1):
                ordered_tuples.append(make_original_tuple(c, idx, station_num))
                
            ordered_tuples.append(make_intercept_tuple(end_pt, len(ordered_tuples), station_num, end_tag))
            
            point_objects = [MyPoint(*tup) for tup in ordered_tuples]
            for p_idx, pt in enumerate(point_objects):
                if p_idx > 0: pt.prev = point_objects[p_idx - 1]
                if p_idx < len(point_objects) - 1: pt.next = point_objects[p_idx + 1]

            curve_name = "Station_{}_Part_{}".format(station_num, int(i/2))
            curve = MyCurve(point_objects, ship_limits_matrix, station_plane_vector, curve_name)
            new_station_curves.append(curve)
            
            i += 2 

    return new_station_curves


class MyPoint:
    def __init__(self, rg_pt, index, limits, plane, pt_type, station_number, is_original, is_intercept, boundary_hit=None):
        self.original_coords = rg_pt
        self.limits = limits
        self.index = index
        self.is_original = is_original
        self.pt_type = pt_type
        self.is_intercept = is_intercept
        self.station_number = station_number
        self.plane = plane
        self.hit = boundary_hit #fos,fob,prof
        self.id = rs.AddPoint(rg_pt)
        
        self.prev = None
        self.next = None
    @property
    def coords(self):
        """ 
        Redirects all calls for .coords to .original_coords.
        Now self.next.coords will work perfectly!
        """
        return self.original_coords

    @coords.setter
    def coords(self, value):
        """ Allows you to update the point location if needed later """
        self.original_coords = value
    @property
    def boundary_hit(self):
        """
        Calculates the finalized hit tag.
        Combines the self.hit attribute with spatial limit detection.
        """
        tags = []
        
        # 1. Handle the manual 'hit' attribute (supports strings or lists)
        if self.hit:
            if isinstance(self.hit, list):
                tags.extend(self.hit)
            else:
                tags.append(self.hit)
        
        # 2. Check spatial hits via the limits_bool_list
        # [[Xmin, Xmax], [Ymin, Ymax], [Zmin, Zmax]]
        bools = self.limits_bool_list
        
        if bools[0][0]: tags.append("TRANSOM")
        if bools[1][0]: tags.append("CL")     # Centerline
        if bools[1][1]: tags.append("FOS")    # Flat of Side
        if bools[2][0]: tags.append("BL")     # Baseline
        if bools[2][1]: tags.append("DECK")   # Main Deck

        # 3. Deduplicate and sort for a consistent output
        unique_tags = sorted(list(set(tags)))

        if not unique_tags:
            return "None"
            
        # 4. Return as a single clean string (e.g., "CL+PROFILE")
        return "+".join(unique_tags)
    
    
    @property 
    def distance_from_original_point(self):
        """
        calculates distance between current and previous location of the same point
        """
        current_pos = rs.PointCoordinates(self.id)
        return rs.Distance(self.original_coords, current_pos)
    
    @property
    def limits_bool_list(self):
        """
        makes a 2x3 matrix, 1st row is x second is y and third is z 
        the first column is min value and the second is max value
        the values of thi smatrix can either be 1 or 0, 1 means that the point has a constaint 
        due to the applied limit from the attributes and 0 means that it doesnt have such a constraint
        we will use this info to find dof of the point and other stuff, this is not completed because this function
        doesnt take into consideration consraint due to 2 points being on the same line x=... or y=... or z=...

        """
        bool_matrix = []
        tolerance = 0.001
        current_pos = rs.PointCoordinates(self.id)
        for j in [0,1,2]:
            row = []
            
            #we check the plane vector
            if self.plane[j] == 1:
                bool_matrix.append([0, 0])
                continue

            for i in [0,1]: #min and max
                if self.limits[j][i] is not None:
                    dif = abs(self.limits[j][i] - current_pos[j])
                    if dif <= tolerance:
                        row.append(1)
                    else:
                        row.append(0)
                else: row.append(0) #no limit exists 
            bool_matrix.append(row)
        return bool_matrix
        
    @property
    def is_constrained(self):
        """
        this function views the elements of the limits_bool_list matrix and determines if the point is constrained
        if it is constrained it cannot be used in the fair algorithm of rhino, it only moves in the allowed dof 
        i updated it, it outputs 0,1,2 read below 
        """
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
            return 1 #one dof, can only slide along a vertical or horizontal line 
        
        return 0 #free
        
    @property
    def is_line(self):
        # Allow line detection for waterlines and stations
        if self.is_intercept and self.pt_type not in ["station", "waterline"]:
            return [0, 0]

        line_matrix = [0, 0]
        neighbors = [self.prev, self.next]
        tolerance = 0.001

        # ENHANCED: Larger tolerance for waterlines to catch faired parallel midbody
        if self.pt_type == "waterline":
            tolerance = 0.01  # 15cm tolerance for near-parallel sections

        current_coords = rs.PointCoordinates(self.id)

        for index, neighbor in enumerate(neighbors):
            if not neighbor:
                continue
            neighbor_coords = rs.PointCoordinates(neighbor.id)

            # Check coordinates perpendicular to plane
            for axis in range(3):
                if self.plane[axis] == 0:
                    dif = abs(current_coords[axis] - neighbor_coords[axis])
                    if dif <= tolerance:
                        line_matrix[index] = 1
                        break

        return line_matrix
    
    @property
    def is_tangent(self):
        """
        determines the required tangent vector for a spline 
        connecting to this point
        """
       
        if self.is_line == [1,0] or self.is_line == [0,1]: #if a point is part of a straight line segment, it has a tangent 
            return True
        
        if self.is_line == [1, 1]: #if its part of a line then it doesnt make sense to have a tangent condition
            return False
         
        if self.limits_bool_list[2][1]:#exception, if a point is at zmax, it does have a constraint, it can only move on the x or y direction, but it doesnt
                                       #mean that it also has a forced tangent, although if is_line has non zero elements, it can have a tangent 
            return False
        
        if any(any(row) for row in self.limits_bool_list): #any other case has a forced tangent 
            return True
        
        return False
    
    @property
    def line_directions(self):
        """
        For each neighbor that forms a straight line with this point,
        returns the unit vector pointing in the direction of travel:
          index 0 → direction FROM prev TOWARD current (line arrives from prev)
          index 1 → direction FROM current TOWARD next (line departs to next)
        Returns [None, None] if no line connections exist.
        """
        directions = [None, None]
        current_coords = rs.PointCoordinates(self.id)
        neighbors = [self.prev, self.next]

        for idx, neighbor in enumerate(neighbors):
            if not neighbor:
                continue
            if self.is_line[idx] == 0:
                continue

            neighbor_coords = rs.PointCoordinates(neighbor.id)

            if idx == 0:
                # direction: prev → current
                vec = rg.Vector3d(
                    current_coords[0] - neighbor_coords[0],
                    current_coords[1] - neighbor_coords[1],
                    current_coords[2] - neighbor_coords[2]
                )
            else:
                # direction: current → next
                vec = rg.Vector3d(
                    neighbor_coords[0] - current_coords[0],
                    neighbor_coords[1] - current_coords[1],
                    neighbor_coords[2] - current_coords[2]
                )

            if vec.Length > 0.001:
                vec.Unitize()
                directions[idx] = vec

        return directions

    @property
    def is_knuckle(self):
        """
        True if this is a profile point whose line connection is vertical,
        i.e. parallel to (0,0,1) — same X as neighbor, different Z.
        These are the stern knuckle points. They must NOT receive a forced tangent
        because the spline is meant to break direction at that point.
        """
        if self.pt_type != "profile":
            return False

        for d in self.line_directions:
            if d is None:
                continue
            # A vertical line in XZ has near-zero X and near-unit Z
            if abs(d.X) < 0.01 and abs(d.Y) < 0.01 and abs(d.Z) > 0.99:
                return True

        return False

    @property
    def required_tangent_vector(self):
        hit = self.boundary_hit
        pt_type_lower = str(self.pt_type).lower()
        current_coords = rs.PointCoordinates(self.id)

        # --- 0. THE KNUCKLE GUARD (Priority #1) ---
        if getattr(self, 'is_knuckle', False):
            line_status = getattr(self, 'is_line', [0, 0])
            if line_status == [0, 1]:
                return rg.Vector3d(-1, 0, 0)
            elif line_status == [1, 0]:
                return rg.Vector3d(1, 0, 0)
            return None

        # --- TRANSOM CENTERLINE TANGENCY ---
        if pt_type_lower == "transom" and "CL" in hit:
            return rg.Vector3d(0, 1, 0)

        # --- STATION BOUNDARY TANGENTS ---
        if pt_type_lower == "station":
            if "CL" in hit or "BL" in hit:
                ref = self.next if self.next else self.prev
                if ref:
                    if self.next:
                        raw_dir = self.next.coords - self.coords
                    else:
                        raw_dir = self.coords - self.prev.coords
                    projected = rg.Vector3d(raw_dir.X, raw_dir.Y, 0.0)
                    if projected.Length > 0.0001:
                        projected.Unitize()
                        return projected
                return rg.Vector3d(0, 1, 0)

            if "FOS" in hit:
                ref = self.next if self.next else self.prev
                if ref:
                    if self.next:
                        raw_dir = self.next.coords - self.coords
                    else:
                        raw_dir = self.coords - self.prev.coords
                    projected = rg.Vector3d(raw_dir.X, 0.0, raw_dir.Z)
                    if projected.Length > 0.0001:
                        projected.Unitize()
                        return projected
                return rg.Vector3d(0, 0, 1)

        # --- NEW: WATERLINE TANGENTS ---
        if pt_type_lower == "waterline":
            x_min = self.limits[0][0]

            # At transom (x_min) → G0 only, no forced tangent
            if x_min is not None and abs(current_coords[0] - x_min) < 0.001:
                return None

            # At profile endpoints → G0 only
            if "PROFILE" in hit:
                return None

            # Line-spline junctions: use line direction
            line_st = self.is_line
            if line_st == [0, 1]: return self.line_directions[1]
            if line_st == [1, 0]: return self.line_directions[0]

            return None

        # --- LINE-SPLINE JUNCTION (for other types) ---
        line_st = self.is_line
        if line_st == [0, 1]: return self.line_directions[1]
        if line_st == [1, 0]: return self.line_directions[0]

        return None
    
class MySegment:
    """
    Self-aware segment object. Knows its geometry, both endpoints in full
    detail, and every constraint relevant for CreateMatchCurve / Fair.
    """
    def __init__(self, crv_id, all_pt_objs, seg_type, curve_name, seg_index):
        # ── Identity ────────────────────────────────────────────────────────
        self.id         = crv_id                       # Rhino GUID
        self.type       = seg_type                     # "BSPLINE" or "LINE"
        self.curve_name = curve_name                   # parent curve name
        self.index      = seg_index                    # position in parent
        self.name       = "{}_SEG_{}".format(curve_name, seg_index)

        # ── Points ──────────────────────────────────────────────────────────
        self.points = all_pt_objs                      # all MyPoint objects
        self.start  = all_pt_objs[0]                   # first MyPoint
        self.end    = all_pt_objs[-1]                  # last  MyPoint

    # ── START endpoint ───────────────────────────────────────────────────────
    @property
    def start_id(self):
        return self.start.id

    @property
    def start_coords(self):
        return self.start.coords

    @property
    def start_tangent(self):
        return self.start.required_tangent_vector

    @property
    def start_is_line(self):
        return self.start.is_line

    @property
    def start_is_knuckle(self):
        return self.start.is_knuckle

    @property
    def start_hit(self):
        return self.start.boundary_hit

    # ── END endpoint ─────────────────────────────────────────────────────────
    @property
    def end_id(self):
        return self.end.id

    @property
    def end_coords(self):
        return self.end.coords

    @property
    def end_tangent(self):
        return self.end.required_tangent_vector

    @property
    def end_is_line(self):
        return self.end.is_line

    @property
    def end_is_knuckle(self):
        return self.end.is_knuckle

    @property
    def end_hit(self):
        return self.end.boundary_hit

    # ── Segment-level boundary summary ───────────────────────────────────────
    @property
    def boundary_hits(self):
        """
        Union of all boundary tags touched by this segment's two endpoints.
        Returns a sorted list — e.g. ['BL', 'FOB'] or ['FOS'].
        """
        hits = set()
        for tag in self.start_hit.split("+"):
            if tag and tag != "None":
                hits.add(tag)
        for tag in self.end_hit.split("+"):
            if tag and tag != "None":
                hits.add(tag)
        return sorted(hits)

    def hits(self, tag):
        """Convenience: seg.hits('FOB') → True/False"""
        return tag in self.boundary_hits

    # ── Display ──────────────────────────────────────────────────────────────
    def display_report(self):
        W = 130
        print("\n" + "=" * W)
        print("SEGMENT : {}".format(self.name))
        print("Type    : {}  |  GUID: {}".format(self.type, self.id))
        print("Hits    : {}".format(", ".join(self.boundary_hits) if self.boundary_hits else "None"))
        print("-" * W)

        hdr = "{:<7} {:<5} {:<20} {:<10} {:<8} {:<26} {}"
        print(hdr.format("Role", "Kind", "Hit", "IsLine", "Knuckle",
                          "Tangent (X, Y, Z)", "Coords (X, Y, Z)"))
        print("-" * W)

        for role, pt in [("START", self.start), ("END", self.end)]:
            tan = pt.required_tangent_vector
            tan_str  = ("({:6.3f},{:6.3f},{:6.3f})".format(tan.X, tan.Y, tan.Z)
                        if tan else "None")
            kind     = "INT" if pt.is_intercept else "ORIG"
            c        = pt.coords
            coord_str = "({:.3f},{:.3f},{:.3f})".format(c.X, c.Y, c.Z)
            knuckle  = "YES" if pt.is_knuckle else "No"

            print(hdr.format(role, kind, pt.boundary_hit,
                             str(pt.is_line), knuckle, tan_str, coord_str))

        print("=" * W + "\n")    

class MyCurve:
    def __init__(self, point_objects, limits, plane_vector, name=None):
        self.pts    = point_objects
        self.limits = limits
        self.plane  = plane_vector

        # Auto-name from the first point's metadata
        if name:
            self.name = name
        elif self.pts and hasattr(self.pts[0], 'pt_type'):
            self.name = str(self.pts[0].pt_type).upper()
            if self.name == "STATION" and hasattr(self.pts[0], 'station_number'):
                self.name = "STATION_{}".format(self.pts[0].station_number)
        else:
            self.name = "UNKNOWN_CURVE"

        self.segments       = []   # list of MySegment objects
        self.segment_matrix = []

        self.filter_intercept_overlaps()
        self.rebuild()

    # ─────────────────────────────────────────────────────────────────────────
    # GEOMETRY CONSTRUCTION
    # ─────────────────────────────────────────────────────────────────────────

    def filter_intercept_overlaps(self):
        """
        Remove original data points that are too close to intercept points.
        """
        if "station" not in self.name.lower():
            return

        intercepts = []
        originals = []

        for p in self.pts:
            if p.is_intercept:
                intercepts.append(p)
            else:
                originals.append(p)

        print("FILTER DEBUG: {} - {} intercepts, {} originals".format(
            self.name, len(intercepts), len(originals)))

        if not intercepts or not originals:
            return

        to_delete = []

        for orig in originals:
            orig_coords = rs.PointCoordinates(orig.id)

            for intercept in intercepts:
                int_coords = rs.PointCoordinates(intercept.id)
                dist = rs.Distance(orig_coords, int_coords)

                if dist < 0.5:
                    print("  -> Deleting point at Z={:.3f} (dist={:.3f} from intercept at Z={:.3f})".format(
                        orig_coords[2], dist, int_coords[2]))
                    to_delete.append(orig)
                    break

        # Delete from Rhino
        if to_delete:
            rs.DeleteObjects([p.id for p in to_delete if rs.IsObject(p.id)])
            self.pts = [p for p in self.pts if p not in to_delete]
            print("  -> Deleted {} points, {} remaining".format(len(to_delete), len(self.pts)))

        # Re-sort and re-link
        self.pts.sort(key=lambda p: rs.PointCoordinates(p.id)[2])

        for i in range(len(self.pts)):
            self.pts[i].prev = self.pts[i - 1] if i > 0 else None
            self.pts[i].next = self.pts[i + 1] if i < len(self.pts) - 1 else None

    def rebuild(self):
        """
        1. Delete any existing Rhino geometry for this curve.
        2. Walk the point list and group consecutive points into LINE or
           BSPLINE rows using each point's is_line[1] flag.
        3. Create the Rhino geometry and wrap every row in a MySegment.
        """
        # ── 1. Clean up old geometry ─────────────────────────────────────────
        if self.segments:
            for seg in self.segments:
                if rs.IsObject(seg.id):
                    rs.DeleteObject(seg.id)

        self.segments       = []
        self.segment_matrix = []

        pts = self.pts
        if len(pts) < 2:
            return None

        # ── 2. Build segment_matrix ──────────────────────────────────────────
        # Each row: [type_flag, pt_0, pt_1, ..., pt_n]
        # type_flag 1 → LINE, 0 → BSPLINE
        i = 0
        while i < len(pts) - 1:
            type_flag = 1 if pts[i].is_line[1] == 1 else 0
            row = [type_flag, pts[i]]

            while i < len(pts) - 1:
                current_seg_type = 1 if pts[i].is_line[1] == 1 else 0
                if current_seg_type != type_flag:
                    break
                row.append(pts[i + 1])
                i += 1

            self.segment_matrix.append(row)

        # ── 3. Create geometry + MySegment objects ───────────────────────────
        for seg_idx, row in enumerate(self.segment_matrix):
            seg_type = row[0]
            pt_objs  = row[1:]
            coords   = [rs.PointCoordinates(p.id) for p in pt_objs]

            if seg_type == 1:
                crv_id = rs.AddLine(coords[0], coords[-1])
                t_str  = "LINE"
            else:
                start_tan = pt_objs[0].required_tangent_vector
                end_tan   = pt_objs[-1].required_tangent_vector
                crv_id    = rs.AddInterpCurve(coords, 3, 0, start_tan, end_tan)
                t_str     = "BSPLINE"

            # --- THE CRITICAL FIX ---
            # Tag the actual Rhino object with the name of the curve
            if crv_id:
                rs.ObjectName(crv_id, self.name)

            self.segments.append(
                MySegment(crv_id, pt_objs, t_str, self.name, seg_idx)
            )

        return self.segments

    # ─────────────────────────────────────────────────────────────────────────
    # GEOMETRY QUERIES
    # ─────────────────────────────────────────────────────────────────────────

    def get_intercepts_with_plane(self, station_x):
        """
        Intersect every segment of this curve with the YZ plane at station_x.
        Returns all intersection points sorted by ascending Z.
        Handles complex sterns that produce multiple intercepts.
        """
        if not self.segments:
            return []

        origin = rg.Point3d(station_x, 0, 0)
        plane  = rg.Plane(origin, rg.Vector3d.XAxis)

        all_pts = []
        for seg in self.segments:
            if not rs.IsObject(seg.id):
                continue
            rhino_curve = rs.coercecurve(seg.id)
            if not rhino_curve:
                continue
            result = rg.Intersect.Intersection.CurvePlane(rhino_curve, plane, 0.001)
            if result:
                for x in result:
                    all_pts.append(x.PointA)

        all_pts.sort(key=lambda p: p.Z)
        return all_pts

    def calculate_segment_inflections(self, segment_id):
        """
        Sample the curvature sign along a segment and return 3-D points
        where the sign flips (inflection points).
        """
        rhino_curve = rs.coercecurve(segment_id)
        if not rhino_curve:
            return []

        domain    = rhino_curve.Domain
        steps     = 50
        step_size = domain.Length / steps

        inflection_points = []
        last_sign = 0

        for i in range(steps + 1):
            t       = domain.Min + (i * step_size)
            success, pt, t_vec, k_vec = rhino_curve.Evaluate(t, 2)
            if success:
                cross = rg.Vector3d.CrossProduct(t_vec, k_vec)
                if abs(cross.Z) > 0.05:
                    current_sign = 1 if cross.Z > 0 else -1
                    if last_sign != 0 and current_sign != last_sign:
                        inflection_points.append(pt)
                    last_sign = current_sign

        return inflection_points

    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY / DEBUG
    # ─────────────────────────────────────────────────────────────────────────

    def display_report(self):
        """
        Full point-level audit table for this curve, followed by a
        summary of its geometry segments.
        """
        W = 135
        print("\n" + "=" * W)
        print("CURVE REPORT: {}".format(self.name))
        print("=" * W)

        # ── Point table ──────────────────────────────────────────────────────
        print("\nPOINT LIST ({} points):".format(len(self.pts)))
        print("{:<4} {:<5} {:<7} {:<8} {:<12} {:<20} {:<22} {:<25}".format(
            "Idx", "Type", "Stat", "L-M", "Hit",
            "Lim-Bool(X,Y,Z)", "Req-Tangent(X,Y,Z)", "Coordinates(X,Y,Z)"
        ))
        print("-" * W)

        for p in self.pts:
            p_type  = "INT"   if p.is_intercept  else "ORIG"
            status  = ("Fixed"  if p.is_constrained == 2 else
                       "Slider" if p.is_constrained == 1 else "Free")
            l_mat   = str(p.is_line).replace(" ", "")
            hit_val = p.boundary_hit
            lim_str = str(p.limits_bool_list).replace(" ", "")
            tan     = p.required_tangent_vector
            tan_str = ("({:.2f},{:.2f},{:.2f})".format(tan.X, tan.Y, tan.Z)
                       if tan else "None")
            c       = getattr(p, 'coords', p.original_coords)
            c_str   = "({:.3f},{:.3f},{:.3f})".format(c.X, c.Y, c.Z)
            knuckle = " *K*" if p.is_knuckle else ""

            print("{:<4} {:<5} {:<7} {:<8} {:<12} {:<20} {:<22} {}{}".format(
                p.index, p_type, status, l_mat, hit_val,
                lim_str, tan_str, c_str, knuckle
            ))

        # ── Segment summary ───────────────────────────────────────────────────
        print("\nGEOMETRY SEGMENTS:")
        print("-" * W)
        for seg in self.segments:
            indices  = [p.index for p in seg.points]
            hits_str = ", ".join(seg.boundary_hits) if seg.boundary_hits else "None"
            print("Segment {}: {:<10} | Hits: {:<25} | Points: {}".format(
                seg.index, seg.type, hits_str, indices
            ))

        print("=" * W + "\n")
        print("=" * W + "\n")

    def display_segments_report(self):
        """
        Call display_report() on every MySegment belonging to this curve.
        Useful for drilling into endpoint tangents / constraints before fairing.
        """
        for seg in self.segments:
            seg.display_report()

    # ─────────────────────────────────────────────────────────────────────────
    # LEGACY PROPERTY (kept for any code that still calls .segment_list)
    # ─────────────────────────────────────────────────────────────────────────

    @property
    def segment_list(self):
        out = ["\n" + "=" * 30, "SEGMENT REPORT: {}".format(self.name), "-" * 30]
        for seg in self.segments:
            ids = [p.index for p in seg.points]
            out.append("Seg {}: {} | Hits: {} | Indices: {}".format(
                seg.index, seg.type,
                ", ".join(seg.boundary_hits) if seg.boundary_hits else "None",
                ids
            ))
        out.append("=" * 30)
        return "\n".join(out)


"""
calling the functions
"""
profile_plane_vector = [0,1,0]
ship_limits_matrix = get_limits(profile_nodim, l_bp, b_half, d)
profile_curve_type = "profile"
profile_data_tuples, profile_is_station = get_points_from_data(profile_nodim, l_bp, b_whole, d, profile_curve_type, ship_limits_matrix)
my_profile_point_objects = get_point_objects(profile_data_tuples, profile_is_station)
my_profile_curve_object = MyCurve(my_profile_point_objects, ship_limits_matrix, profile_plane_vector)

fos_plane_vector = [0,1,0]
# ship_limits_matrix is already calculated from the profile, so we reuse it
fos_curve_type = "fos"
fos_data_tuples, fos_is_station = get_points_from_data(fos_nodim, l_bp, b_whole, d, fos_curve_type, ship_limits_matrix)
my_fos_point_objects = get_point_objects(fos_data_tuples, fos_is_station)
my_fos_curve_object = MyCurve(my_fos_point_objects, ship_limits_matrix, fos_plane_vector)

transom_plane_vector = [1, 0, 0]
transom_curve_type = "transom"
transom_data_tuples, transom_is_station = get_points_from_data(transom_nodim, l_bp, b_whole, d, transom_curve_type, ship_limits_matrix)
my_transom_point_objects = get_point_objects(transom_data_tuples, transom_is_station)
my_transom_curve_object = MyCurve(my_transom_point_objects, ship_limits_matrix, transom_plane_vector)

fob_plane_vector = [0, 0, 1]
fob_curve_type = "fob"
fob_data_tuples, fob_is_station = get_points_from_data(fob_nodim, l_bp, b_whole, d, fob_curve_type, ship_limits_matrix)
my_fob_point_objects = get_point_objects(fob_data_tuples, fob_is_station)
my_fob_curve_object = MyCurve(my_fob_point_objects, ship_limits_matrix, fob_plane_vector)




# Boundary curve reports
# my_fob_curve_object.display_report()
# my_profile_curve_object.display_report()
# my_fos_curve_object.display_report()
# my_transom_curve_object.display_report()


# my_fob_curve_object.display_segments_report()
# my_profile_curve_object.display_segments_report()
# my_fos_curve_object.display_segments_report()
# my_transom_curve_object.display_segments_report()


def universal_fair_function(seg):
    """
    Polishes a curve segment based on its length and tangent requirements.
    Classifies segments as SMALL, MEDIUM, or BIG and clarifies G0/G1 status for both ends.
    """
    # 1. IMMEDIATE SKIP FOR LINES
    if seg.type == "LINE":
        print(f"   -> {seg.name}: Skipped (Type is LINE).")
        return

    # 2. DATA ACQUISITION
    base_geo = rs.coercecurve(seg.id)
    if not base_geo:
        print(f"   -> {seg.name}: Error - Could not find geometry.")
        return

    nurbs = base_geo.ToNurbsCurve()
    
    # 3. FAIRING PARAMETERS 
    ang = float(math.radians(80)) 
    dist = float(100000) 
    loop = int(100) 

    # 4. DYNAMIC CLAMPING (0 = G0 Position, 1 = G1 Tangency)
    clamp_start = 1 if seg.start_tangent is not None else 0
    clamp_end = 1 if seg.end_tangent is not None else 0

    # 5. DYNAMIC POINT DENSITY & CLASSIFICATION
    length = nurbs.GetLength()
    
    # Thresholds
    a, b = 10, 20 
    n_small, n_med, n_big = 6, 12, 18

    if length < a:
        num_of_cp = n_small
        size_label = "SMALL"
    elif a <= length < b:
        num_of_cp = n_med
        size_label = "MEDIUM"
    else:
        num_of_cp = n_big
        size_label = "BIG"

    # 6. EXECUTION
    try:
        # Rebuild(pointCount, degree, preserveEndpoints)
        nurbs = nurbs.Rebuild(num_of_cp, 3, True)
        
        # 5-Parameter Overload for Rhino 8
        fair_func = nurbs.Fair.Overloads[System.Double, System.Double, System.Int32, System.Int32, System.Int32]
        success = fair_func(dist, ang, clamp_start, clamp_end, loop)
        
        if success:
            Rhino.RhinoDoc.ActiveDoc.Objects.Replace(seg.id, nurbs)
            
            # --- UPDATED STATUS LOGIC ---
            # Map the integer values to readable strings
            s_stat = "G1 (Tangent)" if clamp_start == 1 else "G0 (Pos)"
            e_stat = "G1 (Tangent)" if clamp_end == 1 else "G0 (Pos)"
            status = f"Start:{s_stat} | End:{e_stat}"
            
            print(f"   -> {seg.name}: {size_label} | {num_of_cp} CPs | {length:.2f} units | {status}")
        else:
            print(f"   -> {seg.name}: {size_label} | Warning - No improvement possible.")

    except Exception as e:
        print(f"   -> {seg.name}: {size_label} | CRITICAL ERROR - {e}")


# --- EXECUTION ---
print("\n--- INITIATING SHIP FAIRING CYCLE ---")
for seg in my_fob_curve_object.segments:
    universal_fair_function(seg)

print("\n--- INITIATING SHIP FAIRING CYCLE ---")
for seg in my_fos_curve_object.segments:
    universal_fair_function(seg)

print("\n--- INITIATING SHIP FAIRING CYCLE ---")
for seg in my_profile_curve_object.segments:
    universal_fair_function(seg)

print("\n--- INITIATING SHIP FAIRING CYCLE ---")
for seg in my_transom_curve_object.segments:
    universal_fair_function(seg)

Rhino.RhinoDoc.ActiveDoc.Views.Redraw()

station_plane_vector = [1, 0, 0]
station_curve_type = "station"
station_data_tuples, station_is_station = get_points_from_data(offsets_nodim, l_bp, b_whole, d, station_curve_type, ship_limits_matrix)
my_station_point_objects = get_point_objects(station_data_tuples, station_is_station)

# Because stations output a list of lists, we loop through them to create multiple curves
my_station_curves = build_station_segments(
    my_station_point_objects,
    my_fos_curve_object,
    my_fob_curve_object,
    my_profile_curve_object,
    ship_limits_matrix,
    station_plane_vector
)

# # Station curve reports
for st_curve in my_station_curves:
    st_curve.display_report()

for st_curve in my_station_curves:
    st_curve.display_segments_report()

for st_curve in my_station_curves:
    print("\n--- INITIATING SHIP FAIRING CYCLE ---")
    for seg in st_curve.segments:
        universal_fair_function(seg)

def snap_parallel_midbody(intercepts):
    """
    Force parallel midbody to be perfectly straight by snapping ALL points
    in the parallel section to the same Y coordinate.
    """
    # Find FOS intercepts
    fos_points = [(i, pt, tag) for i, (pt, tag) in enumerate(intercepts) if "FOS" in tag]
    
    start_idx = None
    end_idx = None
    target_y = None
    
    if len(fos_points) == 2:
        # Use FOS intercepts as parallel section boundaries
        start_idx = fos_points[0][0]
        end_idx = fos_points[1][0]
        target_y = (fos_points[0][1].Y + fos_points[1][1].Y) / 2.0
        
    else:
        # Use midship stations (X between 75-180m)
        midship = [(i, pt, tag) for i, (pt, tag) in enumerate(intercepts) 
                   if "STATION" in tag and 0.3*l_bp < pt.X < 0.73*l_bp]
        
        if len(midship) >= 2:
            start_idx = midship[0][0]
            end_idx = midship[-1][0]
            target_y = (midship[0][1].Y + midship[-1][1].Y) / 2.0
    
    # Snap ALL points between start and end (inclusive) to target_y
    if start_idx is not None and end_idx is not None and target_y is not None:
        for i in range(start_idx, end_idx + 1):
            pt, tag = intercepts[i]
            intercepts[i] = (rg.Point3d(pt.X, target_y, pt.Z), tag)
    
    return intercepts
num_waterlines = int(50)
def build_waterline_segments(fos_curve, profile_curve, transom_curve, station_curves, ship_limits_matrix, num_waterlines=10):
    """
    Create horizontal waterline curves at different Z heights.
    Intersects with FOS, Profile, Transom, and all stations.
    """
    waterline_plane_vector = [0, 0, 1]  # Perpendicular to XY plane
    z_min = ship_limits_matrix[2][0]
    z_max = ship_limits_matrix[2][1]
    
    # Start above baseline to avoid FOB
    z_start = z_min + 0.5
    z_range = z_max - z_start
    z_step = z_range / (num_waterlines - 1) if num_waterlines > 1 else 0
    
    waterline_curves = []
    
    def make_intercept_tuple(rg_pt, idx, wl_num, b_tag):
        return (rg_pt, idx, ship_limits_matrix, waterline_plane_vector, "waterline", wl_num, False, True, b_tag)
    
    for wl_idx in range(num_waterlines):
        wl_z = z_start + (wl_idx * z_step)
        
        # Create horizontal plane
        plane_origin = rg.Point3d(0, 0, wl_z)
        plane = rg.Plane(plane_origin, rg.Vector3d.ZAxis)
        
        # Collect intercepts with tags
        intercepts = []
        
        # FOS intersection
        for seg in fos_curve.segments:
            if rs.IsObject(seg.id):
                rhino_curve = rs.coercecurve(seg.id)
                if rhino_curve:
                    result = rg.Intersect.Intersection.CurvePlane(rhino_curve, plane, 0.001)
                    if result:
                        for x in result:
                            intercepts.append((x.PointA, "FOS"))
        
        # Profile intersection
        for seg in profile_curve.segments:
            if rs.IsObject(seg.id):
                rhino_curve = rs.coercecurve(seg.id)
                if rhino_curve:
                    result = rg.Intersect.Intersection.CurvePlane(rhino_curve, plane, 0.001)
                    if result:
                        for x in result:
                            intercepts.append((x.PointA, "PROFILE"))
        
        # Transom intersection
        for seg in transom_curve.segments:
            if rs.IsObject(seg.id):
                rhino_curve = rs.coercecurve(seg.id)
                if rhino_curve:
                    result = rg.Intersect.Intersection.CurvePlane(rhino_curve, plane, 0.001)
                    if result:
                        for x in result:
                            intercepts.append((x.PointA, "TRANSOM"))
        
        # Station intersections
        for st_curve in station_curves:
            for seg in st_curve.segments:
                if rs.IsObject(seg.id):
                    rhino_curve = rs.coercecurve(seg.id)
                    if rhino_curve:
                        result = rg.Intersect.Intersection.CurvePlane(rhino_curve, plane, 0.001)
                        if result:
                            for x in result:
                                intercepts.append((x.PointA, "STATION"))
        
        if len(intercepts) < 2:
            continue
        
        # Sort by X (stern to bow)
        intercepts.sort(key=lambda item: item[0].X)

        # For points at the same X, reorder by Y (centerline to side)
        i = 0
        while i < len(intercepts):
            # Find all points at the same X
            same_x_group = [intercepts[i]]
            j = i + 1
            while j < len(intercepts) and abs(intercepts[j][0].X - intercepts[i][0].X) < 0.001:
                same_x_group.append(intercepts[j])
                j += 1

            # If multiple points at same X, sort them by Y
            if len(same_x_group) > 1:
                same_x_group.sort(key=lambda item: item[0].Y)
                # Replace in original list
                for k, item in enumerate(same_x_group):
                    intercepts[i + k] = item

            i = j if j > i + 1 else i + 1
        # SNAP PARALLEL MIDBODY TO STRAIGHT LINE
        intercepts = snap_parallel_midbody(intercepts)

        # DEBUG: Print first few points after manual reordering
        if wl_idx == 8:
            print("\nDEBUG Waterline_8 after manual Y-reordering:")
            for i, (pt, tag) in enumerate(intercepts[:5]):
                print("  Point {}: X={:.3f}, Y={:.3f}, Z={:.3f}, Tag={}".format(
                    i, pt.X, pt.Y, pt.Z, tag))

        # Remove duplicates and merge tags (rest stays the same)
        unique_intercepts = []
        for pt, tag in intercepts:
            # Check if this point is very close to the last one
            if unique_intercepts:
                last_pt, last_tag = unique_intercepts[-1]
                # Use 3D distance instead of just X
                dist = math.sqrt(
                    (pt.X - last_pt.X)**2 + 
                    (pt.Y - last_pt.Y)**2 + 
                    (pt.Z - last_pt.Z)**2
                )
                
                if dist < 0.01:  # Within 1cm - same point
                    # Merge tags if different
                    if tag not in last_tag:
                        merged_tag = "+".join(sorted([last_tag, tag]))
                        unique_intercepts[-1] = (last_pt, merged_tag)
                    continue
            
            unique_intercepts.append((pt, tag))
        
        # Create point objects
        point_objects = []
        for idx, (pt, tag) in enumerate(unique_intercepts):
            point_objects.append(MyPoint(*make_intercept_tuple(pt, idx, wl_idx, tag)))
        

        # Link prev/next
        for i in range(len(point_objects)):
            if i > 0:
                point_objects[i].prev = point_objects[i - 1]
            if i < len(point_objects) - 1:
                point_objects[i].next = point_objects[i + 1]
        
        # Create curve
        curve_name = "Waterline_{}_Z{:.1f}".format(wl_idx, wl_z)
        wl_curve = MyCurve(point_objects, ship_limits_matrix, waterline_plane_vector, curve_name)
        waterline_curves.append(wl_curve)
    
    return waterline_curves

# ============================================================================
# WATERLINES GENERATION
# ============================================================================

print("\n" + "="*80)
print("GENERATING WATERLINES")
print("="*80)

my_waterline_curves = build_waterline_segments(
    my_fos_curve_object,
    my_profile_curve_object,
    my_transom_curve_object,
    my_station_curves,
    ship_limits_matrix,
    num_waterlines
)

print("\nCreated {} waterlines".format(len(my_waterline_curves)))

# Display waterline reports
# for wl_curve in my_waterline_curves:
#     wl_curve.display_report()

# for wl_curve in my_waterline_curves:
#     wl_curve.display_segments_report()

print("\n--- INITIATING SHIP FAIRING CYCLE ---")
for wl_curve in my_waterline_curves:
    for seg in wl_curve.segments:
        universal_fair_function(seg)

def rebuild_stations_with_waterlines(station_curves, waterline_curves, ship_limits_matrix):
    """
    Rebuild each station curve using waterline intercepts as intermediate points.
    Preserves segment structure and tangent continuity from original stations.
    
    For each segment:
    - Keep original start/end points with their tangents
    - Insert waterline intercepts that fall within segment's Z range
    - Create new interpolated curve through all points
    """
    station_plane_vector = [1, 0, 0]
    rebuilt_stations = []
    
    for st_curve in station_curves:
        # Get station X value
        station_x = rs.PointCoordinates(st_curve.pts[0].id)[0]
        station_num = st_curve.pts[0].station_number
        
        # Collect ALL waterline intercepts at this station X
        wl_intercepts_at_x = []
        for wl_curve in waterline_curves:
            for pt_obj in wl_curve.pts:
                coords = rs.PointCoordinates(pt_obj.id)
                if abs(coords[0] - station_x) < 0.1:  # Within 10cm of station
                    wl_intercepts_at_x.append((coords[2], coords))  # (Z, coords)
        
        # Sort by Z
        wl_intercepts_at_x.sort(key=lambda item: item[0])
        
        # Rebuild each segment independently
        all_new_points = []
        point_index = 0
        
        for seg in st_curve.segments:
            if seg.type == "LINE":
                # Lines: just keep start and end
                if not all_new_points:  # First segment
                    all_new_points.append({
                        'coords': seg.start_coords,
                        'hit': seg.start_hit,
                        'is_intercept': True
                    })
                all_new_points.append({
                    'coords': seg.end_coords,
                    'hit': seg.end_hit,
                    'is_intercept': True
                })
            else:
                # BSPLINE: insert waterline points between start and end
                start_z = seg.start_coords.Z
                end_z = seg.end_coords.Z
                
                # Add start point (if first segment)
                if not all_new_points:
                    all_new_points.append({
                        'coords': seg.start_coords,
                        'hit': seg.start_hit,
                        'is_intercept': True
                    })
                
                # Add waterline intercepts within this segment's Z range
                for z, coords in wl_intercepts_at_x:
                    if start_z + 0.01 < z < end_z - 0.01:  # Margin to avoid duplicates
                        all_new_points.append({
                            'coords': rg.Point3d(coords[0], coords[1], coords[2]),
                            'hit': "WATERLINE",
                            'is_intercept': False  # Interior point
                        })
                
                # Add end point
                all_new_points.append({
                    'coords': seg.end_coords,
                    'hit': seg.end_hit,
                    'is_intercept': True
                })
        
        # Create MyPoint objects from collected points
        point_objects = []
        for idx, pt_data in enumerate(all_new_points):
            pt_tuple = (
                pt_data['coords'],
                idx,
                ship_limits_matrix,
                station_plane_vector,
                "station",
                station_num,
                not pt_data['is_intercept'],  # is_original
                pt_data['is_intercept'],       # is_intercept
                pt_data['hit']
            )
            point_objects.append(MyPoint(*pt_tuple))
        
        # Link prev/next
        for i in range(len(point_objects)):
            if i > 0:
                point_objects[i].prev = point_objects[i - 1]
            if i < len(point_objects) - 1:
                point_objects[i].next = point_objects[i + 1]
        
        # Create new curve (automatically calls rebuild with proper tangents)
        curve_name = "{}_Rebuilt".format(st_curve.name)
        new_curve = MyCurve(point_objects, ship_limits_matrix, station_plane_vector, curve_name)
        rebuilt_stations.append(new_curve)
    
    return rebuilt_stations

# ============================================================================
# CROSS-FAIRING MASTER LOOP (NAME-BASED PURGE)
# ============================================================================

# 1. USER SETTINGS
total_cycles = 5  

def purge_geometry_by_name(curve_list):
    """
    Finds and deletes EVERY object in the Rhino doc that matches 
    the names in the curve_list, regardless of its current ID.
    """
    for curve_obj in curve_list:
        if hasattr(curve_obj, 'name') and curve_obj.name:
            # Fairing changes IDs but preserves the Object Name.
            # rs.ObjectsByName finds the 'ghost' IDs created by fairing.
            ghost_ids = rs.ObjectsByName(curve_obj.name)
            if ghost_ids:
                rs.DeleteObjects(ghost_ids)

# 2. INITIALIZATION
# Ensure the starting stations are properly named in Rhino 
# so the very first purge cycle can find them.
for st in my_station_curves:
    # This triggers your MyCurve.rebuild() which now handles rs.ObjectName
    st.rebuild() 

current_stations = my_station_curves
current_waterlines = []

# 3. MASTER EXECUTION
for cycle in range(total_cycles):
    print("\n" + "="*80)
    print(f"STARTING CROSS-FAIRING CYCLE {cycle + 1} OF {total_cycles}")
    print("="*80)

    # --- STEP A: WATERLINES ---
    # Delete waterlines from the PREVIOUS cycle before making new ones
    if current_waterlines:
        print(f"[CLEANUP] Purging previous waterlines by name...")
        purge_geometry_by_name(current_waterlines)

    print("[STEP A] Building and Fairing Waterlines...")
    current_waterlines = build_waterline_segments(
        my_fos_curve_object,
        my_profile_curve_object,
        my_transom_curve_object,
        current_stations,
        ship_limits_matrix,
        num_waterlines
    )
    
    # Fair the waterlines. Their IDs change here, but names persist.
    for wl in current_waterlines:
        for seg in wl.segments:
            universal_fair_function(seg)

    # --- STEP B: STATIONS ---
    print("[STEP B] Rebuilding and Refairing Stations...")
    new_stations = rebuild_stations_with_waterlines(
        current_stations,
        current_waterlines,
        ship_limits_matrix
    )
    
    # Delete the 'old' station geometry by name
    purge_geometry_by_name(current_stations)
    
    # Update our Python reference to the new rebuilt objects
    current_stations = new_stations
    
    # Fair the new stations.
    for st in current_stations:
        for seg in st.segments:
            universal_fair_function(seg)

print("\n" + "="*80)
print("CROSS-FAIRING COMPLETE")
print(f"Final Count: {len(current_stations)} Stations | {len(current_waterlines)} Waterlines")
print("="*80)

# Force the viewport to update
Rhino.RhinoDoc.ActiveDoc.Views.Redraw()

def create_hull_surface_network(station_curves, waterline_curves, surface_name="Hull_Surface"):
    """
    Create hull surface from stations and waterlines using NetworkSrf.
    """
    print("\n" + "="*80)
    print("CREATING HULL SURFACE FROM STATION/WATERLINE NETWORK")
    print("="*80)
    
    # Extract ALL segment IDs from MyCurve objects
    station_ids = []
    for st in station_curves:
        for seg in st.segments:
            if rs.IsObject(seg.id):
                station_ids.append(seg.id)
    
    waterline_ids = []
    for wl in waterline_curves:
        for seg in wl.segments:
            if rs.IsObject(seg.id):
                waterline_ids.append(seg.id)
    
    print("\nCollected {} station segments and {} waterline segments".format(
        len(station_ids), len(waterline_ids)))
    
    if not station_ids or not waterline_ids:
        print("\n✗ Error: No valid curve segments found!")
        return None
    
    # Combine all curves into ONE list (NetworkSrf figures out the network automatically)
    all_curve_ids = station_ids + waterline_ids
    
    # Create network surface
    surface_id = rs.AddNetworkSrf(
        all_curve_ids,          # Single list of all curves
        continuity=1,           # G1 continuity (tangent)
        edge_tolerance=0.01,    # 1cm tolerance at edges
        interior_tolerance=0.01,# 1cm tolerance at interior
        angle_tolerance=1.0     # 1 degree angle tolerance
    )
    
    if surface_id:
        rs.ObjectName(surface_id, surface_name)
        print("\n✓ Surface created successfully: {}".format(surface_name))
        
        # Get surface information
        if rs.IsSurface(surface_id):
            u_degree = rs.SurfaceDegree(surface_id, 0)
            v_degree = rs.SurfaceDegree(surface_id, 1)
            u_count = rs.SurfacePointCount(surface_id)[0]
            v_count = rs.SurfacePointCount(surface_id)[1]
            
            print("  Surface degree: U={}, V={}".format(u_degree, v_degree))
            print("  Control points: {} x {}".format(u_count, v_count))
    else:
        print("\n✗ Surface creation failed!")
        print("  NetworkSrf requires curves that form a proper grid network")
        print("  Try the Loft method as an alternative")
    
    return surface_id


def create_hull_surface_loft(station_curves, surface_name="Hull_Surface_Loft"):
    """
    Alternative: Create hull surface by lofting through stations.
    More forgiving than network surface.
    """
    print("\n" + "="*80)
    print("CREATING HULL SURFACE BY LOFTING STATIONS")
    print("="*80)
    
    # Extract segment IDs from station curves
    station_ids = []
    for st in station_curves:
        for seg in st.segments:
            if rs.IsObject(seg.id):
                station_ids.append(seg.id)
    
    print("\nLofting through {} station segments".format(len(station_ids)))
    
    if not station_ids:
        print("\n✗ Error: No valid station segments found!")
        return None
    
    # Create loft surface
    surface_id = rs.AddLoftSrf(
        object_ids=station_ids,
        start=None,
        end=None,
        loft_type=0,  # Normal loft
        closed=False
    )
    
    if surface_id:
        # Loft may return array if multiple surfaces
        if isinstance(surface_id, list):
            surface_id = surface_id[0]
        
        rs.ObjectName(surface_id, surface_name)
        print("\n✓ Loft surface created: {}".format(surface_name))
    else:
        print("\n✗ Loft surface creation failed!")
    
    return surface_id

def create_hull_surface_loft(station_curves, surface_name="Hull_Surface_Loft"):
    """
    Alternative: Create hull surface by lofting through stations.
    More forgiving than network surface.
    """
    print("\n" + "="*80)
    print("CREATING HULL SURFACE BY LOFTING STATIONS")
    print("="*80)
    
    # Extract segment IDs from station curves
    station_ids = []
    for st in station_curves:
        for seg in st.segments:
            if rs.IsObject(seg.id):
                station_ids.append(seg.id)
    
    print("\nLofting through {} station segments".format(len(station_ids)))
    
    if not station_ids:
        print("\n✗ Error: No valid station segments found!")
        return None
    
    # Create loft surface
    surface_id = rs.AddLoftSrf(
        object_ids=station_ids,
        start=None,
        end=None,
        loft_type=0,  # Normal loft
        closed=False
    )
    
    if surface_id:
        # Loft may return array if multiple surfaces
        if isinstance(surface_id, list):
            surface_id = surface_id[0]
        
        rs.ObjectName(surface_id, surface_name)
        print("\n✓ Loft surface created: {}".format(surface_name))
    else:
        print("\n✗ Loft surface creation failed!")
    
    return surface_id

# ============================================================================
# CREATE HULL SURFACE
# ============================================================================

# Use the FINAL cross-faired stations and waterlines
hull_surface_network = create_hull_surface_network(
    current_stations,     # These are the final cross-faired stations
    current_waterlines,   # These are the final cross-faired waterlines
    surface_name="Hull_NetworkSrf"
)

# Alternative: Loft surface (simpler, more forgiving)
hull_surface_loft = create_hull_surface_loft(
    current_stations,
    surface_name="Hull_Loft"
)

print("\n" + "="*80)
print("HULL SURFACE GENERATION COMPLETE")
print("="*80)