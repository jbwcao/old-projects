from gpiozero import Button
import bme280, smbus2, glob
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class BME280:
	def __init__(self):
		self.port = 1
		self.address = 0x77 # Adafruit BME280 address
		self.bus = smbus2.SMBus(self.port)
		
	def start(self):
		bme280.load_calibration_params(self.bus,self.address)
		
		print("BME280 on (air temperature, humidity, pressure)")
		
	def output_humidity_pressure_temp(self):
		bme280_data = bme280.sample(self.bus,self.address)
		
		humidity = bme280_data.humidity
		pressure = bme280_data.pressure
		temperature = bme280_data.temperature
		
		return [humidity, pressure, temperature]

class DS18B20:
	def __init__(self):
		self.device_file = glob.glob('/sys/bus/w1/devices/28*')[0] + '/w1_slave'
		self.lines = self.extract_data(self.device_file)
		
	def check_working(self):
		if "YES" == self.lines[0].strip()[-3:]: #YODA CONDITION POG
			print("DS1820 on (ground temperature)")
			
			return True
		else:
			print("Error: Check DS1820(ground temperature)")
			
			return False
			
	def output_ground_temp(self):
		self.lines = self.extract_data(self.device_file)
		index_pos = self.lines[1].find('t=')
		
		if index_pos != -1:
			ground_temp_string = self.lines[1][index_pos + 2:]
			
			
			return float(ground_temp_string)/1000
			
	def extract_data(self,path):
		with open(path, 'r') as f:
			return f.readlines()
			
class Anemometer:
	
	def __init__(self, radius, button):
		self.vane = Button(button)
		self.radius = radius
		self.previous_revolutions = 0
		self.revolutions = 0
		self.time = time.perf_counter()
		self.windspeed = 0
		
	def revolution_completed(self):
		self.revolutions += 1
		
	def get_reading(self):
		#print(f'{self.windspeed} m/s, {self.windspeed * 2.237} mph')
		self.windspeed = (1 / (time.perf_counter() - self.time)) * 2 * 3.14159 * self.radius * (self.revolutions - self.previous_revolutions)
		self.time = time.perf_counter()
		self.previous_revolutions = self.revolutions
		return self.windspeed

		
def main():
	time_counter = 0
	anemo_list = []
	temp_list = []
	ground_temp_list = []
	pressure_list = []
	humidity_list = []
	time_data = [0]
	
	bme280_sensor = BME280()
	ds18b20_sensor = DS18B20()
	anemometer = Anemometer(.09,6)
	
	bme280_sensor.start()
	ds18b20_sensor.check_working()
	
	anemometer.vane.when_pressed = anemometer.revolution_completed
	
	def update(frame):
		
		BME_info = bme280_sensor.output_humidity_pressure_temp()
		ground_temp = ds18b20_sensor.output_ground_temp()
		wind_speed = anemometer.get_reading()
				
		anemo_list.append(wind_speed)
		temp_list.append(BME_info[2])
		ground_temp_list.append(ground_temp)
		pressure_list.append(BME_info[1])
		humidity_list.append(BME_info[0])
		
		if 10 < len(anemo_list):
			anemo_list.pop(0)
			temp_list.pop(0)
			ground_temp_list.pop(0)
			pressure_list.pop(0)
			humidity_list.pop(0)
			
		ax_temp.clear()
		ax_temp.plot(time_data, temp_list)

		ax_anemo.clear()
		ax_anemo.plot(time_data, anemo_list)
		
		ax_ground.clear()
		ax_ground.plot(time_data, ground_temp_list)
		
		ax_pressure.clear()
		ax_pressure.plot(time_data, pressure_list)
		
		ax_humidity.clear()
		ax_humidity.plot(time_data, humidity_list)
		
		ax_nothing.clear()
		ax_nothing.plot(time_data, [0 for i in range(len(time_data))])
		
		ax_anemo.set_title('wind speed (m/s)')
		ax_temp.set_title('temperature (C)')
		ax_ground.set_title('ground temperature (C)')
		ax_humidity.set_title('humidity (%)')
		ax_pressure.set_title('pressure (hPa)')
		ax_nothing.set_title('precipitation')
		
		fig.suptitle('Weather Data')
		
		print(anemo_list,temp_list,ground_temp_list,pressure_list,humidity_list)
		
		time_data.append(time_data[-1] + 1)
		if 10 < len(time_data):
			time_data.pop(0)
		
		'''
		print(f'Cycle {time_counter}')
		print(f'Humidity: {BME_info[0]} %')
		print(f'Pressure: {BME_info[1]} Hectopascals')
		print(f'Temperature: {BME_info[2]} Celsius / {BME_info[2] * (9/5) +32} Fahrenheit')
		print(f'Ground Temperature: {ground_temp} Celsius / {ground_temp * (9/5) + 32} Fahrenheit')
		print()
		'''
		
	fig, axs = plt.subplots(3, 2)
	ax_anemo, ax_temp, ax_ground, ax_humidity, ax_pressure, ax_nothing = axs.flatten()

	animation_temp = FuncAnimation(fig, update, frames=range(100), interval=1000)
	plt.tight_layout()
	plt.show()

if __name__ == '__main__':
	main()
