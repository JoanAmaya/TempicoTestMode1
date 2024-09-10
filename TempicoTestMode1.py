import numpy as np
import matplotlib.pyplot as plt
import pyTempico as tempico
import time

class TestModeOneTempico():
    def __init__(self):
        self.sentinelRunning=False
        try:
            self.device=tempico.TempicoDevice('COM35')    
            self.device.open()
            self.sentinelRunning=True
        except:
            self.sentinelRunning=False
            
        if(self.sentinelRunning):
            #Create sentinel of Continue Measurement
            self.finishMeasurement=False
            #Enable all channels
            self.device.ch1.enableChannel()
            self.device.ch2.disableChannel()
            self.device.ch3.disableChannel()
            self.device.ch4.disableChannel()
            
            #Create the data for the labels
            self.histogramValue=[]
            self.numberRuns=100
            self.device.setNumberOfRuns(self.numberRuns)
            self.device.setThresholdVoltage(1.6)
            #Set the mode One for the channels
            self.device.ch1.setMode(1)
            self.device.ch2.setMode(1)
            self.device.ch3.setMode(1)
            self.device.ch4.setMode(1)
            #Set the number of stops
            self.device.ch1.setNumberOfStops(1)
            self.device.ch2.setNumberOfStops(1)
            self.device.ch3.setNumberOfStops(1)
            self.device.ch4.setNumberOfStops(1)
            #Set the stop mask
            self.device.ch1.setStopMask(0)
            self.device.ch2.setStopMask(0)
            self.device.ch3.setStopMask(0)
            self.device.ch4.setStopMask(0)
            #Start the measurement
            while( not self.finishMeasurement):
                self.takeMeasure()
            #Get the average of the measurement
            average=self.averageMeasurements()
            unitsMultiplier=self.getUnits(average)
            print('The average value is:')
            newValue=round(average/unitsMultiplier[1],2)
            print(str(newValue)+' '+unitsMultiplier[0])
            #Normalized Values
            self.normalizeValues(unitsMultiplier[1])
            #Graph the histogram with the values
            self.createHistogram(unitsMultiplier[0])
            #Show the settings of Tempico Device
            print('The settings of the device are: ')
            print(self.device.getSettings())
            
            #Enable the channels after take measurement
            self.device.ch1.enableChannel()
            self.device.ch2.enableChannel()
            self.device.ch3.enableChannel()
            self.device.ch4.enableChannel()
            
        else:
            print('Check if the device is being using for another software or if the COM port in the line 10 is correct')
    
    def takeMeasure(self):
        for i in range(100):
        
            print('Measure number '+str(i+1))
            measure=self.device.measure()
            print(measure)
            if len(measure)!=0:
                for i in measure:
                    #Is only One stop so the value of the measurement will be the index 3
                    if(len(i)==4):
                        currentValue=i[3]
                        if currentValue!=-1:
                            self.histogramValue.append(currentValue)
        print(len(self.histogramValue))
        if len(self.histogramValue)>=100:
            self.finishMeasurement=True
        else:
            print('The measurement could not be completed, check the device connections or the data source')
            exitOrNot=input('Write 1 if you want to continue or write anything if you want to exit')
            if exitOrNot=='1':
                print('Starting a new measurement...')
                time.sleep(2)
            else:
                print("Leaving test...")
                time.sleep(2)
                self.finishMeasurement=True
    
    #Get the average of the measurements
    def averageMeasurements(self):
        totalCumSum=sum(self.histogramValue)
        totalLen=len(self.histogramValue)
        average=round(totalCumSum/totalLen)
        print('Time Average value in picoseconds is:')
        print(average)
        return average

    def getUnits(self,picosecondsValue):
        if picosecondsValue < 1e3:
            return ["ps",1]
        elif picosecondsValue < 1e6:
            return ["ns",10**3]
        elif picosecondsValue < 1e9:
            return ["µs",10**6]
        elif picosecondsValue < 1e12:
            return ["ms",10**9]
    
    def createHistogram(self,units):
        #hist,_=np.histogram(self.correctUnitsValues,bins=200)
        plt.hist(self.correctUnitsValues, bins=200)
        plt.xlabel('Time ('+units+')')
        plt.ylabel('Frequency')
        plt.title('Histogram')
        plt.savefig('HistogramMode1.png')
        plt.show()
        
        
    def normalizeValues(self,divFactor):
        self.correctUnitsValues=[]
        for i in self.histogramValue:
            newValue=round(i/divFactor,2)
            self.correctUnitsValues.append(newValue)
        


objectTest=TestModeOneTempico()
        
    
    