#! /usr/bin/env python
SOURCE_DIR='/home/hexiang/git/SW42DRM/SRC'
import h5py
import scipy as sp
import time
import pickle

from ESSI_location import * 
from interpolation_function_array import *
from numpy.linalg import inv
import matlab.engine



######################### usr input variable ###################################################################
model_name=input('Specify the model name: ');

sw4_motion_path=input('Specify the sw4 motion directory: ');    #'/home/hexiang/SMR_work/smr/sw4_motion/M5.5_ESSI_srf.sw4output';
sample_time_step_interval=input('Specify the interval of time steps for sampling: ');
Interpolation_Radius=input('Specify initial search radius: ');
scale_ratio=input('Specify radius scale ratio: ');

########################## Ending usr input ####################################################################

DRM_hdf5_filename=model_name+".h5.drminput"

matlab_path=SOURCE_DIR+'/sw4_tools';

No_new_node=new_node.shape[0]

boundary_node=sp.loadtxt("boundary_node.txt",dtype=sp.int32)

exterior_node=sp.loadtxt("exterior_node.txt",dtype=sp.int32)

element=sp.loadtxt("DRM_element.txt",dtype=sp.int32)


# u_total=sp.loadtxt("u_total.txt")

############################################ Generate time data #####################################
eng = matlab.engine.start_matlab()

eng.cd(matlab_path, nargout=0)

[u,t,No_time_step]=eng.read_station(sw4_motion_path,0,0,0);

original_time_step= t/(No_time_step-1);

sampled_time_step=original_time_step*sample_time_step_interval;

sampled_No_time_step=(No_time_step-1)/sample_time_step_interval+1;

Time=[i*sampled_time_step for i in xrange(0,sampled_No_time_step)];

print Time;


# ####################################################################################################

# ######################################### generate DRM node and element data########################

# Ne=exterior_node.shape[0]
# Nb=boundary_node.shape[0]
# Nt=Ne+Nb

# Exterior_node=sp.zeros((Ne))
# Boundary_node=sp.zeros((Nb))

# for i1 in xrange(0,Ne):
# 	Exterior_node[i1]=exterior_node[i1,0]
# for i2 in xrange(0,Nb):
# 	Boundary_node[i2]=boundary_node[i2,0]

# all_nodes=sp.hstack((Boundary_node,Exterior_node))
# is_boundary_node=sp.zeros(Nt, dtype=sp.int32)
# is_boundary_node[0:Nb]=1

# ######################################################################################################

# #################################### generate displacement and acceleration data ###################
# # station_grid_space=10;
# # search_scale=1.1;
# # Interpolation_Radius=station_grid_space*search_scale;
# # scale_ratio=1.2;

# 	############search all interpolation nodes#####################################################
# def interpolation_nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio):
# 	No_station=station.shape[0];
# 	interpolation_nodes=[];
# 	interpolation_nodes_index=0
# 	for i4 in xrange(0,No_station):
# 		selected_points=sp.zeros((7));
# 		if (station[i4,3]-new_node_x)*(station[i4,3]-new_node_x)+(station[i4,4]-new_node_y)*(station[i4,4]-new_node_y)+(station[i4,5]-new_node_z)*(station[i4,5]-new_node_z)<=Interpolation_Radius*Interpolation_Radius:
# 			selected_points[0:6]=station[i4,0:6]
# 			selected_points[6]=i4;
# 			interpolation_nodes.append(selected_points);
# 			interpolation_nodes_index=interpolation_nodes_index+1
# 	# print interpolation_nodes,interpolation_nodes_index,"I am here"
# 	while interpolation_nodes_index<4:
# 		print "serach radius R is too small for node ", new_node_index, ", search again using",scale_ratio, "*R..."
# 		Interpolation_Radius=Interpolation_Radius*scale_ratio
# 		interpolation_nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio)
# 	while interpolation_nodes_index>10:
# 		print "serach radius R is too big for node ", new_node_index, ", search again using R/",scale_ratio,"..."
# 		Interpolation_Radius=Interpolation_Radius/scale_ratio
# 		interpolation_nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio)
# 	print "Done interpolation nodes searching"
# 	return interpolation_nodes


# # def interpolated_motion(interpolation_nodes,new_node_x,new_node_y,new_node_z,u_total):
# # 	# No_station=(u_total.shape[1]-1)/3;
# # 	No_interpolation_nodes=len(interpolation_nodes)
# # 	No_time_step=u_total.shape[0]
# # 	node_motion_component=sp.zeros((3,No_time_step))

# # 	for i7 in xrange(0,No_time_step):  
# # 	# for i7 in xrange(0,1): 
# # 		for i6 in xrange(0,3):  # 0 1 2 for ux uy uz
# # 			RHS=sp.zeros((No_interpolation_nodes,1))
# # 			LHS=[]
# # 			for i5 in xrange(0,No_interpolation_nodes):
# # 				LHS_component=sp.zeros((No_interpolation_nodes))
# # 				for i12 in xrange(0,No_interpolation_nodes):
# # 					LHS_component[i12]=fun_list[i12](interpolation_nodes[i5][3],interpolation_nodes[i5][4],interpolation_nodes[i5][5])
# # 				# print LHS_component, "\n"
# # 				LHS.append(LHS_component)
# # 				RHS_column=int(interpolation_nodes[i5][6]*3+i6+1)
# # 				RHS[i5,0]=u_total[i7][RHS_column]
# # 			LHS=sp.array(LHS)
# # 	 		# print RHS,"\n"
# # 	 		# print LHS,"\n"
# # 			inv_LHS=inv(LHS)
# # 			interpolation_parameter=np.dot(inv_LHS, RHS)
# # 			# print interpolation_parameter, "\n"
# # 			motion=0;
# # 			for i8 in xrange(0,No_interpolation_nodes):
# # 				motion=motion+interpolation_parameter[i8,0]*fun_list[i8](new_node_x,new_node_y,new_node_z)
# # 			node_motion_component[i6,i7]=motion
# # 	return node_motion_component

# 	#####################finally generate motion for every DRM node##############################################

# def getField (new_node_x,new_node_y,new_node_z,new_node_index,sample_time_step_interval):
# 	interpolation_nodes=interpolation_nodes(station,new_node_x,new_node_y,new_node_z,Interpolation_Radius,new_node_index,scale_ratio);
# 	No_interpolation_nodes=len(interpolation_nodes);
# 	original_velocity=sp.zeros((3,No_time_step));
# 	original_displacement=sp.zeros((3,No_time_step));
# 	original_acceleration=sp.zeros((3,No_time_step));
# 	sampled_displacement=sp.zeros((3,sampled_No_time_step));
# 	sampled_acceleration=sp.zeros((3,sampled_No_time_step));


# 	for i7 in xrange(0,No_time_step):  
# 		for i6 in xrange(0,3):  # 0 1 2 for ux uy uz
# 			RHS=sp.zeros((No_interpolation_nodes,1))
# 			LHS=[]
# 			for i5 in xrange(0,No_interpolation_nodes):
# 				LHS_component=sp.zeros((No_interpolation_nodes))
# 				for i12 in xrange(0,No_interpolation_nodes):
# 					LHS_component[i12]=fun_list[i12](interpolation_nodes[i5][3],interpolation_nodes[i5][4],interpolation_nodes[i5][5])
# 				# print LHS_component, "\n"
# 				LHS.append(LHS_component)

# 				station_id_x=interpolation_nodes[i5][0];
# 				station_id_y=interpolation_nodes[i5][1];
# 				station_id_z=interpolation_nodes[i6][2];

# 				[u,t,no_time_step]=read_station(sw4_motion_path,station_id_x,station_id_y,station_id_z);

# 				RHS[i5,0]=u[i7][i6]

# 			LHS=sp.array(LHS)
# 	 		# print RHS,"\n"
# 	 		# print LHS,"\n"
# 			inv_LHS=inv(LHS)
# 			interpolation_parameter=np.dot(inv_LHS, RHS)
# 			# print interpolation_parameter, "\n"
# 			node_velocity=0;
# 			for i8 in xrange(0,No_interpolation_nodes):
# 				node_velocity=node_velocity+interpolation_parameter[i8,0]*fun_list[i8](new_node_x,new_node_y,new_node_z)
# 			original_velocity[i6,i7]=node_velocity;
# 	for x10 in xrange(1,No_time_step):
# 		original_displacement[:,x10]=original_displacement[:,x10-1]+original_velocity[:,x10]*original_time_step;
# 		original_acceleration[:,x10]=(original_velocity[:,x10]-original_velocity[:,x10-1])/original_time_step;
# 	for x11 in xrange(0,sampled_No_time_step):
# 		sampled_displacement[:,x11]=original_displacement[:,x11*sample_time_step_interval];
# 		sampled_acceleration[:,x11]=original_acceleration[:,x11*sample_time_step_interval];
# 	return sampled_displacement,sampled_acceleration;

# sampled_acceleration=[]
# sampled_displacement=[]


# for i9 in xrange(0,No_new_node):
# # for i9 in xrange(0,3):
# 	sampled_displacement,sampled_acceleration=getField(new_node[i9,1],new_node[i9,2],new_node[i9,3],new_node[i9,0],sample_time_step_interval);
# 	sampled_acceleration.append(sampled_acceleration)
# 	sampled_displacement.append(sampled_displacement)

# sampled_acceleration=sp.array(sampled_acceleration)
# sampled_displacement=sp.array(sampled_displacement)


# #############################from displacement generate velocity and acceleration#############################

# # u=sp.zeros((3*Nt,No_time_step))
# # a=
# # for i10 in xrange(1,No_time_step):
# # 	v[:,i10]=(node_motion[:,i10]-node_motion[:,i10-1])/time_step
# # for i11 in xrange(1,No_time_step):
# # 	a[:,i11]=(v[:,i11]-v[:,i11-1])/time_step


# ############################################write output hdf5 file###################################
# h5file=h5py.File(DRM_hdf5_filename,"w")
# h5file.create_dataset("Elements", data=element)
# h5file.create_dataset("DRM Nodes", data=all_nodes)
# h5file.create_dataset("Is Boundary Node", data=is_boundary_node)
# h5file.create_dataset("Number of Exterior Nodes", data=Ne)
# h5file.create_dataset("Number of Boundary Nodes", data=Nb)
# h5file.create_dataset("Time", data=Time)
# h5file.create_dataset("Accelerations", data=sampled_acceleration)
# h5file.create_dataset("Displacements", data=sampled_displacement)

# h5file.close()
# ##################################################################################################




























