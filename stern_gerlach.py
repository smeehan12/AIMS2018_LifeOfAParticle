######################################
# Stern-Gerlach Experiment Simulator
#
#
#
######################################

import random as r
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

############################
# v0 : 
# generation  : 
#   - classical - fully random
# observation : 
#   - classical - state persists
############################
def unpolarized_v0():
    val = r.uniform(-1.0,1.0)
    return val
    
def observe_v0(atom, direction, gradient):
        
    if direction=="z":
        atom["z"]["obs"] = gradient*atom["z"]["val"]
        atom["x"]["obs"] = 0
    elif direction=="x":
        atom["x"]["obs"] = gradient*atom["x"]["val"]
        atom["z"]["obs"] = 0
        
    return atom

############################
# v1 : 
# generation  : 
#   - two states only 
# observation : classical 
#   - classical - state persists
############################
def unpolarized_v1():
    val = r.uniform(-1.0,1.0)
    if val>=0:
        val=1
    else:
        val=-1
    return val
    
def observe_v1(atom, direction, gradient):
        
    if direction=="z":
        atom["z"]["obs"] = gradient*atom["z"]["val"]
        atom["x"]["obs"] = 0
    elif direction=="x":
        atom["x"]["obs"] = gradient*atom["x"]["val"]
        atom["z"]["obs"] = 0
        
    return atom
    
############################
# v2 : 
# generation  : 
#   - random/unknown "?" mystery state
# observation : 
#   - if "?" then randomly choose state, otherwise follow what we know
############################
def unpolarized_v2():
    val = "?"
    return val
    
def observe_v2(atom, direction, gradient):
        
    if direction=="z":
        if atom["z"]["val"]=="?":
            val = r.uniform(-1.0,1.0)
            if val>=0:
                val=1
            else:
                val=-1
            atom["z"]["obs"] = gradient*val
            atom["x"]["obs"] = 0
            atom["z"]["val"] = val
        else:
            atom["z"]["obs"] = gradient*atom["z"]["val"]
            atom["x"]["obs"] = 0
    elif direction=="x":
        if atom["x"]["val"]=="?":
            val = r.uniform(-1.0,1.0)
            if val>=0:
                val=1
            else:
                val=-1
            atom["x"]["obs"] = gradient*val
            atom["z"]["obs"] = 0
            atom["x"]["val"] = val
        else:
            atom["x"]["obs"] = gradient*atom["x"]["val"]
            atom["z"]["obs"] = 0
        
    return atom
    
############################
# v3 : 
# generation  : 
#   - random/unknown "?" mystery state
# observation : depends on "dir"
#   - if "?" for "dir" then randomly choose state behavior for "dir", otherwise follow what we know
#   - if observing "dir1" then "dir2" val is reset to "?"
############################
def unpolarized_v3():
    val = "?"
    return val
    
def observe_v3(atom, direction, gradient):
        
    if direction=="z":
        if atom["z"]["val"]=="?":
            val = r.uniform(-1.0,1.0)
            if val>=0:
                val=1
            else:
                val=-1
            atom["z"]["obs"] = gradient*val
            atom["x"]["obs"] = 0
            atom["z"]["val"] = val
        else:
            atom["z"]["obs"] = gradient*atom["z"]["val"]
            atom["x"]["obs"] = 0
        #break the x direction
        atom["x"]["val"] = "?"
    elif direction=="x":
        if atom["x"]["val"]=="?":
            val = r.uniform(-1.0,1.0)
            if val>=0:
                val=1
            else:
                val=-1
            atom["x"]["obs"] = gradient*val
            atom["z"]["obs"] = 0
            atom["x"]["val"] = val
        else:
            atom["x"]["obs"] = gradient*atom["x"]["val"]
            atom["z"]["obs"] = 0
        #break the z direction
        atom["z"]["val"] = "?"
        
    return atom

# nevents
nevents=1000

# magnetic field gradient
gradient = 5

# runtype
runtype = 3

# for storing and plotting
vals_z_0 = []
vals_x_0 = []

vals_z_1 = []
vals_x_1 = []

vals_z_2 = []
vals_x_2 = []

vals_z_3 = []
vals_x_3 = []

for i in range(nevents):

    # a new atom
    # know = Do I know the value of the spin?
    # val  = The value/state endowed by nature
    # obs  = The value I observe
    atom = {"z" : {"know":0 , "val":"?", "obs":"?"} , "x" : {"know":0 , "val":"?", "obs":"?"}}
    
    # it is born in the silver boiler
    if runtype==0:
        atom["z"]["val"] = unpolarized_v0()
        atom["x"]["val"] = unpolarized_v0()
    elif runtype==1:
        atom["z"]["val"] = unpolarized_v1()
        atom["x"]["val"] = unpolarized_v1()
    elif runtype==2:
        atom["z"]["val"] = unpolarized_v2()
        atom["x"]["val"] = unpolarized_v2()
    elif runtype==3:
        atom["z"]["val"] = unpolarized_v3()
        atom["x"]["val"] = unpolarized_v3()
    else:
        print "NOT ALLOWED runtype"
        break
        
    # peep on its properties
    print atom
    
    # send it through the first apparatus with Z magnetic field gradient
    if runtype==0:
        atom = observe_v0(atom, "z", gradient)
    elif runtype==1:
        atom = observe_v1(atom, "z", gradient)
    elif runtype==2:
        atom = observe_v2(atom, "z", gradient)
    elif runtype==3:
        atom = observe_v3(atom, "z", gradient)
    else:
        print "NOT ALLOWED runtype"
        break    

    
    # save observations on screen
    vals_z_0.append(atom["z"]["obs"])
    vals_x_0.append(atom["x"]["obs"])

    # only allow the atoms travelling in + direction to pass
    if atom["z"]["obs"]<0:
        continue
        
    # observe again in Z
    # send it through the first apparatus with Z magnetic field gradient
    if runtype==0:
        atom = observe_v0(atom, "z", gradient)
    elif runtype==1:
        atom = observe_v1(atom, "z", gradient)
    elif runtype==2:
        atom = observe_v2(atom, "z", gradient)
    elif runtype==3:
        atom = observe_v3(atom, "z", gradient)
    else:
        print "NOT ALLOWED runtype"
        break    
    
    # save observations on screen
    vals_z_1.append(atom["z"]["obs"])
    vals_x_1.append(atom["x"]["obs"])

    # now observe in X
    # send it through the first apparatus with Z magnetic field gradient
    if runtype==0:
        atom = observe_v0(atom, "x", gradient)
    elif runtype==1:
        atom = observe_v1(atom, "x", gradient)
    elif runtype==2:
        atom = observe_v2(atom, "x", gradient)
    elif runtype==3:
        atom = observe_v3(atom, "x", gradient)
    else:
        print "NOT ALLOWED runtype"
        break    
    
    # save observations on screen
    vals_z_2.append(atom["z"]["obs"])
    vals_x_2.append(atom["x"]["obs"])
    
    # only allow the atoms travelling in + direction to pass
    if atom["x"]["obs"]<0:
        continue
        
    # now observe in X
    # send it through the first apparatus with Z magnetic field gradient
    if runtype==0:
        atom = observe_v0(atom, "z", gradient)
    elif runtype==1:
        atom = observe_v1(atom, "z", gradient)
    elif runtype==2:
        atom = observe_v2(atom, "z", gradient)
    elif runtype==3:
        atom = observe_v3(atom, "z", gradient)
    else:
        print "NOT ALLOWED runtype"
        break    
    
    # save observations on screen
    vals_z_3.append(atom["z"]["obs"])
    vals_x_3.append(atom["x"]["obs"])


print "SIZES : "
print len(vals_z_0)
print len(vals_x_0)
print len(vals_z_1)
print len(vals_x_1)
print len(vals_z_2)
print len(vals_x_2)
print len(vals_z_3)
print len(vals_x_3)




fig = plt.figure(figsize=(16, 8))

gs = gridspec.GridSpec(2, 4)
gs.update(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)

a00 = plt.subplot(gs[0, 0])
a10 = plt.subplot(gs[1, 0])
a01 = plt.subplot(gs[0, 1])
a11 = plt.subplot(gs[1, 1])
a02 = plt.subplot(gs[0, 2])
a12 = plt.subplot(gs[1, 2])
a03 = plt.subplot(gs[0, 3])
a13 = plt.subplot(gs[1, 3])

a00.hist(vals_z_0,bins=100); a00.set_xlim(-10,10); a00.set_xlabel("Z Deflection"); a00.set_ylabel("# Atoms"); a00.set_title("#1 : Obs Z");
a10.hist(vals_x_0,bins=100); a10.set_xlim(-10,10); a10.set_xlabel("Z Deflection"); a10.set_ylabel("# Atoms");
a01.hist(vals_z_1,bins=100); a01.set_xlim(-10,10); a01.set_xlabel("Z Deflection"); a01.set_ylabel("# Atoms"); a01.set_title("#2 : Filt Z/Obs Z");
a11.hist(vals_x_1,bins=100); a11.set_xlim(-10,10); a11.set_xlabel("Z Deflection"); a11.set_ylabel("# Atoms");
a02.hist(vals_z_0,bins=100); a02.set_xlim(-10,10); a02.set_xlabel("Z Deflection"); a02.set_ylabel("# Atoms"); a02.set_title("#3 : Obs X");
a12.hist(vals_x_0,bins=100); a12.set_xlim(-10,10); a12.set_xlabel("Z Deflection"); a12.set_ylabel("# Atoms");
a03.hist(vals_z_1,bins=100); a03.set_xlim(-10,10); a03.set_xlabel("Z Deflection"); a03.set_ylabel("# Atoms"); a03.set_title("#4 : Filt X/Obs Z");
a13.hist(vals_x_1,bins=100); a13.set_xlim(-10,10); a13.set_xlabel("Z Deflection"); a13.set_ylabel("# Atoms");



plt.show()












