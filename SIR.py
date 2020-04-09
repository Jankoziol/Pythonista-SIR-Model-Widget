# SIR-Model

import ui
import matplotlib.pyplot as plt
import io
import numpy as np

def odeint(df,y0,t):
	returner=[y0]
	for i in range(1,len(t)):
		h = t[i]-t[i-1]
		k1 = df(y0)
		k2 = df(y0+0.5*h*k1)
		k3 = df(y0+0.5*h*k2)
		k4 = df(y0+h*k3)
		y0 = y0 + h*1.0/6.0*(k1+2*k2+2*k3+k4)
		returner.append(y0)
	return np.array(returner)
	
	
def plot_view(plt,img_view):
	b = io.BytesIO()
	plt.savefig(b)
	img_view.image = ui.Image.from_data(b.getvalue())
	return img_view
	
def slider_action(sender):

	v = sender.superview
	T = v['slider1'].value*5
	R = v['slider2'].value*5
	I0 = v['slider3'].value*0.1
	Tmax = v['slider4'].value*20
	v['label6'].text = str(T)
	v['label7'].text = str(R)
	v['label8'].text = str(I0)
	v['label9'].text = str(Tmax)
	y_deriv = lambda y : np.array([-T*y[0]*y[1],T*y[0]*y[1]-R*y[1],R*y[1]])
	x = np.linspace(0,Tmax,10000)
	SIR = odeint(y_deriv,[1-I0,I0,0],t=x)
	
	plt.close()
	plt.plot(x,SIR[:,0],color='blue',label='Susceptible People')
	plt.plot(x,SIR[:,1],color='red',label='Infected People')
	plt.plot(x,SIR[:,2],color='green',label='Recovered People')
	plt.legend()
	plt.grid()
	plot_view(plt,v['imageview1'])
	
	
	
v = ui.load_view('SIR')
slider_action(v['slider1'])
slider_action(v['slider2'])
slider_action(v['slider3'])
slider_action(v['slider4'])

if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('sheet')
else:
	# iPhone
	v.present()

