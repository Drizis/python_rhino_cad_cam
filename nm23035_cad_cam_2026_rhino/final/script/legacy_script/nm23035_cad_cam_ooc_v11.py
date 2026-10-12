"""nm23035_cad_cam_v10
Object-Oriented Hull Fairing with Phased Workflow
"""

#libraries
import rhinoscriptsyntax as rs
import math
import Rhino.Geometry as rg
import Rhino
import scriptcontext as sc

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

# Input parameters
number_of_letters = rs.GetInteger("number of letters in first name")
last_number_of_nm = rs.GetInteger("last number of your nm")

L_BP0 = 225
B_HALF0 = 15.9
l_bp = L_BP0 + number_of_letters
b_half = B_HALF0 + (last_number_of_nm/10.0)
d = b_half * 0.62
b_whole = 2 * b_half


def get_limits(profile_data_string, L_scale, B_half, D_scale):
    """Define ship boundary limits as 2x3 matrix"""
    if profile_data_string:
        lines = profile_data_string.strip().split('\n')
        min_raw_x = min(float(line.split(",")[0]) for line in lines if line.strip())
        x_min = min_raw_x * L_scale
        return [
            [x_min, None],     # X: Transom to Bow
            [0, B_half],       # Y: Centerline to FOS
            [0, D_scale]       # Z: Keel to Deck
        ]
    else:
        raise ValueError("Error: profile_data_string is empty.")


def get_points_from_data(data_string, L_scale, B_scale, D_scale, curve_type, ship_limits_matrix):
    """Parse raw data into scaled point tuples with metadata"""
    lines = data_string.strip().split('\n')
    all_points = []
    
    for line in lines:
        if not line.strip(): continue
        raw_x, raw_y, raw_z = map(float, line.split(","))
        all_points.append([raw_x * L_scale, raw_y * B_scale, raw_z * D_scale])

    if curve_type not in {"fob", "fos", "profile", "transom", "station"}:
        raise ValueError(f"Invalid curve_type: {curve_type}")
    
    # Determine plane normal vector
    if curve_type == "fob":
        plane = [0,0,1]
        all_points.sort(key=lambda p: p[0])
    elif curve_type in {"profile", "fos"}:
        plane = [0,1,0]
        if curve_type == "profile":
            aft = [p for p in all_points if p[0] < L_scale/2]
            fwd = [p for p in all_points if p[0] >= L_scale/2]
            aft.sort(key=lambda p: p[2], reverse=True)
            fwd.sort(key=lambda p: p[2])
            all_points = aft + fwd
        else:
            all_points.sort(key=lambda p: p[0])
    elif curve_type == "transom":
        plane = [1,0,0]
        all_points.sort(key=lambda p: p[2])
    elif curve_type == "station":
        plane = [1,0,0]
        # Group by station (x value)
        all_points.sort(key=lambda p: p[0])
        stations = []
        if all_points:
            current_station = [all_points[0]]
            for i in range(1, len(all_points)):
                if abs(all_points[i][0] - all_points[i-1][0]) < 0.01:
                    current_station.append(all_points[i])
                else:
                    current_station.sort(key=lambda p: p[2])
                    stations.append(current_station)
                    current_station = [all_points[i]]
            current_station.sort(key=lambda p: p[2])
            stations.append(current_station)
        
        # Convert to point tuples
        stations_rg_pts = []
        for station_num, curr_station in enumerate(stations):
            curr_station_rg = []
            for pt_idx, pt in enumerate(curr_station):
                rg_pt = rg.Point3d(pt[0], pt[1], pt[2])
                curr_station_rg.append((rg_pt, pt_idx, ship_limits_matrix, plane, 
                                       curve_type, station_num, True, False, None))
            stations_rg_pts.append(curr_station_rg)
        return stations_rg_pts, True
    
    # Convert to point tuples for non-station curves
    all_rg_pts = []
    for pt_idx, pt in enumerate(all_points):
        rg_pt = rg.Point3d(pt[0], pt[1], pt[2])
        all_rg_pts.append((rg_pt, pt_idx, ship_limits_matrix, plane, 
                          curve_type, None, True, False, None))
    return all_rg_pts, False


def get_point_objects(point_data, station_flag):
    """Convert point tuples to MyPoint objects with prev/next linking"""
    if not point_data:
        return []
    
    if not station_flag:
        point_objects = [MyPoint(*data_tuple) for data_tuple in point_data]
        for i in range(len(point_objects)):
            if i > 0:
                point_objects[i].prev = point_objects[i-1]
            if i < len(point_objects) - 1:
                point_objects[i].next = point_objects[i+1]
        return point_objects
    else:
        all_station_objects = []
        for station_list in point_data:
            current_station_objects = [MyPoint(*data_tuple) for data_tuple in station_list]
            for i in range(len(current_station_objects)):
                if i > 0:
                    current_station_objects[i].prev = current_station_objects[i-1]
                if i < len(current_station_objects) - 1:
                    current_station_objects[i].next = current_station_objects[i+1]
            all_station_objects.append(current_station_objects)
        return all_station_objects


def build_station_segments(all_station_objects, fos_curve, fob_curve, profile_curve, 
                           ship_limits_matrix, station_plane_vector):
    """
    Build station segments by intersecting with boundary curves.
    Automatically splits at complex stern geometry.
    """
    new_station_curves = []
    z_max_global = ship_limits_matrix[2][1]

    def make_intercept_tuple(rg_pt, idx, s_num, b_tag):
        return (rg_pt, idx, ship_limits_matrix, station_plane_vector, 
                "station", s_num, False, True, b_tag)

    def make_original_tuple(coords, idx, s_num):
        rg_pt = rg.Point3d(coords[0], coords[1], coords[2])
        return (rg_pt, idx, ship_limits_matrix, station_plane_vector, 
                "station", s_num, True, False, None)

    for station_list in all_station_objects:
        if not station_list:
            continue

        station_x = rs.PointCoordinates(station_list[0].id)[0]
        station_num = station_list[0].station_number

        # Gather ALL boundary intercepts
        fos_ints = fos_curve.get_intercepts_with_plane(station_x)
        fob_ints = fob_curve.get_intercepts_with_plane(station_x)
        prof_ints = profile_curve.get_intercepts_with_plane(station_x)

        # Pool and tag boundaries
        boundaries = []
        if fob_ints:
            for pt in fob_ints: boundaries.append((pt, "FOB"))
        if prof_ints:
            for pt in prof_ints: boundaries.append((pt, "PROFILE"))
        if fos_ints:
            for pt in fos_ints: boundaries.append((pt, "FOS"))

        boundaries.sort(key=lambda b: b[0].Z)

        # Remove duplicates
        unique_boundaries = []
        for b in boundaries:
            if not unique_boundaries or abs(b[0].Z - unique_boundaries[-1][0].Z) > 0.001:
                unique_boundaries.append(b)

        # Original points sorted by Z
        orig_coords = sorted([rs.PointCoordinates(p.id) for p in station_list], 
                            key=lambda c: c[2])

        # Fallback: if odd number of boundaries, cap at z_max
        if len(unique_boundaries) % 2 != 0:
            top_y = orig_coords[-1][1] if orig_coords else 0.0
            unique_boundaries.append((rg.Point3d(station_x, top_y, z_max_global), "Z_MAX_CAP"))

        # Process boundaries in PAIRS to create segments
        i = 0
        while i < len(unique_boundaries) - 1:
            start_pt, start_tag = unique_boundaries[i]
            end_pt, end_tag = unique_boundaries[i+1]
            
            # Filter original points within this segment
            chunk_coords = [c for c in orig_coords 
                           if start_pt.Z + 0.001 < c[2] < end_pt.Z - 0.001]
            
            # Build point tuples
            ordered_tuples = []
            ordered_tuples.append(make_intercept_tuple(start_pt, 0, station_num, start_tag))
            
            for idx, c in enumerate(chunk_coords, start=1):
                ordered_tuples.append(make_original_tuple(c, idx, station_num))
                
            ordered_tuples.append(make_intercept_tuple(end_pt, len(ordered_tuples), 
                                                       station_num, end_tag))
            
            # Create MyPoint objects
            point_objects = [MyPoint(*tup) for tup in ordered_tuples]
            for p_idx, pt in enumerate(point_objects):
                if p_idx > 0: 
                    pt.prev = point_objects[p_idx - 1]
                if p_idx < len(point_objects) - 1: 
                    pt.next = point_objects[p_idx + 1]

            # Create curve segment
            curve_name = "STATION_{}_SEG_{}".format(station_num, int(i/2))
            curve = MyCurve(point_objects, ship_limits_matrix, station_plane_vector, curve_name)
            new_station_curves.append(curve)
            
            i += 2 

    return new_station_curves


class MyPoint:
    """
    Self-aware point object that knows its constraints, DOF, and topological relationships
    """
    def __init__(self, rg_pt, index, limits, plane, pt_type, station_number, 
                 is_original, is_intercept, boundary_hit=None):
        self.original_coords = rg_pt
        self.limits = limits
        self.index = index
        self.is_original = is_original
        self.pt_type = pt_type
        self.is_intercept = is_intercept
        self.station_number = station_number
        self.plane = plane
        self.boundary_hit = boundary_hit  # "FOB", "FOS", "PROFILE", "Z_MAX_CAP", None
        self.id = rs.AddPoint(rg_pt)
        
        self.prev = None
        self.next = None

    @property 
    def distance_from_original_point(self):
        """Distance between current and original position"""
        current_pos = rs.PointCoordinates(self.id)
        return rs.Distance(self.original_coords, current_pos)
    
    @property
    def limits_bool_list(self):
        """2x3 matrix indicating which limits are active [min, max] for [x, y, z]"""
        bool_matrix = []
        tolerance = 0.001
        current_pos = rs.PointCoordinates(self.id)
        
        for j in [0,1,2]:
            if self.plane[j] == 1:
                bool_matrix.append([0, 0])
                continue
            
            row = []
            for i in [0,1]:  # min, max
                if self.limits[j][i] is not None:
                    dif = abs(self.limits[j][i] - current_pos[j])
                    row.append(1 if dif <= tolerance else 0)
                else:
                    row.append(0)
            bool_matrix.append(row)
        return bool_matrix
        
    @property
    def is_constrained(self):
        """
        Returns constraint level:
        0 = free (can move in plane)
        1 = one DOF (constrained to a line)
        2 = fixed (intercept point or hits 2+ limits)
        """
        if self.is_intercept:
            return 2
        
        hit_x = any(self.limits_bool_list[0])
        hit_y = any(self.limits_bool_list[1])
        hit_z = any(self.limits_bool_list[2])
        hit_line = any(self.is_line)
        hit_count = int(hit_x) + int(hit_y) + int(hit_z) + int(hit_line)

        if hit_count >= 2:
            return 2  # fixed
        if hit_count == 1:
            return 1  # one DOF
        return 0  # free
    
    @property
    def is_line(self):
        """Check if point is part of a straight line segment with neighbors"""
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
    def tangent_vector(self):
        """
        Returns required tangent vector based on boundary_hit tag.
        Used for CreateMatchCurve constraints.
        """
        if not self.is_intercept or not self.boundary_hit:
            return None
        
        # Station intercepts have specific tangent requirements
        if self.boundary_hit == "FOS":
            # Tangent to XZ plane (perpendicular to Y)
            return rg.Vector3d(0, 1, 0)
        elif self.boundary_hit in ["FOB", "PROFILE"]:
            # Tangent to XY plane (perpendicular to Z)
            return rg.Vector3d(0, 0, 1)
        
        return None


class MyCurve:
    """
    Self-aware curve object that maintains segments and implements fairing
    """
    def __init__(self, point_objects, limits, plane_vector, name=None):
        self.pts = point_objects
        self.limits = limits
        self.plane = plane_vector
        
        # Auto-generate name from point metadata
        if not name and self.pts:
            if hasattr(self.pts[0], 'pt_type'):
                self.name = str(self.pts[0].pt_type).upper()
                if self.name == "STATION" and hasattr(self.pts[0], 'station_number'):
                    self.name = "STATION_{}".format(self.pts[0].station_number)
            else:
                self.name = "UNKNOWN"
        else:
            self.name = name if name else "CURVE"
        
        self.segments = []  # List of {type, id, points} dicts
        self.joined_id = None  # Joined polycurve for fairing
        self.segment_matrix = []
        
        self.rebuild()

    def rebuild(self):
        """
        Build curve segments (lines vs splines) and join into polycurve
        """
        # Clean up old geometry
        if self.segments:
            for seg in self.segments:
                if rs.IsObject(seg['id']):
                    rs.DeleteObject(seg['id'])
        if self.joined_id and rs.IsObject(self.joined_id):
            rs.DeleteObject(self.joined_id)
        
        self.segments = []
        pts = self.pts 
        if len(pts) < 2:
            return None

        # Build segment_matrix: [type_flag, pt1, pt2, ...]
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

        # Create individual segment curves
        segment_ids = []
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
            
            segment_ids.append(crv_id)
            self.segments.append({
                'type': t_str,
                'id': crv_id,
                'points': pt_objs
            })
        
        # Join segments into single polycurve
        if len(segment_ids) > 1:
            joined = rs.JoinCurves(segment_ids, delete_input=False)
            if joined:
                self.joined_id = joined[0] if isinstance(joined, list) else joined
        elif len(segment_ids) == 1:
            self.joined_id = segment_ids[0]
        
        return self.joined_id
    
    def get_intercepts_with_plane(self, station_x):
        """
        Returns ALL intersections with YZ plane at station_x, sorted by Z.
        Handles complex stern geometry with multiple intercepts.
        """
        if not self.segments:
            return []

        origin = rg.Point3d(station_x, 0, 0)
        plane  = rg.Plane(origin, rg.Vector3d.XAxis)

        all_pts = []
        for seg in self.segments:
            if not rs.IsObject(seg['id']):
                continue
            rhino_curve = rs.coercecurve(seg['id'])
            if not rhino_curve:
                continue
            result = rg.Intersect.Intersection.CurvePlane(rhino_curve, plane, 0.001)
            if result:
                for x in result:
                    all_pts.append(x.PointA)

        all_pts.sort(key=lambda p: p.Z)
        return all_pts
    
    def get_inflection_count(self, samples=100):
        """
        Count inflection points (sign changes in curvature).
        Used to evaluate fairing quality.
        """
        if not self.joined_id or not rs.IsObject(self.joined_id):
            return 0
        
        curve = rs.coercecurve(self.joined_id)
        if not curve:
            return 0
        
        # Plane normal for curvature sign check
        ref_normal = rg.Vector3d(*self.plane)
        domain = curve.Domain
        step = domain.Length / samples
        
        inflection_count = 0
        prev_sign = 0

        for i in range(samples + 1):
            t = domain.Min + (i * step)
            tangent = curve.TangentAt(t)
            curv_vec = curve.CurvatureAt(t)
            
            if curv_vec.Length > 0.000001:
                cp = rg.Vector3d.CrossProduct(tangent, curv_vec)
                dot_product = cp * ref_normal
                curr_sign = 1 if dot_product > 0 else -1
                
                if prev_sign != 0 and prev_sign != curr_sign:
                    inflection_count += 1
                prev_sign = curr_sign
        
        return inflection_count
    
    def clamp_to_limits(self):
        """
        Force control points back within hull limits.
        Called after Fair() to prevent geometry from escaping bounds.
        """
        if not self.joined_id or not rs.IsObject(self.joined_id):
            return False
        
        curve = rs.coercecurve(self.joined_id)
        if not isinstance(curve, rg.NurbsCurve):
            return False
        
        tol = 0.001
        clamped = False
        
        for i in range(curve.Points.Count):
            cp = curve.Points[i]
            loc = cp.Location
            new_loc = rg.Point3d(loc)
            
            # Clamp Z
            if self.limits[2][0] is not None and new_loc.Z < self.limits[2][0] - tol:
                new_loc.Z = self.limits[2][0]
                clamped = True
            if self.limits[2][1] is not None and new_loc.Z > self.limits[2][1] + tol:
                new_loc.Z = self.limits[2][1]
                clamped = True
            
            # Clamp Y
            if self.limits[1][0] is not None and new_loc.Y < self.limits[1][0] - tol:
                new_loc.Y = self.limits[1][0]
                clamped = True
            if self.limits[1][1] is not None and new_loc.Y > self.limits[1][1] + tol:
                new_loc.Y = self.limits[1][1]
                clamped = True
            
            # Clamp X
            if self.limits[0][0] is not None and new_loc.X < self.limits[0][0] - tol:
                new_loc.X = self.limits[0][0]
                clamped = True
            
            if clamped:
                curve.Points[i] = rg.ControlPoint(new_loc, cp.Weight)
        
        if clamped:
            # Update Rhino document
            rs.coercerhinoobject(self.joined_id).CommitChanges()
        
        return clamped
    
    def match_to_constraints(self):
        """
        Apply G2 continuity constraints to curve endpoints using CreateMatchCurve.
        Constraint type depends on curve type and boundary_hit tags.
        """
        if not self.joined_id or not rs.IsObject(self.joined_id):
            return None
        
        curve = rs.coercecurve(self.joined_id)
        if not curve:
            return None
        
        # Get start and end points
        start_pt = self.pts[0]
        end_pt = self.pts[-1]
        
        # Determine constraints
        start_tan = start_pt.tangent_vector if start_pt.is_intercept else None
        end_tan = end_pt.tangent_vector if end_pt.is_intercept else None
        
        # If no constraints, return original
        if not start_tan and not end_tan:
            return curve
        
        # Use CreateMatchCurve for G2 continuity at constrained ends
        # This is a simplified version - full implementation would use the actual
        # boundary curve as the target curve
        
        # For now, we enforce tangent direction constraints
        nurbs = curve.ToNurbsCurve()
        if not nurbs:
            return curve
        
        # Clamp ends to prevent movement
        nurbs.Knots.ClampEnd(rg.CurveEnd.Both)
        
        # TODO: Implement full CreateMatchCurve logic when target curves are available
        # For now, just ensure the curve is properly clamped
        
        return nurbs
    
    def fair(self, initial_tol=0.1, max_tol=1.0, tol_increment=0.05, 
             settle_iterations=5, max_outer_iterations=20):
        """
        HEURISTIC FAIRING ENGINE
        
        Outer Loop: Tolerance controller
        Inner Loop: Fair → Match → Clamp → Evaluate
        
        Returns: True if fairing succeeded, False if failed
        """
        if not self.joined_id or not rs.IsObject(self.joined_id):
            print("[{}] No geometry to fair".format(self.name))
            return False
        
        print("\n" + "="*60)
        print("FAIRING: {}".format(self.name))
        print("="*60)
        
        current_tol = initial_tol
        outer_iter = 0
        
        while current_tol <= max_tol and outer_iter < max_outer_iterations:
            print("\n--- Outer Iteration {} | Tolerance: {:.3f} ---".format(
                outer_iter, current_tol))
            
            # INNER LOOP: Settle loop (5 iterations)
            for settle_iter in range(settle_iterations):
                # Get current curve
                curve = rs.coercecurve(self.joined_id)
                if not isinstance(curve, rg.NurbsCurve):
                    curve = curve.ToNurbsCurve()
                if not curve:
                    print("ERROR: Failed to convert to NurbsCurve")
                    return False
                
                # STEP 1: FAIR
                fair_success = curve.Fair(current_tol, 0.0, 2, 2, 5)
                
                # STEP 2: MATCH (apply G2 constraints at boundaries)
                matched_curve = self.match_to_constraints()
                if matched_curve:
                    curve = matched_curve
                
                # STEP 3: CLAMP (force points back to limits)
                self.clamp_to_limits()
                
                # Update document
                doc = sc.doc
                doc.Objects.Replace(self.joined_id, curve)
                
                if settle_iter % 2 == 0:  # Log every other iteration
                    inflections = self.get_inflection_count()
                    print("  Settle {}: Fair={} | Inflections={}".format(
                        settle_iter, "OK" if fair_success else "LOCKED", inflections))
            
            # EVALUATION PHASE
            final_inflections = self.get_inflection_count()
            print("\nEVALUATION: Inflections = {}".format(final_inflections))
            
            if final_inflections == 0:
                print("SUCCESS: {} faired with tolerance {:.3f}".format(
                    self.name, current_tol))
                return True
            else:
                print("REJECTED: {} inflection points found".format(final_inflections))
                current_tol += tol_increment
                outer_iter += 1
        
        print("\nFAILED: {} could not be faired within tolerance limit".format(self.name))
        return False
    
    @property
    def segment_list(self):
        """Debug report of segments"""
        out = ["\n" + "="*30, "SEGMENTS: {}".format(self.name), "-"*30]
        for idx, seg in enumerate(self.segments):
            ids = [p.index for p in seg['points']]
            out.append("Seg {}: {} | Indices: {}".format(idx, seg['type'], ids))
        out.append("="*30)
        return "\n".join(out)


# ============================================================================
# MAIN EXECUTION: PHASED WORKFLOW
# ============================================================================

print("\n" + "="*70)
print("PHASE 0: DATA LOADING & GEOMETRY INITIALIZATION")
print("="*70)

# Build ship limits
ship_limits_matrix = get_limits(profile_nodim, l_bp, b_half, d)
print("Ship limits defined:")
print("  X: [{}, {}]".format(ship_limits_matrix[0][0], ship_limits_matrix[0][1]))
print("  Y: [{}, {}]".format(ship_limits_matrix[1][0], ship_limits_matrix[1][1]))
print("  Z: [{}, {}]".format(ship_limits_matrix[2][0], ship_limits_matrix[2][1]))

# Create boundary curves
profile_data, _ = get_points_from_data(profile_nodim, l_bp, b_whole, d, "profile", ship_limits_matrix)
my_profile_pts = get_point_objects(profile_data, False)
my_profile = MyCurve(my_profile_pts, ship_limits_matrix, [0,1,0], "PROFILE")

fos_data, _ = get_points_from_data(fos_nodim, l_bp, b_whole, d, "fos", ship_limits_matrix)
my_fos_pts = get_point_objects(fos_data, False)
my_fos = MyCurve(my_fos_pts, ship_limits_matrix, [0,1,0], "FOS")

fob_data, _ = get_points_from_data(fob_nodim, l_bp, b_whole, d, "fob", ship_limits_matrix)
my_fob_pts = get_point_objects(fob_data, False)
my_fob = MyCurve(my_fob_pts, ship_limits_matrix, [0,0,1], "FOB")

transom_data, _ = get_points_from_data(transom_nodim, l_bp, b_whole, d, "transom", ship_limits_matrix)
my_transom_pts = get_point_objects(transom_data, False)
my_transom = MyCurve(my_transom_pts, ship_limits_matrix, [1,0,0], "TRANSOM")

station_data, _ = get_points_from_data(offsets_nodim, l_bp, b_whole, d, "station", ship_limits_matrix)
my_station_pts = get_point_objects(station_data, True)

print("\nBoundary curves created:")
print("  Profile: {} points, {} segments".format(len(my_profile.pts), len(my_profile.segments)))
print("  FOS: {} points, {} segments".format(len(my_fos.pts), len(my_fos.segments)))
print("  FOB: {} points, {} segments".format(len(my_fob.pts), len(my_fob.segments)))
print("  Transom: {} points, {} segments".format(len(my_transom.pts), len(my_transom.segments)))
print("  Stations: {} raw station groups".format(len(my_station_pts)))

# ============================================================================
# PHASE 1: GLOBAL BOUNDARY FAIRING
# ============================================================================

print("\n" + "="*70)
print("PHASE 1: GLOBAL BOUNDARY FAIRING")
print("="*70)

# Fair in order: Transom → Profile → FOB → FOS
my_transom.fair()
my_profile.fair()
my_fob.fair()
my_fos.fair()

# ============================================================================
# PHASE 2: INTERCEPT RECALCULATION
# ============================================================================

print("\n" + "="*70)
print("PHASE 2: STATION INTERCEPT RECALCULATION")
print("="*70)

my_stations = build_station_segments(
    my_station_pts,
    my_fos,
    my_fob,
    my_profile,
    ship_limits_matrix,
    [1,0,0]
)

print("Station segments created: {}".format(len(my_stations)))

# ============================================================================
# PHASE 3: STATION FAIRING
# ============================================================================

print("\n" + "="*70)
print("PHASE 3: STATION FAIRING")
print("="*70)

for station in my_stations:
    station.fair(initial_tol=0.05, max_tol=0.5)

print("\n" + "="*70)
print("FAIRING COMPLETE")
print("="*70)

rs.EnableRedraw(True)