"""
simple demonstration and testing of cad cam ship hull algorithms
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

#define points of curve, all of them will be on the plane with z = 0
points_str = """
0,0,0
0,2,0
0,5,0
1,6,0
3,7,0
4,8,0
4,9,0
5,11,0
7,13,0
8,12,0
8,11,0
10,10,0
12,10,0
"""
#data cleanup 

limits = [
    [0.0, None], # Row 0: X
    [0.0,  None], # Row 1: Y (Min is 0.0, Max is no limit)
    [0.0,  None]  # Row 2: Z (Min is 0.0, Max is no limit)
]

#---------FUNCTIONS OUTSIDE OF CLASSES---------
def get_points_from_data(data_string):
    """
    """
    lines = data_string.strip().split('\n')
    all_points = []
    for line in lines:
        if not line.strip(): continue
        x, y, z = map(float, line.split(","))
        ready_points = [x, y, z]
        all_points.append(ready_points)
    return all_points



    
print(get_points_from_data(points_str))
print(type(get_points_from_data(points_str)))

my_points = get_points_from_data(points_str)
pts_points = rs.AddPoints(my_points)

# curve_points = rs.AddInterpCurve(pts_points)

class MyPoint:
    def __init__(self, original_id, limits, index, is_original, pt_type, is_intercept):
        self.id = original_id
        self.limits = limits
        self.index = index
        self.is_original = is_original
        self.pt_type = pt_type
        self.is_intercept = is_intercept
        self.original_coords = rs.PointCoordinates(self.id)

        #check the pt_type for plane vector 
        if self.pt_type in ["fos", "profile"]:
            self.plane = [0,1,0]
        elif self.pt_type == "fob":
            self.plane = [0,0,1]
        else:
            self.plane = [1,0,0] #for transom and stations
        
        self.prev = None
        self.next = None

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
        line_matrix = [0, 0]
        neighbors = [self.prev, self.next]
        tolerance = 0.001
        
        current_coords = rs.PointCoordinates(self.id)

        for index, neighbor in enumerate(neighbors):
            if not neighbor:
                continue
            neighbor_coords = rs.PointCoordinates(neighbor.id)

            #we take the plane vector and only check the coordinates that correspond to the zero values of the plane vector 
            for axis in range(3):
                if self.plane[axis] == 0:
                    dif = abs(current_coords[axis] - neighbor_coords[axis])
                    if dif <= tolerance:
                        line_matrix[index] = 1
                        #if one axis is colinear (except for the non zero in the plane vector), then we can stop checking
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
    
    

class MyCurve:
    def __init__(self, point_objects, limits, plane_vector):
        #attributes
        self.pts = point_objects
        self.limits = limits
        self.plane = plane_vector
        self.id = None #the guid of the joined polycurve
        self.segment_matrix = []

        self.rebuild()

    def rebuild(self):
        """
        this method creates the rhino polycurve, it checks the line matrix indices, 0 or 1
        reminder [0,1] means a line segment begins
        [1,1] a line segment is prior and after the current point 
        [1,0] a line segment finishes => if more points after, a b spline begins
        [0,0] a bspline continues or ends if no points exist after or begins if no point is before
        checking index of point helps the alorithm (could be dangerous to only go by logic, might also manually check existence of points)
        """
        if self.id and rs.IsObject(self.id):
            rs.DeleteObject(self.id)
        
        pts = self.pts 
        if len(pts) < 2: return None #rhino needs atleast two points to create curve

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
        #now we draw the geometry using the rhino tools, reminder, if the first element of segment matrix is a 1 it means that all the points of this row belong to one straight line 
        #segment, if the first element is 0 then its a bspline

        rhino_segments = []
        for row in self.segment_matrix:
            seg_type = row[0] 
            coords = [rs.PointCoordinates(p.id) for p in row[1:]]

            if seg_type == 1:
                rhino_segments.append(rs.AddLine(coords[0], coords[-1]))
            else:
                rhino_segments.append(rs.AddInterpCurve(coords))
        if rhino_segments:
            self.id = rs.JoinCurves(rhino_segments, delete_input=True)
        
        return self.id
    
    @property
    def segment_list(self):
        """ The property you call at the end to see the results. """
        out = ["\n" + "="*30, "SEGMENT REPORT", "-"*30]
        for idx, row in enumerate(self.segment_matrix):
            t = "LINE" if row[0] == 1 else "BSPLINE"
            ids = [p.index for p in row[1:]]
            out.append("Seg {}: {} | Indices: {}".format(idx, t, ids))
        out.append("="*30)
        return "\n".join(out)


    
# --- ASSEMBLY & INSPECTION ---
# 1. Create objects and stitch them (REQUIRED for the logic to work)
objs = [MyPoint(p_id, limits, idx, True, "fob", False) for idx, p_id in enumerate(pts_points)]
for idx in range(len(objs)):
    if idx > 0: objs[idx].prev = objs[idx-1]
    if idx < len(objs) - 1: objs[idx].next = objs[idx+1]

# 2. MANUAL CHECK: Change this index to inspect different points
i = 12

# 3. PRINT OUTPUT
p = objs[i]
print("-" * 30)
print("POINT INDEX: {}".format(p.index))
print("COORDS:      {}".format(rs.PointCoordinates(p.id)))
print("-" * 30)
print("IS_CONSTRAINED: {}".format(p.is_constrained))
print("LIMITS_BOOL:    {}".format(p.limits_bool_list))
print("IS_LINE [P,N]:  {}".format(p.is_line))
print("-" * 30)
print("TANGENT_BOOL:    {}".format(p.is_tangent))

# --- HOW TO CALL IT ---
hull = MyCurve(objs, limits, [0,0,1])
print(hull.segment_list) # <--- Just print the property at the end