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

ship_limits_matrix = get_limits(profile_nodim, l_bp, b_half, d)

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
                    point_objects[i].prev_pt = point_objects[i-1]
                if i < len(point_objects) - 1:
                    point_objects[i].next_pt = point_objects[i+1]
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
                        current_station_objects[i].prev_pt = current_station_objects[i-1]
                    if i < len(current_station_objects) - 1:
                        current_station_objects[i].next_pt = current_station_objects[i+1]
                    
                all_station_objects.append(current_station_objects)
    
        return all_station_objects