import rhinoscript.userinterface
import rhinoscript.geometry
import rhinoscriptsyntax as rs

__commandname__ = "SolidSplit"

def SplitObject(solid, cSrf):
    
    preInnerSrf = rs.CopyObject(cSrf)
    innerSrfs = rs.TrimBrep(preInnerSrf, solid)
    if not innerSrfs:
        rs.DeleteObject(preInnerSrf)
        return [solid]
    solids = []
    solids.append(solid)
    
    for srf in innerSrfs:
        newSolids = []
        for obj in solids:
            splitObjs = rs.SplitBrep(obj, srf, True)
            if not splitObjs:
                newSolids.append(obj)
            else:
                for sObj in splitObjs:
                    toJoin = [sObj, srf]
                    newSolids.append(rs.JoinSurfaces(toJoin))
                rs.DeleteObjects(splitObjs)
        solids = newSolids
    
    rs.DeleteObjects(innerSrfs)
    
    return solids

def RunCommand( is_interactive ):
    
    filter = rs.filter.polysurface
    objs = rs.GetObjects("Select solid objects to split", filter)
    if not objs: return 1
    
    solids = []
    for obj in objs:
        if rs.IsObjectSolid(obj):
            solids.append(obj)
    if len(solids) == 0:
        print "No solid object found"
        return 1
        
    cSrfs = rs.GetObjects("Select cutting surfaces", filter)
    if not cSrfs:
        return 1
    
    rs.EnableRedraw(False)
    
    for srf in cSrfs:
        newSolids = []
        for solid in solids:
            newSolids.extend(SplitObject(solid, srf))
        solids = newSolids

    rs.EnableRedraw(True)
        
    return 0

RunCommand(True)