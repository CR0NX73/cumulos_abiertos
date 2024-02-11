import numpy as np
from tabulate import tabulate
import re
from pyfiglet import Figlet
import sys
from scipy.integrate import quad


def main():
    figlet = Figlet()
    output_title = figlet.setFont(font='big')
    output_title= figlet.renderText('Magnitud aparente en estrellas')
    print(f"{output_title}")
    get_temperatures()

def get_temperatures():
    print("ADVERTENCIA: Las temperaturas se deben encontrar en el rango de 3.000 K a 50.000 K")
    intentos=3
    for i in range(3):
        while True:
            try:
                temperature = input(f"Ingrese la temperatura {i+1} en grados Kelvin (K): ")
                temperature_info = black_body(temperature)
                data_table=[["Filtro", f"Magnitud a temperatura: {temperature} K"], 
                            ["Ultravioleta (U)", temperature_info.ultraviolet()],
                            ["Blue (B)", temperature_info.blue()],
                            ["Visual (V)", temperature_info.visual()]]
                print(tabulate(data_table[1:], data_table[0], tablefmt="grid"))
                break
            except ValueError:
                intentos-=1
                if intentos > 0:
                    print("\nTemperatura inválida, intente nuevamente")
                    print(f"\nTiene {intentos} intento(s) restante(s)\n")
                elif intentos == 0:
                    sys.exit("Se ha excedido el número de intentos")
                continue


class black_body():
    def __init__(self, temperature):
        self.temperature = temperature
        self.limits_ultraviolet = (299e-9, 431e-9)
        self.limits_blue = (351e-9,529e-9)
        self.limits_visual = (463e-9,639e-9)
        self.F0 = 1361 #W/m^2
        self.MUBV = [-25.97, -26.13, -26.76]

    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, temperature):
        temperature = temperature.strip()
        if re.search(r"^[0-9]*$", temperature):
                temperature=int(temperature)
                if temperature >= 3000 and temperature <= 50000:
                    self._temperature = temperature
                else:
                    raise ValueError
        else:
            raise ValueError
        
    def intensity(self, wavelength):
        c = 3e8 # Speed of light
        h = 6.62607015e-34 # Planck's constant
        kb = 1.380649e-23 # Boltzmann's constant
        return 2*h*c**2/(wavelength**5*(np.exp(h*c/(kb*self.temperature*wavelength))-1))
    
    def absolute_magnitude(self, limits):
        match limits:
            case "ultraviolet":
                integral, error = quad(self.intensity, self.limits_ultraviolet[0], self.limits_ultraviolet[1])
                M0 = self.MUBV[0]
            case "blue":
                integral, error = quad(self.intensity, self.limits_blue[0], self.limits_blue[1])
                M0 = self.MUBV[1]
            case "visual":
                integral, error = quad(self.intensity, self.limits_visual[0], self.limits_visual[1])
                M0 = self.MUBV[2]
        return -2.5*np.log10(np.pi*integral/self.F0) + M0
    
    def ultraviolet(self, d = 10):
        Mu = self.absolute_magnitude("ultraviolet")
        return 5*np.log10(d) -5 + Mu
    
    def blue(self, d = 10):
        Mb = self.absolute_magnitude("blue")
        return 5*np.log10(d) -5 + Mb

    def visual(self, d = 10):
        Mv = self.absolute_magnitude("visual")
        return 5*np.log10(d) -5 + Mv


if __name__=='__main__':
    main()