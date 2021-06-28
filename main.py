

from PyQt5 import QtCore, QtGui, QtWidgets
from scipy import signal
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq,ifft,fftshift,ifftshift,rfft,rfftfreq,irfft
import cmath
from PyQt5.QtWidgets import QFileDialog
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.figure import Figure
import scipy.io.wavfile
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import Ui_MainWindow
import os



# class definition for application window components like the main_window_class
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow,self).__init__()
        self.main_window_class = Ui_MainWindow()
        self.main_window_class.setupUi(self)
        self.main_window_class.actionNew.triggered.connect(self.open_newwindow)
        self.main_window_class.resume_button.clicked.connect(self.play_back)
        #self.main_window_class.lim.clicked.connect(self.limits)
        self.main_window_class.back_button.clicked.connect(self.backword)
        self.main_window_class.forword_button.clicked.connect(self.forword)
        self.main_window_class.zin.clicked.connect(self.zoomin)
        self.main_window_class.zout.clicked.connect(self.zoomout)
        self.sliders_list=self.main_window_class.sliderlist#,self.main_window_class.slider2,self.main_window_class.slider3,self.main_window_class.slider4,self.main_window_class.slider5,self.main_window_class.slider6,self.main_window_class.slider7,self.main_window_class.slider8,self.main_window_class.slider9,self.main_window_class.slider10] #(0+1)*1/(self.Ts*2*10)
        #i=0
        #fl=True
        #for slider_count in range(0,len(self.sliders_list)):
        #    print(slider_count)
        #    s= self.sliders_list[slider_count]
#
        #    s.valueChanged[int].connect(lambda value: print(s.objectName()) )#self.gain(value,slider_count/(self.Ts*2*10),(slider_count+1)/(self.Ts*2*10)))
        #slider_count=0
        #    #print(slider_count)
        #    #self.sliders_list[slider_count].valueChanged
        #fl=False    
        #self.main_window_class.s1.slider1.valueChanged[int].connect(lambda value: self.gain(value,0,1/(self.Ts*2*10)))
        #self.main_window_class.slider2.valueChanged[int].connect(lambda value: self.gain(value,1/(self.Ts*2*10),2/(self.Ts*2*10)))
        #self.main_window_class.slider3.valueChanged[int].connect(lambda value: self.gain(value,2/(self.Ts*2*10)/10,3/(self.Ts*2*10)))
        #self.main_window_class.slider4.valueChanged[int].connect(lambda value: self.gain(value,3/(self.Ts*2*10),4/(self.Ts*2*10)))
        #self.main_window_class.slider5.valueChanged[int].connect(lambda value: self.gain(value,4/(self.Ts*2*10),5/(self.Ts*2*10)))
        #self.main_window_class.slider6.valueChanged[int].connect(lambda value: self.gain(value,5/(self.Ts*2*10),6/(self.Ts*2*10)))
        #self.main_window_class.slider7.valueChanged[int].connect(lambda value: self.gain(value,6/(self.Ts*2*10),7/(self.Ts*2*10)))
        #self.main_window_class.slider8.valueChanged[int].connect(lambda value: self.gain(value,7/(self.Ts*2*10),8/(self.Ts*2*10)))
        #self.main_window_class.slider9.valueChanged[int].connect(lambda value: self.gain(value,8/(self.Ts*2*10),9/(self.Ts*2*10)))
        #self.main_window_class.slider10.valueChanged[int].connect(lambda value: self.gain(value,9/(self.Ts*2*10),10/(self.Ts*2*10)))
        self.main_window_class.combobox_color.currentTextChanged.connect(self.spectrograph)
        self.main_window_class.combobox_interval.currentTextChanged.connect(self.change_interval)
        self.main_window_class.minimum_slider.sliderReleased.connect(self.spectrograph)
        self.main_window_class.max_freq_slider.sliderReleased.connect(self.spectrograph)
        #self.main_window_class.actionOpen_csv.triggered.connect(self.imp_csv)
        self.main_window_class.actionexport_pdf.triggered.connect(self.report)
        self.main_window_class.scrol_slider.valueChanged[int].connect(self.sl)
        self.main_window_class.actionOpen_WAV.triggered.connect(self.imp_audio)
        #self.main_window_class.apply.clicked.connect(self.apply_lim)
    def change_interval(self):
        #self.play_back()
        import time
        self.flag_start_stop=True
        self.interval_value=int(self.main_window_class.combobox_interval.currentText())
        #time.sleep(1)
        #self.flag_start_stop=False
        #time.sleep(1)
        self.play_back()

    def open_newwindow(self):
        child_window()
    def plot_time_domain(self,a=0.05,b=0.05):
        self.main_window_class.scrol_slider.setValue(self.frame_counter)
        range_min=2*int(((self.frame_counter-self.size_per_frame)+abs(self.frame_counter-self.size_per_frame))/2)
        range_max=2*self.frame_counter
        x=self.time[range_min:range_max]
        ya=self.amplitude_original[range_min:range_max]
        yb=np.real(self.amplitude_copy[range_min:range_max])
        self.main_window_class.fig.clear()
        self.main_window_class.fig.subplots(2,1,sharex=True)
        ax=self.main_window_class.fig.axes[0]
        ax2=self.main_window_class.fig.axes[1]
        ax.cla()
        ax2.cla()
        ax.margins(x=a,y=b)
        ax.grid(True)
        ax.set_facecolor((0.29,0.29,0.29))
        ax2.margins(x=a,y=b)
        ax2.set_facecolor((0.29,0.29,0.29))
        ax2.grid(True)
        if a==b:
            ax.set_ylim(min(self.amplitude_original),max(self.amplitude_original))
            if min(np.real(self.amplitude_copy)) == max(np.real(self.amplitude_copy)):
                ax2.set_ylim(min(self.amplitude_original),max(self.amplitude_original))
            else:
                ax2.set_ylim(min(np.real(self.amplitude_copy)),max(np.real(self.amplitude_copy)))
        ax.plot(x,ya,"yellow")
        ax2.plot(x,yb,"yellow")
        self.main_window_class.fig.canvas.draw()                
        self.main_window_class.fig.canvas.flush_events()
    
    def spectrograph(self,processing=0):
        from scipy import signal
        from scipy.fft import fftshift
        import matplotlib.pyplot as plt
        lista=[plt]
        self.main_window_class.fig_spectrogram.clear()
        self.cmap_color = self.main_window_class.combobox_color.currentText()
        ax1 = self.main_window_class.fig_spectrogram.add_subplot(111)
        #scipy.signal.spectrogram(np.real(self.amplitude_copy), fs=1/self.Ts, window='tukey', 0.25, nperseg=None, noverlap=None, nfft=None, detrend='constant', return_onesided=True, scaling='density', axis=- 1, mode='psd')
        #ax1.specgram(np.real(self.amplitude_copy), Fs=1/self.Ts,cmap=self.cmap_color , NFFT=256, noverlap=256/2,)        
        #if self.main_window_class.minimum_slider.value()/self.duration<self.main_window_class.max_freq_slider.value()/self.duration:
        #    ax1.set_ylim(self.main_window_class.minimum_slider.value()/self.duration,self.main_window_class.max_freq_slider.value()/self.duration)
        #self.main_window_class.fig_spectrogram.canvas.draw()
        f,t,DBS=self.dBS_calculation()
        if self.main_window_class.minimum_slider.value()>self.main_window_class.max_freq_slider.value():
            
            spectrogram=ax1.pcolormesh(t, f, DBS, shading='gouraud',cmap=self.cmap_color,vmin=np.min(DBS),vmax=np.max(DBS))
        else:
            spectrogram=ax1.pcolormesh(t, f, DBS, shading='gouraud',cmap=self.cmap_color,vmin=self.main_window_class.minimum_slider.value(),vmax=self.main_window_class.max_freq_slider.value())
        self.main_window_class.fig_spectrogram.colorbar(spectrogram)
        #print(self.main_window_class.minimum_slider.value(),self.main_window_class.max_freq_slider.value())
        self.main_window_class.fig_spectrogram.canvas.draw()
        self.main_window_class.fig_spectrogram.canvas.flush_events()
        if processing:
            if self.main_window_class.minimum_slider.value()>self.main_window_class.max_freq_slider.value():
                plt.pcolormesh(t, f, DBS, shading='gouraud',cmap=self.cmap_color,vmin=np.min(DBS),vmax=np.max(DBS))
            else:
                plt.pcolormesh(t, f, DBS, shading='gouraud',cmap=self.cmap_color,vmin=self.main_window_class.minimum_slider.value(),vmax=self.main_window_class.max_freq_slider.value())
    def variables(self):
        self.Ts = 0
        self.time = []                   
        self.amplitude_original = []
        self.amplitude_copy=0
        self.frequency_values=0
        self.frequency_values_copy=[]
        self.frequency_values_limits=[]
        self.frame_counter=25
        self.flag_start_stop=False
        self.cmap_color='spring'
        self.interval_value=50
        self.duration=0
        self.size_per_frame=25
    def dBS_calculation(self):
        f, t, Sxx = signal.spectrogram(np.real(self.amplitude_copy),1/self.Ts )
        #DBS=20*np.log10(Sxx)-40
        return f,t,Sxx
    def init(self):
        self.length_amp=len(self.amplitude_original)
        self.amplitude_copy=self.amplitude_original.copy()
        self.frequency_values=rfft(self.amplitude_original)
        self.frequency_values=np.array(self.frequency_values)
        DBS_VALUE=self.dBS_calculation()
        max_min_list_slider=[self.main_window_class.minimum_slider,self.main_window_class.max_freq_slider]
        self.initialize_max_min_sliders(DBS_VALUE[2],max_min_list_slider[0])
        self.initialize_max_min_sliders(DBS_VALUE[2],max_min_list_slider[1])
        self.main_window_class.minimum_slider.setValue(np.min(DBS_VALUE[2]))
        self.main_window_class.max_freq_slider.setValue(np.max(DBS_VALUE[2]))
        
        for i in range(0,len(self.frequency_values)):
            if np.abs(self.frequency_values[i])<1:
                self.frequency_values[i]=0
        self.frequency_values_copy=list(self.frequency_values).copy()
        self.frequency_values_limits=list(self.frequency_values).copy()
        self.main_window_class.scrol_slider.setMinimum(self.size_per_frame)
        self.main_window_class.scrol_slider.setMaximum(int(self.length_amp/2)-1)
    def initialize_max_min_sliders(self,DBS,slider):
        slider.setMinimum(np.min(DBS))
        slider.setMaximum(np.max(DBS))
    def imp_audio(self):
        self.variables()
        path_audio= QFileDialog.getOpenFileName(None, 'Open WAV ', '/home', "WAV (*.WAV)")[0]
        sampleRate, audioBuffer = scipy.io.wavfile.read(path_audio)
        self.Ts=1/sampleRate
        for i in range(0,len(audioBuffer)):
            self.amplitude_original.append(audioBuffer[i])
        self.time = np.arange(0,len(audioBuffer)*self.Ts,self.Ts)
        self.duration=len(audioBuffer)*self.Ts
        self.length_amp=len(self.amplitude_original)
        self.init()
        self.gain_ranges()
        self.play_back() 
    #def imp_csv(self):
    #    self.variables()
    #    path_csv = QFileDialog.getOpenFileName(None, 'Open CSV ', '/home', "CSV (*.csv)")[0]
    #    ds_ecg= pd.read_csv(path_csv)
    #    self.time=ds_ecg.iloc[0:-1,1].values
    #    self.amplitude_original=ds_ecg.iloc[0:-1,2].values
    #    self.Ts=ds_ecg.iloc[0:1,3].values
    #    dur_Rec=ds_ecg.iloc[0:1,4].values
    #    self.duration=float(dur_Rec)
    #    self.Ts=float(self.Ts)      
    #    self.length_amp=len(self.amplitude_original)
    #    self.init()
    #    self.gain_ranges()
    #    self.play_back()  
    def gain_ranges(self):
        for slider_count in range(10):
            self.sliders_list[slider_count].set_range((slider_count)/(self.Ts*2*10),(slider_count+1)/(self.Ts*2*10))
    def play_back(self):
        self.plot_time_domain()
        self.spectrograph()
        self.main_window_class.fig.clear()
        if self.flag_start_stop == False:
            self.flag_start_stop=True
            c=self.frame_counter
            lines_bef = [ax.plot([],[])[0] for ax in self.main_window_class.fig.axes]
            def update_bef(i):
                self.main_window_class.scrol_slider.setValue(self.frame_counter)
                if not self.flag_start_stop or self.frame_counter>=(int(self.length_amp/2)-self.size_per_frame):
                    self.ani_st_bef.event_source.stop()
                    self.main_window_class.fig.canvas.flush_events()
                    self.plot_time_domain()
                else:
                    self.frame_counter=i+c
                    self.plot_time_domain()
                self.main_window_class.fig.canvas.flush_events()
                return lines_bef
            self.ani_st_bef = FuncAnimation(self.main_window_class.fig, update_bef,interval=int(self.main_window_class.combobox_interval.currentText()),frames=np.arange(0,int((self.length_amp/2))-25),blit=True,repeat=False)
        else:
            self.flag_start_stop=False
    def backword(self):
        if self.frame_counter>self.size_per_frame+10:
            self.frame_counter=self.frame_counter-10
            self.plot_time_domain()
        else:
            print("no enough points")
    def forword(self):
        if self.frame_counter<(self.length_amp/2-10):
            self.frame_counter=self.frame_counter+10
            self.plot_time_domain()
        else:
            print("no enough points")
    def zoomin(self):
        self.plot_time_domain(-0.3,0.05)
    def zoomout(self):
        self.plot_time_domain(0.05,1)

    def gain_calculation(self,i,value):
        self.frequency_values_copy[i]=self.frequency_values[i]*value
    
    def gain(self,value,minim,maxim): 
        fr=rfftfreq(self.length_amp,self.Ts)
        minimum_index=int(minim*self.duration)
        #if maxim==1/(self.Ts*2):
        #    print("true")
        #    print(value)
        #    for i in range (minimum_index,len(self.frequency_values_copy)):
        #        self.gain_calculation(i,value)
        #else:
        maximum_index=int(maxim*self.duration)
        print(minimum_index,maximum_index)
        for i in range (minimum_index,maximum_index):
            self.gain_calculation(i,value)
        #plt.scatter(fr,np.abs(self.frequency_values_copy))
        #plt.show()
        #print(fr(int(maxim)))
        print(len(self.frequency_values_copy))
        self.frequency_values_copy[0]=0
        self.amplitude_copy=irfft(self.frequency_values_copy)
        self.spectrograph()
        self.plot_time_domain()
    def sl(self,value):
        if not self.flag_start_stop:
            self.frame_counter=value
            self.plot_time_domain()
    def report(self):
        fig=plt
        def Signalplot (a,b,c,d):
            plt.subplot(3, 1, 1)
            plt.title("before eq.")
            plt.xlabel('Time')
            plt.ylabel('self.amplitude_original')
            plt.plot(a, b)
            plt.subplot(3, 1, 2)
            plt.title("After eq.")
            plt.xlabel('Time')
            plt.ylabel('self.amplitude_original')
            plt.plot(a, c)
            plt.subplot(3, 1, 3)
            plt.title("Spectrogram")
            plt.xlabel('self.time')
            plt.ylabel('freq')
            #spectrogram_pdf=self.spectrograph(1)
            #f,t,DBS,pcolor=self.dBS_calculation()
            #plt.pcolormesh(t, f, DBS, shading='gouraud',cmap=self.cmap_color,vmin=self.main_window_class.minimum_slider.value(),vmax=self.main_window_class.max_freq_slider.value())
            self.spectrograph(1)
            #plt.specgram(np.real(c), Fs=1/self.Ts,cmap=d , NFFT=256, noverlap=256/2,)        
        Signalplot(self.time,self.amplitude_original,self.amplitude_copy,self.cmap_color)
        fig.tight_layout()
        plt.savefig('C:/Users/abdoz/Downloads/Task eq/Report_2_Team_2.pdf')
def window():
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())
    return win

def child_window():
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    ases=window()
