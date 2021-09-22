import onnx
import numpy as np
from ortools.linear_solver import pywraplp
import caffe2.python.onnx.backend as backend

def onnxcall(A,rep):
	k = np.array(A).astype(np.float32)
	o = rep.run(k)
	return o

def find_ub(ar,pos,p,rep):
	while p >= 0.0001:

		output = []
		for i in range(len(ar)):
			out = onnxcall(ar[i],rep)
			output.append(out[0][0][pos])

		#print(output)
		maxi = np.max(output)
		maxi_pos = output.index(maxi)
		maxi_inp = ar[maxi_pos] 
		prev = ar.copy()

		zipped = zip(*prev)

		arr = []
		for i in list(zipped):
			arr.append(set(i))

		A = []
		for i in arr:
			t = list(i)
			A.append(t)

		for i in range(len(maxi_inp)):
			if maxi_inp[i] == A[i][0]:
				A[i][1] = (maxi_inp[i]+A[i][1])/2
			else:
				A[i][0] = (maxi_inp[i]+A[i][0])/2

		#ar.clear()
		ar = [[i,j,k,l,m] for i in A[0] for j in A[1] for k in A[2] for l in A[3] for m in A[4]]

		if maxi_inp[pos] == A[pos][0]:
			p = maxi_inp[pos] - A[pos][1]
		else:
			p = maxi_inp[pos] - A[pos][0]
		#print(p)
    
		if p < 0.0001:
			#print(f"max[{pos}]={maxi}")
			return maxi

def find_lb(ar,pos,p,rep):
	while p >= 0.0001:

		output = []
		for i in range(len(ar)):
			out = onnxcall(ar[i],rep)
			output.append(out[0][0][pos])

		mini = np.min(output)
		mini_pos = output.index(mini)
		mini_inp = ar[mini_pos] 
		prev = ar.copy()

		zipped = zip(*prev)

		arr = []
		for i in list(zipped):
			arr.append(set(i))

		A = []
		for i in arr:
			t = list(i)
			A.append(t)

		for i in range(len(mini_inp)):
			if mini_inp[i] == A[i][0]:
				A[i][1] = (mini_inp[i]+A[i][1])/2
			else:
				A[i][0] = (mini_inp[i]+A[i][0])/2

		ar = [[i,j,k,l,m] for i in A[0] for j in A[1] for k in A[2] for l in A[3] for m in A[4]]

		if mini_inp[pos] == A[pos][0]:
			p = mini_inp[pos] - A[pos][1]
		else:
			p = mini_inp[pos] - A[pos][0]

		#print(p)
		if p < 0.0001:
			#print(f"Min[{pos}]={mini}")
			return mini
		

def new_py(file_name,input_lb,input_ub):
	m = onnx.load(file_name)
	rep = backend.prepare(m, device="CPU")

	inp = []
	for i in range(len(input_lb)):
		inp.append([input_lb[i],input_ub[i]])

	check = [[i,j,k,l,m] for i in inp[0] for j in inp[1] for k in inp[2] for l in inp[3] for m in inp[4]]

	u = []
	l = []
	for i in range(len(input_lb)):
		diff = input_ub[i] - input_lb[i]
		ub = find_ub(check,i,diff,rep)
		#print("u,i",ub,i)
		u.append(ub)
		#print("Enter lower bound")
		lb = find_lb(check,i,diff,rep)
		#print("l,i",lb,i)
		l.append(lb)
	print(l)
	print(u)
	return [l,u]

#SCIP optimization function
def scip_py(input_lb,input_ub,bias,weight):

	
	positive_infnity = float('inf')
	negative_infnity = float('-inf')
	#create a new model
	solver = pywraplp.Solver.CreateSolver('SCIP')

	#get data from onnx
	inp = len(bias) + 1

	no = [len(input_ub)]
	for i in range(inp-1):
		no.append(len(bias[i]))

	b = []
	for i in range(inp):
		b.append([])
		for j in range(no[i]):
			b[i].append(0)

	z = []
	for i in range(inp):
		z.append([])
		for j in range(no[i]):
			z[i].append(0)

	t = []
	for i in range(inp):
		t.append([])
		for j in range(no[i]):
			t[i].append(0)

	w = []
	arr = []
	for i in range(no[0]):
		arr.append(0)
	w.append(arr)
	for i in weight:
		w.append(i)

	Y = []
	for i in range(no[inp-1]):
		Y.append(0)

	for i in range(inp):
		for j in range(no[i]):
			z[i][j] = solver.NumVar(negative_infnity,positive_infnity , f"x{i}{j}")

			if i!= 0:
				if i!= inp-1:
					t[i][j] = solver.IntVar(0, 1, f"t{i}{j}")
					solver.Add(t[i][j] >= 0)
					solver.Add(t[i][j] <= 1)
				b[i][j] = bias[i-1][j]

	for i in range(len(input_lb)):
		solver.Add(z[0][i] >= input_lb[i])

	for i in range(len(input_ub)):
		solver.Add(z[0][i] <= input_ub[i]) 

	summ = b

	for i in range(inp):
		for j in range(no[i]):
			for k in range(no[i-1]):
				if i!=0:
					summ[i][j] = summ[i][j] + w[i][k][j]*z[i-1][k]

	M = 100000

	for k in range(no[inp-1]):
		Y[k] = summ[inp-1][k]

	#set constraints
	for i in range(1,inp-1):
		for j in range(no[i]):
			solver.Add(z[i][j] >= summ[i][j])
			solver.Add(z[i][j] <= summ[i][j] + M*t[i][j])
			solver.Add(z[i][j] <= M*(1-t[i][j]))

	l = []
	#set Objective Minimize
	for i in range(no[inp-1]):
		solver.Minimize(Y[i])
		status_l = solver.Solve()
		if status_l== pywraplp.Solver.OPTIMAL:
			l.append(solver.Objective().Value())

	u = []
	#set Objective Maximize
	for i in range(no[inp-1]):
		solver.Maximize(Y[i])
		status_u = solver.Solve()
		if status_u== pywraplp.Solver.OPTIMAL:
			u.append(solver.Objective().Value())

	return [l,u]

